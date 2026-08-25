"""Generic GEDCOM parser/writer for the normalized genealogy boundary.

The parser keeps typed facts as claims with raw dates, uncertainty metadata,
XREFs, and unknown extensions. It does not decide canonical truth.
"""

from __future__ import annotations

from wanxiang_substrate.genealogy.gedcom_serialization import serialize_document
from wanxiang_substrate.genealogy.gedcom_support import (
    EVENT_TAGS,
    LINE_RE,
    EventBuffer,
    FamBuffer,
    IndiBuffer,
    SourceBuffer,
    finish_event,
    finish_fam,
    finish_indi,
    finish_source,
    handle_fam_1,
    handle_indi_1,
    handle_indi_2,
    handle_source_1,
    new_fam,
    new_indi,
    new_source,
)
from wanxiang_substrate.genealogy.model import (
    GedcomDocument,
    GedcomFamily,
    GedcomIndividual,
    GedcomSource,
)

SUPPORTED_PROFILE = (
    "GEDCOM normalized profile: INDI/FAM/SOUR, XREF links, typed events,"
    " uncertain dates, places, claims/evidence locators, and preserved extensions"
)


def parse_gedcom(text: str) -> GedcomDocument:
    """Parse a GEDCOM document while retaining all supported facts."""
    individuals: list[GedcomIndividual] = []
    families: list[GedcomFamily] = []
    sources: list[GedcomSource] = []
    diagnostics: list[str] = []
    header_extensions: list[tuple[str, str]] = []
    current_kind = ""
    current_indi: IndiBuffer | None = None
    current_fam: FamBuffer | None = None
    current_source: SourceBuffer | None = None
    current_tag = ""
    active_event: EventBuffer | None = None
    version = "5.5"
    header_source = ""
    header_source_version = ""

    def finish_active_event() -> None:
        nonlocal active_event
        if active_event is None:
            return
        event = finish_event(active_event)
        if current_indi is not None:
            current_indi["events"].append(event)
            if event.tag == "BIRT" and event.date:
                current_indi["birth"] = event.date
            if event.tag == "DEAT" and event.date:
                current_indi["death"] = event.date
            if event.place and not current_indi["place"]:
                current_indi["place"] = event.place
        elif current_fam is not None:
            current_fam["events"].append(event)
        active_event = None

    def close_record() -> None:
        nonlocal current_indi, current_fam, current_source, current_kind, current_tag
        finish_active_event()
        if current_indi is not None:
            individuals.append(finish_indi(current_indi))
        if current_fam is not None:
            families.append(finish_fam(current_fam))
        if current_source is not None:
            sources.append(finish_source(current_source))
        current_indi, current_fam, current_source = None, None, None
        current_kind, current_tag = "", ""

    for line_number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        match = LINE_RE.match(raw)
        if match is None:
            diagnostics.append(f"line {line_number}: unparsed")
            continue
        level = int(match.group(1))
        xref = match.group(2) or ""
        tag = match.group(3)
        value = match.group(4).strip()
        if level == 0:
            close_record()
            current_kind = tag
            if tag == "INDI":
                current_indi = new_indi(xref)
            elif tag == "FAM":
                current_fam = new_fam(xref)
            elif tag == "SOUR":
                current_source = new_source(xref)
            continue
        if level == 1:
            finish_active_event()
            current_tag = tag
            if tag in EVENT_TAGS and current_kind in ("INDI", "FAM"):
                active_event = EventBuffer(tag=tag, date="", place="", value=value, ext=[])
            elif current_kind == "INDI" and current_indi is not None:
                handle_indi_1(current_indi, tag, value)
            elif current_kind == "FAM" and current_fam is not None:
                handle_fam_1(current_fam, tag, value)
            elif current_kind == "SOUR" and current_source is not None:
                handle_source_1(current_source, tag, value)
            elif current_kind == "HEAD":
                if tag == "SOUR":
                    header_source = value
                elif tag not in ("GEDC", "CHAR", "DATE", "FILE", "SUBM"):
                    header_extensions.append((tag, value))
            continue
        if level >= 2:
            if active_event is not None:
                if tag == "DATE":
                    active_event["date"] = value
                elif tag == "PLAC":
                    active_event["place"] = value
                elif tag in ("VALUE", "TYPE"):
                    active_event["value"] = value
                else:
                    active_event["ext"].append((tag, value))
            elif current_kind == "HEAD":
                if current_tag == "GEDC" and tag == "VERS":
                    version = value or version
                elif current_tag == "SOUR" and tag == "VERS":
                    header_source_version = value
                else:
                    header_extensions.append((f"{current_tag}.{tag}", value))
            elif current_indi is not None:
                handle_indi_2(current_indi, current_tag, tag, value)
            elif current_fam is not None:
                current_fam["ext"].append((f"{current_tag}.{tag}", value))
            elif current_source is not None:
                current_source["ext"].append((f"{current_tag}.{tag}", value))
            continue
        diagnostics.append(f"line {line_number}: unsupported level {level}")
    close_record()
    return GedcomDocument(
        individuals=tuple(individuals),
        families=tuple(families),
        sources=tuple(sources),
        version=version,
        diagnostics=tuple(diagnostics),
        header_source=header_source,
        header_source_version=header_source_version,
        header_extensions=tuple(header_extensions),
    )


def serialize_gedcom(doc: GedcomDocument) -> str:
    """Write a deterministic GEDCOM representation of the normalized model."""
    return serialize_document(doc)


__all__ = ["SUPPORTED_PROFILE", "parse_gedcom", "serialize_gedcom"]
