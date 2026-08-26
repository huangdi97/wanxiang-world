"""Versioned product-side records for the shared World Workshop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

CreationMode = Literal["source", "prompt", "hybrid"]
WorkshopStatus = Literal["draft", "review_required", "previewable", "publishable", "published"]
PanelKind = Literal[
    "world_home",
    "source",
    "prompt",
    "hybrid",
    "scenario",
    "experience",
    "publishing",
    "review",
    "registry",
]


@dataclass(frozen=True, slots=True)
class WorkshopPanel:
    """One product panel backed by the common workshop document."""

    panel_id: PanelKind
    title: str
    draft_path: str
    read_only: bool = False

    def __post_init__(self) -> None:
        if not self.panel_id or not self.title or not self.draft_path:
            raise ContractError("workshop panel requires id, title and draft path")

    def to_dict(self) -> dict[str, object]:
        return {
            "panel_id": self.panel_id,
            "title": self.title,
            "draft_path": self.draft_path,
            "read_only": self.read_only,
        }


@dataclass(frozen=True, slots=True)
class WorkshopHome:
    """Information architecture for the World home and creation entry points."""

    panels: tuple[WorkshopPanel, ...]
    creation_modes: tuple[CreationMode, ...] = ("source", "prompt", "hybrid")
    shared_draft_backend: str = "wanxiang_substrate.workshop.WorkshopDraftStore"

    def __post_init__(self) -> None:
        if not self.panels:
            raise ContractError("workshop home requires at least one panel")
        if len({panel.panel_id for panel in self.panels}) != len(self.panels):
            raise ContractError("workshop panel ids must be unique")
        if set(self.creation_modes) != {"source", "prompt", "hybrid"}:
            raise ContractError("workshop must expose source, prompt and hybrid modes")

    def to_dict(self) -> dict[str, object]:
        return {
            "panels": [panel.to_dict() for panel in self.panels],
            "creation_modes": list(self.creation_modes),
            "shared_draft_backend": self.shared_draft_backend,
        }


@dataclass(frozen=True, slots=True)
class WorkshopDraft:
    """Immutable product draft pointer; canonical world state is never embedded."""

    workshop_id: str
    revision: int
    mode: CreationMode
    owner_id: str
    status: WorkshopStatus = "draft"
    world_draft_id: str = ""
    world_draft_revision: int = 0
    source_job_id: str = ""
    intent_id: str = ""
    scenario_ref: str = ""
    experience_ref: str = ""
    publishing_profile_ref: str = ""
    provenance_refs: tuple[str, ...] = ()
    generated_claim_refs: tuple[str, ...] = ()
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.workshop_id or not self.owner_id:
            raise ContractError("workshop draft requires workshop and owner ids")
        if self.revision < 1 or self.schema_version != 1:
            raise ContractError("unsupported workshop draft revision or schema")
        if self.mode not in {"source", "prompt", "hybrid"}:
            raise ContractError(f"unsupported workshop creation mode {self.mode!r}")
        if self.status not in {
            "draft",
            "review_required",
            "previewable",
            "publishable",
            "published",
        }:
            raise ContractError(f"unsupported workshop draft status {self.status!r}")
        if self.world_draft_revision < 0:
            raise ContractError("world draft revision cannot be negative")
        if len(set(self.provenance_refs)) != len(self.provenance_refs):
            raise ContractError("workshop provenance refs must be unique")
        if len(set(self.generated_claim_refs)) != len(self.generated_claim_refs):
            raise ContractError("generated claim refs must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "workshop_id": self.workshop_id,
            "revision": self.revision,
            "mode": self.mode,
            "owner_id": self.owner_id,
            "status": self.status,
            "world_draft_id": self.world_draft_id,
            "world_draft_revision": self.world_draft_revision,
            "source_job_id": self.source_job_id,
            "intent_id": self.intent_id,
            "scenario_ref": self.scenario_ref,
            "experience_ref": self.experience_ref,
            "publishing_profile_ref": self.publishing_profile_ref,
            "provenance_refs": list(self.provenance_refs),
            "generated_claim_refs": list(self.generated_claim_refs),
        }
