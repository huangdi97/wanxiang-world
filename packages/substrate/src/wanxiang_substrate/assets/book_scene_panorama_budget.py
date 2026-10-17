"""World-scoped conservative budget reservations for synchronous T2 panoramas."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from threading import Lock
from typing import cast

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock


@dataclass(frozen=True, slots=True)
class _PanoramaBudgetSnapshot:
    reserved: int
    remaining: int
    reservations: int

    def to_dict(self) -> dict[str, int]:
        return {
            "reserved": self.reserved,
            "remaining": self.remaining,
            "reservations": self.reservations,
        }


def _snapshot(rows: dict[str, int], budget: int) -> _PanoramaBudgetSnapshot:
    if budget < 0:
        raise ValueError("panorama budget must be non-negative")
    reserved = sum(rows.values())
    return _PanoramaBudgetSnapshot(
        reserved=reserved,
        remaining=max(0, budget - reserved),
        reservations=len(rows),
    )


class _PanoramaBudgetLedger:
    """Thread-safe conservative reservation ledger for one API process."""

    def __init__(self) -> None:
        self._rows: dict[str, dict[str, int]] = {}
        self._lock = Lock()

    def usage(self, scope_key: str, budget: int) -> _PanoramaBudgetSnapshot:
        with self._lock:
            return _snapshot(dict(self._rows.get(scope_key, {})), budget)

    def reserve(
        self,
        scope_key: str,
        reservation_key: str,
        cost_units: int,
        budget: int,
    ) -> _PanoramaBudgetSnapshot:
        if not scope_key or not reservation_key:
            raise ValueError("panorama reservation requires scope and identity")
        if cost_units < 0 or budget < 0:
            raise ValueError("panorama cost values must be non-negative")
        with self._lock:
            rows = self._rows.setdefault(scope_key, {})
            existing = rows.get(reservation_key)
            if existing is not None:
                if existing != cost_units:
                    raise ValueError("persisted panorama reservation cost changed")
                return _snapshot(dict(rows), budget)
            if sum(rows.values()) + cost_units > budget:
                raise ValueError("panorama world budget is exhausted")
            rows[reservation_key] = cost_units
            return _snapshot(dict(rows), budget)


class _LocalJson_PanoramaBudgetLedger(_PanoramaBudgetLedger):
    """Cross-process local reservation ledger; malformed state fails closed."""

    def __init__(self, path: pathlib.Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> dict[str, dict[str, int]]:
        if not self._path.exists():
            return {}
        try:
            decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError("panorama budget ledger is unreadable") from exc
        if not isinstance(decoded, dict):
            raise ValueError("panorama budget ledger is invalid")
        result: dict[str, dict[str, int]] = {}
        for raw_scope, raw_rows in cast(dict[object, object], decoded).items():
            if not isinstance(raw_scope, str) or not isinstance(raw_rows, dict):
                raise ValueError("panorama budget ledger is invalid")
            scoped: dict[str, int] = {}
            for raw_key, raw_cost in cast(dict[object, object], raw_rows).items():
                if (
                    not isinstance(raw_key, str)
                    or isinstance(raw_cost, bool)
                    or not isinstance(raw_cost, int)
                    or raw_cost < 0
                ):
                    raise ValueError("panorama budget ledger is invalid")
                scoped[raw_key] = raw_cost
            result[raw_scope] = scoped
        return result

    def _write(self, rows: dict[str, dict[str, int]]) -> None:
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(rows, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        temporary.replace(self._path)

    def usage(self, scope_key: str, budget: int) -> _PanoramaBudgetSnapshot:
        lock_path = self._path.with_suffix(self._path.suffix + ".lock")
        with _exclusive_index_lock(lock_path):
            rows = self._read()
            return _snapshot(dict(rows.get(scope_key, {})), budget)

    def reserve(
        self,
        scope_key: str,
        reservation_key: str,
        cost_units: int,
        budget: int,
    ) -> _PanoramaBudgetSnapshot:
        if not scope_key or not reservation_key:
            raise ValueError("panorama reservation requires scope and identity")
        if cost_units < 0 or budget < 0:
            raise ValueError("panorama cost values must be non-negative")
        lock_path = self._path.with_suffix(self._path.suffix + ".lock")
        with _exclusive_index_lock(lock_path):
            rows = self._read()
            scoped = rows.setdefault(scope_key, {})
            existing = scoped.get(reservation_key)
            if existing is not None:
                if existing != cost_units:
                    raise ValueError("persisted panorama reservation cost changed")
                return _snapshot(dict(scoped), budget)
            if sum(scoped.values()) + cost_units > budget:
                raise ValueError("panorama world budget is exhausted")
            scoped[reservation_key] = cost_units
            self._write(rows)
            return _snapshot(dict(scoped), budget)


PanoramaBudgetLedger = _PanoramaBudgetLedger
LocalJsonPanoramaBudgetLedger = _LocalJson_PanoramaBudgetLedger
