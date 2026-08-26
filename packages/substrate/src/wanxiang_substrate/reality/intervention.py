"""Branch-isolated experiment interventions (M88 / G91E)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import WorldInstanceId

from wanxiang_substrate.authoring.living_ports import LivingRuntimePort
from wanxiang_substrate.reality.errors import ExperimentError

InterventionKind = Literal[
    "pressure", "opportunity", "director", "environment", "actor", "reversal"
]
TriggerKind = Literal["time", "event"]


@dataclass(frozen=True, slots=True)
class InterventionTrigger:
    """An explicit time or committed-event trigger, never an implicit hook."""

    kind: TriggerKind
    value: int | str

    def __post_init__(self) -> None:
        if self.kind == "time":
            if isinstance(self.value, bool) or not isinstance(self.value, int) or self.value < 0:
                raise ExperimentError("time trigger must use a non-negative tick")
        elif self.kind == "event":
            if not isinstance(self.value, str) or not self.value:
                raise ExperimentError("event trigger must use a non-empty event ref")
        else:
            raise ExperimentError(f"unsupported intervention trigger {self.kind!r}")

    @classmethod
    def at_time(cls, at_ticks: int) -> InterventionTrigger:
        return cls("time", at_ticks)

    @classmethod
    def on_event(cls, event_ref: str) -> InterventionTrigger:
        return cls("event", event_ref)

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind, "value": self.value}


@dataclass(frozen=True, slots=True)
class Intervention:
    """A reversible, artifact-linked proposal to apply on an experiment branch."""

    intervention_id: str
    kind: InterventionKind
    trigger: InterventionTrigger
    parent_branch_ref: str
    artifact_ref: str
    payload: tuple[tuple[str, str], ...] = ()
    reversible: bool = True
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.intervention_id or not self.parent_branch_ref or not self.artifact_ref:
            raise ExperimentError("intervention requires id, parent branch and artifact refs")
        if self.kind not in {
            "pressure",
            "opportunity",
            "director",
            "environment",
            "actor",
            "reversal",
        }:
            raise ExperimentError(f"unsupported intervention kind {self.kind!r}")
        if self.schema_version != 1:
            raise ExperimentError("unsupported intervention schema")
        if any(not key or not value for key, value in self.payload):
            raise ExperimentError("intervention payload keys and values must be non-empty")

    @property
    def payload_dict(self) -> dict[str, str]:
        return dict(self.payload)

    def reversal(self) -> Intervention:
        if not self.reversible:
            raise ExperimentError("irreversible intervention cannot produce a reversal proposal")
        return replace(
            self,
            intervention_id=f"{self.intervention_id}:reversal",
            kind="reversal",
            payload=(
                *self.payload,
                ("reverses", self.intervention_id),
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "intervention_id": self.intervention_id,
            "kind": self.kind,
            "trigger": self.trigger.to_dict(),
            "parent_branch_ref": self.parent_branch_ref,
            "artifact_ref": self.artifact_ref,
            "payload": dict(self.payload),
            "reversible": self.reversible,
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True, slots=True)
class ExperimentSetup:
    """Immutable setup carried into a later WorldRunArtifact."""

    setup_id: str
    baseline_instance_ref: str
    baseline_branch_ref: str
    artifact_ref: str
    interventions: tuple[Intervention, ...] = ()
    reversible: bool = True
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.setup_id or not self.baseline_instance_ref or not self.baseline_branch_ref:
            raise ExperimentError("experiment setup requires baseline refs")
        if not self.artifact_ref or self.schema_version != 1:
            raise ExperimentError("experiment setup requires v1 artifact ref")
        ids = [intervention.intervention_id for intervention in self.interventions]
        if len(ids) != len(set(ids)):
            raise ExperimentError("experiment intervention ids must be unique")
        if not self.reversible and any(
            intervention.reversible for intervention in self.interventions
        ):
            raise ExperimentError(
                "irreversible setup cannot contain reversible intervention metadata"
            )

    def add(self, intervention: Intervention) -> ExperimentSetup:
        if intervention.parent_branch_ref != self.baseline_branch_ref:
            raise ExperimentError("intervention parent does not match experiment baseline")
        return replace(self, interventions=(*self.interventions, intervention))

    def to_dict(self) -> dict[str, object]:
        return {
            "setup_id": self.setup_id,
            "baseline_instance_ref": self.baseline_instance_ref,
            "baseline_branch_ref": self.baseline_branch_ref,
            "artifact_ref": self.artifact_ref,
            "interventions": [item.to_dict() for item in self.interventions],
            "reversible": self.reversible,
            "schema_version": self.schema_version,
        }


@dataclass(frozen=True, slots=True)
class InterventionBranch:
    """Evidence ref for the child branch; parent history remains untouched."""

    instance_ref: str
    parent_branch_ref: str
    branch_ref: str
    fork_revision: int
    intervention_id: str
    artifact_ref: str
    isolated: bool = True


class ExperimentInterventionRunner:
    """Uses the existing runtime branch authority for isolated setup only."""

    def fork(
        self,
        runtime: LivingRuntimePort,
        instance_id: WorldInstanceId,
        parent_branch_id: BranchId,
        setup: ExperimentSetup,
        intervention: Intervention,
    ) -> InterventionBranch:
        if setup.baseline_instance_ref != instance_id.value:
            raise ExperimentError("experiment setup instance does not match runtime instance")
        if setup.baseline_branch_ref != parent_branch_id.value:
            raise ExperimentError("experiment setup branch does not match runtime parent")
        if intervention not in setup.interventions:
            raise ExperimentError("intervention is not present in experiment setup")
        parent_state = runtime.current_state(instance_id, parent_branch_id)
        child = runtime.create_branch(instance_id, parent_branch_id)
        child_branch = getattr(child, "branch_id", None)
        if not isinstance(child_branch, BranchId):
            raise ExperimentError("runtime did not return a branch id")
        revision = getattr(getattr(parent_state, "revision", None), "value", None)
        if not isinstance(revision, int):
            raise ExperimentError("runtime parent state did not expose a revision")
        return InterventionBranch(
            instance_ref=instance_id.value,
            parent_branch_ref=parent_branch_id.value,
            branch_ref=child_branch.value,
            fork_revision=revision,
            intervention_id=intervention.intervention_id,
            artifact_ref=intervention.artifact_ref,
        )
