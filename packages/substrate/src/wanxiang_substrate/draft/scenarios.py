"""Scenario candidate mining (G59F)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.draft.model import WorldDraft


@dataclass(frozen=True, slots=True)
class ScenarioCandidate:
    scenario_id: str
    initial_time: str
    participants: tuple[str, ...]
    source_refs: tuple[str, ...]
    description: str

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ContractError("scenario requires an id")


class ScenarioMiner:
    """Mines runnable scenario start candidates from draft events."""

    def mine(self, draft: WorldDraft) -> tuple[ScenarioCandidate, ...]:
        candidates: list[ScenarioCandidate] = []
        # One candidate per distinct event date (deterministic cluster).
        by_date: dict[str, list[tuple[str, str]]] = {}
        for event_id, date in draft.events:
            by_date.setdefault(date, []).append((event_id, date))
        for index, (date, events) in enumerate(sorted(by_date.items()), start=1):
            participants = tuple(sorted({p for e in draft.relations for p in (e[0], e[1])})[:5])
            candidates.append(
                ScenarioCandidate(
                    scenario_id=f"scenario_{index}",
                    initial_time=date or "unknown",
                    participants=participants,
                    source_refs=(),
                    description=f"start at {date or 'unknown'} with {len(events)} event(s)",
                )
            )
        return tuple(candidates)
