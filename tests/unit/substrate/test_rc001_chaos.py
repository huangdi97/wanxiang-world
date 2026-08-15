"""G37D: RC-001 replay / crash / chaos checks (mechanism)."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.rc001 import genesis_delta
from wanxiang_substrate.rc001.chaos import (
    detect_stream_corruption,
    duplicate_command_rejected,
    provider_failure_isolated,
    reconnect_embodiment,
    run_chaos_checks,
    snapshot_restart,
)
from wanxiang_substrate.session.embodiment import EmbodimentController
from wanxiang_substrate.session.model import Session

INSTANCE = WorldInstanceId("wld_rc001")
BRANCH = BranchId("br_rc001")
RULES = RuntimeVersion(1)
SCHEMA = SchemaVersion(1)


def _state() -> InMemoryCanonicalState:
    base = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    return base.apply(genesis_delta())


def _request() -> CommitRequest:
    return CommitRequest(
        command_id=CommandId("cmd_1"),
        instance_id=INSTANCE,
        branch_id=BRANCH,
        expected_revision=BranchRevision(0),
        delta=genesis_delta(),
        world_time=None,  # type: ignore[arg-type]
        rule_version=RULES,
        kind="state",
    )


@pytest.mark.unit
def test_snapshot_restart_preserves_hash() -> None:
    assert snapshot_restart(_state()) is True


@pytest.mark.unit
def test_corrupt_stream_detection() -> None:
    assert detect_stream_corruption(_state(), corrupt=False) is True
    assert detect_stream_corruption(_state(), corrupt=True) is True


@pytest.mark.unit
def test_duplicate_command_rejected() -> None:
    state = InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)

    def factory() -> CommitRequest:
        return _request()

    assert duplicate_command_rejected(authority, state, factory) is True


@pytest.mark.unit
def test_client_reconnect_reacquires_lease() -> None:
    controller = EmbodimentController()
    session = Session(
        session_id="ses_h",
        controller="human",
        instance_id=INSTANCE,
        mode="embody",
        created_seq=0,
    )
    assert reconnect_embodiment(controller, session, "c1", lease_id="lease_1") is True


@pytest.mark.unit
def test_provider_failure_isolation() -> None:
    state = _state()

    def failing() -> None:
        raise ValidationRejected("provider down")

    assert provider_failure_isolated(failing, state) is True


@pytest.mark.unit
def test_aggregate_chaos_report() -> None:
    state = _state()
    report = run_chaos_checks(
        state=state,
        authority=None,
        failing_resolver=lambda: (_ for _ in ()).throw(ValidationRejected("down")),
    )
    assert report.all_passed is True
    names = [c.name for c in report.checks]
    assert "snapshot_restart" in names
    assert "corrupt_stream_detection" in names
    assert "provider_failure_isolation" in names
