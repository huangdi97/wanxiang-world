"""Canonical JSON hashing shared by the reality contracts and profiles."""

from __future__ import annotations

import hashlib
import json


def canonical_digest(payload: object) -> str:
    """Return the sha256 hex digest of the canonical JSON encoding of ``payload``.

    Canonical encoding means sorted keys, compact separators and UTF-8 output,
    so logically equal payloads always produce the same digest.
    """
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
