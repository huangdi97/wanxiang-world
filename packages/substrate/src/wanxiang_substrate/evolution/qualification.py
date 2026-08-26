"""Baseline/evolved comparisons for the M90 evolution qualification (G93H)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


def _pairs(values: tuple[tuple[str, str], ...], label: str) -> None:
    if any(not key.strip() or not value.strip() for key, value in values):
        raise ContractError(f"{label} fingerprints require non-blank refs")
    if len({key for key, _ in values}) != len(values):
        raise ContractError(f"{label} fingerprints require unique refs")


def _refs(values: tuple[str, ...], label: str) -> None:
    if any(not value.strip() for value in values) or len(set(values)) != len(values):
        raise ContractError(f"{label} refs must be unique and non-blank")


@dataclass(frozen=True, slots=True)
class EvolutionProjectionSnapshot:
    """A measured projection checkpoint; canonical history remains external."""

    run_id: str
    elapsed_days: int
    world_ticks: int
    source_ref: str
    source_content_hash: str
    package_ref: str
    canonical_hash: str
    replay_hash: str
    canonical_revision: int
    canonical_event_refs: tuple[str, ...]
    actor_fingerprints: tuple[tuple[str, str], ...]
    relationship_fingerprints: tuple[tuple[str, str], ...]
    organization_fingerprints: tuple[tuple[str, str], ...]
    evidence_refs: tuple[str, ...]
    validated_delta_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.run_id.strip() or not self.source_ref.strip() or not self.package_ref.strip():
            raise ContractError("evolution snapshot identity is incomplete")
        if self.elapsed_days < 0 or self.world_ticks < 0 or self.canonical_revision < 0:
            raise ContractError("evolution snapshot metrics cannot be negative")
        if not self.source_content_hash.strip() or not self.canonical_hash.strip():
            raise ContractError("evolution snapshot hashes are required")
        if not self.replay_hash.strip():
            raise ContractError("evolution snapshot replay hash is required")
        _refs(self.canonical_event_refs, "canonical event")
        _pairs(self.actor_fingerprints, "actor")
        _pairs(self.relationship_fingerprints, "relationship")
        _pairs(self.organization_fingerprints, "organization")
        _refs(self.evidence_refs, "evolution evidence")
        _refs(self.validated_delta_ids, "validated delta")
        if self.canonical_revision != len(self.canonical_event_refs):
            raise ContractError("canonical revision must match event refs")


def _changed_refs(
    before: tuple[tuple[str, str], ...], after: tuple[tuple[str, str], ...]
) -> tuple[str, ...]:
    old = dict(before)
    new = dict(after)
    return tuple(sorted(key for key in set(old) | set(new) if old.get(key) != new.get(key)))


@dataclass(frozen=True, slots=True)
class EvolutionRunComparison:
    """Evidence-bound baseline/evolved comparison for the M90 gate."""

    baseline: EvolutionProjectionSnapshot
    evolved: EvolutionProjectionSnapshot
    required_days: int
    changed_actor_refs: tuple[str, ...]
    changed_relationship_refs: tuple[str, ...]
    changed_organization_refs: tuple[str, ...]

    @property
    def source_unchanged(self) -> bool:
        return (
            self.baseline.source_ref == self.evolved.source_ref
            and self.baseline.source_content_hash == self.evolved.source_content_hash
        )

    @property
    def package_unchanged(self) -> bool:
        return self.baseline.package_ref == self.evolved.package_ref

    @property
    def canonical_history_preserved(self) -> bool:
        prefix = self.evolved.canonical_event_refs[: len(self.baseline.canonical_event_refs)]
        return prefix == self.baseline.canonical_event_refs

    @property
    def replay_equal(self) -> bool:
        return self.evolved.canonical_hash == self.evolved.replay_hash

    @property
    def nonzero_projection_change(self) -> bool:
        return bool(
            self.changed_actor_refs
            and self.changed_relationship_refs
            and self.changed_organization_refs
        )

    @property
    def qualified(self) -> bool:
        elapsed = self.evolved.elapsed_days - self.baseline.elapsed_days
        return (
            self.required_days > 0
            and elapsed >= self.required_days
            and self.evolved.world_ticks > self.baseline.world_ticks
            and self.evolved.canonical_revision > self.baseline.canonical_revision
            and len(self.evolved.canonical_event_refs) > len(self.baseline.canonical_event_refs)
            and self.source_unchanged
            and self.package_unchanged
            and self.canonical_history_preserved
            and self.replay_equal
            and self.nonzero_projection_change
            and bool(self.evolved.evidence_refs)
            and bool(self.evolved.validated_delta_ids)
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.evolved.run_id,
            "required_days": self.required_days,
            "elapsed_days": self.evolved.elapsed_days - self.baseline.elapsed_days,
            "world_ticks": self.evolved.world_ticks,
            "changed_actor_refs": list(self.changed_actor_refs),
            "changed_relationship_refs": list(self.changed_relationship_refs),
            "changed_organization_refs": list(self.changed_organization_refs),
            "source_unchanged": self.source_unchanged,
            "package_unchanged": self.package_unchanged,
            "canonical_history_preserved": self.canonical_history_preserved,
            "replay_equal": self.replay_equal,
            "qualified": self.qualified,
        }


def compare_evolution(
    baseline: EvolutionProjectionSnapshot,
    evolved: EvolutionProjectionSnapshot,
    *,
    required_days: int = 30,
) -> EvolutionRunComparison:
    """Compare typed actor/relationship/organization projection checkpoints."""
    if baseline.run_id != evolved.run_id:
        raise ContractError("evolution snapshots belong to different runs")
    if required_days < 1:
        raise ContractError("evolution qualification requires positive duration")
    return EvolutionRunComparison(
        baseline=baseline,
        evolved=evolved,
        required_days=required_days,
        changed_actor_refs=_changed_refs(baseline.actor_fingerprints, evolved.actor_fingerprints),
        changed_relationship_refs=_changed_refs(
            baseline.relationship_fingerprints, evolved.relationship_fingerprints
        ),
        changed_organization_refs=_changed_refs(
            baseline.organization_fingerprints, evolved.organization_fingerprints
        ),
    )
