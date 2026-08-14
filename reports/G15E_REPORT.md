# Goal G15E Acceptance Report — Material Custody, Information Propagation & Social Continuity Qualification

## Status
PASS

## Objective
Prove objects, messages and information persist and propagate through explicit world mechanisms rather than narrative text shortcuts.

## Delivered
- `tests/integration/test_g15e_material_info.py` — 3 tests.
- `reports/MATERIAL_INFORMATION_SOCIAL_CONTINUITY.md`, `reports/G15E_REPORT.md`.

## Findings
- Objects never exist in two exclusive containers simultaneously (move semantics enforced).
- Sealed payloads are not knowledge: non-custodian reads rejected; custody transfer + read is the causal path;
  readers recorded; double-read rejected.
- Branch outcomes diverge causally (child delivery vs parent) and both replay to stable distinct hashes.

## Evidence
- 3 tests passed; ruff/pyright clean.

## Remaining limitations
- Real messages/communications channels remain EXTERNAL_BLOCKED; explicit material/info mechanisms qualified.

## Final checkpoint
- commit: `g15e: material custody, information propagation & social continuity qualification`
