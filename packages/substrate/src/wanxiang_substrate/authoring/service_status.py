"""Status snapshot mixin for AuthoringService."""

from __future__ import annotations

from typing import Any

from wanxiang_substrate.authoring.model import AuthoringSnapshot, PipelineBuild


class StatusMixin:
    def status(self: Any, job_id: str) -> AuthoringSnapshot:
        job = self._jobs.status(job_id)
        build = self._builds.get(job_id)
        package = self._packages.get(job_id)
        preview = self._previews.for_package(package.package_id) if package else None
        checkpoint = dict(self._progress.get(job_id, ()))
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
            product_state=self._product_states.get(
                job_id, self._product_state_for_build(build) if build else "CREATED"
            ),
            checkpoint=tuple(sorted(checkpoint.items())),
            parsed_nodes=(
                int(build.draft.compiler_metadata.get("parsed_nodes", "0"))
                if build
                else int(checkpoint.get("parsed_nodes", "0"))
            ),
            segment_count=(
                build.distillation.segment_count if build else int(checkpoint.get("segments", "0"))
            ),
            batch_count=(
                build.distillation.batch_count if build else int(checkpoint.get("batches", "0"))
            ),
            provider_id=(
                build.distillation.provider_id if build else checkpoint.get("provider_id", "")
            ),
            stage_errors=(
                build.distillation.stage_errors
                if build
                else tuple(item for item in checkpoint.get("stage_errors", "").split("|") if item)
            ),
        )

    @staticmethod
    def _product_state_for_build(build: PipelineBuild) -> str:
        if build.draft.unresolved_rights:
            return "RIGHTS_ACTION_REQUIRED"
        if build.draft.coverage <= 0.0:
            return "ZERO_COVERAGE"
        if build.draft.status != "READY_TO_COMPILE":
            return "REVIEW_REQUIRED"
        return "READY"
