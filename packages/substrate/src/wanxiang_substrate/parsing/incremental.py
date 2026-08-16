"""Incremental parsing: content/version cache + segment diff (G56E).

Parse results are cached by (source_id, version, content_hash, parser_version,
segmenter_version). A changed content hash or parser/segmenter version
invalidates the cache; segment diffs identify exactly what changed for local
re-runs. Never mutates sources or canon.
"""

from __future__ import annotations

import hashlib
import json

from wanxiang_substrate.parsing.model import ParsedDocument
from wanxiang_substrate.parsing.parser import StructureParser
from wanxiang_substrate.sources.adapter import IngestResult


class ParseCache:
    """Content/version-addressed parse cache with explicit invalidation."""

    def __init__(self) -> None:
        self._entries: dict[str, ParsedDocument] = {}

    @staticmethod
    def key(
        *,
        source_id: str,
        version: str,
        content_hash: str,
        parser_version: int,
        segmenter_version: int,
    ) -> str:
        payload = json.dumps(
            {
                "source_id": source_id,
                "version": version,
                "content_hash": content_hash,
                "parser_version": parser_version,
                "segmenter_version": segmenter_version,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get(self, key: str) -> ParsedDocument | None:
        return self._entries.get(key)

    def put(self, key: str, parsed: ParsedDocument) -> None:
        self._entries[key] = parsed

    def invalidate_source(self, source_id: str) -> int:
        keys = [k for k, doc in self._entries.items() if doc.metadata.source_id == source_id]
        for key in keys:
            del self._entries[key]
        return len(keys)


class IncrementalParser:
    """Parses only when content/version changed; supports partial diffs."""

    def __init__(self, parser: StructureParser | None = None) -> None:
        self._parser = parser or StructureParser()
        self._cache = ParseCache()

    def parse(
        self,
        result: IngestResult,
        *,
        source_id: str,
        version: str,
        content_hash: str = "",
    ) -> tuple[ParsedDocument, bool]:
        key = ParseCache.key(
            source_id=source_id,
            version=version,
            content_hash=content_hash or result.content,
            parser_version=self._parser.parser_version,
            segmenter_version=self._parser.segmenter_version,
        )
        cached = self._cache.get(key)
        if cached is not None:
            return cached, True
        parsed = self._parser.parse(
            result, source_id=source_id, version=version, content_hash=content_hash
        )
        self._cache.put(key, parsed)
        return parsed, False

    def invalidate(self, source_id: str) -> int:
        return self._cache.invalidate_source(source_id)


def changed_segments(previous: ParsedDocument, current: ParsedDocument) -> tuple[str, ...]:
    """Segment/node ids whose content hash changed between parses."""
    before = {node.node_id: node.content_hash for node in previous.nodes}
    after = {node.node_id: node.content_hash for node in current.nodes}
    changed: list[str] = []
    for node_id in sorted(set(before) | set(after)):
        if before.get(node_id) != after.get(node_id):
            changed.append(node_id)
    return tuple(changed)
