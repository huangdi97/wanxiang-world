"""SkillRuntime: deterministic step expansion executed through Commit Authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.skills.errors import InvalidSkillStep, SkillPrerequisiteError
from wanxiang_substrate.skills.model import SkillDefinition, SkillInstance, SkillStep
from wanxiang_substrate.skills.registry import SkillRegistry


class SkillRuntime:
    """Executes a skill step-by-step; every step command goes through the
    authoritative runtime (validate -> resolve -> commit)."""

    def __init__(
        self,
        runtime: WorldRuntime,
        registry: SkillRegistry,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        actor_field: str = "actor_id",
    ) -> None:
        self._runtime = runtime
        self._registry = registry
        self._instance_id = instance_id
        self._branch_id = branch_id
        self._actor_field = actor_field

    def execute(
        self,
        skill_instance_id: EntityId,
        skill_id: EntityId,
        actor_id: EntityId,
        *,
        skill_version: int = 1,
    ) -> list[str]:
        definition = self._registry.get(skill_id, skill_version)
        if definition is None:
            raise SkillPrerequisiteError(f"skill {skill_id.value} v{skill_version} not found")
        self._check_permission(actor_id, definition)
        self._start(skill_instance_id, skill_id, actor_id)
        completed: list[str] = []
        instance = self._load_instance(skill_instance_id, skill_id, actor_id)
        while True:
            step = instance.next_step(definition)
            if step is None:
                self._set_state(
                    skill_instance_id,
                    actor_id,
                    "completed",
                    len(definition.steps),
                    ",".join(completed),
                )
                return completed
            self._advance(skill_instance_id, actor_id, step, instance, completed)
            instance = self._load_instance(skill_instance_id, skill_id, actor_id)
            completed = list(instance.completed_steps)

    def pause(self, skill_instance_id: EntityId, actor_id: EntityId) -> None:
        self._set_state(skill_instance_id, actor_id, "paused", 0, "")

    def resume(self, skill_instance_id: EntityId, skill_id: EntityId, actor_id: EntityId) -> None:
        instance = self._load_instance(skill_instance_id, skill_id, actor_id)
        self._set_state(
            skill_instance_id,
            actor_id,
            "running",
            instance.current_step_index,
            ",".join(instance.completed_steps),
        )

    def cancel(self, skill_instance_id: EntityId, actor_id: EntityId) -> None:
        self._set_state(skill_instance_id, actor_id, "cancelled", 0, "")

    # -- internals ----------------------------------------------------------

    def _check_permission(self, actor_id: EntityId, definition: SkillDefinition) -> None:
        if definition.required_permission is None:
            return
        from wanxiang_substrate.institution.query import InstitutionQuery

        state = self._runtime.current_state(self._instance_id, self._branch_id)
        if (
            not InstitutionQuery(state)
            .check_permission(actor_id, definition.required_permission)
            .allow
        ):
            raise SkillPrerequisiteError(f"actor lacks {definition.required_permission!r}")

    def _start(self, skill_instance_id: EntityId, skill_id: EntityId, actor_id: EntityId) -> None:
        self._submit(
            "skill.start",
            {
                "instance_id": skill_instance_id.value,
                "skill_id": skill_id.value,
                "actor_id": actor_id.value,
            },
        )
        self._set_state(skill_instance_id, actor_id, "running", 0, "")

    def _advance(
        self,
        skill_instance_id: EntityId,
        actor_id: EntityId,
        step: SkillStep,
        instance: SkillInstance,
        completed: list[str],
    ) -> None:
        payload = dict(step.payload)
        if self._actor_field in step.payload and not step.payload[self._actor_field]:
            payload[self._actor_field] = actor_id.value
        try:
            self._check_step_capability(actor_id, step)
            self._submit(step.action_type, payload)
        except Exception as exc:
            self._set_state(
                skill_instance_id,
                actor_id,
                "failed",
                instance.current_step_index,
                ",".join(completed),
            )
            raise InvalidSkillStep(f"step {step.step_id!r} failed: {exc}") from exc
        completed.append(step.step_id)
        self._set_state(
            skill_instance_id,
            actor_id,
            "running",
            instance.current_step_index + 1,
            ",".join(completed),
        )

    def _check_step_capability(self, actor_id: EntityId, step: SkillStep) -> None:
        """Reject a step whose required capability level is not met (G03G)."""
        if step.requires_capability is None:
            return
        name, sep, min_raw = step.requires_capability.partition(":")
        min_level = int(min_raw) if sep and min_raw.isdigit() else 1
        from wanxiang_substrate.capability.query import CapabilityQuery

        state = self._runtime.current_state(self._instance_id, self._branch_id)
        if not CapabilityQuery(state).requires(actor_id, name, min_level):
            raise SkillPrerequisiteError(
                f"actor lacks capability {step.requires_capability!r} (need >= {min_level})"
            )

    def _set_state(
        self,
        skill_instance_id: EntityId,
        actor_id: EntityId,
        state: str,
        current_index: int,
        completed: str,
    ) -> None:
        self._submit(
            "skill.set_state",
            {
                "instance_id": skill_instance_id.value,
                "state": state,
                "current_step_index": current_index,
                "completed_steps": completed,
            },
        )

    def _submit(self, action_type: str, payload: Mapping[str, FieldValue]) -> None:
        clean_payload: dict[str, FieldValue] = {
            str(k): v
            for k, v in payload.items()
            if isinstance(v, (str, int, float, bool)) or v is None
        }
        state = self._runtime.current_state(self._instance_id, self._branch_id)
        self._runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(
                    f"skill_{action_type.replace('.', '_')}_{state.revision.value}"
                ),
                instance_id=self._instance_id,
                branch_id=self._branch_id,
                expected_revision=state.revision,
                action_type=action_type,
                payload=clean_payload,
                actor_id=ActorId(str(payload.get("actor_id") or "skill_actor")),
                world_time=WorldTime(state.revision.value + 1),
            )
        )

    def _load_instance(
        self, skill_instance_id: EntityId, skill_id: EntityId, actor_id: EntityId
    ) -> SkillInstance:
        from wanxiang_substrate.skills.components import SKILL_INSTANCE_COMPONENT

        state = self._runtime.current_state(self._instance_id, self._branch_id)
        entity = state.entity(skill_instance_id)
        if entity is None:
            raise SkillPrerequisiteError(f"skill instance {skill_instance_id.value} does not exist")
        for component in entity.components.values():
            if component.component_type == SKILL_INSTANCE_COMPONENT:
                return SkillInstance(
                    instance_id=skill_instance_id,
                    skill_id=skill_id,
                    actor_id=actor_id,
                    state=str(component.fields.get("state") or "idle"),  # type: ignore[arg-type]
                    current_step_index=int(component.fields.get("current_step_index") or 0),
                    completed_steps=tuple(
                        s
                        for s in str(component.fields.get("completed_steps") or "").split(",")
                        if s
                    ),
                )
        raise SkillPrerequisiteError(f"skill instance {skill_instance_id.value} has no component")
