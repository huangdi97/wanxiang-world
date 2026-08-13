# ADR-0027: Structured Compiler MVP Design (G04C)

- Status: accepted
- Date: 2026-08-13

## Context

G04C needs a deterministic compiler over gated sources (TXT/MD/JSON/YAML) that
emits candidates with provenance and fails safely on malformed/oversized/
unsupported inputs, without fake PDF/OCR/video extraction.

## Decision

1. The compiler pipeline is read -> validate -> compile -> emit; candidates are
   deterministic (stable hash for same inputs + compiler version).
2. Readers are per-format with strict validation: JSON strict, YAML restricted
   safe subset (no anchors/tags/flow), markdown explicit `## id` sections,
   text as facts. PDF/OCR/video/audio/image are explicitly unsupported.
3. Candidates carry source refs, offsets and provenance; payloads are primitive
   FieldValues; non-primitive values are rejected.
4. Diagnostics are structured (level/code/message/source_id); malformed and
   oversized inputs fail safely with error diagnostics, never partial output.

## Consequences

- Deterministic, provenance-bound compilation; unsupported formats are explicit
  rather than faked; review exports carry compiler version and hashes.