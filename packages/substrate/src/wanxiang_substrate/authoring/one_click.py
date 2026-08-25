"""One-click source family flows and living-instance handoff (M69)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.authoring.orchestrator import (
    AuthoringOrchestrator,
    OrchestrationRun,
    ProviderRequest,
)
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.compile import PackageValidationResult
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.preview import PreviewInstall, PreviewWorld, instantiate_preview
from wanxiang_substrate.preview.runtime import PreviewRuntimePort
from wanxiang_substrate.sources.model import SourceRecord

SOURCE_PROFILES = ("book", "family", "structured", "mixed")


@dataclass(frozen=True, slots=True)
class OneClickResult:
    job_id: str
    source_profile: str
    package: WorldPackageDraft
    preview: PreviewInstall
    orchestration: OrchestrationRun | None = None


class OneClickAuthoring:
    """Book/family/structured/mixed flows share the same backend pipeline."""

    def __init__(self, service: AuthoringService | None = None) -> None:
        self.service = service or AuthoringService()
        self.orchestrator = AuthoringOrchestrator(providers=self.service.providers)

    def run(
        self,
        job_id: str,
        sources: tuple[SourceRecord, ...],
        *,
        profile: str = "mixed",
        semantic_provider: str | None = None,
    ) -> OneClickResult:
        if profile not in SOURCE_PROFILES:
            raise ValueError(f"unknown source profile {profile!r}")
        self._validate_profile(profile, sources)
        self.service.create_job(
            job_id,
            sources=sources,
            created_by="one-click",
            semantic_provider=semantic_provider,
        )
        requests = (
            (
                ProviderRequest(
                    "semantic", private_source=any(source.access != "public" for source in sources)
                ),
            )
            if semantic_provider is not None
            and self.service.providers.capability("semantic") is not None
            else ()
        )
        orchestration = self.orchestrator.run(
            self.service,
            job_id,
            provider_requests=requests,
        )
        if orchestration.stopped_reason:
            raise ContractError(
                f"one-click authoring stopped for {job_id!r}: {orchestration.stopped_reason}"
            )
        package = self.service.package(job_id)
        if package is None:
            raise ContractError(f"one-click job {job_id!r} did not produce a package")
        preview = self.service.preview(job_id)
        return OneClickResult(job_id, profile, package, preview, orchestration)

    def enter_living_instance(
        self, result: OneClickResult, runtime: PreviewRuntimePort
    ) -> PreviewWorld:
        return instantiate_preview(runtime, result.package, result.preview)

    def publish(self, result: OneClickResult) -> PackageValidationResult:
        return self.service.publish(result.job_id)

    @staticmethod
    def _validate_profile(profile: str, sources: tuple[SourceRecord, ...]) -> None:
        if not sources:
            raise ValueError("one-click authoring requires at least one source")
        kinds = {source.kind for source in sources}
        requirements = {
            "book": {"text", "markdown", "epub", "docx", "pdf"},
            "family": {"gedcom"},
            "structured": {"json", "csv", "yaml"},
        }
        if profile in requirements and not kinds.intersection(requirements[profile]):
            expected = ", ".join(sorted(requirements[profile]))
            raise ValueError(f"profile {profile!r} requires one of: {expected}")
        if profile == "mixed" and len(sources) < 2:
            raise ValueError("mixed profile requires at least two source records")
