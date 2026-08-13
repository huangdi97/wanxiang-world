"""Pure skill value objects: definitions, steps, instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

SkillState = Literal["idle", "running", "paused", "completed", "failed", "cancelled"]


@dataclass(frozen=True, slots=True)
class SkillStep:
    step_id: str
    action_type: str
    payload: dict[str, FieldValue]
    requires_capability: str | None = None
    duration_ticks: int = 0
    cost: int = 0

    def __post_init__(self) -> None:
        if not self.step_id or not self.action_type:
            raise ContractError("skill step requires step_id and action_type")


@dataclass(frozen=True, slots=True)
class SkillDefinition:
    skill_id: EntityId
    version: int
    name: str
    steps: tuple[SkillStep, ...]
    required_permission: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.steps:
            raise ContractError("skill requires a name and at least one step")
        if self.version <= 0:
            raise ContractError("skill version must be positive")

    def step(self, step_id: str) -> SkillStep | None:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None


@dataclass(frozen=True, slots=True)
class SkillInstance:
    instance_id: EntityId
    skill_id: EntityId
    actor_id: EntityId
    state: SkillState = "idle"
    current_step_index: int = 0
    completed_steps: tuple[str, ...] = ()

    def next_step(self, definition: SkillDefinition) -> SkillStep | None:
        if self.current_step_index >= len(definition.steps):
            return None
        return definition.steps[self.current_step_index]
