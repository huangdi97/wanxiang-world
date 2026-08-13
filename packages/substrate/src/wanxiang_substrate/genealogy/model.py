"""GEDCOM normalized intermediate model (G09A)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


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


@dataclass(frozen=True, slots=True)
class GedcomDocument:
    """Parsed GEDCOM document (round-trip stable)."""

    individuals: tuple[GedcomIndividual, ...]
    families: tuple[GedcomFamily, ...]
    sources: tuple[GedcomSource, ...]
    version: str = "5.5"
    diagnostics: tuple[str, ...] = ()

    def individual(self, xref: str) -> GedcomIndividual | None:
        for indi in self.individuals:
            if indi.xref == xref:
                return indi
        return None
