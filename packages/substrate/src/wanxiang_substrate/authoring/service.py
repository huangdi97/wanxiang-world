"""Authoring job facade shared by Studio/API/CLI (M58-M70)."""

from __future__ import annotations

from wanxiang_domain.errors import ContractError, WanxiangError

from wanxiang_substrate.authoring.model import AuthoringSnapshot, PipelineBuild
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.compile import CompilerBoundary, CompilerInput, PackageAssembler
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.jobs.errors import InvalidJobTransition, JobNotFound
from wanxiang_substrate.jobs.service import JobService
from wanxiang_substrate.jobs.store import JobStore
from wanxiang_substrate.preview import PreviewInstall, PreviewRegistry
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.sources.registry import SourceRegistry


class AuthoringService:
    """One in-memory Forge service; canonical world state is outside this class."""

    def __init__(self, pipeline: SourceToDraftPipeline | None = None) -> None:
        self._jobs = JobService(JobStore())
        self._sources = SourceRegistry()
        self._pipeline = pipeline or SourceToDraftPipeline()
        self._job_sources: dict[str, tuple[str, ...]] = {}
        self._builds: dict[str, PipelineBuild] = {}
        self._packages: dict[str, WorldPackageDraft] = {}
        self._previews = PreviewRegistry()
        self._reviews = ReviewLedger()

    def create_job(
        self,
        job_id: str,
        *,
        version: str = "1",
        sources: tuple[SourceRecord, ...] = (),
        created_by: str = "studio",
    ) -> AuthoringSnapshot:
        try:
            existing = self._jobs.status(job_id)
        except JobNotFound:
            existing = None
        if existing is not None:
            current_fingerprint = tuple(
                sorted(
                    (
                        record.source_id,
                        record.kind,
                        record.content_hash,
                        record.version,
                    )
                    for source_id in self._job_sources.get(job_id, ())
                    for record in (self._sources.require(source_id),)
                )
            )
            incoming_fingerprint = tuple(
                sorted(
                    (record.source_id, record.kind, record.content_hash, record.version)
                    for record in sources
                )
            )
            if current_fingerprint != incoming_fingerprint or existing.job_id != job_id:
                raise ContractError(
                    f"job {job_id!r} already exists with a different source fingerprint; "
                    "use a new job id or source version"
                )
            return self.status(job_id)
        source_ids = self._register_sources(sources)
        job_source_refs = source_ids or (f"job_{job_id}",)
        self._jobs.create(job_id, "authoring", job_source_refs, version, created_by)
        self._job_sources.setdefault(job_id, source_ids)
        return self.status(job_id)

    def add_source(self, job_id: str, record: SourceRecord) -> AuthoringSnapshot:
        job = self._jobs.status(job_id)
        if job.status not in ("created", "cancelled"):
            raise InvalidJobTransition("sources can only be added before authoring starts")
        self._sources.register(record)
        current = self._job_sources.get(job_id, ())
        if record.source_id not in current:
            self._job_sources[job_id] = (*current, record.source_id)
        return self.status(job_id)

    def start(self, job_id: str) -> AuthoringSnapshot:
        job = self._jobs.status(job_id)
        if job.status == "done":
            return self.status(job_id)
        if job.status == "created":
            self._jobs.start(job_id)
        if job.status == "cancelled":
            self._jobs.resume(job_id)
        if job_id in self._builds:
            return self.status(job_id)
        records = tuple(
            self._sources.require(source_id) for source_id in self._job_sources.get(job_id, ())
        )
        try:
            build = self._pipeline.run(records, draft_id=f"wd_{job_id}")
            self._builds[job_id] = build
            for stage, payload in (
                ("registered", {"sources": str(len(records))}),
                ("parsed", {"sources": str(len(records))}),
                ("segmented", {"segments": str(len(build.segments))}),
                ("distilled", {"candidates": str(len(build.candidates))}),
                ("fused", {"conflicts": str(len(build.conflicts))}),
                ("reviewed", {"pending": str(len(build.candidates))}),
                ("drafted", {"draft_id": build.draft.draft_id}),
            ):
                self._jobs.checkpoint(job_id, stage, payload)
            return self.status(job_id)
        except Exception as exc:
            current = self._jobs.status(job_id)
            if current.status == "running":
                self._jobs.fail(job_id, f"{type(exc).__name__}:{exc}")
            if isinstance(exc, WanxiangError):
                raise
            raise ContractError(str(exc)) from exc

    def resume(self, job_id: str) -> AuthoringSnapshot:
        job, _checkpoint = self._jobs.resume(job_id)
        if job.status in ("done", "failed"):
            return self.status(job_id)
        return self.start(job_id)

    def cancel(self, job_id: str) -> AuthoringSnapshot:
        self._jobs.cancel(job_id)
        return self.status(job_id)

    def review_candidate(
        self,
        job_id: str,
        candidate_id: str,
        *,
        action: str,
        reviewer: str,
        rationale: str,
    ) -> ReviewDecision:
        build = self._require_build(job_id)
        if candidate_id not in build.candidate_ids:
            raise ContractError(f"candidate {candidate_id!r} is not part of job {job_id!r}")
        decision = ReviewDecision(
            decision_id=f"rev_{candidate_id}_{len(self._reviews.history(candidate_id)) + 1}",
            target_id=candidate_id,
            action=action,  # type: ignore[arg-type]
            reviewer=reviewer,
            rationale=rationale,
        )
        return self._reviews.record(decision)

    def build_package(self, job_id: str) -> WorldPackageDraft:
        build = self._require_build(job_id)
        draft = build.draft
        source_versions = draft.source_versions
        domain_versions = tuple((domain_id, "1.0.0") for domain_id in draft.selected_domains)
        outcome = CompilerBoundary().check(
            CompilerInput(
                draft=draft,
                draft_revision=draft.revision,
                source_versions=source_versions,
                domain_versions=domain_versions,
            )
        )
        if not outcome.ok:
            raise ContractError("; ".join(outcome.reasons))
        package = PackageAssembler().assemble(
            draft,
            compile_outcome=outcome,
            domain_versions=domain_versions,
            evidence_coverage=draft.coverage,
            for_preview=True,
        )
        self._packages[job_id] = package
        self._jobs.checkpoint(job_id, "compiled", {"package_id": package.package_id})
        return package

    def preview(self, job_id: str) -> PreviewInstall:
        package = self._packages.get(job_id) or self.build_package(job_id)
        install = self._previews.install(package)
        self._jobs.checkpoint(job_id, "previewed", {"preview_id": install.preview_id})
        return install

    def package(self, job_id: str) -> WorldPackageDraft | None:
        return self._packages.get(job_id)

    def build(self, job_id: str) -> PipelineBuild | None:
        return self._builds.get(job_id)

    def status(self, job_id: str) -> AuthoringSnapshot:
        job = self._jobs.status(job_id)
        build = self._builds.get(job_id)
        package = self._packages.get(job_id)
        preview = self._previews.for_package(package.package_id) if package else None
        return AuthoringSnapshot(
            job_id=job.job_id,
            status=job.status,
            stage=job.stage,
            source_ids=self._job_sources.get(job_id, ()),
            draft_id=build.draft.draft_id if build else None,
            package_id=package.package_id if package else None,
            preview_id=preview.preview_id if preview else None,
            candidate_count=len(build.candidates) if build else 0,
            conflict_count=len(build.conflicts) if build else 0,
            error=job.error,
            diagnostics=build.diagnostics if build else (),
        )

    def _register_sources(self, records: tuple[SourceRecord, ...]) -> tuple[str, ...]:
        ids: list[str] = []
        for record in records:
            self._sources.register(record)
            ids.append(record.source_id)
        return tuple(ids)

    def _require_build(self, job_id: str) -> PipelineBuild:
        build = self._builds.get(job_id)
        if build is None:
            self.start(job_id)
            build = self._builds.get(job_id)
        if build is None:
            raise ContractError(f"authoring job {job_id!r} has no draft")
        return build
