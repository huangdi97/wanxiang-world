"""Generic asset registration adapter (G55F).

Images/audio/video are REGISTERED as content-addressed GenericAsset references;
semantic understanding (vision/ASR) is an OPTIONAL capability. When no provider
is available the adapter honestly reports semantic_available=False and never
fabricates a transcript/caption. Adapters only register assets; they never
mutate sources or canon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.adapter import IngestResult, SourceAdapter, SourceInspection
from wanxiang_substrate.sources.blob import BlobRef, SourceBlobStore
from wanxiang_substrate.sources.errors import UnsupportedSource
from wanxiang_substrate.sources.model import SourceRecord

AssetKind = Literal["image", "audio", "video", "other"]
VALID_ASSET_KINDS = ("image", "audio", "video", "other")
_ASSET_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
)

_EXTENSION_TO_KIND: dict[str, AssetKind] = {
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".webp": "image",
    ".bmp": "image",
    ".mp3": "audio",
    ".wav": "audio",
    ".flac": "audio",
    ".ogg": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".webm": "video",
    ".mkv": "video",
}


@dataclass(frozen=True, slots=True)
class GenericAsset:
    """A registered media asset; semantic understanding is optional."""

    asset_id: str
    kind: AssetKind
    mime_type: str
    blob_ref: BlobRef
    size: int
    semantic_available: bool = False
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.asset_id:
            raise ContractError("asset requires an id")
        if self.kind not in VALID_ASSET_KINDS:
            raise ContractError(f"invalid asset kind {self.kind!r}")
        if self.size < 0:
            raise ContractError("asset size must be non-negative")


def kind_for(filename: str, *, kind: str = "") -> AssetKind | None:
    lowered = filename.lower()
    for extension, asset_kind in _EXTENSION_TO_KIND.items():
        if lowered.endswith(extension):
            return asset_kind
    if kind in VALID_ASSET_KINDS:
        return kind  # type: ignore[return-value]
    return None


class AssetAdapter(SourceAdapter):
    """Registers image/audio/video as GenericAsset (no fake understanding)."""

    name = "generic_asset"

    def can_handle(
        self,
        *,
        kind: str,
        filename: str = "",
        content_type: str = "",
    ) -> bool:
        lowered = filename.lower() if filename else ""
        return (
            kind in ("image", "audio", "video", "asset", "generic_asset")
            or lowered.endswith(_ASSET_EXTENSIONS)
            or content_type.startswith(("image/", "audio/", "video/"))
        )

    def inspect(self, record: SourceRecord) -> SourceInspection:
        return SourceInspection(
            source_id=record.source_id,
            detected_format=record.kind,
            text_available=False,
            ocr_required=False,
            size_bytes=len(record.payload.encode("utf-8")),
            diagnostics=("semantic_understanding_capability=unavailable",),
        )

    def ingest(
        self,
        record: SourceRecord,
        blob: bytes | None = None,
    ) -> IngestResult:
        asset_kind = kind_for("", kind=record.kind)
        if asset_kind is None:
            raise UnsupportedSource(f"asset adapter cannot ingest kind {record.kind!r}")
        blob_ref = None
        if blob is not None:
            blob_ref = self._blob_store.store(
                blob, content_type=f"{asset_kind}/octet-stream", kind="asset"
            )
        return IngestResult(
            source_id=record.source_id,
            kind=record.kind,
            content="",
            detected_format=record.kind,
            blob_ref=blob_ref,
            diagnostics=("semantic_understanding_capability=unavailable",),
        )

    def resume(self, source_id: str) -> IngestResult | None:
        return None

    def __init__(self, blob_store: SourceBlobStore) -> None:
        self._blob_store = blob_store


def register_asset(
    record: SourceRecord,
    blob: bytes,
    blob_store: SourceBlobStore,
    *,
    mime_type: str = "application/octet-stream",
) -> GenericAsset:
    """Register a media asset as a content-addressed GenericAsset."""
    asset_kind = kind_for("", kind=record.kind)
    if asset_kind is None:
        raise UnsupportedSource(f"cannot register asset of kind {record.kind!r}")
    blob_ref = blob_store.store(blob, content_type=mime_type, kind="asset")
    return GenericAsset(
        asset_id=record.source_id,
        kind=asset_kind,
        mime_type=mime_type,
        blob_ref=blob_ref,
        size=len(blob),
        semantic_available=False,
        metadata=(("source_id", record.source_id),),
    )
