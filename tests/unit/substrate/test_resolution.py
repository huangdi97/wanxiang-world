"""G03E: adjudication determinism, provenance, version pinning."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.resolution.adjudicators import (
    DeterministicTransferAdjudicator,
    GambleAdjudicator,
)
from wanxiang_substrate.resolution.errors import ResolverVersionError
from wanxiang_substrate.resolution.model import ResolverVersionPin
from wanxiang_substrate.resolution.registry import AdjudicatorRegistry
from wanxiang_substrate.resolution.rng import SeededRng
from wanxiang_substrate.resolution.service import AdjudicationService


def _state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=WorldInstanceId("wld_r"),
        branch_id=BranchId("br_r"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )


def _state_with_resources() -> InMemoryCanonicalState:
    """State with source/target entities carrying material.resource components."""
    from wanxiang_substrate.resolution.adjudicators import resource_component

    state = _state()
    return state.apply(
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId("a"),
                    entity_type="person",
                    components=(resource_component(EntityId("a"), 10),),
                ),
                EntityCreate(
                    entity_id=EntityId("b"),
                    entity_type="person",
                    components=(resource_component(EntityId("b"), 0),),
                ),
            )
        )
    )


def _command(action: str, payload: Mapping[str, FieldValue]) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId("cmd_r"),
        instance_id=WorldInstanceId("wld_r"),
        branch_id=BranchId("br_r"),
        expected_revision=BranchRevision(0),
        action_type=action,
        payload=payload,
    )


@pytest.mark.unit
def test_seeded_rng_is_deterministic() -> None:
    a = SeededRng(42, stream="s").draw()
    b = SeededRng(42, stream="s").draw()
    assert a == b
    c = SeededRng(43, stream="s").draw()
    assert c != a  # different seed -> different draw (overwhelmingly)


@pytest.mark.unit
def test_gamble_same_seed_same_outcome() -> None:
    registry = AdjudicatorRegistry()
    registry.register("resolution.gamble", 1, GambleAdjudicator())
    service = AdjudicationService(registry)
    command = _command("resolution.gamble", {"actor_id": "a", "success_probability": 0.5})
    first = service.resolve(command, _state_with_resources(), seed=7)
    second = service.resolve(command, _state_with_resources(), seed=7)
    assert first.outcome == second.outcome
    assert first.delta == second.delta
    assert first.provenance and "seeded_gamble" in first.provenance[0]


@pytest.mark.unit
def test_resolver_cannot_write_store() -> None:
    registry = AdjudicatorRegistry()
    registry.register("resolution.gamble", 1, GambleAdjudicator())
    service = AdjudicationService(registry)
    state = _state_with_resources()
    before = state.semantic_hash()
    adjudication = service.resolve(_command("resolution.gamble", {"actor_id": "a"}), state, seed=1)
    # The adjudicator returns a delta only; state is untouched.
    assert state.semantic_hash() == before
    assert isinstance(adjudication.delta, object)


@pytest.mark.unit
def test_version_pinning_missing_fails() -> None:
    registry = AdjudicatorRegistry()
    registry.register("resolution.gamble", 1, GambleAdjudicator())
    service = AdjudicationService(registry)
    with pytest.raises(ResolverVersionError):
        service.resolve(
            _command("resolution.gamble", {"actor_id": "a"}),
            _state(),
            seed=1,
            pins=(ResolverVersionPin("resolution.gamble", 99),),
        )


@pytest.mark.unit
def test_deterministic_transfer_adjudication() -> None:
    registry = AdjudicatorRegistry()
    registry.register("resolution.transfer", 1, DeterministicTransferAdjudicator())
    service = AdjudicationService(registry)
    state = _state_with_resources()
    adjudication = service.resolve(
        _command("resolution.transfer", {"source_id": "a", "target_id": "b", "amount": 3}),
        state,
        seed=0,
    )
    assert adjudication.outcome == "transferred"
    assert adjudication.uncertainty == 0.0
    # Delta is compatible (dry-run apply succeeds on a copy).
    applied = state.apply(adjudication.delta)
    assert applied is not None
