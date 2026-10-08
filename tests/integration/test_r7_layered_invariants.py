"""R7 layered invariant acceptance: Kernel -> Domain -> World, fail closed."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_domain.errors import ConstitutionViolation
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_runtime.invariants import InvariantCheck


def test_domain_invariant_denial_blocks_commit_without_advancing_history() -> None:
    def deny_forbidden_status(_state: object, op: object) -> None:
        if "forbidden-domain" in repr(op):
            raise ConstitutionViolation("domain invariant denied")

    runtime = build_reference_runtime(domain_invariants=(deny_forbidden_status,))
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_domain_invariant"))
    player = ExperiencePlayerService(runtime)
    branch = world.root_branch_id
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_domain_guard", "count": 0},
        "act_guard",
        "cmd_guard_seed",
    )

    with pytest.raises(ConstitutionViolation, match="domain invariant"):
        player.act(
            world.instance_id,
            branch,
            1,
            "set_status",
            {"entity_id": "ent_domain_guard", "status": "forbidden-domain"},
            "act_guard",
            "cmd_guard_denied",
        )

    assert runtime.current_state(world.instance_id, branch).revision.value == 1
    assert len(runtime.events(world.instance_id, branch)) == 1


def test_world_invariant_layer_runs_after_domain_and_before_commit() -> None:
    calls: list[str] = []

    def domain(_state: object, _op: object) -> None:
        calls.append("domain")

    def world(_state: object, op: object) -> None:
        calls.append("world")
        if "world-deny" in repr(op):
            raise ConstitutionViolation("world invariant denied")

    domain_check: InvariantCheck = domain  # type: ignore[assignment]
    world_check: InvariantCheck = world  # type: ignore[assignment]
    runtime = build_reference_runtime(
        domain_invariants=(domain_check,),
        world_invariants=(world_check,),
    )
    created = runtime.create_world(instance_id=WorldInstanceId("wld_r7_world_invariant"))
    player = ExperiencePlayerService(runtime)
    player.act(
        created.instance_id,
        created.root_branch_id,
        0,
        "create_entity",
        {"entity_id": "ent_world_guard", "count": 0},
        "act_guard",
        "cmd_world_guard_seed",
    )
    calls.clear()

    with pytest.raises(ConstitutionViolation, match="world invariant"):
        player.act(
            created.instance_id,
            created.root_branch_id,
            1,
            "set_status",
            {"entity_id": "ent_world_guard", "status": "world-deny"},
            "act_guard",
            "cmd_world_guard_denied",
        )

    assert calls == ["domain", "world"]
    assert len(runtime.events(created.instance_id, created.root_branch_id)) == 1
