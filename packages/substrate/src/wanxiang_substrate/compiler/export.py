"""Package-candidate export suitable for review (G04C)."""

from __future__ import annotations

from wanxiang_substrate.compiler.model import CompileResult


def export_package_candidate(result: CompileResult) -> dict[str, object]:
    """JSON-serializable review export with compiler version and provenance."""
    return {
        "job_id": result.job_id,
        "compiler_version": result.compiler_version,
        "candidates": [candidate.canonical() for candidate in result.candidates],
        "diagnostics": [diagnostic.as_dict() for diagnostic in result.diagnostics],
        "hash": result.result_hash(),
    }
