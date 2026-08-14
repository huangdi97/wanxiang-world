"""Generate the deterministic lineage graph fixture + visualization (G31H).

Writes:
  tests/fixtures/v5_2_lineage_graph.json  (nodes/edges primitives + hash)
  reports/V5_2_LINEAGE_GRAPH.md           (mermaid diagram + tables)

Run from the repository root:
    uv run python scripts/generate_lineage_fixture.py
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wanxiang_domain.lineage import LineageEdge, LineageGraph, LineageNode  # noqa: E402


def build_graph() -> LineageGraph:
    graph = LineageGraph()
    graph.add_node(
        LineageNode(node_id="wd_sf_root", kind="definition", definition_ref="pack://sf-world@1.0.0")
    )
    graph.add_node(
        LineageNode(
            node_id="wl_rc_001",
            kind="worldline",
            definition_ref="pack://redchamber@1.0.0",
            constitution_version=2,
            evolution_policy="canonical_replay",
        )
    )
    graph.add_node(
        LineageNode(
            node_id="wl_rc_001_exp",
            kind="worldline",
            definition_ref="pack://redchamber@1.0.0",
            inherited_history_ref="wl_rc_001:120",
            evolution_policy="living_open",
        )
    )
    graph.add_node(
        LineageNode(
            node_id="wd_rc_derived",
            kind="derived_world",
            definition_ref="pack://redchamber-derived@1.0.0",
            inherited_history_ref="wl_rc_001_exp:240",
            rights_ref="rights:cc0",
        )
    )
    graph.add_edge(LineageEdge("wd_sf_root", "wl_rc_001", edge_kind="fork"))
    graph.add_edge(LineageEdge("wl_rc_001", "wl_rc_001_exp", edge_kind="fork"))
    graph.add_edge(
        LineageEdge(
            "wl_rc_001_exp", "wd_rc_derived", edge_kind="promotion", origin_ref="cand_rc_001"
        )
    )
    return graph


def main() -> int:
    graph = build_graph()
    payload = {
        "kind": "V5_2_LINEAGE_GRAPH_FIXTURE",
        "nodes": [n.to_primitive() for n in graph.nodes()],
        "edges": [e.to_primitive() for e in graph.edges()],
        "common_ancestors": {
            "wd_rc_derived": list(graph.common_ancestors("wl_rc_001", "wd_rc_derived"))
        },
        "hash": hashlib.sha256(
            json.dumps(
                {
                    "nodes": [n.to_primitive() for n in graph.nodes()],
                    "edges": [e.to_primitive() for e in graph.edges()],
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest(),
    }
    target = ROOT / "tests" / "fixtures" / "v5_2_lineage_graph.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# V5.2 Lineage Graph Visualization (G31H)",
        "",
        "Deterministic lineage DAG over world definitions / worldlines / derived worlds.",
        "",
        "```mermaid",
        "graph TD",
        '    wd_sf_root["wd_sf_root (definition)"]',
        '    wl_rc_001["wl_rc_001 (worldline, canonical_replay)"]',
        '    wl_rc_001_exp["wl_rc_001_exp (worldline, living_open)"]',
        '    wd_rc_derived["wd_rc_derived (derived_world)"]',
        "    wd_sf_root -->|fork| wl_rc_001",
        "    wl_rc_001 -->|fork| wl_rc_001_exp",
        "    wl_rc_001_exp -->|promotion cand_rc_001| wd_rc_derived",
        "```",
        "",
        "| Node | Kind | Constitution | Evolution policy |",
        "|---|---|---|---|",
    ]
    for node in graph.nodes():
        lines.append(
            f"| {node.node_id} | {node.kind} | {node.constitution_version} |"
            f"{node.evolution_policy} |"
        )
    lines += [
        "",
        "| Edge | Kind | Origin |",
        "|---|---|---|",
    ]
    for edge in graph.edges():
        lines.append(
            f"| {edge.parent_node_id} -> {edge.child_node_id} | {edge.edge_kind} |"
            f" {edge.origin_ref or ''} |"
        )
    lines += ["", f"Fixture: `tests/fixtures/v5_2_lineage_graph.json` (hash {payload['hash']})", ""]
    (ROOT / "reports" / "V5_2_LINEAGE_GRAPH.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote fixture + visualization (nodes={len(graph.nodes())} edges={len(graph.edges())})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
