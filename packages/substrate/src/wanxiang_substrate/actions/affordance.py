"""Affordance computation: which actions an actor can perform right now."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import ActorId, CommandId, EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.actions.registry import ActionRegistry
from wanxiang_substrate.actions.validator import ActionValidator

_PARAM_CODES = {"missing_parameter", "parameter_type"}


@dataclass(frozen=True, slots=True)
class Affordance:
    action_type: str
    available: bool
    reasons: tuple[str, ...] = ()


def compute_affordances(
    actor: EntityId,
    state: InMemoryCanonicalState,
    registry: ActionRegistry,
    validator: ActionValidator,
) -> tuple[Affordance, ...]:
    """Availability of each registered action for `actor` (no state mutation)."""
    result: list[Affordance] = []
    for definition in registry.all():
        probe_payload: dict[str, FieldValue] = {}
        if any(param.name == "actor_id" for param in definition.parameters):
            probe_payload["actor_id"] = actor.value
        probe = CommandEnvelope(
            command_id=CommandId(f"probe_{definition.action_type.replace('.', '_')}"),
            instance_id=state.instance_id,
            branch_id=state.branch_id,
            expected_revision=state.revision,
            action_type=definition.action_type,
            payload=probe_payload,
            actor_id=ActorId(actor.value) if definition.requires_actor else None,
        )
        check = validator.validate(probe, state)
        blocker_codes = [i.code for i in check.issues if i.code not in _PARAM_CODES]
        if blocker_codes:
            result.append(
                Affordance(
                    action_type=definition.action_type,
                    available=False,
                    reasons=tuple(
                        issue.message for issue in check.issues if issue.code in blocker_codes
                    ),
                )
            )
        else:
            result.append(Affordance(action_type=definition.action_type, available=True))
    return tuple(result)
