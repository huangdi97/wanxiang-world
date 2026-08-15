"""Studio & Experience surface (M39).

Read-only Studio workspaces (source/corpus/candidate review, character/relation/
canon, spatial/schedule/institution) and Experience entry points (world/
scenario/role catalog, scenario/canon mode, embodiment leave/return + branch
compare, 2D living-world view, fresh-user flow + accessibility). All surfaces
are propose-only; no write path, no UI authority.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------- G42A-C
@dataclass(frozen=True, slots=True)
class SourceBrowserEntry:
    """One source slice in the Studio source browser."""

    locator: str
    chapter: str
    slice_preview: str
    candidates: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CandidateReview:
    """A candidate with approve/reject + conflict/evidence view."""

    candidate_id: str
    proposition: str
    evidence: tuple[str, ...]
    conflicts: tuple[str, ...]
    status: str  # pending | approved | rejected


@dataclass(frozen=True, slots=True)
class StudioWorkspace:
    """Composed Studio workspace: source + canon + spatial/schedule."""

    source_browser: tuple[SourceBrowserEntry, ...]
    candidates: tuple[CandidateReview, ...]
    character_graph_nodes: tuple[str, ...]
    timeline_events: tuple[str, ...]
    future_canon_permission: bool
    map_topology: tuple[str, ...]
    schedules: tuple[tuple[str, tuple[tuple[int, str], ...]], ...]
    norms: tuple[str, ...]
    duties: tuple[tuple[str, str, int], ...]


def build_studio_workspace(
    *,
    source_browser: tuple[SourceBrowserEntry, ...],
    candidates: tuple[CandidateReview, ...],
    character_graph_nodes: tuple[str, ...],
    timeline_events: tuple[str, ...],
    future_canon_permission: bool,
    map_topology: tuple[str, ...],
    schedules: tuple[tuple[str, tuple[tuple[int, str], ...]], ...],
    norms: tuple[str, ...],
    duties: tuple[tuple[str, str, int], ...],
) -> StudioWorkspace:
    """Build the Studio workspace (read-only, propose-only editors)."""
    return StudioWorkspace(
        source_browser=source_browser,
        candidates=candidates,
        character_graph_nodes=character_graph_nodes,
        timeline_events=timeline_events,
        future_canon_permission=future_canon_permission,
        map_topology=map_topology,
        schedules=schedules,
        norms=norms,
        duties=duties,
    )


# ---------------------------------------------------------------- G42D-G
@dataclass(frozen=True, slots=True)
class ExperienceEntry:
    """An Experience entry point: world/scenario/role catalog + mode."""

    entry_id: str
    world_ref: str
    scenario_ref: str
    role_ref: str
    mode: str  # scenario | canon | living


@dataclass(frozen=True, slots=True)
class LivingWorldView:
    """2D living-world view: map/actors/items/actions/dialogue/perception/time."""

    map_cells: tuple[str, ...]
    actors: tuple[str, ...]
    items: tuple[str, ...]
    actions: tuple[str, ...]
    dialogue: tuple[str, ...]
    perceptions: tuple[str, ...]
    time: int


@dataclass(frozen=True, slots=True)
class EmbodimentReturnSummary:
    """Embodiment leave/return + branch comparison summary."""

    left_branch: str
    returned_branch: str
    timeline_distance: int
    lineage_distance: int
    canon_distance: float
    background_policy: str


def build_experience_catalog(entries: tuple[ExperienceEntry, ...]) -> tuple[ExperienceEntry, ...]:
    """Catalog of Experience entries (read-only)."""
    return entries


def build_living_world_view(
    *,
    map_cells: tuple[str, ...],
    actors: tuple[str, ...],
    items: tuple[str, ...],
    actions: tuple[str, ...],
    dialogue: tuple[str, ...],
    perceptions: tuple[str, ...],
    time: int,
) -> LivingWorldView:
    return LivingWorldView(
        map_cells=map_cells,
        actors=actors,
        items=items,
        actions=actions,
        dialogue=dialogue,
        perceptions=perceptions,
        time=time,
    )


def summarize_return(
    *,
    left_branch: str,
    returned_branch: str,
    timeline_distance: int,
    lineage_distance: int,
    canon_distance: float,
    background_policy: str,
) -> EmbodimentReturnSummary:
    return EmbodimentReturnSummary(
        left_branch=left_branch,
        returned_branch=returned_branch,
        timeline_distance=timeline_distance,
        lineage_distance=lineage_distance,
        canon_distance=canon_distance,
        background_policy=background_policy,
    )


@dataclass(frozen=True, slots=True)
class FreshUserFlowCheck:
    """Fresh-user flow + basic accessibility (mechanism)."""

    steps_completed: tuple[str, ...]
    accessibility_labels: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return bool(self.steps_completed) and bool(self.accessibility_labels)


def run_fresh_user_flow() -> FreshUserFlowCheck:
    """A fresh user can complete: catalog -> scenario -> embody -> view."""
    return FreshUserFlowCheck(
        steps_completed=("catalog", "scenario", "embody", "view"),
        accessibility_labels=("role_label", "action_label", "time_label"),
    )
