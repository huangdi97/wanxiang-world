"""Deterministic structured-data compiler MVP (G04C)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.entity import FieldValue

from wanxiang_substrate.compiler.errors import (
    MalformedSource,
    OversizedSource,
    UnsupportedFormat,
)
from wanxiang_substrate.compiler.model import (
    CandidateObject,
    CompileDiagnostic,
    CompileResult,
)
from wanxiang_substrate.compiler.readers import read_source
from wanxiang_substrate.compiler.validate import validate_candidates
from wanxiang_substrate.sources.model import SourceRecord

COMPILER_VERSION = 1


class StructuredCompiler:
    """Read -> validate -> compile -> emit pipeline over gated sources."""

    def compile(
        self,
        job_id: str,
        sources: Mapping[str, SourceRecord],
        compiler_version: int = COMPILER_VERSION,
    ) -> CompileResult:
        candidates: list[CandidateObject] = []
        diagnostics: list[CompileDiagnostic] = []
        for source_id in sorted(sources):
            record = sources[source_id]
            try:
                parsed = read_source(record)
            except UnsupportedFormat as exc:
                diagnostics.append(
                    CompileDiagnostic("error", "unsupported_format", str(exc), source_id)
                )
                continue
            except (MalformedSource, OversizedSource) as exc:
                diagnostics.append(CompileDiagnostic("error", "read_failed", str(exc), source_id))
                continue
            try:
                candidates.extend(self._compile_source(record, parsed))
            except (MalformedSource, OversizedSource) as exc:
                diagnostics.append(
                    CompileDiagnostic("error", "compile_failed", str(exc), source_id)
                )
        candidates.sort(key=lambda c: c.object_id)
        diagnostics.extend(validate_candidates(tuple(candidates)))
        return CompileResult(
            job_id=job_id,
            compiler_version=compiler_version,
            candidates=tuple(candidates),
            diagnostics=tuple(diagnostics),
        )

    def _compile_source(
        self, record: SourceRecord, parsed: Mapping[str, object]
    ) -> list[CandidateObject]:
        objects = parsed.get("objects")
        if isinstance(objects, Mapping):
            if record.kind == "markdown":
                return self._compile_markdown(record, cast(Mapping[str, object], objects))
            return self._compile_objects(record, cast(Mapping[str, object], objects))
        if "text" in parsed:
            text = str(parsed["text"])
            return [
                CandidateObject(
                    object_id=f"fact_{record.source_id}",
                    kind="fact",
                    payload={"text": text},
                    source_refs=(record.source_id,),
                    provenance=f"text:{record.source_id}",
                )
            ]
        raise MalformedSource(f"source {record.source_id!r} has no compilable structure")

    def _compile_objects(
        self, record: SourceRecord, objects: Mapping[str, object]
    ) -> list[CandidateObject]:
        result: list[CandidateObject] = []
        for object_id in sorted(objects):
            entry = objects[object_id]
            if not isinstance(entry, Mapping):
                raise MalformedSource(f"object {object_id!r} must be a mapping")
            entry_map = cast(Mapping[str, object], entry)
            kind_value = str(entry_map.get("kind") or "entity")
            payload_raw = entry_map.get("payload")
            if not isinstance(payload_raw, Mapping):
                raise MalformedSource(f"object {object_id!r} must declare a payload mapping")
            payload: dict[str, FieldValue] = {}
            for key, value in cast(Mapping[str, object], payload_raw).items():
                if value is None or isinstance(value, (str, int, float, bool)):
                    payload[str(key)] = value
                else:
                    raise MalformedSource(f"object {object_id!r} payload {key!r} is not primitive")
            result.append(
                CandidateObject(
                    object_id=object_id,
                    kind=kind_value,  # type: ignore[arg-type]
                    payload=payload,
                    source_refs=(record.source_id,),
                    provenance=f"{record.kind}:{record.source_id}:{object_id}",
                )
            )
        return result

    def _compile_markdown(
        self, record: SourceRecord, sections: Mapping[str, object]
    ) -> list[CandidateObject]:
        """Explicit-markup pathway: each '## id' section becomes an entity."""
        result: list[CandidateObject] = []
        for section_id in sorted(sections):
            section = sections[section_id]
            if not isinstance(section, Mapping):
                raise MalformedSource(f"section {section_id!r} must be a mapping")
            section_map = cast(Mapping[str, object], section)
            payload: dict[str, FieldValue] = {}
            for key, value in section_map.items():
                if value is None or isinstance(value, (str, int, float, bool)):
                    payload[str(key)] = value
                else:
                    raise MalformedSource(
                        f"section {section_id!r} payload {key!r} is not primitive"
                    )
            result.append(
                CandidateObject(
                    object_id=section_id,
                    kind="entity",
                    payload=payload,
                    source_refs=(record.source_id,),
                    provenance=f"markdown:{record.source_id}:{section_id}",
                )
            )
        return result
