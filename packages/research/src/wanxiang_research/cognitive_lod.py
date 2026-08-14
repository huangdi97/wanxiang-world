"""Cognitive LOD & large-population scheduling research (G19D, experimental).

Active/background/dormant/crowd tiers with event-driven wakeups; transitions
preserve identity and required obligations; dormant actors never require LLM
calls; aggregate models never invent private knowledge for individuals.
"""

from __future__ import annotations

from dataclasses import dataclass

TIERS = ("active", "background", "dormant", "crowd")


@dataclass(frozen=True, slots=True)
class Actor:
    actor_id: str
    tier: str = "dormant"
    obligations: tuple[str, ...] = ()
    wake_event: str = ""

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"unknown LOD tier {self.tier!r}")


class CognitiveLodScheduler:
    def __init__(self) -> None:
        self._actors: dict[str, Actor] = {}
        self._wakeups: dict[str, int] = {}

    def register(self, actor: Actor) -> None:
        self._actors[actor.actor_id] = actor

    def set_tier(self, actor_id: str, tier: str) -> None:
        if tier not in TIERS:
            raise ValueError(f"unknown LOD tier {tier!r}")
        actor = self._actors[actor_id]
        self._actors[actor_id] = Actor(
            actor_id=actor.actor_id,
            tier=tier,
            obligations=actor.obligations,  # obligations preserved across transitions
            wake_event=actor.wake_event,
        )

    def wake(self, actor_id: str, event: str) -> bool:
        """Event-driven wakeup: promote an actor for a tick."""
        actor = self._actors[actor_id]
        if actor.tier in ("dormant", "crowd"):
            self._wakeups[actor_id] = self._wakeups.get(actor_id, 0) + 1
            self.set_tier(actor_id, "active")
            self._actors[actor_id] = Actor(
                actor_id=actor.actor_id,
                tier="active",
                obligations=actor.obligations,
                wake_event=event,
            )
            return True
        return False

    def demote(self, actor_id: str, tier: str) -> None:
        self.set_tier(actor_id, tier)

    def actor(self, actor_id: str) -> Actor:
        return self._actors[actor_id]

    def wakeup_count(self, actor_id: str) -> int:
        return self._wakeups.get(actor_id, 0)

    def active_count(self) -> int:
        return sum(1 for a in self._actors.values() if a.tier == "active")

    def resource_cost(self) -> int:
        """Declared resource-use metric: only non-dormant actors consume budget."""
        weights = {"active": 4, "background": 2, "dormant": 0, "crowd": 0}
        return sum(weights[a.tier] for a in self._actors.values())
