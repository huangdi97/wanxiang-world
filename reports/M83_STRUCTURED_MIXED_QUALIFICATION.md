# M83 / G86 Structured and Mixed-Source Qualification

Date: 2026-08-25
Scope: structured evidence and mixed-source authoring; no model training.

## Decision

`PASS` for the synthetic structured/mixed qualification and regression
infrastructure.

## Evidence

Artifact: `artifacts/m79_m84/structured_mixed_smoke.json`

The integration path combines one synthetic book source, one JSON source, and
one CSV source into one `WorldDraft`, with 9 candidates and 3 fusion
alignments. Candidate evidence retains all three source references and a
conflict is preserved for review rather than silently collapsed.

Structured locators round-trip through the evidence layer:

- JSON Pointer: `json://json_m83#record//people/0/name`
- CSV cell: `csv://csv_m83#column/row_2/column_3`

The same mixed input reaches the existing OneClick authoring path and produces
one WorldPackage plus a Preview reference. The integration test covers the
JSON/CSV locator values, evidence retention, fusion alignment, conflict
preservation, one-draft invariant, package creation, and preview creation.

This qualification uses only anonymized/synthetic data. It does not replace
the M79 second-real-book gate or the M82 real-GEDCOM gate.
