"""G95B: versioned definitions, recoverable runs and concurrent claims."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest
from wanxiang_domain.errors import Conflict
from wanxiang_substrate.world_lab import (
    ExperimentDefinition,
    ExperimentRegistry,
    ExperimentRun,
)


def _definition(version: int = 1) -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="experiment:g95b",
        version=version,
        world_package_ref="world:g95b",
        world_package_version=f"1.{version}.0",
        scenario_ref="scenario:g95b",
        scenario_version="1",
        seeds=(7, 3),
        parameter_variants=(("pressure", "high"), ("pressure", "low")),
        provider_matrix=(("alice", "policy:1"), ("bob", "agent:1")),
        population_policy="mixed",
        interventions=("intervention:none",),
        run_horizon=90,
        metrics=("event_count", "state_hash"),
        validation_profile_ref="validation:V0-V7",
        stop_conditions=("budget_exhausted",),
        owner_id="owner:g95b",
        rights_ref="rights:private-approved",
    )


def test_definition_and_run_metadata_round_trip() -> None:
    definition = _definition()
    registry = ExperimentRegistry()
    registry.save_definition(definition)
    run = registry.create_run(
        definition.experiment_id,
        seed=3,
        parameters=(("pressure", "high"),),
    )
    claimed = registry.claim_run(run.run_id, worker_id="worker:one")
    completed = registry.complete_run(
        claimed.run_id,
        worker_id="worker:one",
        worldline_ref="worldline:g95b:3",
        artifact_ref="artifact:g95b:3",
    )

    restored = ExperimentRegistry.from_dict(registry.to_dict())

    assert restored.definition("experiment:g95b") == definition
    assert restored.run(completed.run_id) == completed
    assert definition.to_spec().seeds == (3, 7)


def test_definition_versions_are_append_only_and_stale_run_write_is_rejected() -> None:
    registry = ExperimentRegistry()
    registry.register(_definition())
    registry.register(_definition(2))
    run = registry.create_run("experiment:g95b", seed=7)
    stale = replace(run, status="failed", error="stale")

    with pytest.raises(Conflict, match="revision"):
        registry.save_run(stale)
    with pytest.raises(Conflict, match="already exists"):
        registry.register(_definition())

    assert registry.definition("experiment:g95b").version == 2


def test_only_one_concurrent_worker_can_claim_a_run() -> None:
    registry = ExperimentRegistry()
    registry.register(_definition())
    run = registry.create_run("experiment:g95b", seed=7)

    def claim(worker: str) -> str:
        try:
            registry.claim_run(run.run_id, worker_id=worker)
        except Conflict:
            return "conflict"
        return "claimed"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = tuple(pool.map(claim, ("worker:one", "worker:two")))

    assert sorted(outcomes) == ["claimed", "conflict"]
    assert registry.run(run.run_id).status == "running"


def test_inflight_runs_recover_to_queue_without_losing_revision() -> None:
    registry = ExperimentRegistry()
    registry.register(_definition())
    run = registry.create_run("experiment:g95b", seed=7)
    claimed = registry.claim_run(run.run_id, worker_id="worker:one")

    recovered = registry.recover_inflight()

    assert recovered == (replace(claimed, status="queued", worker_id="", revision=2),)
    assert registry.run(run.run_id).status == "queued"


def test_run_record_is_immutable() -> None:
    run = ExperimentRun(
        run_id="run:g95b",
        experiment_id="experiment:g95b",
        definition_version=1,
        seed=1,
    )

    with pytest.raises(AttributeError):
        run.status = "running"  # type: ignore[misc]
