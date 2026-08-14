"""G18B: Studio / World IDE completion.

- Studio can diagnose a failed command and replay/branch state without direct DB access.
- Dangerous admin actions require explicit privilege and are audited.
- No canned world data in the production path (server-truth only).
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_api.studio_service import StudioRequiresAdmin, StudioService
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime


def _cmd(
    iid: WorldInstanceId,
    branch: BranchId,
    revision: int,
    action: str,
    payload: dict[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=iid,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


def test_studio_diagnoses_failed_command_and_replay_without_db(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        _cmd(iid, branch, 0, "create_entity", {"entity_id": "a", "count": 1}, "ok_1")
    )
    # A failed command: no event committed.
    try:  # noqa: SIM105
        runtime.submit_command(_cmd(iid, branch, 1, "no_such_action", {}, "bad_1"))
    except WanxiangError:
        pass
    studio = StudioService(runtime)
    diag = studio.diagnose_command(iid, "bad_1")
    assert diag["committed"] is False
    ok = studio.diagnose_command(iid, "ok_1")
    assert ok["committed"] is True and ok["event_seq"] == 1
    # Replay + branch state through the service (no raw DB).
    replay = studio.branch_replay(iid, branch)
    assert replay["revision"] == 1 and replay["hash"]
    child = runtime.create_branch(iid, branch)
    diff = studio.branch_diff(iid, branch, child.branch_id)
    assert "added" in diff


def test_dangerous_admin_actions_require_privilege_and_are_audited(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    # Non-admin Studio cannot run the debug projection.
    studio = StudioService(runtime, admin=False)
    with pytest.raises(StudioRequiresAdmin):
        studio.debug_projection(iid, branch, "alice")
    # Admin Studio can, and the action is audited.
    admin_studio = StudioService(runtime, admin=True)
    snap = admin_studio.debug_projection(iid, branch, "alice")
    assert snap.mode == "debug"
    actions = {a["action"] for a in admin_studio.audit_log()}
    assert "debug_projection" in actions


def test_studio_composes_from_server_truth_not_canned(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        _cmd(iid, branch, 0, "create_entity", {"entity_id": "studio_thing", "count": 5}, "s1")
    )
    admin_studio = StudioService(runtime, admin=True)
    snap = admin_studio.debug_projection(iid, branch, "any")
    # The projection reflects the committed server state (revision 1, entity present).
    assert snap.revision == 1
    ids = {i.entity_id for i in snap.items}
    assert "studio_thing" in ids
