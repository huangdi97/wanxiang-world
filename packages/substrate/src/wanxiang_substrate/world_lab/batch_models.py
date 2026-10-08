"""Batch worldline plans, checkpoints, and result models (G95D)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.registry_models import ExperimentRun
from wanxiang_substrate.world_lab.registry_support import parameters as normalize_parameters

BATCH_SCHEMA_VERSION = 1
BatchResultStatus = Literal["completed", "failed"]


def ref(value: object, name: str, *, allow_empty: bool = False) -> str:
    if (
        not isinstance(value, str)
        or (not allow_empty and not value.strip())
        or any(char.isspace() for char in value)
    ):
        raise ContractError(f"{name} must be a non-empty opaque reference")
    return value


def count(value: object, name: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ContractError(f"{name} must be an integer >= {minimum}")
    return value


def names(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(ref(value, f"{name} item") for value in values)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return result


def metric_pairs(values: Sequence[object]) -> tuple[tuple[str, float], ...]:
    result: list[tuple[str, float]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError("metrics items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError("metrics items must be pairs")
        name = ref(pair[0], "metric name")
        value = pair[1]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise ContractError("metric values must be finite numbers")
        result.append((name, float(value)))
    if len({name for name, _value in result}) != len(result):
        raise ContractError("metric names must be unique")
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class BatchPlan:
    """Deterministic queue of registry-owned experiment runs."""

    batch_id: str
    experiment_id: str
    definition_version: int
    run_ids: tuple[str, ...]
    schema_version: int = BATCH_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.batch_id, "batch_id")
        ref(self.experiment_id, "experiment_id")
        count(self.definition_version, "definition_version", minimum=1)
        if not self.run_ids:
            raise ContractError("batch plan requires at least one run")
        names(self.run_ids, "run_ids")
        if self.schema_version != BATCH_SCHEMA_VERSION:
            raise ContractError("unsupported batch plan schema")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "batch_id": self.batch_id,
            "experiment_id": self.experiment_id,
            "definition_version": self.definition_version,
            "run_ids": list(self.run_ids),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> BatchPlan:
        from wanxiang_substrate.world_lab.batch_serialization import plan_from_dict

        return plan_from_dict(data)


@dataclass(frozen=True, slots=True)
class BatchRunResult:
    """Sanitized output from one claimed registry run."""

    run_id: str
    seed: int
    parameters: tuple[tuple[str, object], ...]
    status: BatchResultStatus = "completed"
    worldline_ref: str = ""
    artifact_ref: str = ""
    checkpoint_ref: str = ""
    metrics: tuple[tuple[str, float], ...] = ()
    error: str = ""
    schema_version: int = BATCH_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.run_id, "run_id")
        count(self.seed, "seed")
        object.__setattr__(self, "parameters", normalize_parameters(self.parameters, "parameters"))
        object.__setattr__(self, "metrics", metric_pairs(self.metrics))
        for name in ("worldline_ref", "artifact_ref", "checkpoint_ref"):
            ref(getattr(self, name), name, allow_empty=True)
        if self.status not in {"completed", "failed"}:
            raise ContractError(f"unsupported batch result status {self.status!r}")
        if self.status == "completed" and (not self.worldline_ref or not self.artifact_ref):
            raise ContractError("completed batch result requires worldline and artifact refs")
        if self.status == "failed" and not self.error.strip():
            raise ContractError("failed batch result requires an error")
        if "\n" in self.error or "\r" in self.error:
            raise ContractError("batch result error must be one line")
        if self.schema_version != BATCH_SCHEMA_VERSION:
            raise ContractError("unsupported batch result schema")

    @classmethod
    def from_registry_run(cls, run: ExperimentRun) -> BatchRunResult:
        if run.status == "completed":
            return cls(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                worldline_ref=run.worldline_ref,
                artifact_ref=run.artifact_ref,
            )
        if run.status in {"failed", "cancelled"}:
            return cls(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                status="failed",
                error=run.error or f"registry run is {run.status}",
            )
        raise ContractError("only terminal registry runs can become batch results")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "seed": self.seed,
            "parameters": [list(item) for item in self.parameters],
            "status": self.status,
            "worldline_ref": self.worldline_ref,
            "artifact_ref": self.artifact_ref,
            "checkpoint_ref": self.checkpoint_ref,
            "metrics": [list(item) for item in self.metrics],
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> BatchRunResult:
        from wanxiang_substrate.world_lab.batch_serialization import result_from_dict

        return result_from_dict(data)


@dataclass(frozen=True, slots=True)
class BatchCheckpoint:
    """Serializable queue cursor; canonical events remain in the runtime."""

    batch_id: str
    sequence: int
    queued_run_ids: tuple[str, ...] = ()
    running_run_ids: tuple[str, ...] = ()
    completed_run_ids: tuple[str, ...] = ()
    failed_run_ids: tuple[str, ...] = ()
    results: tuple[BatchRunResult, ...] = ()
    schema_version: int = BATCH_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.batch_id, "batch_id")
        count(self.sequence, "sequence", minimum=1)
        groups = (
            self.queued_run_ids,
            self.running_run_ids,
            self.completed_run_ids,
            self.failed_run_ids,
        )
        all_ids = tuple(item for group in groups for item in group)
        names(all_ids, "checkpoint run ids")
        result_ids = tuple(result.run_id for result in self.results)
        names(result_ids, "checkpoint result ids")
        if not set(result_ids).issubset(all_ids):
            raise ContractError("checkpoint result is outside its run partition")
        if self.schema_version != BATCH_SCHEMA_VERSION:
            raise ContractError("unsupported batch checkpoint schema")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "batch_id": self.batch_id,
            "sequence": self.sequence,
            "queued_run_ids": list(self.queued_run_ids),
            "running_run_ids": list(self.running_run_ids),
            "completed_run_ids": list(self.completed_run_ids),
            "failed_run_ids": list(self.failed_run_ids),
            "results": [result.to_dict() for result in self.results],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> BatchCheckpoint:
        from wanxiang_substrate.world_lab.batch_serialization import checkpoint_from_dict

        return checkpoint_from_dict(data)


__all__ = [
    "BATCH_SCHEMA_VERSION",
    "BatchCheckpoint",
    "BatchPlan",
    "BatchResultStatus",
    "BatchRunResult",
    "count",
    "metric_pairs",
    "names",
    "ref",
]
