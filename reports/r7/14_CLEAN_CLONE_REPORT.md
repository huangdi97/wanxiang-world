# R7 14 — Exact-SHA Clean Clone Report

Qualification anchor: `f7b719df2ccdd906bf2c0f9c3474b1cbe219bbbf`.

Status: `PASS`.

GitHub Actions run `37582984421`, job
`R7 exact-SHA clean clone qualification`, cloned the exact pushed SHA into a
fresh directory and completed all required R7 steps with **0 failed / 0 skipped**.

Artifact: `r7-exact-sha-f7b719df2ccdd906bf2c0f9c3474b1cbe219bbbf`
(artifact id `11465099366`).

## Qualification steps

The uploaded machine-readable qualification records 19/19 PASS:

1. Python sync;
2. architecture check;
3. write-surface inventory;
4. Ruff check;
5. Ruff format check;
6. Pyright;
7. Playwright/Chromium install;
8. full pytest with live PostgreSQL dependency available;
9. R7 focused unit qualification;
10. RuntimeLock qualification;
11. Reality migration qualification;
12. security denial qualification;
13. four reference worlds;
14. pnpm frozen install;
15. TS typecheck;
16. TS lint;
17. TS tests;
18. TS build;
19. browser E2E.

Focused counts in the artifact include `281 passed` for the R7 unit selection,
`31 passed` for RuntimeLock, `19 passed` for migration, `8 passed` for
security denials, `4 passed` for reference worlds and `2 passed` for browser
E2E.

The workflow also verifies that qualification regenerates only declared evidence
outputs and leaves no source drift.
