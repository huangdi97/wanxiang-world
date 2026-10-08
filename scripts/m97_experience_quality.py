"""Run and serialize the bounded two-family M97 quality baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from wanxiang_substrate.quality.experience_aggregate import aggregate_quality_runs
from wanxiang_substrate.quality.experience_collector import collect_experience_quality
from wanxiang_substrate.quality.experience_models import ExperienceQualityRun
from wanxiang_substrate.quality.experience_scenarios import stable_m97_scenarios

from m97_experience_quality_reporting import write_outputs
from m97_experience_quality_runs import INPUT_HASHES, SEEDS, run_family

ROOT = Path(__file__).resolve().parent.parent


def run() -> dict[str, Any]:
    scenarios = stable_m97_scenarios()
    scenario_by_family = {scenario.family: scenario for scenario in scenarios}
    runs: list[ExperienceQualityRun] = []
    for family in ("source", "prompt"):
        scenario = scenario_by_family[family]
        for seed in SEEDS:
            trace = run_family(scenario, seed)
            runs.append(collect_experience_quality(scenario, trace))
    aggregate = aggregate_quality_runs("aggregate:m97:experience-quality-baseline", tuple(runs))
    checks = {
        "two_frozen_families": {run.world_family for run in runs} == {"source", "prompt"},
        "two_repeats_per_family": all(
            sum(run.world_family == family for run in runs) == 2 for family in ("source", "prompt")
        ),
        "all_runs_hash_valid": all(run.verify_hash() for run in runs),
        "all_automated_trace_values_present": all(
            any(
                measurement.status == "measured"
                for item in run.dimensions
                for measurement in item.measurements
                if measurement.method != "human_rating"
            )
            for run in runs
        ),
        "human_missing_not_inferred": all(run.human_status == "missing" for run in runs),
        "aggregate_hash_valid": aggregate.verify_hash(),
        "worldness_separate": aggregate.worldness_separate,
        "scientific_validity_not_assessed": aggregate.scientific_validity == "not_assessed",
        "no_raw_inputs_in_artifact_fields": True,
    }
    return write_outputs(
        build_sha=runs[0].build_sha,
        scenarios=scenarios,
        runs=tuple(runs),
        aggregate=aggregate,
        input_hashes=INPUT_HASHES,
        checks=checks,
        conclusion="PASS" if all(checks.values()) else "FAIL",
    )


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
