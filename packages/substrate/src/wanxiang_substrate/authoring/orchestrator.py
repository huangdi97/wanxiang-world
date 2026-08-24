"""Bounded unattended authoring orchestration (M67)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.authoring.model import AuthoringSnapshot
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService

AUTHORING_STAGES = (
    "ingest",
    "parse",
    "distill",
    "fuse",
    "domain",
    "complete",
    "scenario",
    "compile",
    "preview",
    "evaluate",
)


@dataclass(frozen=True, slots=True)
class StagePolicy:
    stage: str
    auto_run: bool = True
    requires_review: bool = False
    budget: int = 100


@dataclass(frozen=True, slots=True)
class AuthoringBudget:
    max_candidates: int = 10000
    max_repair_rounds: int = 7
    max_provider_calls: int = 0


@dataclass(frozen=True, slots=True)
class OrchestrationRun:
    job_id: str
    stages: tuple[str, ...]
    snapshot: AuthoringSnapshot
    stopped_reason: str = ""
    provider_kinds: tuple[str, ...] = ()


class AuthoringOrchestrator:
    """Runs the reference DAG with explicit budgets and stop criteria."""

    def __init__(
        self,
        *,
        policies: tuple[StagePolicy, ...] = (),
        providers: ProviderRouter | None = None,
    ) -> None:
        self._policies = {policy.stage: policy for policy in policies}
        self._providers = providers or ProviderRouter()

    def run(
        self,
        service: AuthoringService,
        job_id: str,
        *,
        budget: AuthoringBudget | None = None,
    ) -> OrchestrationRun:
        active_budget = budget or AuthoringBudget()
        snapshot = service.start(job_id)
        build = service.build(job_id)
        if build is not None and len(build.candidates) > active_budget.max_candidates:
            return OrchestrationRun(
                job_id, ("ingest", "parse", "distill"), snapshot, "candidate budget exceeded"
            )
        service.build_package(job_id)
        service.preview(job_id)
        final = service.status(job_id)
        provider_kinds = tuple(
            kind
            for kind in ("llm", "embedding", "ocr", "asr", "vision")
            if self._providers.capability(kind) is not None  # type: ignore[arg-type]
        )
        return OrchestrationRun(
            job_id,
            AUTHORING_STAGES,
            final,
            provider_kinds=provider_kinds,
        )
