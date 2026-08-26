"""Immutable revision store shared by all World Workshop creation panels."""

from __future__ import annotations

from wanxiang_domain.errors import ContractError, NotFound

from wanxiang_substrate.workshop.models import CreationMode, WorkshopDraft, WorkshopStatus


class DraftRevisionConflict(ContractError):
    """Raised when a workshop editor saves against a stale revision."""

    code = "workshop_draft_revision_conflict"


class WorkshopDraftStore:
    """One versioned draft port for Source, Prompt and Hybrid editors."""

    def __init__(self) -> None:
        self._history: dict[str, dict[int, WorkshopDraft]] = {}

    def create(self, workshop_id: str, *, mode: CreationMode, owner_id: str) -> WorkshopDraft:
        if workshop_id in self._history:
            raise ContractError(f"workshop draft {workshop_id!r} already exists")
        draft = WorkshopDraft(workshop_id, 1, mode, owner_id)
        self._history[workshop_id] = {1: draft}
        return draft

    def save(self, draft: WorkshopDraft, *, expected_revision: int) -> WorkshopDraft:
        revisions = self._history.get(draft.workshop_id)
        if revisions is None:
            raise NotFound(f"workshop draft {draft.workshop_id!r} not found")
        latest = max(revisions)
        if expected_revision != latest or draft.revision != latest + 1:
            raise DraftRevisionConflict(
                f"workshop draft {draft.workshop_id!r} expected {expected_revision}, "
                f"latest {latest}"
            )
        revisions[draft.revision] = draft
        return draft

    def get(self, workshop_id: str) -> WorkshopDraft:
        revisions = self._history.get(workshop_id)
        if not revisions:
            raise NotFound(f"workshop draft {workshop_id!r} not found")
        return revisions[max(revisions)]

    def get_revision(self, workshop_id: str, revision: int) -> WorkshopDraft:
        revisions = self._history.get(workshop_id)
        if not revisions or revision not in revisions:
            raise NotFound(f"workshop draft {workshop_id!r} revision {revision} not found")
        return revisions[revision]

    def history(self, workshop_id: str) -> tuple[WorkshopDraft, ...]:
        revisions = self._history.get(workshop_id)
        if not revisions:
            raise NotFound(f"workshop draft {workshop_id!r} not found")
        return tuple(revisions[index] for index in sorted(revisions))

    def transition(
        self,
        workshop_id: str,
        *,
        status: WorkshopStatus,
        expected_revision: int,
        **changes: object,
    ) -> WorkshopDraft:
        current = self.get(workshop_id)
        values = {field: getattr(current, field) for field in current.__dataclass_fields__}
        values.update(changes)
        values.update(revision=current.revision + 1, status=status)
        return self.save(WorkshopDraft(**values), expected_revision=expected_revision)


__all__ = ["DraftRevisionConflict", "WorkshopDraftStore"]
