# Goal G17D Acceptance Report — Third-party Package Conformance & Certification Harness

## Status
PASS

## Objective
Provide an automated suite that certifies package structure, schemas, dependencies, rights/source metadata, deterministic install/instantiate behavior and forbidden privileged access.

## Delivered
- `scripts/wxpack.py certify` subcommand — static validation + forbidden-import scan + runtime dry-run install, emitting a machine-readable report with versions.
- `tests/integration/test_g17d_certification.py` — 2 tests.
- `reports/PACKAGE_CERTIFICATION_HARNESS.md`, `reports/G17D_REPORT.md`.

## Findings
- A reference package passes certification; known-bad fixtures fail for expected reasons.
- Certification output includes runtime/SDK/package versions; the harness is a release gate for bundled examples.

## Evidence
- 2 tests passed (plus G17B authoring regression 5 passed); ruff/pyright clean.

## Remaining limitations
- Certification covers platform conformance, not legal/factual endorsement; untrusted arbitrary code is not executed.

## Final checkpoint
- commit: `g17d: third-party package conformance & certification harness`
