# Continuous Execution & Resume Protocol — v5.1 M18→M25

Codex may continue automatically through all Goals and milestones.

If context is compressed/restarted, recover in this order:

1. `git status` / current branch / last local commit;
2. `STATUS.md` and `PLAN.md`;
3. latest `reports/Gxx_REPORT.md`;
4. latest milestone report;
5. `reports/V5_1_TRACEABILITY_MATRIX.md`;
6. `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
7. `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
8. current Goal file;
9. rerun the narrow acceptance test for the last claimed PASS before continuing.

Never reconstruct state from chat memory.

A Goal is resumable only from committed/reported evidence. Uncommitted partial work must be inspected before reuse.
