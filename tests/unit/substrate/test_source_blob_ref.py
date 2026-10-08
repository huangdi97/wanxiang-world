"""G55B: content-addressed source/blob/asset reference (M52)."""

from __future__ import annotations

import pathlib
import uuid
from collections.abc import Iterator

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.assets.storage import LocalObjectStore
from wanxiang_substrate.sources.blob import BlobRef, SourceBlobStore, is_blob_uri

ROOT = pathlib.Path(__file__).resolve().parents[3]
BLOB_ROOT = ROOT / "tests" / "_arch_tmp"


@pytest.fixture()
def blob_store() -> Iterator[SourceBlobStore]:
    d = BLOB_ROOT / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield SourceBlobStore(LocalObjectStore(d))
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


@pytest.mark.unit
def test_store_and_roundtrip(blob_store: SourceBlobStore) -> None:
    blob = b"pdf-bytes-placeholder"
    ref = blob_store.store(blob, content_type="application/pdf")
    assert ref.content_hash == ref.content_hash
    assert ref.size == len(blob)
    assert blob_store.load(ref) == blob


@pytest.mark.unit
def test_same_content_deduplicates(blob_store: SourceBlobStore) -> None:
    blob = b"duplicate-bytes"
    first = blob_store.store(blob, content_type="application/octet-stream")
    second = blob_store.store(blob, content_type="application/octet-stream")
    assert first.blob_id == second.blob_id
    assert blob_store.locate(first.content_hash) is not None


@pytest.mark.unit
def test_different_content_distinct_blobs(blob_store: SourceBlobStore) -> None:
    a = blob_store.store(b"aaa", content_type="text/plain")
    b = blob_store.store(b"bbb", content_type="text/plain")
    assert a.blob_id != b.blob_id
    assert a.content_hash != b.content_hash


@pytest.mark.unit
def test_size_guard_enforced(blob_store: SourceBlobStore) -> None:
    import pathlib as _pl
    import uuid as _uuid

    d = _pl.Path(__file__).resolve().parents[3] / "tests" / "_arch_tmp" / _uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    small = SourceBlobStore(LocalObjectStore(d), max_bytes=10)
    with pytest.raises(ContractError):
        small.store(b"x" * 100, content_type="text/plain")


@pytest.mark.unit
def test_uri_scheme_detection() -> None:
    ref = BlobRef(blob_id="blob_1", content_hash="a" * 64, size=3, content_type="text/plain")
    assert ref.uri().startswith("blob://")
    assert is_blob_uri(ref.uri())
    assert not is_blob_uri("file:///local/path")


@pytest.mark.unit
def test_invalid_blob_ref_rejected() -> None:
    with pytest.raises(ContractError):
        BlobRef(blob_id="", content_hash="a" * 64, size=1, content_type="text/plain")
    with pytest.raises(ContractError):
        BlobRef(blob_id="b", content_hash="short", size=1, content_type="text/plain")
    with pytest.raises(ContractError):
        BlobRef(blob_id="b", content_hash="a" * 64, size=-1, content_type="text/plain")
