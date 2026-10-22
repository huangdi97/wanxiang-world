"""Restart-safe T3 spatial generation without any Canon/History write authority."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false, reportUnusedImport=false

from __future__ import annotations

import hashlib
from dataclasses import replace

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_frame import (
    _projection_frame_from_mapping,
    _projection_frame_to_dict,
)
from wanxiang_substrate.assets.book_spatial_poll_validation import (
    _require_monotonic_spatial_poll,
    _validated_spatial_poll_result,
)
from wanxiang_substrate.assets.book_spatial_safety import (
    _require_spatial_asset_refs,
    _spatial_submission_guard,
)
from wanxiang_substrate.assets.book_spatial_store import (
    _InMemorySpatialJobStore,
    _LocalJsonSpatialJobStore,  # noqa: F401 - compatibility re-export
)
from wanxiang_substrate.assets.book_spatial_submission_validation import (
    _validated_spatial_submission_receipt,
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

    require_asset_refs = staticmethod(_require_spatial_asset_refs)

    def _submission_id(self, request: _SourceSceneRequest, scope_key: str, attempt: int = 0) -> str:
        retry = f":retry:{attempt}" if attempt else ""
        identity = (
            f"{scope_key}:{request.cache_key}:t3-job-v2:"
            f"{self.provider.provider_id}@{self.provider.provider_version}{retry}"
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
        attempt: int = 0,
    ) -> _SpatialGenerationTicket:
        if attempt < 0:
            raise ValueError("spatial attempt must be non-negative")
        submission_id = self._submission_id(request, scope_key, attempt)
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
                if existing.state == "submission_ambiguous":
                    if existing.provider_task_ref:
                        raise ValueError(
                            "ambiguous spatial submission has an invalid task reference"
                        )
                    if not self.provider.submit_is_idempotent:
                        raise ValueError(
                            "spatial submission outcome is ambiguous; automatic resubmit blocked"
                        )
                    return self._submit_reserved_intent(request, existing)
                return existing

            reserved_total = sum(
                row.accounted_cost_units for row in self.jobs.list_scope(scope_key)
            )
            if reserved_total + self.provider.cost_units_per_job > max_cost_units:
                raise ValueError("spatial world budget is exhausted")

            # Persist the cost reservation and uncertain submission outcome
            # before any provider call. If this process dies after the remote
            # task is accepted but before its task id is stored, a non-idempotent
            # provider cannot be silently billed again on restart.
            intent = _SpatialGenerationTicket(
                submission_id=submission_id,
                scene_key=request.stable_key,
                provider_id=self.provider.provider_id,
                provider_version=self.provider.provider_version,
                provider_task_ref="",
                state="submission_ambiguous",
                reserved_cost_units=self.provider.cost_units_per_job,
                delivery_rights=delivery_rights,
                scope_key=scope_key,
                reason="provider_submit_outcome_unknown",
                attempt=attempt,
            )
            self.jobs.put(intent)
            return self._submit_reserved_intent(request, intent)

    def _submit_reserved_intent(
        self,
        request: _SourceSceneRequest,
        intent: _SpatialGenerationTicket,
    ) -> _SpatialGenerationTicket:
        # Treat the provider boundary as untrusted at runtime even though the
        # protocol is statically typed; third-party adapters can still violate it.
        task_ref, request_ref = _validated_spatial_submission_receipt(
            self.provider.submit(request, idempotency_key=intent.submission_id)
        )
        submitted = replace(
            intent,
            provider_task_ref=task_ref,
            provider_request_ref=request_ref,
            state="submitted",
            reason="",
        )
        self.jobs.put(submitted)
        return submitted

    def poll(self, submission_id: str) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state in {
            "submission_ambiguous",
            "verified",
            "attached",
            "failed",
            "cancelled",
            "expired",
        }:
            return ticket
        if (
            ticket.provider_id != self.provider.provider_id
            or ticket.provider_version != self.provider.provider_version
        ):
            raise ValueError("configured spatial provider does not match persisted ticket")
        result = _validated_spatial_poll_result(self.provider.poll(ticket.provider_task_ref))
        _require_monotonic_spatial_poll(ticket, result)
        if result.provider_usage_units is not None:
            ticket = replace(ticket, provider_usage_units=result.provider_usage_units)
            if result.provider_usage_units > ticket.reserved_cost_units:
                failed = replace(ticket, state="failed", reason="provider_cost_overrun")
                self.jobs.put(failed)
                return failed
        if result.state in {"queued", "running"}:
            updated = replace(ticket, state=result.state, reason=result.reason[:240])
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
        projection_frame = None
        if result.projection_frame is not None:
            try:
                projection_frame = _projection_frame_from_mapping(
                    _projection_frame_to_dict(result.projection_frame)
                )
            except ValueError:
                return self._verification_failed(
                    ticket, reason="projection_frame_verification_failed"
                )
        refs = [
            self.objects.put(
                artifact.content,
                content_type=artifact.media_type,
                rights=ticket.delivery_rights,
            )
            for artifact in result.artifacts
        ]
        verified = replace(
            ticket,
            state="verified",
            asset_refs=tuple(refs),
            reason="",
            projection_frame=projection_frame,
        )
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

    def _verification_failed(
        self,
        ticket: _SpatialGenerationTicket,
        *,
        reason: str = "artifact_verification_failed",
    ) -> _SpatialGenerationTicket:
        failed = replace(ticket, state="failed", reason=reason)
        self.jobs.put(failed)
        return failed

    def attach(
        self,
        submission_id: str,
        catalog: _DerivedSpatialAttachments,
        *,
        expected_delivery_rights: str | None = None,
    ) -> _SpatialGenerationTicket:
        ticket = self.jobs.get(submission_id)
        if ticket is None:
            raise KeyError(submission_id)
        if ticket.state not in {"verified", "attached"} or not ticket.asset_refs:
            raise ValueError("only verified spatial assets may be attached")
        current_rights = expected_delivery_rights or ticket.delivery_rights
        if ticket.delivery_rights != current_rights:
            raise ValueError("persisted spatial ticket rights do not match current source rights")
        _require_spatial_asset_refs(
            self.objects,
            ticket.asset_refs,
            delivery_rights=current_rights,
            allowed_media_types=self.provider.allowed_media_types,
        )
        catalog.attach(ticket.scene_key, ticket.asset_refs)
        if ticket.state == "attached":
            return ticket
        attached = replace(ticket, state="attached")
        self.jobs.put(attached)
        return attached
