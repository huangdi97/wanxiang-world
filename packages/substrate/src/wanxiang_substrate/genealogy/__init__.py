"""Genealogy / family substrate (G09A-G09C)."""

from wanxiang_substrate.genealogy.errors import (
    GedcomParseError,
    GenealogyError,
    InvalidKinship,
    PrivacyDenied,
)
from wanxiang_substrate.genealogy.family import (
    FamilyClaim,
    FamilyWorld,
    Kinship,
    KinshipRole,
    LifeEvent,
    Person,
)
from wanxiang_substrate.genealogy.gedcom import (
    SUPPORTED_PROFILE,
    parse_gedcom,
    serialize_gedcom,
)
from wanxiang_substrate.genealogy.model import (
    GedcomDocument,
    GedcomFamily,
    GedcomIndividual,
    GedcomSource,
)
from wanxiang_substrate.genealogy.privacy import (
    ConsentState,
    LivingArchive,
    PersonaMode,
    mode_label,
)

__all__ = [
    "ConsentState",
    "FamilyClaim",
    "FamilyWorld",
    "GedcomDocument",
    "GedcomFamily",
    "GedcomIndividual",
    "GedcomParseError",
    "GedcomSource",
    "GenealogyError",
    "InvalidKinship",
    "Kinship",
    "KinshipRole",
    "LifeEvent",
    "LivingArchive",
    "Person",
    "PersonaMode",
    "PrivacyDenied",
    "SUPPORTED_PROFILE",
    "mode_label",
    "parse_gedcom",
    "serialize_gedcom",
]
