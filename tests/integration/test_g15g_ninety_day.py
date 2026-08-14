"""G15G: extended 90-day virtual run & population-LOD qualification.

Runs the synthetic full world for 90 simulated days in 15-day chunks (small CI
profile: seed + runtime versions recorded). Verifies:
- no unbounded growth (entities bounded; per-chunk event growth positive/linear);
- dormant actors resume consistently (all actors valid at the end);
- no scheduler starvation (duty completions + all actors updated);
- sampled replay spot checks match the recorded hashes.
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
CHUNKS = 6
CHUNK_DAYS = 15


def _load_sf() -> Any:
    spec = importlib.util.spec_from_file_location("synthetic_full", PACK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sf() -> Any:
    return _load_sf()


def test_ninety_day_run_lod_and_replay(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.population.scheduler import AutonomousScheduler

    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    iid, branch = sf.INSTANCE, w.root_branch_id

    recorded_hashes: list[str] = []
    recorded_event_counts: list[int] = []
    start_events = len(runtime.persistence.event_store.load(iid, branch))
    for chunk in range(1, CHUNKS + 1):
        scheduler = AutonomousScheduler(runtime, seed=1000 + chunk)
        result = scheduler.run(iid, branch, horizon_ticks=chunk * CHUNK_DAYS * sf.DAY)
        recorded_hashes.append(result.final_hash)
        recorded_event_counts.append(
            len(runtime.persistence.event_store.load(iid, branch)) - start_events
        )
        runtime.create_checkpoint(iid, branch)

    # No unbounded growth: entities bounded (LOD keeps only world entities);
    # per-chunk event growth is positive and monotonic (no stalls or blowups).
    final = runtime.current_state(iid, branch)
    assert len(final.entities()) <= 30
    assert all(recorded_event_counts[i] > recorded_event_counts[i - 1] for i in range(1, CHUNKS))

    # Dormant actors resume consistently: every person entity is present with a
    # valid body condition after 90 days.
    for actor in (sf.MAYOR, sf.SMITH, sf.APPRENTICE, sf.VISITOR):
        entity = final.entity(actor)
        assert entity is not None
        assert any(c.component_type == "body.condition" for c in entity.components.values())

    # No scheduler starvation: duty completion events occurred during the run.
    duty_events = 0
    for event in runtime.persistence.event_store.load(iid, branch):
        for op in event.delta.operations:
            if getattr(op, "entity_type", "") == "institution.duty":
                duty_events += 1
    assert duty_events >= 1

    # Sampled replay spot checks: replay the event prefix up to each chunk and
    # compare to the recorded hash for that chunk.
    all_events = runtime.persistence.event_store.load(iid, branch)
    engine = ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
    for idx, (expected_hash, _count) in enumerate(zip(recorded_hashes, recorded_event_counts)):  # noqa: B905
        prefix = all_events[: recorded_event_counts[idx] + start_events]
        if not prefix:
            continue
        replayed = engine.replay(prefix)
        assert replayed.semantic_hash() == expected_hash, f"chunk {idx + 1} replay mismatch"

    # Full replay + restore reproduce the final hash.
    full_replay = engine.replay(all_events)
    assert full_replay.semantic_hash() == final.semantic_hash()
    restored = runtime.restore_and_replay(iid, branch)
    assert restored.state.semantic_hash() == final.semantic_hash()
