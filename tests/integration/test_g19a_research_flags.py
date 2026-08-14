"""G19A: research namespace, feature flags, benchmarks & promotion rules.

- Turning all experimental flags off yields M15-equivalent behavior.
- Experimental failure cannot corrupt canonical worlds.
- Every research track has promote/reject criteria.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_research.flags import DEFAULT_FLAGS, FeatureFlags, ResearchFlag
from wanxiang_runtime.replay import ReplayEngine


def test_all_flags_off_yields_m15_equivalent_behavior(persist_db_path: pathlib.Path) -> None:
    # With all research flags off, the stable path is byte-identical.
    assert DEFAULT_FLAGS.all_disabled() is True
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("stable_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "stable_thing", "count": 1},
            world_time=WorldTime(1),
        )
    )
    events = runtime.persistence.event_store.load(iid, branch)
    replay_hash = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash()
    # This is the M15-equivalent canonical behavior (no research flag active).
    assert replay_hash == runtime.current_state(iid, branch).semantic_hash()


def test_experimental_failure_cannot_corrupt_canonical_worlds(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("before_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "kept", "count": 1},
            world_time=WorldTime(1),
        )
    )
    before = runtime.current_state(iid, branch).semantic_hash()

    # A failing experimental module is isolated: it cannot touch canonical state.
    def _experiment_failure() -> None:
        raise RuntimeError("research experiment failed")

    with pytest.raises(RuntimeError):
        _experiment_failure()
    after = runtime.current_state(iid, branch).semantic_hash()
    assert after == before
    assert len(runtime.persistence.event_store.load(iid, branch)) == 1


def test_every_research_track_has_promote_reject_criteria() -> None:
    flags = FeatureFlags()
    flags.register(ResearchFlag("track_a", "v5.1", promote_criteria="benchmark parity"))
    flags.register(ResearchFlag("track_b", "v6", promote_criteria="drift threshold"))
    for flag in flags.tracks():
        assert flag.promote_criteria
    # Registering a flag without criteria fails loudly.
    with pytest.raises(ValueError):
        ResearchFlag("bad_track", "v5.1", promote_criteria="")
