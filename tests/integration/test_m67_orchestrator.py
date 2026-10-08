"""M67 DAG, policy, provider routing, stopping, budgets, and resume contracts."""

from __future__ import annotations

import pytest
from wanxiang_substrate.authoring.orchestration_dag import AuthoringDAG
from wanxiang_substrate.authoring.orchestrator import (
    AuthoringBudget,
    AuthoringOrchestrator,
    LoopSignals,
    ProviderRequest,
    StagePolicy,
)
from wanxiang_substrate.authoring.providers import (
    ProviderCapability,
    ProviderRouter,
    ReferenceProvider,
)
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.errors import CapabilityUnavailable
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _record(source_id: str = "m67_source") -> SourceRecord:
    content = "# Chapter\nAlice arrived in Beijing in 1985.\nrule: keep promises\n"
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="fixture", usage="test", approved=True),
        payload=content,
        provenance="synthetic:m67",
        access="public",
    )


def _service(job_id: str = "job_m67") -> AuthoringService:
    service = AuthoringService()
    service.create_job(job_id, sources=(_record(job_id),))
    return service


@pytest.mark.integration
def test_authoring_dag_is_topologically_ordered_and_policies_are_explicit() -> None:
    dag = AuthoringDAG()
    order = dag.order()
    assert order == (
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
    assert dag.dependencies("preview") == ("compile",)
    policy = StagePolicy(
        "distill",
        precondition="parsed",
        postcondition="candidates_checkpointed",
        retry_limit=2,
        timeout_seconds=30,
        cost_units=4,
    )
    AuthoringOrchestrator(policies=(policy,))
    with pytest.raises(ValueError):
        AuthoringOrchestrator(policies=(StagePolicy("missing"),))


@pytest.mark.integration
def test_provider_selection_honors_privacy_determinism_and_cost() -> None:
    provider = ReferenceProvider(
        ProviderCapability(
            "private_vision",
            "vision",
            "1",
            cost_units=2,
            deterministic=True,
            private_safe=True,
        )
    )
    router = ProviderRouter((provider,))
    selected = router.select("vision", private_source=True, max_cost_units=2)
    assert selected.provider_id == "private_vision"
    with pytest.raises(CapabilityUnavailable, match="cost exceeds"):
        router.select("vision", max_cost_units=1)


@pytest.mark.integration
def test_unattended_loop_routes_provider_and_returns_checkpoint() -> None:
    provider = ReferenceProvider(ProviderCapability("offline_vision", "vision", "1"))
    service = _service("job_m67_route")
    run = AuthoringOrchestrator(providers=ProviderRouter((provider,))).run(
        service,
        "job_m67_route",
        budget=AuthoringBudget(max_provider_calls=1),
        provider_requests=(ProviderRequest("vision"),),
    )
    assert run.stopped_reason == ""
    assert run.provider_ids == ("offline_vision",)
    assert run.stages[-1] == "evaluate"
    assert run.checkpoint is not None and run.checkpoint.resume_safe is True


@pytest.mark.integration
def test_stop_and_budget_reasons_are_explicit() -> None:
    service = _service("job_m67_stop")
    stopped = AuthoringOrchestrator().run(
        service,
        "job_m67_stop",
        signals=LoopSignals(rights_ok=False),
    )
    assert stopped.stopped_reason == "rights_blocked"
    assert stopped.next_action == "review_rights"

    budget_service = _service("job_m67_budget")
    budgeted = AuthoringOrchestrator().run(
        budget_service,
        "job_m67_budget",
        budget=AuthoringBudget(max_candidates=0),
    )
    assert budgeted.stopped_reason == "budget:candidates"
    assert budgeted.checkpoint is not None


@pytest.mark.integration
def test_cancelled_or_crashed_job_resumes_from_existing_checkpoint() -> None:
    service = _service("job_m67_resume")
    service.start("job_m67_resume")
    service.cancel("job_m67_resume")
    resumed = AuthoringOrchestrator().resume(service, "job_m67_resume")
    assert resumed.stopped_reason == ""
    assert resumed.snapshot.preview_id is not None
    assert resumed.checkpoint is not None
    assert resumed.checkpoint.next_stage is None
