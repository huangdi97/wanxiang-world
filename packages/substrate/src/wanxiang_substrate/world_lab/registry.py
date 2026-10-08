"""Thread-safe experiment definition and run registry (G95B)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from threading import RLock
from typing import cast

from wanxiang_domain.errors import Conflict, ContractError
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.world_lab.registry_models import (
    REGISTRY_SCHEMA_VERSION,
    ExperimentDefinition,
    ExperimentRun,
    RunStatus,
)
from wanxiang_substrate.world_lab.registry_support import (
    integer,
    ref,
    sequence,
    variant_options,
)
from wanxiang_substrate.world_lab.registry_support import parameters as normalize_parameters


class ExperimentRegistry:
    """Metadata registry; canonical state stays in the injected WorldRuntime."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._definitions: dict[tuple[str, int], ExperimentDefinition] = {}
        self._runs: dict[str, ExperimentRun] = {}

    def save_definition(self, definition: ExperimentDefinition) -> ExperimentDefinition:
        key = (definition.experiment_id, definition.version)
        with self._lock:
            if key in self._definitions:
                raise Conflict(f"experiment definition {key!r} already exists")
            self._definitions[key] = definition
        return definition

    register = save_definition

    def definition(self, experiment_id: str, version: int | None = None) -> ExperimentDefinition:
        with self._lock:
            candidates = [
                item
                for (item_id, item_version), item in self._definitions.items()
                if item_id == experiment_id and (version is None or item_version == version)
            ]
            if not candidates:
                raise ContractError(f"experiment definition {experiment_id!r} not found")
            return max(candidates, key=lambda item: item.version)

    def definitions(self) -> tuple[ExperimentDefinition, ...]:
        with self._lock:
            return tuple(self._definitions[key] for key in sorted(self._definitions))

    def create_run(
        self,
        experiment_id: str,
        *,
        seed: int,
        parameters: tuple[tuple[str, object], ...] = (),
        definition_version: int | None = None,
        run_id: str | None = None,
    ) -> ExperimentRun:
        definition = self.definition(experiment_id, definition_version)
        if seed not in definition.seeds:
            raise ContractError("run seed is not declared by the experiment")
        normalized = normalize_parameters(parameters, "parameters")
        if normalized and normalized not in variant_options(definition.parameter_variants):
            raise ContractError("run parameters are not declared by the experiment")
        variant_hash = semantic_sha256(normalized)[:16]
        resolved_id = run_id or f"{experiment_id}:v{definition.version}:{seed}:{variant_hash}"
        run = ExperimentRun(
            run_id=resolved_id,
            experiment_id=experiment_id,
            definition_version=definition.version,
            seed=seed,
            parameters=normalized,
        )
        with self._lock:
            if resolved_id in self._runs:
                raise Conflict(f"experiment run {resolved_id!r} already exists")
            self._runs[resolved_id] = run
        return run

    def save_run(
        self, run: ExperimentRun, *, expected_revision: int | None = None
    ) -> ExperimentRun:
        with self._lock:
            current = self._runs.get(run.run_id)
            if current is None:
                if run.revision != 0:
                    raise Conflict("new experiment run must start at revision zero")
                self._require_definition(run.experiment_id, run.definition_version)
            else:
                expected = current.revision if expected_revision is None else expected_revision
                if current.revision != expected or run.revision <= current.revision:
                    raise Conflict("experiment run revision is stale")
            self._runs[run.run_id] = run
            return run

    def run(self, run_id: str) -> ExperimentRun:
        with self._lock:
            run = self._runs.get(run_id)
            if run is None:
                raise ContractError(f"experiment run {run_id!r} not found")
            return run

    def runs(self, experiment_id: str | None = None) -> tuple[ExperimentRun, ...]:
        with self._lock:
            values = tuple(self._runs.values())
            if experiment_id is not None:
                values = tuple(item for item in values if item.experiment_id == experiment_id)
            return tuple(sorted(values, key=lambda item: item.run_id))

    def claim_run(self, run_id: str, *, worker_id: str) -> ExperimentRun:
        ref(worker_id, "worker_id")
        with self._lock:
            current = self.run(run_id)
            if current.status != "queued":
                raise Conflict(f"experiment run {run_id!r} is not queued")
            updated = replace(
                current,
                status="running",
                worker_id=worker_id,
                revision=current.revision + 1,
            )
            self._runs[run_id] = updated
            return updated

    def complete_run(
        self,
        run_id: str,
        *,
        worker_id: str,
        worldline_ref: str,
        artifact_ref: str,
    ) -> ExperimentRun:
        return self._finish(
            run_id,
            worker_id=worker_id,
            status="completed",
            worldline_ref=worldline_ref,
            artifact_ref=artifact_ref,
        )

    def fail_run(self, run_id: str, *, worker_id: str, error: str) -> ExperimentRun:
        if not error.strip():
            raise ContractError("failed experiment run requires an error")
        return self._finish(run_id, worker_id=worker_id, status="failed", error=error)

    def recover_inflight(self) -> tuple[ExperimentRun, ...]:
        with self._lock:
            recovered: list[ExperimentRun] = []
            for run_id, current in sorted(self._runs.items()):
                if current.status != "running":
                    continue
                updated = replace(
                    current,
                    status="queued",
                    worker_id="",
                    revision=current.revision + 1,
                )
                self._runs[run_id] = updated
                recovered.append(updated)
            return tuple(recovered)

    def to_dict(self) -> dict[str, object]:
        with self._lock:
            return {
                "schema_version": REGISTRY_SCHEMA_VERSION,
                "definitions": [item.to_dict() for item in self.definitions()],
                "runs": [item.to_dict() for item in self.runs()],
            }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExperimentRegistry:
        if (
            integer(data.get("schema_version"), "schema_version", minimum=1)
            != REGISTRY_SCHEMA_VERSION
        ):
            raise ContractError("unsupported experiment registry schema")
        registry = cls()
        for raw in sequence(data.get("definitions", ()), "definitions"):
            registry.save_definition(ExperimentDefinition.from_dict(_mapping(raw, "definition")))
        for raw in sequence(data.get("runs", ()), "runs"):
            run = ExperimentRun.from_dict(_mapping(raw, "run"))
            registry._require_definition(run.experiment_id, run.definition_version)
            if run.run_id in registry._runs:
                raise Conflict(f"experiment run {run.run_id!r} already exists")
            registry._runs[run.run_id] = run
        return registry

    def _finish(
        self,
        run_id: str,
        *,
        worker_id: str,
        status: RunStatus,
        worldline_ref: str = "",
        artifact_ref: str = "",
        error: str = "",
    ) -> ExperimentRun:
        ref(worker_id, "worker_id")
        ref(worldline_ref, "worldline_ref", allow_empty=True)
        ref(artifact_ref, "artifact_ref", allow_empty=True)
        with self._lock:
            current = self.run(run_id)
            if current.status != "running" or current.worker_id != worker_id:
                raise Conflict(f"experiment run {run_id!r} is not owned by worker")
            updated = replace(
                current,
                status=status,
                worldline_ref=worldline_ref,
                artifact_ref=artifact_ref,
                error=error,
                revision=current.revision + 1,
            )
            self._runs[run_id] = updated
            return updated

    def _require_definition(self, experiment_id: str, version: int) -> None:
        if (experiment_id, version) not in self._definitions:
            raise ContractError("run references an unknown experiment definition")


def _mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be a mapping")
    return cast(Mapping[str, object], value)


__all__ = [
    "ExperimentDefinition",
    "ExperimentRegistry",
    "ExperimentRun",
    "REGISTRY_SCHEMA_VERSION",
    "RunStatus",
]
