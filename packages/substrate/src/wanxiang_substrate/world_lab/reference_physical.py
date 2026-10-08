"""CI reference physical provider for deterministic navigation/collision."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite

from wanxiang_domain.delta import EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

from wanxiang_substrate.world_lab.physical_models import (
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
)
from wanxiang_substrate.world_lab.physical_outputs import (
    PhysicalProviderHealth,
    PhysicalResolution,
)
from wanxiang_substrate.world_lab.registry_support import ref


@dataclass(frozen=True, slots=True)
class ReferencePhysicalProvider:
    """Small deterministic provider that emits movement proposals only."""

    provider_id: str
    provider_version: str

    def __post_init__(self) -> None:
        ref(self.provider_id, "provider_id")
        ref(self.provider_version, "provider_version")

    def health(self) -> PhysicalProviderHealth:
        return PhysicalProviderHealth(
            provider_id=self.provider_id,
            version=self.provider_version,
            available=True,
            deterministic=True,
            capabilities=("navigation", "collision", "replay"),
        )

    def simulate(
        self,
        snapshot: PhysicalSnapshot,
        request: PhysicalSimulationRequest,
    ) -> PhysicalResolution:
        if (
            request.snapshot_ref != snapshot.snapshot_ref
            or request.snapshot_revision != snapshot.revision
        ):
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "snapshot_mismatch"),),
            )
        if request.action not in {"navigate", "step"}:
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "unsupported_action"), ("action", request.action)),
            )
        if request.actor_ref is None:
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "actor_required"),),
            )
        actor = next((body for body in snapshot.bodies if body.body_ref == request.actor_ref), None)
        if actor is None:
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "actor_not_found"), ("actor_ref", request.actor_ref)),
            )
        try:
            speed = self._speed(request)
            destination = self._destination(actor, request, speed)
            self._validate_entity_ref(actor.body_ref)
        except ContractError as exc:
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "invalid_request"), ("reason", str(exc))),
            )
        blocker = self._collision_blocker(actor, destination, snapshot.bodies)
        if blocker is not None:
            return self._result(
                snapshot,
                request,
                "rejected",
                ProposedWorldDelta(),
                (("outcome", "collision"), ("blocked_by", blocker.body_ref)),
            )
        delta = ProposedWorldDelta(
            operations=(self._update(actor, destination, request.step_ticks, snapshot),)
        )
        return self._result(
            snapshot,
            request,
            "resolved",
            delta,
            (("outcome", "resolved"), ("body_ref", actor.body_ref)),
        )

    @staticmethod
    def _speed(request: PhysicalSimulationRequest) -> float:
        value = next((value for key, value in request.parameters if key == "speed"), 1.0)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ContractError("speed must be a finite positive number")
        speed = float(value)
        if not isfinite(speed) or speed <= 0.0:
            raise ContractError("speed must be a finite positive number")
        return speed

    @staticmethod
    def _destination(
        actor: PhysicalBody,
        request: PhysicalSimulationRequest,
        speed: float,
    ) -> tuple[float, float]:
        if request.action == "navigate":
            if request.target_position is None:
                raise ContractError("navigate requires target_position")
            target = request.target_position
            dx, dy = target[0] - actor.position[0], target[1] - actor.position[1]
            distance = hypot(dx, dy)
            if distance == 0.0:
                return actor.position
            travel = min(distance, speed * request.step_ticks)
            scale = travel / distance
            return (actor.position[0] + dx * scale, actor.position[1] + dy * scale)
        return (
            actor.position[0] + actor.velocity[0] * request.step_ticks,
            actor.position[1] + actor.velocity[1] * request.step_ticks,
        )

    @classmethod
    def _collision_blocker(
        cls,
        actor: PhysicalBody,
        destination: tuple[float, float],
        bodies: tuple[PhysicalBody, ...],
    ) -> PhysicalBody | None:
        for body in bodies:
            if body.body_ref == actor.body_ref or not body.collidable:
                continue
            if cls._segment_distance(actor.position, destination, body.position) <= (
                actor.radius + body.radius
            ):
                return body
        return None

    @staticmethod
    def _segment_distance(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> float:
        line_x, line_y = end[0] - start[0], end[1] - start[1]
        length_squared = line_x * line_x + line_y * line_y
        if length_squared == 0.0:
            return hypot(point[0] - start[0], point[1] - start[1])
        along = ((point[0] - start[0]) * line_x + (point[1] - start[1]) * line_y) / length_squared
        along = max(0.0, min(1.0, along))
        nearest = (start[0] + along * line_x, start[1] + along * line_y)
        return hypot(point[0] - nearest[0], point[1] - nearest[1])

    @staticmethod
    def _validate_entity_ref(body_ref: str) -> None:
        EntityId(body_ref)

    @staticmethod
    def _update(
        actor: PhysicalBody,
        destination: tuple[float, float],
        step_ticks: int,
        snapshot: PhysicalSnapshot,
    ) -> EntityUpdate:
        component_id = ComponentId("physical_" + semantic_sha256(actor.body_ref)[:24])
        component = ComponentData(
            component_id=component_id,
            component_type="world_lab.physical_body",
            schema_version=SchemaVersion(1),
            fields={
                "position_x": destination[0],
                "position_y": destination[1],
                "velocity_x": (destination[0] - actor.position[0]) / step_ticks,
                "velocity_y": (destination[1] - actor.position[1]) / step_ticks,
                "world_time_ticks": snapshot.world_time_ticks + step_ticks,
            },
        )
        return EntityUpdate(entity_id=EntityId(actor.body_ref), components=(component,))

    def _result(
        self,
        snapshot: PhysicalSnapshot,
        request: PhysicalSimulationRequest,
        status: str,
        delta: ProposedWorldDelta,
        diagnostics: tuple[tuple[str, object], ...],
    ) -> PhysicalResolution:
        evidence_hash = semantic_sha256(
            {
                "provider_id": self.provider_id,
                "provider_version": self.provider_version,
                "snapshot": snapshot.to_dict(),
                "request": request.to_dict(),
                "status": status,
                "diagnostics": diagnostics,
            }
        )
        return PhysicalResolution(
            resolution_id="resolution:" + evidence_hash,
            request_id=request.request_id,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            snapshot_ref=snapshot.snapshot_ref,
            snapshot_revision=snapshot.revision,
            status=status,  # type: ignore[arg-type]
            proposed_delta=delta,
            evidence_refs=("evidence:physical:" + evidence_hash,),
            diagnostics=diagnostics + (("evidence_hash", evidence_hash),),
        )


__all__ = ["ReferencePhysicalProvider"]
