"""SOURCE_TO_LIVING_WORLD cache restart evidence (Phase 6).

Proves the visual cache lives on disk (`artifacts/local-visual-cache/blobs/` +
`index.json`), not only in Python process memory. This file must be executed as
TWO separate OS processes:

    uv run python scripts/source_to_living_world_cache_restart.py --phase first
    uv run python scripts/source_to_living_world_cache_restart.py --phase verify

`first` runs one Book -> Scene authoring against an empty
artifacts/local-visual-cache and records provider_calls/cache_hits/sha256.
A completely new process (`verify`) re-requests the same book with only the
on-disk cache and asserts provider_calls == 0, cache_hits >= 1 and an
unchanged content hash.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

from wanxiang_substrate.assets.book_scene_cache import LocalJsonVisualCacheIndex, VisualAssetCache
from wanxiang_substrate.assets.storage import LocalObjectStore
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "artifacts" / "local-visual-cache"
STATE_PATH = CACHE_DIR / "restart_state.json"

BOOK = (
    "# 第一章\n角色：沈砚\n沈砚来到江南城。\n"
    "沈砚来到机关桥。\n规则：入城者必须登记。\n"
    "1921年，沈砚到达江南城。\n"
)


def _source() -> SourceRecord:
    return SourceRecord(
        source_id="cache_restart_book",
        kind="text",
        content_hash=payload_hash(BOOK),
        content_ref="memory://cache_restart_book",
        stage="E3",
        rights=RightsEnvelope(
            owner="synthetic",
            usage="test",
            approved=True,
            public_export_allowed=True,
        ),
        payload=BOOK,
        provenance="synthetic:cache-restart",
        access="public",
    )


def _service() -> AuthoringService:
    return AuthoringService(providers=ProviderRouter((LocalSemanticProvider(),)))


def _disk_cache() -> VisualAssetCache:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return VisualAssetCache(
        LocalObjectStore(CACHE_DIR / "blobs"),
        LocalJsonVisualCacheIndex(CACHE_DIR / "index.json"),
    )


def _measure(job_id: str) -> dict[str, Any]:
    authored = OneClickAuthoring(_service(), visual_cache=_disk_cache()).run(
        job_id,
        (_source(),),
        profile="book",
        semantic_provider="local",
    )
    assert authored.visual_plan is not None
    assert authored.visual_assets, "book produced no visual assets"
    first_asset = authored.visual_assets[0]
    return {
        "provider_calls": authored.visual_provider_calls,
        "cache_hits": authored.visual_cache_hits,
        "content_sha256": first_asset.content_sha256,
        "media_type": first_asset.media_type,
        "scene_count": len(authored.visual_plan.scene_requests),
    }


def _disk_state() -> dict[str, Any]:
    blobs = sorted(path for path in (CACHE_DIR / "blobs").rglob("*") if path.is_file())
    return {
        "blob_count": len(blobs),
        "disk_index_exists": (CACHE_DIR / "index.json").is_file(),
        "blobs_dir": str(CACHE_DIR / "blobs"),
        "index_path": str(CACHE_DIR / "index.json"),
    }


def phase_first() -> int:
    result = _measure("cache_restart_job")
    assert result["provider_calls"] > 0, "cold first run must call the provider"
    assert result["cache_hits"] == 0, "cold first run must have no cache hits"
    result.update(_disk_state())
    assert result["blob_count"] > 0 and result["disk_index_exists"], "cache not on disk"
    STATE_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("CACHE_RESTART_FIRST=PASS")
    return 0


def phase_verify() -> int:
    previous = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    # Brand-new process: only the on-disk cache is available.
    current = _measure("cache_restart_job_verify")
    assert current["provider_calls"] == 0, current
    assert current["cache_hits"] >= 1, current
    assert current["content_sha256"] == previous["content_sha256"], (previous, current)
    current.update(_disk_state())
    assert current["blob_count"] > 0 and current["disk_index_exists"], "cache missing on disk"

    evidence = {
        "first_process": previous,
        "restarted_process": current,
        "provider_calls_after_restart": current["provider_calls"],
        "cache_hits_after_restart": current["cache_hits"],
        "content_sha256_unchanged": current["content_sha256"] == previous["content_sha256"],
    }
    out = ROOT / "artifacts" / "runtime-evidence" / "2026-10-09-source-to-living-world"
    out.mkdir(parents=True, exist_ok=True)
    (out / "cache_restart.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
    print("CACHE_RESTART_VERIFY=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("first", "verify"), required=True)
    args = parser.parse_args()
    if args.phase == "first":
        return phase_first()
    return phase_verify()


if __name__ == "__main__":
    raise SystemExit(main())
