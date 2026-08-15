"""G38B: kernel v1 ABI manifest + golden fixtures (mechanism)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from wanxiang_substrate.kernel.abi import (
    KERNEL_V1_ABI,
    abi_golden,
    abi_manifest,
    verify_abi_golden,
)

GOLDEN = Path(__file__).resolve().parents[3] / "reports" / "kernel_v1_abi_golden.json"


@pytest.mark.unit
def test_abi_manifest_is_stable() -> None:
    first = abi_manifest()
    second = abi_manifest()
    assert first == second
    assert first.version == 1
    assert len(first.entries) == len(KERNEL_V1_ABI)
    assert first.entry("CommitAuthority") is not None


@pytest.mark.unit
def test_abi_golden_hash_reproducible() -> None:
    assert abi_golden()["golden_hash"] == abi_golden()["golden_hash"]
    assert len(abi_golden()["golden_hash"]) == 64


@pytest.mark.unit
def test_abi_golden_round_trip_and_persistence() -> None:
    golden = abi_golden()
    GOLDEN.write_text(json.dumps(golden, indent=2, sort_keys=True), encoding="utf-8")
    persisted = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert verify_abi_golden(persisted) is True
    # A tampered golden fails verification.
    tampered = dict(persisted)
    tampered["golden_hash"] = "x" * 64
    assert verify_abi_golden(tampered) is False
