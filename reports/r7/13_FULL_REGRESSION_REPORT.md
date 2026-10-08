# R7 13 — Full Regression Report

Implementation code anchor: `8ebbc4f04a265ab4d9c380fc8da7bbabfe86ce8f`.

Status: `PASS`.

GitHub Actions CI run `37722944558` completed successfully with all six
declared jobs green.

## Python / architecture

The main Python job reports:

- `1802 passed, 1 skipped`;
- the one skip is the ordinary SQLite/no-PostgreSQL path and is not a failed R7
  assertion;
- the dedicated PostgreSQL 16 job separately runs the live profile: `4 passed`;
- `ruff check .` PASS;
- `ruff format --check .` PASS (`2921 files already formatted`);
- Pyright: `0 errors, 0 warnings, 0 informations`;
- `scripts/architecture_check.py` PASS;
- `scripts/kernel_guard.py`: 0 violations.

The post-closure tests include Profile/Bundle/Lock/Artifact composition,
World Bootstrap/WorldHandle, expanded Gateway scope/rights, execution
checkpoint/resume, real Docker reference isolation, marketplace/paper-capability
binding, layered invariants, three-ledger provenance and ExperienceRuntime.

## TypeScript / Cordis / SDK

The exact-SHA qualification reports:

- SDK TypeScript: 6 files / 22 tests PASS;
- Cordis host: 10 files / 77 tests PASS;
- lint/typecheck/build PASS;
- cross-language Python history/authority and harness seams remain exercised.

## Packaging / safety

The same CI run passes service-contract projection, SDK/OpenAPI drift, package
authoring/certification, release-build clean-room smoke, repository secret scan
and forbidden-file checks.

No Stable/v5.6 release status is inferred from these engineering gates.
