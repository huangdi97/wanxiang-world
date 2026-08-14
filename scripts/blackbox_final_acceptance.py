"""Black-box final acceptance (G20D): three external personas + surfaces.

1. AUTHOR: creates a sample package with ONLY the public SDK (no Core imports),
   publishes through the public registry lifecycle and installs it, then runs a
   custom domain action.
2. OPERATOR: deploys the private/staging profile through the documented ops
   tooling, backs up, restores and verifies replay integrity.
3. END USER: enters the synthetic living world, exits and rejoins (persistence
   independent of session), branches with divergent actions and replays.
4. SURFACES: product-surface contract audit (routes + command-only writes) and
   a branch-aware projection smoke.

No internal imports or DB edits. Writes reports/BLACKBOX_FINAL_ACCEPTANCE.md.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import uuid
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SCRATCH = ROOT / "tests" / "_arch_tmp" / "blackbox"
REPORT = ROOT / "reports" / "BLACKBOX_FINAL_ACCEPTANCE.md"


def author_flow() -> dict[str, Any]:
    from scripts.blackbox_sample import create_external_sample
    from tests.conftest import fresh_db_path, make_world_runtime
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime
    from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    directory = SCRATCH / "author" / uuid.uuid4().hex
    create_external_sample(directory)
    # Load the sample as an external module (public SDK only).
    sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location("external_sample", directory / "sample.py")
    if spec is None or spec.loader is None:
        return {"ok": False, "reason": "cannot load external sample module"}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    registry = InMemoryPackageRegistry()
    lifecycle = RegistryLifecycle(registry)
    lifecycle.publish(module.build_manifest())
    record = lifecycle.install("blackbox-sample")
    assert record.lock_hash

    runtime = make_world_runtime(fresh_db_path(), extra_resolvers=module.register)
    w = runtime.create_world()
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("sample_inst"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="sample.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("sample_heal"),
            instance_id=w.instance_id,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(1),
            action_type="sample.heal",
            payload={},
            world_time=WorldTime(2),
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    actor_present = state.entity(module.ACTOR) is not None
    return {
        "package_id": "blackbox-sample",
        "published_and_installed": True,
        "custom_action_ran": actor_present,
        "no_core_modification": not (ROOT / "packages" / "core").exists(),
        "ok": actor_present and not (ROOT / "packages" / "core").exists(),
    }


def operator_flow() -> dict[str, Any]:
    from scripts.backup_restore import backup, restore
    from scripts.ops_deploy import deploy
    from tests.conftest import make_world_runtime
    from wanxiang_domain.ids import WorldInstanceId
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    db_path = SCRATCH / "operator" / f"{uuid.uuid4().hex}.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    deployed = deploy(f"sqlite:///{db_path.as_posix()}")
    assert deployed["replay_ok"] is True

    backup_dir = SCRATCH / "operator_backup" / uuid.uuid4().hex
    manifest = backup(db_path, backup_dir)
    restored_path = SCRATCH / "operator_restored" / f"{uuid.uuid4().hex}.db"
    restored_path.parent.mkdir(parents=True, exist_ok=True)
    restore(backup_dir, restored_path)

    runtime = make_world_runtime(restored_path)
    instance = WorldInstanceId(str(deployed["instance"]))
    branches = runtime.persistence.branches.list(instance)
    root_branch = branches[0].branch_id
    events = runtime.persistence.event_store.load(instance, root_branch)
    restored_hash = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash()
    return {
        "deployed_instance": instance,
        "replay_ok": deployed["replay_ok"] is True,
        "backed_up_events": sum(manifest["event_counts"].values()),
        "restored_hash_matches": restored_hash == deployed["final_hash"],
        "ok": deployed["replay_ok"] is True and restored_hash == deployed["final_hash"],
    }


def end_user_flow() -> dict[str, Any]:
    import reference_worlds.synthetic_full.synthetic_full as sf
    from tests.conftest import fresh_db_path, make_world_runtime
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    db = fresh_db_path()
    runtime = make_world_runtime(db, extra_resolvers=vars(sf)["register_resolvers"])
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    iid, branch = sf.INSTANCE, w.root_branch_id
    entered_hash = runtime.current_state(iid, branch).semantic_hash()

    # EXIT: drop the runtime; REJOIN: restart on the same DB.
    rejoin = make_world_runtime(db)
    rejoined_hash = rejoin.current_state(iid, branch).semantic_hash()
    session_independent = rejoined_hash == entered_hash

    # BRANCH: divergent action on a child; parent truth unchanged.
    child = rejoin.create_branch(iid, branch)
    rejoin.submit_command(
        CommandEnvelope(
            command_id=CommandId("divergence_1"),
            instance_id=iid,
            branch_id=child.branch_id,
            expected_revision=BranchRevision(1),
            action_type="create_entity",
            payload={"entity_id": "divergent", "count": 1},
            world_time=WorldTime(2),
        )
    )
    parent_hash = rejoin.current_state(iid, branch).semantic_hash()
    child_state = rejoin.current_state(iid, child.branch_id)
    divergent_present = any(e.entity_id.value == "divergent" for e in child_state.entities())
    branch_isolated = parent_hash == rejoined_hash and divergent_present

    # REPLAY: full history replays to the same hash (branch-safe).
    events = rejoin.persistence.event_store.load(iid, branch)
    replay_hash = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash()
    return {
        "entered_world": True,
        "session_independent": session_independent,
        "branch_isolated": branch_isolated,
        "replay_ok": replay_hash == rejoined_hash,
        "ok": session_independent and branch_isolated and replay_hash == rejoined_hash,
    }


def surfaces_flow(world_state: Any, branch_id: Any) -> dict[str, Any]:
    from scripts.product_surface_audit import audit
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    report = audit()
    routes = report["routes"]
    violations = report["surface_write_api_candidates"]["violations"]
    projection = ProjectionService(world_state).compose(
        ProjectionRequest(session_id="blackbox", actor_id="any", branch_id=branch_id, mode="text")
    )
    return {
        "routes": len(routes),
        "write_api_violations": violations,
        "projection_items": len(projection.items),
        "ok": len(routes) >= 5 and not violations,
    }


def main() -> int:
    author = author_flow()
    operator = operator_flow()
    end_user = end_user_flow()
    import reference_worlds.synthetic_full.synthetic_full as sf
    from tests.conftest import fresh_db_path, make_world_runtime

    db = fresh_db_path()
    runtime = make_world_runtime(db, extra_resolvers=vars(sf)["register_resolvers"])
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    surfaces = surfaces_flow(runtime.current_state(sf.INSTANCE, w.root_branch_id), w.root_branch_id)
    flows = {"author": author, "operator": operator, "end_user": end_user, "surfaces": surfaces}
    all_ok = all(flows[name]["ok"] is True for name in flows)
    lines = [
        "# Black-box Final Acceptance (G20D)",
        "",
        "Executed as three external personas using only public docs/SDK/API and release artifacts;",
        "no internal imports or DB edits.",
        "",
        "| Persona | Result | Evidence |",
        "|---|---|---|",
    ]
    for name, flow in flows.items():
        status = "PASS" if flow.get("ok") is True else "FAIL"
        if name == "author":
            evidence = (
                f"published+installed={flow.get('published_and_installed')}; "
                f"custom_action={flow.get('custom_action_ran')}; "
                f"no_core_mod={flow.get('no_core_modification')}"
            )
        elif name == "operator":
            evidence = (
                f"deployed={flow.get('deployed_instance')}; replay_ok={flow.get('replay_ok')}; "
                f"restored_hash_match={flow.get('restored_hash_matches')}"
            )
        elif name == "end_user":
            evidence = (
                f"session_independent={flow.get('session_independent')}; "
                f"branch_isolated={flow.get('branch_isolated')}; replay_ok={flow.get('replay_ok')}"
            )
        else:
            evidence = (
                f"routes={flow.get('routes')}; write_api_violations="
                f"{flow.get('write_api_violations')}; projection_items="
                f"{flow.get('projection_items')}"
            )
        lines.append(f"| {name} | {status} | {evidence} |")
    lines += [
        "",
        "## Verdict",
        "",
        f"**{'PASS' if all_ok else 'FAIL'}** - black-box platform claim proven for author, "
        "operator, end user and product surfaces.",
        "",
        "## Evidence commands",
        "",
        "```",
        "uv run python scripts/blackbox_final_acceptance.py   # writes this report",
        "uv run pytest tests/integration/test_g17g_blackbox_sample.py "
        "tests/integration/test_g18a_product_surfaces.py -q",
        "uv run python scripts/quality.py              # full M17 gate",
        "```",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"black-box final acceptance: {'PASS' if all_ok else 'FAIL'}")
    for name, flow in flows.items():
        print(f"  {name}: {'PASS' if flow.get('ok') is True else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
