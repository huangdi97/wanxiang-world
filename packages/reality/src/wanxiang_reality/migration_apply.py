"""Apply a RealityProfile migration plan: migrate, fork, or refuse.

A major upgrade is never a silent hot swap. Applying a plan requires the recorded
human approval, and the artifact keeps the from/to profiles and locks, the
preconditions, the semantic diff, the invariant results and the lineage output so
the decision is reconstructable later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_reality.errors import ProfileError
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.migration import MIGRATION_SCHEMA, MigrationPlan
from wanxiang_reality.profiles import RealityProfile, RuntimeLock, profile_hash
from wanxiang_reality.registry import RealityProfileRegistry


@dataclass(frozen=True, slots=True)
class Approval:
    """Recorded human approval for a major upgrade."""

    approver: str
    approved_on: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.approver:
            raise ProfileError("approval requires a named approver")
        if not self.approved_on:
            raise ProfileError("approval requires the date it was given")


class MigrationSink(Protocol):
    """Writes the outcome of an accepted plan; the only mutating collaborator."""

    def migrate(self, plan: MigrationPlan, target_lock: RuntimeLock) -> str:
        """Move the worldline onto the target profile and lock; return a lineage ref."""
        ...

    def fork(self, plan: MigrationPlan, target_lock: RuntimeLock) -> str:
        """Create a child branch from the pinned head; return its lineage ref."""
        ...


@dataclass(frozen=True, slots=True)
class MigrationArtifact:
    """Persisted record of one evaluated plan and, if any, its application."""

    schema: str
    worldline_id: str
    from_profile_ref: str
    to_profile_ref: str
    from_profile_digest: str
    to_profile_digest: str
    from_lock_digest: str
    to_lock_digest: str
    migration_code_version: str
    recommendation: str
    requires_approval: bool
    approved: bool
    approver: str | None
    preconditions: tuple[str, ...]
    blocked_by: tuple[str, ...]
    drifted_dimensions: tuple[str, ...]
    invariant_failures: tuple[str, ...]
    lineage: tuple[str, ...]

    @property
    def digest(self) -> str:
        return canonical_digest(
            {
                "schema": self.schema,
                "worldline_id": self.worldline_id,
                "from_profile_ref": self.from_profile_ref,
                "to_profile_ref": self.to_profile_ref,
                "from_profile_digest": self.from_profile_digest,
                "to_profile_digest": self.to_profile_digest,
                "from_lock_digest": self.from_lock_digest,
                "to_lock_digest": self.to_lock_digest,
                "migration_code_version": self.migration_code_version,
                "recommendation": self.recommendation,
                "requires_approval": self.requires_approval,
                "approved": self.approved,
                "approver": self.approver,
                "preconditions": list(self.preconditions),
                "blocked_by": list(self.blocked_by),
                "drifted_dimensions": list(self.drifted_dimensions),
                "invariant_failures": list(self.invariant_failures),
                "lineage": list(self.lineage),
            }
        )


@dataclass(frozen=True, slots=True)
class MigrationOutcome:
    """What was executed, if anything."""

    recommendation: str
    executed: bool
    new_lock_digest: str | None
    lineage_ref: str | None
    artifact_digest: str


def _artifact(
    plan: MigrationPlan,
    baseline_profile: RealityProfile,
    target_profile: RealityProfile,
    approval: Approval | None,
    lineage: tuple[str, ...],
) -> MigrationArtifact:
    return MigrationArtifact(
        schema=MIGRATION_SCHEMA,
        worldline_id=plan.worldline_id,
        from_profile_ref=plan.from_profile_ref,
        to_profile_ref=plan.to_profile_ref,
        from_profile_digest=profile_hash(baseline_profile),
        to_profile_digest=profile_hash(target_profile),
        from_lock_digest=plan.from_lock_digest,
        to_lock_digest=plan.to_lock_digest,
        migration_code_version=plan.migration_code_version,
        recommendation=plan.recommendation,
        requires_approval=plan.requires_approval,
        approved=approval is not None,
        approver=approval.approver if approval else None,
        preconditions=tuple(item.name for item in plan.preconditions),
        blocked_by=plan.blocked_by,
        drifted_dimensions=plan.drift.drifted_dimensions,
        invariant_failures=plan.drift.invariant_failures,
        lineage=lineage,
    )


def migrate_worldline(
    plan: MigrationPlan,
    *,
    registry: RealityProfileRegistry,
    sink: MigrationSink,
    baseline_profile: RealityProfile,
    target_profile: RealityProfile,
    target_lock: RuntimeLock,
    approval: Approval | None = None,
) -> MigrationOutcome:
    """Execute an accepted plan, or refuse with the reason.

    Raises:
        ProfileError: when the plan recommends `reject`, when the recorded approval
            is missing for a major upgrade, when the worldline is not pinned to the
            baseline profile, or when the target lock does not belong to the target
            profile.
    """
    if plan.recommendation == "reject":
        raise ProfileError(
            f"migration of {plan.worldline_id} is rejected; failed preconditions: "
            f"{', '.join(plan.blocked_by) or 'semantic drift with broken invariants'}"
        )
    if plan.recommendation == "fork" and plan.drift.invariant_failures:
        raise ProfileError(
            "a fork still requires the declared invariants to hold: "
            f"{', '.join(plan.drift.invariant_failures)}"
        )
    if plan.requires_approval and approval is None:
        raise ProfileError(
            f"major upgrade {plan.from_profile_ref} -> {plan.to_profile_ref} needs recorded "
            "human approval before it can be applied"
        )

    pin = registry.resolve(plan.worldline_id)
    if pin.ref != plan.from_profile_ref:
        raise ProfileError(
            f"worldline {plan.worldline_id} is pinned to {pin.ref}, plan starts from "
            f"{plan.from_profile_ref}"
        )
    expected_target = f"{target_profile.profile_id}@{target_profile.version}"
    if target_lock.reality_profile_ref != expected_target:
        raise ProfileError(
            f"target lock pins {target_lock.reality_profile_ref}, expected {expected_target}"
        )

    approval_ref = f"approved-by:{approval.approver}" if approval else "not-required"
    if plan.recommendation == "migrate":
        sink_ref = sink.migrate(plan, target_lock)
        registry.repin_after_migration(plan.worldline_id, target_profile)
        lineage = (
            f"migrate:{plan.from_profile_ref}->{plan.to_profile_ref}",
            approval_ref,
            sink_ref,
        )
    else:
        sink_ref = sink.fork(plan, target_lock)
        lineage = (
            f"fork:{plan.from_profile_ref}->{plan.to_profile_ref}",
            approval_ref,
            sink_ref,
        )

    artifact = _artifact(plan, baseline_profile, target_profile, approval, lineage)
    return MigrationOutcome(
        recommendation=plan.recommendation,
        executed=True,
        new_lock_digest=target_lock.lock_digest(),
        lineage_ref=sink_ref,
        artifact_digest=artifact.digest,
    )


def dry_run_artifact(
    plan: MigrationPlan,
    baseline_profile: RealityProfile,
    target_profile: RealityProfile,
) -> MigrationArtifact:
    """The artifact for an evaluated-but-not-applied plan."""
    return _artifact(plan, baseline_profile, target_profile, None, ())
