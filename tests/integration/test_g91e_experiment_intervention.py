"""G91E: explicit intervention setup and real branch isolation."""

from __future__ import annotations

from typing import cast

from scripts.reference_runtime import build_reference_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.living_ports import LivingRuntimePort
from wanxiang_substrate.reality.intervention import (
    ExperimentInterventionRunner,
    ExperimentSetup,
    Intervention,
    InterventionTrigger,
)


def _setup(instance_id: str, branch_id: str) -> tuple[ExperimentSetup, Intervention]:
    intervention = Intervention(
        intervention_id="int_pressure_1",
        kind="pressure",
        trigger=InterventionTrigger.at_time(10),
        parent_branch_ref=branch_id,
        artifact_ref="run-artifact:exp-1",
        payload=(("profile_ref", "pressure:market:v1"),),
    )
    setup = ExperimentSetup(
        setup_id="setup_exp_1",
        baseline_instance_ref=instance_id,
        baseline_branch_ref=branch_id,
        artifact_ref="run-artifact:exp-1",
    ).add(intervention)
    return setup, intervention


def test_time_and_event_triggers_and_reversible_setup_are_explicit() -> None:
    at_time = InterventionTrigger.at_time(10)
    on_event = InterventionTrigger.on_event("event:market_open")
    assert at_time.to_dict() == {"kind": "time", "value": 10}
    assert on_event.to_dict()["kind"] == "event"
    setup, intervention = _setup("wld_g91e", "br_parent")
    records = cast(list[dict[str, object]], setup.to_dict()["interventions"])
    assert records[0]["artifact_ref"] == "run-artifact:exp-1"
    reversal = intervention.reversal()
    assert reversal.kind == "reversal"
    assert reversal.payload_dict["reverses"] == intervention.intervention_id


def test_intervention_forks_existing_runtime_without_parent_history_write() -> None:
    runtime = build_reference_runtime()
    created = runtime.create_world(instance_id=WorldInstanceId("wld_g91e"))
    setup, intervention = _setup(created.instance_id.value, created.root_branch_id.value)
    before_hash = runtime.current_state(created.instance_id, created.root_branch_id).semantic_hash()
    before_events = runtime.events(created.instance_id, created.root_branch_id)
    result = ExperimentInterventionRunner().fork(
        cast(LivingRuntimePort, runtime),
        created.instance_id,
        created.root_branch_id,
        setup,
        intervention,
    )
    assert result.isolated is True
    assert result.parent_branch_ref == created.root_branch_id.value
    assert result.branch_ref != created.root_branch_id.value
    assert result.fork_revision == 0
    assert runtime.events(created.instance_id, created.root_branch_id) == before_events
    assert (
        runtime.current_state(created.instance_id, created.root_branch_id).semantic_hash()
        == before_hash
    )
    assert isinstance(BranchId(result.branch_ref), BranchId)
