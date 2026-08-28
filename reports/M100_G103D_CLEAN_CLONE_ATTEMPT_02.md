# M100 G103D Isolated Clean Clone
Conclusion: FAIL; 0/18.
Candidate: `250623e937f35f0fbb1ec69cd7db6440043520f3`; clone: `--no-local`, detached exact-SHA, cleanup.
| Command | Status | Exit | Duration |
|---|---|---:|---:|
| git_clone_no_local | FAIL | 128 | 40.062 ms |
Coverage: install, migration, CLI, replay, Playable, Studio, API, SDK, Python, kernel,
PostgreSQL, TypeScript.
External: browser/PG/pnpm gaps are EXTERNAL_BLOCKED only with prerequisite evidence; other non-zero
results FAIL.
Boundaries: IMPLEMENTED runtime; VALIDATED PASS; EXPERIMENTAL/BOUNDED provider;
NOT_PROVEN live customer/production/hardware.
Evidence: artifacts/v55_stable/m100/clean_clone.json
Reproduce: uv run python scripts/m100_clean_clone.py
