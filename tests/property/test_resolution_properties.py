"""G03E: property ? same input+seed+version gives same adjudication."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.resolution.adjudicators import GambleAdjudicator
from wanxiang_substrate.resolution.registry import AdjudicatorRegistry
from wanxiang_substrate.resolution.service import AdjudicationService

_INSTANCE = WorldInstanceId("wld_prop")


def _state() -> InMemoryCanonicalState:
    from wanxiang_substrate.resolution.adjudicators import resource_component

    base = InMemoryCanonicalState(
        instance_id=_INSTANCE,
        branch_id=BranchId("br_prop"),
        revision=BranchRevision(0),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    return base.apply(
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=EntityId("a"),
                    entity_type="person",
                    components=(resource_component(EntityId("a"), 10),),
                ),
            )
        )
    )


@settings(max_examples=10, deadline=None)
@given(
    st.integers(min_value=0, max_value=10**6),
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False),
)
def test_gamble_reproducible_for_seed_and_probability(seed: int, probability: float) -> None:
    registry = AdjudicatorRegistry()
    registry.register("resolution.gamble", 1, GambleAdjudicator())
    service = AdjudicationService(registry)
    command = CommandEnvelope(
        command_id=CommandId("cmd_prop"),
        instance_id=_INSTANCE,
        branch_id=BranchId("br_prop"),
        expected_revision=BranchRevision(0),
        action_type="resolution.gamble",
        payload={"actor_id": "a", "success_probability": probability},  # type: ignore[arg-type]
    )
    first = service.resolve(command, _state(), seed=seed)
    second = service.resolve(command, _state(), seed=seed)
    assert first.outcome == second.outcome
    assert first.delta == second.delta
