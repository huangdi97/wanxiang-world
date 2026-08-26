"""Shared Source/Prompt/Hybrid Workshop service over the v5.4 product chain."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.playable.models import Visibility
from wanxiang_substrate.preview import PreviewRegistry
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.workshop.editor import WorkshopEditor
from wanxiang_substrate.workshop.factory import (
    compile_preview_draft,
    hybrid_world_draft,
    prompt_world_draft,
)
from wanxiang_substrate.workshop.genesis_contract import CreatorIntent
from wanxiang_substrate.workshop.genesis_provider import (
    PromptGenesisCheckpoint,
    PromptGenesisProviderService,
    PromptGenesisRun,
)
from wanxiang_substrate.workshop.home import WorldWorkshop
from wanxiang_substrate.workshop.hybrid_genesis import claim_from_candidate, fuse_hybrid_genesis
from wanxiang_substrate.workshop.publishing_editor import PublishingEditor
from wanxiang_substrate.workshop.service_models import WorkshopBuild
from wanxiang_substrate.workshop.service_support import (
    finish_hybrid,
    finish_prompt,
    finish_source,
    refresh_build,
)
from wanxiang_substrate.workshop.store import WorkshopDraftStore


class WorkshopService:
    """One shared editor/orchestration facade; canonical commits stay elsewhere."""

    def __init__(
        self,
        authoring: AuthoringService | None = None,
        *,
        providers: ProviderRouter | None = None,
        drafts: WorkshopDraftStore | None = None,
    ) -> None:
        self.authoring = authoring or AuthoringService(providers=providers)
        self.providers = providers or self.authoring.providers
        self.drafts = drafts or WorkshopDraftStore()
        self.editor = WorkshopEditor(self.drafts)
        self.publishing_editor = PublishingEditor(self.drafts)
        self.information = WorldWorkshop(self.drafts)
        self.previews = PreviewRegistry()
        self._builds: dict[str, WorkshopBuild] = {}
        self._prompt_runs: dict[str, PromptGenesisRun] = {}

    def home(self):
        return self.information.home()

    def create_from_source(
        self,
        workshop_id: str,
        *,
        owner_id: str,
        sources: tuple[SourceRecord, ...],
        profile: str = "book",
        visibility: Visibility = "private",
        display_name: str | None = None,
        semantic_provider: str | None = None,
    ) -> WorkshopBuild:
        result = OneClickAuthoring(self.authoring).run(
            f"workshop_job_{workshop_id}",
            sources,
            profile=profile,
            semantic_provider=semantic_provider,
        )
        package = result.package
        build = finish_source(
            self.drafts,
            self.editor,
            self.publishing_editor,
            workshop_id,
            owner_id=owner_id,
            package=package,
            preview=self.previews.install(package),
            sources=sources,
            visibility=visibility,
            display_name=display_name,
            source_job_id=result.job_id,
        )
        self._builds[workshop_id] = build
        return build

    def create_from_prompt(
        self,
        workshop_id: str,
        *,
        owner_id: str,
        intent: CreatorIntent,
        visibility: Visibility = "private",
        display_name: str | None = None,
    ) -> WorkshopBuild:
        run = PromptGenesisProviderService(self.providers).generate(intent, private_source=True)
        draft = prompt_world_draft(
            run.contract,
            draft_id=f"wd_{workshop_id}",
            provider_id=run.provider_id,
        )
        package = compile_preview_draft(draft)
        build = finish_prompt(
            self.drafts,
            self.editor,
            self.publishing_editor,
            workshop_id,
            owner_id=owner_id,
            package=package,
            preview=self.previews.install(package),
            run=run,
            visibility=visibility,
            display_name=display_name,
        )
        self._prompt_runs[workshop_id] = run
        self._builds[workshop_id] = build
        return build

    def create_hybrid(
        self,
        workshop_id: str,
        *,
        owner_id: str,
        sources: tuple[SourceRecord, ...],
        intent: CreatorIntent,
        profile: str = "book",
        visibility: Visibility = "private",
        display_name: str | None = None,
        semantic_provider: str | None = None,
    ) -> WorkshopBuild:
        source = OneClickAuthoring(self.authoring).run(
            f"workshop_job_{workshop_id}",
            sources,
            profile=profile,
            semantic_provider=semantic_provider,
        )
        run = PromptGenesisProviderService(self.providers).generate(intent, private_source=True)
        source_build = self.authoring.build(source.job_id)
        if source_build is None:
            raise ContractError("hybrid source job has no pipeline build")
        source_claims = tuple(
            claim_from_candidate(candidate) for candidate in source_build.candidates
        )
        hybrid = fuse_hybrid_genesis(source_claims, run.contract)
        draft = hybrid_world_draft(
            source.package.draft,
            hybrid,
            draft_id=f"wd_{workshop_id}",
        )
        package = compile_preview_draft(draft)
        build = finish_hybrid(
            self.drafts,
            self.editor,
            self.publishing_editor,
            workshop_id,
            owner_id=owner_id,
            package=package,
            preview=self.previews.install(package),
            sources=sources,
            run=run,
            hybrid=hybrid,
            visibility=visibility,
            display_name=display_name,
            source_job_id=source.job_id,
        )
        self._prompt_runs[workshop_id] = run
        self._builds[workshop_id] = build
        return build

    def accept_prompt_review(self, workshop_id: str, action: str) -> WorkshopBuild:
        run = self._prompt_runs.get(workshop_id)
        if run is None:
            raise ContractError(f"workshop {workshop_id!r} has no prompt genesis run")
        contract = run.contract.accept(action)
        checkpoint = PromptGenesisCheckpoint(
            run.checkpoint.intent_id,
            run.checkpoint.provider_id,
            run.checkpoint.attempts,
            run.checkpoint.proposal_count,
            run.checkpoint.complete,
        )
        updated = PromptGenesisRun(contract, run.provider_id, run.proposals, checkpoint)
        self._prompt_runs[workshop_id] = updated
        draft = self.drafts.get(workshop_id)
        if contract.review_gate.ready_for_preview and draft.publishing is not None:
            self.publishing_editor.save_profile(
                workshop_id,
                replace(draft.publishing, review_complete=True),
                expected_revision=draft.revision,
            )
        return self._store(
            refresh_build(self.drafts, self.publishing_editor, self.get(workshop_id), updated)
        )

    def evidence_audit(self, workshop_id: str) -> dict[str, object]:
        build = self.get(workshop_id)
        prompt_claims = (
            tuple(claim.completion_id for claim in build.prompt_run.contract.claims)
            if build.prompt_run
            else ()
        )
        hybrid_prompt = (
            tuple(trace.claim_id for trace in build.hybrid.traces if trace.origin == "prompt")
            if build.hybrid
            else ()
        )
        return {
            "workshop_id": workshop_id,
            "mode": build.workshop.mode,
            "prompt_claim_ids": list(prompt_claims),
            "hybrid_prompt_trace_ids": list(hybrid_prompt),
            "all_prompt_claims_e5": (
                all(claim.completion_class == "E5" for claim in build.prompt_run.contract.claims)
                if build.prompt_run
                else True
            ),
            "all_hybrid_prompt_traces_e5": (
                all(
                    trace.evidence_class == "E5"
                    for trace in build.hybrid.traces
                    if trace.origin == "prompt"
                )
                if build.hybrid
                else True
            ),
            "source_refs": list(build.package.source_versions),
            "preview_id": build.preview.preview_id,
        }

    def get(self, workshop_id: str) -> WorkshopBuild:
        build = self._builds.get(workshop_id)
        if build is None:
            raise ContractError(f"workshop build {workshop_id!r} not found")
        return build

    def _store(self, build: WorkshopBuild) -> WorkshopBuild:
        self._builds[build.workshop.workshop_id] = build
        return build


__all__ = ["WorkshopBuild", "WorkshopService"]
