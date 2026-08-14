"""G31H: lineage graph fixture reproducibility."""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import cast

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "v5_2_lineage_graph.json"
SCRIPT = ROOT / "scripts" / "generate_lineage_fixture.py"


def _load() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.mark.architecture
def test_fixture_regenerates_stably() -> None:
    before = FIXTURE.read_bytes()
    subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, check=True
    )
    after = FIXTURE.read_bytes()
    assert before == after, "lineage fixture is not deterministic"


@pytest.mark.architecture
def test_fixture_hash_matches_content() -> None:
    data = _load()
    expected = hashlib.sha256(
        json.dumps({"nodes": data["nodes"], "edges": data["edges"]}, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert data["hash"] == expected


@pytest.mark.architecture
def test_fixture_is_valid_lineage_dag() -> None:
    from wanxiang_domain.lineage import LineageGraph

    data = _load()
    graph = LineageGraph()
    for raw in cast(list[dict[str, object]], data["nodes"]):
        from wanxiang_domain.lineage import LineageNode

        graph.add_node(LineageNode(node_id=str(raw["node_id"]), kind=raw["kind"]))  # type: ignore[arg-type]
    for raw in cast(list[dict[str, object]], data["edges"]):
        from wanxiang_domain.lineage import LineageEdge

        graph.add_edge(
            LineageEdge(
                parent_node_id=str(raw["parent_node_id"]),
                child_node_id=str(raw["child_node_id"]),
                edge_kind=raw["edge_kind"],  # type: ignore[arg-type]
                origin_ref=cast(str | None, raw.get("origin_ref")),
            )
        )
    assert graph.ancestors("wd_rc_derived") == (
        "wd_sf_root",
        "wl_rc_001",
        "wl_rc_001_exp",
    )  # sorted
    assert graph.descendants("wd_sf_root") == ("wd_rc_derived", "wl_rc_001", "wl_rc_001_exp")
