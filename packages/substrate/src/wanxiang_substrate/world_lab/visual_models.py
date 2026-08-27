"""Visual provider input records for the M93 projection boundary."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.assets.storage import AssetRef
from wanxiang_substrate.world_lab.registry_support import integer, names, ref, sequence

VISUAL_PROVIDER_SCHEMA_VERSION = 1


def _number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{name} must be a finite number")
    result = float(value)
    if not isfinite(result):
        raise ContractError(f"{name} must be a finite number")
    return result


def _vector(value: object, name: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)):
        raise ContractError(f"{name} must contain exactly two numbers")
    pair = cast(list[object] | tuple[object, ...], value)
    if len(pair) != 2:
        raise ContractError(f"{name} must contain exactly two numbers")
    return (_number(pair[0], f"{name}[0]"), _number(pair[1], f"{name}[1]"))


def _assets(values: Sequence[object], name: str) -> tuple[AssetRef, ...]:
    assets = tuple(value for value in values if type(value) is AssetRef)
    if len(assets) != len(values):
        raise ContractError(f"{name} must contain AssetRef values")
    if len({asset.asset_id for asset in assets}) != len(assets):
        raise ContractError(f"{name} asset ids must be unique")
    return tuple(sorted(assets, key=lambda asset: asset.asset_id))


def _asset_from_dict(value: object, name: str) -> AssetRef:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be a mapping")
    data = cast(Mapping[str, object], value)
    return AssetRef(
        asset_id=ref(data.get("asset_id"), f"{name}.asset_id"),
        content_hash=ref(data.get("content_hash"), f"{name}.content_hash"),
        size=integer(data.get("size"), f"{name}.size", minimum=0),
        content_type=ref(data.get("content_type"), f"{name}.content_type"),
        rights=ref(data.get("rights", "public"), f"{name}.rights"),
    )


def _asset_to_dict(asset: AssetRef) -> dict[str, object]:
    return {
        "asset_id": asset.asset_id,
        "content_hash": asset.content_hash,
        "size": asset.size,
        "content_type": asset.content_type,
        "rights": asset.rights,
    }


def _refs(values: Sequence[object], name: str) -> tuple[str, ...]:
    return names(values, name)


@dataclass(frozen=True, slots=True)
class VisualSceneObject:
    """Read-only scene object; audience refs are input policy, never output truth."""

    object_ref: str
    entity_ref: str
    position: tuple[float, float]
    asset_ref: AssetRef | None = None
    audience_refs: tuple[str, ...] = ()
    event_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        ref(self.object_ref, "object_ref")
        ref(self.entity_ref, "entity_ref")
        object.__setattr__(self, "position", _vector(self.position, "position"))
        if self.asset_ref is not None and type(self.asset_ref) is not AssetRef:
            raise ContractError("asset_ref must be an AssetRef")
        object.__setattr__(self, "audience_refs", _refs(self.audience_refs, "audience_refs"))
        object.__setattr__(self, "event_refs", _refs(self.event_refs, "event_refs"))

    def to_dict(self) -> dict[str, object]:
        return {
            "object_ref": self.object_ref,
            "entity_ref": self.entity_ref,
            "position": list(self.position),
            "asset_ref": _asset_to_dict(self.asset_ref) if self.asset_ref else None,
            "audience_refs": list(self.audience_refs),
            "event_refs": list(self.event_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> VisualSceneObject:
        raw_asset = data.get("asset_ref")
        return cls(
            object_ref=ref(data.get("object_ref"), "object_ref"),
            entity_ref=ref(data.get("entity_ref"), "entity_ref"),
            position=_vector(data.get("position"), "position"),
            asset_ref=_asset_from_dict(raw_asset, "asset_ref") if raw_asset is not None else None,
            audience_refs=tuple(
                ref(value, "audience_refs item")
                for value in sequence(data.get("audience_refs", ()), "audience_refs")
            ),
            event_refs=tuple(
                ref(value, "event_refs item")
                for value in sequence(data.get("event_refs", ()), "event_refs")
            ),
        )


@dataclass(frozen=True, slots=True)
class VisualSceneState:
    """Immutable scene read model pinned to one canonical snapshot revision."""

    scene_ref: str
    snapshot_ref: str
    world_instance_ref: str
    branch_ref: str
    revision: int
    world_time_ticks: int
    state_hash: str
    objects: tuple[VisualSceneObject, ...] = ()
    asset_refs: tuple[AssetRef, ...] = ()
    event_refs: tuple[str, ...] = ()
    schema_version: int = VISUAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in (
            "scene_ref",
            "snapshot_ref",
            "world_instance_ref",
            "branch_ref",
            "state_hash",
        ):
            ref(getattr(self, name), name)
        integer(self.revision, "revision", minimum=0)
        integer(self.world_time_ticks, "world_time_ticks", minimum=0)
        if self.schema_version != VISUAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported visual scene schema")
        if any(type(item) is not VisualSceneObject for item in self.objects):
            raise ContractError("objects must contain VisualSceneObject values")
        object_refs = tuple(item.object_ref for item in self.objects)
        if len(object_refs) != len(set(object_refs)):
            raise ContractError("scene object refs must be unique")
        assets = _assets(self.asset_refs, "asset_refs")
        asset_ids = {asset.asset_id for asset in assets}
        if any(
            item.asset_ref is not None and item.asset_ref.asset_id not in asset_ids
            for item in self.objects
        ):
            raise ContractError("scene object asset is missing from asset_refs")
        object.__setattr__(
            self, "objects", tuple(sorted(self.objects, key=lambda item: item.object_ref))
        )
        object.__setattr__(self, "asset_refs", assets)
        object.__setattr__(self, "event_refs", _refs(self.event_refs, "event_refs"))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "scene_ref": self.scene_ref,
            "snapshot_ref": self.snapshot_ref,
            "world_instance_ref": self.world_instance_ref,
            "branch_ref": self.branch_ref,
            "revision": self.revision,
            "world_time_ticks": self.world_time_ticks,
            "state_hash": self.state_hash,
            "objects": [item.to_dict() for item in self.objects],
            "asset_refs": [_asset_to_dict(asset) for asset in self.asset_refs],
            "event_refs": list(self.event_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> VisualSceneState:
        raw_objects = sequence(data.get("objects", ()), "objects")
        objects = tuple(
            VisualSceneObject.from_dict(cast(Mapping[str, object], item))
            for item in raw_objects
            if isinstance(item, Mapping)
        )
        if len(objects) != len(raw_objects):
            raise ContractError("objects must contain mappings")
        raw_assets = sequence(data.get("asset_refs", ()), "asset_refs")
        assets = tuple(_asset_from_dict(item, "asset_refs item") for item in raw_assets)
        return cls(
            scene_ref=ref(data.get("scene_ref"), "scene_ref"),
            snapshot_ref=ref(data.get("snapshot_ref"), "snapshot_ref"),
            world_instance_ref=ref(data.get("world_instance_ref"), "world_instance_ref"),
            branch_ref=ref(data.get("branch_ref"), "branch_ref"),
            revision=integer(data.get("revision"), "revision", minimum=0),
            world_time_ticks=integer(data.get("world_time_ticks"), "world_time_ticks", minimum=0),
            state_hash=ref(data.get("state_hash"), "state_hash"),
            objects=objects,
            asset_refs=assets,
            event_refs=tuple(
                ref(value, "event_refs item")
                for value in sequence(data.get("event_refs", ()), "event_refs")
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class ActorPerspective:
    """Immutable actor view policy used to derive a projection frame."""

    perspective_ref: str
    actor_ref: str
    origin: tuple[float, float]
    view_radius: float
    allowed_object_refs: tuple[str, ...] = ()
    denied_object_refs: tuple[str, ...] = ()
    allowed_rights: tuple[str, ...] = ("public",)
    schema_version: int = VISUAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.perspective_ref, "perspective_ref")
        ref(self.actor_ref, "actor_ref")
        object.__setattr__(self, "origin", _vector(self.origin, "origin"))
        radius = _number(self.view_radius, "view_radius")
        if radius < 0.0:
            raise ContractError("view_radius must be non-negative")
        if self.schema_version != VISUAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported actor perspective schema")
        allowed = _refs(self.allowed_object_refs, "allowed_object_refs")
        denied = _refs(self.denied_object_refs, "denied_object_refs")
        if set(allowed).intersection(denied):
            raise ContractError("allowed and denied object refs must be disjoint")
        object.__setattr__(self, "view_radius", radius)
        object.__setattr__(self, "allowed_object_refs", allowed)
        object.__setattr__(self, "denied_object_refs", denied)
        object.__setattr__(self, "allowed_rights", _refs(self.allowed_rights, "allowed_rights"))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "perspective_ref": self.perspective_ref,
            "actor_ref": self.actor_ref,
            "origin": list(self.origin),
            "view_radius": self.view_radius,
            "allowed_object_refs": list(self.allowed_object_refs),
            "denied_object_refs": list(self.denied_object_refs),
            "allowed_rights": list(self.allowed_rights),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ActorPerspective:
        return cls(
            perspective_ref=ref(data.get("perspective_ref"), "perspective_ref"),
            actor_ref=ref(data.get("actor_ref"), "actor_ref"),
            origin=_vector(data.get("origin"), "origin"),
            view_radius=_number(data.get("view_radius"), "view_radius"),
            allowed_object_refs=tuple(
                ref(value, "allowed_object_refs item")
                for value in sequence(data.get("allowed_object_refs", ()), "allowed_object_refs")
            ),
            denied_object_refs=tuple(
                ref(value, "denied_object_refs item")
                for value in sequence(data.get("denied_object_refs", ()), "denied_object_refs")
            ),
            allowed_rights=tuple(
                ref(value, "allowed_rights item")
                for value in sequence(data.get("allowed_rights", ("public",)), "allowed_rights")
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


VisualActorPerspective = ActorPerspective

__all__ = [
    "ActorPerspective",
    "VISUAL_PROVIDER_SCHEMA_VERSION",
    "VisualActorPerspective",
    "VisualSceneObject",
    "VisualSceneState",
]
