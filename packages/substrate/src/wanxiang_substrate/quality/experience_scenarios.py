"""Frozen M97 benchmark families and reproducible action plans."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ScenarioFamily = Literal["source", "prompt"]


@dataclass(frozen=True, slots=True)
class ExperienceBenchmarkScenario:
    """A scenario plan containing references, never canonical world state."""

    scenario_id: str
    family: ScenarioFamily
    world_ref: str
    package_ref: str
    version: str
    action_script: tuple[str, ...]
    human_slots: tuple[str, ...]
    provenance_policy: str

    def __post_init__(self) -> None:
        for name in (
            "scenario_id",
            "world_ref",
            "package_ref",
            "version",
            "provenance_policy",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ContractError(f"{name} must be a non-empty value")
        if self.family not in {"source", "prompt"}:
            raise ContractError(f"unsupported benchmark family {self.family!r}")
        if not self.action_script or len(set(self.action_script)) != len(self.action_script):
            raise ContractError("benchmark action_script must be non-empty and unique")
        if not self.human_slots or len(set(self.human_slots)) != len(self.human_slots):
            raise ContractError("benchmark human_slots must be non-empty and unique")
        if any(not item.strip() for item in (*self.action_script, *self.human_slots)):
            raise ContractError("benchmark slot values must be non-empty")

    def to_dict(self) -> dict[str, object]:
        return {
            "scenario_id": self.scenario_id,
            "family": self.family,
            "world_ref": self.world_ref,
            "package_ref": self.package_ref,
            "version": self.version,
            "action_script": list(self.action_script),
            "human_slots": list(self.human_slots),
            "provenance_policy": self.provenance_policy,
        }


def stable_m97_scenarios() -> tuple[ExperienceBenchmarkScenario, ...]:
    """Return the two Stable benchmark families frozen for M97."""
    human_slots = (
        "session_id",
        "action_trace",
        "ratings_1_to_5",
        "critical_blocker",
        "free_notes",
    )
    return (
        ExperienceBenchmarkScenario(
            scenario_id="scenario:m97:source-qualification-v1",
            family="source",
            world_ref="world:m97:source-qualification-v1",
            package_ref="world:wd_m97_source_qualification",
            version="1",
            action_script=(
                "enter:embodiment",
                "action:set_status:source_active",
                "action:set_status:source_progress",
                "action:set_status:source_complete",
                "leave",
                "continue",
            ),
            human_slots=human_slots,
            provenance_policy="creator_owned_synthetic_source_only",
        ),
        ExperienceBenchmarkScenario(
            scenario_id="scenario:m97:original-prompt-v1",
            family="prompt",
            world_ref="world:wd_m96_original_prompt_world",
            package_ref="world:wd_m96_original_prompt_world",
            version="1",
            action_script=(
                "enter:embodiment",
                "action:set_status:prompt_active",
                "action:set_status:prompt_progress",
                "action:set_status:prompt_complete",
                "leave",
                "continue",
            ),
            human_slots=human_slots,
            provenance_policy="creator_intent_hash_only_no_source_book",
        ),
    )


__all__ = ["ExperienceBenchmarkScenario", "ScenarioFamily", "stable_m97_scenarios"]
