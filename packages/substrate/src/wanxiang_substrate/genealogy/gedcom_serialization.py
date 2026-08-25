"""Deterministic serialization for the normalized GEDCOM model."""

from __future__ import annotations

from wanxiang_substrate.genealogy.model import GedcomDocument, GedcomEvent


def serialize_document(doc: GedcomDocument) -> str:
    """Write a deterministic GEDCOM representation of the normalized model."""
    lines = ["0 HEAD", "1 GEDC", f"2 VERS {doc.version}"]
    if doc.header_source:
        lines.append(f"1 SOUR {doc.header_source}")
        if doc.header_source_version:
            lines.append(f"2 VERS {doc.header_source_version}")
    lines.extend(f"1 {tag} {value}".rstrip() for tag, value in doc.header_extensions)
    lines.append("0 @SUBM@ SUBM")
    for source in sorted(doc.sources, key=lambda item: item.xref):
        lines.append(f"0 @{source.xref}@ SOUR")
        if source.title:
            lines.append(f"1 TITL {source.title}")
        if source.author:
            lines.append(f"1 AUTH {source.author}")
        if source.note:
            lines.append(f"1 NOTE {source.note}")
        lines.extend(f"1 {tag} {value}".rstrip() for tag, value in source.extensions)
    for indi in sorted(doc.individuals, key=lambda item: item.xref):
        lines.append(f"0 @{indi.xref}@ INDI")
        lines.append(f"1 NAME {indi.name}")
        if indi.given_name:
            lines.append(f"2 GIVN {indi.given_name}")
        if indi.surname:
            lines.append(f"2 SURN {indi.surname}")
        if indi.sex:
            lines.append(f"1 SEX {indi.sex}")
        lines.extend(f"1 FAMC @{value}@" for value in indi.family_child_refs)
        lines.extend(f"1 FAMS @{value}@" for value in indi.family_spouse_refs)
        lines.extend(serialize_event(event) for event in indi.events)
        if indi.place and not any(event.place == indi.place for event in indi.events):
            lines.append(f"1 PLAC {indi.place}")
        lines.extend(f"1 ALIA {value}" for value in indi.aliases)
        lines.extend(f"1 SOUR @{value}@" for value in indi.source_refs)
        lines.extend(f"1 OBJE @{value}@" for value in indi.media_refs)
        lines.extend(f"1 {tag} {value}".rstrip() for tag, value in indi.extensions)
    for family in sorted(doc.families, key=lambda item: item.xref):
        lines.append(f"0 @{family.xref}@ FAM")
        if family.husband_xref:
            lines.append(f"1 HUSB @{family.husband_xref}@")
        if family.wife_xref:
            lines.append(f"1 WIFE @{family.wife_xref}@")
        lines.extend(f"1 CHIL @{value}@" for value in family.child_xrefs)
        lines.extend(serialize_event(event) for event in family.events)
        lines.extend(f"1 SOUR @{value}@" for value in family.source_refs)
        lines.extend(f"1 {tag} {value}".rstrip() for tag, value in family.extensions)
    lines.append("0 TRLR")
    return "\n".join(lines)


def serialize_event(event: GedcomEvent) -> str:
    lines = [f"1 {event.tag}" + (f" {event.value}" if event.value else "")]
    if event.date:
        lines.append(f"2 DATE {event.date}")
    if event.place:
        lines.append(f"2 PLAC {event.place}")
    lines.extend(f"2 {tag} {value}".rstrip() for tag, value in event.extensions)
    return "\n".join(lines)
