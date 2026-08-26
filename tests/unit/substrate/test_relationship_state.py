"""G89E: time/event relationship state and actor-scoped visibility."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.actor_continuity import (
    RelationshipDimensions,
    RelationshipGraph,
    RelationshipState,
)


def relation(
    ref: str, *, at: int, trust: float, visibility: str = "participants"
) -> RelationshipState:
    return RelationshipState(
        relationship_id="rel_ab",
        source_actor_id=EntityId("actor_a"),
        target_actor_id=EntityId("actor_b"),
        relation_type="ally",
        dimensions=RelationshipDimensions(trust=trust),
        valid_from=at,
        event_refs=(ref,),
        visibility=visibility,  # type: ignore[arg-type]
    )


@pytest.mark.unit
def test_relationship_evolution_replays_and_is_time_scoped() -> None:
    graph, created = RelationshipGraph().add(
        relation("evt:formed", at=1, trust=0.2),
        event_ref="rev:1",
        at_ticks=1,
        reason="formed after a shared task",
    )
    graph, revised = graph.revise(
        relation("evt:helped", at=5, trust=0.8),
        event_ref="rev:2",
        at_ticks=5,
        reason="help increased trust",
    )
    replayed = RelationshipGraph.replay((created, revised))
    assert replayed.state("rel_ab", at_ticks=2).dimensions.trust == 0.2  # type: ignore[union-attr]
    assert replayed.state("rel_ab", at_ticks=6).dimensions.trust == 0.8  # type: ignore[union-attr]
    assert replayed.revisions == graph.revisions
    assert replayed.revisions[1].before == graph.revisions[1].before


@pytest.mark.unit
def test_private_relationship_is_not_globally_visible() -> None:
    graph, _ = RelationshipGraph().add(
        relation("evt:private", at=1, trust=0.5, visibility="source"),
        event_ref="rev:private",
        at_ticks=1,
        reason="private source view",
    )
    assert graph.visible_to(EntityId("actor_a"))
    assert graph.visible_to(EntityId("actor_b")) == ()
    assert graph.visible_to(EntityId("observer")) == ()
    assert graph.visible_to(EntityId("observer"), admin=True)
    with pytest.raises(ContractError):
        RelationshipDimensions(trust=1.1)
