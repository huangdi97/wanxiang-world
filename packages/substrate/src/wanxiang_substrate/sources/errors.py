"""Structured source registry / source gate error taxonomy (G04B)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SourceError(WanxiangError):
    """Base error for source registry failures."""

    code = "source_error"


class SourceNotApproved(SourceError):
    code = "source_not_approved"


class RightsDenied(SourceError):
    code = "source_rights_denied"


class MaliciousSource(SourceError):
    code = "malicious_source"


class InvalidTransition(SourceError):
    code = "invalid_source_transition"


class DuplicateSource(SourceError):
    code = "duplicate_source"


class SourceNotFound(SourceError):
    code = "source_not_found"


class UnsupportedSource(SourceError):
    """No adapter can handle this source kind/format."""

    code = "unsupported_source"


class OcrRequired(SourceError):
    """Scanned content needs an OCR provider; none is available (honest)."""

    code = "ocr_required"


class CapabilityUnavailable(SourceError):
    """An optional provider capability is not registered."""

    code = "capability_unavailable"


class MalformedSourceContent(SourceError):
    """Source bytes could not be parsed as the declared format."""

    code = "malformed_source_content"


class ContentHashMismatch(SourceError):
    """Resolved source bytes do not match the immutable source record."""

    code = "content_hash_mismatch"


class IngestError(SourceError):
    """Adapter ingest failed (typed, never silent fallback)."""

    code = "ingest_error"
