"""Authoring job facade shared by Studio/API/CLI (M58-M70)."""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_domain.errors import ContractError, WanxiangError

from wanxiang_substrate.authoring.model import AuthoringSnapshot, PipelineBuild
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.review_inbox import InboxItem, ReviewAudit, ReviewInbox
from wanxiang_substrate.authoring.service_living import LivingWorldMixin
from wanxiang_substrate.authoring.service_package import PackageServiceMixin
from wanxiang_substrate.authoring.service_status import StatusMixin
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.jobs.errors import InvalidJobTransition, JobNotFound
from wanxiang_substrate.jobs.service import JobService
from wanxiang_substrate.jobs.store import JobStore
from wanxiang_substrate.preview import PreviewRegistry
from wanxiang_substrate.review.decisions import ReviewDecision, ReviewLedger
from wanxiang_substrate.sources.model import SourceRecord
from wanxiang_substrate.sources.registry import SourceRegistry


class AuthoringService(PackageServiceMixin, LivingWorldMixin, StatusMixin):
    """One in-memory Forge service; canonical world state is outside this class."""

    def __init__(
        self,
        pipeline: SourceToDraftPipeline | None = None,
        *,
        providers: ProviderRouter | None = None,
        blob_loader: Callable[[SourceRecord], bytes | None] | None = None,
    ) -> None:
        self._jobs = JobService(JobStore())
        self._sources = SourceRegistry()
        self._providers = providers or ProviderRouter()
        self._source_blobs: dict[str, bytes] = {}
        self._pipeline = pipeline or SourceToDraftPipeline(
            blob_loader=blob_loader or self._load_source_blob,
            providers=self._providers,
        )
        self._job_sources: dict[str, tuple[str, ...]] = {}
        self._job_semantic: dict[str, bool] = {}
        self._progress: dict[str, tuple[tuple[str, str], ...]] = {}
        self._product_states: dict[str, str] = {}
        self._builds: dict[str, PipelineBuild] = {}
        self._packages: dict[str, WorldPackageDraft] = {}
        self._previews = PreviewRegistry()
        self._living_worlds: dict[str, object] = {}
        self._living_records: dict[str, object] = {}
        self._worldness_runs: dict[str, object] = {}
        self._reviews = ReviewLedger()
        self._inbox = ReviewInbox(self._reviews)

    def create_job(
        self,
        job_id: str,
        *,
        version: str = "1",
        sources: tuple[SourceRecord, ...] = (),
        created_by: str = "studio",
        semantic_provider: str | None = None,
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
            if self._job_semantic.get(job_id, False) != (semantic_provider is not None):
                raise ContractError(
                    f"job {job_id!r} already exists with a different semantic provider selection"
                )
            return self.status(job_id)
        source_ids = self._register_sources(sources)
        job_source_refs = source_ids or (f"job_{job_id}",)
        self._jobs.create(job_id, "authoring", job_source_refs, version, created_by)
        self._job_sources.setdefault(job_id, source_ids)
        self._job_semantic[job_id] = semantic_provider is not None
        self._product_states[job_id] = "CREATED"
        return self.status(job_id)

    @property
    def providers(self) -> ProviderRouter:
        return self._providers

    def add_source(self, job_id: str, record: SourceRecord) -> AuthoringSnapshot:
        job = self._jobs.status(job_id)
        if job.status not in ("created", "cancelled"):
            raise InvalidJobTransition("sources can only be added before authoring starts")
        self._sources.register(record)
        current = self._job_sources.get(job_id, ())
        if record.source_id not in current:
            self._job_sources[job_id] = (*current, record.source_id)
        return self.status(job_id)

    def attach_source_blob(self, source_id: str, blob: bytes) -> None:
        """Attach private raw bytes for the existing generic blob-loader port."""
        current = self._source_blobs.get(source_id)
        if current is not None and current != blob:
            raise ContractError(f"source blob {source_id!r} cannot be replaced")
        self._source_blobs[source_id] = bytes(blob)

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
            build = self._pipeline.run(
                records,
                draft_id=f"wd_{job_id}",
                use_semantic_provider=self._job_semantic.get(job_id, False),
            )
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
            self._progress[job_id] = tuple(sorted(build.distillation.checkpoint().items()))
            self._product_states[job_id] = self._product_state_for_build(build)
            return self.status(job_id)
        except Exception as exc:
            current = self._jobs.status(job_id)
            details = dict(exc.details) if isinstance(exc, WanxiangError) else {}
            details.setdefault("error", f"{type(exc).__name__}:{exc}")
            if isinstance(exc, WanxiangError):
                details.setdefault("product_state", getattr(exc, "product_state", "FAILED"))
            self._progress[job_id] = tuple(sorted((str(k), str(v)) for k, v in details.items()))
            self._product_states[job_id] = details.get("product_state", "FAILED")
            if current.status == "running":
                checkpoint_stage = "distilled" if "batches" in details else current.stage
                self._jobs.checkpoint(job_id, checkpoint_stage, details)
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

    def review_inbox(self, job_id: str) -> tuple[InboxItem, ...]:
        """Return impact-ranked review items over the shared candidate build."""
        build = self._require_build(job_id)
        return self._inbox.build(build.candidates)

    def review_inbox_batch(
        self,
        job_id: str,
        candidate_ids: tuple[str, ...],
        *,
        action: str,
        reviewer: str,
        rationale: str,
    ) -> tuple[ReviewDecision, ...]:
        build = self._require_build(job_id)
        unknown = set(candidate_ids).difference(build.candidate_ids)
        if unknown:
            raise ContractError(f"candidate ids are not part of job {job_id!r}: {sorted(unknown)}")
        return self._inbox.batch(
            candidate_ids,
            action=action,
            reviewer=reviewer,
            rationale=rationale,
        )

    def review_audit(self, job_id: str) -> tuple[ReviewAudit, ...]:
        self._require_build(job_id)
        return self._inbox.audit()

    def package(self, job_id: str) -> WorldPackageDraft | None:
        return self._packages.get(job_id)

    def build(self, job_id: str) -> PipelineBuild | None:
        return self._builds.get(job_id)

    def _register_sources(self, records: tuple[SourceRecord, ...]) -> tuple[str, ...]:
        ids: list[str] = []
        for record in records:
            self._sources.register(record)
            ids.append(record.source_id)
        return tuple(ids)

    def _load_source_blob(self, record: SourceRecord) -> bytes | None:
        return self._source_blobs.get(record.source_id)

    def _require_build(self, job_id: str) -> PipelineBuild:
        build = self._builds.get(job_id)
        if build is None:
            self.start(job_id)
            build = self._builds.get(job_id)
        if build is None:
            raise ContractError(f"authoring job {job_id!r} has no draft")
        return build
