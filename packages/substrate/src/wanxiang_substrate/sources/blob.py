"""Content-addressed source blob reference (G55B).

Business records (SourceRecord, ParsedDocument, Segment) must never store raw
large bytes; they reference blobs by content-addressed identity. This module
reuses the single durable ObjectStore port (G16D) and adds a source-oriented
BlobRef + dedupe adapter: same content hash = same blob (no duplicate storage),
size-guarded, with an honest URI scheme so records can be checked and resolved.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.assets.storage import AssetRef, ObjectStore

BlobKind = Literal["source", "asset"]
VALID_BLOB_KINDS = ("source", "asset")
BLOB_URI_SCHEME = "blob://"
MAX_BLOB_BYTES = 256 * 1024 * 1024  # 256 MiB guard for a single source blob.


@dataclass(frozen=True, slots=True)
class BlobRef:
    """Content-addressed reference to a stored source/asset blob."""

    blob_id: str
    content_hash: str
    size: int
    content_type: str
    kind: BlobKind = "source"
    rights: str = "private"

    def __post_init__(self) -> None:
        if not self.blob_id or not self.content_hash:
            raise ContractError("blob ref requires id and content hash")
        if len(self.content_hash) != 64:
            raise ContractError("content_hash must be a sha256 hex digest")
        if self.size < 0:
            raise ContractError("blob size must be non-negative")
        if self.kind not in VALID_BLOB_KINDS:
            raise ContractError(f"invalid blob kind {self.kind!r}")

    def uri(self) -> str:
        return f"{BLOB_URI_SCHEME}{self.blob_id}"


class SourceBlobStore:
    """Deduplicating blob adapter over the single ObjectStore port (G16D)."""

    def __init__(self, store: ObjectStore, *, max_bytes: int = MAX_BLOB_BYTES) -> None:
        self._store = store
        self._max_bytes = max_bytes
        self._index: dict[str, BlobRef] = {}

    def store(
        self,
        blob: bytes,
        *,
        content_type: str,
        kind: BlobKind = "source",
        rights: str = "private",
    ) -> BlobRef:
        if len(blob) > self._max_bytes:
            raise ContractError(f"blob exceeds {self._max_bytes} byte limit")
        content_hash = hashlib.sha256(blob).hexdigest()
        existing = self._index.get(content_hash)
        if existing is not None:
            return existing
        asset_ref = self._store.put(blob, content_type=content_type, rights=rights)
        ref = BlobRef(
            blob_id=asset_ref.asset_id,
            content_hash=content_hash,
            size=len(blob),
            content_type=content_type,
            kind=kind,
            rights=rights,
        )
        self._index[content_hash] = ref
        return ref

    def load(self, ref: BlobRef) -> bytes:
        asset_ref = AssetRef(
            asset_id=ref.blob_id,
            content_hash=ref.content_hash,
            size=ref.size,
            content_type=ref.content_type,
            rights=ref.rights,
        )
        return self._store.get(asset_ref)

    def locate(self, content_hash: str) -> BlobRef | None:
        return self._index.get(content_hash)

    def stat(self, ref: BlobRef) -> BlobRef:
        return ref


def is_blob_uri(content_ref: str) -> bool:
    return content_ref.startswith(BLOB_URI_SCHEME)
