"""G95D: registry-backed batch queue, bounded workers, checkpoints, aggregation."""

from __future__ import annotations

from threading import Lock
from time import sleep

from wanxiang_substrate.world_lab import (
    BatchCheckpoint,
    BatchRunResult,
    BatchWorldlineExecutor,
    ExperimentDefinition,
    ExperimentRegistry,
)
from wanxiang_substrate.world_lab.registry_models import ExperimentRun


def _registry() -> ExperimentRegistry:
    registry = ExperimentRegistry()
    registry.register(
        ExperimentDefinition(
            experiment_id="experiment:g95d",
            version=1,
            world_package_ref="world:g95d",
            world_package_version="1",
            scenario_ref="scenario:g95d",
            scenario_version="1",
            seeds=(1, 2, 3),
            parameter_variants=(("pressure", "low"), ("pressure", "high")),
            owner_id="owner:g95d",
            rights_ref="rights:g95d",
        )
    )
    return registry


def test_batch_queue_is_reproducible_and_parallelism_is_bounded() -> None:
    registry = _registry()
    executor = BatchWorldlineExecutor(registry, max_parallelism=2)
    plan = executor.enqueue("experiment:g95d", batch_id="batch:g95d")
    assert executor.enqueue("experiment:g95d", batch_id="batch:g95d") == plan
    active = 0
    peak = 0
    lock = Lock()

    def worker(run: ExperimentRun) -> BatchRunResult:
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        sleep(0.01)
        with lock:
            active -= 1
        pressure = dict(run.parameters)["pressure"]
        score = float(run.seed) + (1.0 if pressure == "high" else 0.0)
        return BatchRunResult(
            run_id=run.run_id,
            seed=run.seed,
            parameters=run.parameters,
            worldline_ref=f"worldline:{run.run_id}",
            artifact_ref=f"artifact:{run.run_id}",
            metrics=(("score", score),),
        )

    execution = executor.execute(plan, worker, max_parallelism=4)

    assert len(execution.results) == 6
    assert execution.aggregate.completed_runs == 6
    assert execution.aggregate.failed_runs == 0
    assert peak <= 2
    assert execution.aggregate.metric("score") is not None
    assert execution.checkpoint.completed_run_ids == plan.run_ids
    assert execution.checkpoint.queued_run_ids == ()
    assert BatchCheckpoint.from_dict(execution.checkpoint.to_dict()) == execution.checkpoint


def test_batch_resume_reuses_completed_registry_runs_and_recovers_inflight() -> None:
    registry = _registry()
    executor = BatchWorldlineExecutor(registry, max_parallelism=2)
    plan = executor.enqueue("experiment:g95d", batch_id="batch:g95d:resume")
    claimed = registry.claim_run(plan.run_ids[0], worker_id="worker:crashed")
    assert claimed.status == "running"
    assert executor.recover(plan)[0].status == "queued"
    calls: list[str] = []

    def worker(run: ExperimentRun) -> BatchRunResult:
        calls.append(run.run_id)
        return BatchRunResult(
            run_id=run.run_id,
            seed=run.seed,
            parameters=run.parameters,
            worldline_ref=f"worldline:{run.run_id}",
            artifact_ref=f"artifact:{run.run_id}",
        )

    first = executor.execute(plan, worker)
    second = executor.resume(plan, worker)

    assert len(calls) == len(plan.run_ids)
    assert second.results == first.results
    assert second.checkpoint.sequence > first.checkpoint.sequence
