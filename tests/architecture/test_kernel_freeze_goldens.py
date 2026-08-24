"""G54B: kernel freeze goldens reproducibility + guards (M51)."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "reports" / "kernel_freeze_golden.json"
ABI_GOLDEN = ROOT / "reports" / "kernel_v1_abi_golden.json"
GENERATOR = ROOT / "scripts" / "generate_kernel_freeze_golden.py"


def _load() -> dict[str, object]:
    from typing import cast

    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return cast(dict[str, object], data)


@pytest.mark.architecture
def test_golden_regenerates_stably() -> None:
    before = GOLDEN.read_bytes()
    subprocess.run(
        [sys.executable, str(GENERATOR)], cwd=ROOT, capture_output=True, text=True, check=True
    )
    after = GOLDEN.read_bytes()
    assert before == after, "kernel freeze golden is not deterministic"


@pytest.mark.architecture
def test_replay_and_branch_goldens_reproduce() -> None:
    import scripts.generate_kernel_freeze_golden as gen

    current = gen.build_golden()
    golden = _load()
    assert current["replay_final_state_hash"] == golden["replay_final_state_hash"]
    assert current["branch_fork"] == golden["branch_fork"]
    assert current["event_hashes"] == golden["event_hashes"]
    assert current["worldline"] == golden["worldline"]
    assert current["package"] == golden["package"]
    assert current["combined"] == golden["combined"]


@pytest.mark.architecture
def test_branch_fork_is_isolated_from_parent() -> None:
    from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
    from wanxiang_runtime.replay import ReplayEngine

    events = build_fixture_events()
    parent = ReplayEngine(RULES, SCHEMA).replay(events[:2])
    full = ReplayEngine(RULES, SCHEMA).replay(events)
    assert parent.semantic_hash() != full.semantic_hash()
    golden = _load()
    fork = golden["branch_fork"]
    assert isinstance(fork, dict)
    assert fork["parent_state_hash_unchanged"] == parent.semantic_hash()


@pytest.mark.architecture
def test_kernel_abi_golden_matches_committed_golden() -> None:
    from wanxiang_substrate.kernel.abi import abi_golden

    committed = json.loads(ABI_GOLDEN.read_text(encoding="utf-8"))
    assert committed["golden_hash"] == abi_golden()["golden_hash"]
    assert committed == abi_golden()


@pytest.mark.architecture
def test_kernel_guard_passes_on_current_tree() -> None:
    import scripts.kernel_guard as guard

    assert guard.run() == ()
