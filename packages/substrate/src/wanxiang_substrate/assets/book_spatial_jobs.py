"""Restart-safe T3 spatial generation without any Canon/History write authority."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

import hashlib
from dataclasses import replace

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_safety import (
    _require_spatial_asset_refs,
    _spatial_submission_guard,
)
from wanxiang_substrate.assets.book_spatial_store import (
    _InMemorySpatialJobStore,
    _LocalJsonSpatialJobStore,  # noqa: F401 - compatibility re-export
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
    _SpatialJobStore,
    _SpatialPollResult,
)
from wanxiang_substrate.assets.book_spatial_validation import _known_spatial_signature_matches
from wanxiang_substrate.assets.storage import AssetRef, InMemoryObjectStore, ObjectStore


class _DerivedSpatialAttachments:
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

    def _submission_id(self, request: _SourceSceneRequest, scope_key: str) -> str:
        identity = (
            f"{scope_key}:{request.cache_key}:t3-job-v2:"
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
        scope_key: str = "",
    ) -> _SpatialGenerationTicket:
        submission_id = self._submission_id(request, scope_key)
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

        with _spatial_submission_guard(self.jobs, submission_id, scope_key=scope_key):
            existing = self.jobs.get(submission_id)
            if existing is not None:
                if (
                    existing.provider_id != self.provider.provider_id
                    or existing.provider_version != self.provider.provider_version
                ):
                    raise ValueError("configured spatial provider does not match persisted ticket")
                if existing.reserved_cost_units > max_cost_units:
                    raise ValueError("persisted spatial ticket exceeds current budget")
                if existing.delivery_rights != delivery_rights:
                    raise ValueError(
                        "persisted spatial ticket rights do not match current delivery rights"
                    )
                return existing

            reserved_total = sum(
                row.reserved_cost_units for row in self.jobs.list_scope(scope_key)
            )
            if reserved_total + self.provider.cost_units_per_job > max_cost_units:
                raise ValueError("spatial world budget is exhausted")

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
                scope_key=scope_key,
            )
            self.jobs.put(ticket)
            return ticket

    def poll(self, submission_id: str) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state in {"verified", "attached", "failed", "cancelled", "expired"}:
            return ticket
        if (
            ticket.provider_id != self.provider.provider_id
            or ticket.provider_version != self.provider.provider_version
        ):
            raise ValueError("configured spatial provider does not match persisted ticket")
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
        if not all(self._valid_artifact(artifact) for artifact in result.artifacts):
            return self._verification_failed(ticket)
        refs = [
            self.objects.put(
                artifact.content,
                content_type=artifact.media_type,
                rights=ticket.delivery_rights,
            )
            for artifact in result.artifacts
        ]
        verified = replace(ticket, state="verified", asset_refs=tuple(refs), reason="")
        self.jobs.put(verified)
        return verified

    def _valid_artifact(self, artifact: _SpatialArtifactCandidate) -> bool:
        return (
            artifact.media_type in self.provider.allowed_media_types
            and bool(artifact.content)
            and len(artifact.content) <= self.max_asset_bytes
            and hashlib.sha256(artifact.content).hexdigest() == artifact.content_sha256
            and _known_spatial_signature_matches(artifact.media_type, artifact.content)
        )

    def _verification_failed(self, ticket: _SpatialGenerationTicket) -> _SpatialGenerationTicket:
        failed = replace(ticket, state="failed", reason="artifact_verification_failed")
        self.jobs.put(failed)
        return failed

    def attach(
        self,
        submission_id: str,
        catalog: _DerivedSpatialAttachments,
    ) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state not in {"verified", "attached"} or not ticket.asset_refs:
            raise ValueError("only verified spatial assets may be attached")
        _require_spatial_asset_refs(self.objects, ticket.asset_refs)
        catalog.attach(ticket.scene_key, ticket.asset_refs)
        if ticket.state == "attached":
            return ticket
        attached = replace(ticket, state="attached")
        self.jobs.put(attached)
        return attached
