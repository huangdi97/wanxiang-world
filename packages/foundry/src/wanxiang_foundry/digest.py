"""Canonical JSON hashing and digest-shape checks shared by the foundry.

Every foundry digest is the sha256 of the canonical JSON form of its fields
(sorted keys, compact separators, UTF-8, non-ASCII preserved) so equal values
always yield equal digests and any field change changes the digest.

This module is pure and raises no typed foundry error, so every value object can
wrap these results in the error appropriate to its own stage.
"""

from __future__ import annotations

import hashlib
import json
import re

_HEX_DIGEST_RE = re.compile(r"[0-9a-f]{64}")


def canonical_sha256(payload: object) -> str:
    """Return the lowercase hex sha256 of the canonical JSON form of payload."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_hex_digest(value: str) -> bool:
    """Return True when value is a 64-character lowercase hex sha256 digest."""
    return _HEX_DIGEST_RE.fullmatch(value) is not None
