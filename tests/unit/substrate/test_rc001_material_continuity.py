"""G36D: RC-001 material/information continuity (mechanism; synthetic).

Letters/poems/gifts/medicine object continuity: instantiate, deliver, hide,
read (forms observation memory), seal, gift, consume. Synthetic objects ONLY.
"""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.material.components import custody_component, item_component
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.reading import ACTION_READ_AND_REMEMBER, register_reading_resolvers
from wanxiang_substrate.material.resolver import register_material_resolvers

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def _state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _command(action: str, payload: Mapping[str, FieldValue]) -> CommandEnvelope:
    safe = action.replace(".", "_")
    return CommandEnvelope(
        command_id=CommandId(f"cmd_{safe}"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(0),
        action_type=action,
        payload=payload,
    )


def _apply(
    state: InMemoryCanonicalState,
    resolvers: ResolverRegistry,
    action: str,
    payload: Mapping[str, FieldValue],
) -> InMemoryCanonicalState:
    return state.apply(resolvers.resolve(_command(action, payload), state))


def _resolvers() -> ResolverRegistry:
    registry = ResolverRegistry()
    register_material_resolvers(registry)
    register_reading_resolvers(registry)
    return registry


@pytest.mark.unit
def test_instantiate_deliver_seal_read_forms_memory() -> None:
    resolvers = _resolvers()
    # Package fixture: writer owns + seals; messenger holds custody.
    state = _apply(
        _state(), resolvers, "material.instantiate", {"fixture": "package", "version": 1}
    )
    state = _apply(
        state,
        resolvers,
        "material.transfer",
        {"item_id": "letter_1", "from_custodian": "messenger", "to_custodian": "recipient"},
    )
    # Reading forms an observation memory for the reader.
    state = _apply(
        state,
        resolvers,
        ACTION_READ_AND_REMEMBER,
        {"item_id": "letter_1", "reader_id": "recipient", "at_ticks": 5},
    )
    memories = EpistemicQuery(state).memories(EntityId("recipient"))
    assert memories
    assert memories[0].kind == "observation"
    assert memories[0].content_ref == "item:letter_1"
    assert memories[0].at_ticks == 5
    info = MaterialQuery(state).payload(EntityId("letter_1"))
    assert info is not None
    assert info.state == "read"


@pytest.mark.unit
def test_hide_in_container_preserves_custody_chain() -> None:
    resolvers = _resolvers()
    state = _apply(
        _state(), resolvers, "material.create_item", {"item_id": "letter_2", "kind": "letter"}
    )
    state = _apply(
        state, resolvers, "material.create_container", {"container_id": "box_2", "capacity": 2}
    )
    state = _apply(
        state,
        resolvers,
        "material.move_into_container",
        {"item_id": "letter_2", "container_id": "box_2"},
    )
    query = MaterialQuery(state)
    assert query.container_of(EntityId("letter_2")) == EntityId("box_2")


@pytest.mark.unit
def test_gift_and_medicine_continuity() -> None:
    resolvers = _resolvers()
    gift_delta = EntityCreate(
        entity_id=EntityId("gift_1"),
        entity_type="material.item",
        components=(
            item_component(EntityId("gift_1"), "gift"),
            custody_component(EntityId("gift_1"), EntityId("c1")),
        ),
    )
    state = _state().apply(ProposedWorldDelta(operations=(gift_delta,)))
    state = _apply(
        state, resolvers, "material.give_ownership", {"item_id": "gift_1", "to_owner": "c2"}
    )
    state = _apply(
        state,
        resolvers,
        "material.transfer",
        {"item_id": "gift_1", "from_custodian": "c1", "to_custodian": "c2"},
    )
    query = MaterialQuery(state)
    assert query.owner(EntityId("gift_1")) == EntityId("c2")
    assert query.custodian(EntityId("gift_1")) == EntityId("c2")
    state = _apply(
        state, resolvers, "material.create_item", {"item_id": "medicine_1", "kind": "medicine"}
    )
    state = _apply(state, resolvers, "material.consume", {"item_id": "medicine_1"})
    medicine = MaterialQuery(state).item(EntityId("medicine_1"))
    assert medicine is not None
    assert medicine.state == "consumed"
