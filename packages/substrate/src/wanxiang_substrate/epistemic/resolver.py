"""Epistemic resolvers: beliefs/memories through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.epistemic.components import (
    BELIEF_COMPONENT,
    MEMORY_COMPONENT,
    belief_component,
    memory_component,
)
from wanxiang_substrate.epistemic.query import EpistemicQuery

ACTION_RECORD_OBSERVATION = "epistemic.record_observation"
ACTION_ADOPT_BELIEF = "epistemic.adopt_belief"
ACTION_CORRECT_BELIEF = "epistemic.correct_belief"
ACTION_FORGET = "epistemic.forget"
ACTION_COMPACT_MEMORY = "epistemic.compact_memory"
ACTION_GRANT_MEMORY_ACCESS = "epistemic.grant_memory_access"
ACTION_INSTANTIATE = "epistemic.instantiate"


def register_epistemic_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_RECORD_OBSERVATION, _record_observation)
    registry.register(ACTION_ADOPT_BELIEF, _adopt_belief)
    registry.register(ACTION_CORRECT_BELIEF, _correct_belief)
    registry.register(ACTION_FORGET, _forget)
    registry.register(ACTION_COMPACT_MEMORY, _compact_memory)
    registry.register(ACTION_GRANT_MEMORY_ACCESS, _grant_memory_access)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _float(payload: Mapping[str, object], key: str, default: float = 0.5) -> float:
    value = payload.get(key, default)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be a number")
    return float(value)


def _record_observation(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    memory_id = EntityId(_str(payload, "memory_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    content_ref = _str(payload, "content_ref")
    at_ticks = _int(payload, "at_ticks")
    salience = _float(payload, "salience", 0.5)
    source_obs_ref = payload.get("source_obs_ref")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=memory_id,
                entity_type="epistemic.memory",
                components=(
                    memory_component(
                        memory_id,
                        actor_id,
                        "observation",
                        content_ref,
                        at_ticks,
                        salience,
                        str(source_obs_ref) if isinstance(source_obs_ref, str) else None,
                    ),
                ),
            ),
        )
    )


def _adopt_belief(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    belief_id = EntityId(_str(payload, "belief_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    proposition = _str(payload, "proposition")
    confidence = _float(payload, "confidence", 0.5)
    at_ticks = _int(payload, "at_ticks")
    source_ref = payload.get("source_ref")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=belief_id,
                entity_type="epistemic.belief",
                components=(
                    belief_component(
                        belief_id,
                        actor_id,
                        proposition,
                        confidence,
                        at_ticks,
                        str(source_ref) if isinstance(source_ref, str) else None,
                    ),
                ),
            ),
        )
    )


def _correct_belief(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("correction requires current state")
    payload = dict(command.payload)
    old_belief_id = EntityId(_str(payload, "belief_id"))
    new_belief_id = EntityId(_str(payload, "new_belief_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    proposition = _str(payload, "proposition")
    confidence = _float(payload, "confidence", 0.8)
    at_ticks = _int(payload, "at_ticks")
    query = EpistemicQuery(state)
    old = query.belief(old_belief_id)
    if old is None:
        raise ValidationRejected(f"belief {old_belief_id.value} does not exist")
    entity = state.entity(old_belief_id)
    assert entity is not None
    current = next(
        (c for c in entity.components.values() if c.component_type == BELIEF_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected(f"entity {old_belief_id.value} is not a belief")
    fields = dict(current.fields)
    fields["status"] = "corrected"
    fields["corrected_by"] = new_belief_id.value
    corrected = ComponentData(
        component_id=current.component_id,
        component_type=BELIEF_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(entity_id=old_belief_id, components=(corrected,)),
            EntityCreate(
                entity_id=new_belief_id,
                entity_type="epistemic.belief",
                components=(
                    belief_component(
                        new_belief_id,
                        actor_id,
                        proposition,
                        confidence,
                        at_ticks,
                        None,
                        "active",
                        supersedes=old_belief_id,
                    ),
                ),
            ),
        )
    )


def _forget(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("forget requires current state")
    payload = dict(command.payload)
    memory_id = EntityId(_str(payload, "memory_id"))
    entity = state.entity(memory_id)
    if entity is None:
        raise ValidationRejected(f"memory {memory_id.value} does not exist")
    current = next(
        (c for c in entity.components.values() if c.component_type == MEMORY_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected(f"entity {memory_id.value} is not a memory")
    fields = dict(current.fields)
    fields["forgotten"] = True
    updated = ComponentData(
        component_id=current.component_id,
        component_type=MEMORY_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(EntityUpdate(entity_id=memory_id, components=(updated,)),)
    )


def _compact_memory(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("compaction requires current state")
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    keep = _int(payload, "keep", 10)
    query = EpistemicQuery(state)
    memories = query.memories(actor_id, include_forgotten=True)
    if len(memories) <= keep:
        return ProposedWorldDelta()
    updates: list[EntityUpdate] = []
    for memory in memories[keep:]:
        entity = state.entity(memory.memory_id)
        assert entity is not None
        current = next(
            (c for c in entity.components.values() if c.component_type == MEMORY_COMPONENT), None
        )
        if current is None:
            continue
        fields = dict(current.fields)
        fields["forgotten"] = True
        updates.append(
            EntityUpdate(
                entity_id=memory.memory_id,
                components=(
                    ComponentData(
                        component_id=current.component_id,
                        component_type=MEMORY_COMPONENT,
                        schema_version=current.schema_version,
                        fields=fields,
                    ),
                ),
            )
        )
    return ProposedWorldDelta(operations=tuple(updates))


def _grant_memory_access(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    from wanxiang_substrate.epistemic.components import memory_access_component

    payload = dict(command.payload)
    owner_id = EntityId(_str(payload, "owner_id"))
    authorized = EntityId(_str(payload, "authorized_actor"))
    grant_id = EntityId(f"access_{owner_id.value}_{authorized.value}")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=grant_id,
                entity_type="epistemic.memory_access",
                components=(memory_access_component(owner_id, authorized),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic epistemic fixture."""
    from wanxiang_substrate.epistemic.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
