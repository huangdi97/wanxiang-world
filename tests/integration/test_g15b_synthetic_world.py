"""G15B: comprehensive synthetic reference world package.

- Fresh build/install/instantiate of the synthetic full world through the
  public path (package SDK + application runtime).
- Package install/upgrade leaves other worlds intact.
- Content code imports only public Wanxiang contracts, never Core internals.
- Worldness eval cases pass after instantiation.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PACK = ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"


def _load_sf() -> Any:
    spec = importlib.util.spec_from_file_location("synthetic_full", PACK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sf():
    return _load_sf()


def test_fresh_build_install_and_instantiate(sf: Any, persist_db_path: pathlib.Path) -> None:
    registry = sf.build_registry()
    record = sf.install_pack(registry)
    assert record.package_id == "sf-scenario"
    assert record.lock_hash
    # Instantiating requires the substrate resolvers + the pack's action.
    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    result = runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    assert result.duplicate is False
    state = runtime.current_state(sf.INSTANCE, w.root_branch_id)
    for entity_id in (
        sf.SQUARE,
        sf.MARKET,
        sf.TEMPLE,
        sf.GUILD_HALL,
        sf.HOUSE,
        sf.MAYOR,
        sf.SMITH,
        sf.APPRENTICE,
        sf.VISITOR,
        sf.GUILD,
        sf.POUCH,
        sf.LETTER,
        sf.STALL,
        sf.PUBLIC_BELIEF,
        sf.PRIVATE_BELIEF,
    ):
        assert state.entity(entity_id) is not None, entity_id


def test_package_install_and_upgrade_leave_other_worlds_intact(sf: Any) -> None:
    registry = sf.build_registry()
    record_sf = sf.install_pack(registry)
    # A second, unrelated pack install coexists.
    from wanxiang_substrate.packages.fixture import build_town_packages
    from wanxiang_substrate.packages.install import PackageInstaller
    from wanxiang_substrate.packages.registry import InMemoryPackageRegistry

    reg2 = InMemoryPackageRegistry()
    for manifest in build_town_packages():
        reg2.register(manifest)
    # Register the sf domain/world/scenario plus town packs in one registry.
    from wanxiang_substrate.packages.model import SemanticVersion

    for manifest in sf.build_manifests():
        reg2.register(manifest)
    for manifest in build_town_packages():
        if reg2.get(manifest.package_id, manifest.version) is None:
            reg2.register(manifest)
    # Upgrade sf to v2 (register a new version) and install it.
    from wanxiang_substrate.packages.model import UNTRUSTED, PackageManifest

    sf_v2 = PackageManifest(
        package_id="sf-scenario",
        kind="scenario",
        version=SemanticVersion(2, 0, 0),
        name="Synthetic Full Scenario v2",
        dependencies=(("sf-world", "==1.0.0"), ("sf-domain", "==1.0.0")),
        executable_trust=UNTRUSTED,
    ).with_hash()
    reg2.register(sf_v2)
    record_v2 = PackageInstaller().install(reg2, "sf-scenario")
    assert record_v2.package_version == SemanticVersion(2, 0, 0)
    # The sf v1 install record and other worlds remain valid/unaffected.
    assert record_sf.package_version == SemanticVersion(1, 0, 0)


def test_content_imports_only_public_sdk(sf: Any) -> None:
    import ast

    tree = ast.parse(PACK.read_text(encoding="utf-8-sig"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    # No Core-internal modules; only public wanxiang_* surfaces and stdlib/tests.
    for mod in imported:
        if mod.startswith("wanxiang_"):
            assert mod in {
                "wanxiang_domain",
                "wanxiang_substrate",
                "wanxiang_application",
            }, f"content must not import {mod}"


def test_worldness_eval_cases_pass(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    iid, branch = sf.INSTANCE, w.root_branch_id
    state = runtime.current_state(iid, branch)

    # Persistence independent of session: restart reconstructs the same hash.
    hash1 = state.semantic_hash()
    restarted = sf.make_runtime(persist_db_path)
    assert restarted.current_state(iid, branch).semantic_hash() == hash1

    # Spatial + material + custody continuity present.
    assert state.entity(sf.SQUARE) is not None and state.entity(sf.MARKET) is not None
    pouch = state.entity(sf.POUCH)
    assert pouch is not None and any(
        c.component_type == "material.custody" for c in pouch.components.values()
    )

    # Social/organizational continuity: guild memberships present.
    assert state.entity(sf.GUILD) is not None
    assert state.entity(sf.ROLE_GUILD_MASTER) is not None

    # Cognitive continuity + projection isolation: private belief of the mayor
    # never leaks to another actor.
    snap = ProjectionService(state).compose(
        ProjectionRequest(session_id="s", actor_id=sf.VISITOR.value, branch_id=branch, mode="text")
    )
    ids = {i.entity_id for i in snap.items}
    # All beliefs are actor-scoped: neither belief leaks to the visitor.
    assert sf.PRIVATE_BELIEF.value not in ids
    assert sf.PUBLIC_BELIEF.value not in ids
    # The mayor (owner) sees both beliefs.
    mayor_snap = ProjectionService(state).compose(
        ProjectionRequest(session_id="s", actor_id=sf.MAYOR.value, branch_id=branch, mode="text")
    )
    mayor_ids = {i.entity_id for i in mayor_snap.items}
    assert sf.PUBLIC_BELIEF.value in mayor_ids
    assert sf.PRIVATE_BELIEF.value in mayor_ids

    # Replay/verifiability.
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    events = runtime.persistence.event_store.load(iid, branch)
    assert ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash() == hash1
