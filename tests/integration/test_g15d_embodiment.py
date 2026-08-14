"""G15D: human embodiment, exit, re-entry & control continuity qualification.

Scenario: a human takes over a body, acts (normal committed command), exits;
the world advances autonomously; shadow advice is recorded; a conflicting
takeover is rejected; re-entry receives the authoritative current perspective.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PACK = ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"


def _load_sf() -> Any:
    spec = importlib.util.spec_from_file_location("synthetic_full", PACK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sf() -> Any:
    return _load_sf()


def _session(session_id: str, controller: str) -> Any:
    from wanxiang_domain.ids import WorldInstanceId
    from wanxiang_substrate.session.model import Session

    return Session(
        session_id=session_id,
        controller=controller,
        instance_id=WorldInstanceId("wld_sf"),
        mode="embody",
        created_seq=1,
    )


def test_embodiment_exit_reentry_control_continuity(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.population.scheduler import AutonomousScheduler
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService
    from wanxiang_substrate.session.control import ControlHandoff, ShadowPolicy
    from wanxiang_substrate.session.errors import LeaseConflict
    from wanxiang_substrate.session.service import LeaseService

    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    iid, branch = sf.INSTANCE, w.root_branch_id

    # 1) Human takes over the mayor (embodiment lease).
    leases = LeaseService()
    session_a = _session("s_human_1", "human-client")
    leases.acquire(session_a, sf.MAYOR.value, "lease_h1", acquired_seq=1, expires_seq=100)
    assert leases.primary_controller(sf.MAYOR.value) == "s_human_1"

    # Human commands are normal committed actions (through Commit Authority).
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    result = runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("human_act_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(1),
            action_type="temporal.advance",
            payload={"ticks": 10},
            world_time=WorldTime(2),
            actor_id=sf.MAYOR,
        )
    )
    assert result.duplicate is False and result.event is not None

    # Shadow policy: advice is recorded while the human controls.
    shadow = ShadowPolicy()
    advice = shadow.advise(sf.MAYOR.value, "guard the gate", advice_seq=1)
    assert any("guard the gate" in a for a in advice)
    assert any("guard the gate" in h for h in shadow.history(sf.MAYOR.value))

    # 2) Conflicting takeover is rejected (one primary controller).
    session_b = _session("s_human_2", "human-client-2")
    with pytest.raises(LeaseConflict):
        leases.acquire(session_b, sf.MAYOR.value, "lease_h2", acquired_seq=2, expires_seq=200)

    # 3) Human exits; the world keeps advancing autonomously.
    handoff = ControlHandoff()
    handoff.acquire(sf.MAYOR.value, "s_human_1")
    leases.release("lease_h1", released_seq=5)
    assert leases.primary_controller(sf.MAYOR.value) is None
    handoff.hand_back(sf.MAYOR.value, last_commit_seq=5)
    handoff.resume(sf.MAYOR.value)
    before = runtime.current_state(iid, branch).revision.value
    scheduler = AutonomousScheduler(runtime, seed=77)
    scheduler.run(iid, branch, horizon_ticks=sf.DAY)
    after = runtime.current_state(iid, branch).revision.value
    assert after > before, "world must advance after user exit"

    # 4) Re-entry receives the authoritative current perspective.
    session_c = _session("s_human_3", "human-client-3")
    leases.acquire(
        session_c, sf.MAYOR.value, "lease_h3", acquired_seq=after, expires_seq=after + 100
    )
    assert leases.primary_controller(sf.MAYOR.value) == "s_human_3"
    state = runtime.current_state(iid, branch)
    snap = ProjectionService(state).compose(
        ProjectionRequest(
            session_id="s_human_3", actor_id=sf.MAYOR.value, branch_id=branch, mode="text"
        )
    )
    assert snap.revision == after
    ids = {i.entity_id for i in snap.items}
    assert sf.MAYOR.value in ids
    # The re-entering human sees the world as it is now, not a stale snapshot.
    assert sf.PRIVATE_BELIEF.value in ids  # owner sees own belief
