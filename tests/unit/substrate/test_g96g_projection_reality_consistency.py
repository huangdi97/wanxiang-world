"""G96G: provider output is checked against canonical read models only."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.world_lab import (
    ActorPerspective,
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    RealityConsistencyChecker,
    ReferencePhysicalProvider,
    ReferenceVisualProvider,
    VisualProjectedObject,
    VisualSceneObject,
    VisualSceneState,
)


def _scene() -> VisualSceneState:
    return VisualSceneState(
        scene_ref="scene:g96g",
        snapshot_ref="snapshot:g96g",
        world_instance_ref="world:g96g",
        branch_ref="branch:g96g",
        revision=5,
        world_time_ticks=20,
        state_hash="statehash:g96g",
        objects=(
            VisualSceneObject(
                object_ref="object:g96g:alice",
                entity_ref="entity:g96g:alice",
                position=(1.0, 0.0),
                audience_refs=("actor:alice",),
                event_refs=("event:g96g:alice",),
            ),
            VisualSceneObject(
                object_ref="object:g96g:public",
                entity_ref="entity:g96g:public",
                position=(0.0, 1.0),
                event_refs=("event:g96g:public",),
            ),
        ),
        event_refs=("event:g96g:alice", "event:g96g:public"),
    )


def _frame(scene: VisualSceneState):
    return ReferenceVisualProvider("provider:g96g", "1.0.0").project(
        scene,
        ActorPerspective(
            perspective_ref="perspective:g96g:alice",
            actor_ref="actor:alice",
            origin=(0.0, 0.0),
            view_radius=3.0,
        ),
    )


def _physical_snapshot() -> PhysicalSnapshot:
    return PhysicalSnapshot(
        snapshot_ref="snapshot:g96g:physical",
        world_instance_ref="world:g96g",
        branch_ref="branch:g96g",
        revision=5,
        world_time_ticks=20,
        state_hash="statehash:g96g:physical",
        bodies=(
            PhysicalBody(
                body_ref="entity_g96g_actor",
                position=(0.0, 0.0),
                velocity=(1.0, 0.0),
                radius=0.1,
            ),
        ),
    )


def test_visual_consistency_round_trips_and_retains_empty_proposal() -> None:
    scene = _scene()
    result = RealityConsistencyChecker().check_visual(scene, _frame(scene))

    assert result.is_consistent
    assert result.mismatch_codes == ()
    assert result.proposal.action == "retain"
    assert result.proposal.proposed_delta.is_empty()
    assert RealityConsistencyChecker().check(scene, _frame(scene)) == result
    assert (
        result.replay_hash
        == RealityConsistencyChecker().check_visual(scene, _frame(scene)).replay_hash
    )
    assert type(result).from_dict(result.to_dict()) == result


def test_stale_and_hallucinated_visual_outputs_never_become_reality() -> None:
    scene = _scene()
    frame = _frame(scene)
    stale = replace(frame, snapshot_revision=scene.revision - 1)
    stale_result = RealityConsistencyChecker().check_visual(scene, stale)
    assert stale_result.status == "stale"
    assert stale_result.proposal.action == "refresh_projection"
    assert stale_result.proposal.proposed_delta.is_empty()

    hallucinated = VisualProjectedObject(
        object_ref="object:g96g:hallucinated",
        entity_ref="entity:g96g:hallucinated",
        position=(2.0, 2.0),
    )
    divergent = replace(frame, objects=frame.objects + (hallucinated,))
    divergent_result = RealityConsistencyChecker().check_visual(scene, divergent)
    assert divergent_result.status == "divergent"
    assert "unknown_object_ref" in divergent_result.mismatch_codes
    assert divergent_result.proposal.action == "review"
    assert divergent_result.proposal.proposed_delta.is_empty()


def test_physical_resolution_checks_snapshot_revision_and_proposes_recompute() -> None:
    snapshot = _physical_snapshot()
    request = PhysicalSimulationRequest(
        request_id="request:g96g",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        actor_ref="entity_g96g_actor",
        action="step",
        step_ticks=1,
    )
    resolution = ReferencePhysicalProvider("provider:g96g:physical", "1.0.0").simulate(
        snapshot, request
    )
    checker = RealityConsistencyChecker()
    assert checker.check_physical(snapshot, resolution).status == "consistent"
    stale_snapshot = replace(snapshot, revision=snapshot.revision + 1)
    stale = checker.check_physical(stale_snapshot, resolution)
    assert stale.status == "stale"
    assert stale.proposal.action == "recompute_physical"
    assert stale.proposal.proposed_delta.is_empty()
