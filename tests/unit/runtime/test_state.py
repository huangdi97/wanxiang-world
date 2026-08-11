"""GOAL_01B: immutable canonical state and pure delta application."""

from __future__ import annotations

import pytest
from tests.unit.runtime.conftest import SCHEMA, make_create_delta
from wanxiang_domain.delta import EntityDelete, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import Conflict, ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta


@pytest.mark.unit
def test_apply_create_derives_new_state_without_mutating_input(
    empty_state: InMemoryCanonicalState,
) -> None:
    delta = make_create_delta()
    derived = apply_delta(empty_state, delta)
    assert derived.entity(EntityId("ent_a")) is not None
    assert empty_state.entity(EntityId("ent_a")) is None
    assert derived.revision == empty_state.revision


@pytest.mark.unit
def test_no_public_mutator_on_canonical_state(empty_state: InMemoryCanonicalState) -> None:
    for name in ("_entities", "_relations"):
        assert hasattr(empty_state, name)
    public = [n for n in dir(empty_state) if not n.startswith("_")]
    assert "entity" in public and "entities" in public
    assert "apply" in public and "with_revision" in public
    assert "semantic_hash" in public


@pytest.mark.unit
def test_update_merges_components_by_id(empty_state: InMemoryCanonicalState) -> None:
    state = apply_delta(empty_state, make_create_delta())
    update = ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=EntityId("ent_a"),
                components=(
                    ComponentData(
                        component_id=ComponentId("cmp_ent_a"),
                        component_type="resource",
                        schema_version=SCHEMA,
                        fields={"count": 9},
                    ),
                ),
            ),
        )
    )
    updated = apply_delta(state, update)
    updated_entity = updated.entity(EntityId("ent_a"))
    assert updated_entity is not None
    component = updated_entity.components[ComponentId("cmp_ent_a")]
    assert component.fields["count"] == 9
    prior_entity = state.entity(EntityId("ent_a"))
    assert prior_entity is not None
    prior = prior_entity.components[ComponentId("cmp_ent_a")]
    assert prior.fields["count"] == 5


@pytest.mark.unit
def test_duplicate_entity_create_is_conflict(empty_state: InMemoryCanonicalState) -> None:
    state = apply_delta(empty_state, make_create_delta())
    with pytest.raises(Conflict):
        apply_delta(state, make_create_delta())


@pytest.mark.unit
def test_update_missing_entity_is_validation_rejected(empty_state: InMemoryCanonicalState) -> None:
    delta = ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=EntityId("nope"),
                components=(ComponentData(ComponentId("c1"), "resource", SCHEMA),),
            ),
        )
    )
    with pytest.raises(ValidationRejected):
        apply_delta(empty_state, delta)


@pytest.mark.unit
def test_delete_missing_entity_is_validation_rejected(empty_state: InMemoryCanonicalState) -> None:
    delta = ProposedWorldDelta(operations=(EntityDelete(entity_id=EntityId("nope")),))
    with pytest.raises(ValidationRejected):
        apply_delta(empty_state, delta)


@pytest.mark.unit
def test_semantic_hash_stable_and_revision_sensitive(empty_state: InMemoryCanonicalState) -> None:
    state = apply_delta(empty_state, make_create_delta())
    assert state.semantic_hash() == state.semantic_hash()
    bumped = state.with_revision(BranchRevision(1))
    assert bumped.semantic_hash() != state.semantic_hash()
