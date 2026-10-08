"""RealityProfile major-upgrade planning: shadow replay and drift detection.

The planner never mutates anything. It replays the same worldline under the old
and the candidate RealityProfile, compares the results dimension by dimension, and
recommends `migrate`, `fork` or `reject`. Applying a plan is
:mod:`wanxiang_reality.migration_apply`, which requires explicit human approval for
a major upgrade.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from wanxiang_reality.errors import ProfileError
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.profiles import RealityProfile, RuntimeLock

MIGRATION_SCHEMA = "wanxiang.r7.reality-profile-migration.v1"

#: Dimensions compared between the baseline and the shadow replay.
DRIFT_DIMENSIONS = (
    "world_identity",
    "entity_identity",
    "history_head",
    "state_hash",
    "normalized_projection",
    "branch_graph",
    "lineage",
    "rights_evidence",
)


@dataclass(frozen=True, slots=True)
class LockedSnapshot:
    """Immutable read model a replay starts from."""

    world_id: str
    worldline_id: str
    revision: int
    state_hash: str
    event_count: int
    profile_ref: str
    lock_digest: str


@dataclass(frozen=True, slots=True)
class ReplayOutcome:
    """Result of replaying one worldline under one profile and lock."""

    world_id: str
    worldline_id: str
    history_head: int
    state_hash: str
    entity_ids: tuple[str, ...]
    branch_graph_digest: str
    lineage_digest: str
    rights_evidence_digest: str
    projection: Mapping[str, str]
    invariants: Mapping[str, bool]
    failed: bool = False
    failure_reason: str | None = None


class ReplaySource(Protocol):
    """Read-only services a migration needs; implemented by the world runtime."""

    def snapshot(self, worldline_id: str) -> LockedSnapshot:
        """Capture the worldline head before any replay."""
        ...

    def replay(
        self, worldline_id: str, profile: RealityProfile, lock: RuntimeLock
    ) -> ReplayOutcome:
        """Replay the worldline under the given profile and lock, without writing."""
        ...


@dataclass(frozen=True, slots=True)
class DriftEntry:
    dimension: str
    baseline: str
    candidate: str
    drifted: bool


@dataclass(frozen=True, slots=True)
class DriftReport:
    """Per-dimension comparison of two replays."""

    entries: tuple[DriftEntry, ...]
    invariant_failures: tuple[str, ...]
    replay_failed: bool
    failure_reason: str | None

    @property
    def drifted_dimensions(self) -> tuple[str, ...]:
        return tuple(entry.dimension for entry in self.entries if entry.drifted)

    @property
    def semantic_drift(self) -> bool:
        """True when the two profiles do not produce the same world semantics."""
        return bool(self.drifted_dimensions) or self.replay_failed

    @property
    def digest(self) -> str:
        return canonical_digest(
            {
                "entries": [
                    {
                        "dimension": entry.dimension,
                        "baseline": entry.baseline,
                        "candidate": entry.candidate,
                        "drifted": entry.drifted,
                    }
                    for entry in self.entries
                ],
                "invariant_failures": list(self.invariant_failures),
                "replay_failed": self.replay_failed,
            }
        )


def _compare(dimension: str, baseline: object, candidate: object) -> DriftEntry:
    left = str(baseline)
    right = str(candidate)
    return DriftEntry(dimension, left, right, left != right)


def compare_replay(baseline: ReplayOutcome, candidate: ReplayOutcome) -> DriftReport:
    """Compare the baseline replay with the shadow replay, dimension by dimension."""
    entries = [
        _compare("world_identity", baseline.world_id, candidate.world_id),
        _compare(
            "entity_identity",
            ",".join(sorted(baseline.entity_ids)),
            ",".join(sorted(candidate.entity_ids)),
        ),
        _compare("history_head", baseline.history_head, candidate.history_head),
        _compare("state_hash", baseline.state_hash, candidate.state_hash),
        _compare(
            "normalized_projection",
            canonical_digest(dict(baseline.projection)),
            canonical_digest(dict(candidate.projection)),
        ),
        _compare("branch_graph", baseline.branch_graph_digest, candidate.branch_graph_digest),
        _compare("lineage", baseline.lineage_digest, candidate.lineage_digest),
        _compare(
            "rights_evidence",
            baseline.rights_evidence_digest,
            candidate.rights_evidence_digest,
        ),
    ]
    failures = tuple(sorted(name for name, ok in candidate.invariants.items() if not ok))
    return DriftReport(
        entries=tuple(entries),
        invariant_failures=failures,
        replay_failed=candidate.failed,
        failure_reason=candidate.failure_reason,
    )


@dataclass(frozen=True, slots=True)
class Precondition:
    name: str
    satisfied: bool
    detail: str


@dataclass(frozen=True, slots=True)
class MigrationPlan:
    """The evaluated upgrade plan; a recommendation, never an action."""

    worldline_id: str
    from_profile_ref: str
    to_profile_ref: str
    from_lock_digest: str
    to_lock_digest: str
    migration_code_version: str
    requires_approval: bool
    recommendation: str
    preconditions: tuple[Precondition, ...]
    drift: DriftReport

    @property
    def plan_digest(self) -> str:
        return canonical_digest(
            {
                "schema": MIGRATION_SCHEMA,
                "worldline_id": self.worldline_id,
                "from_profile_ref": self.from_profile_ref,
                "to_profile_ref": self.to_profile_ref,
                "from_lock_digest": self.from_lock_digest,
                "to_lock_digest": self.to_lock_digest,
                "migration_code_version": self.migration_code_version,
                "requires_approval": self.requires_approval,
                "recommendation": self.recommendation,
                "preconditions": [
                    {
                        "name": item.name,
                        "satisfied": item.satisfied,
                        "detail": item.detail,
                    }
                    for item in self.preconditions
                ],
                "drift": self.drift.digest,
            }
        )

    @property
    def blocked_by(self) -> tuple[str, ...]:
        """Preconditions that failed, in declaration order."""
        return tuple(item.name for item in self.preconditions if not item.satisfied)


def plan_migration(
    *,
    worldline_id: str,
    baseline_profile: RealityProfile,
    target_profile: RealityProfile,
    baseline_lock: RuntimeLock,
    target_lock: RuntimeLock,
    source: ReplaySource,
    migration_code_version: str,
) -> MigrationPlan:
    """Shadow-replay one worldline and recommend migrate / fork / reject.

    Raises:
        ProfileError: when the target profile is not a major upgrade, when a lock
            does not belong to the profile it is paired with, or when a lock is
            invalid.
    """
    if not migration_code_version:
        raise ProfileError("migration_code_version is required")
    if not target_profile.version.is_major_upgrade_from(baseline_profile.version):
        raise ProfileError(
            f"{target_profile.profile_id}@{target_profile.version} is not a major upgrade of "
            f"{baseline_profile.version}; a non-major change must not open a migration path"
        )
    baseline_lock.validate()
    target_lock.validate()
    for lock, profile in ((baseline_lock, baseline_profile), (target_lock, target_profile)):
        expected = f"{profile.profile_id}@{profile.version}"
        if lock.reality_profile_ref != expected:
            raise ProfileError(f"runtime lock pins {lock.reality_profile_ref}, expected {expected}")

    snapshot = source.snapshot(worldline_id)
    baseline = source.replay(worldline_id, baseline_profile, baseline_lock)
    candidate = source.replay(worldline_id, target_profile, target_lock)
    drift = compare_replay(baseline, candidate)

    preconditions = (
        Precondition(
            "major_upgrade",
            True,
            f"{baseline_profile.version} -> {target_profile.version}",
        ),
        Precondition(
            "snapshot_matches_baseline_profile",
            snapshot.profile_ref == f"{baseline_profile.profile_id}@{baseline_profile.version}",
            f"snapshot profile {snapshot.profile_ref}",
        ),
        Precondition(
            "replay_integrity",
            not drift.replay_failed,
            drift.failure_reason or "baseline and shadow replay completed",
        ),
        Precondition(
            "declared_invariants_hold",
            not drift.invariant_failures,
            ", ".join(drift.invariant_failures) or "no invariant failure",
        ),
    )

    if not all(item.satisfied for item in preconditions):
        recommendation = "reject"
    elif drift.semantic_drift:
        recommendation = "fork"
    else:
        recommendation = "migrate"

    return MigrationPlan(
        worldline_id=worldline_id,
        from_profile_ref=f"{baseline_profile.profile_id}@{baseline_profile.version}",
        to_profile_ref=f"{target_profile.profile_id}@{target_profile.version}",
        from_lock_digest=baseline_lock.lock_digest(),
        to_lock_digest=target_lock.lock_digest(),
        migration_code_version=migration_code_version,
        requires_approval=True,
        recommendation=recommendation,
        preconditions=preconditions,
        drift=drift,
    )
