"""Read-model queries for capability & learning state (pure, no mutation)."""

from __future__ import annotations

import json
from typing import cast

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.capability.components import (
    ASSESSMENT_COMPONENT,
    CAPABILITY_STATE_COMPONENT,
    PRACTICE_RECORD_COMPONENT,
)
from wanxiang_substrate.capability.model import (
    AssessmentEvidence,
    CapabilityState,
    LearnerState,
    PracticeRecord,
)


def capability_entity_id(actor_id: EntityId, capability: str) -> EntityId:
    return EntityId(f"cap_{actor_id.value}_{capability}")


def _as_str(value: object, field: str) -> str:
    return str(value or "")


class CapabilityQuery:
    """Queries over committed canonical state (authoritative read model)."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._state = state

    def capability(self, actor_id: EntityId, name: str) -> CapabilityState | None:
        entity = self._state.entity(capability_entity_id(actor_id, name))
        if entity is None:
            return None
        component = next(
            (
                c
                for c in entity.components.values()
                if c.component_type == CAPABILITY_STATE_COMPONENT
            ),
            None,
        )
        if component is None:
            return None
        return self._state_from_component(component)

    def requires(self, actor_id: EntityId, name: str, min_level: int = 1) -> bool:
        current = self.capability(actor_id, name)
        return current is not None and current.level >= min_level

    def capabilities(self, actor_id: EntityId) -> tuple[CapabilityState, ...]:
        prefix = f"cap_{actor_id.value}_"
        found: list[CapabilityState] = []
        for entity in self._state.entities():
            for component in entity.components.values():
                if (
                    component.component_type == CAPABILITY_STATE_COMPONENT
                    and str(component.fields.get("actor_id")) == actor_id.value
                ):
                    found.append(self._state_from_component(component))
        found.sort(key=lambda c: (c.capability, prefix))
        return tuple(found)

    def practice_records(self, actor_id: EntityId) -> tuple[PracticeRecord, ...]:
        records: list[PracticeRecord] = []
        for entity in self._state.entities():
            for component in entity.components.values():
                if (
                    component.component_type == PRACTICE_RECORD_COMPONENT
                    and str(component.fields.get("actor_id")) == actor_id.value
                ):
                    records.append(
                        PracticeRecord(
                            record_id=EntityId(
                                _as_str(component.fields.get("record_id"), "record_id")
                            ),
                            actor_id=actor_id,
                            capability=_as_str(component.fields.get("capability"), "capability"),
                            practice_count=int(component.fields.get("practice_count") or 0),
                            evidence_ref=_as_str(
                                component.fields.get("evidence_ref"), "evidence_ref"
                            ),
                        )
                    )
        records.sort(key=lambda r: r.record_id.value)
        return tuple(records)

    def assessments(self, actor_id: EntityId) -> tuple[AssessmentEvidence, ...]:
        found: list[AssessmentEvidence] = []
        for entity in self._state.entities():
            for component in entity.components.values():
                if (
                    component.component_type == ASSESSMENT_COMPONENT
                    and str(component.fields.get("actor_id")) == actor_id.value
                ):
                    found.append(
                        AssessmentEvidence(
                            assessment_id=EntityId(
                                _as_str(component.fields.get("assessment_id"), "assessment_id")
                            ),
                            actor_id=actor_id,
                            capability=_as_str(component.fields.get("capability"), "capability"),
                            assessment_type=_as_str(
                                component.fields.get("assessment_type"), "assessment_type"
                            ),
                            outcome=_as_str(component.fields.get("outcome"), "outcome"),
                            evidence_ref=_as_str(
                                component.fields.get("evidence_ref"), "evidence_ref"
                            ),
                        )
                    )
        found.sort(key=lambda a: a.assessment_id.value)
        return tuple(found)

    def biography(self, actor_id: EntityId) -> tuple[str, ...]:
        events: list[tuple[int, str]] = []
        for entity in self._state.entities():
            for component in entity.components.values():
                if (
                    component.component_type in (PRACTICE_RECORD_COMPONENT, ASSESSMENT_COMPONENT)
                    and str(component.fields.get("actor_id")) == actor_id.value
                ):
                    seq = int(component.fields.get("seq") or 0)
                    ref = _as_str(component.fields.get("evidence_ref"), "evidence_ref")
                    events.append((seq, ref))
        events.sort(key=lambda item: item[0])
        return tuple(ref for _, ref in events)

    def learner_state(self, actor_id: EntityId) -> LearnerState:
        return LearnerState(
            actor_id=actor_id,
            capabilities=self.capabilities(actor_id),
            practice_records=len(self.practice_records(actor_id)),
            assessment_records=len(self.assessments(actor_id)),
            biography=self.biography(actor_id),
        )

    def record_count(self, actor_id: EntityId) -> int:
        return len(self.practice_records(actor_id)) + len(self.assessments(actor_id))

    @staticmethod
    def _state_from_component(component: object) -> CapabilityState:
        from wanxiang_domain.entity import ComponentData

        data = cast(ComponentData, component)
        evidence_raw = data.fields.get("evidence_refs", "[]")
        try:
            decoded = json.loads(str(evidence_raw))
        except ValueError:
            decoded = []
        decoded_list = cast(list[object], decoded)
        refs = tuple(sorted(str(item) for item in decoded_list if isinstance(item, str)))
        return CapabilityState(
            actor_id=EntityId(_as_str(data.fields.get("actor_id"), "actor_id")),
            capability=_as_str(data.fields.get("capability"), "capability"),
            level=int(data.fields.get("level") or 0),
            mastery=float(data.fields.get("mastery") or 0.0),
            confidence=float(data.fields.get("confidence") or 0.0),
            evidence_refs=refs,
            updated_revision=int(data.fields.get("updated_revision") or 0),
        )
