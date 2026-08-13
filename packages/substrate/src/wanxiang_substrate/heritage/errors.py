"""Heritage / museum error taxonomy (G10A-G10D)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class HeritageError(WanxiangError):
    """Base error for heritage failures."""

    code = "heritage_error"


class IiifParseError(HeritageError):
    code = "iiif_parse_error"


class MappingError(HeritageError):
    code = "linked_art_mapping_error"


class TwinError(HeritageError):
    code = "semantic_twin_error"
