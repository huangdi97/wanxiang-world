"""G30A: Reality Root semantic contract invariants.

The five primitives (Distinction, Relation, Transition, Commitment, History)
must be expressible with the existing core types, must be free of
physical/magical/domain rules, and must build a minimal synthetic world through
the single commit boundary with append-only, replayable history.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA, build_fixture_events
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta, RelationCreate
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import (
    CommandId,
    ComponentId,
    EntityId,
    RelationId,
)
from wanxiang_domain.reality_root import REALITY_ROOT_SEMANTICS
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.state import InMemoryCanonicalState

ROOT = pathlib.Path(__file__).resolve().parents[3]


@pytest.mark.unit
def test_five_semantics_documented_without_domain_rules() -> None:
    names = [m.name for m in REALITY_ROOT_SEMANTICS]
    assert names == ["Distinction", "Relation", "Transition", "Commitment", "History"]
    assert all(m.no_domain_rules for m in REALITY_ROOT_SEMANTICS)
    # The Reality Root module must not import domain-rule machinery.
    source = (ROOT / "packages/domain/src/wanxiang_domain/reality_root.py").read_text(
        encoding="utf-8"
    )
    import_lines = [ln for ln in source.splitlines() if ln.strip().startswith(("import ", "from "))]
    for forbidden in (
        "spatial",
        "temporal",
        "body",
        "institution",
        "material",
        "population",
        "agency",
        "skill",
        "epistemic",
    ):
        assert not any(forbidden in ln for ln in import_lines), (
            f"Reality Root must not import {forbidden!r}"
        )


@pytest.mark.unit
def test_distinction_maps_to_entity_identity() -> None:
    from wanxiang_runtime.state import apply_delta

    state = apply_delta(
        InMemoryCanonicalState(
            instance_id=INSTANCE,
            branch_id=BRANCH,
            revision=BranchRevision(0),
            schema_version=SCHEMA,
            rule_version=RULES,
        ),
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId("stone"),
                    entity_type="thing",
                    components=(
                        ComponentData(
                            component_id=ComponentId("stone_weight"),
                            component_type="weight",
                            schema_version=SCHEMA,
                            fields={"value": 3},
                        ),
                    ),
                ),
            )
        ),
    )
    entity = state.entity(EntityId("stone"))
    assert entity is not None
    assert entity.entity_type == "thing"
    assert entity.components[ComponentId("stone_weight")].fields == {"value": 3}


@pytest.mark.unit
def test_relation_links_two_distinctions() -> None:
    from wanxiang_runtime.state import apply_delta

    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    state = apply_delta(
        base,
        ProposedWorldDelta(
            operations=(
                EntityCreate(entity_id=EntityId("a"), entity_type="person"),
                EntityCreate(entity_id=EntityId("b"), entity_type="person"),
            )
        ),
    )
    state = apply_delta(
        state,
        ProposedWorldDelta(
            operations=(
                RelationCreate(
                    relation_id=RelationId("r1"),
                    relation_type="gift",
                    source_id=EntityId("a"),
                    target_id=EntityId("b"),
                    attributes={"since": 1},
                ),
            )
        ),
    )
    relation = state.relation(RelationId("r1"))
    assert relation is not None
    assert relation.source_id == EntityId("a")
    assert relation.target_id == EntityId("b")


@pytest.mark.unit
def test_transition_is_a_committed_event() -> None:
    events = build_fixture_events()
    assert len(events) == 5
    for index, event in enumerate(events, start=1):
        assert event.event_seq.value == index
        assert event.delta.operations  # a transition carries an atomic delta
    final = ReplayEngine(RULES, SCHEMA).replay(events)
    assert final.revision.value == 5


@pytest.mark.unit
def test_commitment_is_single_boundary() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    result = authority.commit(
        state,
        CommitRequest(
            command_id=CommandId("cmd_root_1"),
            instance_id=INSTANCE,
            branch_id=BRANCH,
            expected_revision=BranchRevision(0),
            delta=ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId("a"), entity_type="thing"),)
            ),
            world_time=WorldTime(1),
            rule_version=RULES,
        ),
    )
    assert result.event.revision.value == 1
    assert result.state_after.revision.value == 1
    # History is append-only: the store exposes the exact committed stream.
    assert store.load(INSTANCE, BRANCH) == (result.event,)


@pytest.mark.unit
def test_history_is_append_only_and_replayable() -> None:
    events = build_fixture_events()
    first = ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()
    second = ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()
    assert first == second
    # Structural check: replay of the same stream is deterministic and the
    # committed events are frozen value objects (append-only by construction).
    from dataclasses import is_dataclass

    assert is_dataclass(events[0])
    assert first == ReplayEngine(RULES, SCHEMA).replay(events).semantic_hash()


@pytest.mark.unit
def test_minimal_synthetic_world_via_contract() -> None:
    """Any world type can build a minimal synthetic world via the contract."""
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    # Distinction + Relation through the single boundary.
    for index, delta in enumerate(
        (
            ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
            ),
            ProposedWorldDelta(
                operations=(EntityCreate(entity_id=EntityId("bob"), entity_type="person"),)
            ),
            ProposedWorldDelta(
                operations=(
                    RelationCreate(
                        relation_id=RelationId("gift"),
                        relation_type="gift",
                        source_id=EntityId("alice"),
                        target_id=EntityId("bob"),
                    ),
                )
            ),
        ),
        start=1,
    ):
        result = authority.commit(
            state,
            CommitRequest(
                command_id=CommandId(f"cmd_min_{index}"),
                instance_id=INSTANCE,
                branch_id=BRANCH,
                expected_revision=BranchRevision(index - 1),
                delta=delta,
                world_time=WorldTime(index),
                rule_version=RULES,
            ),
        )
        state = result.state_after
    history = store.load(INSTANCE, BRANCH)
    assert len(history) == 3
    rebuilt = ReplayEngine(RULES, SCHEMA).replay(history)
    assert rebuilt.relation(RelationId("gift")) is not None
    assert rebuilt.entity(EntityId("alice")) is not None
    assert rebuilt.entity(EntityId("bob")) is not None
