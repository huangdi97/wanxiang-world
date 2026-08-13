"""G05A-G05C: world host boundary, sessions, embodiment leases and handoff."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.host.errors import (
    HostNotFound,
    HostNotRunning,
    InvalidHostTransition,
)
from wanxiang_substrate.host.host import HostRegistry, WorldHost
from wanxiang_substrate.session.control import ControlHandoff, ShadowPolicy
from wanxiang_substrate.session.errors import (
    LeaseConflict,
    ShadowCannotCommit,
)
from wanxiang_substrate.session.service import LeaseService, SessionService
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_host")
TOWN = EntityId("town")
ALICE = EntityId("alice")


def make_host_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("host.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),
        )
    )


def _cmd(
    branch: BranchId, revision: int, action: str, payload: Mapping[str, FieldValue]
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(f"cmd_{action.replace('.', '_')}_{revision}"),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def host_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_host_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_host_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="host.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_host_is_orchestration_boundary(
    host_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = host_world
    host = WorldHost(runtime, INSTANCE, w.root_branch_id)
    before = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
    host.submit(
        _cmd(w.root_branch_id, before, "create_entity", {"entity_id": "x", "entity_type": "thing"})
    )
    after = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
    assert after == before + 1  # committed through the authoritative path only


@pytest.mark.integration
def test_host_lifecycle_and_registry(
    host_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = host_world
    host = WorldHost(runtime, INSTANCE, w.root_branch_id)
    registry = HostRegistry()
    registry.register(host)
    assert registry.require(INSTANCE) is host
    assert registry.get(WorldInstanceId("wld_missing")) is None
    with pytest.raises(HostNotFound):
        registry.require(WorldInstanceId("wld_missing"))
    host.pause()
    with pytest.raises(HostNotRunning):
        host.submit(_cmd(w.root_branch_id, 2, "create_entity", {}))
    host.resume()
    host.stop()
    with pytest.raises(HostNotRunning):
        host.submit(_cmd(w.root_branch_id, 2, "create_entity", {}))
    with pytest.raises(InvalidHostTransition):
        host.stop()  # stopped cannot stop again


@pytest.mark.integration
def test_one_primary_controller_per_actor() -> None:
    sessions = SessionService()
    alice_session = sessions.create("s1", "human-a", INSTANCE, "embody", 1)
    bob_session = sessions.create("s2", "human-b", INSTANCE, "observe", 2)
    leases = LeaseService()
    first = leases.acquire(alice_session, ALICE.value, "lease_1", 1, 100)
    assert first.active is True
    # A second session cannot embody the same actor while the lease is active.
    with pytest.raises(LeaseConflict):
        leases.acquire(bob_session, ALICE.value, "lease_2", 3, 100)
    # An observe-mode session cannot embody at all.
    with pytest.raises(LeaseConflict):
        leases.acquire(bob_session, "bob", "lease_3", 3, 100)
    assert leases.primary_controller(ALICE.value) == "s1"
    leases.release("lease_1", 50)
    assert leases.primary_controller(ALICE.value) is None
    # Now another embody-mode session can take over.
    carol_session = sessions.create("s3", "human-c", INSTANCE, "embody", 3)
    second = leases.acquire(carol_session, ALICE.value, "lease_2", 51, 200)
    assert second.active is True


@pytest.mark.unit
def test_lease_expire_releases_controller() -> None:
    sessions = SessionService()
    session = sessions.create("s9", "human-c", INSTANCE, "embody", 1)
    leases = LeaseService()
    leases.acquire(session, "carl", "lease_9", 1, 100)
    leases.expire("lease_9")
    assert leases.primary_controller("carl") is None


@pytest.mark.unit
def test_shadow_policy_is_advice_only() -> None:
    shadow = ShadowPolicy()
    history = shadow.advise(ALICE.value, "suggest moving to town", advice_seq=1)
    assert history == ("advice:1:suggest moving to town",)
    # Shadow can never commit canonical actions.
    with pytest.raises(ShadowCannotCommit):
        shadow.commit(actor_id=ALICE.value)


@pytest.mark.integration
def test_control_handoff_cycle_and_shadow_isolation() -> None:
    handoff = ControlHandoff()
    autonomous = handoff.state(ALICE.value)
    assert autonomous.state == "autonomous"
    shadow = ShadowPolicy()
    # Shadow advice during autonomous does not change control.
    shadow.advise(ALICE.value, "advice while autonomous", advice_seq=1)
    assert handoff.state(ALICE.value).state == "autonomous"
    # Human acquires control.
    controlled = handoff.acquire(ALICE.value, "s_human", resume_ref="ref://resume")
    assert controlled.state == "human_control"
    assert controlled.controller_session == "s_human"
    # Shadow advice exists but never becomes authoritative control.
    shadow.advise(ALICE.value, "advice while human controls", advice_seq=2)
    assert handoff.state(ALICE.value).controller_session == "s_human"
    # Hand back and resume the deterministic controller.
    handoff.hand_back(ALICE.value, last_commit_seq=10)
    resumed = handoff.resume(ALICE.value)
    assert resumed.state == "autonomous"
    assert resumed.controller_session is None
    assert resumed.resume_ref == "ref://resume"
