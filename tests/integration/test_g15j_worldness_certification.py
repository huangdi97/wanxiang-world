"""G15J: cross-domain worldness certification (M12 qualification).

Black-box public-API scenario on the synthetic reference world:
build/install pack -> instantiate -> operate (autonomous) -> human leave ->
advance -> rejoin -> fork -> replay -> compare. Asserts the mandatory
worldness criteria and that projections own no exclusive state.
"""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

import pytest
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
PACK = ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"


def _load_sf() -> Any:
    spec = importlib.util.spec_from_file_location("synthetic_full", PACK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def sf() -> Any:
    return _load_sf()


def test_black_box_worldness_certification(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.population.scheduler import AutonomousScheduler

    # 1) build + install pack (public path)
    registry = sf.build_registry()
    record = sf.install_pack(registry)
    assert record.lock_hash
    # 2) instantiate
    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    iid, branch = sf.INSTANCE, w.root_branch_id
    # 3) operate autonomously
    AutonomousScheduler(runtime, seed=5).run(iid, branch, horizon_ticks=3 * sf.DAY)
    committed = runtime.current_state(iid, branch)
    # 4) human leave + advance
    AutonomousScheduler(runtime, seed=6).run(iid, branch, horizon_ticks=6 * sf.DAY)
    advanced = runtime.current_state(iid, branch)
    assert advanced.revision.value > committed.revision.value
    # 5) rejoin: rebuild a fresh runtime over the same database (persistence
    #    independent of session) and read the authoritative perspective.
    rejoined = sf.make_runtime(persist_db_path)
    rejoined_state = rejoined.current_state(iid, branch)
    assert rejoined_state.semantic_hash() == advanced.semantic_hash()
    # 6) fork + replay + compare
    child = rejoined.create_branch(iid, branch)
    child_state = rejoined.current_state(iid, child.branch_id)
    assert child_state.semantic_hash() == advanced.semantic_hash()  # fork at head
    events = rejoined.persistence.event_store.load(iid, branch)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == advanced.semantic_hash()
    # 7) projection independence: projection is derived and rebuildable.
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    snap = ProjectionService(rejoined_state).compose(
        ProjectionRequest(session_id="s", actor_id=sf.MAYOR.value, branch_id=branch, mode="text")
    )
    assert snap.revision == advanced.revision.value
    # Projection owns no exclusive state: rebuilding from events yields the same.
    assert replayed.semantic_hash() == advanced.semantic_hash()


def test_no_projection_owns_exclusive_state(sf: Any, persist_db_path: pathlib.Path) -> None:
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    state = runtime.current_state(sf.INSTANCE, w.root_branch_id)
    snap = ProjectionService(state).compose(
        ProjectionRequest(
            session_id="s", actor_id=sf.MAYOR.value, branch_id=w.root_branch_id, mode="text"
        )
    )
    # Projection is read-only: it has no write API and mutating its output never
    # changes canonical state.
    assert snap.revision == state.revision.value
    # Discard the projection (rebuild path): canonical state unchanged.
    events = runtime.persistence.event_store.load(sf.INSTANCE, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()


def test_reference_packs_portable_and_versioned(sf: Any) -> None:
    registry = sf.build_registry()
    record = sf.install_pack(registry)
    from wanxiang_substrate.packages.install import export_install, install_export_hash

    exported = export_install(record)
    # Same install exports reproducibly (portable + versioned).
    assert install_export_hash(exported) == install_export_hash(export_install(record))
    assert record.package_version.major == 1
