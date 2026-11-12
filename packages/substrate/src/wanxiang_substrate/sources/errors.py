"""Structured source registry / source gate error taxonomy (G04B)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SourceError(WanxiangError):
    """Base error for source registry failures."""

    code = "source_error"
    product_state = "SOURCE_REJECTED"


class SourceNotApproved(SourceError):
    code = "source_not_approved"
    product_state = "RIGHTS_ACTION_REQUIRED"


class RightsDenied(SourceError):
    code = "source_rights_denied"
    product_state = "RIGHTS_ACTION_REQUIRED"


class MaliciousSource(SourceError):
    code = "malicious_source"


class InvalidTransition(SourceError):
    code = "invalid_source_transition"
    product_state = "INVALID_SOURCE_TRANSITION"


class DuplicateSource(SourceError):
    code = "duplicate_source"
    product_state = "SOURCE_DUPLICATE"


class SourceNotFound(SourceError):
    code = "source_not_found"


class UnsupportedSource(SourceError):
    """No adapter can handle this source kind/format."""

    code = "unsupported_source"
    product_state = "SOURCE_UNSUPPORTED"


class OcrRequired(SourceError):
    """Scanned content needs an OCR provider; none is available (honest)."""

    code = "ocr_required"
    product_state = "OCR_REQUIRED"


class CapabilityUnavailable(SourceError):
    """An optional provider capability is not registered."""

    code = "capability_unavailable"
    product_state = "CAPABILITY_UNAVAILABLE"


class SemanticProviderRequired(CapabilityUnavailable):
    """Semantic extraction cannot continue without an explicitly configured provider."""

    code = "semantic_provider_required"
    product_state = "SEMANTIC_PROVIDER_REQUIRED"


class SemanticProviderSchemaError(CapabilityUnavailable):
    """A semantic provider returned data outside the structured candidate contract."""

    code = "semantic_provider_schema_error"
    product_state = "SEMANTIC_PROVIDER_SCHEMA_ERROR"


class ZeroCoverage(SourceError):
    """The real pipeline produced no compileable semantic coverage."""

    code = "zero_coverage"
    product_state = "ZERO_COVERAGE"


class MalformedSourceContent(SourceError):
    """Source bytes could not be parsed as the declared format."""

    code = "malformed_source_content"
    product_state = "SOURCE_MALFORMED"


class ContentHashMismatch(SourceError):
    """Resolved source bytes do not match the immutable source record."""

    code = "content_hash_mismatch"
    product_state = "SOURCE_INTEGRITY_FAILED"


class IngestError(SourceError):
    """Adapter ingest failed (typed, never silent fallback)."""

    code = "ingest_error"
