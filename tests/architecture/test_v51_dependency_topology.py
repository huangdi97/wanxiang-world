"""G21D: physical package dependency topology acceptance.

Pins the current package dependency edge set (golden) so the topology is
deterministic and any future boundary change is explicit. Also verifies the
mapping document covers the 16-kernel -> physical-package mapping.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "v51_dependency_graph.py"
MAPPING = ROOT / "docs" / "architecture" / "V5_1_PHYSICAL_PACKAGE_MAPPING.md"

# Golden edge set: package -> imported workspace packages (from G21D scan).
GOLDEN_EDGES: dict[str, tuple[str, ...]] = {
    "apps/api": (
        "packages/application",
        "packages/domain",
        "packages/persistence",
        "packages/runtime",
        "packages/substrate",
    ),
    "packages/application": ("packages/domain", "packages/runtime"),
    "packages/domain": (),
    "packages/evidence": (),
    "packages/model_providers": (),
    "packages/observability": (),
    "packages/persistence": ("packages/domain", "packages/runtime"),
    "packages/research": ("packages/domain",),
    "packages/runtime": ("packages/domain",),
    "packages/sdk_ts": (),
    "packages/substrate": ("packages/application", "packages/domain", "packages/runtime"),
}


def _parse_edges(stdout: str) -> dict[str, tuple[str, ...]]:
    edges: dict[str, tuple[str, ...]] = {}
    for line in stdout.splitlines():
        stripped = line.strip()
        if ":" not in stripped:
            continue
        pkg, rest = stripped.split(":", 1)
        if not (pkg.startswith("packages/") or pkg.startswith("apps/")):
            continue
        targets = rest.strip()
        if targets == "(none)":
            edges[pkg] = ()
        else:
            edges[pkg] = tuple(sorted(t.strip() for t in targets.split(",") if t.strip()))
    return edges


def _run() -> str:
    result = subprocess.run(
        [sys.executable, str(SCANNER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@pytest.mark.architecture
def test_dependency_graph_matches_golden() -> None:
    edges = _parse_edges(_run())
    assert edges == GOLDEN_EDGES, f"dependency topology drifted: {edges}"


@pytest.mark.architecture
def test_mapping_document_covers_all_kernels() -> None:
    text = MAPPING.read_text(encoding="utf-8")
    for kernel in (
        "Source/Evidence Kernel",
        "World Compiler",
        "Package/Schema/Dependency Registry",
        "Canonical State Kernel",
        "Living World Substrate",
        "Reality Bridge",
        "Co-Simulation Fabric",
        "Event/Branch/Temporal Kernel",
        "Perception-Belief-Memory",
        "Actor/Org Runtime",
        "Skill-Action-Affordance",
        "Capability & Learning",
        "Opportunity-Challenge-Event",
        "Embodiment/Director/Experiment",
        "World Host/Lifecycle/Multiplayer",
        "Projection/Rendering/Gateway",
    ):
        assert kernel in text, f"mapping document missing kernel {kernel}"
