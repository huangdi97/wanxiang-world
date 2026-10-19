"""Bounded, deduplicated source co-occurrence clues for scene planning."""

# pyright: reportUnusedFunction=false, reportPrivateUsage=false

from __future__ import annotations

import unicodedata
from typing import cast

from wanxiang_substrate.assets.book_scene_evidence import _object_dict

_UNKNOWN_OWNERS = frozenset(
    {"", "unknown", "none", "n/a", "na", "null", "nil", "anonymous", "-", "?"}
)
_MAX_CONTEXT_LABEL_CHARS = 160
_MAX_CONTEXT_CANDIDATES = 8


def _place_identity(value: str) -> str:
    """Unicode-normalized, case-insensitive key for source place names."""
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def _context_identity(value: str) -> str:
    kind, _, label = value.partition(":")
    return f"{kind}:{_place_identity(label)}"


def _context_candidates(rows: list[dict[str, object]]) -> list[str]:
    """Collect bounded clues, excluding objects with a concrete owner."""
    candidates: list[str] = []
    for row in rows:
        raw_context = row.get("cooccurring_candidates", [])
        if not isinstance(raw_context, list):
            continue
        for raw_item in cast(list[object], raw_context):
            item = _object_dict(raw_item)
            if item is None:
                continue
            kind, label = item.get("kind"), item.get("label")
            actor = item.get("actor")
            if (
                kind == "object"
                and isinstance(actor, str)
                and actor.strip().casefold() not in _UNKNOWN_OWNERS
            ):
                continue
            if isinstance(kind, str) and isinstance(label, str):
                bounded_label = label.strip()[:_MAX_CONTEXT_LABEL_CHARS]
                if bounded_label:
                    candidates.append(f"{kind}:{bounded_label}")
    by_identity: dict[str, str] = {}
    for item in candidates:
        by_identity.setdefault(_context_identity(item), item)
    return list(by_identity.values())[:_MAX_CONTEXT_CANDIDATES]
