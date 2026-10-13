"""T3 submission and persisted-asset safety helpers."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import hashlib
import pathlib
from collections.abc import Generator
from contextlib import contextmanager
from threading import Lock

from wanxiang_substrate.assets.book_scene_interprocess import _exclusive_index_lock
from wanxiang_substrate.assets.errors import AssetCorrupt, AssetNotFound
from wanxiang_substrate.assets.storage import AssetRef, ObjectStore

_IN_PROCESS_SUBMISSION_LOCK = Lock()


def _require_spatial_asset_refs(objects: ObjectStore, refs: tuple[AssetRef, ...]) -> None:
    """Fail closed when a persisted T3 reference no longer resolves intact."""
    try:
        for ref in refs:
            content = objects.get(ref)
            if len(content) != ref.size:
                raise ValueError("spatial asset size does not match persisted reference")
    except (AssetNotFound, AssetCorrupt) as exc:
        raise ValueError("verified spatial asset storage is unavailable") from exc


@contextmanager
def _spatial_submission_guard(jobs: object, submission_id: str) -> Generator[None, None, None]:
    """Serialize one logical T3 submit before any provider-side billing call."""
    path = getattr(jobs, "_path", None)
    if isinstance(path, pathlib.Path):
        digest = hashlib.sha256(submission_id.encode()).hexdigest()[:24]
        lock_path = path.with_suffix(path.suffix + f".submit-{digest}.lock")
        with _exclusive_index_lock(lock_path):
            yield
        return
    with _IN_PROCESS_SUBMISSION_LOCK:
        yield
