"""Serialize the M97 ExperienceQuality baseline and its boundary report."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from wanxiang_substrate.quality.experience_aggregate import ExperienceQualityAggregate
from wanxiang_substrate.quality.experience_models import ExperienceQualityRun
from wanxiang_substrate.quality.experience_scenarios import ExperienceBenchmarkScenario

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m97" / "experience_quality_baseline.json"
REPORT = ROOT / "reports" / "M97_EXPERIENCE_QUALITY_BENCHMARK.md"


def _write(payload: dict[str, Any]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_outputs(
    *,
    build_sha: str,
    scenarios: tuple[ExperienceBenchmarkScenario, ...],
    runs: tuple[ExperienceQualityRun, ...],
    aggregate: ExperienceQualityAggregate,
    input_hashes: dict[str, str],
    checks: dict[str, bool],
    conclusion: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m97.experience-quality.v1",
        "conclusion": conclusion,
        "gates": {"70": conclusion, "71": conclusion, "72": conclusion},
        "build_sha": build_sha,
        "inputs": {
            "sha256": input_hashes,
            "raw_source_emitted": False,
            "raw_prompt_emitted": False,
            "source_scope": "creator_owned_synthetic_qualification_only",
        },
        "seed_set": sorted({run.seed for run in runs}),
        "scenarios": [scenario.to_dict() for scenario in scenarios],
        "runs": [run.to_dict() for run in runs],
        "aggregate": aggregate.to_dict(),
        "missing_data": {
            "human_status": aggregate.human_status,
            "human_fields_are_missing_not_inferred": aggregate.human_status != "provided",
            "automated_measurements_are_not_human_ratings": True,
        },
        "separation": {
            "worldness_is_reference_only": aggregate.worldness_separate,
            "scientific_validity": aggregate.scientific_validity,
            "model_judge_used_as_authority": False,
        },
        "checks": checks,
        "boundaries": {
            "implemented": [
                "versioned ten-dimension ExperienceQuality schema",
                "source and original-prompt benchmark collection",
                "missing-aware per-run and aggregate baseline",
            ],
            "validated": [
                "real local Workshop/API/Playable traces",
                "state-diff, continuation, replay, and bounded continuity refs",
            ],
            "experimental": ["bounded quality baseline interpretation"],
            "not_proven": [
                "universal experience quality",
                "scientific validity",
                "population-level human preference",
            ],
            "external_blocked": [],
        },
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _write(payload)
    report = f"""# M97 Experience Quality Benchmark

**Conclusion:** `{conclusion}` for bounded Gates 70–72.

The benchmark uses the versioned ten-dimension ExperienceQuality schema and
four independent local product runs: two creator-owned source-driven runs and
two M96 original-prompt runs. Each run contains only opaque event/state/replay
references, a seed, action-script reference, and hash-verifiable measurements;
canonical state is not copied into this report.

Automated values come from real Workshop/API/Playable traces, including
committed StateDiff, rejection, leave/continue identity, replay, and bounded
actor-continuity evidence. Genuine human session and 1–5 ratings are explicitly
`missing`/`USER_INPUT_REQUIRED` in every run and are not inferred from the
automated trace. No model judge is used as authority and no universal quality
threshold is claimed.

Worldness remains a separate reference surface and scientific validity is
`NOT_ASSESSED`. Prompt Genesis, bounded long-horizon continuity, and any
emergence interpretation remain `EXPERIMENTAL`/`BOUNDED`.

Machine-readable evidence: `artifacts/v55_stable/m97/experience_quality_baseline.json`.
"""
    REPORT.write_text(report, encoding="utf-8")
    return payload
