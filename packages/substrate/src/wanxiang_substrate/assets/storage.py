"""Durable asset/object storage (G16D).

Content-addressed blob store with integrity hashes and rights-filtered delivery.
Semantic truth stays in canonical state/events; this store holds durable blobs
referenced by immutable AssetRef identity/version (never a mutable anonymous
path). Local filesystem adapter for dev; object-storage-compatible production
seam is the same Port contract.
"""

from __future__ import annotations

import hashlib
import pathlib
from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.assets.errors import AssetCorrupt, AssetNotFound, AssetRightsDenied


@dataclass(frozen=True, slots=True)
class AssetRef:
    """Immutable content-addressed reference to a stored blob."""

    asset_id: str
    content_hash: str
    size: int
    content_type: str
    rights: str = "public"

    def __post_init__(self) -> None:
        if not self.asset_id or not self.content_hash:
            raise ValueError("asset ref requires id and content hash")


class ObjectStore(Protocol):
    """Durable blob storage port (local filesystem or object-storage seam)."""

    def put(self, blob: bytes, *, content_type: str, rights: str = "public") -> AssetRef: ...
    def get(self, ref: AssetRef) -> bytes: ...
    def stat(self, ref: AssetRef) -> AssetRef: ...
    def delete(self, ref: AssetRef) -> None: ...


class LocalObjectStore:
    """Content-addressed local filesystem adapter (dev default)."""

    def __init__(self, root: pathlib.Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _hash(blob: bytes) -> str:
        return hashlib.sha256(blob).hexdigest()

    def _path_for(self, content_hash: str) -> pathlib.Path:
        return self._root / content_hash[:2] / content_hash

    def put(self, blob: bytes, *, content_type: str, rights: str = "public") -> AssetRef:
        content_hash = self._hash(blob)
        path = self._path_for(content_hash)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        return AssetRef(
            asset_id=f"asset:{content_hash[:16]}",
            content_hash=content_hash,
            size=len(blob),
            content_type=content_type,
            rights=rights,
        )

    def get(self, ref: AssetRef) -> bytes:
        path = self._path_for(ref.content_hash)
        if not path.exists():
            raise AssetNotFound(f"blob {ref.content_hash[:12]} missing")
        blob = path.read_bytes()
        if self._hash(blob) != ref.content_hash:
            raise AssetCorrupt(f"blob {ref.content_hash[:12]} integrity mismatch")
        return blob

    def stat(self, ref: AssetRef) -> AssetRef:
        path = self._path_for(ref.content_hash)
        if not path.exists():
            raise AssetNotFound(f"blob {ref.content_hash[:12]} missing")
        return ref

    def delete(self, ref: AssetRef) -> None:
        path = self._path_for(ref.content_hash)
        if path.exists():
            path.unlink()


class InMemoryObjectStore:
    """Deterministic reference ObjectStore for bounded no-API composition."""

    def __init__(self) -> None:
        self._rows: dict[str, tuple[bytes, AssetRef]] = {}

    def put(self, blob: bytes, *, content_type: str, rights: str = "public") -> AssetRef:
        content_hash = hashlib.sha256(blob).hexdigest()
        existing = self._rows.get(content_hash)
        if existing is not None:
            return existing[1]
        ref = AssetRef(
            asset_id=f"memory:{content_hash[:16]}",
            content_hash=content_hash,
            size=len(blob),
            content_type=content_type,
            rights=rights,
        )
        self._rows[content_hash] = (bytes(blob), ref)
        return ref

    def get(self, ref: AssetRef) -> bytes:
        row = self._rows.get(ref.content_hash)
        if row is None or hashlib.sha256(row[0]).hexdigest() != ref.content_hash:
            raise AssetNotFound(f"blob {ref.content_hash[:12]} missing")
        return row[0]

    def stat(self, ref: AssetRef) -> AssetRef:
        self.get(ref)
        return ref

    def delete(self, ref: AssetRef) -> None:
        self._rows.pop(ref.content_hash, None)


def require_delivery_rights(ref: AssetRef, actor_rights: frozenset[str]) -> None:
    """Rights-filtered delivery: denied rights prevent blob delivery."""
    if ref.rights != "public" and ref.rights not in actor_rights:
        raise AssetRightsDenied(f"actor lacks {ref.rights!r} for asset {ref.asset_id}")
