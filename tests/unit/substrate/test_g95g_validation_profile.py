"""G95G: independent V0-V7 profile and conservative report semantics."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import (
    VALIDATION_LEVELS,
    ValidationCheck,
    ValidationProfile,
    ValidationStack,
)


def _profile() -> ValidationProfile:
    return ValidationProfile("validation:g95g", 1)


def _passing_checks() -> tuple[ValidationCheck, ...]:
    return tuple(
        ValidationCheck(
            level=level,
            status="pass",
            reason=f"explicit evidence for {level}",
            evidence_refs=(f"evidence:g95g:{level}",),
            score=1.0,
        )
        for level in VALIDATION_LEVELS
    )


def test_profile_round_trip_declares_worldness_mapping_without_aliasing_it() -> None:
    profile = _profile()

    restored = ValidationProfile.from_dict(profile.to_dict())

    assert restored == profile
    assert restored.required_levels == VALIDATION_LEVELS
    assert restored.mapping_for("V6") == ("branch_isolation", "replayability")
    assert restored.to_dict()["level_names"] == {
        "V0": "Structural Validity",
        "V1": "Source Fidelity",
        "V2": "Behavioral Validity",
        "V3": "Mechanism Validity",
        "V4": "Macro Validity",
        "V5": "Long-Horizon Stability",
        "V6": "Counterfactual Validity",
        "V7": "External Calibration",
    }


def test_missing_evidence_is_unknown_and_never_accepted() -> None:
    report = ValidationStack().evaluate(_profile())

    assert report.complete is True
    assert report.overall_status == "unknown"
    assert report.accepted is False
    assert report.unknown_levels == VALIDATION_LEVELS
    assert all(check.status == "unknown" for check in report.checks)


def test_all_levels_need_explicit_pass_and_worldness_ref_is_not_a_shortcut() -> None:
    stack = ValidationStack()
    profile = _profile()
    report = stack.evaluate(
        profile,
        _passing_checks(),
        worldness_ref="worldness:g95g:independent",
    )
    changed_ref = stack.evaluate(
        profile,
        _passing_checks(),
        worldness_ref="worldness:g95g:changed",
    )

    assert report.overall_status == "pass"
    assert report.accepted is True
    assert changed_ref.accepted is True
    assert report.to_dict()["accepted"] is True
    assert stack.api_report(profile, report)["report"] == report.to_dict()


def test_unknown_external_calibration_blocks_acceptance_even_when_other_levels_pass() -> None:
    checks = list(_passing_checks())
    checks[-1] = ValidationCheck(
        level="V7",
        status="unknown",
        reason="no external calibration dataset is in scope",
    )

    report = ValidationStack().evaluate(_profile(), checks)

    assert report.overall_status == "unknown"
    assert report.accepted is False
    assert report.unknown_levels == ("V7",)


def test_stack_rejects_mismatched_mapping_keys_and_invalid_profile_mapping() -> None:
    with pytest.raises(ContractError, match="does not match"):
        ValidationStack().evaluate(
            _profile(),
            {"V0": ValidationCheck("V1", "unknown", "mismatched")},
        )
    with pytest.raises(ContractError, match="must cover V0-V7"):
        ValidationProfile(
            "validation:invalid",
            1,
            worldness_mapping=(("V0", ("persistence",)),),
        )
