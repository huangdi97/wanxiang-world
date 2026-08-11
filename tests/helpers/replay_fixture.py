"""Deterministic synthetic replay fixture (explicitly synthetic).

Builds a small token-transfer scenario: two entities with a resource component
and a gift relation, committed across 5 events. Used by golden replay tests and
the M1 acceptance scenario.
"""

from __future__ import annotations

from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta, RelationCreate
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    EventId,
    RelationId,
    WorldInstanceId,
)
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

INSTANCE = WorldInstanceId("wld_golden")
BRANCH = BranchId("br_golden")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def build_fixture_events() -> tuple[CommittedEvent, ...]:
    """Five deterministic events ending at revision 5."""
    events: list[CommittedEvent] = []
    specs = [
        (
            "evt_1",
            "cmd_1",
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("alice"),
                        entity_type="person",
                        components=(
                            ComponentData(
                                component_id=ComponentId("alice_res"),
                                component_type="resource",
                                schema_version=SCHEMA,
                                fields={"count": 10},
                            ),
                        ),
                    ),
                )
            ),
        ),
        (
            "evt_2",
            "cmd_2",
            ProposedWorldDelta(
                operations=(
                    EntityCreate(
                        entity_id=EntityId("bob"),
                        entity_type="person",
                        components=(
                            ComponentData(
                                component_id=ComponentId("bob_res"),
                                component_type="resource",
                                schema_version=SCHEMA,
                                fields={"count": 0},
                            ),
                        ),
                    ),
                )
            ),
        ),
        (
            "evt_3",
            "cmd_3",
            ProposedWorldDelta(
                operations=(
                    EntityUpdate(
                        entity_id=EntityId("alice"),
                        components=(
                            ComponentData(
                                component_id=ComponentId("alice_res"),
                                component_type="resource",
                                schema_version=SCHEMA,
                                fields={"count": 7},
                            ),
                        ),
                    ),
                )
            ),
        ),
        (
            "evt_4",
            "cmd_4",
            ProposedWorldDelta(
                operations=(
                    EntityUpdate(
                        entity_id=EntityId("bob"),
                        components=(
                            ComponentData(
                                component_id=ComponentId("bob_res"),
                                component_type="resource",
                                schema_version=SCHEMA,
                                fields={"count": 3},
                            ),
                        ),
                    ),
                )
            ),
        ),
        (
            "evt_5",
            "cmd_5",
            ProposedWorldDelta(
                operations=(
                    RelationCreate(
                        relation_id=RelationId("gift_1"),
                        relation_type="gift",
                        source_id=EntityId("alice"),
                        target_id=EntityId("bob"),
                        attributes={"since": 1},
                    ),
                )
            ),
        ),
    ]
    for index, (event_id, command_id, delta) in enumerate(specs, start=1):
        events.append(
            CommittedEvent(
                event_id=EventId(event_id),
                instance_id=INSTANCE,
                branch_id=BRANCH,
                event_seq=EventSeq(index),
                revision=BranchRevision(index),
                schema_version=SCHEMA,
                command_id=CommandId(command_id),
                delta=delta,
                world_time=WorldTime(index),
                rule_version=RULES,
            )
        )
    return tuple(events)
