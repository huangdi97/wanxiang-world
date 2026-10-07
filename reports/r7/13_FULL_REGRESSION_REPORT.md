# R7 13 — Full Regression Report

Qualification anchor: `f7b719df2ccdd906bf2c0f9c3474b1cbe219bbbf`.

Status: `PASS`.

GitHub Actions run `37582984372` completed successfully with all declared
jobs green.

## Python / architecture

The main Python job reports:

- `1749 passed, 1 skipped`;
- the one skip is the local-no-PostgreSQL test path, not a failed R7 assertion;
- `ruff check .` PASS;
- `ruff format --check .` PASS;
- `pyright` 0 errors / 0 warnings;
- `scripts/architecture_check.py` PASS;
- `scripts/kernel_guard.py` 0 violations.

The dedicated PostgreSQL job brought up PostgreSQL 16 and ran the live profile:
`4 passed`.

## TypeScript / Cordis / SDK

The TS job reports:

- pnpm lint PASS;
- TypeScript typecheck PASS;
- SDK TS: 6 files / 22 tests PASS;
- Cordis host: 9 files / 74 tests PASS;
- build PASS;
- real cross-language Python seams are exercised in the Cordis test suite.

## Packaging / safety

The same run passed API/package/SDK generation drift, release build,
clean-room certification smoke, repository secret scan and forbidden-file
checks.

No v5.5 Stable tag or v5.6 release is inferred from these engineering gates.
