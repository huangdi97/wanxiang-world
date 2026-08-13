"""Structured compiler error taxonomy (G04C)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class CompilerError(WanxiangError):
    """Base error for the structured compiler."""

    code = "compiler_error"


class UnsupportedFormat(CompilerError):
    code = "unsupported_source_format"


class MalformedSource(CompilerError):
    code = "malformed_source"


class OversizedSource(CompilerError):
    code = "oversized_source"


class InvalidCandidate(CompilerError):
    code = "invalid_candidate"
