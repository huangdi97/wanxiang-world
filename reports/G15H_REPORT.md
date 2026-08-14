# Goal G15H Acceptance Report — Red Chamber Source-gated Qualified Reference Slice

## Status
PASS (generic capability); real-data slice EXTERNAL_BLOCKED (never fabricated PASS)

## Objective
Build or requalify the mother-spec Red Chamber minimal seven-day reference slice using only approved source material and explicit canon/completion/model provenance.

## Delivered
- `tests/integration/test_g15h_red_chamber.py` — 3 tests (unapproved material cannot compile as canonical;
  canon/completion/model labels distinguishable; canonical-claim provenance retained).
- `reports/RED_CHAMBER_REFERENCE_QUALIFICATION.md`, `reports/G15H_REPORT.md`.

## Findings
- Source-gate semantics exercised end-to-end with synthetic provenance; no canon fabricated from memory.
- Ledger truth labels (canon / source_backed / model_inference) remain distinct in projection/audit.
- Real Red Chamber corpus absent -> EXTERNAL_BLOCKED with exact missing source/rights needs documented.

## Evidence
- 3 tests passed; ruff/pyright clean.

## Remaining limitations
- Seven-day reference acceptance on approved sources requires the EXTERNAL_BLOCKED corpus; synthetic worldness
  acceptance (G15B-G15G) is unaffected.

## Final checkpoint
- commit: `g15h: red chamber source-gated qualified reference slice`
