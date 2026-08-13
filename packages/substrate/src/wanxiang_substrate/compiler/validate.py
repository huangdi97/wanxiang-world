"""Candidate schema/invariant validation before output (G04C)."""

from __future__ import annotations

from wanxiang_substrate.compiler.model import CandidateObject, CompileDiagnostic


def validate_candidates(candidates: tuple[CandidateObject, ...]) -> tuple[CompileDiagnostic, ...]:
    """Every candidate must carry provenance and satisfy its kind schema."""
    diagnostics: list[CompileDiagnostic] = []
    for candidate in candidates:
        if not candidate.object_id:
            diagnostics.append(
                CompileDiagnostic("error", "missing_object_id", "candidate has no object_id")
            )
        if not candidate.source_refs:
            diagnostics.append(
                CompileDiagnostic(
                    "error", "missing_provenance", f"{candidate.object_id} has no source refs"
                )
            )
        if candidate.kind == "entity":
            if "entity_id" not in candidate.payload:
                diagnostics.append(
                    CompileDiagnostic(
                        "error", "missing_entity_id", f"{candidate.object_id} lacks entity_id"
                    )
                )
            if "entity_type" not in candidate.payload:
                diagnostics.append(
                    CompileDiagnostic(
                        "error", "missing_entity_type", f"{candidate.object_id} lacks entity_type"
                    )
                )
        for key, value in candidate.payload.items():
            if not _is_primitive(value):
                diagnostics.append(
                    CompileDiagnostic(
                        "error",
                        "non_primitive_payload",
                        f"{candidate.object_id} payload {key!r} is not primitive",
                    )
                )
    return tuple(diagnostics)


def _is_primitive(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))
