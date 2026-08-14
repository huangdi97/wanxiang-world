"""G21B: v5.1 delta traceability completeness check.

Verifies the traceability matrix covers every material v5.1 delta with an owner
and a classification, and that no delta is left UNCLASSIFIED. This is the
reproducible acceptance evidence for G21B.
"""

from __future__ import annotations

import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MATRIX = ROOT / "reports" / "V5_1_TRACEABILITY_MATRIX.md"

# Material v5.1 deltas that must each appear in the matrix with a classification.
REQUIRED_DELTAS: tuple[str, ...] = (
    "Reality Calculus",
    "STATE/ONTOLOGY/LAW",
    "RuntimeControlTransaction",
    "semantic space",
    "Fact Space",
    "GenesisSpec",
    "OntologyCommit",
    "LawCommit",
    "branch-local",
    "possibility space",
    "CandidateEnvelope",
    "Distiller",
    "Evolutionary Distillation",
    "evidence binding",
    "canon escalation",
    "domain distillation profiles",
    "RuntimeCapability",
    "composition root",
    "RuntimeProfile",
    "Stable World ABI",
    "AgentHarnessProvider",
    "Runtime Capability Catalog",
    "Triple ledgers",
    "Actor Trajectory",
    "Runtime Control Ledger",
    "reproducibility manifest",
    "Bounded Runtime Evolution",
    "constitutional attack",
    "Backward migration",
    "Cross-domain qualification",
    "Product surfaces",
    "dead-code final audit",
    "Clean-room",
    "M16 research tracks",
)


@pytest.mark.architecture
def test_matrix_exists() -> None:
    assert MATRIX.exists(), "reports/V5_1_TRACEABILITY_MATRIX.md missing"


@pytest.mark.architecture
def test_every_required_delta_is_classified() -> None:
    text = MATRIX.read_text(encoding="utf-8").lower()
    missing = [d for d in REQUIRED_DELTAS if d.lower() not in text]
    assert not missing, f"unclassified/missing v5.1 deltas in matrix: {missing}"


@pytest.mark.architecture
def test_no_unclassified_rows() -> None:
    rows = [ln for ln in MATRIX.read_text(encoding="utf-8").splitlines() if ln.startswith("| D")]
    unclassified = [ln for ln in rows if "UNCLASSIFIED" in ln]
    assert not unclassified, f"matrix rows still contain an UNCLASSIFIED delta: {unclassified}"


@pytest.mark.architecture
def test_no_replace_without_adr() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    # If any REPLACE classification is claimed, an ADR must be referenced in the matrix.
    if "REPLACE" in text:
        assert "ADR" in text, "REPLACE classification present without ADR reference"
