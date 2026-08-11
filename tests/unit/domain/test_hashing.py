"""GOAL_01A: semantic hashing determinism and wall-clock exclusion."""

from __future__ import annotations

import pytest
from wanxiang_domain.hashing import canonical_json, semantic_sha256


@pytest.mark.unit
def test_canonical_json_sorts_keys() -> None:
    a = canonical_json({"b": 1, "a": 2})
    b = canonical_json({"a": 2, "b": 1})
    assert a == b


@pytest.mark.unit
def test_semantic_hash_ignores_wall_clock_and_audit_fields() -> None:
    left = semantic_sha256({"count": 3, "commit_timestamp": "2026-01-01", "trace_id": "x"})
    right = semantic_sha256({"count": 3, "commit_timestamp": "2026-06-01", "trace_id": "y"})
    assert left == right


@pytest.mark.unit
def test_semantic_hash_differs_for_different_state() -> None:
    assert semantic_sha256({"count": 3}) != semantic_sha256({"count": 4})


@pytest.mark.unit
def test_semantic_hash_stable_across_calls() -> None:
    payload = {"entities": [{"id": "ent_a", "count": 5}]}
    assert semantic_sha256(payload) == semantic_sha256(payload)
