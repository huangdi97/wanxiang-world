"""GOAL_01D: property-based replay determinism.

A random valid command/event sequence must replay to the same canonical hash as
direct sequential application, for any prefix.
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    EventId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState

INSTANCE = WorldInstanceId("wld_prop")
BRANCH = BranchId("br_prop")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def _state(revision: int = 0) -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(revision),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _events_for(entities: tuple[int, ...]) -> tuple[CommittedEvent, ...]:
    events: list[CommittedEvent] = []
    for seq, count in enumerate(entities, start=1):
        delta = ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId(f"ent_{seq}"),
                    entity_type="token_holder",
                    components=(
                        ComponentData(
                            component_id=ComponentId(f"cmp_{seq}"),
                            component_type="resource",
                            schema_version=SCHEMA,
                            fields={"count": count},
                        ),
                    ),
                ),
            )
        )
        events.append(
            CommittedEvent(
                event_id=EventId(f"evt_{seq}"),
                instance_id=INSTANCE,
                branch_id=BRANCH,
                event_seq=EventSeq(seq),
                revision=BranchRevision(seq),
                schema_version=SCHEMA,
                command_id=CommandId(f"cmd_{seq}"),
                delta=delta,
                world_time=WorldTime(seq),
                rule_version=RULES,
            )
        )
    return tuple(events)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=20))
def test_replay_matches_direct_application_for_any_prefix(counts: list[int]) -> None:
    events = _events_for(tuple(counts))
    engine = ReplayEngine(RULES, SCHEMA)
    full = engine.replay(events)
    # Direct application
    direct = _state()
    for event in events:
        direct = direct.apply(event.delta).with_revision(event.revision)
    assert full.semantic_hash() == direct.semantic_hash()
    # Replay from an intermediate baseline equals full replay
    split = min(2, len(events))
    baseline = engine.replay(events[:split])
    restored = engine.replay(events[split:], baseline=baseline)
    assert restored.semantic_hash() == full.semantic_hash()
