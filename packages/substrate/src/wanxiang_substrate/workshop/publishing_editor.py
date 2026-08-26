"""Publishing panel facade over the shared Workshop draft store."""

from __future__ import annotations

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.workshop.models import WorkshopDraft
from wanxiang_substrate.workshop.publishing import (
    PublishingDecision,
    PublishingPolicy,
    PublishingProfile,
)
from wanxiang_substrate.workshop.store import WorkshopDraftStore


class PublishingEditor:
    def __init__(self, drafts: WorkshopDraftStore, policy: PublishingPolicy | None = None) -> None:
        self._drafts = drafts
        self._policy = policy or PublishingPolicy()

    def save_profile(
        self,
        workshop_id: str,
        profile: PublishingProfile,
        *,
        expected_revision: int,
    ) -> WorkshopDraft:
        draft = self._drafts.get(workshop_id)
        if draft.revision != expected_revision:
            raise ContractError(
                f"publishing editor expected revision {expected_revision}, got {draft.revision}"
            )
        decision = self._policy.assess(profile)
        values = {field: getattr(draft, field) for field in draft.__dataclass_fields__}
        values.update(
            publishing=profile,
            publishing_profile_ref=profile.profile_id,
            revision=draft.revision + 1,
            status="publishable" if decision.publishable else "review_required",
        )
        return self._drafts.save(WorkshopDraft(**values), expected_revision=expected_revision)

    def assess(self, workshop_id: str) -> PublishingDecision:
        draft = self._drafts.get(workshop_id)
        if draft.publishing is None:
            raise ContractError("workshop has no publishing profile")
        return self._policy.assess(draft.publishing)


__all__ = ["PublishingEditor"]
