"""G88G: committed StateDiff and projection boundary."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, ComponentId, EntityId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.playable import CommittedStateDiff, render_narrative


def _state(revision: int = 0) -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        WorldInstanceId("instance_diff"),
        BranchId("branch_diff"),
        BranchRevision(revision),
        SchemaVersion(1),
        RuntimeVersion(1),
    )


def _component(component_id: str, component_type: str, fields: dict[str, object]) -> ComponentData:
    return ComponentData(
        ComponentId(component_id),
        component_type,
        SchemaVersion(1),
        fields,  # type: ignore[arg-type]
    )


def test_diff_categories_permissions_and_replay_are_deterministic() -> None:
    before = _state()
    before = before.apply(
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    EntityId("actor_a"),
                    "person",
                    (_component("profile_a", "profile", {"display_name": "A"}),),
                ),
                EntityCreate(
                    EntityId("belief_a"),
                    "epistemic.belief",
                    (
                        _component(
                            "belief_component",
                            "epistemic.belief",
                            {"actor_id": "actor_a", "value": "old"},
                        ),
                    ),
                ),
            )
        )
    ).with_revision(BranchRevision(1))
    after = before.apply(
        ProposedWorldDelta(
            operations=(
                EntityUpdate(
                    EntityId("actor_a"),
                    (_component("profile_a", "profile", {"display_name": "A2"}),),
                ),
                EntityUpdate(
                    EntityId("belief_a"),
                    (
                        _component(
                            "belief_component",
                            "epistemic.belief",
                            {"actor_id": "actor_a", "value": "new"},
                        ),
                    ),
                ),
            )
        )
    ).with_revision(BranchRevision(2))
    diff = CommittedStateDiff.from_states(
        before, after, event_id="event_diff", viewer_actor_id="actor_a"
    )
    replay_diff = CommittedStateDiff.from_states(
        before, after, event_id="event_diff", viewer_actor_id="actor_a"
    )
    assert diff.to_dict() == replay_diff.to_dict()
    assert {change.category for change in diff.changes} == {"actor", "knowledge"}
    assert diff.no_change is False


def test_private_knowledge_is_filtered_and_narrative_cannot_change_facts() -> None:
    before = _state()
    after = before.apply(
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    EntityId("belief_b"),
                    "epistemic.belief",
                    (
                        _component(
                            "belief_b_component",
                            "epistemic.belief",
                            {"actor_id": "actor_b", "value": "private"},
                        ),
                    ),
                ),
            )
        )
    ).with_revision(BranchRevision(1))
    diff = CommittedStateDiff.from_states(before, after, viewer_actor_id="actor_a")
    assert diff.no_change is True

    @dataclass
    class Renderer:
        def render(self, diff: CommittedStateDiff) -> str:
            _ = diff
            return "a story"

    original = diff.to_dict()
    assert render_narrative(diff, Renderer()) == "a story"
    assert diff.to_dict() == original
