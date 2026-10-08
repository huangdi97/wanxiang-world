"""M97 versioned ExperienceQuality schema and missing-data semantics."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.quality.experience_aggregate import aggregate_quality_runs
from wanxiang_substrate.quality.experience_collector import (
    ExperienceTraceEvidence,
    collect_experience_quality,
)
from wanxiang_substrate.quality.experience_models import (
    QUALITY_DIMENSIONS,
    ExperienceDimension,
    ExperienceMeasurement,
    ExperienceQualityRun,
    measurement_from_dict,
)
from wanxiang_substrate.quality.experience_scenarios import stable_m97_scenarios


def _run() -> ExperienceQualityRun:
    dimensions = tuple(
        ExperienceDimension(
            name,
            (
                ExperienceMeasurement(
                    "behavioral_trace",
                    "measured",
                    1.0,
                    (f"trace:{index}",),
                    sample_size=1,
                ),
                ExperienceMeasurement(
                    "human_rating",
                    "missing",
                    note="genuine human session not available",
                ),
            ),
        )
        for index, name in enumerate(QUALITY_DIMENSIONS, start=1)
    )
    return ExperienceQualityRun(
        run_id="run:m97:test",
        scenario_id="scenario:m97:test",
        world_family="prompt",
        world_ref="world:m97:test",
        package_ref="package:m97:test",
        scenario_version="1",
        build_sha="a" * 40,
        seed=9701,
        action_script=("action:set_status",),
        event_refs=("event:test",),
        state_refs=("state:before", "state:after"),
        replay_refs=("replay:test",),
        dimensions=dimensions,
        worldness_ref="worldness:test",
        missing_data=("human_session", "human_ratings"),
    ).with_hash()


def test_experience_quality_run_is_versioned_and_hash_verifiable() -> None:
    run = _run()
    assert run.verify_hash() is True
    assert run.to_dict()["schema"] == "wanxiang.v5.5.experience-quality.v1"
    assert all(item.name in QUALITY_DIMENSIONS for item in run.dimensions)
    assert all(
        any(measurement.status == "missing" for measurement in item.measurements)
        for item in run.dimensions
    )


def test_measured_quality_requires_traceable_evidence() -> None:
    with pytest.raises(ContractError, match="sample_size and evidence_refs"):
        ExperienceMeasurement("behavioral_trace", "measured", 1.0)


def test_measurement_reader_keeps_missing_human_value_null() -> None:
    measurement = measurement_from_dict(
        {"method": "human_rating", "status": "missing", "value": None}
    )
    assert measurement.value is None
    assert measurement.status == "missing"


def test_m97_freezes_source_and_original_prompt_scenarios() -> None:
    scenarios = stable_m97_scenarios()
    assert {scenario.family for scenario in scenarios} == {"source", "prompt"}
    assert all(scenario.action_script and scenario.human_slots for scenario in scenarios)
    assert all(scenario.version == "1" for scenario in scenarios)


def test_collector_and_aggregate_keep_missing_human_data_explicit() -> None:
    scenario = stable_m97_scenarios()[0]

    def trace(suffix: str, seed: int) -> ExperienceTraceEvidence:
        return ExperienceTraceEvidence(
            run_id=f"run:{scenario.scenario_id}:{suffix}",
            build_sha="b" * 40,
            seed=seed,
            trace_ref=f"trace:m97:{suffix}",
            worldness_ref=f"worldness:m97:{suffix}",
            event_refs=(f"event:m97:{suffix}:1", f"event:m97:{suffix}:2"),
            state_refs=(f"state:m97:{suffix}:before", f"state:m97:{suffix}:after"),
            replay_refs=(f"replay:m97:{suffix}",),
            action_committed=True,
            rejection_observed=True,
            replay_equal=True,
            character_identity_stable=True,
            leave_continue_equal=True,
            revision_aligned=True,
            goal_visible=True,
            state_diff_count=2,
            after_state_hashes=(f"hash:m97:{suffix}:1", f"hash:m97:{suffix}:2"),
            memory_revision_count=2,
        )

    first = collect_experience_quality(scenario, trace("one", 9701))
    second = collect_experience_quality(scenario, trace("two", 9702))
    aggregate = aggregate_quality_runs("aggregate:m97:test", (first, second))
    assert first.human_status == "missing"
    assert aggregate.human_status == "missing"
    assert aggregate.verify_hash() is True
    agency = next(item for item in aggregate.distributions if item.dimension == "Agency")
    assert agency.mean == 1.0
    assert agency.method_counts == (("behavioral_trace", 2), ("human_rating", 2))
