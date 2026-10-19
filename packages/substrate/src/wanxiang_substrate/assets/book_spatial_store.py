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
    _SpatialJobStore,
)
from wanxiang_substrate.assets.storage import AssetRef


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
        return AssetRef(
            asset_id=cast(str, data["asset_id"]),
            content_hash=cast(str, data["content_hash"]),
            size=cast(int, data["size"]),
            content_type=cast(str, data["content_type"]),
            rights=cast(str, data["rights"]),
        )

    @classmethod
    def _ticket(cls, data: dict[str, object]) -> _SpatialGenerationTicket:
        raw_assets = data.get("asset_refs", [])
        assets = tuple(
            cls._asset(cast(dict[str, object], item))
            for item in cast(list[object], raw_assets)
            if isinstance(item, dict)
        )
        raw_usage = data.get("provider_usage_units")
        if raw_usage is not None and (
            isinstance(raw_usage, bool) or not isinstance(raw_usage, int) or raw_usage < 0
        ):
            raise ValueError("spatial ticket provider usage must be a non-negative integer")
        provider_usage_units = cast(int, raw_usage) if raw_usage is not None else None
        return _SpatialGenerationTicket(
            submission_id=cast(str, data["submission_id"]),
            scene_key=cast(str, data["scene_key"]),
            provider_id=cast(str, data["provider_id"]),
            provider_version=cast(str, data["provider_version"]),
            provider_task_ref=cast(str, data["provider_task_ref"]),
            state=cast(object, data["state"]),  # type: ignore[arg-type]
            reserved_cost_units=cast(int, data["reserved_cost_units"]),
            delivery_rights=cast(str, data["delivery_rights"]),
            scope_key=cast(str, data.get("scope_key", "")),
            asset_refs=assets,
            reason=cast(str, data.get("reason", "")),
            projection_frame=(
                _projection_frame_from_mapping(data["projection_frame"])
                if data.get("projection_frame") is not None
                else None
            ),
            provider_usage_units=provider_usage_units,
        )

    def _rows(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("spatial job store must contain an object")
        return {
            key: cast(dict[str, object], value)
            for key, value in cast(dict[object, object], decoded).items()
            if isinstance(key, str) and isinstance(value, dict)
        }

    def get(self, submission_id: str) -> _SpatialGenerationTicket | None:
        with _exclusive_index_lock(self._path.with_suffix(".lock")):
            row = self._rows().get(submission_id)
            return self._ticket(row) if row is not None else None

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
                "scope_key": ticket.scope_key,
                "reason": ticket.reason,
                "provider_usage_units": ticket.provider_usage_units,
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
            rows = tuple(self._ticket(row) for row in self._rows().values())
        return tuple(row for row in rows if row.scope_key == scope_key)
