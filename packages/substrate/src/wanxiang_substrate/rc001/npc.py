"""RC-001 NPC schedule / duty / body / social policy (G36C).

Deterministic daily schedule for NPC actors composing institution duties,
body (meal/rest), narrative visits and idle time; plus population resolution
under place capacity. Pure policies; actions flow through the Commit
Authority via the existing resolvers (no direct writes). Synthetic anonymized
content only (real《红楼梦》 canon EXTERNAL_BLOCKED).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ActivityKind = Literal["meal", "rest", "duty", "visit", "idle"]
VALID_ACTIVITIES = ("meal", "rest", "duty", "visit", "idle")


@dataclass(frozen=True, slots=True)
class NPCProfile:
    """A schedulable actor with a deterministic daily activity plan."""

    actor_key: str
    role: str
    schedule: tuple[tuple[int, ActivityKind], ...]
    duty_ref: str = ""
    place_ref: str = ""

    def __post_init__(self) -> None:
        if not self.actor_key or not self.role:
            raise ContractError("npc profile requires actor key and role")
        for _tick, activity in self.schedule:
            if activity not in VALID_ACTIVITIES:
                raise ContractError(f"invalid activity {activity!r}")

    def activity_at(self, tick_of_day: int) -> ActivityKind:
        """Activity scheduled at a tick of the day (idle by default)."""
        best: tuple[int, ActivityKind] = (-1, "idle")
        for tick, activity in self.schedule:
            if tick <= tick_of_day and tick >= best[0]:
                best = (tick, activity)
        return best[1]


@dataclass(frozen=True, slots=True)
class Activity:
    """One resolved daily activity with its action mapping."""

    actor_key: str
    tick: int
    kind: ActivityKind
    action_type: str = ""
    payload: tuple[tuple[str, object], ...] = ()

    def payload_dict(self) -> dict[str, object]:
        return dict(self.payload)


def daily_schedule(profile: NPCProfile, day_ticks: int = 24) -> tuple[Activity, ...]:
    """Resolve a deterministic day: schedule -> action mapping.

    duty -> institution.complete_duty, visit -> narrative.visit_sick,
    meal/rest -> body.rest, idle -> no action. Deterministic per profile.
    """
    activities: list[Activity] = []
    for tick, kind in profile.schedule:
        if tick >= day_ticks:
            continue
        if kind == "duty":
            action, payload = "institution.complete_duty", (("duty_id", profile.duty_ref),)
        elif kind == "visit":
            action, payload = (
                "narrative.visit_sick",
                (("visit_id", f"visit_{profile.actor_key}_{tick}"),),
            )
        elif kind in ("meal", "rest"):
            action, payload = "body.rest", (("actor_id", profile.actor_key), ("ticks", 2))
        else:
            action, payload = "", ()
        activities.append(
            Activity(
                actor_key=profile.actor_key,
                tick=tick,
                kind=kind,
                action_type=action,
                payload=payload,
            )
        )
    return tuple(activities)


def resolve_population(
    profiles: tuple[NPCProfile, ...],
    *,
    place_capacity: int = 10,
) -> tuple[NPCProfile, ...]:
    """Population resolution: deterministic ordering by (role, actor_key).

    Capacity is a placement bound enforced by callers; the resolved ordering is
    stable so the same input yields the same population.
    """
    return tuple(sorted(profiles, key=lambda p: (p.role, p.actor_key)))


def resolve_population_result(
    profiles: tuple[NPCProfile, ...],
    *,
    place_capacity: int = 10,
) -> tuple[tuple[NPCProfile, ...], int]:
    """Return (resolved order, overflow count) under a place capacity bound."""
    resolved = resolve_population(profiles, place_capacity=place_capacity)
    overflow = max(0, len(resolved) - place_capacity)
    return resolved, overflow
