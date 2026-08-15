"""G36C: RC-001 NPC schedule / duty / body / social (mechanism; synthetic).

Synthetic anonymized profiles ONLY - never real《红楼梦》canon.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.rc001 import (
    NPCProfile,
    daily_schedule,
    resolve_population_result,
)


def _profile(actor: str, role: str = "maid") -> NPCProfile:
    return NPCProfile(
        actor_key=actor,
        role=role,
        schedule=(
            (6, "meal"),
            (8, "duty"),
            (12, "meal"),
            (14, "visit"),
            (21, "rest"),
        ),
        duty_ref=f"duty_{actor}",
        place_ref="place_hall",
    )


@pytest.mark.unit
def test_daily_schedule_is_deterministic() -> None:
    first = daily_schedule(_profile("c1"))
    second = daily_schedule(_profile("c1"))
    assert first == second
    assert [a.kind for a in first] == ["meal", "duty", "meal", "visit", "rest"]


@pytest.mark.unit
def test_duty_and_visit_map_to_authority_actions() -> None:
    activities = daily_schedule(_profile("c1"))
    duty = next(a for a in activities if a.kind == "duty")
    assert duty.action_type == "institution.complete_duty"
    assert duty.payload_dict()["duty_id"] == "duty_c1"
    visit = next(a for a in activities if a.kind == "visit")
    assert visit.action_type == "narrative.visit_sick"
    assert str(visit.payload_dict()["visit_id"]).startswith("visit_c1_")
    meal = next(a for a in activities if a.kind == "meal")
    assert meal.action_type == "body.rest"
    idle_profile = NPCProfile(actor_key="c9", role="guest", schedule=((10, "idle"),))
    assert all(a.action_type == "" for a in daily_schedule(idle_profile))


@pytest.mark.unit
def test_activity_at_resolves_current_activity() -> None:
    profile = _profile("c1")
    assert profile.activity_at(7) == "meal"
    assert profile.activity_at(9) == "duty"
    assert profile.activity_at(0) == "idle"


@pytest.mark.unit
def test_population_resolution_respects_capacity() -> None:
    profiles = tuple(_profile(f"c{i}") for i in range(1, 6))
    resolved, overflow = resolve_population_result(profiles, place_capacity=3)
    assert overflow == 2
    assert [p.actor_key for p in resolved] == sorted(p.actor_key for p in profiles)
    resolved_full, overflow_full = resolve_population_result(profiles, place_capacity=10)
    assert overflow_full == 0
    assert len(resolved_full) == 5


@pytest.mark.unit
def test_role_ordering_is_deterministic() -> None:
    profiles = (
        _profile("c2", role="maid"),
        _profile("c1", role="lady"),
    )
    resolved = resolve_population_result(profiles, place_capacity=10)[0]
    assert [p.actor_key for p in resolved] == ["c1", "c2"]  # role then key
