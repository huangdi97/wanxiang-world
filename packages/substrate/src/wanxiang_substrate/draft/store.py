"""WorldDraft store: save / load / revision (G59D).

Versioned draft store with immutable revisions: saving a new revision never
mutates an old one; loading by id returns the latest; a prior revision can be
restored (re-revisioned). Persistence is in-memory for now, behind a single
store boundary (no second state system).
"""

from __future__ import annotations

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.draft.model import WorldDraft


class DraftNotFound(ContractError):
    code = "draft_not_found"


class DraftStore:
    def __init__(self) -> None:
        self._drafts: dict[str, dict[int, WorldDraft]] = {}

    def create(self, draft_id: str, *, constitution_ref: str = "") -> WorldDraft:
        if draft_id in self._drafts:
            raise ContractError(f"draft {draft_id!r} already exists")
        draft = WorldDraft(
            draft_id=draft_id,
            revision=1,
            status="CREATED",
            constitution_ref=constitution_ref,
        )
        self._drafts[draft_id] = {1: draft}
        return draft

    def save(self, draft: WorldDraft) -> WorldDraft:
        if draft.draft_id not in self._drafts:
            raise DraftNotFound(f"draft {draft.draft_id!r} not found")
        revisions = self._drafts[draft.draft_id]
        latest = max(revisions)
        if draft.revision <= latest:
            raise ContractError(
                f"draft {draft.draft_id!r} revision {draft.revision} is not newer than {latest}"
            )
        revisions[draft.revision] = draft
        return draft

    def load(self, draft_id: str) -> WorldDraft | None:
        revisions = self._drafts.get(draft_id)
        if not revisions:
            return None
        return revisions[max(revisions)]

    def require(self, draft_id: str) -> WorldDraft:
        draft = self.load(draft_id)
        if draft is None:
            raise DraftNotFound(f"draft {draft_id!r} not found")
        return draft

    def load_revision(self, draft_id: str, revision: int) -> WorldDraft:
        revisions = self._drafts.get(draft_id)
        if not revisions or revision not in revisions:
            raise DraftNotFound(f"draft {draft_id!r} revision {revision} not found")
        return revisions[revision]

    def revision_count(self, draft_id: str) -> int:
        revisions = self._drafts.get(draft_id)
        return len(revisions) if revisions else 0

    def next_revision(self, draft_id: str) -> int:
        revisions = self._drafts.get(draft_id)
        return (max(revisions) + 1) if revisions else 1
