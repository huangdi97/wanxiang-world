"""T3 spatial jobs are idempotent, restart-safe and projection-only."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import pathlib
from dataclasses import dataclass, field

import pytest
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_jobs import (
    _DerivedSpatialAttachments,
    _InMemorySpatialJobStore,
    _LocalJsonSpatialJobStore,
    _SpatialGenerationCoordinator,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.assets.storage import InMemoryObjectStore, LocalObjectStore


def _glb(payload: bytes = b"scene") -> bytes:
    total_length = 12 + len(payload)
    return b"glTF" + (2).to_bytes(4, "little") + total_length.to_bytes(4, "little") + payload


def _request() -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name="机关桥",
        stable_key="bridge",
        spec=SemanticSceneSpec(
            spec_id="scene-bridge",
            semantic_id="place:bridge",
            kind="illustrated-environment",
        ),
        cache_key="cache-bridge",
        style_key="story-style",
    )


@dataclass
class _FakeSpatialProvider(_SpatialGenerationProvider):
    provider_id: str = "spatial:test"
    provider_version: str = "2026-10"
    requires_network: bool = True
    private_safe: bool = False
    cost_units_per_job: int = 7
    allowed_media_types: frozenset[str] = frozenset({"model/gltf-binary"})
    submissions: list[str] = field(default_factory=lambda: list[str]())
    polls: list[_SpatialPollResult] = field(default_factory=lambda: list[_SpatialPollResult]())

    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        _ = request
        self.submissions.append(idempotency_key)
        return f"task:{len(self.submissions)}"

    def poll(self, task_ref: str) -> _SpatialPollResult:
        _ = task_ref
        return self.polls.pop(0)


def _coordinator(provider: _FakeSpatialProvider) -> _SpatialGenerationCoordinator:
    return _SpatialGenerationCoordinator(provider)


def _submit(coordinator: _SpatialGenerationCoordinator):
    return coordinator.submit(
        _request(),
        allow_network=True,
        external_processing_allowed=True,
        private_source=False,
        max_cost_units=7,
        delivery_rights="source-gated",
    )


def test_t3_submission_is_idempotent_before_billing_or_network_retry() -> None:
    provider = _FakeSpatialProvider()
    coordinator = _coordinator(provider)

    first = _submit(coordinator)
    replay = _submit(coordinator)

    assert first == replay
    assert len(provider.submissions) == 1
    assert first.reserved_cost_units == 7
    assert not hasattr(coordinator, "commit")
    assert not hasattr(coordinator, "apply")


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"allow_network": False}, "network permission"),
        ({"external_processing_allowed": False}, "source rights"),
        ({"private_source": True}, "private-safe"),
        ({"max_cost_units": 6}, "reserved budget"),
        ({"delivery_rights": "public"}, "rights do not match"),
    ],
)
def test_t3_existing_ticket_still_obeys_current_governance(
    kwargs: dict[str, object],
    message: str,
) -> None:
    provider = _FakeSpatialProvider()
    coordinator = _coordinator(provider)
    _submit(coordinator)
    options: dict[str, object] = {
        "allow_network": True,
        "external_processing_allowed": True,
        "private_source": False,
        "max_cost_units": 7,
        "delivery_rights": "source-gated",
    }
    options.update(kwargs)

    with pytest.raises(ValueError, match=message):
        coordinator.submit(_request(), **options)  # type: ignore[arg-type]

    assert len(provider.submissions) == 1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"allow_network": False}, "network permission"),
        ({"external_processing_allowed": False}, "source rights"),
        ({"private_source": True}, "private-safe"),
        ({"max_cost_units": 6}, "reserved budget"),
    ],
)
def test_t3_governance_blocks_new_submission_before_provider_call(
    kwargs: dict[str, object],
    message: str,
) -> None:
    provider = _FakeSpatialProvider()
    coordinator = _coordinator(provider)
    options: dict[str, object] = {
        "allow_network": True,
        "external_processing_allowed": True,
        "private_source": False,
        "max_cost_units": 7,
        "delivery_rights": "source-gated",
    }
    options.update(kwargs)
    with pytest.raises(ValueError, match=message):
        coordinator.submit(_request(), **options)  # type: ignore[arg-type]
    assert provider.submissions == []


def test_t3_ticket_survives_restart_and_resumes_existing_provider_task(
    tmp_path: pathlib.Path,
) -> None:
    provider = _FakeSpatialProvider()
    jobs_path = tmp_path / "spatial-jobs.json"
    first = _SpatialGenerationCoordinator(
        provider,
        jobs=_LocalJsonSpatialJobStore(jobs_path),
        objects=LocalObjectStore(tmp_path / "objects"),
    )
    submitted = _submit(first)

    restarted = _SpatialGenerationCoordinator(
        provider,
        jobs=_LocalJsonSpatialJobStore(jobs_path),
        objects=LocalObjectStore(tmp_path / "objects"),
    )
    resumed = _submit(restarted)

    assert resumed == submitted
    assert len(provider.submissions) == 1
    assert resumed.provider_task_ref == "task:1"


def test_t3_poll_verifies_assets_then_attaches_only_to_derived_catalog() -> None:
    payload = _glb()
    provider = _FakeSpatialProvider(
        polls=[
            _SpatialPollResult("running"),
            _SpatialPollResult(
                "succeeded",
                (
                    _SpatialArtifactCandidate(
                        payload,
                        "model/gltf-binary",
                        hashlib.sha256(payload).hexdigest(),
                    ),
                ),
            ),
        ]
    )
    coordinator = _coordinator(provider)
    ticket = _submit(coordinator)

    running = coordinator.poll(ticket.submission_id)
    verified = coordinator.poll(ticket.submission_id)
    catalog = _DerivedSpatialAttachments()
    attached = coordinator.attach(ticket.submission_id, catalog)

    assert running.state == "running"
    assert verified.state == "verified"
    assert len(verified.asset_refs) == 1
    assert verified.asset_refs[0].rights == "source-gated"
    assert attached.state == "attached"
    assert catalog.get("bridge") == attached.asset_refs
    assert not hasattr(catalog, "commit")
    assert not hasattr(catalog, "worldline")


@pytest.mark.parametrize(
    "candidate",
    [
        _SpatialArtifactCandidate(b"bad", "text/html", hashlib.sha256(b"bad").hexdigest()),
        _SpatialArtifactCandidate(b"bad", "model/gltf-binary", "0" * 64),
        _SpatialArtifactCandidate(b"", "model/gltf-binary", hashlib.sha256(b"").hexdigest()),
    ],
)
def test_t3_completed_task_fails_closed_when_artifact_verification_fails(
    candidate: _SpatialArtifactCandidate,
) -> None:
    provider = _FakeSpatialProvider(polls=[_SpatialPollResult("succeeded", (candidate,))])
    coordinator = _coordinator(provider)
    ticket = _submit(coordinator)

    failed = coordinator.poll(ticket.submission_id)

    assert failed.state == "failed"
    assert failed.reason == "artifact_verification_failed"
    assert failed.asset_refs == ()


def test_t3_restart_refuses_to_poll_a_ticket_with_another_provider() -> None:
    first_provider = _FakeSpatialProvider()
    jobs = _InMemorySpatialJobStore()
    first = _SpatialGenerationCoordinator(first_provider, jobs=jobs)
    ticket = _submit(first)

    replacement_provider = _FakeSpatialProvider(
        provider_id="spatial:replacement",
        provider_version="2026-11",
    )
    restarted = _SpatialGenerationCoordinator(replacement_provider, jobs=jobs)

    with pytest.raises(ValueError, match="does not match persisted ticket"):
        restarted.poll(ticket.submission_id)

    assert replacement_provider.polls == []


def test_t3_known_spatial_formats_require_matching_file_signatures() -> None:
    provider = _FakeSpatialProvider(
        allowed_media_types=frozenset({"model/gltf-binary", "application/x-ply", "image/png"})
    )
    coordinator = _coordinator(provider)
    candidates = (
        _SpatialArtifactCandidate(
            b"not-a-glb",
            "model/gltf-binary",
            hashlib.sha256(b"not-a-glb").hexdigest(),
        ),
        _SpatialArtifactCandidate(
            b"not-ply",
            "application/x-ply",
            hashlib.sha256(b"not-ply").hexdigest(),
        ),
        _SpatialArtifactCandidate(
            b"<html>not-png</html>",
            "image/png",
            hashlib.sha256(b"<html>not-png</html>").hexdigest(),
        ),
    )

    for candidate in candidates:
        provider.polls = [_SpatialPollResult("succeeded", (candidate,))]
        ticket = _submit(coordinator)
        failed = coordinator.poll(ticket.submission_id)
        assert failed.state == "failed"
        assert failed.reason == "artifact_verification_failed"
        coordinator.jobs = _InMemorySpatialJobStore()


def test_t3_unknown_spatial_media_type_fails_closed_even_if_provider_allows_it() -> None:
    payload = b"vendor-binary"
    provider = _FakeSpatialProvider(
        allowed_media_types=frozenset({"application/octet-stream"}),
        polls=[
            _SpatialPollResult(
                "succeeded",
                (
                    _SpatialArtifactCandidate(
                        payload,
                        "application/octet-stream",
                        hashlib.sha256(payload).hexdigest(),
                    ),
                ),
            )
        ],
    )
    coordinator = _coordinator(provider)
    ticket = _submit(coordinator)

    failed = coordinator.poll(ticket.submission_id)

    assert failed.state == "failed"
    assert failed.reason == "artifact_verification_failed"
    assert failed.asset_refs == ()


def test_attached_t3_ticket_rehydrates_derived_catalog_after_restart(
    tmp_path: pathlib.Path,
) -> None:
    payload = _glb(b"restart")
    provider = _FakeSpatialProvider(
        polls=[
            _SpatialPollResult(
                "succeeded",
                (
                    _SpatialArtifactCandidate(
                        payload,
                        "model/gltf-binary",
                        hashlib.sha256(payload).hexdigest(),
                    ),
                ),
            )
        ]
    )
    jobs_path = tmp_path / "spatial-jobs.json"
    objects_path = tmp_path / "objects"
    first = _SpatialGenerationCoordinator(
        provider,
        jobs=_LocalJsonSpatialJobStore(jobs_path),
        objects=LocalObjectStore(objects_path),
    )
    submitted = _submit(first)
    verified = first.poll(submitted.submission_id)
    first_catalog = _DerivedSpatialAttachments()
    attached = first.attach(verified.submission_id, first_catalog)

    restarted = _SpatialGenerationCoordinator(
        provider,
        jobs=_LocalJsonSpatialJobStore(jobs_path),
        objects=LocalObjectStore(objects_path),
    )
    restored_catalog = _DerivedSpatialAttachments()
    restored = restarted.attach(attached.submission_id, restored_catalog)

    assert restored == attached
    assert restored_catalog.get("bridge") == attached.asset_refs
    assert len(provider.submissions) == 1


def test_t3_terminal_failure_never_attaches_assets() -> None:
    provider = _FakeSpatialProvider(
        polls=[_SpatialPollResult("failed", reason="provider task failed")]
    )
    coordinator = _coordinator(provider)
    ticket = _submit(coordinator)

    failed = coordinator.poll(ticket.submission_id)

    assert failed.state == "failed"
    with pytest.raises(ValueError, match="only verified"):
        coordinator.attach(ticket.submission_id, _DerivedSpatialAttachments())

def test_t3_batch_verification_writes_nothing_when_any_artifact_is_invalid() -> None:
    class _CountingStore(InMemoryObjectStore):
        def __init__(self) -> None:
            super().__init__()
            self.put_calls = 0

        def put(self, blob: bytes, *, content_type: str, rights: str = "public"):
            self.put_calls += 1
            return super().put(blob, content_type=content_type, rights=rights)

    valid = _glb(b"valid")
    invalid = b"not-a-glb"
    provider = _FakeSpatialProvider(
        polls=[
            _SpatialPollResult(
                "succeeded",
                (
                    _SpatialArtifactCandidate(
                        valid,
                        "model/gltf-binary",
                        hashlib.sha256(valid).hexdigest(),
                    ),
                    _SpatialArtifactCandidate(
                        invalid,
                        "model/gltf-binary",
                        hashlib.sha256(invalid).hexdigest(),
                    ),
                ),
            )
        ]
    )
    objects = _CountingStore()
    coordinator = _SpatialGenerationCoordinator(provider, objects=objects)
    ticket = _submit(coordinator)

    failed = coordinator.poll(ticket.submission_id)

    assert failed.state == "failed"
    assert failed.asset_refs == ()
    assert objects.put_calls == 0
