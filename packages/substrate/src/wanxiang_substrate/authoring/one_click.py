"""One-click source family flows and living-instance handoff (M69)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.authoring.orchestrator import AuthoringOrchestrator
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.preview import PreviewInstall, PreviewWorld, instantiate_preview
from wanxiang_substrate.preview.runtime import PreviewRuntimePort
from wanxiang_substrate.sources.model import SourceRecord


@dataclass(frozen=True, slots=True)
class OneClickResult:
    job_id: str
    source_profile: str
    package: WorldPackageDraft
    preview: PreviewInstall


class OneClickAuthoring:
    """Book/family/structured/mixed flows share the same backend pipeline."""

    def __init__(self, service: AuthoringService | None = None) -> None:
        self.service = service or AuthoringService()
        self.orchestrator = AuthoringOrchestrator()

    def run(
        self,
        job_id: str,
        sources: tuple[SourceRecord, ...],
        *,
        profile: str = "mixed",
    ) -> OneClickResult:
        if profile not in ("book", "family", "structured", "mixed"):
            raise ValueError(f"unknown source profile {profile!r}")
        self.service.create_job(job_id, sources=sources, created_by="one-click")
        self.orchestrator.run(self.service, job_id)
        package = self.service.package(job_id)
        if package is None:
            raise ValueError(f"one-click job {job_id!r} did not produce a package")
        preview = self.service.preview(job_id)
        return OneClickResult(job_id, profile, package, preview)

    def enter_living_instance(
        self, result: OneClickResult, runtime: PreviewRuntimePort
    ) -> PreviewWorld:
        return instantiate_preview(runtime, result.package, result.preview)
