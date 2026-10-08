"""Living-instance lifecycle mixin for AuthoringService."""

from __future__ import annotations

from typing import Any

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.living_world import (
    LivingInstanceRecord,
    LivingRuntimePort,
    WorldnessRun,
    evaluate_living_world,
    instantiate_living_world,
)


class LivingWorldMixin:
    def instantiate_living(
        self: Any, job_id: str, runtime: LivingRuntimePort
    ) -> LivingInstanceRecord:
        existing = self._living_records.get(job_id)
        if existing is not None:
            return existing
        package = self._packages.get(job_id) or self.build_package(job_id)
        install = self._previews.for_package(package.package_id) or self.preview(job_id)
        world, record = instantiate_living_world(runtime, package, install)
        self._living_worlds[job_id] = world
        self._living_records[job_id] = record
        self._product_states[job_id] = "LIVING_INSTANCE_READY"
        return record

    def living(self: Any, job_id: str) -> LivingInstanceRecord | None:
        return self._living_records.get(job_id)

    def evaluate_worldness(self: Any, job_id: str, runtime: LivingRuntimePort) -> WorldnessRun:
        existing = self._worldness_runs.get(job_id)
        if existing is not None:
            return existing
        package = self._packages.get(job_id) or self.build_package(job_id)
        living = self._living_records.get(job_id) or self.instantiate_living(job_id, runtime)
        world = self._living_worlds.get(job_id)
        if world is None:
            raise ContractError(f"living world {job_id!r} is not instantiated")
        run, updated = evaluate_living_world(runtime, world, package, living)
        self._living_records[job_id] = updated
        self._worldness_runs[job_id] = run
        self._product_states[job_id] = (
            "WORLDNESS_ACCEPTED" if run.score.passed else "WORLDNESS_FAILED"
        )
        return run

    def worldness(self: Any, job_id: str) -> WorldnessRun | None:
        return self._worldness_runs.get(job_id)
