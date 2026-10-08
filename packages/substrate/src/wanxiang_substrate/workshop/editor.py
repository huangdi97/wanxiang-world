"""Versioned Scenario/Experience editing and read-only Workshop preview."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.playable.experience import ExperiencePackage, PublishMode
from wanxiang_substrate.playable.models import ScenarioProfile
from wanxiang_substrate.workshop.models import WorkshopDraft
from wanxiang_substrate.workshop.store import WorkshopDraftStore


@dataclass(frozen=True, slots=True)
class EditorValidation:
    workshop_id: str
    mode: PublishMode
    ok: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorkshopPreview:
    workshop_id: str
    revision: int
    scenario_ref: str
    experience_ref: str
    preview_hash: str
    published: bool = False


class WorkshopEditor:
    """One editor facade for scenario and experience panels."""

    def __init__(self, drafts: WorkshopDraftStore) -> None:
        self._drafts = drafts

    def edit_scenario(
        self, workshop_id: str, scenario: ScenarioProfile, *, expected_revision: int
    ) -> WorkshopDraft:
        draft = self._drafts.get(workshop_id)
        self._require_base_revision(draft, expected_revision)
        if draft.world_draft_id and scenario.world_package_ref != draft.world_draft_id:
            raise ContractError("scenario package ref does not match workshop world draft")
        return self._save(
            draft,
            expected_revision,
            scenario=scenario,
            scenario_ref=scenario.scenario_id,
            status="review_required",
        )

    def edit_experience(
        self, workshop_id: str, experience: ExperiencePackage, *, expected_revision: int
    ) -> WorkshopDraft:
        draft = self._drafts.get(workshop_id)
        self._require_base_revision(draft, expected_revision)
        experience.validate(mode="preview")
        if draft.world_draft_id and experience.world_package_ref != draft.world_draft_id:
            raise ContractError("experience package ref does not match workshop world draft")
        return self._save(
            draft,
            expected_revision,
            experience=experience,
            experience_ref=experience.experience_id,
            status="previewable" if draft.scenario is not None else "review_required",
        )

    def validate(self, workshop_id: str, *, mode: PublishMode = "preview") -> EditorValidation:
        draft = self._drafts.get(workshop_id)
        reasons: list[str] = []
        if draft.scenario is None:
            reasons.append("scenario is not configured")
        if draft.experience is None:
            reasons.append("experience is not configured")
        if draft.scenario is not None and draft.scenario_ref != draft.scenario.scenario_id:
            reasons.append("scenario ref does not match scenario revision")
        if draft.experience is not None:
            if draft.experience_ref != draft.experience.experience_id:
                reasons.append("experience ref does not match experience revision")
            try:
                draft.experience.validate(mode=mode)
            except ContractError as exc:
                reasons.append(str(exc))
        return EditorValidation(workshop_id, mode, not reasons, tuple(reasons))

    def preview(self, workshop_id: str) -> WorkshopPreview:
        draft = self._drafts.get(workshop_id)
        validation = self.validate(workshop_id)
        if not validation.ok or draft.scenario is None or draft.experience is None:
            raise ContractError(
                "workshop draft is not previewable: " + "; ".join(validation.reasons)
            )
        payload = {
            "workshop_id": draft.workshop_id,
            "revision": draft.revision,
            "scenario": draft.scenario.to_dict(),
            "experience": draft.experience.to_dict(),
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return WorkshopPreview(
            draft.workshop_id,
            draft.revision,
            draft.scenario.scenario_id,
            draft.experience.experience_id,
            digest,
        )

    @staticmethod
    def _require_base_revision(draft: WorkshopDraft, expected_revision: int) -> None:
        if draft.revision != expected_revision:
            raise ContractError(
                f"workshop editor expected revision {expected_revision}, got {draft.revision}"
            )

    def _save(
        self, draft: WorkshopDraft, expected_revision: int, **changes: object
    ) -> WorkshopDraft:
        values = {field: getattr(draft, field) for field in draft.__dataclass_fields__}
        values.update(changes)
        values["revision"] = draft.revision + 1
        return self._drafts.save(WorkshopDraft(**values), expected_revision=expected_revision)


__all__ = ["EditorValidation", "WorkshopEditor", "WorkshopPreview"]
