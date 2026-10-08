"""Physical provider input value objects for the M93 bridge boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.registry_support import integer, names, parameters, ref, sequence

PHYSICAL_PROVIDER_SCHEMA_VERSION = 1


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


@dataclass(frozen=True, slots=True)
class PhysicalBody:
    """Read-only spatial body data needed by a physical provider."""

    body_ref: str
    position: tuple[float, float]
    velocity: tuple[float, float] = (0.0, 0.0)
    radius: float = 0.0
    collidable: bool = True

    def __post_init__(self) -> None:
        ref(self.body_ref, "body_ref")
        object.__setattr__(self, "position", _vector(self.position, "position"))
        object.__setattr__(self, "velocity", _vector(self.velocity, "velocity"))
        radius = _number(self.radius, "radius")
        if radius < 0.0:
            raise ContractError("radius must be non-negative")
        if type(self.collidable) is not bool:
            raise ContractError("collidable must be boolean")
        object.__setattr__(self, "radius", radius)

    def to_dict(self) -> dict[str, object]:
        return {
            "body_ref": self.body_ref,
            "position": list(self.position),
            "velocity": list(self.velocity),
            "radius": self.radius,
            "collidable": self.collidable,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PhysicalBody:
        return cls(
            body_ref=ref(data.get("body_ref"), "body_ref"),
            position=_vector(data.get("position"), "position"),
            velocity=_vector(data.get("velocity", (0.0, 0.0)), "velocity"),
            radius=_number(data.get("radius", 0.0), "radius"),
            collidable=data.get("collidable", True),  # type: ignore[arg-type]
        )


@dataclass(frozen=True, slots=True)
class PhysicalSnapshot:
    """Immutable physical read model derived from canonical state."""

    snapshot_ref: str
    world_instance_ref: str
    branch_ref: str
    revision: int
    world_time_ticks: int
    state_hash: str
    bodies: tuple[PhysicalBody, ...] = ()
    event_refs: tuple[str, ...] = ()
    schema_version: int = PHYSICAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ("snapshot_ref", "world_instance_ref", "branch_ref", "state_hash"):
            ref(getattr(self, name), name)
        integer(self.revision, "revision", minimum=0)
        integer(self.world_time_ticks, "world_time_ticks", minimum=0)
        if self.schema_version != PHYSICAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported physical snapshot schema")
        if any(type(body) is not PhysicalBody for body in self.bodies):
            raise ContractError("physical snapshot bodies must be PhysicalBody values")
        body_refs = tuple(body.body_ref for body in self.bodies)
        if len(body_refs) != len(set(body_refs)):
            raise ContractError("physical snapshot body refs must be unique")
        object.__setattr__(
            self,
            "bodies",
            tuple(sorted(self.bodies, key=lambda body: body.body_ref)),
        )
        object.__setattr__(self, "event_refs", names(self.event_refs, "event_refs"))

    @property
    def body(self) -> tuple[PhysicalBody, ...]:
        """Compatibility spelling for consumers that call bodies a body set."""
        return self.bodies

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "snapshot_ref": self.snapshot_ref,
            "world_instance_ref": self.world_instance_ref,
            "branch_ref": self.branch_ref,
            "revision": self.revision,
            "world_time_ticks": self.world_time_ticks,
            "state_hash": self.state_hash,
            "bodies": [body.to_dict() for body in self.bodies],
            "event_refs": list(self.event_refs),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PhysicalSnapshot:
        raw_bodies = sequence(data.get("bodies", ()), "bodies")
        bodies = tuple(
            PhysicalBody.from_dict(cast(Mapping[str, object], item))
            for item in raw_bodies
            if isinstance(item, Mapping)
        )
        if len(bodies) != len(raw_bodies):
            raise ContractError("bodies must contain mappings")
        return cls(
            snapshot_ref=ref(data.get("snapshot_ref"), "snapshot_ref"),
            world_instance_ref=ref(data.get("world_instance_ref"), "world_instance_ref"),
            branch_ref=ref(data.get("branch_ref"), "branch_ref"),
            revision=integer(data.get("revision"), "revision", minimum=0),
            world_time_ticks=integer(data.get("world_time_ticks"), "world_time_ticks", minimum=0),
            state_hash=ref(data.get("state_hash"), "state_hash"),
            bodies=bodies,
            event_refs=tuple(
                ref(value, "event_refs item")
                for value in sequence(data.get("event_refs", ()), "event_refs")
            ),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class PhysicalSimulationRequest:
    """Deterministic request against one immutable physical snapshot."""

    request_id: str
    snapshot_ref: str
    snapshot_revision: int
    action: str = "step"
    actor_ref: str | None = None
    target_position: tuple[float, float] | None = None
    step_ticks: int = 1
    seed: int = 0
    parameters: tuple[tuple[str, object], ...] = ()
    schema_version: int = PHYSICAL_PROVIDER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        for name in ("request_id", "snapshot_ref", "action"):
            ref(getattr(self, name), name)
        if self.actor_ref is not None:
            ref(self.actor_ref, "actor_ref")
        integer(self.snapshot_revision, "snapshot_revision", minimum=0)
        integer(self.step_ticks, "step_ticks", minimum=1)
        if type(self.seed) is not int:
            raise ContractError("seed must be an integer")
        if self.schema_version != PHYSICAL_PROVIDER_SCHEMA_VERSION:
            raise ContractError("unsupported physical simulation request schema")
        if self.target_position is not None:
            object.__setattr__(
                self, "target_position", _vector(self.target_position, "target_position")
            )
        object.__setattr__(self, "parameters", parameters(self.parameters, "parameters"))

    @property
    def input_hash(self) -> str:
        return semantic_sha256(
            {
                "schema_version": self.schema_version,
                "request_id": self.request_id,
                "snapshot_ref": self.snapshot_ref,
                "snapshot_revision": self.snapshot_revision,
                "action": self.action,
                "actor_ref": self.actor_ref,
                "target_position": self.target_position,
                "step_ticks": self.step_ticks,
                "seed": self.seed,
                "parameters": self.parameters,
            }
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "request_id": self.request_id,
            "snapshot_ref": self.snapshot_ref,
            "snapshot_revision": self.snapshot_revision,
            "action": self.action,
            "actor_ref": self.actor_ref,
            "target_position": list(self.target_position)
            if self.target_position is not None
            else None,
            "step_ticks": self.step_ticks,
            "seed": self.seed,
            "parameters": [list(item) for item in self.parameters],
            "input_hash": self.input_hash,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> PhysicalSimulationRequest:
        target = data.get("target_position")
        result = cls(
            request_id=ref(data.get("request_id"), "request_id"),
            snapshot_ref=ref(data.get("snapshot_ref"), "snapshot_ref"),
            snapshot_revision=integer(
                data.get("snapshot_revision"), "snapshot_revision", minimum=0
            ),
            action=ref(data.get("action", "step"), "action"),
            actor_ref=(
                ref(data["actor_ref"], "actor_ref")
                if "actor_ref" in data and data.get("actor_ref") is not None
                else None
            ),
            target_position=_vector(target, "target_position") if target is not None else None,
            step_ticks=integer(data.get("step_ticks", 1), "step_ticks", minimum=1),
            seed=data.get("seed", 0),  # type: ignore[arg-type]
            parameters=parameters(sequence(data.get("parameters", ()), "parameters"), "parameters"),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )
        if data.get("input_hash") != result.input_hash:
            raise ContractError("physical simulation request input hash does not verify")
        return result


ReadonlyPhysicalSnapshot = PhysicalSnapshot
PhysicalWorldSnapshot = PhysicalSnapshot
SimulationRequest = PhysicalSimulationRequest

__all__ = [
    "PHYSICAL_PROVIDER_SCHEMA_VERSION",
    "PhysicalBody",
    "PhysicalSimulationRequest",
    "PhysicalSnapshot",
    "PhysicalWorldSnapshot",
    "ReadonlyPhysicalSnapshot",
    "SimulationRequest",
]
