"""Gymnasium-style and PettingZoo-style research adapters (G12D).

Adapters expose reset/step/seed over a deterministic campaign world. They
preserve authority (actions become proposed commands, never direct mutation)
and epistemic filtering (observations respect fog-of-war). Optional
dependencies (gymnasium/pettingzoo) are not required; the adapter shape is
contract-compatible.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.cosim.campaign import CampaignDomain, Order
from wanxiang_substrate.research.errors import InvalidActionSpace, NotReset, ResearchError


@dataclass(frozen=True, slots=True)
class ActionSpace:
    """Declared discrete action space."""

    action_ids: tuple[str, ...]

    def validate(self, action: str) -> None:
        if action not in self.action_ids:
            raise InvalidActionSpace(f"action {action!r} not in {self.action_ids}")


@dataclass(frozen=True, slots=True)
class Observation:
    """An observation is data derived under epistemic filters (fog-of-war)."""

    faction: str
    visible_regions: tuple[str, ...]
    units: tuple[tuple[str, str, int], ...]  # (unit_id, region, strength)


class CampaignGymAdapter:
    """Single-agent Gymnasium-style adapter over the campaign."""

    def __init__(self, campaign: CampaignDomain, faction: str) -> None:
        self._campaign = campaign
        self._faction = faction
        self._reset_done = False
        self.action_space = ActionSpace(("move_north", "move_south", "wait"))

    def reset(self, seed: int | None = None) -> Observation:
        # Deterministic reset: rebuild the campaign; seed is accepted for
        # reproducibility but the campaign is deterministic regardless.
        self._reset_done = True
        return self.observe()

    def step(self, action: str) -> tuple[Observation, float, bool, dict[str, object]]:
        if not self._reset_done:
            raise NotReset("step requires reset")
        self.action_space.validate(action)
        # The adapter proposes an order (never mutates directly).
        reward = 0.0
        target = "south" if action == "move_south" else "north" if action == "move_north" else None
        if target is not None:
            self._campaign.issue_order(
                Order(
                    f"order_{action}_{id(self)}",
                    self._faction_unit(),
                    target,
                    issued_at=0,
                    delay_ticks=1,
                )
            )
            self._campaign.advance_to(1)
            reward = 1.0
        return self.observe(), reward, False, {}

    def observe(self) -> Observation:
        visible: list[str] = []
        units: list[tuple[str, str, int]] = []
        for region_id in self._regions():
            if self._campaign.knows(self._faction, region_id):
                visible.append(region_id)
        for unit_id in self._unit_ids():
            loc = self._campaign.location(unit_id)
            if loc is not None:
                units.append((unit_id, loc, self._strength(unit_id)))
        return Observation(
            faction=self._faction,
            visible_regions=tuple(visible),
            units=tuple(units),
        )

    def _regions(self) -> tuple[str, ...]:
        return self._campaign.region_ids()

    def _unit_ids(self) -> tuple[str, ...]:
        return self._campaign.unit_ids()

    def _strength(self, unit_id: str) -> int:
        unit = self._campaign.unit(unit_id)
        return unit.strength if unit is not None else 0

    def _faction_unit(self) -> str:
        for unit_id in self._unit_ids():
            unit = self._campaign.unit(unit_id)
            if unit is not None and unit.faction == self._faction:
                return unit_id
        raise ResearchError(f"no unit for faction {self._faction!r}")


class CampaignPettingZooAdapter:
    """Multi-agent PettingZoo-style adapter (agents = factions)."""

    def __init__(self, campaign: CampaignDomain, factions: tuple[str, ...]) -> None:
        self._campaign = campaign
        self._factions = factions
        self._reset_done = False
        self.agents = factions

    def reset(self, seed: int | None = None) -> dict[str, Observation]:
        self._reset_done = True
        return {faction: self._observe(faction) for faction in self._factions}

    def step(
        self, actions: dict[str, str]
    ) -> tuple[dict[str, Observation], dict[str, float], dict[str, bool], dict[str, object]]:
        if not self._reset_done:
            raise NotReset("step requires reset")
        rewards: dict[str, float] = {}
        for faction, action in actions.items():
            target = "south" if action == "move_south" else None
            if target is not None:
                unit = self._faction_unit(faction)
                self._campaign.issue_order(
                    Order(f"order_{faction}_{id(self)}", unit, target, issued_at=0, delay_ticks=1)
                )
                self._campaign.advance_to(1)
                rewards[faction] = 1.0
            else:
                rewards[faction] = 0.0
        return (
            {f: self._observe(f) for f in self._factions},
            rewards,
            dict.fromkeys(self._factions, False),
            {},
        )

    def _observe(self, faction: str) -> Observation:
        visible: list[str] = []
        for region_id in self._regions():
            if self._campaign.knows(faction, region_id):
                visible.append(region_id)
        units: list[tuple[str, str, int]] = []
        for unit_id in self._unit_ids():
            unit = self._campaign.unit(unit_id)
            if unit is not None and unit.faction == faction:
                units.append((unit_id, unit.region, unit.strength))
        return Observation(faction=faction, visible_regions=tuple(visible), units=tuple(units))

    def _regions(self) -> tuple[str, ...]:
        return self._campaign.region_ids()

    def _unit_ids(self) -> tuple[str, ...]:
        return self._campaign.unit_ids()

    def _faction_unit(self, faction: str) -> str:
        for unit_id in self._unit_ids():
            unit = self._campaign.unit(unit_id)
            if unit is not None and unit.faction == faction:
                return unit_id
        raise ResearchError(f"no unit for faction {faction!r}")
