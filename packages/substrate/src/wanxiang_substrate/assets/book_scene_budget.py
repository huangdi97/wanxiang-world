"""Per-world on-demand visual spend ledger.

The ledger persists paid provider-call counts next to the local visual cache so
a restart of the same deployment does not forget the budget. It is still a
single-filesystem adapter: it is not a distributed reservation system.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import json
import pathlib
from typing import cast

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock


class VisualBudgetLedger:
    """Counts paid on-demand visual calls per world; optional durable JSON file."""

    def __init__(self, path: pathlib.Path | None = None) -> None:
        self._path = path
        self._counts: dict[str, int] = self._load() if path is not None else {}

    def _load(self) -> dict[str, int]:
        if self._path is None or not self._path.exists():
            return {}
        try:
            decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(decoded, dict):
            return {}
        counts: dict[str, int] = {}
        for raw_key, raw_value in cast(dict[object, object], decoded).items():
            if isinstance(raw_key, str) and isinstance(raw_value, int) and raw_value >= 0:
                counts[raw_key] = raw_value
        return counts

    def _write(self, counts: dict[str, int]) -> None:
        if self._path is None:
            self._counts = counts
            return
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(counts, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        temporary.replace(self._path)
        self._counts = counts

    def used(self, profile_id: str) -> int:
        """Return the recorded spend; durable ledgers always re-read the file."""
        if self._path is not None:
            self._counts = self._load()
        return self._counts.get(profile_id, 0)

    def record(self, profile_id: str, calls: int) -> None:
        """Add paid calls under the single-filesystem lock."""
        if calls <= 0:
            return
        if self._path is None:
            self._counts[profile_id] = self.used(profile_id) + calls
            return
        lock_path = self._path.with_suffix(self._path.suffix + ".lock")
        with _exclusive_index_lock(lock_path):
            counts = self._load()
            counts[profile_id] = counts.get(profile_id, 0) + calls
            self._write(counts)
