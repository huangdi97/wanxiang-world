"""G91A: PressureProfile is a versioned Scenario/Domain value object."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.reality.pressure import (
    PRESSURE_DIMENSIONS,
    PressureProfile,
)


def _profile() -> PressureProfile:
    return PressureProfile(
        profile_id="pressure_market_v1",
        scenario_ref="scenario_market",
        domain_ref="domain_town",
        scarcity=0.7,
        goals=0.6,
        private_information=0.4,
        obligation=0.5,
        authority=0.3,
        reward=0.8,
        sanction=0.2,
        reputation=0.9,
        time=0.65,
        risk=0.55,
        norm=0.75,
        source_refs=("scenario:market", "scenario:market"),
    )


def test_profile_carries_all_v1_dimensions_and_provenance() -> None:
    profile = _profile()
    assert tuple(profile.dimensions()) == PRESSURE_DIMENSIONS
    assert profile.goal_pressure == profile.goals
    assert profile.source_refs == ("scenario:market",)
    assert profile.schema_version == 1
    assert profile.version == 1


def test_profile_round_trip_and_fingerprint_are_deterministic() -> None:
    profile = _profile()
    restored = PressureProfile.from_dict(profile.to_dict())
    assert restored == profile
    assert restored.fingerprint() == profile.fingerprint()
    assert restored.without_pressure().dimensions() == dict.fromkeys(PRESSURE_DIMENSIONS, 0.0)
    assert profile.distance(restored) == 0.0


def test_flat_goal_pressure_compatibility_reads_as_v1() -> None:
    raw = {"profile_id": "legacy", "goal_pressure": 0.25, "scarcity": 0.5}
    profile = PressureProfile.from_dict(raw)
    assert profile.goals == 0.25
    assert profile.scarcity == 0.5
    assert profile.to_dict()["schema_version"] == 1


@pytest.mark.parametrize("field", ["scarcity", "risk", "norm"])
def test_pressure_levels_are_bounded(field: str) -> None:
    with pytest.raises(ContractError):
        PressureProfile.from_dict({"profile_id": "bad", field: 1.1})


def test_pressure_profile_is_not_in_the_domain_kernel() -> None:
    import wanxiang_domain

    assert not hasattr(wanxiang_domain, "PressureProfile")
