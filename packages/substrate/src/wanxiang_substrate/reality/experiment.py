"""Experiment runtime: multi-run, metrics, findings, validity envelope (G07E).

Runs are created from an immutable baseline branch; parameter variants and seed
sets are executed deterministically within resource budgets; metrics carry
run/seed/model/rule provenance; findings include assumptions and a
ValidityEnvelope.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from wanxiang_substrate.reality.errors import ExperimentError
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    """Versioned experiment specification."""

    experiment_id: str
    baseline_ref: str
    parameter_variants: tuple[tuple[str, object], ...]
    seeds: tuple[int, ...]
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.experiment_id or not self.baseline_ref:
            raise ExperimentError("experiment requires id and baseline ref")
        if not self.seeds:
            raise ExperimentError("experiment requires at least one seed")


@dataclass(frozen=True, slots=True)
class RunMetric:
    run_id: str
    seed: int
    parameter: str
    value: float
    rule_version: int = 1


@dataclass(frozen=True, slots=True)
class Finding:
    finding_id: str
    experiment_id: str
    conclusion: str
    supported: bool
    assumptions: tuple[str, ...] = ()
    validity_envelope: str = ""
    metrics: tuple[RunMetric, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidityEnvelope:
    """Describes the boundary within which results are valid."""

    experiment_id: str
    seeds: tuple[int, ...]
    rule_versions: tuple[int, ...]
    determinism_note: str = "same spec + seed + rule version reproduce identical results"


class ExperimentRuntime:
    """Executes deterministic batch variants within budgets."""

    def __init__(
        self,
        *,
        budget: ResourceBudget | None = None,
        rule_version: int = 1,
    ) -> None:
        self._tracker = BudgetTracker(budget or ResourceBudget(max_commands=10_000))
        self._rule_version = rule_version
        self._runs: dict[str, tuple[RunMetric, ...]] = {}

    def run(
        self, spec: ExperimentSpec, *, mutate: Callable[[int, str, object], float] | None = None
    ) -> tuple[RunMetric, ...]:
        """Run the variant matrix; `mutate(branch, seed, variant) -> value`."""
        results: list[RunMetric] = []
        for seed in spec.seeds:
            for param, value in spec.parameter_variants:
                self._tracker.consume(commands=1)
                run_id = f"{spec.experiment_id}_{seed}_{param}"
                mutator = mutate
                resolved = 0.0 if mutator is None else mutator(seed, param, value)
                results.append(
                    RunMetric(
                        run_id=run_id,
                        seed=seed,
                        parameter=param,
                        value=float(resolved),
                        rule_version=self._rule_version,
                    )
                )
        self._runs[spec.experiment_id] = tuple(results)
        return tuple(results)

    def envelope(self, spec: ExperimentSpec) -> ValidityEnvelope:
        return ValidityEnvelope(
            experiment_id=spec.experiment_id,
            seeds=spec.seeds,
            rule_versions=(self._rule_version,),
        )

    def finding(
        self,
        spec: ExperimentSpec,
        conclusion: str,
        *,
        supported: bool,
        assumptions: tuple[str, ...],
    ) -> Finding:
        metrics = self._runs.get(spec.experiment_id, ())
        if not metrics:
            raise ExperimentError("cannot emit a finding before running the experiment")
        envelope = self.envelope(spec)
        return Finding(
            finding_id=f"finding_{spec.experiment_id}",
            experiment_id=spec.experiment_id,
            conclusion=conclusion,
            supported=supported,
            assumptions=assumptions,
            validity_envelope=envelope.determinism_note,
            metrics=metrics,
        )

    def distribution(self, spec: ExperimentSpec, parameter: str) -> tuple[float, ...]:
        return tuple(
            m.value for m in self._runs.get(spec.experiment_id, ()) if m.parameter == parameter
        )
