"""RC-001 Experience Studio minimal surface (G36H).

Read-only Studio queries composing the RC-001 living world: map, characters,
available actions, committed events, source canon, completion ledger and
branch baseline comparison. Reuses existing queries; no write path, no UI
authority.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.actions.registry import ActionRegistry
from wanxiang_substrate.ledger.completion import CompletionReviewLedger, CompletionStudio
from wanxiang_substrate.rc001.strategies import BaselineComparison, compare_to_baseline
from wanxiang_substrate.sources.canon import CompiledCanon
from wanxiang_substrate.spatial.query import SpatialQuery


@dataclass(frozen=True, slots=True)
class ExperienceViews:
    """Aggregated read-only Studio views over the RC-001 world."""

    places: tuple[str, ...]
    portals: tuple[str, ...]
    characters: tuple[str, ...]
    actions: tuple[str, ...]
    events: tuple[str, ...]
    source_claims: tuple[str, ...]
    completion_pending: tuple[str, ...]
    branch_matches_baseline: bool | None


class ExperienceStudio:
    """Read-only Studio queries (never mutates state)."""

    def __init__(
        self,
        *,
        state: InMemoryCanonicalState,
        actions: ActionRegistry,
        events: tuple[str, ...] = (),
        canon: CompiledCanon | None = None,
        completions: CompletionReviewLedger | None = None,
    ) -> None:
        self._state = state
        self._actions = actions
        self._events = events
        self._canon = canon
        self._completions = completions

    def views(
        self, *, baseline_hash: str | None = None, baseline_revision: int = 0
    ) -> ExperienceViews:
        spatial = SpatialQuery(self._state)
        places = tuple(sorted(p.value for p in spatial.places()))
        portals = tuple(sorted(p.value for p in spatial.portals()))
        characters = tuple(
            sorted(
                e.entity_id.value
                for e in self._state.entities()
                if e.entity_type in ("actor", "person")
            )
        )
        actions = tuple(d.action_type for d in self._actions.all())
        source_claims = (
            tuple(c.proposition for c in self._canon.runtime_view) if self._canon else ()
        )
        completion_pending = (
            tuple(c.completion_id for c in CompletionStudio(self._completions).pending_review())
            if self._completions
            else ()
        )
        matches: bool | None = None
        if baseline_hash is not None:
            comparison: BaselineComparison = compare_to_baseline(
                baseline_hash=baseline_hash,
                current_hash=self._state.semantic_hash(),
                current_revision=self._state.revision.value,
                baseline_revision=baseline_revision,
            )
            matches = comparison.matches
        return ExperienceViews(
            places=places,
            portals=portals,
            characters=characters,
            actions=actions,
            events=self._events,
            source_claims=source_claims,
            completion_pending=completion_pending,
            branch_matches_baseline=matches,
        )
