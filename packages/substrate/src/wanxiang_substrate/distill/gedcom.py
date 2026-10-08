"""Shared generic GEDCOM views used by deterministic and local passes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wanxiang_substrate.genealogy.model import GedcomDocument, GedcomEvent


def document_for_segment(text: str) -> GedcomDocument | None:
    """Return the normalized GEDCOM record, or None for other formats."""
    from wanxiang_substrate.genealogy.gedcom import parse_gedcom

    document = parse_gedcom(text)
    return document if document.individuals or document.families or document.sources else None


def identity_key(source_id: str, xref: str) -> str:
    """Scope a GEDCOM XREF to its immutable source identity."""
    return f"gedcom:{source_id}:{xref}"


def family_key(source_id: str, xref: str) -> str:
    return f"gedcom:{source_id}:family:{xref}"


def event_kind(tag: str) -> str:
    return {
        "BIRT": "birth",
        "DEAT": "death",
        "MARR": "marriage",
        "DIV": "divorce",
        "RESI": "residence",
        "EMIG": "migration",
        "IMMI": "migration",
        "EDUC": "education",
        "OCCU": "occupation",
    }.get(tag, tag.lower())


def event_fields(
    event: GedcomEvent,
    *,
    subject_xref: str = "",
    family_xref: str = "",
) -> dict[str, str]:
    fields = {
        "event_type": event_kind(event.tag),
        "gedcom_tag": event.tag,
        "date": event.date or "unknown",
        "date_raw": event.date or "",
        "date_precision": event.date_precision,
        "uncertain": str(event.uncertain).lower(),
    }
    if subject_xref:
        fields["subject_xref"] = subject_xref
    if family_xref:
        fields["family_xref"] = family_xref
    if event.place:
        fields["place"] = event.place
    if event.value:
        fields["value"] = event.value
    return fields


def claim_fields(
    *,
    proposition: str,
    value: str,
    xref: str = "",
    family_xref: str = "",
) -> dict[str, str]:
    fields = {"proposition": proposition, "value": value}
    if xref:
        fields["subject_xref"] = xref
    if family_xref:
        fields["family_xref"] = family_xref
    return fields


__all__ = [
    "claim_fields",
    "document_for_segment",
    "event_fields",
    "event_kind",
    "family_key",
    "identity_key",
]
