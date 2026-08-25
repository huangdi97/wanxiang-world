"""GEDCOM normalized intermediate model (G09A/M82).

The model keeps imported facts reversible: dates retain their raw form and
precision, relationships retain XREFs, and unknown tags remain extensions.
Nothing in this module promotes an imported fact to canonical truth.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


@dataclass(frozen=True, slots=True)
class GedcomEvent:
    """One typed GEDCOM fact with explicit date uncertainty."""

    tag: str
    date: str = ""
    place: str = ""
    date_precision: str = "unknown"
    uncertain: bool = True
    value: str = ""
    extensions: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.tag:
            raise ContractError("GEDCOM event requires a tag")


@dataclass(frozen=True, slots=True)
class GedcomIndividual:
    """A normalized GEDCOM individual with source/media references."""

    xref: str
    name: str
    birth_date: str = ""
    death_date: str = ""
    place: str = ""
    source_refs: tuple[str, ...] = ()
    media_refs: tuple[str, ...] = ()
    extensions: tuple[tuple[str, str], ...] = ()
    living: bool = False
    given_name: str = ""
    surname: str = ""
    aliases: tuple[str, ...] = ()
    sex: str = ""
    family_child_refs: tuple[str, ...] = ()
    family_spouse_refs: tuple[str, ...] = ()
    events: tuple[GedcomEvent, ...] = ()

    def __post_init__(self) -> None:
        if not self.xref:
            raise ContractError("individual requires an xref")


@dataclass(frozen=True, slots=True)
class GedcomFamily:
    """A normalized GEDCOM family linking individuals."""

    xref: str
    husband_xref: str = ""
    wife_xref: str = ""
    child_xrefs: tuple[str, ...] = ()
    source_refs: tuple[str, ...] = ()
    marriage_date: str = ""
    marriage_place: str = ""
    events: tuple[GedcomEvent, ...] = ()
    extensions: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.xref:
            raise ContractError("family requires an xref")


@dataclass(frozen=True, slots=True)
class GedcomSource:
    """A GEDCOM source record (preserved, never discarded)."""

    xref: str
    title: str = ""
    author: str = ""
    note: str = ""
    extensions: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class GedcomDocument:
    """Parsed GEDCOM document (round-trip stable)."""

    individuals: tuple[GedcomIndividual, ...]
    families: tuple[GedcomFamily, ...]
    sources: tuple[GedcomSource, ...]
    version: str = "5.5"
    diagnostics: tuple[str, ...] = ()
    header_source: str = ""
    header_source_version: str = ""
    header_extensions: tuple[tuple[str, str], ...] = ()

    def individual(self, xref: str) -> GedcomIndividual | None:
        for indi in self.individuals:
            if indi.xref == xref:
                return indi
        return None
