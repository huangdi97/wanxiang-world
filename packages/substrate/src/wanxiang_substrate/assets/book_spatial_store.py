"""Restart-safe stores for non-authoritative T3 generation tickets."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

import json
import pathlib
from typing import cast

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock
from wanxiang_substrate.assets.book_spatial_frame import (
    _projection_frame_from_mapping,
    _projection_frame_to_dict,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationTicket,
    _SpatialJobState,
    _SpatialJobStore,
)
from wanxiang_substrate.assets.storage import AssetRef

_VALID_JOB_STATES = frozenset(
    {
        "submission_ambiguous",
        "submitted",
        "queued",
        "running",
        "verified",
        "attached",
        "failed",
        "cancelled",
        "expired",
    }
)


def _required_string(data: dict[str, object], key: str, *, allow_empty: bool = False) -> str:
    value = data.get(key)
    if not isinstance(value, str) or (not allow_empty and not value):
        raise ValueError(f"spatial ticket {key} must be a string")
    return value


def _optional_string(data: dict[str, object], key: str) -> str:
    value = data.get(key, "")
    if not isinstance(value, str):
        raise ValueError(f"spatial ticket {key} must be a string")
    return value


class _InMemorySpatialJobStore(_SpatialJobStore):
    def __init__(self) -> None:
        self._rows: dict[str, _SpatialGenerationTicket] = {}

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        return self._rows.get(submission_id)

    def put(self, ticket: _SpatialGenerationTicket) -> None:
        self._rows[ticket.submission_id] = ticket

    def list_scope(self, scope_key: str) -> tuple[_SpatialGenerationTicket, ...]:
        return tuple(row for row in self._rows.values() if row.scope_key == scope_key)


class _LocalJsonSpatialJobStore(_SpatialJobStore):
    """Single-filesystem durable ticket store for restart-safe task resumption."""

    def __init__(self, path: pathlib.Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _asset(data: dict[str, object]) -> AssetRef:
        asset_id = _required_string(data, "asset_id")
        content_hash = _required_string(data, "content_hash")
        content_type = _required_string(data, "content_type")
        rights = _required_string(data, "rights")
        size = data.get("size")
        if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
            raise ValueError("spatial asset size must be a positive integer")
        if len(content_hash) != 64 or any(
            char not in "0123456789abcdefABCDEF" for char in content_hash
        ):
            raise ValueError("spatial asset content hash must be sha256")
        return AssetRef(
            asset_id=asset_id,
            content_hash=content_hash.casefold(),
            size=size,
            content_type=content_type,
            rights=rights,
        )

    @classmethod
    def _ticket(cls, data: dict[str, object]) -> _SpatialGenerationTicket:
        raw_assets = data.get("asset_refs", [])
        if not isinstance(raw_assets, list):
            raise ValueError("spatial ticket asset_refs must be a list")
        asset_rows = cast(list[object], raw_assets)
        assets = tuple(
            cls._asset(cast(dict[str, object], item))
            for item in asset_rows
            if isinstance(item, dict)
        )
        if len(assets) != len(asset_rows):
            raise ValueError("spatial ticket asset_refs contains an invalid row")

        state = data.get("state")
        if not isinstance(state, str) or state not in _VALID_JOB_STATES:
            raise ValueError("spatial ticket state is invalid")
        reserved = data.get("reserved_cost_units")
        if isinstance(reserved, bool) or not isinstance(reserved, int) or reserved < 0:
            raise ValueError("spatial ticket reserved cost must be a non-negative integer")
        raw_usage = data.get("provider_usage_units")
        if raw_usage is not None and (
            isinstance(raw_usage, bool) or not isinstance(raw_usage, int) or raw_usage < 0
        ):
            raise ValueError("spatial ticket provider usage must be a non-negative integer")
        if raw_usage is not None and raw_usage > reserved and state != "failed":
            raise ValueError("spatial ticket provider usage exceeds reserved cost")
        attempt = data.get("attempt", 0)
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0:
            raise ValueError("spatial ticket attempt must be a non-negative integer")
        cancellation_requested = data.get("cancellation_requested", False)
        if not isinstance(cancellation_requested, bool):
            raise ValueError("spatial ticket cancellation_requested must be boolean")
        delivery_rights = _required_string(data, "delivery_rights")
        if any(ref.rights != delivery_rights for ref in assets):
            raise ValueError("spatial asset rights do not match ticket delivery rights")
        if state in {"verified", "attached"} and not assets:
            raise ValueError("verified spatial ticket requires asset refs")
        if state not in {"verified", "attached"} and assets:
            raise ValueError("unverified spatial ticket cannot carry asset refs")

        request_ref = data.get("provider_request_ref", "")
        if (
            not isinstance(request_ref, str)
            or len(request_ref) > 2048
            or "\r" in request_ref
            or "\n" in request_ref
        ):
            raise ValueError("spatial ticket provider request reference is invalid")
        task_ref = _required_string(data, "provider_task_ref", allow_empty=True)
        if (
            len(task_ref) > 2048
            or "\r" in task_ref
            or "\n" in task_ref
            or (state == "submission_ambiguous" and bool(task_ref))
            or (state != "submission_ambiguous" and not task_ref)
        ):
            raise ValueError("spatial ticket provider task reference is invalid")

        return _SpatialGenerationTicket(
            submission_id=_required_string(data, "submission_id"),
            scene_key=_required_string(data, "scene_key"),
            provider_id=_required_string(data, "provider_id"),
            provider_version=_required_string(data, "provider_version"),
            provider_task_ref=task_ref,
            state=cast(_SpatialJobState, state),
            reserved_cost_units=reserved,
            delivery_rights=delivery_rights,
            provider_request_ref=request_ref,
            scope_key=_optional_string(data, "scope_key"),
            asset_refs=assets,
            reason=_optional_string(data, "reason"),
            projection_frame=(
                _projection_frame_from_mapping(data["projection_frame"])
                if data.get("projection_frame") is not None
                else None
            ),
            provider_usage_units=raw_usage,
            attempt=attempt,
            cancellation_requested=cancellation_requested,
        )

    def _rows(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("spatial job store must contain an object")
        decoded_rows = cast(dict[object, object], decoded)
        rows: dict[str, dict[str, object]] = {}
        for key, value in decoded_rows.items():
            # T3 rows carry durable world-budget reservations. A corrupt row
            # must never disappear from accounting by being silently skipped.
            if not isinstance(key, str) or not isinstance(value, dict):
                raise ValueError("spatial job store contains an invalid ticket row")
            rows[key] = cast(dict[str, object], value)
        return rows

    @classmethod
    def _ticket_for_key(
        cls, submission_id: str, row: dict[str, object]
    ) -> _SpatialGenerationTicket:
        ticket = cls._ticket(row)
        if ticket.submission_id != submission_id:
            raise ValueError("spatial ticket key does not match submission_id")
        return ticket

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        with _exclusive_index_lock(self._path.with_suffix(".lock")):
            row = self._rows().get(submission_id)
            return self._ticket_for_key(submission_id, row) if row is not None else None

    def put(self, ticket: _SpatialGenerationTicket) -> None:
        lock_path = self._path.with_suffix(".lock")
        with _exclusive_index_lock(lock_path):
            rows = self._rows()
            rows[ticket.submission_id] = {
                "submission_id": ticket.submission_id,
                "scene_key": ticket.scene_key,
                "provider_id": ticket.provider_id,
                "provider_version": ticket.provider_version,
                "provider_task_ref": ticket.provider_task_ref,
                "state": ticket.state,
                "reserved_cost_units": ticket.reserved_cost_units,
                "delivery_rights": ticket.delivery_rights,
                "provider_request_ref": ticket.provider_request_ref,
                "scope_key": ticket.scope_key,
                "reason": ticket.reason,
                "provider_usage_units": ticket.provider_usage_units,
                "attempt": ticket.attempt,
                "cancellation_requested": ticket.cancellation_requested,
                "projection_frame": (
                    _projection_frame_to_dict(ticket.projection_frame)
                    if ticket.projection_frame is not None
                    else None
                ),
                "asset_refs": [
                    {
                        "asset_id": ref.asset_id,
                        "content_hash": ref.content_hash,
                        "size": ref.size,
                        "content_type": ref.content_type,
                        "rights": ref.rights,
                    }
                    for ref in ticket.asset_refs
                ],
            }
            temporary = self._path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(rows, sort_keys=True, separators=(",", ":")),
                encoding="utf-8",
            )
            temporary.replace(self._path)

    def list_scope(self, scope_key: str) -> tuple[_SpatialGenerationTicket, ...]:
        with _exclusive_index_lock(self._path.with_suffix(".lock")):
            rows = tuple(
                self._ticket_for_key(submission_id, row)
                for submission_id, row in self._rows().items()
            )
        return tuple(row for row in rows if row.scope_key == scope_key)
