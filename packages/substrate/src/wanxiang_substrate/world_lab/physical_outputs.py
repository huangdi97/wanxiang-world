"""Physical provider health and proposal-only resolution records (M93)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.physical_models import (
    PHYSICAL_PROVIDER_SCHEMA_VERSION,
)
from wanxiang_substrate.world_lab.registry_support import integer, names, parameters, ref, sequence

PhysicalProviderStatus = Literal["ready", "degraded", "unavailable"]
PhysicalResolutionStatus = Literal["resolved", "rejected", "unavailable"]
_HEALTH_STATUSES = frozenset({"ready", "degraded", "unavailable"})
_RESOLUTION_STATUSES = frozenset({"resolved", "rejected", "unavailable"})


def _status(value: object, name: str, allowed: frozenset[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ContractError(f"unsupported {name} {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class PhysicalProviderHealth:
    """Capability and availability record for a physical provider."""

    provider_id: str
    version: str
    available: bool
    deterministic: bool
    capabilities: tuple[str, ...] = ()
    status: PhysicalProviderStatus = "ready"
    reason: str = ""
    schema_version: int = PHYSICAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.provider_id, "provider_id")
        ref(self.version, "provider version")
        if type(self.available) is not bool or type(self.deterministic) is not bool:
            raise ContractError("provider availability and determinism must be boolean")
        status = _status(self.status, "provider health status", _HEALTH_STATUSES)
        if status == "ready" and not self.available:
            raise ContractError("ready provider health must be available")
        if status == "unavailable" and self.available:
            raise ContractError("unavailable provider health must not be available")
        if self.schema_version != PHYSICAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported physical provider health schema")
        object.__setattr__(self, "capabilities", names(self.capabilities, "capabilities"))
        if "\n" in self.reason or "\r" in self.reason:
            raise ContractError("provider health reason must be one-line text")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "provider_id": self.provider_id,
            "version": self.version,
            "available": self.available,
            "deterministic": self.deterministic,
            "capabilities": list(self.capabilities),
            "status": self.status,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PhysicalProviderHealth:
        status = _status(data.get("status"), "provider health status", _HEALTH_STATUSES)
        reason = data.get("reason", "")
        if not isinstance(reason, str):
            raise ContractError("provider health reason must be text")
        return cls(
            provider_id=ref(data.get("provider_id"), "provider_id"),
            version=ref(data.get("version"), "provider version"),
            available=data.get("available"),  # type: ignore[arg-type]
            deterministic=data.get("deterministic"),  # type: ignore[arg-type]
            capabilities=tuple(
                ref(value, "capabilities item")
                for value in sequence(data.get("capabilities", ()), "capabilities")
            ),
            status=cast(PhysicalProviderStatus, status),
            reason=reason,
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class PhysicalResolution:
    """Provider resolution carrying only a typed proposal and evidence refs."""

    resolution_id: str
    request_id: str
    provider_id: str
    provider_version: str
    snapshot_ref: str
    snapshot_revision: int
    status: PhysicalResolutionStatus
    proposed_delta: ProposedWorldDelta = ProposedWorldDelta()
    evidence_refs: tuple[str, ...] = ()
    diagnostics: tuple[tuple[str, object], ...] = ()
    schema_version: int = PHYSICAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "resolution_id",
            "request_id",
            "provider_id",
            "provider_version",
            "snapshot_ref",
        ):
            ref(getattr(self, name), name)
        integer(self.snapshot_revision, "snapshot_revision", minimum=0)
        status = _status(self.status, "physical resolution status", _RESOLUTION_STATUSES)
        if type(self.proposed_delta) is not ProposedWorldDelta:
            raise ContractError("proposed_delta must be ProposedWorldDelta")
        if status != "resolved" and not self.proposed_delta.is_empty():
            raise ContractError("non-resolved physical output cannot carry a proposed delta")
        if self.schema_version != PHYSICAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported physical resolution schema")
        object.__setattr__(self, "evidence_refs", names(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "diagnostics", parameters(self.diagnostics, "diagnostics"))

    @property
    def delta(self) -> ProposedWorldDelta:
        """Short read-only spelling for consumers that call it a delta."""
        return self.proposed_delta

    def canonical_payload(self) -> dict[str, object]:
        from wanxiang_domain.serialization import delta_to_primitive

        return {
            "schema_version": self.schema_version,
            "request_id": self.request_id,
            "provider_id": self.provider_id,
            "provider_version": self.provider_version,
            "snapshot_ref": self.snapshot_ref,
            "snapshot_revision": self.snapshot_revision,
            "status": self.status,
            "proposed_delta": delta_to_primitive(self.proposed_delta),
            "evidence_refs": list(self.evidence_refs),
            "diagnostics": [list(item) for item in self.diagnostics],
        }

    @property
    def replay_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["resolution_id"] = self.resolution_id
        payload["replay_hash"] = self.replay_hash
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PhysicalResolution:
        from wanxiang_domain.serialization import delta_from_primitive

        raw_delta = data.get("proposed_delta")
        if not isinstance(raw_delta, Mapping):
            raise ContractError("proposed_delta must be a mapping")
        raw_diagnostics = sequence(data.get("diagnostics", ()), "diagnostics")
        diagnostics: list[tuple[str, object]] = []
        for item in raw_diagnostics:
            if not isinstance(item, (list, tuple)):
                raise ContractError("diagnostics items must be pairs")
            pair = cast(list[object] | tuple[object, ...], item)
            if len(pair) != 2:
                raise ContractError("diagnostics items must be pairs")
            if not isinstance(pair[0], str):
                raise ContractError("diagnostics keys must be text")
            diagnostics.append((pair[0], pair[1]))
        result = cls(
            resolution_id=ref(data.get("resolution_id"), "resolution_id"),
            request_id=ref(data.get("request_id"), "request_id"),
            provider_id=ref(data.get("provider_id"), "provider_id"),
            provider_version=ref(data.get("provider_version"), "provider_version"),
            snapshot_ref=ref(data.get("snapshot_ref"), "snapshot_ref"),
            snapshot_revision=integer(
                data.get("snapshot_revision"), "snapshot_revision", minimum=0
            ),
            status=cast(
                PhysicalResolutionStatus,
                _status(data.get("status"), "physical resolution status", _RESOLUTION_STATUSES),
            ),
            proposed_delta=delta_from_primitive(cast(dict[str, object], raw_delta)),
            evidence_refs=tuple(
                ref(value, "evidence_refs item")
                for value in sequence(data.get("evidence_refs", ()), "evidence_refs")
            ),
            diagnostics=tuple(diagnostics),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )
        if data.get("replay_hash") != result.replay_hash:
            raise ContractError("physical resolution replay hash does not verify")
        return result


PhysicalSimulationResolution = PhysicalResolution

__all__ = [
    "PhysicalProviderHealth",
    "PhysicalProviderStatus",
    "PhysicalResolution",
    "PhysicalResolutionStatus",
    "PhysicalSimulationResolution",
]
