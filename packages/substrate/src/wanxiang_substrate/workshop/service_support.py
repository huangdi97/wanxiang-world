"""Shared Workshop product-shell assembly helpers."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.experience import ExperiencePackage
from wanxiang_substrate.playable.models import ScenarioProfile, Visibility
from wanxiang_substrate.preview import PreviewInstall
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.workshop.editor import WorkshopEditor
from wanxiang_substrate.workshop.genesis_provider import PromptGenesisRun
from wanxiang_substrate.workshop.hybrid_genesis import HybridGenesisResult
from wanxiang_substrate.workshop.models import CreationMode, WorkshopDraft
from wanxiang_substrate.workshop.publishing import (
    PackageMetadata,
    PublishingProfile,
    RightsSummary,
)
from wanxiang_substrate.workshop.publishing_editor import PublishingEditor
from wanxiang_substrate.workshop.service_models import WorkshopBuild
from wanxiang_substrate.workshop.store import WorkshopDraftStore


def start_workshop_draft(
    drafts: WorkshopDraftStore,
    workshop_id: str,
    *,
    mode: CreationMode,
    owner_id: str,
    package: WorldPackageDraft,
    source_job_id: str = "",
    intent_id: str = "",
) -> WorkshopDraft:
    draft = drafts.create(workshop_id, mode=mode, owner_id=owner_id)
    values = {field: getattr(draft, field) for field in draft.__dataclass_fields__}
    values.update(
        world_draft_id=package.package_id,
        world_draft_revision=package.draft_revision,
        source_job_id=source_job_id,
        intent_id=intent_id,
        revision=draft.revision + 1,
        status="review_required",
    )
    return drafts.save(WorkshopDraft(**values), expected_revision=draft.revision)


def make_product_profile(
    drafts: WorkshopDraftStore,
    editor: WorkshopEditor,
    workshop_id: str,
    *,
    owner_id: str,
    package: WorldPackageDraft,
    visibility: Visibility,
    display_name: str | None,
    source_refs: tuple[str, ...],
    rights: RightsSummary,
    review_complete: bool,
) -> PublishingProfile:
    default_actor = package.draft.entities[0][0] if package.draft.entities else ""
    scenario = ScenarioProfile(
        f"scenario:{workshop_id}", package.package_id, default_actor_ref=default_actor
    )
    editor.edit_scenario(
        workshop_id,
        scenario,
        expected_revision=drafts.get(workshop_id).revision,
    )
    experience = ExperiencePackage(
        f"experience:{workshop_id}",
        package.package_id,
        scenario.scenario_id,
        "projection:player",
        visibility=visibility,
        owner_id=owner_id,
        display_name=display_name or package.manifest.name,
    )
    editor.edit_experience(
        workshop_id,
        experience,
        expected_revision=drafts.get(workshop_id).revision,
    )
    return PublishingProfile(
        f"publishing:{workshop_id}",
        visibility,
        owner_id,
        PackageMetadata(
            package.package_id,
            str(package.manifest.version),
            display_name or package.manifest.name,
            categories=("workshop",),
            tags=("source",) if len(source_refs) == 1 else ("hybrid", "workshop"),
            compatibility=("v5.4",),
            provenance_refs=source_refs,
        ),
        rights,
        review_complete=review_complete,
    )


def finish_source(
    drafts: WorkshopDraftStore,
    editor: WorkshopEditor,
    publisher: PublishingEditor,
    workshop_id: str,
    *,
    owner_id: str,
    package: WorldPackageDraft,
    preview: PreviewInstall,
    sources: tuple[SourceRecord, ...],
    visibility: Visibility,
    display_name: str | None,
    source_job_id: str,
) -> WorkshopBuild:
    start_workshop_draft(
        drafts,
        workshop_id,
        mode="source",
        owner_id=owner_id,
        package=package,
        source_job_id=source_job_id,
    )
    profile = make_product_profile(
        drafts,
        editor,
        workshop_id,
        owner_id=owner_id,
        package=package,
        visibility=visibility,
        display_name=display_name,
        source_refs=tuple(source.source_id for source in sources),
        rights=RightsSummary.from_sources(sources),
        review_complete=True,
    )
    publisher.save_profile(workshop_id, profile, expected_revision=drafts.get(workshop_id).revision)
    return WorkshopBuild(drafts.get(workshop_id), package, preview, publisher.assess(workshop_id))


def finish_prompt(
    drafts: WorkshopDraftStore,
    editor: WorkshopEditor,
    publisher: PublishingEditor,
    workshop_id: str,
    *,
    owner_id: str,
    package: WorldPackageDraft,
    preview: PreviewInstall,
    run: PromptGenesisRun,
    visibility: Visibility,
    display_name: str | None,
) -> WorkshopBuild:
    intent_id = run.contract.intent.intent_id
    start_workshop_draft(
        drafts,
        workshop_id,
        mode="prompt",
        owner_id=owner_id,
        package=package,
        intent_id=intent_id,
    )
    profile = make_product_profile(
        drafts,
        editor,
        workshop_id,
        owner_id=owner_id,
        package=package,
        visibility=visibility,
        display_name=display_name,
        source_refs=(intent_id,),
        rights=RightsSummary.creator_intent(intent_id),
        review_complete=run.contract.review_gate.ready_for_preview,
    )
    publisher.save_profile(workshop_id, profile, expected_revision=drafts.get(workshop_id).revision)
    return WorkshopBuild(
        drafts.get(workshop_id), package, preview, publisher.assess(workshop_id), prompt_run=run
    )


def finish_hybrid(
    drafts: WorkshopDraftStore,
    editor: WorkshopEditor,
    publisher: PublishingEditor,
    workshop_id: str,
    *,
    owner_id: str,
    package: WorldPackageDraft,
    preview: PreviewInstall,
    sources: tuple[SourceRecord, ...],
    run: PromptGenesisRun,
    hybrid: HybridGenesisResult,
    visibility: Visibility,
    display_name: str | None,
    source_job_id: str,
) -> WorkshopBuild:
    intent_id = run.contract.intent.intent_id
    start_workshop_draft(
        drafts,
        workshop_id,
        mode="hybrid",
        owner_id=owner_id,
        package=package,
        source_job_id=source_job_id,
        intent_id=intent_id,
    )
    profile = make_product_profile(
        drafts,
        editor,
        workshop_id,
        owner_id=owner_id,
        package=package,
        visibility=visibility,
        display_name=display_name,
        source_refs=tuple(source.source_id for source in sources) + (intent_id,),
        rights=RightsSummary.from_sources(sources),
        review_complete=run.contract.review_gate.ready_for_preview,
    )
    publisher.save_profile(workshop_id, profile, expected_revision=drafts.get(workshop_id).revision)
    return WorkshopBuild(
        drafts.get(workshop_id),
        package,
        preview,
        publisher.assess(workshop_id),
        prompt_run=run,
        hybrid=hybrid,
    )


def refresh_build(
    drafts: WorkshopDraftStore,
    publisher: PublishingEditor,
    current: WorkshopBuild,
    prompt_run: PromptGenesisRun,
) -> WorkshopBuild:
    return replace(
        current,
        workshop=drafts.get(current.workshop.workshop_id),
        publishing=publisher.assess(current.workshop.workshop_id),
        prompt_run=prompt_run,
    )


__all__ = [
    "finish_hybrid",
    "finish_prompt",
    "finish_source",
    "make_product_profile",
    "refresh_build",
    "start_workshop_draft",
]
