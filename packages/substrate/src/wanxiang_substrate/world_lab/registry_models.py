"""Versioned experiment definition and run records (G95B)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.reality.experiment import ExperimentSpec
from wanxiang_substrate.world_lab.registry_support import (
    integer,
    names,
    pairs,
    parameters,
    ref,
    sequence,
    variants,
)

REGISTRY_SCHEMA_VERSION = 1
RunStatus = Literal["queued", "running", "completed", "failed", "cancelled"]
_RUN_STATUSES: frozenset[str] = frozenset({"queued", "running", "completed", "failed", "cancelled"})


@dataclass(frozen=True, slots=True)
class ExperimentDefinition:
    """Version-pinned experiment metadata; it owns no world state."""

    experiment_id: str
    version: int
    world_package_ref: str
    world_package_version: str
    scenario_ref: str
    scenario_version: str
    seeds: tuple[int, ...]
    parameter_variants: tuple[tuple[str, object], ...]
    provider_matrix: tuple[tuple[str, str], ...] = ()
    population_policy: str = "single-provider"
    interventions: tuple[str, ...] = ()
    run_horizon: int = 0
    metrics: tuple[str, ...] = ()
    validation_profile_ref: str = "validation:unknown"
    stop_conditions: tuple[str, ...] = ()
    owner_id: str = "owner:unknown"
    rights_ref: str = "rights:unknown"
    schema_version: int = REGISTRY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.experiment_id, "experiment_id")
        integer(self.version, "version", minimum=1)
        for name in (
            "world_package_ref",
            "scenario_ref",
            "validation_profile_ref",
            "owner_id",
            "rights_ref",
            "world_package_version",
            "scenario_version",
        ):
            ref(getattr(self, name), name)
        if not self.seeds:
            raise ContractError("experiment requires at least one seed")
        seeds = tuple(integer(seed, "seed") for seed in self.seeds)
        if len(seeds) != len(set(seeds)):
            raise ContractError("experiment seeds must be unique")
        if self.schema_version != REGISTRY_SCHEMA_VERSION:
            raise ContractError("unsupported experiment definition schema")
        ref(self.population_policy, "population_policy")
        integer(self.run_horizon, "run_horizon")
        object.__setattr__(self, "seeds", tuple(sorted(seeds)))
        object.__setattr__(
            self,
            "parameter_variants",
            variants(self.parameter_variants, "parameter_variants"),
        )
        object.__setattr__(self, "provider_matrix", pairs(self.provider_matrix, "provider_matrix"))
        object.__setattr__(self, "interventions", names(self.interventions, "interventions"))
        object.__setattr__(self, "metrics", names(self.metrics, "metrics"))
        object.__setattr__(
            self,
            "stop_conditions",
            names(self.stop_conditions, "stop_conditions"),
        )

    def to_spec(self) -> ExperimentSpec:
        return ExperimentSpec(
            experiment_id=self.experiment_id,
            baseline_ref=self.world_package_ref,
            parameter_variants=self.parameter_variants,
            seeds=self.seeds,
            schema_version=self.schema_version,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "experiment_id": self.experiment_id,
            "version": self.version,
            "world_package_ref": self.world_package_ref,
            "world_package_version": self.world_package_version,
            "scenario_ref": self.scenario_ref,
            "scenario_version": self.scenario_version,
            "seeds": list(self.seeds),
            "parameter_variants": [list(item) for item in self.parameter_variants],
            "provider_matrix": [list(item) for item in self.provider_matrix],
            "population_policy": self.population_policy,
            "interventions": list(self.interventions),
            "run_horizon": self.run_horizon,
            "metrics": list(self.metrics),
            "validation_profile_ref": self.validation_profile_ref,
            "stop_conditions": list(self.stop_conditions),
            "owner_id": self.owner_id,
            "rights_ref": self.rights_ref,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExperimentDefinition:
        return cls(
            experiment_id=ref(data.get("experiment_id"), "experiment_id"),
            version=integer(data.get("version"), "version", minimum=1),
            world_package_ref=ref(data.get("world_package_ref"), "world_package_ref"),
            world_package_version=ref(data.get("world_package_version"), "world_package_version"),
            scenario_ref=ref(data.get("scenario_ref"), "scenario_ref"),
            scenario_version=ref(data.get("scenario_version"), "scenario_version"),
            seeds=tuple(integer(item, "seed") for item in sequence(data.get("seeds", ()), "seeds")),
            parameter_variants=variants(
                sequence(data.get("parameter_variants", ()), "parameter_variants"),
                "parameter_variants",
            ),
            provider_matrix=pairs(
                sequence(data.get("provider_matrix", ()), "provider_matrix"),
                "provider_matrix",
            ),
            population_policy=ref(data.get("population_policy"), "population_policy"),
            interventions=names(
                sequence(data.get("interventions", ()), "interventions"), "interventions"
            ),
            run_horizon=integer(data.get("run_horizon", 0), "run_horizon"),
            metrics=names(sequence(data.get("metrics", ()), "metrics"), "metrics"),
            validation_profile_ref=ref(
                data.get("validation_profile_ref"), "validation_profile_ref"
            ),
            stop_conditions=names(
                sequence(data.get("stop_conditions", ()), "stop_conditions"), "stop_conditions"
            ),
            owner_id=ref(data.get("owner_id"), "owner_id"),
            rights_ref=ref(data.get("rights_ref"), "rights_ref"),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


@dataclass(frozen=True, slots=True)
class ExperimentRun:
    """Versioned run lease and result references."""

    run_id: str
    experiment_id: str
    definition_version: int
    seed: int
    parameters: tuple[tuple[str, object], ...] = ()
    status: RunStatus = "queued"
    worldline_ref: str = ""
    artifact_ref: str = ""
    worker_id: str = ""
    error: str = ""
    revision: int = 0
    schema_version: int = REGISTRY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        ref(self.run_id, "run_id")
        ref(self.experiment_id, "experiment_id")
        integer(self.definition_version, "definition_version", minimum=1)
        integer(self.seed, "seed")
        integer(self.revision, "revision")
        if self.status not in _RUN_STATUSES:
            raise ContractError(f"unsupported run status {self.status!r}")
        if self.schema_version != REGISTRY_SCHEMA_VERSION:
            raise ContractError("unsupported experiment run schema")
        object.__setattr__(self, "parameters", parameters(self.parameters, "parameters"))
        for name in ("worldline_ref", "artifact_ref", "worker_id"):
            ref(getattr(self, name), name, allow_empty=True)
        if self.status == "running" and not self.worker_id:
            raise ContractError("running experiment run requires a worker")
        if self.status == "completed" and (not self.worldline_ref or not self.artifact_ref):
            raise ContractError("completed experiment run requires worldline and artifact refs")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "definition_version": self.definition_version,
            "seed": self.seed,
            "parameters": [list(item) for item in self.parameters],
            "status": self.status,
            "worldline_ref": self.worldline_ref,
            "artifact_ref": self.artifact_ref,
            "worker_id": self.worker_id,
            "error": self.error,
            "revision": self.revision,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ExperimentRun:
        status = data.get("status", "queued")
        error = data.get("error", "")
        if not isinstance(status, str) or status not in _RUN_STATUSES:
            raise ContractError("invalid experiment run status")
        if not isinstance(error, str):
            raise ContractError("run error must be text")
        return cls(
            run_id=ref(data.get("run_id"), "run_id"),
            experiment_id=ref(data.get("experiment_id"), "experiment_id"),
            definition_version=integer(
                data.get("definition_version"), "definition_version", minimum=1
            ),
            seed=integer(data.get("seed"), "seed"),
            parameters=parameters(sequence(data.get("parameters", ()), "parameters"), "parameters"),
            status=cast(RunStatus, status),
            worldline_ref=ref(data.get("worldline_ref", ""), "worldline_ref", allow_empty=True),
            artifact_ref=ref(data.get("artifact_ref", ""), "artifact_ref", allow_empty=True),
            worker_id=ref(data.get("worker_id", ""), "worker_id", allow_empty=True),
            error=error,
            revision=integer(data.get("revision", 0), "revision"),
            schema_version=integer(data.get("schema_version"), "schema_version", minimum=1),
        )


__all__ = [
    "ExperimentDefinition",
    "ExperimentRun",
    "REGISTRY_SCHEMA_VERSION",
    "RunStatus",
]
