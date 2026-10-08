"""G54A: repository truth audit invariants (M51)."""

from __future__ import annotations

import pathlib

import pytest
import scripts.forge_truth_audit as audit

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.mark.architecture
def test_audit_verdict_is_pass_on_current_tree() -> None:
    _inventory, violations = audit.run()
    assert violations == []


@pytest.mark.architecture
def test_forbidden_files_never_tracked() -> None:
    assert audit.forbidden_tracked() == []


@pytest.mark.architecture
def test_restricted_corpus_contains_only_readme_and_manifest() -> None:
    assert audit.corpus_check() == []


@pytest.mark.architecture
def test_no_secret_patterns_in_packages() -> None:
    assert audit.secret_scan() == []


@pytest.mark.architecture
def test_forge_capability_inventory_present() -> None:
    _inventory, _ = audit.run()
    inv = audit.inventory()
    # Foundation Forge modules from 03_SOURCE_ADAPTER_MATRIX / pipeline.
    for module in ("sources", "compiler", "corpus", "worldpack"):
        assert inv.forge_modules[module] > 0
    # Kernel must exist and stay frozen (KEEP, never DELETE).
    assert inv.packages["domain"] > 0
    assert inv.packages["runtime"] > 0
    assert inv.packages["substrate"] > 0
    assert ROOT.joinpath("scripts/architecture_check.py").exists()
    assert ROOT.joinpath("scripts/kernel_guard.py").exists()
