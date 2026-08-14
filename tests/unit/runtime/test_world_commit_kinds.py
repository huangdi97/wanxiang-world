"""G30F: three World Commit kinds + Runtime Control isolation."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import BRANCH, INSTANCE, RULES, SCHEMA
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.world_commit import (
    DELTA_SCHEMA_VERSION,
    WORLD_COMMIT_KINDS,
    validate_world_commit_kind,
)
from wanxiang_runtime.authority import CommitAuthority, CommitRequest
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.capability.runtime_control import (
    RuntimeControlLedger,
    RuntimeControlTransaction,
)


def _base_state() -> InMemoryCanonicalState:
    return InMemoryCanonicalState(
        instance_id=INSTANCE,
        branch_id=BRANCH,
        revision=BranchRevision(0),
        schema_version=SCHEMA,
        rule_version=RULES,
    )


def _delta() -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(EntityCreate(entity_id=EntityId("alice"), entity_type="person"),)
    )


@pytest.mark.unit
def test_world_commit_kinds_are_exactly_three() -> None:
    assert WORLD_COMMIT_KINDS == ("state", "ontology", "law")
    assert DELTA_SCHEMA_VERSION == 1
    assert validate_world_commit_kind("state") == "state"
    assert validate_world_commit_kind("ontology") == "ontology"
    assert validate_world_commit_kind("law") == "law"
    with pytest.raises(ContractError):
        validate_world_commit_kind("capability")


@pytest.mark.unit
def test_state_ontology_law_commits_all_pass_single_pipeline() -> None:
    for index, kind in enumerate(WORLD_COMMIT_KINDS, start=1):
        store = InMemoryEventStore()
        authority = CommitAuthority(store, RULES, SCHEMA)
        state = _base_state()
        result = authority.commit(
            state,
            CommitRequest(
                command_id=CommandId(f"cmd_{kind}"),
                instance_id=INSTANCE,
                branch_id=BRANCH,
                expected_revision=BranchRevision(0),
                delta=_delta(),
                world_time=WorldTime(index),
                rule_version=RULES,
                kind=kind,
            ),
        )
        assert result.audit.kind == kind
        assert result.audit.delta_schema_version == DELTA_SCHEMA_VERSION
        assert len(store.load(INSTANCE, BRANCH)) == 1  # one event stream


@pytest.mark.unit
def test_capability_kind_is_rejected_with_no_mutation() -> None:
    store = InMemoryEventStore()
    authority = CommitAuthority(store, RULES, SCHEMA)
    state = _base_state()
    with pytest.raises(ContractError):
        authority.commit(
            state,
            CommitRequest(
                command_id=CommandId("cmd_cap"),
                instance_id=INSTANCE,
                branch_id=BRANCH,
                expected_revision=BranchRevision(0),
                delta=_delta(),
                world_time=WorldTime(1),
                rule_version=RULES,
                kind="capability",  # type: ignore[arg-type]
            ),
        )
    assert store.load(INSTANCE, BRANCH) == ()
    assert state.revision == BranchRevision(0)


@pytest.mark.unit
def test_runtime_control_transaction_is_not_a_world_commit() -> None:
    event_store = InMemoryEventStore()
    ledger = RuntimeControlLedger()
    tx = RuntimeControlTransaction(
        transaction_id="tx_1",
        operation="activate",
        provider_id="provider.deepseek",
        capability_name="actor_policy",
        version="1.0.0",
        rationale="enable deterministic policy provider",
        created_at="2026-08-15T00:00:00Z",
    )
    ledger.record(tx)
    # The runtime control change lands ONLY in the runtime control ledger.
    assert len(ledger.entries()) == 1
    assert event_store.load(INSTANCE, BRANCH) == ()
    # A capability activate never produces a World Commit / committed event.
    assert not hasattr(tx, "event_id")
    assert not hasattr(tx, "revision")


@pytest.mark.unit
def test_runtime_control_ledger_is_append_only() -> None:
    ledger = RuntimeControlLedger()
    for i in range(3):
        ledger.record(
            RuntimeControlTransaction(
                transaction_id=f"tx_{i}",
                operation="install",
                provider_id=f"provider.{i}",
                capability_name="cap",
                version="1.0.0",
                rationale="install",
                created_at=f"2026-08-15T00:00:{i:02d}Z",
            )
        )
    entries = ledger.entries()
    assert len(entries) == 3
    assert [e.transaction_id for e in entries] == ["tx_0", "tx_1", "tx_2"]
