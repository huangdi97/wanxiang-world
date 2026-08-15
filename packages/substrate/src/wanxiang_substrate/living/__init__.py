"""Full Living Runtime substrate (M38)."""

from wanxiang_substrate.living.runtime import (
    WORLDNESS_CLASSES,
    EvolutionSummary,
    InstitutionEvolution,
    LongRunReport,
    LoopStep,
    PopulationResolution,
    PropagationGraph,
    ScenarioInstance,
    build_propagation_graph,
    evolve_institutions,
    evolve_long_term,
    instantiate_scenarios,
    resolve_population,
    run_autonomous_loop,
    run_long_horizon,
)

__all__ = [
    "EvolutionSummary",
    "InstitutionEvolution",
    "LongRunReport",
    "LoopStep",
    "PopulationResolution",
    "PropagationGraph",
    "ScenarioInstance",
    "WORLDNESS_CLASSES",
    "build_propagation_graph",
    "evolve_institutions",
    "evolve_long_term",
    "instantiate_scenarios",
    "resolve_population",
    "run_autonomous_loop",
    "run_long_horizon",
]
