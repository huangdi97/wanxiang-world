"""Rebuildable pattern observations derived from committed history (G94A)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    RelationCreate,
)
from wanxiang_domain.errors import ContractError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hashing import semantic_sha256

from wanxiang_substrate.evolution.pattern_observation_model import (
    PatternKind,
    PatternObservation,
    PatternStatistics,
)

_EXCHANGE_COMPONENTS = frozenset({"material.custody", "material.ownership", "material.contained"})


def _require_range(window_start: int, window_end: int) -> None:
    if isinstance(window_start, bool) or isinstance(window_end, bool):
        raise ContractError("pattern windows require integer ticks")
    if window_start < 0 or window_end <= window_start:
        raise ContractError("pattern window must be non-negative and non-empty")


def _unique_refs(values: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return tuple(result)


def _kind_for_component(component_type: str) -> PatternKind:
    if component_type in _EXCHANGE_COMPONENTS:
        return "exchange"
    if component_type.startswith(("institution.", "organization.")):
        return "organization"
    return "behavior"


def _kind_for_entity(entity_type: str) -> PatternKind:
    if entity_type.startswith(("institution.", "organization.")):
        return "organization"
    return "behavior"


def _features(subject_refs: tuple[str, ...], has_actor: bool) -> tuple[tuple[str, float], ...]:
    return (
        ("operation_count", 1.0),
        ("subject_count", float(len(subject_refs))),
        ("actor_present", float(has_actor)),
    )


def _subjects(event: CommittedEvent, refs: Iterable[str]) -> tuple[str, ...]:
    actor = (event.actor_id.value,) if event.actor_id is not None else ()
    return _unique_refs((*actor, *refs))


def _signals(
    event: CommittedEvent, operation_index: int
) -> Iterable[tuple[PatternKind, str, tuple[str, ...], int]]:
    for component_index, operation in enumerate(event.delta.operations):
        if isinstance(operation, EntityCreate):
            subjects = _subjects(event, (operation.entity_id.value,))
            yield (
                _kind_for_entity(operation.entity_type),
                f"entity.create:{operation.entity_type}",
                subjects,
                component_index,
            )
        elif isinstance(operation, EntityUpdate):
            component_types = tuple(component.component_type for component in operation.components)
            if not component_types:
                component_types = ("unknown",)
            for component_type in component_types:
                subjects = _subjects(event, (operation.entity_id.value,))
                yield (
                    _kind_for_component(component_type),
                    f"entity.update:{component_type}",
                    subjects,
                    operation_index + component_index,
                )
        elif isinstance(operation, EntityDelete):
            yield (
                "behavior",
                "entity.delete",
                _subjects(event, (operation.entity_id.value,)),
                component_index,
            )
        elif isinstance(operation, RelationCreate):
            subjects = _subjects(event, (operation.source_id.value, operation.target_id.value))
            yield (
                "relationship",
                f"relation.create:{operation.relation_type}",
                subjects,
                component_index,
            )
        else:
            yield (
                "relationship",
                "relation.delete",
                _subjects(event, (operation.relation_id.value,)),
                component_index,
            )


def _derive(events: tuple[CommittedEvent, ...], window_size: int) -> tuple[PatternObservation, ...]:
    observations: list[PatternObservation] = []
    for event in events:
        window_start = (event.world_time.ticks // window_size) * window_size
        window_end = window_start + window_size
        for signal_index, (kind, key, subjects, operation_index) in enumerate(
            _signals(event, event.event_seq.value)
        ):
            observations.append(
                PatternObservation(
                    observation_id=(
                        f"pattern_obs:{event.event_id.value}:{operation_index}:{signal_index}"
                    ),
                    kind=kind,
                    key=key,
                    subject_refs=subjects,
                    observed_at=event.world_time.ticks,
                    window_start=window_start,
                    window_end=window_end,
                    event_refs=(event.event_id.value,),
                    features=_features(subjects, event.actor_id is not None),
                )
            )
    return tuple(observations)


def _matches(
    observation: PatternObservation,
    window_start: int,
    window_end: int | None,
    kind: PatternKind | None,
    key: str | None,
    subject_ref: str | None,
) -> bool:
    if observation.window_end <= window_start:
        return False
    if window_end is not None and observation.window_start >= window_end:
        return False
    return (
        (kind is None or observation.kind == kind)
        and (key is None or observation.key == key)
        and (subject_ref is None or subject_ref in observation.subject_refs)
    )


@dataclass(frozen=True, slots=True)
class PatternObservationStore:
    """Immutable derived cache that can always be rebuilt from events."""

    window_size: int
    _observations: tuple[PatternObservation, ...] = ()

    def __post_init__(self) -> None:
        if self.window_size < 1:
            raise ContractError("pattern window size must be positive")
        ids = tuple(item.observation_id for item in self._observations)
        if len(ids) != len(set(ids)):
            raise ContractError("pattern observation ids must be unique")

    @classmethod
    def rebuild(
        cls, events: Iterable[CommittedEvent], *, window_size: int = 100
    ) -> PatternObservationStore:
        """Rebuild the cache from one committed branch history."""
        if window_size < 1:
            raise ContractError("pattern window size must be positive")
        ordered = tuple(
            sorted(events, key=lambda event: (event.event_seq.value, event.event_id.value))
        )
        event_ids = tuple(event.event_id.value for event in ordered)
        if len(event_ids) != len(set(event_ids)):
            raise ContractError("committed history contains duplicate event refs")
        if ordered:
            stream = {(event.instance_id.value, event.branch_id.value) for event in ordered}
            if len(stream) != 1:
                raise ContractError("pattern cache requires one instance and branch history")
        return cls(window_size=window_size, _observations=_derive(ordered, window_size))

    from_events = rebuild

    def observations(self) -> tuple[PatternObservation, ...]:
        return self._observations

    def event_refs(self) -> tuple[str, ...]:
        return tuple(sorted({ref for item in self._observations for ref in item.event_refs}))

    def query_window(
        self,
        window_start: int,
        window_end: int,
        *,
        kind: PatternKind | None = None,
        key: str | None = None,
        subject_ref: str | None = None,
    ) -> tuple[PatternObservation, ...]:
        _require_range(window_start, window_end)
        return tuple(
            item
            for item in self._observations
            if _matches(item, window_start, window_end, kind, key, subject_ref)
        )

    def query(
        self,
        *,
        window_start: int = 0,
        window_end: int | None = None,
        kind: PatternKind | None = None,
        key: str | None = None,
        subject_ref: str | None = None,
    ) -> tuple[PatternObservation, ...]:
        if window_start < 0 or (window_end is not None and window_end <= window_start):
            raise ContractError("invalid pattern query window")
        return tuple(
            item
            for item in self._observations
            if _matches(item, window_start, window_end, kind, key, subject_ref)
        )

    def statistics(
        self,
        *,
        window_start: int = 0,
        window_end: int | None = None,
        kind: PatternKind | None = None,
        key: str | None = None,
        subject_ref: str | None = None,
    ) -> PatternStatistics:
        selected = self.query(
            window_start=window_start,
            window_end=window_end,
            kind=kind,
            key=key,
            subject_ref=subject_ref,
        )
        resolved_end = window_end or max(
            (item.window_end for item in selected), default=window_start
        )
        event_refs = {ref for item in selected for ref in item.event_refs}
        subject_refs = {ref for item in selected for ref in item.subject_refs}
        feature_values: dict[str, list[float]] = {}
        for item in selected:
            for name, value in item.features:
                feature_values.setdefault(name, []).append(value)
        means = tuple(
            (name, sum(values) / len(values)) for name, values in sorted(feature_values.items())
        )
        by_kind: dict[str, int] = {}
        for item in selected:
            by_kind[item.kind] = by_kind.get(item.kind, 0) + 1
        span = max((item.observed_at for item in selected), default=0) - min(
            (item.observed_at for item in selected), default=0
        )
        total_subjects = sum(len(item.subject_refs) for item in selected)
        return PatternStatistics(
            window_start=window_start,
            window_end=resolved_end,
            observation_count=len(selected),
            total_occurrences=sum(item.occurrence_count for item in selected),
            unique_event_count=len(event_refs),
            unique_key_count=len({item.key for item in selected}),
            unique_subject_count=len(subject_refs),
            mean_subject_count=(total_subjects / len(selected) if selected else 0.0),
            span_ticks=max(0, span),
            by_kind=tuple(sorted(by_kind.items())),
            feature_means=means,
        )

    def cache_hash(self) -> str:
        return semantic_sha256(
            {
                "window_size": self.window_size,
                "observations": [item.to_dict() for item in self._observations],
            }
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "window_size": self.window_size,
            "event_refs": list(self.event_refs()),
            "observations": [item.to_dict() for item in self._observations],
            "cache_hash": self.cache_hash(),
        }
