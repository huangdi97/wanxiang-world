"""G18H: operator/admin/source/rights/evaluation console & M15 qualification.

- All major product faces connect to the same backend truth.
- Privileged operations are server-authorized and audited.
- No major surface relies on placeholder data (all compose from server state).
- Critical E2E flows pass.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_api.operator_console_service import OperatorConsoleService, OperatorRequiresAdmin
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime


def test_privileged_operations_require_admin_and_are_audited(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    _w = runtime.create_world()
    console = OperatorConsoleService(runtime, admin=False)
    with pytest.raises(OperatorRequiresAdmin):
        console.rights_decision("src_1", approved=True)
    admin = OperatorConsoleService(runtime, admin=True)
    assert admin.rights_decision("src_1", approved=True)["approved"] == "True"
    actions = {a["action"] for a in admin.audit_log()}
    assert "rights_decision" in actions


def test_all_surfaces_connect_to_same_backend_truth(persist_db_path: pathlib.Path) -> None:
    from wanxiang_api.experience_player_service import ExperiencePlayerService
    from wanxiang_api.operator_console_service import OperatorConsoleService

    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("e2e_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "shared_truth", "count": 1},
            world_time=WorldTime(1),
        )
    )
    # Player surface + operator console both derive from the SAME runtime state.
    player = ExperiencePlayerService(runtime)
    snap = player.project(iid, branch, "alice")
    assert snap.revision == 1
    console = OperatorConsoleService(runtime, admin=True)
    health = console.health(iid, branch)
    assert health["revision"] == 1 and health["events"] == 1
    assert "shared_truth" in {i.entity_id for i in snap.items}


def test_no_placeholder_data_in_product_surfaces(persist_db_path: pathlib.Path) -> None:
    from wanxiang_api.studio_service import StudioService

    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("real_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "real_entity", "count": 3},
            world_time=WorldTime(1),
        )
    )
    # Studio composes its diagnosis/replay from the real committed stream.
    studio = StudioService(runtime)
    diag = studio.diagnose_command(iid, "real_1")
    assert diag["committed"] is True and diag["event_seq"] == 1
    replay = studio.branch_replay(iid, branch)
    assert replay["revision"] == 1
