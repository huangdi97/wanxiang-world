"""Large-source chunking, cache, and recovery records (M59/M60)."""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceChunk:
    source_id: str
    ordinal: int
    text: str
    content_hash: str


@dataclass(frozen=True, slots=True)
class ParseRecovery:
    source_id: str
    next_ordinal: int
    source_hash: str
    completed: bool = False


class SourceChunker:
    """Deterministic chunk view; it avoids a second source storage system."""

    def __init__(self, chunk_chars: int = 4096) -> None:
        if chunk_chars <= 0:
            raise ValueError("chunk_chars must be positive")
        self._chunk_chars = chunk_chars

    def chunks(self, source_id: str, content: str) -> tuple[SourceChunk, ...]:
        return tuple(self.iter_chunks(source_id, content))

    def iter_chunks(self, source_id: str, content: str) -> Iterator[SourceChunk]:
        """Yield bounded chunks without retaining the whole chunk list."""
        for ordinal, start in enumerate(range(0, len(content), self._chunk_chars)):
            text = content[start : start + self._chunk_chars]
            yield SourceChunk(
                source_id=source_id,
                ordinal=ordinal,
                text=text,
                content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            )

    def recovery(self, source_id: str, content: str, next_ordinal: int) -> ParseRecovery:
        if next_ordinal < 0:
            raise ValueError("next_ordinal must be non-negative")
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        chunk_count = (len(content) + self._chunk_chars - 1) // self._chunk_chars
        return ParseRecovery(source_id, next_ordinal, digest, next_ordinal >= chunk_count)


class ContentHashCache:
    """Small deterministic cache keyed by source id/version/content hash."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str, str], tuple[SourceChunk, ...]] = {}

    def put(
        self, source_id: str, version: str, content: str, chunks: tuple[SourceChunk, ...]
    ) -> None:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        self._entries[(source_id, version, content_hash)] = chunks

    def get(self, source_id: str, version: str, content: str) -> tuple[SourceChunk, ...] | None:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return self._entries.get((source_id, version, content_hash))
