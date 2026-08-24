"""Incremental package rebuild (G60D).

Rebuilds only sections whose content hash changed since the previous package;
a draft revision change forces a full rebuild. Deterministic and idempotent.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RebuildResult:
    package_id: str
    rebuilt_sections: tuple[str, ...]
    full_rebuild: bool

    @property
    def changed(self) -> bool:
        return bool(self.rebuilt_sections) or self.full_rebuild


class IncrementalRebuilder:
    """Content-hash-driven partial rebuild planning."""

    def plan(
        self,
        *,
        package_id: str,
        previous_hashes: dict[str, str],
        current_hashes: dict[str, str],
        draft_revision_changed: bool = False,
    ) -> RebuildResult:
        if draft_revision_changed:
            return RebuildResult(package_id, tuple(sorted(current_hashes)), True)
        rebuilt = [
            section
            for section in sorted(set(previous_hashes) | set(current_hashes))
            if previous_hashes.get(section) != current_hashes.get(section)
        ]
        return RebuildResult(package_id, tuple(rebuilt), False)

    @staticmethod
    def content_hash(payload: Mapping[str, object]) -> str:
        """Return the canonical section hash used by the rebuild planner."""
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
