"""Fail-closed per-world reservation ledger for on-demand T1 visual generation.

Paid provider attempts are reserved before the network boundary so concurrent
requests cannot race through a world generation limit. Durable ledgers are
single-filesystem coordination adapters, not distributed databases.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import json
import pathlib
from threading import Lock
from typing import cast

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock

_FORMAT_KEY = "__wanxiang_visual_budget__"
_FORMAT_VERSION = 2


class VisualBudgetLedger:
    """Count usage and idempotent paid-attempt reservations per world."""

    def __init__(self, path: pathlib.Path | None = None) -> None:
        self._path = path
        self._lock = Lock()
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            self._counts, self._reservations = self._load()
        else:
            self._counts: dict[str, int] = {}
            self._reservations: dict[str, set[str]] = {}

    @staticmethod
    def _legacy_counts(decoded: dict[object, object]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for raw_key, raw_value in decoded.items():
            if (
                not isinstance(raw_key, str)
                or isinstance(raw_value, bool)
                or not isinstance(raw_value, int)
                or raw_value < 0
            ):
                raise ValueError("visual budget ledger is invalid")
            counts[raw_key] = raw_value
        return counts

    @staticmethod
    def _versioned_state(
        decoded: dict[object, object],
    ) -> tuple[dict[str, int], dict[str, set[str]]]:
        raw_counts = decoded.get("counts")
        raw_reservations = decoded.get("reservations")
        if not isinstance(raw_counts, dict) or not isinstance(raw_reservations, dict):
            raise ValueError("visual budget ledger is invalid")
        counts = VisualBudgetLedger._legacy_counts(cast(dict[object, object], raw_counts))
        reservations: dict[str, set[str]] = {}
        for raw_profile, raw_keys in cast(dict[object, object], raw_reservations).items():
            if not isinstance(raw_profile, str) or not isinstance(raw_keys, list):
                raise ValueError("visual budget ledger is invalid")
            keys = cast(list[object], raw_keys)
            if any(not isinstance(key, str) or not key for key in keys):
                raise ValueError("visual budget ledger is invalid")
            unique = set(cast(list[str], keys))
            if len(unique) != len(keys):
                raise ValueError("visual budget ledger contains duplicate reservations")
            if len(unique) > counts.get(raw_profile, 0):
                raise ValueError("visual budget reservations exceed recorded usage")
            reservations[raw_profile] = unique
        return counts, reservations

    def _load(self) -> tuple[dict[str, int], dict[str, set[str]]]:
        if self._path is None or not self._path.exists():
            return {}, {}
        try:
            decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError("visual budget ledger is unreadable") from exc
        if not isinstance(decoded, dict):
            raise ValueError("visual budget ledger is invalid")
        rows = cast(dict[object, object], decoded)
        if _FORMAT_KEY not in rows:
            return self._legacy_counts(rows), {}
        if rows.get(_FORMAT_KEY) != _FORMAT_VERSION:
            raise ValueError("visual budget ledger version is unsupported")
        return self._versioned_state(rows)

    def _write(
        self,
        counts: dict[str, int],
        reservations: dict[str, set[str]],
    ) -> None:
        self._counts = dict(counts)
        self._reservations = {profile: set(keys) for profile, keys in reservations.items()}
        if self._path is None:
            return
        payload = {
            _FORMAT_KEY: _FORMAT_VERSION,
            "counts": counts,
            "reservations": {
                profile: sorted(keys)
                for profile, keys in reservations.items()
                if keys
            },
        }
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        temporary.replace(self._path)

    def _lock_path(self) -> pathlib.Path:
        assert self._path is not None
        return self._path.with_suffix(self._path.suffix + ".lock")

    def used(self, profile_id: str) -> int:
        """Return conservative recorded usage; corrupt durable state never resets spend."""
        if self._path is None:
            with self._lock:
                return self._counts.get(profile_id, 0)
        with _exclusive_index_lock(self._lock_path()):
            counts, reservations = self._load()
            self._counts, self._reservations = counts, reservations
            return counts.get(profile_id, 0)

    def record(self, profile_id: str, calls: int) -> None:
        """Compatibility path for unbounded calls that still need usage accounting."""
        if calls <= 0:
            return
        if not profile_id:
            raise ValueError("visual budget record requires a profile id")
        if self._path is None:
            with self._lock:
                counts = dict(self._counts)
                counts[profile_id] = counts.get(profile_id, 0) + calls
                self._write(counts, self._reservations)
            return
        with _exclusive_index_lock(self._lock_path()):
            counts, reservations = self._load()
            counts[profile_id] = counts.get(profile_id, 0) + calls
            self._write(counts, reservations)

    def reserve(self, profile_id: str, reservation_key: str, limit: int) -> bool:
        """Atomically reserve one paid attempt; repeated identity never reserves twice."""
        if not profile_id or not reservation_key:
            raise ValueError("visual budget reservation requires profile and identity")
        if limit <= 0:
            raise ValueError("visual budget reservation limit must be positive")

        def mutate(
            counts: dict[str, int],
            reservations: dict[str, set[str]],
        ) -> bool:
            keys = reservations.setdefault(profile_id, set())
            if reservation_key in keys:
                return False
            used = counts.get(profile_id, 0)
            if used >= limit:
                raise ValueError(f"world on-demand visual budget exhausted ({used}/{limit})")
            keys.add(reservation_key)
            counts[profile_id] = used + 1
            self._write(counts, reservations)
            return True

        if self._path is None:
            with self._lock:
                return mutate(dict(self._counts), {k: set(v) for k, v in self._reservations.items()})
        with _exclusive_index_lock(self._lock_path()):
            counts, reservations = self._load()
            return mutate(counts, reservations)
