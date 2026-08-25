"""Package/preview lifecycle mixin for AuthoringService."""

from __future__ import annotations

from typing import Any

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.compile import (
    CompilerBoundary,
    CompilerInput,
    PackageAssembler,
    PackageValidationResult,
    PackageValidator,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.jobs.errors import InvalidJobTransition
from wanxiang_substrate.jobs.model import JOB_STAGES
from wanxiang_substrate.preview import PreviewInstall


class PackageServiceMixin:
    def build_package(self: Any, job_id: str, *, for_preview: bool = True) -> WorldPackageDraft:
        build = self._require_build(job_id)
        draft = build.draft
        domain_versions = tuple((domain_id, "1.0.0") for domain_id in draft.selected_domains)
        outcome = CompilerBoundary().check(
            CompilerInput(
                draft=draft,
                draft_revision=draft.revision,
                source_versions=draft.source_versions,
                domain_versions=domain_versions,
            )
        )
        if not outcome.ok:
            raise ContractError(
                "; ".join(outcome.reasons),
                details={
                    "product_state": "RIGHTS_ACTION_REQUIRED"
                    if any("rights" in reason for reason in outcome.reasons)
                    else "ZERO_COVERAGE"
                },
            )
        package = PackageAssembler().assemble(
            draft,
            compile_outcome=outcome,
            domain_versions=domain_versions,
            evidence_coverage=draft.coverage,
            for_preview=for_preview,
        )
        self._packages[job_id] = package
        current = self._jobs.status(job_id)
        if JOB_STAGES.index(current.stage) <= JOB_STAGES.index("compiled"):
            self._jobs.checkpoint(job_id, "compiled", {"package_id": package.package_id})
        return package

    def package_validation(self: Any, job_id: str) -> PackageValidationResult:
        package = self._packages.get(job_id) or self.build_package(job_id)
        return PackageValidator().validate(package)

    def publish(self: Any, job_id: str) -> PackageValidationResult:
        current = self._jobs.status(job_id)
        if current.status == "done" and current.stage == "published":
            return self.package_validation(job_id)
        package = self.build_package(job_id, for_preview=False)
        validation = PackageValidator().validate(package)
        if not validation.publish_ok:
            raise ContractError(
                f"package {package.package_id!r} is not publishable: "
                + "; ".join(validation.reasons)
            )
        if self._jobs.status(job_id).status != "running":
            raise InvalidJobTransition(f"cannot publish job {job_id!r} in its current state")
        self._jobs.checkpoint(job_id, "published", {"package_id": package.package_id})
        self._jobs.finish(job_id)
        return validation

    def preview(self: Any, job_id: str) -> PreviewInstall:
        package = self._packages.get(job_id) or self.build_package(job_id)
        install = self._previews.install(package)
        self._jobs.checkpoint(job_id, "previewed", {"preview_id": install.preview_id})
        return install
