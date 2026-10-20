"""Public API job stores with world-scoped recovery over durable T3 tickets."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock
from wanxiang_substrate.assets.book_spatial_jobs import (
    _InMemorySpatialJobStore,
    _LocalJsonSpatialJobStore,
)
from wanxiang_substrate.assets.book_spatial_types import _SpatialGenerationTicket


class _RecoverableInMemorySpatialJobStore(_InMemorySpatialJobStore):
    def list_scope(self, scope_key: str) -> tuple[_SpatialGenerationTicket, ...]:
        return tuple(row for row in self._rows.values() if row.scope_key == scope_key)


class _RecoverableLocalJsonSpatialJobStore(_LocalJsonSpatialJobStore):
    def list_scope(self, scope_key: str) -> tuple[_SpatialGenerationTicket, ...]:
        with _exclusive_index_lock(self._path.with_suffix(".lock")):
            rows = tuple(
                self._ticket_for_key(submission_id, row)
                for submission_id, row in self._rows().items()
            )
        return tuple(row for row in rows if row.scope_key == scope_key)
