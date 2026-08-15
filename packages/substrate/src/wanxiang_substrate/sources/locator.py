"""Chapter/segment stable source locators (G35B).

Converts a source text into stable, citable chapter/segment locators WITHOUT
rewriting the original text. Locators preserve source offsets + chapter numbers
so any Canon claim can be back-linked to the exact source slice.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

_CHAPTER_RE = re.compile(r"^(第[一二三四五六七八九十百千0-9]+回|[0-9]+)\s*$")


@dataclass(frozen=True, slots=True)
class SourceLocator:
    """A stable locator into the source text (offsets + chapter)."""

    source_id: str
    chapter: str
    segment_id: str
    start_offset: int
    end_offset: int
    locator: str

    def __post_init__(self) -> None:
        if self.end_offset < self.start_offset:
            raise ContractError("locator end_offset must be >= start_offset")
        if not self.locator:
            raise ContractError("locator must be non-empty")


def segment_source(source_id: str, text: str) -> tuple[SourceLocator, ...]:
    """Segment a chapter-marked text into stable locators (read-only).

    A segment is a run of lines after a chapter marker; the original text is
    never modified. Re-running on the same text yields identical locators.
    """
    lines = text.splitlines()
    locators: list[SourceLocator] = []
    current_chapter = "front"
    chapter_start = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if _CHAPTER_RE.match(stripped):
            if index > chapter_start:
                locators.append(
                    SourceLocator(
                        source_id=source_id,
                        chapter=current_chapter,
                        segment_id=f"{source_id}:{current_chapter}:{chapter_start}-{index}",
                        start_offset=chapter_start,
                        end_offset=index,
                        locator=f"{source_id}#{current_chapter}:{chapter_start}-{index}",
                    )
                )
            current_chapter = stripped
            chapter_start = index + 1
    if len(lines) > chapter_start:
        locators.append(
            SourceLocator(
                source_id=source_id,
                chapter=current_chapter,
                segment_id=f"{source_id}:{current_chapter}:{chapter_start}-{len(lines)}",
                start_offset=chapter_start,
                end_offset=len(lines),
                locator=f"{source_id}#{current_chapter}:{chapter_start}-{len(lines)}",
            )
        )
    return tuple(locators)


def source_slice(text: str, locator: SourceLocator) -> str:
    """Read the exact source slice a locator points at (original text untouched)."""
    lines = text.splitlines()
    return "\n".join(lines[locator.start_offset : locator.end_offset])


def locator_stable_hash(locators: tuple[SourceLocator, ...]) -> str:
    payload = "|".join(item.locator for item in locators)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
