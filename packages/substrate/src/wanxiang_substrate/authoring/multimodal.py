"""Multimodal source contracts with deterministic capability checks (M62)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MediaLocator:
    source_id: str
    media_kind: str
    start_ms: int = 0
    end_ms: int | None = None
    page: int | None = None
    region: str | None = None

    def to_string(self) -> str:
        suffix = f"@{self.start_ms}-{self.end_ms or ''}"
        if self.page is not None:
            suffix += f"/page/{self.page}"
        if self.region:
            suffix += f"/region/{self.region}"
        return f"{self.media_kind}://{self.source_id}{suffix}"


@dataclass(frozen=True, slots=True)
class SubtitleCue:
    cue_id: str
    start_ms: int
    end_ms: int
    text: str
    source_id: str


@dataclass(frozen=True, slots=True)
class BundleEntry:
    source_id: str
    kind: str
    content_hash: str
    rights_approved: bool
    private: bool = False


@dataclass(frozen=True, slots=True)
class SourceBundleManifest:
    bundle_id: str
    entries: tuple[BundleEntry, ...]
    manifest_hash: str

    @classmethod
    def build(cls, bundle_id: str, entries: tuple[BundleEntry, ...]) -> SourceBundleManifest:
        payload = [
            {
                "source_id": entry.source_id,
                "kind": entry.kind,
                "content_hash": entry.content_hash,
                "rights_approved": entry.rights_approved,
                "private": entry.private,
            }
            for entry in sorted(entries, key=lambda item: item.source_id)
        ]
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return cls(
            bundle_id=bundle_id,
            entries=tuple(sorted(entries, key=lambda item: item.source_id)),
            manifest_hash=digest,
        )

    @property
    def rights_ok(self) -> bool:
        return all(entry.rights_approved for entry in self.entries)

    @property
    def private_source_ids(self) -> tuple[str, ...]:
        return tuple(entry.source_id for entry in self.entries if entry.private)
