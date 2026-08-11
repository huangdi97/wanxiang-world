"""GOAL_01A: command/proposal/commit distinction and delta typing."""

from __future__ import annotations

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ContractError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, EntityId, EventId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


def _command(**overrides: object) -> CommandEnvelope:
    values: dict[str, object] = {
        "command_id": CommandId("cmd_1"),
        "instance_id": WorldInstanceId("wld_1"),
        "branch_id": BranchId("br_1"),
        "expected_revision": BranchRevision(0),
        "action_type": "transfer_resource",
        "payload": {"target": "ent_b", "amount": 3},
    }
    values.update(overrides)
    return CommandEnvelope(**values)  # type: ignore[arg-type]


@pytest.mark.unit
def test_command_envelope_requires_action_type() -> None:
    with pytest.raises(ContractError):
        _command(action_type="")


@pytest.mark.unit
def test_proposal_is_distinct_from_committed_event() -> None:
    delta = ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId("ent_a"),
                entity_type="token_holder",
                components=(
                    ComponentData(
                        component_type="resource",
                        schema_version=SchemaVersion(1),
                        fields={"count": 5},
                    ),
                ),
            ),
        )
    )
    assert delta.is_empty() is False
    event = CommittedEvent(
        event_id=EventId("evt_1"),
        instance_id=WorldInstanceId("wld_1"),
        branch_id=BranchId("br_1"),
        event_seq=EventSeq(1),
        revision=BranchRevision(1),
        schema_version=SchemaVersion(1),
        command_id=CommandId("cmd_1"),
        delta=delta,
        world_time=WorldTime(1),
        rule_version=RuntimeVersion(1),
    )
    assert isinstance(event.delta, ProposedWorldDelta)
    assert event.revision.value == 1


@pytest.mark.unit
def test_empty_delta_is_empty() -> None:
    assert ProposedWorldDelta().is_empty() is True


@pytest.mark.unit
def test_entity_update_keeps_identity() -> None:
    update = EntityUpdate(
        entity_id=EntityId("ent_a"),
        components=(ComponentData("status", SchemaVersion(1), {"active": True}),),
    )
    assert update.entity_id == EntityId("ent_a")
