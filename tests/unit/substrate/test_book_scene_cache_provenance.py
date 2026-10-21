"""Visual cache validates derived provider provenance before object-store writes."""

# pyright: reportPrivateUsage=false

import hashlib
import pathlib

import pytest
from wanxiang_substrate.assets.book_scene_cache import (
    LocalJsonVisualCacheIndex,
    VisualAssetCache,
)
from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset
from wanxiang_substrate.assets.storage import LocalObjectStore


def _asset(**changes: object) -> _SceneVisualAsset:
    content = b"\x89PNG\r\n\x1a\ncache-proof"
    values: dict[str, object] = {
        "scene_key": "scene-a",
        "place_name": "Garden",
        "provider_id": "provider:test",
        "media_type": "image/png",
        "content": content,
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "cache_key": "cache-a",
        "provider_version": "1",
    }
    values.update(changes)
    return _SceneVisualAsset(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"content_sha256": "0" * 64}, "digest"),
        ({"provider_usage_units": -1}, "usage"),
        ({"provider_usage_units": True}, "usage"),
        ({"provider_request_id": "bad\ntrace"}, "request id"),
        ({"provider_operation_id": "bad\rtrace"}, "operation id"),
        ({"presentation_kind": "spatial"}, "presentation"),
    ],
)
def test_visual_cache_rejects_invalid_asset_before_blob_write(
    changes: dict[str, object], message: str
) -> None:
    cache = VisualAssetCache()
    with pytest.raises(ValueError, match=message):
        cache.put(_asset(**changes))

    assert cache.index.list() == ()


def test_visual_cache_accepts_valid_private_provider_provenance() -> None:
    cache = VisualAssetCache()
    asset = _asset(
        provider_usage_units=500_000,
        provider_request_id="request-1",
        provider_operation_id="operation-1",
        presentation_kind="panorama",
    )

    ref = cache.put(asset, rights="source-gated")
    cached = cache.get(asset.cache_key, rights="source-gated")

    assert ref.content_hash == asset.content_sha256
    assert cached is not None
    assert cached[0].provider_usage_units == 500_000
    assert cached[0].provider_request_id == "request-1"
    assert cached[0].provider_operation_id == "operation-1"


def test_durable_visual_cache_corruption_fails_closed_before_regeneration(
    tmp_path: pathlib.Path,
) -> None:
    index_path = tmp_path / "index.json"
    index_path.write_text("{not-json", encoding="utf-8")
    cache = VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        LocalJsonVisualCacheIndex(index_path),
    )

    with pytest.raises(ValueError, match="index is unreadable"):
        cache.get("paid-scene:tencent-tokenhub-image@hy-image-v3")
    with pytest.raises(ValueError, match="index is unreadable"):
        cache.index.list()


@pytest.mark.parametrize(
    "payload",
    [
        "[]",
        '{"bad-row":"not-an-object"}',
        '{"paid-scene":{"cache_key":7}}',
    ],
)
def test_invalid_durable_visual_cache_schema_never_degrades_to_a_cache_miss(
    tmp_path: pathlib.Path, payload: str
) -> None:
    index_path = tmp_path / "index.json"
    index_path.write_text(payload, encoding="utf-8")
    cache = VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        LocalJsonVisualCacheIndex(index_path),
    )

    with pytest.raises(ValueError, match="visual cache index"):
        cache.index.list()
