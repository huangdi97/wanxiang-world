"""Multimodal source contracts with deterministic capability checks (M62)."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Protocol

from wanxiang_substrate.sources.errors import MalformedSourceContent


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

    def __post_init__(self) -> None:
        if not self.cue_id or self.start_ms < 0 or self.end_ms <= self.start_ms:
            raise ValueError("subtitle cue has invalid identity or time range")


_TIMESTAMP = re.compile(
    r"(?P<hours>\d{1,2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})[,.](?P<millis>\d{3})"
)


def _timestamp_ms(value: str) -> int:
    match = _TIMESTAMP.fullmatch(value.strip())
    if match is None:
        raise MalformedSourceContent(f"invalid subtitle timestamp {value!r}")
    return (
        int(match["hours"]) * 3_600_000
        + int(match["minutes"]) * 60_000
        + int(match["seconds"]) * 1_000
        + int(match["millis"])
    )


class SubtitleAdapter:
    """Deterministic SRT/WebVTT cue parser; it produces no semantic claim."""

    def parse(self, source_id: str, text: str) -> tuple[SubtitleCue, ...]:
        lines = text.replace("\r\n", "\n").split("\n")
        cues: list[SubtitleCue] = []
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if not line or line == "WEBVTT" or line.startswith("NOTE"):
                index += 1
                continue
            cue_id = line
            if "-->" not in line:
                if index + 1 >= len(lines) or "-->" not in lines[index + 1]:
                    raise MalformedSourceContent("subtitle cue has no timing line")
                index += 1
                timing = lines[index]
            else:
                timing = line
                cue_id = f"cue_{len(cues) + 1}"
            start_raw, end_raw = (part.strip().split(" ", 1)[0] for part in timing.split("-->", 1))
            start_ms = _timestamp_ms(start_raw)
            end_ms = _timestamp_ms(end_raw)
            index += 1
            payload: list[str] = []
            while index < len(lines) and lines[index].strip():
                payload.append(lines[index].strip())
                index += 1
            text_value = "\n".join(payload)
            if not text_value:
                raise MalformedSourceContent(f"subtitle cue {cue_id!r} is empty")
            cues.append(SubtitleCue(cue_id, start_ms, end_ms, text_value, source_id))
        if not cues:
            raise MalformedSourceContent("subtitle contains no cues")
        return tuple(cues)


@dataclass(frozen=True, slots=True)
class ExternalSourceRequest:
    source_id: str
    uri: str
    expected_hash: str = ""


@dataclass(frozen=True, slots=True)
class ConnectorObservation:
    source_id: str
    uri: str
    available: bool
    content_hash: str
    etag: str = ""
    diagnostics: tuple[str, ...] = ()


class ExternalSourceConnector(Protocol):
    """IIIF/API connector port; implementations return observations only."""

    def observe(self, request: ExternalSourceRequest) -> ConnectorObservation: ...


class ReferenceExternalConnector:
    """Offline connector that never performs network I/O in reference runs."""

    def observe(self, request: ExternalSourceRequest) -> ConnectorObservation:
        if not request.uri.startswith(("https://", "http://", "iiif://", "api://")):
            raise ValueError("external source URI must use an explicit connector scheme")
        return ConnectorObservation(
            source_id=request.source_id,
            uri=request.uri,
            available=False,
            content_hash=request.expected_hash,
            diagnostics=("EXTERNAL_FETCH_DISABLED_REFERENCE",),
        )


@dataclass(frozen=True, slots=True)
class BundleEntry:
    source_id: str
    kind: str
    content_hash: str
    rights_approved: bool
    private: bool = False

    def __post_init__(self) -> None:
        if not self.source_id or not self.kind or len(self.content_hash) != 64:
            raise ValueError("bundle entry requires source id, kind, and sha256 hash")


@dataclass(frozen=True, slots=True)
class SourceBundleManifest:
    bundle_id: str
    entries: tuple[BundleEntry, ...]
    manifest_hash: str

    @classmethod
    def build(cls, bundle_id: str, entries: tuple[BundleEntry, ...]) -> SourceBundleManifest:
        if not bundle_id or not entries:
            raise ValueError("bundle requires an id and at least one entry")
        source_ids = [entry.source_id for entry in entries]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("bundle source ids must be unique")
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
    def rights_blockers(self) -> tuple[str, ...]:
        return tuple(entry.source_id for entry in self.entries if not entry.rights_approved)

    @property
    def private_source_ids(self) -> tuple[str, ...]:
        return tuple(entry.source_id for entry in self.entries if entry.private)
