"""WorldDraft v1 model (G59D).

WorldDraft is the editable Forge compile intermediate (05_WORLD_DRAFT_SCHEMA):
NOT a running world and never owns Commit Authority. Revisioned, saveable,
restorable, and recompilable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from wanxiang_domain.errors import ContractError

DraftStatus = Literal[
    "CREATED",
    "INGESTING",
    "DISTILLING",
    "FUSING",
    "REVIEW_REQUIRED",
    "COMPLETION_REQUIRED",
    "VALIDATING",
    "READY_TO_COMPILE",
    "PREVIEWABLE",
    "PUBLISHABLE",
]
VALID_STATUSES = (
    "CREATED",
    "INGESTING",
    "DISTILLING",
    "FUSING",
    "REVIEW_REQUIRED",
    "COMPLETION_REQUIRED",
    "VALIDATING",
    "READY_TO_COMPILE",
    "PREVIEWABLE",
    "PUBLISHABLE",
)
# Allowed forward transitions (draft lifecycle).
DRAFT_TRANSITIONS: dict[DraftStatus, tuple[DraftStatus, ...]] = {
    "CREATED": ("INGESTING",),
    "INGESTING": ("DISTILLING",),
    "DISTILLING": ("FUSING", "REVIEW_REQUIRED"),
    "FUSING": ("REVIEW_REQUIRED", "COMPLETION_REQUIRED"),
    "REVIEW_REQUIRED": ("COMPLETION_REQUIRED", "VALIDATING", "DISTILLING"),
    "COMPLETION_REQUIRED": ("VALIDATING", "REVIEW_REQUIRED"),
    "VALIDATING": ("READY_TO_COMPILE", "COMPLETION_REQUIRED"),
    "READY_TO_COMPILE": ("PREVIEWABLE",),
    "PREVIEWABLE": ("PUBLISHABLE", "VALIDATING"),
    "PUBLISHABLE": ("PREVIEWABLE",),
}


@dataclass(frozen=True, slots=True)
class WorldDraft:
    """Editable compile intermediate; never a runtime state."""

    draft_id: str
    revision: int
    status: DraftStatus
    source_refs: tuple[str, ...] = ()
    source_versions: tuple[tuple[str, str], ...] = ()
    constitution_ref: str = ""
    selected_domains: tuple[str, ...] = ()
    dependency_lock: tuple[str, ...] = ()
    entities: tuple[tuple[str, str], ...] = ()  # (key, display_name)
    aliases: tuple[tuple[str, str], ...] = ()  # (identity_key, alias)
    character_profiles: tuple[str, ...] = ()
    organizations: tuple[str, ...] = ()
    relations: tuple[tuple[str, str, str], ...] = ()  # (source, target, type)
    places: tuple[str, ...] = ()
    objects: tuple[str, ...] = ()
    events: tuple[tuple[str, str], ...] = ()  # (event_id, date)
    knowledge_boundaries: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    skills: tuple[str, ...] = ()
    completion_items: tuple[str, ...] = ()
    unresolved_conflicts: tuple[str, ...] = ()
    unresolved_rights: tuple[str, ...] = ()
    scenario_candidates: tuple[str, ...] = ()
    genesis_candidates: tuple[str, ...] = ()
    coverage: float = 0.0
    uncertainty: float = 0.0
    quality: float = 0.0
    compiler_metadata: dict[str, str] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        if not self.draft_id:
            raise ContractError("draft requires an id")
        if self.revision < 1:
            raise ContractError("draft revision must be >= 1")
        if self.status not in VALID_STATUSES:
            raise ContractError(f"invalid draft status {self.status!r}")
        if not (0.0 <= self.coverage <= 1.0):
            raise ContractError("coverage must be within [0,1]")
        if not (0.0 <= self.uncertainty <= 1.0):
            raise ContractError("uncertainty must be within [0,1]")
        if not (0.0 <= self.quality <= 1.0):
            raise ContractError("quality must be within [0,1]")

    def can_transition(self, next_status: DraftStatus) -> bool:
        return next_status in DRAFT_TRANSITIONS[self.status]

    def with_status(self, next_status: DraftStatus) -> WorldDraft:
        if not self.can_transition(next_status):
            raise ContractError(
                f"draft {self.draft_id!r} cannot move from {self.status} to {next_status}"
            )
        return WorldDraft(
            draft_id=self.draft_id,
            revision=self.revision,
            status=next_status,
            source_refs=self.source_refs,
            source_versions=self.source_versions,
            constitution_ref=self.constitution_ref,
            selected_domains=self.selected_domains,
            dependency_lock=self.dependency_lock,
            entities=self.entities,
            aliases=self.aliases,
            character_profiles=self.character_profiles,
            organizations=self.organizations,
            relations=self.relations,
            places=self.places,
            objects=self.objects,
            events=self.events,
            knowledge_boundaries=self.knowledge_boundaries,
            rules=self.rules,
            skills=self.skills,
            completion_items=self.completion_items,
            unresolved_conflicts=self.unresolved_conflicts,
            unresolved_rights=self.unresolved_rights,
            scenario_candidates=self.scenario_candidates,
            genesis_candidates=self.genesis_candidates,
            coverage=self.coverage,
            uncertainty=self.uncertainty,
            quality=self.quality,
            compiler_metadata=dict(self.compiler_metadata),
        )
