"""Compiler job/stage/candidate contracts (G04C)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.entity import FieldValue

CompilerStage = Literal["read", "validate", "compile", "emit", "done"]
DiagnosticLevel = Literal["info", "warning", "error"]

SUPPORTED_KINDS = ("text", "markdown", "json", "yaml")
EXPLICITLY_UNSUPPORTED = ("pdf", "ocr", "video", "audio", "image")


@dataclass(frozen=True, slots=True)
class CompileDiagnostic:
    level: DiagnosticLevel
    code: str
    message: str
    source_id: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "source_id": self.source_id,
        }


@dataclass(frozen=True, slots=True)
class SourceOffset:
    source_id: str
    line: int
    column: int


@dataclass(frozen=True, slots=True)
class CandidateObject:
    """A compiled candidate with source/evidence provenance."""

    object_id: str
    kind: Literal["entity", "relation", "evidence", "fact"]
    payload: dict[str, FieldValue]
    source_refs: tuple[str, ...]
    offsets: tuple[SourceOffset, ...] = ()
    provenance: str = ""

    def canonical(self) -> dict[str, object]:
        return {
            "object_id": self.object_id,
            "kind": self.kind,
            "payload": dict(self.payload),
            "source_refs": sorted(self.source_refs),
            "offsets": [
                {"source_id": o.source_id, "line": o.line, "column": o.column} for o in self.offsets
            ],
            "provenance": self.provenance,
        }

    def compute_hash(self) -> str:
        payload = json.dumps(self.canonical(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class CompileResult:
    job_id: str
    compiler_version: int
    candidates: tuple[CandidateObject, ...]
    diagnostics: tuple[CompileDiagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(d.level == "error" for d in self.diagnostics)

    def result_hash(self) -> str:
        payload = {
            "job_id": self.job_id,
            "compiler_version": self.compiler_version,
            "candidates": [c.canonical() for c in self.candidates],
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
