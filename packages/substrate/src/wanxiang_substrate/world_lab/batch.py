"""Bounded, registry-backed batch worldline execution (G95D)."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import suppress
from threading import RLock, get_ident

from wanxiang_domain.errors import Conflict, ContractError

from wanxiang_substrate.world_lab.batch_aggregate import BatchExecution, aggregate_results
from wanxiang_substrate.world_lab.batch_models import (
    BatchCheckpoint,
    BatchPlan,
    BatchRunResult,
)
from wanxiang_substrate.world_lab.registry import ExperimentRegistry
from wanxiang_substrate.world_lab.registry_models import ExperimentRun

BatchWorker = Callable[[ExperimentRun], BatchRunResult]


class BatchWorldlineExecutor:
    """Queue and execute registry runs without owning canonical world state."""

    def __init__(self, registry: ExperimentRegistry, *, max_parallelism: int = 1) -> None:
        if type(max_parallelism) is not int or max_parallelism < 1:
            raise ContractError("max_parallelism must be a positive integer")
        self.registry = registry
        self.max_parallelism = max_parallelism
        self._lock = RLock()
        self._plans: dict[str, BatchPlan] = {}
        self._checkpoints: dict[str, BatchCheckpoint] = {}

    def enqueue(
        self,
        experiment_id: str,
        *,
        batch_id: str,
        definition_version: int | None = None,
    ) -> BatchPlan:
        definition = self.registry.definition(experiment_id, definition_version)
        existing = self._plans.get(batch_id)
        if existing is not None:
            if existing.experiment_id != experiment_id or (
                existing.definition_version != definition.version
            ):
                raise Conflict(f"batch {batch_id!r} already targets another definition")
            return existing
        variants = definition.parameter_variants
        parameter_sets = (
            ((),) if not variants else tuple(((name, value),) for name, value in variants)
        )
        run_ids: list[str] = []
        for seed in definition.seeds:
            for variant_index, parameters in enumerate(parameter_sets):
                run_id = f"{batch_id}:run:{seed}:{variant_index}"
                self._ensure_run(
                    experiment_id,
                    definition.version,
                    run_id,
                    seed,
                    parameters,
                )
                run_ids.append(run_id)
        plan = BatchPlan(
            batch_id=batch_id,
            experiment_id=experiment_id,
            definition_version=definition.version,
            run_ids=tuple(run_ids),
        )
        with self._lock:
            self._plans[batch_id] = plan
        return plan

    def execute(
        self,
        plan: BatchPlan,
        worker: BatchWorker,
        *,
        max_parallelism: int | None = None,
        checkpoint: BatchCheckpoint | None = None,
    ) -> BatchExecution:
        self._validate_plan(plan)
        limit = self._parallelism(max_parallelism)
        results = {item.run_id: item for item in (checkpoint.results if checkpoint else ())}
        pending: list[str] = []
        for run_id in plan.run_ids:
            run = self.registry.run(run_id)
            if run.status in {"completed", "failed", "cancelled"}:
                results.setdefault(run_id, BatchRunResult.from_registry_run(run))
            elif run.status == "queued":
                pending.append(run_id)
            else:
                raise Conflict(f"batch run {run_id!r} is still in flight; recover it first")
        if pending:
            with ThreadPoolExecutor(
                max_workers=limit,
                thread_name_prefix=f"wanxiang-{plan.batch_id}",
            ) as pool:
                futures = {
                    pool.submit(self._execute_one, plan, run_id, worker, results): run_id
                    for run_id in pending
                }
                for future in as_completed(futures):
                    result = future.result()
                    results[result.run_id] = result
        latest = self._publish_checkpoint(plan, results)
        ordered = tuple(results[run_id] for run_id in plan.run_ids)
        return BatchExecution(
            plan=plan,
            results=ordered,
            checkpoint=latest,
            aggregate=aggregate_results(plan.batch_id, ordered),
        )

    def resume(
        self,
        plan: BatchPlan,
        worker: BatchWorker,
        *,
        max_parallelism: int | None = None,
    ) -> BatchExecution:
        return self.execute(
            plan,
            worker,
            max_parallelism=max_parallelism,
            checkpoint=self.checkpoint(plan.batch_id),
        )

    def recover(self, plan: BatchPlan) -> tuple[ExperimentRun, ...]:
        self._validate_plan(plan)
        run_ids = set(plan.run_ids)
        return tuple(item for item in self.registry.recover_inflight() if item.run_id in run_ids)

    def checkpoint(self, batch_id: str) -> BatchCheckpoint | None:
        with self._lock:
            return self._checkpoints.get(batch_id)

    def _execute_one(
        self,
        plan: BatchPlan,
        run_id: str,
        worker: BatchWorker,
        results: dict[str, BatchRunResult],
    ) -> BatchRunResult:
        claimed: ExperimentRun | None = None
        run = self.registry.run(run_id)
        worker_id = f"{plan.batch_id}:worker:{get_ident()}"
        try:
            claimed = self.registry.claim_run(run_id, worker_id=worker_id)
            candidate = worker(claimed)
            self._validate_result(claimed, candidate)
            if candidate.status == "completed":
                self.registry.complete_run(
                    run_id,
                    worker_id=worker_id,
                    worldline_ref=candidate.worldline_ref,
                    artifact_ref=candidate.artifact_ref,
                )
            else:
                self.registry.fail_run(run_id, worker_id=worker_id, error=candidate.error)
            result = candidate
        except Exception as exc:  # worker failure is retained as a terminal run result
            error = _error_text(exc)
            if claimed is not None:
                with suppress(Conflict):
                    self.registry.fail_run(run_id, worker_id=worker_id, error=error)
            result = BatchRunResult(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                status="failed",
                error=error,
            )
        with self._lock:
            results[run_id] = result
            self._publish_checkpoint_locked(plan, results)
        return result

    def _ensure_run(
        self,
        experiment_id: str,
        definition_version: int,
        run_id: str,
        seed: int,
        parameters: tuple[tuple[str, object], ...],
    ) -> None:
        try:
            self.registry.create_run(
                experiment_id,
                seed=seed,
                parameters=parameters,
                definition_version=definition_version,
                run_id=run_id,
            )
        except Conflict:
            existing = self.registry.run(run_id)
            if (
                existing.experiment_id != experiment_id
                or existing.definition_version != definition_version
                or existing.seed != seed
                or existing.parameters != parameters
            ):
                raise Conflict(
                    f"batch run {run_id!r} conflicts with existing registry metadata"
                ) from None

    def _validate_plan(self, plan: BatchPlan) -> None:
        known = self._plans.get(plan.batch_id)
        if known is not None and known != plan:
            raise Conflict(f"batch plan {plan.batch_id!r} is not the registered plan")
        for run_id in plan.run_ids:
            run = self.registry.run(run_id)
            if run.experiment_id != plan.experiment_id or (
                run.definition_version != plan.definition_version
            ):
                raise Conflict(f"batch run {run_id!r} does not match its plan")

    def _parallelism(self, requested: int | None) -> int:
        if requested is None:
            return self.max_parallelism
        if type(requested) is not int or requested < 1:
            raise ContractError("max_parallelism must be a positive integer")
        return min(self.max_parallelism, requested)

    def _publish_checkpoint(
        self,
        plan: BatchPlan,
        results: dict[str, BatchRunResult],
    ) -> BatchCheckpoint:
        with self._lock:
            return self._publish_checkpoint_locked(plan, results)

    def _publish_checkpoint_locked(
        self,
        plan: BatchPlan,
        results: dict[str, BatchRunResult],
    ) -> BatchCheckpoint:
        queued: list[str] = []
        running: list[str] = []
        completed: list[str] = []
        failed: list[str] = []
        for run_id in plan.run_ids:
            status = self.registry.run(run_id).status
            if status == "queued":
                queued.append(run_id)
            elif status == "running":
                running.append(run_id)
            elif status == "completed":
                completed.append(run_id)
            else:
                failed.append(run_id)
        previous = self._checkpoints.get(plan.batch_id)
        checkpoint = BatchCheckpoint(
            batch_id=plan.batch_id,
            sequence=(previous.sequence + 1 if previous else 1),
            queued_run_ids=tuple(queued),
            running_run_ids=tuple(running),
            completed_run_ids=tuple(completed),
            failed_run_ids=tuple(failed),
            results=tuple(results[run_id] for run_id in plan.run_ids if run_id in results),
        )
        self._checkpoints[plan.batch_id] = checkpoint
        return checkpoint

    @staticmethod
    def _validate_result(run: ExperimentRun, result: BatchRunResult) -> None:
        if type(result) is not BatchRunResult:
            raise ContractError("batch worker must return BatchRunResult")
        if result.run_id != run.run_id or result.seed != run.seed:
            raise ContractError("batch worker result does not match claimed run")
        if result.parameters != run.parameters:
            raise ContractError("batch worker result parameters do not match claimed run")


def _error_text(error: Exception) -> str:
    text = f"{type(error).__name__}: {error}".replace("\r", " ").replace("\n", " ").strip()
    return text[:512] or type(error).__name__


BatchExecutor = BatchWorldlineExecutor
WorldlineBatchExecutor = BatchWorldlineExecutor


__all__ = [
    "BatchExecutor",
    "BatchWorker",
    "BatchWorldlineExecutor",
    "WorldlineBatchExecutor",
]
