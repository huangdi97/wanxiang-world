"""M97 versioned ExperienceQuality schema and missing-data semantics."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.quality.experience_models import (
    QUALITY_DIMENSIONS,
    ExperienceDimension,
    ExperienceMeasurement,
    ExperienceQualityRun,
    measurement_from_dict,
)


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
