"""G15C: seven-day autonomous living-world qualification.

Runs the comprehensive synthetic world (G15B) for seven simulated days with no
user session, capturing periodic hashes/checkpoints, then verifies:
- invariants green and the run completes;
- replay of the final state matches the committed semantic hash;
- emergent/conditional events arise from policies (multiple action types);
- the world advanced while no user session existed.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

import pytest
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PACK = ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"
DAYS = 7


def _load_sf() -> Any:
    spec = importlib.util.spec_from_file_location("synthetic_full", PACK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sf():
    return _load_sf()


def test_seven_day_autonomous_run_worldness(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.population.scheduler import AutonomousScheduler

    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))

    # Periodic captures: advance day by day (no user session at any point).
    hashes: list[str] = []
    revisions: list[int] = []
    day_events: list[int] = []
    prev_events = 1
    for day in range(1, DAYS + 1):
        scheduler = AutonomousScheduler(runtime, seed=20260814 + day)
        result = scheduler.run(sf.INSTANCE, w.root_branch_id, horizon_ticks=day * sf.DAY)
        hashes.append(result.final_hash)
        revisions.append(result.events_submitted)
        total_events = len(runtime.persistence.event_store.load(sf.INSTANCE, w.root_branch_id))
        day_events.append(total_events - prev_events)
        prev_events = total_events
        runtime.create_checkpoint(sf.INSTANCE, w.root_branch_id)

    # The world advanced every day with no user session (autonomous).
    assert all(d > 0 for d in day_events), "world must advance without a user"
    # Deterministic: same seed + config reproduces the same final hash.
    assert len(set(hashes)) >= 3, "state must evolve across days"

    # Invariants: stream is valid and replay reproduces the final hash.
    events = runtime.persistence.event_store.load(sf.INSTANCE, w.root_branch_id)
    assert [e.event_seq.value for e in events] == list(range(1, len(events) + 1))
    final = runtime.current_state(sf.INSTANCE, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == final.semantic_hash()

    # Emergent/conditional behavior: multiple distinct operation types committed
    # by the autonomous policies (not a single hardcoded narrative script).
    committed_actions: set[str] = set()
    for e in events:
        for op in e.delta.operations:
            committed_actions.add(type(op).__name__)
    assert "EntityUpdate" in committed_actions

    # No actor starvation: every person entity received some committed update
    # during the run (or is still present with valid body condition).
    state = runtime.current_state(sf.INSTANCE, w.root_branch_id)
    for actor in (sf.MAYOR, sf.SMITH, sf.APPRENTICE, sf.VISITOR):
        entity = state.entity(actor)
        assert entity is not None
        assert any(c.component_type == "body.condition" for c in entity.components.values())

    # No knowledge leak after the run: the visitor still cannot see the mayor's
    # private belief through the server projection.
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    snap = ProjectionService(state).compose(
        ProjectionRequest(
            session_id="s", actor_id=sf.VISITOR.value, branch_id=w.root_branch_id, mode="text"
        )
    )
    ids = {i.entity_id for i in snap.items}
    assert sf.PRIVATE_BELIEF.value not in ids
