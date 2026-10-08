"""Compatibility readers for the versioned batch evidence schema (G95D)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.world_lab.batch_models import (
    BatchCheckpoint,
    BatchPlan,
    BatchResultStatus,
    BatchRunResult,
    count,
    metric_pairs,
    ref,
)


def plan_from_dict(data: Mapping[str, object]) -> BatchPlan:
    return BatchPlan(
        batch_id=ref(data.get("batch_id"), "batch_id"),
        experiment_id=ref(data.get("experiment_id"), "experiment_id"),
        definition_version=count(data.get("definition_version"), "definition_version", minimum=1),
        run_ids=tuple(
            ref(item, "run id") for item in _sequence(data.get("run_ids", ()), "run_ids")
        ),
        schema_version=count(data.get("schema_version"), "schema_version"),
    )


def result_from_dict(data: Mapping[str, object]) -> BatchRunResult:
    status = data.get("status", "completed")
    if not isinstance(status, str) or status not in {"completed", "failed"}:
        raise ContractError("invalid batch result status")
    error = data.get("error", "")
    if not isinstance(error, str):
        raise ContractError("batch result error must be text")
    return BatchRunResult(
        run_id=ref(data.get("run_id"), "run_id"),
        seed=count(data.get("seed"), "seed"),
        parameters=_parameter_pairs(data.get("parameters", ())),
        status=cast(BatchResultStatus, status),
        worldline_ref=ref(data.get("worldline_ref", ""), "worldline_ref", allow_empty=True),
        artifact_ref=ref(data.get("artifact_ref", ""), "artifact_ref", allow_empty=True),
        checkpoint_ref=ref(data.get("checkpoint_ref", ""), "checkpoint_ref", allow_empty=True),
        metrics=metric_pairs(_sequence(data.get("metrics", ()), "metrics")),
        error=error,
        schema_version=count(data.get("schema_version"), "schema_version"),
    )


def checkpoint_from_dict(data: Mapping[str, object]) -> BatchCheckpoint:
    results = tuple(
        result_from_dict(_mapping(item, "batch result"))
        for item in _sequence(data.get("results", ()), "results")
    )
    return BatchCheckpoint(
        batch_id=ref(data.get("batch_id"), "batch_id"),
        sequence=count(data.get("sequence"), "sequence", minimum=1),
        queued_run_ids=_refs(data.get("queued_run_ids", ()), "queued_run_ids"),
        running_run_ids=_refs(data.get("running_run_ids", ()), "running_run_ids"),
        completed_run_ids=_refs(data.get("completed_run_ids", ()), "completed_run_ids"),
        failed_run_ids=_refs(data.get("failed_run_ids", ()), "failed_run_ids"),
        results=results,
        schema_version=count(data.get("schema_version"), "schema_version"),
    )


def _sequence(value: object, name: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractError(f"{name} must be a list")
    return tuple(cast(list[object] | tuple[object, ...], value))


def _pairs(value: object, name: str) -> tuple[tuple[object, object], ...]:
    result: list[tuple[object, object]] = []
    for item in _sequence(value, name):
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((pair[0], pair[1]))
    return tuple(result)


def _parameter_pairs(value: object) -> tuple[tuple[str, object], ...]:
    result: list[tuple[str, object]] = []
    for key, item in _pairs(value, "parameters"):
        if not isinstance(key, str):
            raise ContractError("parameter key must be a string")
        result.append((key, item))
    return tuple(result)


def _refs(value: object, name: str) -> tuple[str, ...]:
    return tuple(ref(item, f"{name} item") for item in _sequence(value, name))


def _mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be a mapping")
    return cast(Mapping[str, object], value)


__all__ = ["checkpoint_from_dict", "plan_from_dict", "result_from_dict"]
