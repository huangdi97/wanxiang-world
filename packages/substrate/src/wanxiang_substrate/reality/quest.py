"""Quest projection over Opportunity records (M88 / G91F)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.reality.challenge import Opportunity
from wanxiang_substrate.reality.errors import RealityError

QuestStatus = Literal["active", "ready", "ignored", "declined", "expired", "completed"]


class QuestProjectionError(RealityError):
    code = "quest_projection_error"


@dataclass(frozen=True, slots=True)
class CommittedStateEvidence:
    """Refs extracted from committed state/events; narrative text is not accepted."""

    state_refs: tuple[str, ...] = ()
    event_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        refs = (*self.state_refs, *self.event_refs)
        if any(not ref for ref in refs):
            raise QuestProjectionError("committed evidence refs must be non-empty")
        object.__setattr__(self, "state_refs", tuple(dict.fromkeys(self.state_refs)))
        object.__setattr__(self, "event_refs", tuple(dict.fromkeys(self.event_refs)))

    @property
    def refs(self) -> frozenset[str]:
        return frozenset((*self.state_refs, *self.event_refs))


@dataclass(frozen=True, slots=True)
class QuestObjective:
    """Optional or required objective keyed by a committed evidence ref."""

    objective_id: str
    label: str
    evidence_ref: str
    optional: bool = False

    def __post_init__(self) -> None:
        if not self.objective_id or not self.label or not self.evidence_ref:
            raise QuestProjectionError("quest objective requires id, label and evidence ref")


@dataclass(frozen=True, slots=True)
class QuestObjectiveProgress:
    objective_id: str
    label: str
    evidence_ref: str
    optional: bool
    completed: bool


@dataclass(frozen=True, slots=True)
class QuestProjection:
    """Read-only experience view; it never becomes world truth."""

    quest_id: str
    opportunity_id: str
    title: str
    status: QuestStatus
    progress: float
    objectives: tuple[QuestObjectiveProgress, ...]
    source_refs: tuple[str, ...]
    world_state_refs: tuple[str, ...]
    projection_only: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "quest_id": self.quest_id,
            "opportunity_id": self.opportunity_id,
            "title": self.title,
            "status": self.status,
            "progress": self.progress,
            "objectives": [
                {
                    "objective_id": objective.objective_id,
                    "label": objective.label,
                    "evidence_ref": objective.evidence_ref,
                    "optional": objective.optional,
                    "completed": objective.completed,
                }
                for objective in self.objectives
            ],
            "source_refs": list(self.source_refs),
            "world_state_refs": list(self.world_state_refs),
            "projection_only": self.projection_only,
        }


class QuestProjectionAdapter:
    """Projects Opportunity into UI/task shape from committed refs only."""

    def project(
        self,
        opportunity: Opportunity,
        committed: CommittedStateEvidence,
        *,
        optional_objectives: tuple[QuestObjective, ...] = (),
        narrative_text: str | None = None,
    ) -> QuestProjection:
        if narrative_text is not None:
            raise QuestProjectionError("narrative text cannot provide quest progress")
        required = tuple(
            QuestObjective(
                objective_id=f"evidence:{index}",
                label=evidence_ref,
                evidence_ref=evidence_ref,
            )
            for index, evidence_ref in enumerate(opportunity.evidence_refs, start=1)
        )
        objectives = (*required, *optional_objectives)
        ids = [objective.objective_id for objective in objectives]
        refs = [objective.evidence_ref for objective in objectives]
        if len(ids) != len(set(ids)) or len(refs) != len(set(refs)):
            raise QuestProjectionError("quest objectives and evidence refs must be unique")
        progress_items = tuple(
            QuestObjectiveProgress(
                objective_id=objective.objective_id,
                label=objective.label,
                evidence_ref=objective.evidence_ref,
                optional=objective.optional,
                completed=objective.evidence_ref in committed.refs,
            )
            for objective in objectives
        )
        required_items = tuple(item for item in progress_items if not item.optional)
        completed_required = sum(item.completed for item in required_items)
        progress = completed_required / len(required_items) if required_items else 0.0
        status: QuestStatus
        if opportunity.status == "ignored":
            status = "ignored"
        elif opportunity.status == "declined":
            status = "declined"
        elif opportunity.status == "expired":
            status = "expired"
        elif opportunity.status == "completed":
            status = "completed"
        else:
            status = "ready" if progress == 1.0 else "active"
        return QuestProjection(
            quest_id=f"quest:{opportunity.opportunity_id}",
            opportunity_id=opportunity.opportunity_id,
            title=opportunity.condition,
            status=status,
            progress=progress,
            objectives=progress_items,
            source_refs=opportunity.evidence_refs,
            world_state_refs=opportunity.world_state_refs,
        )

    def from_opportunity(
        self,
        opportunity: Opportunity,
        *,
        committed_state_refs: tuple[str, ...] = (),
        committed_event_refs: tuple[str, ...] = (),
        optional_objectives: tuple[QuestObjective, ...] = (),
    ) -> QuestProjection:
        return self.project(
            opportunity,
            CommittedStateEvidence(committed_state_refs, committed_event_refs),
            optional_objectives=optional_objectives,
        )
