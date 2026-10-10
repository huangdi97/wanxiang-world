"""Restart-safe metadata cache for source-derived visual assets."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import _thread
import json
import pathlib
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from threading import Lock
from typing import cast

from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset
from wanxiang_substrate.assets.errors import AssetNotFound
from wanxiang_substrate.assets.storage import AssetRef, InMemoryObjectStore, ObjectStore


@dataclass(frozen=True, slots=True)
class _VisualCacheRecord:
    cache_key: str
    scene_key: str
    place_name: str
    provider_id: str
    provider_version: str
    media_type: str
    content_sha256: str
    asset_id: str
    size: int
    illustrative: bool
    style_key: str


class _VisualCacheIndex:
    """Replaceable metadata index; blob bytes remain owned by ObjectStore."""

    def get(self, cache_key: str) -> _VisualCacheRecord | None:
        raise TypeError("concrete visual implementation required")

    def put(self, record: _VisualCacheRecord) -> None:
        raise TypeError("concrete visual implementation required")


class _InMemoryVisualCacheIndex(_VisualCacheIndex):
    def __init__(self) -> None:
        self._rows: dict[str, _VisualCacheRecord] = {}

    def get(self, cache_key: str) -> _VisualCacheRecord | None:
        return self._rows.get(cache_key)

    def put(self, record: _VisualCacheRecord) -> None:
        self._rows[record.cache_key] = record


class LocalJsonVisualCacheIndex(_VisualCacheIndex):
    """Single-process durable dev index; production may inject a DB/object index."""

    def __init__(self, path: pathlib.Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._write_lock = Lock()

    def _rows(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        try:
            decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(decoded, dict):
            return {}
        decoded_rows = cast(dict[object, object], decoded)
        rows: dict[str, dict[str, object]] = {}
        for raw_key, raw_value in decoded_rows.items():
            if not isinstance(raw_key, str) or not isinstance(raw_value, dict):
                continue
            value_map = cast(dict[object, object], raw_value)
            rows[raw_key] = {key: value for key, value in value_map.items() if isinstance(key, str)}
        return rows

    @staticmethod
    def _record(raw: dict[str, object]) -> _VisualCacheRecord | None:
        required_strings = (
            "cache_key",
            "scene_key",
            "place_name",
            "provider_id",
            "provider_version",
            "media_type",
            "content_sha256",
            "asset_id",
            "style_key",
        )
        if not all(isinstance(raw.get(name), str) for name in required_strings):
            return None
        size = raw.get("size")
        illustrative = raw.get("illustrative")
        if not isinstance(size, int) or not isinstance(illustrative, bool):
            return None
        return _VisualCacheRecord(
            cache_key=cast(str, raw["cache_key"]),
            scene_key=cast(str, raw["scene_key"]),
            place_name=cast(str, raw["place_name"]),
            provider_id=cast(str, raw["provider_id"]),
            provider_version=cast(str, raw["provider_version"]),
            media_type=cast(str, raw["media_type"]),
            content_sha256=cast(str, raw["content_sha256"]),
            asset_id=cast(str, raw["asset_id"]),
            size=size,
            illustrative=illustrative,
            style_key=cast(str, raw["style_key"]),
        )

    def get(self, cache_key: str) -> _VisualCacheRecord | None:
        raw = self._rows().get(cache_key)
        return self._record(raw) if raw is not None else None

    def put(self, record: _VisualCacheRecord) -> None:
        with self._write_lock:
            rows = self._rows()
            rows[record.cache_key] = {
                "cache_key": record.cache_key,
                "scene_key": record.scene_key,
                "place_name": record.place_name,
                "provider_id": record.provider_id,
                "provider_version": record.provider_version,
                "media_type": record.media_type,
                "content_sha256": record.content_sha256,
                "asset_id": record.asset_id,
                "size": record.size,
                "illustrative": record.illustrative,
                "style_key": record.style_key,
            }
            temporary = self._path.with_suffix(self._path.suffix + ".tmp")
            temporary.write_text(
                json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                encoding="utf-8",
            )
            temporary.replace(self._path)


class VisualAssetCache:
    """Content-addressed blobs plus cache-key metadata."""

    def __init__(
        self,
        store: ObjectStore | None = None,
        index: _VisualCacheIndex | None = None,
    ) -> None:
        self.store = store or InMemoryObjectStore()
        self.index = index or _InMemoryVisualCacheIndex()
        self._guard_lock = Lock()
        self._scene_locks: dict[str, _thread.LockType] = {}

    @contextmanager
    def generation_guard(self, cache_keys: Iterable[str]) -> Iterator[None]:
        """Coalesce concurrent same-scene generation in one Python process."""
        with self._guard_lock:
            locks = [self._scene_locks.setdefault(key, Lock()) for key in sorted(set(cache_keys))]
        for lock in locks:
            lock.acquire()
        try:
            yield
        finally:
            for lock in reversed(locks):
                lock.release()

    def get(
        self,
        cache_key: str,
        *,
        rights: str = "public",
    ) -> tuple[_SceneVisualAsset, AssetRef] | None:
        metadata = self.index.get(cache_key)
        if metadata is None:
            return None
        ref = AssetRef(
            asset_id=metadata.asset_id,
            content_hash=metadata.content_sha256,
            size=metadata.size,
            content_type=metadata.media_type,
            rights=rights,
        )
        try:
            content = self.store.get(ref)
        except AssetNotFound:
            # Stale metadata is a cache miss, not a broken world. The caller
            # still enforces provider rights, network permission and budget.
            return None
        return (
            _SceneVisualAsset(
                scene_key=metadata.scene_key,
                place_name=metadata.place_name,
                provider_id=metadata.provider_id,
                media_type=metadata.media_type,
                content=content,
                content_sha256=metadata.content_sha256,
                cache_key=metadata.cache_key,
                illustrative=metadata.illustrative,
                style_key=metadata.style_key,
                provider_version=metadata.provider_version,
            ),
            ref,
        )

    def put(self, asset: _SceneVisualAsset, *, rights: str = "public") -> AssetRef:
        ref = self.store.put(asset.content, content_type=asset.media_type, rights=rights)
        self.index.put(
            _VisualCacheRecord(
                cache_key=asset.cache_key,
                scene_key=asset.scene_key,
                place_name=asset.place_name,
                provider_id=asset.provider_id,
                provider_version=asset.provider_version,
                media_type=asset.media_type,
                content_sha256=asset.content_sha256,
                asset_id=ref.asset_id,
                size=ref.size,
                illustrative=asset.illustrative,
                style_key=asset.style_key,
            )
        )
        return ref
