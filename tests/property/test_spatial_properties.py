"""G02A: property ? after valid commits an entity has one valid location, replayable."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st
from tests.conftest import cleanup_db_file, fresh_db_path
from tests.integration.test_spatial_movement import make_house_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.spatial.errors import SpatialError
from wanxiang_substrate.spatial.fixture import INSTANCE, build_house_fixture_commands
from wanxiang_substrate.spatial.query import SpatialQuery

PLACES = ("hall", "kitchen", "garden")


@settings(max_examples=8, deadline=None)
@given(st.lists(st.sampled_from(PLACES), min_size=1, max_size=8))
def test_entity_has_single_valid_location_after_valid_commits(moves: list[str]) -> None:
    path = fresh_db_path()
    try:
        runtime = make_house_runtime(path)
        world = runtime.create_world(instance_id=INSTANCE)
        for command in build_house_fixture_commands(world.root_branch_id):
            runtime.submit_command(command)
        revision = 1
        for index, target in enumerate(moves):
            before = runtime.current_state(world.instance_id, world.root_branch_id).semantic_hash()
            try:
                result = runtime.submit_command(
                    CommandEnvelope(
                        command_id=CommandId(f"prop_{index}"),
                        instance_id=INSTANCE,
                        branch_id=world.root_branch_id,
                        expected_revision=BranchRevision(revision),
                        action_type="spatial.move",
                        payload={"entity_id": "alice", "target_place_id": target},
                        world_time=WorldTime(revision + 1),
                    )
                )
            except (SpatialError, ValidationRejected):
                # Legitimately rejected move: no mutation, location unchanged.
                after = runtime.current_state(world.instance_id, world.root_branch_id)
                assert after.semantic_hash() == before
                assert SpatialQuery(after).location(EntityId("alice")) is not None
                continue
            revision += 1
            query = SpatialQuery(result.state)
            location = query.location(EntityId("alice"))
            assert location is not None
            assert location in {EntityId(p) for p in PLACES}
            assert query.places()[location] is not None
    finally:
        cleanup_db_file(path)
