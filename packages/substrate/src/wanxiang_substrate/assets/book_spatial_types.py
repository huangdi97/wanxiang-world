"""Non-authoritative T3 spatial-generation contracts for source-derived scenes."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.storage import AssetRef

_SpatialJobState = Literal[
    "submitted",
    "queued",
    "running",
    "verified",
    "attached",
    "failed",
    "cancelled",
    "expired",
]
_SpatialProviderState = Literal["queued", "running", "succeeded", "failed", "cancelled", "expired"]


@dataclass(frozen=True, slots=True)
class _SpatialArtifactCandidate:
    content: bytes
    media_type: str
    content_sha256: str


@dataclass(frozen=True, slots=True)
class _SpatialPollResult:
    state: _SpatialProviderState
    artifacts: tuple[_SpatialArtifactCandidate, ...] = ()
    reason: str = ""


@dataclass(frozen=True, slots=True)
class _SpatialGenerationTicket:
    submission_id: str
    scene_key: str
    provider_id: str
    provider_version: str
    provider_task_ref: str
    state: _SpatialJobState
    reserved_cost_units: int
    delivery_rights: str
    scope_key: str = ""
    asset_refs: tuple[AssetRef, ...] = ()
    reason: str = ""


class _SpatialGenerationProvider:
    """Replaceable T3 generation contract; it is not a Kernel/runtime port."""

    provider_id: str = ""
    provider_version: str = ""
    requires_network: bool = True
    private_safe: bool = False
    cost_units_per_job: int = 0
    allowed_media_types: frozenset[str] = frozenset()

    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        raise TypeError("concrete spatial provider required")

    def poll(self, task_ref: str) -> _SpatialPollResult:
        raise TypeError("concrete spatial provider required")


class _SpatialJobStore:
    """Task metadata persistence seam; derived jobs never own canonical state."""

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        raise TypeError("concrete spatial job store required")

    def put(self, ticket: _SpatialGenerationTicket) -> None:
        raise TypeError("concrete spatial job store required")

    def list_scope(self, scope_key: str) -> tuple[_SpatialGenerationTicket, ...]:
        raise TypeError("concrete spatial job store required")
