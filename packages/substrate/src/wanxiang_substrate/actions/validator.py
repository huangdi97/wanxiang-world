"""Side-effect-free ActionValidator: reject impossible/unauthorized/epistemic
actions before resolution."""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.ids import ActorId, EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.actions.model import ActionDefinition, ValidationIssue, ValidationResult
from wanxiang_substrate.actions.registry import ActionRegistry
from wanxiang_substrate.agency.query import AgencyQuery
from wanxiang_substrate.body.query import BodyQuery
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.spatial.query import SpatialQuery


class ActionValidator:
    """Validates a command against the current state (pure, no mutation)."""

    def __init__(self, registry: ActionRegistry) -> None:
        self._registry = registry

    def validate(self, command: CommandEnvelope, state: InMemoryCanonicalState) -> ValidationResult:
        issues: list[ValidationIssue] = []
        definition = self._registry.get(command.action_type)
        if definition is None:
            return ValidationResult.failure(
                (
                    ValidationIssue(
                        "unknown_action", f"action {command.action_type!r} is not defined"
                    ),
                )
            )
        issues.extend(_check_parameters(definition, command))
        if definition.requires_actor and command.actor_id is not None:
            issues.extend(_check_actor(command.actor_id, state))
            issues.extend(_check_permission(definition, command.actor_id, state))
            issues.extend(_check_reachability(command, state))
            issues.extend(_check_epistemic(command, state))
        issues.extend(_check_resources(command, state))
        return ValidationResult.success() if not issues else ValidationResult.failure(tuple(issues))


def _check_parameters(
    definition: ActionDefinition, command: CommandEnvelope
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for spec in definition.parameters:
        value = command.payload.get(spec.name)
        if value is None:
            if spec.required:
                issues.append(ValidationIssue("missing_parameter", f"missing {spec.name!r}"))
            continue
        if not _matches_type(value, spec.type):
            issues.append(
                ValidationIssue(
                    "parameter_type",
                    f"parameter {spec.name!r} must be {spec.type}",
                )
            )
    return tuple(issues)


def _matches_type(value: object, type_name: str) -> bool:
    if type_name == "str":
        return isinstance(value, str)
    if type_name == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_name == "bool":
        return isinstance(value, bool)
    return False


def _check_actor(actor_id: ActorId, state: InMemoryCanonicalState) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    actor = EntityId(actor_id.value)
    if state.entity(actor) is None:
        issues.append(ValidationIssue("actor_missing", f"actor {actor.value} does not exist"))
    elif not AgencyQuery(state).is_active(actor):
        issues.append(ValidationIssue("actor_inactive", f"actor {actor.value} is inactive"))
    return tuple(issues)


def _check_permission(
    definition: ActionDefinition, actor_id: ActorId, state: InMemoryCanonicalState
) -> tuple[ValidationIssue, ...]:
    if definition.permission is None:
        return ()
    actor = EntityId(actor_id.value)
    now = _now_ticks(state)
    if (
        not InstitutionQuery(state, now_ticks=now)
        .check_permission(actor, definition.permission)
        .allow
    ):
        return (ValidationIssue("permission_denied", f"actor lacks {definition.permission!r}"),)
    return ()


def _check_reachability(
    command: CommandEnvelope, state: InMemoryCanonicalState
) -> tuple[ValidationIssue, ...]:
    if command.action_type != "spatial.move" or command.actor_id is None:
        return ()
    actor = EntityId(command.actor_id.value)
    target_raw = command.payload.get("target_place_id")
    if not isinstance(target_raw, str):
        return ()
    query = SpatialQuery(state)
    current = query.location(actor)
    target = EntityId(target_raw)
    if current is None or not query.reachable(current, target, ignore_locked=False):
        return (ValidationIssue("not_reachable", f"{target_raw} is not reachable from {current}"),)
    return ()


def _check_epistemic(
    command: CommandEnvelope, state: InMemoryCanonicalState
) -> tuple[ValidationIssue, ...]:
    if command.action_type == "material.read_payload":
        item_raw = command.payload.get("item_id")
        if not isinstance(item_raw, str):
            return ()
        item = EntityId(item_raw)
        material = MaterialQuery(state)
        if material.payload(item) is None:
            return (ValidationIssue("no_payload", f"item {item_raw} has no payload"),)
        # Actor must have knowledge of the item (custody or an observation memory).
        actor = EntityId(command.actor_id.value) if command.actor_id else None
        if actor is None:
            return (ValidationIssue("no_actor", "read_payload requires an actor"),)
        if material.custodian(item) == actor:
            return ()
        epistemic = EpistemicQuery(state)
        if any(item_raw in m.content_ref for m in epistemic.memories(actor)):
            return ()
        return (ValidationIssue("no_knowledge", f"actor has no knowledge of {item_raw}"),)
    return ()


def _check_resources(
    command: CommandEnvelope, state: InMemoryCanonicalState
) -> tuple[ValidationIssue, ...]:
    if command.action_type == "body.rest":
        actor_raw = command.payload.get("actor_id")
        if isinstance(actor_raw, str):
            actor = EntityId(actor_raw)
            if BodyQuery(state).condition(actor) is None:
                return (ValidationIssue("no_body", f"actor {actor_raw} has no body condition"),)
    return ()


def _now_ticks(state: InMemoryCanonicalState) -> int:
    from wanxiang_substrate.temporal.query import TemporalQuery

    return TemporalQuery(state).now()
