"""Versioned skill registry with reference skills."""

from __future__ import annotations

from wanxiang_domain.ids import EntityId

from wanxiang_substrate.skills.model import SkillDefinition, SkillStep

DELIVER_LETTER = EntityId("skill_deliver_letter")
INSPECT_OBJECT = EntityId("skill_inspect_object")


class SkillRegistry:
    """Maps (skill_id, version) -> SkillDefinition."""

    def __init__(self) -> None:
        self._skills: dict[tuple[str, int], SkillDefinition] = {}

    def register(self, definition: SkillDefinition) -> None:
        self._skills[(definition.skill_id.value, definition.version)] = definition

    def get(self, skill_id: EntityId, version: int = 1) -> SkillDefinition | None:
        return self._skills.get((skill_id.value, version))


def register_reference_skills(registry: SkillRegistry) -> None:
    registry.register(
        SkillDefinition(
            skill_id=DELIVER_LETTER,
            version=1,
            name="deliver_letter",
            required_permission="deliver",
            steps=(
                SkillStep(
                    "take",
                    "material.transfer",
                    {
                        "item_id": "letter_1",
                        "from_custodian": "writer",
                        "to_custodian": "messenger",
                    },
                    duration_ticks=5,
                    cost=1,
                ),
                SkillStep(
                    "move",
                    "spatial.move",
                    {"entity_id": "messenger", "target_place_id": "recipient_house"},
                    duration_ticks=20,
                    cost=2,
                ),
                SkillStep(
                    "hand_over",
                    "material.transfer",
                    {
                        "item_id": "letter_1",
                        "from_custodian": "messenger",
                        "to_custodian": "recipient",
                    },
                    duration_ticks=5,
                    cost=1,
                ),
            ),
        )
    )
    registry.register(
        SkillDefinition(
            skill_id=INSPECT_OBJECT,
            version=1,
            name="inspect_object",
            steps=(
                SkillStep(
                    "inspect", "agency.inspect", {"target": "object_1"}, duration_ticks=10, cost=1
                ),
            ),
        )
    )
