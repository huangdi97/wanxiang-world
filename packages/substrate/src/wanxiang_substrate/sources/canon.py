"""Past/Character/Future canon compilation (G35E).

M32: at a chosen Scenario time point, compile source-backed canon claims into
PastCanon (before the scenario), CharacterCanon (character-bound claims up to
and including the scenario), and FutureCanon (after the scenario). FutureCanon
is visible ONLY on the control plane: the running world's runtime view never
contains future claims. Reuses G35B locators; pure and deterministic.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.locator import SourceLocator, segment_source, source_slice

Temporal = Literal["past", "present", "future"]
VALID_TEMPORALS = ("past", "present", "future")


@dataclass(frozen=True, slots=True)
class ScenarioPoint:
    """A concrete scenario time point in the source (a chapter/segment)."""

    scenario_id: str
    source_id: str
    time_ref: str
    locator: SourceLocator

    def __post_init__(self) -> None:
        if not self.scenario_id or not self.source_id or not self.time_ref:
            raise ContractError("scenario requires id, source id and time ref")


@dataclass(frozen=True, slots=True)
class CanonClaim:
    """A source-backed canon claim with a temporal bucket + optional character."""

    claim_id: str
    proposition: str
    temporal: Temporal
    locators: tuple[SourceLocator, ...]
    character_key: str | None = None
    status: Literal["pending", "eligible", "rejected"] = "pending"

    def __post_init__(self) -> None:
        if not self.claim_id or not self.proposition:
            raise ContractError("canon claim requires id and proposition")
        if self.temporal not in VALID_TEMPORALS:
            raise ContractError(f"invalid temporal bucket {self.temporal!r}")
        if not self.locators:
            raise ContractError("canon claim requires at least one evidence locator")

    def with_status(self, status: Literal["pending", "eligible", "rejected"]) -> CanonClaim:
        return CanonClaim(
            claim_id=self.claim_id,
            proposition=self.proposition,
            temporal=self.temporal,
            locators=self.locators,
            character_key=self.character_key,
            status=status,
        )


@dataclass(frozen=True, slots=True)
class CompiledCanon:
    """Canon compiled at a scenario point.

    runtime_view = PastCanon + CharacterCanon (never FutureCanon).
    control_plane_view = PastCanon + CharacterCanon + FutureCanon.
    """

    scenario: ScenarioPoint
    past: tuple[CanonClaim, ...]
    character: tuple[CanonClaim, ...]
    future: tuple[CanonClaim, ...]

    @property
    def runtime_view(self) -> tuple[CanonClaim, ...]:
        """Claims the running world may see at scenario time (no future)."""
        return self.past + self.character

    @property
    def control_plane_view(self) -> tuple[CanonClaim, ...]:
        """Full canon including FutureCanon; control plane only."""
        return self.past + self.character + self.future

    def character_canon(self, character_key: str) -> tuple[CanonClaim, ...]:
        """Per-character canon from the runtime view (identity/knowledge)."""
        return tuple(claim for claim in self.runtime_view if claim.character_key == character_key)


def scenario_at(
    locators: tuple[SourceLocator, ...],
    *,
    chapter: str,
    scenario_id: str = "scenario_001",
) -> ScenarioPoint:
    """Choose a concrete scenario time point at the first segment of a chapter."""
    for locator in locators:
        if locator.chapter == chapter:
            return ScenarioPoint(
                scenario_id=scenario_id,
                source_id=locator.source_id,
                time_ref=chapter,
                locator=locator,
            )
    raise ContractError(f"chapter {chapter!r} not present in source locators")


class CanonCompiler:
    """Deterministic canon compilation at a scenario time point.

    Pure: reads source text and caller-supplied claim rules; produces a
    CompiledCanon. Source eligibility is enforced by the existing SourceGate
    before this class is used; no write path exists here.
    """

    def __init__(
        self,
        *,
        extract_claims: Callable[[str], tuple[tuple[str, str | None], ...]],
    ) -> None:
        self._extract_claims = extract_claims

    def compile(
        self,
        *,
        scenario: ScenarioPoint,
        source_id: str,
        text: str,
    ) -> CompiledCanon:
        """Compile canon; re-running on same inputs is identical."""
        locators = segment_source(source_id, text)
        index_by_locator = {loc.locator: index for index, loc in enumerate(locators)}
        if scenario.locator.locator not in index_by_locator:
            raise ContractError("scenario locator is not a segment of the source")
        scenario_index = index_by_locator[scenario.locator.locator]
        past: list[CanonClaim] = []
        character: list[CanonClaim] = []
        future: list[CanonClaim] = []
        claim_index = 0
        for locator in locators:
            segment_index = index_by_locator[locator.locator]
            if segment_index < scenario_index:
                temporal: Temporal = "past"
            elif segment_index == scenario_index:
                temporal = "present"
            else:
                temporal = "future"
            for proposition, character_key in self._extract_claims(source_slice(text, locator)):
                claim_index += 1
                claim = CanonClaim(
                    claim_id=f"canon_{claim_index:04d}",
                    proposition=proposition,
                    temporal=temporal,
                    locators=(locator,),
                    character_key=character_key,
                )
                if temporal == "past":
                    past.append(claim)
                elif temporal == "present":
                    character.append(claim)
                else:
                    future.append(claim)
        return CompiledCanon(
            scenario=scenario,
            past=tuple(past),
            character=tuple(character),
            future=tuple(future),
        )
