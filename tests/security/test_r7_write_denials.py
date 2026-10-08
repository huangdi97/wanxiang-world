"""R7 Gate C runtime denials: a canonical write without the authority's lease fails.

Behaviour-named negative/security tests. They are deterministic and need no
network, no LLM key and no PostgreSQL.
"""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session, sessionmaker
from tests.helpers.leases import lease_for
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, CommandId, EntityId, EventId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_runtime.canonical_write import (
    CanonicalWriteLease,
    CanonicalWriteRejected,
    require_canonical_write_lease,
)
from wanxiang_runtime.ports import InMemoryEventStore

INSTANCE_A = WorldInstanceId("wld_a")
BRANCH_A = BranchId("br_a")
INSTANCE_B = WorldInstanceId("wld_b")
BRANCH_B = BranchId("br_b")


def _event(
    instance_id: WorldInstanceId,
    branch_id: BranchId,
    *,
    seq: int = 1,
    command: str = "cmd_1",
) -> CommittedEvent:
    return CommittedEvent(
        event_id=EventId(f"evt_{seq}"),
        instance_id=instance_id,
        branch_id=branch_id,
        event_seq=EventSeq(seq),
        revision=BranchRevision(seq),
        schema_version=SchemaVersion(1),
        command_id=CommandId(command),
        delta=ProposedWorldDelta(
            operations=(EntityCreate(entity_id=EntityId("ent_1"), entity_type="person"),)
        ),
        world_time=WorldTime(seq),
        rule_version=RuntimeVersion(1),
    )


def test_append_without_a_lease_is_rejected_and_the_store_stays_empty() -> None:
    store = InMemoryEventStore()
    with pytest.raises(CanonicalWriteRejected):
        store.append(_event(INSTANCE_A, BRANCH_A))
    with pytest.raises(CanonicalWriteRejected):
        store.append(_event(INSTANCE_A, BRANCH_A), lease=None)
    assert store.load(INSTANCE_A, BRANCH_A) == ()
    assert store.last_event_seq(INSTANCE_A, BRANCH_A) == EventSeq(0)


def test_hand_built_look_alike_lease_is_rejected() -> None:
    # Identical public fields, but never minted by the authority: the brand check
    # rejects it, so copying the credential's shape grants nothing.
    look_alike = CanonicalWriteLease(
        instance_id=INSTANCE_A,
        branch_id=BRANCH_A,
        issued_at_ms=0,
        audit_ref="forged",
    )
    store = InMemoryEventStore()
    with pytest.raises(CanonicalWriteRejected):
        store.append(_event(INSTANCE_A, BRANCH_A), lease=look_alike)
    assert store.load(INSTANCE_A, BRANCH_A) == ()


def test_lease_minted_for_another_worldline_is_rejected() -> None:
    store = InMemoryEventStore()
    with pytest.raises(CanonicalWriteRejected):
        # Lease minted for (INSTANCE_B, BRANCH_B) presented for INSTANCE_A.
        store.append(_event(INSTANCE_A, BRANCH_A), lease=lease_for(INSTANCE_B, BRANCH_B))
    with pytest.raises(CanonicalWriteRejected):
        # Same instance, different branch: the branch dimension also denies.
        store.append(_event(INSTANCE_A, BRANCH_B), lease=lease_for(INSTANCE_A, BRANCH_A))
    assert store.load(INSTANCE_A, BRANCH_A) == ()
    assert store.load(INSTANCE_A, BRANCH_B) == ()


def test_append_with_a_valid_lease_succeeds() -> None:
    # Positive control: the guard is a check, not an unconditional denial.
    store = InMemoryEventStore()
    store.append(_event(INSTANCE_A, BRANCH_A), lease=lease_for(INSTANCE_A, BRANCH_A))
    assert store.last_event_seq(INSTANCE_A, BRANCH_A) == EventSeq(1)


def test_sqlalchemy_store_refuses_unleased_and_accepts_leased(
    session_factory: sessionmaker[Session],
) -> None:
    store = SqlAlchemyEventStore(session_factory)
    with pytest.raises(CanonicalWriteRejected):
        store.append(_event(INSTANCE_A, BRANCH_A))
    with pytest.raises(CanonicalWriteRejected):
        store.append(_event(INSTANCE_A, BRANCH_A), lease=lease_for(INSTANCE_B, BRANCH_B))
    store.append(_event(INSTANCE_A, BRANCH_A), lease=lease_for(INSTANCE_A, BRANCH_A))
    assert store.last_event_seq(INSTANCE_A, BRANCH_A) == EventSeq(1)


def test_actor_with_only_the_event_port_cannot_append_or_mint() -> None:
    def ordinary_actor_writes_event(port: InMemoryEventStore) -> None:
        # Shaped like an ordinary plugin/actor: the event port is all it receives.
        port.append(_event(INSTANCE_A, BRANCH_A))

    store = InMemoryEventStore()
    with pytest.raises(CanonicalWriteRejected):
        ordinary_actor_writes_event(store)
    assert store.load(INSTANCE_A, BRANCH_A) == ()
    # The port module exposes no minting name: `require_canonical_write_lease` is
    # validation-only (it can only reject), so an actor allowed to import the port
    # surface still has no public runtime name that produces a lease.
    import wanxiang_runtime.ports as ports_module

    assert not hasattr(ports_module, "mint_canonical_write_lease")


def test_cross_worldline_lease_request_is_denied_for_a_look_alike_target() -> None:
    lease = lease_for(INSTANCE_A, BRANCH_A)
    assert require_canonical_write_lease(lease, instance_id=INSTANCE_A, branch_id=BRANCH_A) is lease
    with pytest.raises(CanonicalWriteRejected):
        require_canonical_write_lease(lease, instance_id=INSTANCE_B, branch_id=BRANCH_A)
    with pytest.raises(CanonicalWriteRejected):
        require_canonical_write_lease(lease, instance_id=INSTANCE_A, branch_id=BRANCH_B)


def test_rpc_history_authority_denies_append_without_a_granted_capability() -> None:
    # Driving `wanxiang_reality.rpc.HistoryAuthority` in-process would couple this
    # suite to the concurrently-edited `wanxiang_reality` package, so the denial is
    # asserted at the transport level via its public entry point instead: an append
    # without a granted capability token must raise, exactly as the existing
    # `tests/unit/reality/test_rpc.py` asserts for the wire protocol.
    from wanxiang_reality.rpc import HistoryAuthority, RpcError

    authority = HistoryAuthority()
    authority.register_holder("holder-1", "audit:holder-1")
    with pytest.raises(RpcError):
        authority.append(
            worldline_id="wl_x",
            expected_revision=0,
            events=(),
            capability_token="not-a-granted-token",
        )
    # A granted token is accepted past the capability gate (a revision check
    # follows), proving the denial above is about the credential and not the call.
    token = authority.grant("holder-1")
    with pytest.raises(RpcError) as granted_error:
        authority.append(
            worldline_id="wl_x", expected_revision=0, events=(), capability_token=token
        )
    assert granted_error.value.code != -32002
