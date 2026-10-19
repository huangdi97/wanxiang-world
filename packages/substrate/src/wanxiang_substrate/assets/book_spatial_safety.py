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
from wanxiang_substrate.assets.book_spatial_validation import _known_spatial_signature_matches
from wanxiang_substrate.assets.storage import AssetRef, ObjectStore

_IN_PROCESS_SUBMISSION_LOCK = Lock()


def _require_spatial_asset_refs(
    objects: ObjectStore,
    refs: tuple[AssetRef, ...],
    *,
    delivery_rights: str,
    allowed_media_types: frozenset[str] | None = None,
) -> None:
    """Re-verify persisted T3 refs before mounting them into the Player stage."""
    try:
        for ref in refs:
            if ref.rights != delivery_rights:
                raise ValueError("spatial asset rights do not match persisted ticket")
            if allowed_media_types is not None and ref.content_type not in allowed_media_types:
                raise ValueError("spatial asset media type is no longer allowed by provider")
            content = objects.get(ref)
            if len(content) != ref.size:
                raise ValueError("spatial asset size does not match persisted reference")
            if not _known_spatial_signature_matches(ref.content_type, content):
                raise ValueError("spatial asset bytes do not match persisted media type")
    except (AssetNotFound, AssetCorrupt) as exc:
        raise ValueError("verified spatial asset storage is unavailable") from exc


@contextmanager
def _spatial_submission_guard(
    jobs: object,
    submission_id: str,
    *,
    scope_key: str = "",
) -> Generator[None, None, None]:
    """Serialize T3 budget reservation and submit before provider-side billing."""
    path = getattr(jobs, "_path", None)
    if isinstance(path, pathlib.Path):
        lock_identity = scope_key or submission_id
        digest = hashlib.sha256(lock_identity.encode()).hexdigest()[:24]
        lock_path = path.with_suffix(path.suffix + f".budget-{digest}.lock")
        with _exclusive_index_lock(lock_path):
            yield
        return
    with _IN_PROCESS_SUBMISSION_LOCK:
        yield
