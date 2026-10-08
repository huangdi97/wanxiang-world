# M100 G103D Isolated Clean Clone
Conclusion: PASS; 18/18.
Candidate: `a9be096ba0cda3b9c05d039e61e27cd529ca6b45`; clone: `--no-local`, detached exact-SHA, cleanup.
| Command | Status | Exit | Duration |
|---|---|---:|---:|
| git_clone_no_local | PASS | 0 | 2881.607 ms |
| git_checkout_exact_sha | PASS | 0 | 6189.527 ms |
| uv_sync_all_groups_packages | PASS | 0 | 14911.71 ms |
| migration_upgrade_head | PASS | 0 | 6372.135 ms |
| clean_room | PASS | 0 | 5738.089 ms |
| quickstart_cli | PASS | 0 | 918.672 ms |
| lineage_replay | PASS | 0 | 4773.461 ms |
| playable_e2e | PASS | 0 | 642.144 ms |
| studio_socket_smoke | PASS | 0 | 4871.496 ms |
| api_surface | PASS | 0 | 5001.2 ms |
| openapi_export | PASS | 0 | 1612.603 ms |
| sdk_baseline | PASS | 0 | 2218.536 ms |
| kernel_guard | PASS | 0 | 473.145 ms |
| python_quality | PASS | 0 | 413176.521 ms |
| postgres_profile | EXTERNAL_BLOCKED | 0 | 1874.13 ms |
| pnpm_install | PASS | 0 | 30376.905 ms |
| ts_lint | PASS | 0 | 18518.516 ms |
| ts_typecheck | PASS | 0 | 3450.266 ms |
| ts_test | PASS | 0 | 2856.363 ms |
| ts_build | PASS | 0 | 1622.61 ms |
Coverage: install, migration, CLI, replay, Playable, Studio, API, SDK, Python, kernel,
PostgreSQL, TypeScript.
External: browser/PG/pnpm gaps are EXTERNAL_BLOCKED only with prerequisite evidence; other non-zero
results FAIL.
Boundaries: IMPLEMENTED runtime; VALIDATED PASS; EXPERIMENTAL/BOUNDED provider;
NOT_PROVEN live customer/production/hardware.
Evidence: artifacts/v55_stable/m100/clean_clone.json
Reproduce: uv run python scripts/m100_clean_clone.py
