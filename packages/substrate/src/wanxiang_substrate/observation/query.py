"""Deterministic perspective queries over canonical state and committed events."""

from __future__ import annotations

from wanxiang_domain.delta import EntityCreate, EntityUpdate
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.material.components import CUSTODY_COMPONENT
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.observation.components import (
    ANNOUNCEMENT_COMPONENT,
    OBSERVATION_VISIBILITY_COMPONENT,
)
from wanxiang_substrate.observation.model import (
    Channel,
    EntityVisibility,
    Observation,
    ObservationFact,
    channel_confidence,
)
from wanxiang_substrate.spatial.components import POSITION_COMPONENT
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.temporal.query import TemporalQuery


class PerspectiveService:
    """Assembles the observations an observer could perceive (deterministic)."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._state = state
        self._spatial = SpatialQuery(state)
        now = TemporalQuery(state).now()
        self._institution = InstitutionQuery(state, now_ticks=now)
        self._material = MaterialQuery(state)
        self._visibility: dict[EntityId, EntityVisibility] = {}
        self._scan_visibility(state)

    def _scan_visibility(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type != OBSERVATION_VISIBILITY_COMPONENT:
                    continue
                entity_id = EntityId(
                    str(component.fields.get("entity_id") or entity.entity_id.value)
                )
                level = str(component.fields.get("level") or "public")
                group_raw = component.fields.get("group_id")
                group = EntityId(group_raw) if isinstance(group_raw, str) and group_raw else None
                self._visibility[entity_id] = EntityVisibility(entity_id, level, group)  # type: ignore[arg-type]

    def context_for(
        self, observer: EntityId, events: tuple[CommittedEvent, ...]
    ) -> tuple[Observation, ...]:
        observations: list[Observation] = []
        for event in events:
            fact = self._fact_from_event(event)
            if fact is None:
                continue
            observations.extend(self._observations_for(observer, event, fact))
        return tuple(sorted(observations, key=lambda o: (o.observed_at, o.observation_id)))

    def _fact_from_event(self, event: CommittedEvent) -> ObservationFact | None:
        if not event.delta.operations:
            return None
        action = event.delta.operations[0]
        if isinstance(action, EntityUpdate):
            if _has_component(action, POSITION_COMPONENT):
                place = _position_place(self._state, action.entity_id)
                return ObservationFact(
                    kind="movement",
                    subject=action.entity_id.value,
                    place=place,
                    fields=(("entity", action.entity_id.value), ("place", place.value)),
                )
            if _has_component(action, CUSTODY_COMPONENT):
                place = self._material_place(action.entity_id)
                return ObservationFact(
                    kind="transfer",
                    subject=action.entity_id.value,
                    place=place or EntityId("unknown"),
                    fields=(("item", action.entity_id.value),),
                )
        if isinstance(action, EntityCreate):
            return _announcement_fact(action)
        return None

    def _material_place(self, item: EntityId) -> EntityId | None:
        custodian = self._material.custodian(item)
        if custodian is None:
            return None
        return self._spatial.location(custodian)

    def _observations_for(
        self, observer: EntityId, event: CommittedEvent, fact: ObservationFact
    ) -> list[Observation]:
        observer_place = self._spatial.location(observer)
        if observer_place is None:
            return []
        visibility = self._visibility_for_event(event)
        if not self._visibility_allows(observer, event, visibility):
            return []
        observations: list[Observation] = []
        visible = self._spatial.visibility_zone(observer_place).visible_places
        if fact.place == observer_place or fact.place in visible:
            observations.append(
                self._make_observation(observer, event, fact, "visual", ("visual:line_of_sight",))
            )
        audible = self._spatial.acoustic_zone(observer_place).audible_places
        if fact.place in audible:
            observations.append(
                self._make_observation(observer, event, fact, "acoustic", ("acoustic:portal",))
            )
        if fact.kind == "announcement" and fact.place == observer_place:
            observations.append(
                self._make_observation(observer, event, fact, "textual", ("textual:direct",))
            )
        return observations

    def _visibility_for_event(self, event: CommittedEvent) -> EntityVisibility:
        actor = _actor_of_event(event)
        if actor is not None and actor in self._visibility:
            return self._visibility[actor]
        return EntityVisibility(actor or EntityId("unknown"), "public")

    def _visibility_allows(
        self,
        observer: EntityId,
        event: CommittedEvent,
        visibility: EntityVisibility,
    ) -> bool:
        if visibility.level == "public":
            return True
        if visibility.level == "private":
            return _actor_of_event(event) == observer
        if visibility.level == "group" and visibility.group_id is not None:
            return any(
                m.actor_id == observer and m.institution_id == visibility.group_id
                for m in self._institution.memberships(observer)
            )
        return False

    def _make_observation(
        self,
        observer: EntityId,
        event: CommittedEvent,
        fact: ObservationFact,
        channel: Channel,
        rules: tuple[str, ...],
    ) -> Observation:
        return Observation(
            observation_id=f"obs_{observer.value}_{event.event_id.value}_{channel}",
            observer_id=observer,
            source_event_id=event.event_id,
            observed_at=event.world_time.ticks,
            place=fact.place,
            channel=channel,
            fact=fact,
            confidence=channel_confidence(channel),
            rule_refs=rules,
        )


def _actor_of_event(event: CommittedEvent) -> EntityId | None:
    if event.actor_id is None:
        return None
    return EntityId(event.actor_id.value)


def _has_component(update: EntityUpdate, component_type: str) -> bool:
    return any(
        getattr(component, "component_type", None) == component_type
        for component in update.components
    )


def _announcement_fact(action: EntityCreate) -> ObservationFact | None:
    for component in action.components:
        if getattr(component, "component_type", None) != ANNOUNCEMENT_COMPONENT:
            continue
        fields = dict(component.fields)
        actor = fields.get("actor_id")
        message = fields.get("message")
        place = fields.get("place_id")
        if not isinstance(actor, str) or not isinstance(message, str) or not isinstance(place, str):
            return None
        return ObservationFact(
            kind="announcement",
            subject=actor,
            place=EntityId(place),
            fields=(("message", message), ("actor", actor)),
        )
    return None


def _position_place(state: InMemoryCanonicalState, entity_id: EntityId) -> EntityId:
    entity = state.entity(entity_id)
    if entity is None:
        return entity_id
    for component in entity.components.values():
        if component.component_type == POSITION_COMPONENT:
            place = component.fields.get("place_id")
            if isinstance(place, str):
                return EntityId(place)
    return entity_id
