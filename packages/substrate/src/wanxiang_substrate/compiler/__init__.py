"""Structured compiler MVP substrate (G04C)."""

from wanxiang_substrate.compiler.compiler import COMPILER_VERSION, StructuredCompiler
from wanxiang_substrate.compiler.errors import (
    CompilerError,
    InvalidCandidate,
    MalformedSource,
    OversizedSource,
    UnsupportedFormat,
)
from wanxiang_substrate.compiler.export import export_package_candidate
from wanxiang_substrate.compiler.fixture import (
    json_source,
    malformed_json_source,
    markdown_source,
    oversized_source,
    pdf_source,
    text_source,
    yaml_source,
)
from wanxiang_substrate.compiler.model import (
    CandidateObject,
    CompileDiagnostic,
    CompileResult,
    SourceOffset,
)
from wanxiang_substrate.compiler.readers import read_source
from wanxiang_substrate.compiler.validate import validate_candidates

__all__ = [
    "COMPILER_VERSION",
    "CandidateObject",
    "CompileDiagnostic",
    "CompileResult",
    "CompilerError",
    "InvalidCandidate",
    "MalformedSource",
    "OversizedSource",
    "SourceOffset",
    "StructuredCompiler",
    "UnsupportedFormat",
    "export_package_candidate",
    "json_source",
    "malformed_json_source",
    "markdown_source",
    "oversized_source",
    "pdf_source",
    "read_source",
    "text_source",
    "validate_candidates",
    "yaml_source",
]
