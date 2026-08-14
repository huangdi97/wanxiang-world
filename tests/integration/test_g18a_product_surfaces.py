"""G18A: product surface information architecture & server-truth contract.

- Changing branch/session context updates surfaces from server truth.
- No surface writes world state outside command APIs.
- Shared types do not drift from OpenAPI/SDK.
"""

from __future__ import annotations

import json
import pathlib

from scripts.product_surface_audit import audit
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def test_branch_context_updates_surfaces_from_server_truth(
    persist_db_path: pathlib.Path,
) -> None:
    """Switching the branch context re-fetches the authoritative server projection."""
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("a1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "root_thing", "count": 1},
            world_time=WorldTime(1),
        )
    )
    child = runtime.create_branch(iid, branch)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("c1"),
            instance_id=iid,
            branch_id=child.branch_id,
            expected_revision=BranchRevision(1),
            action_type="create_entity",
            payload={"entity_id": "child_thing", "count": 1},
            world_time=WorldTime(2),
        )
    )
    # Surface context = server truth per branch.
    root_state = runtime.current_state(iid, branch)
    child_state = runtime.current_state(iid, child.branch_id)
    root_ids = {
        i.entity_id
        for i in ProjectionService(root_state)
        .compose(ProjectionRequest(session_id="s", actor_id="any", branch_id=branch, mode="text"))
        .items
    }
    child_ids = {
        i.entity_id
        for i in ProjectionService(child_state)
        .compose(
            ProjectionRequest(
                session_id="s", actor_id="any", branch_id=child.branch_id, mode="text"
            )
        )
        .items
    }
    assert "root_thing" in root_ids and "child_thing" not in root_ids
    assert "child_thing" in child_ids


def test_no_surface_writes_outside_command_apis() -> None:
    report = audit()
    # No surface writes world state except through the command API: the only
    # write path is the sanctioned `submit(...)` command helper.
    assert report["surface_write_api_candidates"]["violations"] == []
    assert report["surface_write_api_candidates"]["submit_command_path"]
    assert report["routes"]


def test_shared_types_no_drift_from_openapi() -> None:
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    baseline = json.loads((ROOT / "reports/sdk_api_baseline.json").read_text(encoding="utf-8"))
    # The API route set in the SDK baseline matches the contract.
    contract_routes = sorted(
        f"{m.upper()} {path}" for path in contract["paths"] for m in contract["paths"][path]
    )
    assert contract_routes == baseline["api_routes"]
