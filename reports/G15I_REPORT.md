# Goal G15I Acceptance Report — Family, Heritage & Campaign Source-gated Reference Suites

## Status
PASS (synthetic conformance); real slices EXTERNAL_BLOCKED

## Objective
Prove domain generality across genealogy/family, museum/heritage and campaign/co-simulation using approved real data where available and synthetic black-box fixtures otherwise.

## Delivered
- `tests/integration/test_g15i_multidomain.py` — 4 tests (genealogy, heritage, campaign, public-interfaces-only).
- `reports/MULTI_DOMAIN_REFERENCE_QUALIFICATION.md`, `reports/G15I_REPORT.md`.

## Findings
- Synthetic conformance passes for all four domain families (literature, family, heritage, campaign).
- No domain requires Core special-casing (architecture forensics clean; shared Core handles replay/branch).
- Real slices precisely EXTERNAL_BLOCKED; no real facts invented.

## Evidence
- 4 tests passed; ruff/pyright clean.

## Remaining limitations
- Real family/museum/campaign data absent (EXTERNAL_BLOCKED); generic capability and synthetic fixtures complete.

## Final checkpoint
- commit: `g15i: family, heritage & campaign source-gated reference suites`
