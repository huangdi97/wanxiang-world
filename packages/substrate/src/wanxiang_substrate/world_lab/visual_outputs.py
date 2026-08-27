"""Visual provider output records for the M93 projection boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.world_lab.registry_support import integer, names, ref, sequence
from wanxiang_substrate.world_lab.visual_models import (
    VISUAL_PROVIDER_SCHEMA_VERSION,
    _asset_from_dict,  # pyright: ignore[reportPrivateUsage]
    _asset_to_dict,  # pyright: ignore[reportPrivateUsage]
    _vector,  # pyright: ignore[reportPrivateUsage]
)

VisualProviderStatus = Literal["ready", "degraded", "unavailable"]
VisualProjectionStatus = Literal["projected", "rejected", "unavailable"]
_HEALTH_STATUSES = frozenset({"ready", "degraded", "unavailable"})
_PROJECTION_STATUSES = frozenset({"projected", "rejected", "unavailable"})


def _status(value: object, name: str, allowed: frozenset[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ContractError(f"unsupported {name} {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class VisualProjectedObject:
    """Sanitized object in a frame; source audience/rights policy is removed."""

    object_ref: str
    entity_ref: str
    position: tuple[float, float]
    asset_ref: AssetRef | None = None

    def __post_init__(self) -> None:
        ref(self.object_ref, "object_ref")
        ref(self.entity_ref, "entity_ref")
        object.__setattr__(self, "position", _vector(self.position, "position"))
        if self.asset_ref is not None and type(self.asset_ref) is not AssetRef:
            raise ContractError("asset_ref must be an AssetRef")

    def to_dict(self) -> dict[str, object]:
        return {
            "object_ref": self.object_ref,
            "entity_ref": self.entity_ref,
            "position": list(self.position),
            "asset_ref": _asset_to_dict(self.asset_ref) if self.asset_ref else None,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> VisualProjectedObject:
        raw_asset = data.get("asset_ref")
        return cls(
            object_ref=ref(data.get("object_ref"), "object_ref"),
            entity_ref=ref(data.get("entity_ref"), "entity_ref"),
            position=_vector(data.get("position"), "position"),
            asset_ref=_asset_from_dict(raw_asset, "asset_ref") if raw_asset is not None else None,
        )


@dataclass(frozen=True, slots=True)
class VisualProviderHealth:
    """Capability and availability record for a visual provider."""

    provider_id: str
    version: str
    available: bool
    deterministic: bool
    capabilities: tuple[str, ...] = ()
    status: VisualProviderStatus = "ready"
    reason: str = ""
    schema_version: int = VISUAL_PROVIDER_SCHEMA_VERSION

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
        if self.schema_version != VISUAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported visual provider health schema")
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
    def from_dict(cls, data: Mapping[str, object]) -> VisualProviderHealth:
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
            status=cast(VisualProviderStatus, status),
            reason=reason,
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class VisualProjectionFrame:
    """Read-only, actor-scoped frame with explicit snapshot/event provenance."""

    frame_ref: str
    provider_id: str
    provider_version: str
    scene_ref: str
    snapshot_ref: str
    snapshot_revision: int
    actor_ref: str
    perspective_ref: str
    status: VisualProjectionStatus
    objects: tuple[VisualProjectedObject, ...] = ()
    asset_refs: tuple[AssetRef, ...] = ()
    event_refs: tuple[str, ...] = ()
    state_hash: str = ""
    projection_only: bool = True
    schema_version: int = VISUAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "frame_ref",
            "provider_id",
            "provider_version",
            "scene_ref",
            "snapshot_ref",
            "actor_ref",
            "perspective_ref",
            "state_hash",
        ):
            ref(getattr(self, name), name)
        integer(self.snapshot_revision, "snapshot_revision", minimum=0)
        status = _status(self.status, "visual projection status", _PROJECTION_STATUSES)
        if type(self.projection_only) is not bool or not self.projection_only:
            raise ContractError("visual frame must be projection-only")
        if self.schema_version != VISUAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported visual projection schema")
        if any(type(item) is not VisualProjectedObject for item in self.objects):
            raise ContractError("objects must contain VisualProjectedObject values")
        object_refs = tuple(item.object_ref for item in self.objects)
        if len(object_refs) != len(set(object_refs)):
            raise ContractError("projected object refs must be unique")
        assets = tuple(asset for asset in self.asset_refs if type(asset) is AssetRef)
        if len(assets) != len(self.asset_refs):
            raise ContractError("asset_refs must contain AssetRef values")
        if len({asset.asset_id for asset in assets}) != len(assets):
            raise ContractError("frame asset ids must be unique")
        asset_ids = {asset.asset_id for asset in assets}
        if any(
            item.asset_ref is not None and item.asset_ref.asset_id not in asset_ids
            for item in self.objects
        ):
            raise ContractError("projected object asset is missing from asset_refs")
        if status != "projected" and self.objects:
            raise ContractError("non-projected frame cannot contain visible objects")
        object.__setattr__(
            self, "objects", tuple(sorted(self.objects, key=lambda item: item.object_ref))
        )
        object.__setattr__(
            self, "asset_refs", tuple(sorted(assets, key=lambda asset: asset.asset_id))
        )
        object.__setattr__(self, "event_refs", names(self.event_refs, "event_refs"))

    @property
    def visible_objects(self) -> tuple[VisualProjectedObject, ...]:
        return self.objects

    def canonical_payload(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "provider_id": self.provider_id,
            "provider_version": self.provider_version,
            "scene_ref": self.scene_ref,
            "snapshot_ref": self.snapshot_ref,
            "snapshot_revision": self.snapshot_revision,
            "actor_ref": self.actor_ref,
            "perspective_ref": self.perspective_ref,
            "status": self.status,
            "objects": [item.to_dict() for item in self.objects],
            "asset_refs": [_asset_to_dict(asset) for asset in self.asset_refs],
            "event_refs": list(self.event_refs),
            "state_hash": self.state_hash,
            "projection_only": self.projection_only,
        }

    @property
    def projection_hash(self) -> str:
        return semantic_sha256(self.canonical_payload())

    def to_dict(self) -> dict[str, object]:
        payload = self.canonical_payload()
        payload["frame_ref"] = self.frame_ref
        payload["projection_hash"] = self.projection_hash
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> VisualProjectionFrame:
        raw_objects = sequence(data.get("objects", ()), "objects")
        objects = tuple(
            VisualProjectedObject.from_dict(cast(Mapping[str, object], item))
            for item in raw_objects
            if isinstance(item, Mapping)
        )
        if len(objects) != len(raw_objects):
            raise ContractError("objects must contain mappings")
        raw_assets = sequence(data.get("asset_refs", ()), "asset_refs")
        assets = tuple(_asset_from_dict(item, "asset_refs item") for item in raw_assets)
        result = cls(
            frame_ref=ref(data.get("frame_ref"), "frame_ref"),
            provider_id=ref(data.get("provider_id"), "provider_id"),
            provider_version=ref(data.get("provider_version"), "provider_version"),
            scene_ref=ref(data.get("scene_ref"), "scene_ref"),
            snapshot_ref=ref(data.get("snapshot_ref"), "snapshot_ref"),
            snapshot_revision=integer(
                data.get("snapshot_revision"), "snapshot_revision", minimum=0
            ),
            actor_ref=ref(data.get("actor_ref"), "actor_ref"),
            perspective_ref=ref(data.get("perspective_ref"), "perspective_ref"),
            status=cast(
                VisualProjectionStatus,
                _status(data.get("status"), "visual projection status", _PROJECTION_STATUSES),
            ),
            objects=objects,
            asset_refs=assets,
            event_refs=tuple(
                ref(value, "event_refs item")
                for value in sequence(data.get("event_refs", ()), "event_refs")
            ),
            state_hash=ref(data.get("state_hash"), "state_hash"),
            projection_only=data.get("projection_only"),  # type: ignore[arg-type]
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )
        if data.get("projection_hash") != result.projection_hash:
            raise ContractError("visual projection hash does not verify")
        return result


__all__ = [
    "VisualProjectedObject",
    "VisualProjectionFrame",
    "VisualProjectionStatus",
    "VisualProviderHealth",
    "VisualProviderStatus",
]
