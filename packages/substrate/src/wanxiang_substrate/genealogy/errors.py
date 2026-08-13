"""Genealogy / GEDCOM error taxonomy (G09A-G09C)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class GenealogyError(WanxiangError):
    """Base error for genealogy failures."""

    code = "genealogy_error"


class GedcomParseError(GenealogyError):
    code = "gedcom_parse_error"


class InvalidKinship(GenealogyError):
    code = "invalid_kinship"


class PrivacyDenied(GenealogyError):
    code = "family_privacy_denied"
