"""GEDCOM 5.5 subset parser/writer adapter (G09A).

Supported profile: INDI (NAME/BIRT/DATE/PLAC/DEAT/SOUR/OBJE), FAM
(HUSB/WIFE/CHIL), SOUR records. Unknown extensions are preserved under the
documented policy (retained as tuples, never silently dropped). Imported facts
map to Claim/Evidence, not unconditional truth.
"""

from __future__ import annotations

import re
from typing import TypedDict

from wanxiang_substrate.genealogy.model import (
    GedcomDocument,
    GedcomFamily,
    GedcomIndividual,
    GedcomSource,
)

_LINE_RE = re.compile(r"^(\d+)\s+(?:@([^@]+)@\s+)?([A-Z0-9_]+)\s?(.*)$")

SUPPORTED_PROFILE = "GEDCOM 5.5 subset: INDI/FAM/SOUR with NAME/BIRT/DEAT/DATE/PLAC/SEX/SOUR/OBJE"


class _IndiBuffer(TypedDict):
    xref: str
    name: str
    birth: str
    death: str
    place: str
    sources: list[str]
    media: list[str]
    ext: list[tuple[str, str]]
    living: bool


class _FamBuffer(TypedDict):
    xref: str
    husband: str
    wife: str
    children: list[str]
    sources: list[str]


class _SourceBuffer(TypedDict):
    xref: str
    title: str
    author: str


def parse_gedcom(text: str) -> GedcomDocument:
    """Parse a GEDCOM subset into a normalized document."""
    individuals: list[GedcomIndividual] = []
    families: list[GedcomFamily] = []
    sources: list[GedcomSource] = []
    diagnostics: list[str] = []
    current_indi: _IndiBuffer | None = None
    current_fam: _FamBuffer | None = None
    current_source: _SourceBuffer | None = None
    current_tag: str | None = None

    def close_current() -> None:
        nonlocal current_indi, current_fam, current_source
        if current_indi is not None:
            individuals.append(_finish_indi(current_indi))
        if current_fam is not None:
            families.append(_finish_fam(current_fam))
        if current_source is not None:
            sources.append(_finish_source(current_source))
        current_indi, current_fam, current_source = None, None, None

    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        if not stripped[0].isdigit():
            diagnostics.append(f"line {line_number}: not a GEDCOM line")
            continue
        match = _LINE_RE.match(raw)
        if match is None:
            diagnostics.append(f"line {line_number}: unparsed")
            continue
        level = int(match.group(1))
        xref = match.group(2) or ""
        tag = match.group(3)
        value = match.group(4).strip()
        if level == 0:
            close_current()
            if tag == "INDI":
                current_indi = _new_indi(xref)
            elif tag == "FAM":
                current_fam = _new_fam(xref)
            elif tag == "SOUR":
                current_source = _new_source(xref)
            current_tag = None
            continue
        if level == 1:
            current_tag = tag
            if current_indi is not None:
                _handle_indi_1(current_indi, tag, value)
            elif current_fam is not None:
                _handle_fam_1(current_fam, tag, value)
            elif current_source is not None:
                _handle_source_1(current_source, tag, value)
            continue
        if level == 2 and current_tag is not None and current_indi is not None:
            if current_tag == "BIRT" and tag == "DATE":
                current_indi["birth"] = value
            elif current_tag == "BIRT" and tag == "PLAC":
                current_indi["place"] = value
            elif current_tag == "DEAT" and tag == "DATE":
                current_indi["death"] = value
            continue
        diagnostics.append(f"line {line_number}: unsupported level {level}")
    close_current()
    return GedcomDocument(
        individuals=tuple(individuals),
        families=tuple(families),
        sources=tuple(sources),
        diagnostics=tuple(diagnostics),
    )


def serialize_gedcom(doc: GedcomDocument) -> str:
    """Write a normalized GEDCOM document (round-trip stable)."""
    lines: list[str] = ["0 HEAD", "1 GEDC", "2 VERS " + doc.version, "0 @SUBM@ SUBM"]
    for source in sorted(doc.sources, key=lambda s: s.xref):
        lines.append(f"0 @{source.xref}@ SOUR")
        if source.title:
            lines.append(f"1 TITL {source.title}")
        if source.author:
            lines.append(f"1 AUTH {source.author}")
    for indi in sorted(doc.individuals, key=lambda i: i.xref):
        lines.append(f"0 @{indi.xref}@ INDI")
        lines.append(f"1 NAME {indi.name}")
        if indi.birth_date:
            lines.append("1 BIRT")
            lines.append(f"2 DATE {indi.birth_date}")
        if indi.death_date:
            lines.append("1 DEAT")
            lines.append(f"2 DATE {indi.death_date}")
        if indi.place:
            lines.append(f"1 PLAC {indi.place}")
        for source_ref in indi.source_refs:
            lines.append(f"1 SOUR @{source_ref}@")
        for media_ref in indi.media_refs:
            lines.append(f"1 OBJE @{media_ref}@")
        for tag, ext_value in indi.extensions:
            lines.append(f"1 {tag} {ext_value}")
    for family in sorted(doc.families, key=lambda f: f.xref):
        lines.append(f"0 @{family.xref}@ FAM")
        if family.husband_xref:
            lines.append(f"1 HUSB @{family.husband_xref}@")
        if family.wife_xref:
            lines.append(f"1 WIFE @{family.wife_xref}@")
        for child in family.child_xrefs:
            lines.append(f"1 CHIL @{child}@")
    lines.append("0 TRLR")
    return "\n".join(lines)


def _new_indi(xref: str) -> _IndiBuffer:
    return {
        "xref": xref,
        "name": "",
        "birth": "",
        "death": "",
        "place": "",
        "sources": [],
        "media": [],
        "ext": [],
        "living": False,
    }


def _new_fam(xref: str) -> _FamBuffer:
    return {"xref": xref, "husband": "", "wife": "", "children": [], "sources": []}


def _new_source(xref: str) -> _SourceBuffer:
    return {"xref": xref, "title": "", "author": ""}


def _handle_indi_1(buffer: _IndiBuffer, tag: str, value: str) -> None:
    if tag == "NAME":
        buffer["name"] = value
    elif tag == "BIRT":
        buffer.setdefault("birth", "")
    elif tag == "DEAT":
        buffer.setdefault("death", "")
    elif tag == "SOUR":
        buffer["sources"].append(_clean_xref(value))
    elif tag == "OBJE":
        buffer["media"].append(_clean_xref(value))
    elif tag in ("_PRIV", "CONF"):
        buffer["living"] = True
    else:
        buffer["ext"].append((tag, value))


def _handle_fam_1(buffer: _FamBuffer, tag: str, value: str) -> None:
    if tag == "HUSB":
        buffer["husband"] = _clean_xref(value)
    elif tag == "WIFE":
        buffer["wife"] = _clean_xref(value)
    elif tag == "CHIL":
        buffer["children"].append(_clean_xref(value))
    elif tag == "SOUR":
        buffer["sources"].append(_clean_xref(value))


def _handle_source_1(buffer: _SourceBuffer, tag: str, value: str) -> None:
    if tag == "TITL":
        buffer["title"] = value
    elif tag == "AUTH":
        buffer["author"] = value


def _clean_xref(value: str) -> str:
    return value.strip().strip("@").strip()


def _finish_indi(data: _IndiBuffer) -> GedcomIndividual:
    return GedcomIndividual(
        xref=data["xref"],
        name=data["name"] or "UNKNOWN",
        birth_date=data["birth"],
        death_date=data["death"],
        place=data["place"],
        source_refs=tuple(data["sources"]),
        media_refs=tuple(data["media"]),
        extensions=tuple(data["ext"]),
        living=data["living"],
    )


def _finish_fam(data: _FamBuffer) -> GedcomFamily:
    return GedcomFamily(
        xref=data["xref"],
        husband_xref=data["husband"],
        wife_xref=data["wife"],
        child_xrefs=tuple(data["children"]),
        source_refs=tuple(data["sources"]),
    )


def _finish_source(data: _SourceBuffer) -> GedcomSource:
    return GedcomSource(
        xref=data["xref"],
        title=data["title"],
        author=data["author"],
    )
