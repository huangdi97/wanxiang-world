"""Restart-safe T3 spatial generation without any Canon/History write authority."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

import hashlib
import json
import pathlib
from dataclasses import replace
from typing import cast

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
    _SpatialJobStore,
    _SpatialPollResult,
)
from wanxiang_substrate.assets.storage import (
    AssetRef,
    InMemoryObjectStore,
    ObjectStore,
)


class _InMemorySpatialJobStore(_SpatialJobStore):
    def __init__(self) -> None:
        self._rows: dict[str, _SpatialGenerationTicket] = {}

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        return self._rows.get(submission_id)

    def put(self, ticket: _SpatialGenerationTicket) -> None:
        self._rows[ticket.submission_id] = ticket


class _LocalJsonSpatialJobStore(_SpatialJobStore):
    """Single-filesystem durable ticket store for restart-safe task resumption."""

    def __init__(self, path: pathlib.Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _asset(data: dict[str, object]) -> AssetRef:
        return AssetRef(
            asset_id=cast(str, data["asset_id"]),
            content_hash=cast(str, data["content_hash"]),
            size=cast(int, data["size"]),
            content_type=cast(str, data["content_type"]),
            rights=cast(str, data["rights"]),
        )

    @classmethod
    def _ticket(cls, data: dict[str, object]) -> _SpatialGenerationTicket:
        raw_assets = data.get("asset_refs", [])
        assets = tuple(
            cls._asset(cast(dict[str, object], item))
            for item in cast(list[object], raw_assets)
            if isinstance(item, dict)
        )
        return _SpatialGenerationTicket(
            submission_id=cast(str, data["submission_id"]),
            scene_key=cast(str, data["scene_key"]),
            provider_id=cast(str, data["provider_id"]),
            provider_version=cast(str, data["provider_version"]),
            provider_task_ref=cast(str, data["provider_task_ref"]),
            state=cast(object, data["state"]),  # type: ignore[arg-type]
            reserved_cost_units=cast(int, data["reserved_cost_units"]),
            delivery_rights=cast(str, data["delivery_rights"]),
            asset_refs=assets,
            reason=cast(str, data.get("reason", "")),
        )

    def _rows(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("spatial job store must contain an object")
        return {
            key: cast(dict[str, object], value)
            for key, value in cast(dict[object, object], decoded).items()
            if isinstance(key, str) and isinstance(value, dict)
        }

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        with _exclusive_index_lock(self._path.with_suffix(".lock")):
            row = self._rows().get(submission_id)
            return self._ticket(row) if row is not None else None

    def put(self, ticket: _SpatialGenerationTicket) -> None:
        lock_path = self._path.with_suffix(".lock")
        with _exclusive_index_lock(lock_path):
            rows = self._rows()
            rows[ticket.submission_id] = {
                "submission_id": ticket.submission_id,
                "scene_key": ticket.scene_key,
                "provider_id": ticket.provider_id,
                "provider_version": ticket.provider_version,
                "provider_task_ref": ticket.provider_task_ref,
                "state": ticket.state,
                "reserved_cost_units": ticket.reserved_cost_units,
                "delivery_rights": ticket.delivery_rights,
                "reason": ticket.reason,
                "asset_refs": [
                    {
                        "asset_id": ref.asset_id,
                        "content_hash": ref.content_hash,
                        "size": ref.size,
                        "content_type": ref.content_type,
                        "rights": ref.rights,
                    }
                    for ref in ticket.asset_refs
                ],
            }
            temporary = self._path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(rows, sort_keys=True, separators=(",", ":")),
                encoding="utf-8",
            )
            temporary.replace(self._path)


class _DerivedSpatialCatalog:
    """Projection-only scene attachments; deliberately has no canonical writer."""

    def __init__(self) -> None:
        self._rows: dict[str, tuple[AssetRef, ...]] = {}

    def attach(self, scene_key: str, asset_refs: tuple[AssetRef, ...]) -> None:
        self._rows[scene_key] = asset_refs

    def get(self, scene_key: str) -> tuple[AssetRef, ...]:
        return self._rows.get(scene_key, ())


class _SpatialGenerationCoordinator:
    """Idempotent asynchronous T3 submission/poll/verify/attach coordinator."""

    def __init__(
        self,
        provider: _SpatialGenerationProvider,
        *,
        jobs: _SpatialJobStore | None = None,
        objects: ObjectStore | None = None,
        max_asset_bytes: int = 128 * 1024 * 1024,
    ) -> None:
        self.provider = provider
        self.jobs = jobs or _InMemorySpatialJobStore()
        self.objects = objects or InMemoryObjectStore()
        self.max_asset_bytes = max_asset_bytes

    def _submission_id(self, request: _SourceSceneRequest) -> str:
        identity = (
            f"{request.cache_key}:t3-job-v1:"
            f"{self.provider.provider_id}@{self.provider.provider_version}"
        )
        return hashlib.sha256(identity.encode()).hexdigest()

    def submit(
        self,
        request: _SourceSceneRequest,
        *,
        allow_network: bool,
        external_processing_allowed: bool,
        private_source: bool,
        max_cost_units: int,
        delivery_rights: str,
    ) -> _SpatialGenerationTicket:
        submission_id = self._submission_id(request)
        existing = self.jobs.get(submission_id)
        if existing is not None:
            return existing
        if not self.provider.provider_id or not self.provider.provider_version:
            raise ValueError("spatial provider requires id and version")
        if self.provider.cost_units_per_job < 0 or max_cost_units < 0:
            raise ValueError("spatial cost values must be non-negative")
        if self.provider.requires_network and not allow_network:
            raise ValueError("spatial provider requires explicit network permission")
        if self.provider.requires_network and not external_processing_allowed:
            raise ValueError("source rights do not allow external spatial processing")
        if private_source and not self.provider.private_safe:
            raise ValueError("private source requires a private-safe spatial provider")
        if self.provider.cost_units_per_job > max_cost_units:
            raise ValueError("spatial provider cost exceeds reserved budget")

        task_ref = self.provider.submit(request, idempotency_key=submission_id)
        if not task_ref.strip():
            raise ValueError("spatial provider returned an empty task reference")
        ticket = _SpatialGenerationTicket(
            submission_id=submission_id,
            scene_key=request.stable_key,
            provider_id=self.provider.provider_id,
            provider_version=self.provider.provider_version,
            provider_task_ref=task_ref,
            state="submitted",
            reserved_cost_units=self.provider.cost_units_per_job,
            delivery_rights=delivery_rights,
        )
        self.jobs.put(ticket)
        return ticket

    def poll(self, submission_id: str) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state in {"verified", "attached", "failed", "cancelled", "expired"}:
            return ticket
        result = self.provider.poll(ticket.provider_task_ref)
        if result.state in {"queued", "running"}:
            updated = replace(ticket, state=result.state)
            self.jobs.put(updated)
            return updated
        if result.state in {"failed", "cancelled", "expired"}:
            updated = replace(ticket, state=result.state, reason=result.reason[:240])
            self.jobs.put(updated)
            return updated
        return self._verify_success(ticket, result)

    def _verify_success(
        self,
        ticket: _SpatialGenerationTicket,
        result: _SpatialPollResult,
    ) -> _SpatialGenerationTicket:
        if not result.artifacts:
            return self._verification_failed(ticket)
        refs: list[AssetRef] = []
        for artifact in result.artifacts:
            if not self._valid_artifact(artifact):
                return self._verification_failed(ticket)
            refs.append(
                self.objects.put(
                    artifact.content,
                    content_type=artifact.media_type,
                    rights=ticket.delivery_rights,
                )
            )
        verified = replace(ticket, state="verified", asset_refs=tuple(refs), reason="")
        self.jobs.put(verified)
        return verified

    def _valid_artifact(self, artifact: _SpatialArtifactCandidate) -> bool:
        return (
            artifact.media_type in self.provider.allowed_media_types
            and bool(artifact.content)
            and len(artifact.content) <= self.max_asset_bytes
            and hashlib.sha256(artifact.content).hexdigest() == artifact.content_sha256
        )

    def _verification_failed(self, ticket: _SpatialGenerationTicket) -> _SpatialGenerationTicket:
        failed = replace(ticket, state="failed", reason="artifact_verification_failed")
        self.jobs.put(failed)
        return failed

    def attach(
        self,
        submission_id: str,
        catalog: _DerivedSpatialCatalog,
    ) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state != "verified" or not ticket.asset_refs:
            raise ValueError("only verified spatial assets may be attached")
        catalog.attach(ticket.scene_key, ticket.asset_refs)
        attached = replace(ticket, state="attached")
        self.jobs.put(attached)
        return attached
