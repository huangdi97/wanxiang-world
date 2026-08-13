# Structured Compiler MVP (G04C)

Ownership: `wanxiang_substrate.compiler` (safe read -> validate -> compile ->
emit for supported inputs).

## Pipeline

`StructuredCompiler.compile(job_id, sources)` processes sources in sorted order:
read -> compile -> validate -> emit. Every candidate carries source refs and a
provenance string; output is a `CompileResult` with candidates, diagnostics and
a deterministic `result_hash` (same inputs + compiler version -> same hash).

## Safe readers

- `json`: strict `json.loads`; non-object roots are malformed.
- `yaml`: restricted safe subset (`yaml_mini`) supporting plain nested mappings
  and scalars only; anchors/aliases/tags/flow/multi-doc fail loudly.
- `markdown`: limited explicit-markup pathway (`## <id>` sections with
  `key: value` lines) -> entity candidates.
- `text`: plain content -> a single `fact` candidate (provenance only).
- `pdf`/`ocr`/`video`/`audio`/`image`: explicitly unsupported (no fake
  extraction); oversized payloads fail safely at the reader.

## Candidate contract

`CandidateObject` has object_id, kind (entity/relation/evidence/fact), a
primitive `FieldValue` payload, source refs, offsets and provenance. Non-
primitive payload values are rejected. Validation requires provenance and, for
entity candidates, `entity_id` + `entity_type`.

## Export

`export_package_candidate` renders a review-ready JSON structure with compiler
version, candidates, diagnostics and the result hash.