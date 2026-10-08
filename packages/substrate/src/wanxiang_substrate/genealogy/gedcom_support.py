"""Internal typed helpers for the generic GEDCOM boundary."""

from __future__ import annotations

import re
from typing import TypedDict

from wanxiang_substrate.genealogy.model import (
    GedcomEvent,
    GedcomFamily,
    GedcomIndividual,
    GedcomSource,
)

LINE_RE = re.compile(r"^(\d+)\s+(?:@([^@]+)@\s+)?([A-Z0-9_]+)\s?(.*)$")
EVENT_TAGS = frozenset(
    {
        "BIRT",
        "DEAT",
        "MARR",
        "DIV",
        "ANUL",
        "CENS",
        "BAPM",
        "CHR",
        "BURI",
        "CREM",
        "ADOP",
        "EMIG",
        "IMMI",
        "NATU",
        "ORDN",
        "PROB",
        "RETI",
        "WILL",
        "RESI",
        "EDUC",
        "OCCU",
        "EVEN",
        "CAST",
        "DSCR",
        "GRAD",
        "RELI",
        "CONF",
    }
)
_DATE_DAY_RE = re.compile(r"(?:\d{1,2}\s+)?[A-Z]{3}\s+\d{4}$", re.I)
_DATE_MONTH_RE = re.compile(r"(?:\d{4}[-/]\d{1,2}|[A-Z]{3}\s+\d{4})$", re.I)


class IndiBuffer(TypedDict):
    xref: str
    name: str
    birth: str
    death: str
    place: str
    sources: list[str]
    media: list[str]
    ext: list[tuple[str, str]]
    living: bool
    given: str
    surname: str
    aliases: list[str]
    sex: str
    famc: list[str]
    fams: list[str]
    events: list[GedcomEvent]


class FamBuffer(TypedDict):
    xref: str
    husband: str
    wife: str
    children: list[str]
    sources: list[str]
    events: list[GedcomEvent]
    ext: list[tuple[str, str]]


class SourceBuffer(TypedDict):
    xref: str
    title: str
    author: str
    note: str
    ext: list[tuple[str, str]]


class EventBuffer(TypedDict):
    tag: str
    date: str
    place: str
    value: str
    ext: list[tuple[str, str]]


def new_indi(xref: str) -> IndiBuffer:
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
        "given": "",
        "surname": "",
        "aliases": [],
        "sex": "",
        "famc": [],
        "fams": [],
        "events": [],
    }


def new_fam(xref: str) -> FamBuffer:
    return {
        "xref": xref,
        "husband": "",
        "wife": "",
        "children": [],
        "sources": [],
        "events": [],
        "ext": [],
    }


def new_source(xref: str) -> SourceBuffer:
    return {"xref": xref, "title": "", "author": "", "note": "", "ext": []}


def handle_indi_1(buffer: IndiBuffer, tag: str, value: str) -> None:
    if tag == "NAME":
        buffer["name"] = value
        buffer["given"], buffer["surname"] = split_name(value)
    elif tag == "GIVN":
        buffer["given"] = value
    elif tag == "SURN":
        buffer["surname"] = value
    elif tag in ("ALIA", "NICK") and value:
        buffer["aliases"].append(clean_xref(value))
    elif tag == "SEX":
        buffer["sex"] = value
    elif tag == "FAMC":
        buffer["famc"].append(clean_xref(value))
    elif tag == "FAMS":
        buffer["fams"].append(clean_xref(value))
    elif tag == "SOUR":
        buffer["sources"].append(clean_xref(value))
    elif tag == "OBJE":
        buffer["media"].append(clean_xref(value))
    elif tag in ("_PRIV", "CONF"):
        buffer["living"] = True
    else:
        buffer["ext"].append((tag, value))


def handle_indi_2(buffer: IndiBuffer, current_tag: str, tag: str, value: str) -> None:
    if current_tag == "NAME" and tag == "GIVN":
        buffer["given"] = value
    elif current_tag == "NAME" and tag == "SURN":
        buffer["surname"] = value
    else:
        buffer["ext"].append((f"{current_tag}.{tag}", value))


def handle_fam_1(buffer: FamBuffer, tag: str, value: str) -> None:
    if tag == "HUSB":
        buffer["husband"] = clean_xref(value)
    elif tag == "WIFE":
        buffer["wife"] = clean_xref(value)
    elif tag == "CHIL":
        buffer["children"].append(clean_xref(value))
    elif tag == "SOUR":
        buffer["sources"].append(clean_xref(value))
    else:
        buffer["ext"].append((tag, value))


def handle_source_1(buffer: SourceBuffer, tag: str, value: str) -> None:
    if tag == "TITL":
        buffer["title"] = value
    elif tag == "AUTH":
        buffer["author"] = value
    elif tag == "NOTE":
        buffer["note"] = value
    else:
        buffer["ext"].append((tag, value))


def finish_event(data: EventBuffer) -> GedcomEvent:
    precision, uncertain = date_metadata(data["date"])
    return GedcomEvent(
        data["tag"],
        data["date"],
        data["place"],
        precision,
        uncertain,
        data["value"],
        tuple(data["ext"]),
    )


def finish_indi(data: IndiBuffer) -> GedcomIndividual:
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
        given_name=data["given"],
        surname=data["surname"],
        aliases=tuple(data["aliases"]),
        sex=data["sex"],
        family_child_refs=tuple(data["famc"]),
        family_spouse_refs=tuple(data["fams"]),
        events=tuple(data["events"]),
    )


def finish_fam(data: FamBuffer) -> GedcomFamily:
    marriage = next((event for event in data["events"] if event.tag == "MARR"), None)
    return GedcomFamily(
        xref=data["xref"],
        husband_xref=data["husband"],
        wife_xref=data["wife"],
        child_xrefs=tuple(data["children"]),
        source_refs=tuple(data["sources"]),
        marriage_date=marriage.date if marriage else "",
        marriage_place=marriage.place if marriage else "",
        events=tuple(data["events"]),
        extensions=tuple(data["ext"]),
    )


def finish_source(data: SourceBuffer) -> GedcomSource:
    return GedcomSource(
        data["xref"], data["title"], data["author"], data["note"], tuple(data["ext"])
    )


def date_metadata(raw: str) -> tuple[str, bool]:
    """Return a conservative precision label and uncertainty flag."""
    value = " ".join(raw.strip().split())
    upper = value.upper()
    if not value:
        return "unknown", True
    if re.match(r"^(ABT|ABOUT|CAL|CALCULATED|EST|ESTIMATED|~)\b", upper):
        return "approximate", True
    if re.match(r"^(BEF|BEFORE)\b", upper):
        return "before", True
    if re.match(r"^(AFT|AFTER)\b", upper):
        return "after", True
    if re.match(r"^(BET|BETWEEN|FROM)\b", upper):
        return "range", True
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) or _DATE_DAY_RE.fullmatch(value):
        return "day", False
    if re.fullmatch(r"\d{4}", value):
        return "year", True
    if _DATE_MONTH_RE.fullmatch(value):
        return "month", True
    return "text", True


def split_name(value: str) -> tuple[str, str]:
    if "/" in value:
        before, _, after = value.partition("/")
        return before.strip(), after.strip().strip("/")
    parts = value.split()
    return (" ".join(parts[:-1]), parts[-1]) if len(parts) > 1 else (value.strip(), "")


def clean_xref(value: str) -> str:
    return value.strip().strip("@").strip()
