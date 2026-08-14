"""Strategy / Experiment workbench service (G18D).

Wraps the CoSim orchestrator + runtime for deterministic batch experiments.
Results link to package/runtime versions and branch ancestry; counterfactual
results are never presented as historical fact; invalid simulator proposals
are surfaced as rejected, never hidden.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_substrate.cosim.adapter import FakeSimulator
from wanxiang_substrate.cosim.orchestrator import CoSimOrchestrator


class ExperimentDefinition:
    def __init__(
        self, experiment_id: str, seed: int, simulators: dict[str, dict[str, Any]], horizon: int
    ) -> None:
        self.experiment_id = experiment_id
        self.seed = seed
        self.simulators = simulators
        self.horizon = horizon

    def canonical(self) -> str:
        return json.dumps(
            {
                "experiment_id": self.experiment_id,
                "seed": self.seed,
                "simulators": self.simulators,
                "horizon": self.horizon,
            },
            sort_keys=True,
        )

    def config_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode()).hexdigest()


class StrategyWorkbenchService:
    def run(
        self, definition: ExperimentDefinition, ancestry: tuple[str, ...] = ()
    ) -> dict[str, Any]:
        orch = CoSimOrchestrator()
        for name, spec in definition.simulators.items():
            orch.register(
                FakeSimulator(name, rate_ticks=int(spec["rate_ticks"]), growth=int(spec["growth"])),
                rate_ticks=int(spec["rate_ticks"]),
            )
        orch.step_to(definition.horizon)
        result_hash = hashlib.sha256(
            json.dumps(
                {
                    name: orch.simulators[name].checkpoint().value
                    for name in sorted(orch.simulators)
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()
        return {
            "experiment_id": definition.experiment_id,
            "config_hash": definition.config_hash(),
            "result_hash": result_hash,
            "runtime_version": RuntimeVersion(1).value,
            "schema_version": SchemaVersion(1).value,
            "branch_ancestry": ancestry,
            "counterfactual": True,  # simulations are never historical fact
        }

    def arbitrate(self, proposals: dict[str, object]) -> dict[str, Any]:
        orch = CoSimOrchestrator()
        result = orch.arbitrate(proposals)
        return {
            "winner": result.winner,
            "rejected": result.rejected,
            "conflict": result.conflict,
        }
