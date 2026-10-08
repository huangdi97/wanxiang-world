# R7 14 — Exact-SHA Clean Clone Report

Implementation code anchor: `8ebbc4f04a265ab4d9c380fc8da7bbabfe86ce8f`.

Status: `PASS`.

GitHub Actions run `37722944544`, job
`R7 exact-SHA clean clone qualification`, cloned that exact pushed SHA into a
fresh directory and completed all required R7 steps with **0 failed / 0
skipped**.

Artifact:
`r7-exact-sha-8ebbc4f04a265ab4d9c380fc8da7bbabfe86ce8f`
(artifact id `11526915848`, artifact digest
`sha256:b03cc31ba64b113f524613e135947cf2e1e3932c36ace66f429cfc6447b45295`).

## Qualification steps

The machine-readable artifact records 19/19 PASS:

1. Python sync;
2. architecture check;
3. write-surface inventory;
4. Ruff check;
5. Ruff format check;
6. Pyright;
7. Playwright/Chromium install;
8. full pytest with PostgreSQL dependency available;
9. focused R7 unit qualification;
10. RuntimeLock qualification;
11. Reality migration qualification;
12. security-denial qualification;
13. four reference worlds;
14. pnpm frozen install;
15. TS typecheck;
16. TS lint;
17. TS tests;
18. TS build;
19. browser E2E.

Focused counts: `315 passed` R7 unit selection, `31 passed` RuntimeLock,
`19 passed` migration, `8 passed` security denials, `4 passed` reference
worlds, `2 passed` browser E2E, SDK `22/22`, Cordis host `77/77`.

The workflow also restores only declared deterministic evidence regeneration
and then verifies there is no undeclared source drift.

## Documentation-sync rule

The branch will contain a later documentation synchronization commit. This
report does not pretend the code-anchor run proves a later SHA. Final closure is
valid only after CI and the exact-SHA workflow are independently green on the
final documentation HEAD.
