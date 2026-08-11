"""Deterministic canonical serialization and semantic hashing.

Semantic hashing excludes explicitly non-semantic fields (wall-clock
timestamps, trace/audit ids, debug labels). Keys are sorted recursively so
equivalent payloads hash identically regardless of insertion order.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, cast

NON_SEMANTIC_KEYS = frozenset(
    {
        "commit_timestamp",
        "trace_id",
        "created_at",
        "wall_clock",
        "audit_note",
    }
)


def _canonical(value: object) -> object:
    if isinstance(value, dict):
        mapping = cast(dict[str, object], value)
        return {
            str(key): _canonical(item)
            for key, item in sorted(mapping.items())
            if str(key) not in NON_SEMANTIC_KEYS
        }
    if isinstance(value, (list, tuple)):
        items = cast(list[object] | tuple[object, ...], value)
        return [_canonical(item) for item in items]
    return value


def canonical_json(*payloads: object) -> str:
    """Stable JSON encoding of payloads with sorted keys and no non-semantic fields."""
    items: list[object] = [_canonical(p) for p in payloads]
    return json.dumps(
        items,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def semantic_sha256(*payloads: Any) -> str:
    """Deterministic SHA-256 over canonical payloads."""
    return hashlib.sha256(canonical_json(*payloads).encode("utf-8")).hexdigest()
