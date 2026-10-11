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
    _LocalJsonSpatialJobStore,
    _SpatialGenerationCoordinator,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.assets.storage import LocalObjectStore


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
    replay = coordinator.submit(
        _request(),
        allow_network=False,
        external_processing_allowed=False,
        private_source=True,
        max_cost_units=0,
        delivery_rights="source-gated",
    )

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
    payload = b"glTF-binary-test"
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
