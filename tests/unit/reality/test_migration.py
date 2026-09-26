"""Tests for R7 worldline profile pinning and shadow-replay migration."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from wanxiang_reality.errors import ProfileError
from wanxiang_reality.migration import (
    LockedSnapshot,
    ReplayOutcome,
    compare_replay,
    plan_migration,
)
from wanxiang_reality.migration_apply import (
    Approval,
    MigrationArtifact,
    MigrationOutcome,
    dry_run_artifact,
    migrate_worldline,
)
from wanxiang_reality.profiles import RealityProfile, RuntimeLock, WorldProfile, build_runtime_lock
from wanxiang_reality.registry import RealityProfileRegistry
from wanxiang_reality.versions import Version

SEAM = "wanxiang.history@1"
WORLDLINE = "wl_migration"


def _reality(version: str, *, optional: tuple[str, ...] = ()) -> RealityProfile:
    return RealityProfile(
        profile_id="reality:persistent",
        version=Version.parse(version),
        required_seams=(SEAM,),
        optional_seams=optional,
    )


def _world() -> WorldProfile:
    dimensions: dict[str, str] = dict.fromkeys(
        (
            "actors",
            "capabilities",
            "distribution",
            "experience",
            "memory",
            "projection",
            "simulation",
            "space",
            "time",
        ),
        "declared",
    )
    return WorldProfile(
        profile_id="world:fixture",
        version=Version.parse("1"),
        reality_profile_ref=f"reality:persistent@{Version.parse('1')}",
        providers=("history-memory",),
        dimensions=dimensions,
    )


def _lock(reality: RealityProfile) -> RuntimeLock:
    return build_runtime_lock(
        reality,
        _world(),
        world_id="world_fixture",
        world_instance_id="inst_fixture",
        worldline_id=WORLDLINE,
        composition_runtime="cordis",
        composition_runtime_version="4.0.0-rc.10",
        service_contract_versions={SEAM: "1"},
        provider_versions={"history-memory": "1.0.0"},
        artifact_hashes={"world:fixture": "abc"},
        schema_versions={"storage": "1"},
        migration_lineage=("genesis",),
        runtime_config_hash="cfg",
    )


class FakeReplay:
    """Configurable read-only replay source."""

    def __init__(self, baseline: ReplayOutcome, candidate: ReplayOutcome) -> None:
        self.baseline = baseline
        self.candidate = candidate
        self.replays: list[str] = []

    def snapshot(self, worldline_id: str) -> LockedSnapshot:
        return LockedSnapshot(
            world_id="world_fixture",
            worldline_id=worldline_id,
            revision=7,
            state_hash="hash-7",
            event_count=7,
            profile_ref=f"reality:persistent@{Version.parse('1')}",
            lock_digest="0" * 64,
        )

    def replay(
        self, worldline_id: str, profile: RealityProfile, lock: RuntimeLock
    ) -> ReplayOutcome:
        self.replays.append(str(profile.version))
        return self.candidate if profile.version.major == 2 else self.baseline


def _outcome(
    *,
    state_hash: str = "hash-7",
    entity_ids: tuple[str, ...] = ("ent_a", "ent_b"),
    invariants: Mapping[str, bool] | None = None,
    failed: bool = False,
    failure_reason: str | None = None,
) -> ReplayOutcome:
    """A deterministic replay outcome; every default matches the baseline."""
    return ReplayOutcome(
        world_id="world_fixture",
        worldline_id=WORLDLINE,
        history_head=7,
        state_hash=state_hash,
        entity_ids=entity_ids,
        branch_graph_digest="branch-1",
        lineage_digest="lineage-1",
        rights_evidence_digest="rights-1",
        projection={"status": "calm"},
        invariants=invariants
        if invariants is not None
        else {"commit_authority_exclusive": True, "branch_isolation": True},
        failed=failed,
        failure_reason=failure_reason,
    )


class _Sink:
    def __init__(self) -> None:
        self.migrated: list[str] = []
        self.forked: list[str] = []

    def migrate(self, plan: object, target_lock: RuntimeLock) -> str:
        self.migrated.append(target_lock.worldline_id)
        return "lineage:migrate:1"

    def fork(self, plan: object, target_lock: RuntimeLock) -> str:
        self.forked.append(target_lock.worldline_id)
        return "lineage:fork:1"


def _plan(source: FakeReplay, *, target: str = "2"):
    return plan_migration(
        worldline_id=WORLDLINE,
        baseline_profile=_reality("1"),
        target_profile=_reality(target),
        baseline_lock=_lock(_reality("1")),
        target_lock=_lock(_reality(target)),
        source=source,
        migration_code_version="r7-migration-1",
    )


def test_registry_keeps_v1_and_v2_side_by_side() -> None:
    registry = RealityProfileRegistry()
    registry.register(_reality("1"), default=True)
    registry.register(_reality("2"), default=True)

    assert registry.versions("reality:persistent") == (Version.parse("1"), Version.parse("2"))
    assert registry.default_profile("reality:persistent") == _reality("2")


def test_existing_worldline_stays_pinned_to_v1() -> None:
    registry = RealityProfileRegistry()
    registry.register(_reality("1"))
    registry.register(_reality("2"), default=True)
    pin = registry.pin(WORLDLINE, _reality("1"))

    assert pin.ref == f"reality:persistent@{Version.parse('1')}"
    assert registry.default_profile("reality:persistent") == _reality("2")
    assert registry.resolve(WORLDLINE).version == Version.parse("1")


def test_pinning_an_already_pinned_worldline_is_refused_as_a_silent_hot_swap() -> None:
    registry = RealityProfileRegistry()
    registry.pin(WORLDLINE, _reality("1"))

    with pytest.raises(ProfileError, match="already pinned"):
        registry.pin(WORLDLINE, _reality("2"))


def test_migration_requires_a_major_upgrade() -> None:
    source = FakeReplay(_outcome(), _outcome())

    with pytest.raises(ProfileError, match="not a major upgrade"):
        plan_migration(
            worldline_id=WORLDLINE,
            baseline_profile=_reality("1"),
            target_profile=_reality("1.1"),
            baseline_lock=_lock(_reality("1")),
            target_lock=_lock(_reality("1.1")),
            source=source,
            migration_code_version="r7-migration-1",
        )


def test_plan_rejects_a_lock_that_belongs_to_another_profile() -> None:
    source = FakeReplay(_outcome(), _outcome())

    with pytest.raises(ProfileError, match="runtime lock pins"):
        plan_migration(
            worldline_id=WORLDLINE,
            baseline_profile=_reality("1"),
            target_profile=_reality("2"),
            baseline_lock=_lock(_reality("1")),
            target_lock=_lock(_reality("1")),
            source=source,
            migration_code_version="r7-migration-1",
        )


def test_plan_requires_a_migration_code_version() -> None:
    source = FakeReplay(_outcome(), _outcome())

    with pytest.raises(ProfileError, match="migration_code_version"):
        plan_migration(
            worldline_id=WORLDLINE,
            baseline_profile=_reality("1"),
            target_profile=_reality("2"),
            baseline_lock=_lock(_reality("1")),
            target_lock=_lock(_reality("2")),
            source=source,
            migration_code_version="",
        )


def test_identical_shadow_replay_recommends_migrate() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome()))

    assert plan.recommendation == "migrate"
    assert plan.requires_approval is True
    assert plan.drift.semantic_drift is False
    assert plan.blocked_by == ()


def test_entity_identity_drift_recommends_a_fork_instead_of_in_place_upgrade() -> None:
    drifted = _outcome(entity_ids=("ent_a", "ent_c"))
    plan = _plan(FakeReplay(_outcome(), drifted))

    assert plan.recommendation == "fork"
    assert "entity_identity" in plan.drift.drifted_dimensions


def test_state_hash_drift_recommends_a_fork() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome(state_hash="hash-8")))

    assert plan.recommendation == "fork"
    assert "state_hash" in plan.drift.drifted_dimensions


def test_failed_declared_invariant_rejects_the_migration() -> None:
    candidate = _outcome(invariants={"branch_isolation": False})
    plan = _plan(FakeReplay(_outcome(), candidate))

    assert plan.recommendation == "reject"
    assert "declared_invariants_hold" in plan.blocked_by
    assert plan.drift.invariant_failures == ("branch_isolation",)


def test_failed_shadow_replay_rejects_the_migration() -> None:
    failed = _outcome(failed=True, failure_reason="commit authority unavailable")
    plan = _plan(FakeReplay(_outcome(), failed))

    assert plan.recommendation == "reject"
    assert "replay_integrity" in plan.blocked_by
    assert plan.drift.failure_reason == "commit authority unavailable"


def test_snapshot_from_another_profile_rejects_the_migration() -> None:
    class ForeignSnapshot(FakeReplay):
        def snapshot(self, worldline_id: str) -> LockedSnapshot:
            return LockedSnapshot(
                world_id="world_fixture",
                worldline_id=worldline_id,
                revision=7,
                state_hash="hash-7",
                event_count=7,
                profile_ref=f"reality:persistent@{Version.parse('2')}",
                lock_digest="0" * 64,
            )

    plan = _plan(ForeignSnapshot(_outcome(), _outcome()))

    assert plan.recommendation == "reject"
    assert "snapshot_matches_baseline_profile" in plan.blocked_by


def test_plan_digest_is_stable_and_changes_with_drift() -> None:
    first = _plan(FakeReplay(_outcome(), _outcome()))
    second = _plan(FakeReplay(_outcome(), _outcome()))
    drifted = _plan(FakeReplay(_outcome(), _outcome(state_hash="hash-9")))

    assert first.plan_digest == second.plan_digest
    assert first.plan_digest != drifted.plan_digest


def test_compare_replay_compares_every_declared_dimension() -> None:
    report = compare_replay(_outcome(), _outcome(state_hash="hash-x"))

    dimensions = {entry.dimension for entry in report.entries}
    assert dimensions == {
        "world_identity",
        "entity_identity",
        "history_head",
        "state_hash",
        "normalized_projection",
        "branch_graph",
        "lineage",
        "rights_evidence",
    }
    assert report.drifted_dimensions == ("state_hash",)


def test_applying_a_rejected_plan_is_refused() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome(invariants={"branch_isolation": False})))
    registry = RealityProfileRegistry()
    registry.pin(WORLDLINE, _reality("1"))

    with pytest.raises(ProfileError, match="is rejected"):
        migrate_worldline(
            plan,
            registry=registry,
            sink=_Sink(),
            baseline_profile=_reality("1"),
            target_profile=_reality("2"),
            target_lock=_lock(_reality("2")),
        )


def test_major_upgrade_without_recorded_approval_is_refused() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome()))
    registry = RealityProfileRegistry()
    registry.pin(WORLDLINE, _reality("1"))

    with pytest.raises(ProfileError, match="needs recorded"):
        migrate_worldline(
            plan,
            registry=registry,
            sink=_Sink(),
            baseline_profile=_reality("1"),
            target_profile=_reality("2"),
            target_lock=_lock(_reality("2")),
        )
    assert registry.resolve(WORLDLINE).version == Version.parse("1")


def test_approved_migration_repins_the_worldline_and_records_lineage() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome()))
    registry = RealityProfileRegistry()
    registry.pin(WORLDLINE, _reality("1"))
    sink = _Sink()

    outcome = migrate_worldline(
        plan,
        registry=registry,
        sink=sink,
        baseline_profile=_reality("1"),
        target_profile=_reality("2"),
        target_lock=_lock(_reality("2")),
        approval=Approval(approver="human:tester", approved_on="2026-09-25"),
    )

    assert isinstance(outcome, MigrationOutcome)
    assert outcome.executed is True
    assert outcome.new_lock_digest == _lock(_reality("2")).lock_digest()
    assert sink.migrated == [WORLDLINE]
    assert sink.forked == []
    assert registry.resolve(WORLDLINE).version == Version.parse("2")
    assert outcome.lineage_ref == "lineage:migrate:1"


def test_approved_fork_keeps_the_parent_pin_and_uses_the_fork_path() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome(entity_ids=("ent_a", "ent_c"))))
    registry = RealityProfileRegistry()
    registry.pin(WORLDLINE, _reality("1"))
    sink = _Sink()

    outcome = migrate_worldline(
        plan,
        registry=registry,
        sink=sink,
        baseline_profile=_reality("1"),
        target_profile=_reality("2"),
        target_lock=_lock(_reality("2")),
        approval=Approval(approver="human:tester", approved_on="2026-09-25"),
    )

    assert outcome.recommendation == "fork"
    assert sink.forked == [WORLDLINE]
    assert sink.migrated == []
    assert outcome.lineage_ref == "lineage:fork:1"
    # A fork leaves the parent worldline on its original reality profile.
    assert registry.resolve(WORLDLINE).version == Version.parse("1")


def test_migration_artifact_is_dry_run_until_applied() -> None:
    plan = _plan(FakeReplay(_outcome(), _outcome()))
    artifact = dry_run_artifact(plan, _reality("1"), _reality("2"))

    assert isinstance(artifact, MigrationArtifact)
    assert artifact.approved is False
    assert artifact.approver is None
    assert artifact.lineage == ()
    assert artifact.from_lock_digest == plan.from_lock_digest
    assert artifact.to_lock_digest == plan.to_lock_digest
    assert artifact.digest == artifact.digest
