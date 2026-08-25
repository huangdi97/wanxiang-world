"""Bounded unattended authoring orchestration (M67)."""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_substrate.authoring.model import AuthoringSnapshot
from wanxiang_substrate.authoring.orchestration_dag import (
    AUTHORING_STAGES,
    STAGE_DEPENDENCIES,
    AuthoringDAG,
)
from wanxiang_substrate.authoring.providers import ProviderKind, ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.errors import CapabilityUnavailable


@dataclass(frozen=True, slots=True)
class StagePolicy:
    stage: str
    auto_run: bool = True
    requires_review: bool = False
    budget: int = 100
    precondition: str = "predecessors_complete"
    postcondition: str = "checkpoint_written"
    retry_limit: int = 1
    timeout_seconds: int = 300
    cost_units: int = 1


@dataclass(frozen=True, slots=True)
class AuthoringBudget:
    max_candidates: int = 50000
    max_repair_rounds: int = 7
    max_provider_calls: int = 1000
    max_tokens: int = 0
    max_network_calls: int = 0
    max_storage_bytes: int = 0
    max_time_seconds: int = 0


@dataclass(frozen=True, slots=True)
class BudgetUsage:
    candidates: int = 0
    provider_calls: int = 0
    token_units: int = 0
    network_calls: int = 0
    storage_bytes: int = 0
    time_seconds: int = 0

    def exceeded(self, budget: AuthoringBudget) -> str:
        checks = (
            (self.candidates > budget.max_candidates, "candidates"),
            (self.provider_calls > budget.max_provider_calls, "provider_calls"),
            (budget.max_tokens > 0 and self.token_units > budget.max_tokens, "tokens"),
            (
                budget.max_network_calls > 0 and self.network_calls > budget.max_network_calls,
                "network",
            ),
            (
                budget.max_storage_bytes > 0 and self.storage_bytes > budget.max_storage_bytes,
                "storage",
            ),
            (budget.max_time_seconds > 0 and self.time_seconds > budget.max_time_seconds, "time"),
        )
        for failed, name in checks:
            if failed:
                return f"budget:{name}"
        return ""


@dataclass(frozen=True, slots=True)
class ProviderRequest:
    kind: ProviderKind
    private_source: bool = False
    require_deterministic: bool = True
    max_cost_units: int | None = None


@dataclass(frozen=True, slots=True)
class LoopSignals:
    blocking_gaps: tuple[str, ...] = ()
    rights_ok: bool = True
    worldness: float = 1.0
    uncertainty: float = 0.0


@dataclass(frozen=True, slots=True)
class StopDecision:
    stop: bool
    reason: str
    next_action: str


@dataclass(frozen=True, slots=True)
class StopCriteria:
    min_worldness: float = 0.6
    max_uncertainty: float = 0.8
    require_rights: bool = True

    def decide(self, signals: LoopSignals) -> StopDecision:
        if signals.blocking_gaps:
            return StopDecision(True, "blocking_gap", "complete")
        if self.require_rights and not signals.rights_ok:
            return StopDecision(True, "rights_blocked", "review_rights")
        if signals.worldness < self.min_worldness:
            return StopDecision(True, "worldness_below_threshold", "evaluate")
        if signals.uncertainty > self.max_uncertainty:
            return StopDecision(True, "uncertainty_above_threshold", "complete")
        return StopDecision(False, "", "publish_check")


@dataclass(frozen=True, slots=True)
class OrchestrationCheckpoint:
    job_id: str
    completed_stages: tuple[str, ...]
    next_stage: str | None
    attempt: int
    usage: BudgetUsage
    resume_safe: bool = True


@dataclass(frozen=True, slots=True)
class OrchestrationRun:
    job_id: str
    stages: tuple[str, ...]
    snapshot: AuthoringSnapshot
    stopped_reason: str = ""
    provider_kinds: tuple[str, ...] = ()
    provider_ids: tuple[str, ...] = ()
    usage: BudgetUsage = BudgetUsage()
    checkpoint: OrchestrationCheckpoint | None = None
    next_action: str = "publish_check"


class AuthoringOrchestrator:
    """Runs the reference DAG with explicit budgets, stops, and resume points."""

    def __init__(
        self,
        *,
        policies: tuple[StagePolicy, ...] = (),
        providers: ProviderRouter | None = None,
        dag: AuthoringDAG | None = None,
        stop_criteria: StopCriteria | None = None,
    ) -> None:
        self._policies = {policy.stage: policy for policy in policies}
        self._providers = providers or ProviderRouter()
        self._dag = dag or AuthoringDAG()
        self._stop_criteria = stop_criteria or StopCriteria()
        self._validate_policies()

    def run(
        self,
        service: AuthoringService,
        job_id: str,
        *,
        budget: AuthoringBudget | None = None,
        signals: LoopSignals | None = None,
        provider_requests: tuple[ProviderRequest, ...] = (),
        resume: bool = False,
    ) -> OrchestrationRun:
        active_budget = budget or AuthoringBudget()
        provider_ids: list[str] = []
        try:
            for request in provider_requests:
                capability = self._providers.select(
                    request.kind,
                    private_source=request.private_source,
                    require_deterministic=request.require_deterministic,
                    max_cost_units=request.max_cost_units,
                )
                provider_ids.append(capability.provider_id)
        except CapabilityUnavailable as exc:
            current = service.status(job_id)
            return self._stopped(
                job_id, current, f"provider:{exc}", BudgetUsage(), 0, "configure_provider"
            )
        current = service.status(job_id)
        snapshot = (
            service.resume(job_id)
            if resume or current.status in ("running", "cancelled")
            else service.start(job_id)
        )
        build = service.build(job_id)
        usage = BudgetUsage(
            candidates=len(build.candidates) if build is not None else 0,
            token_units=len(build.candidates) * 32 if build is not None else 0,
            storage_bytes=len(build.candidates) * 128 if build is not None else 0,
        )
        budget_reason = usage.exceeded(active_budget)
        if budget_reason:
            return self._stopped(job_id, snapshot, budget_reason, usage, 3)
        usage = replace(usage, provider_calls=len(provider_requests))
        budget_reason = usage.exceeded(active_budget)
        if budget_reason:
            return self._stopped(job_id, snapshot, budget_reason, usage, 6)
        decision = self._stop_criteria.decide(signals or LoopSignals())
        if decision.stop:
            return self._stopped(job_id, snapshot, decision.reason, usage, 6, decision.next_action)
        service.build_package(job_id)
        service.preview(job_id)
        final = service.status(job_id)
        stages = self._dag.order()
        checkpoint = self._checkpoint(job_id, stages, usage, 1)
        available = tuple(
            kind
            for kind in ("llm", "embedding", "ocr", "asr", "vision")
            if self._providers.capability(kind) is not None  # type: ignore[arg-type]
        )
        return OrchestrationRun(
            job_id,
            stages,
            final,
            provider_kinds=available,
            provider_ids=tuple(provider_ids),
            usage=usage,
            checkpoint=checkpoint,
            next_action=decision.next_action,
        )

    def resume(
        self,
        service: AuthoringService,
        job_id: str,
        *,
        budget: AuthoringBudget | None = None,
    ) -> OrchestrationRun:
        """Resume from the existing AuthoringService/JobService checkpoint."""
        return self.run(service, job_id, budget=budget, resume=True)

    def _stopped(
        self,
        job_id: str,
        snapshot: AuthoringSnapshot,
        reason: str,
        usage: BudgetUsage,
        completed_count: int,
        next_action: str = "review",
    ) -> OrchestrationRun:
        stages = self._dag.order()[:completed_count]
        return OrchestrationRun(
            job_id,
            stages,
            snapshot,
            stopped_reason=reason,
            usage=usage,
            checkpoint=self._checkpoint(job_id, stages, usage, 1),
            next_action=next_action,
        )

    def _checkpoint(
        self, job_id: str, stages: tuple[str, ...], usage: BudgetUsage, attempt: int
    ) -> OrchestrationCheckpoint:
        full = self._dag.order()
        next_stage = full[len(stages)] if len(stages) < len(full) else None
        return OrchestrationCheckpoint(job_id, stages, next_stage, attempt, usage)

    def _validate_policies(self) -> None:
        valid = set(self._dag.order())
        for policy in self._policies.values():
            if policy.stage not in valid:
                raise ValueError(f"policy references unknown stage {policy.stage!r}")
            if (
                min(policy.budget, policy.retry_limit, policy.timeout_seconds, policy.cost_units)
                < 0
            ):
                raise ValueError(f"stage policy for {policy.stage!r} has a negative limit")


__all__ = [
    "AUTHORING_STAGES",
    "STAGE_DEPENDENCIES",
    "AuthoringBudget",
    "AuthoringDAG",
    "AuthoringOrchestrator",
    "BudgetUsage",
    "LoopSignals",
    "OrchestrationCheckpoint",
    "OrchestrationRun",
    "ProviderRequest",
    "StagePolicy",
    "StopCriteria",
    "StopDecision",
]
