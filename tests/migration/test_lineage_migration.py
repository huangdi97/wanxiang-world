"""G31C: Lineage repository + migration compatibility."""

from __future__ import annotations

import os
import pathlib

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from tests.conftest import (
    cleanup_db_file,
    fresh_db_path,
    make_sqlite_engine_and_factory,
    upgrade_db,
)
from tests.helpers.replay_fixture import BRANCH, INSTANCE, build_fixture_events
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_persistence.database import create_engine_for
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_persistence.lineage_repository import LineageRepository, branch_lineage_from_branches
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.lineage import LineageEdge, LineageGraph, LineageNode

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _config() -> Config:
    return Config(str(ROOT / "alembic.ini"))


@pytest.mark.migration
def test_fresh_upgrade_to_head_includes_lineage_tables() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    tables = set(inspect(engine).get_table_names())
    assert {"lineage_nodes", "lineage_edges"} <= tables
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_old_db_upgrade_keeps_branch_history() -> None:
    """Upgrade to 0001, insert events, upgrade to head (0003): replay intact."""
    path = fresh_db_path()
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.upgrade(_config(), "0001_initial")
        factory = sessionmaker(
            bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
        )
        store = SqlAlchemyEventStore(factory)
        for event in build_fixture_events():
            store.append(event)
        command.upgrade(_config(), "head")
    finally:
        os.environ.pop("WANXIANG_DATABASE_URL", None)

    factory2 = sessionmaker(
        bind=create_engine_for(f"sqlite:///{path.as_posix()}"), expire_on_commit=False
    )
    store2 = SqlAlchemyEventStore(factory2)
    final = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(store2.load(INSTANCE, BRANCH))
    assert final.revision.value == 5
    assert (
        final.semantic_hash() == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
    )
    engine = factory2.kw["bind"]
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_downgrade_from_lineage_round_trip() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    os.environ["WANXIANG_DATABASE_URL"] = f"sqlite:///{path.as_posix()}"
    try:
        command.downgrade(_config(), "0002_add_event_seq_index")
    finally:
        os.environ.pop("WANXIANG_DATABASE_URL", None)
    engine = create_engine_for(f"sqlite:///{path.as_posix()}")
    tables = set(inspect(engine).get_table_names())
    assert "lineage_nodes" not in tables
    assert "lineage_edges" not in tables
    assert "events" in tables
    engine.dispose()
    cleanup_db_file(path)


@pytest.mark.migration
def test_lineage_repository_round_trip() -> None:
    path = fresh_db_path()
    upgrade_db(path)
    _engine, factory = make_sqlite_engine_and_factory(path)
    repo = LineageRepository(factory)
    repo.save_node(
        LineageNode(
            node_id="wd_root",
            kind="definition",
            definition_ref="pack://sf-world@1.0.0",
            constitution_version=1,
            domain_version=1,
            runtime_version=1,
            rights_ref="rights:cc0",
            provenance=("ref://a",),
        )
    )
    repo.save_node(
        LineageNode(
            node_id="wl_derived",
            kind="derived_world",
            definition_ref="pack://derived@1.0.0",
            inherited_history_ref="wl_parent:5",
            constitution_version=2,
            domain_version=2,
            runtime_version=2,
            evolution_policy="living_open",
        )
    )
    repo.save_edge(LineageEdge("wd_root", "wl_derived", edge_kind="promotion", origin_ref="cand_1"))
    graph = repo.load_graph()
    assert graph.get_node("wd_root") is not None
    derived = graph.get_node("wl_derived")
    assert derived is not None and derived.evolution_policy == "living_open"
    assert graph.edges()[0].edge_kind == "promotion"
    cleanup_db_file(path)


@pytest.mark.migration
def test_branch_lineage_derived_from_existing_branches() -> None:
    """Branch forks stay in the branches table; lineage derives on demand."""
    from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata

    parent = BranchMetadata(
        branch_id=BranchId("br_parent"),
        instance_id=INSTANCE,
        ancestry=BranchAncestry(),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    child = BranchMetadata(
        branch_id=BranchId("br_child"),
        instance_id=INSTANCE,
        ancestry=BranchAncestry(
            parent_branch_id=BranchId("br_parent"),
            fork_revision=BranchRevision(5),
            fork_event_seq=EventSeq(5),
            fork_snapshot_ref="mem://fork",
        ),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
    )
    graph = LineageGraph()
    graph.add_node(LineageNode(node_id="br_parent", kind="worldline"))
    graph.add_node(LineageNode(node_id="br_child", kind="worldline"))
    branch_lineage_from_branches((parent, child), graph)
    assert graph.edges() and graph.edges()[0].parent_node_id == "br_parent"
    assert graph.edges()[0].child_node_id == "br_child"
