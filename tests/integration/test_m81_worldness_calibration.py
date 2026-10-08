"""M81 Worldness calibration and anti-gaming contracts."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_substrate.authoring.worldness import WorldnessEvaluator, WorldnessInput
from wanxiang_substrate.quality.worldness_calibration import run_worldness_calibration


@pytest.mark.integration
def test_adversarial_worldness_calibration_requires_score_separation_and_repair() -> None:
    report = run_worldness_calibration()
    assert report.passed is True
    assert report.minimum_score_drop >= 0.08
    assert report.anti_gaming_passed is True
    assert report.threshold_policy_passed is True
    assert all(not broken.gates.living_ready for _name, broken, _repair in report.cases)


@pytest.mark.integration
def test_endpoint_success_without_action_evidence_is_not_living_ready() -> None:
    value = WorldnessInput(4, 2, 4, 1, 0.1, True, True, evidence_coverage=1.0)
    score = WorldnessEvaluator().evaluate(replace(value, action_committed=True))
    assert score.gates.previewable is True
    assert score.gates.publishable is False
    assert score.gates.living_ready is False
