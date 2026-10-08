"""G55F: Asset adapter — GenericAsset registration, optional semantics (M52)."""

from __future__ import annotations

import pathlib
import uuid
from collections.abc import Iterator

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.assets.storage import LocalObjectStore
from wanxiang_substrate.sources.adapter import AdapterRegistry
from wanxiang_substrate.sources.asset import AssetAdapter, GenericAsset, kind_for, register_asset
from wanxiang_substrate.sources.blob import SourceBlobStore
from wanxiang_substrate.sources.errors import UnsupportedSource
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

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


def _record(kind: str) -> SourceRecord:
    return SourceRecord(
        source_id=f"src_{kind}",
        kind=kind,
        content_hash=payload_hash(f"fixture:{kind}"),
        content_ref="ref://asset",
        stage="E1",
        rights=RightsEnvelope(owner="o", usage="u", approved=True),
        payload="",
        provenance="fixture:g55f",
    )


@pytest.mark.unit
def test_kind_for_extension_and_kind() -> None:
    assert kind_for("photo.png") == "image"
    assert kind_for("song.mp3") == "audio"
    assert kind_for("clip.mp4") == "video"
    assert kind_for("", kind="image") == "image"
    assert kind_for("", kind="audio") == "audio"
    assert kind_for("", kind="text") is None


@pytest.mark.unit
def test_asset_adapter_handles_media() -> None:
    adapter = AssetAdapter(SourceBlobStore(LocalObjectStore(BLOB_ROOT / "probe")))
    assert adapter.can_handle(kind="image")
    assert adapter.can_handle(kind="video")
    assert adapter.can_handle(kind="text", filename="photo.jpg")
    assert not adapter.can_handle(kind="text", filename="book.txt")


@pytest.mark.unit
def test_inspect_reports_no_text_and_no_fake_semantics(blob_store: SourceBlobStore) -> None:
    adapter = AssetAdapter(blob_store)
    inspection = adapter.inspect(_record("image"))
    assert inspection.text_available is False
    assert inspection.ocr_required is False
    assert "semantic_understanding_capability=unavailable" in inspection.diagnostics


@pytest.mark.unit
def test_ingest_registers_blob_without_fabricated_content(blob_store: SourceBlobStore) -> None:
    adapter = AssetAdapter(blob_store)
    result = adapter.ingest(_record("image"), b"\x89PNG-fake")
    assert result.content == ""  # no fake caption/transcript
    assert result.blob_ref is not None
    assert blob_store.load(result.blob_ref) == b"\x89PNG-fake"


@pytest.mark.unit
def test_register_asset_generic() -> None:
    store = SourceBlobStore(LocalObjectStore(BLOB_ROOT / "probe2"))
    asset = register_asset(_record("audio"), b"fake-mp3", store, mime_type="audio/mpeg")
    assert isinstance(asset, GenericAsset)
    assert asset.kind == "audio"
    assert asset.semantic_available is False
    assert asset.blob_ref.content_hash
    assert store.load(asset.blob_ref) == b"fake-mp3"


@pytest.mark.unit
def test_unsupported_kind_rejected(blob_store: SourceBlobStore) -> None:
    adapter = AssetAdapter(blob_store)
    with pytest.raises(UnsupportedSource):
        adapter.ingest(_record("text"))


@pytest.mark.unit
def test_invalid_generic_asset_rejected(blob_store: SourceBlobStore) -> None:
    from wanxiang_substrate.sources.blob import BlobRef

    ref = BlobRef(blob_id="b", content_hash="a" * 64, size=1, content_type="image/png")
    with pytest.raises(ContractError):
        GenericAsset(asset_id="", kind="image", mime_type="x", blob_ref=ref, size=1)
    with pytest.raises(ContractError):
        GenericAsset(asset_id="a", kind="text", mime_type="x", blob_ref=ref, size=1)  # type: ignore[arg-type]


@pytest.mark.unit
def test_asset_adapter_works_in_registry(blob_store: SourceBlobStore) -> None:
    registry = AdapterRegistry((AssetAdapter(blob_store),))
    assert registry.select(kind="video") is not None
    result = registry.ingest(_record("video"), b"fake-video")
    assert result.blob_ref is not None
