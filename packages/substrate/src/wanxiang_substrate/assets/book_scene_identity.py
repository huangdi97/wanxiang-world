"""Stable identity for source-derived scene candidates."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import hashlib
import json


def _source_scene_key(source_digest: str, place_name: str) -> str:
    payload = json.dumps((source_digest, place_name), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]
