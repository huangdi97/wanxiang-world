# M100 G103D Isolated Clean Clone
Conclusion: PASS; 18/18.
Candidate: `62740de39eaae46c118a99a2019837315775a44a`; clone: `--no-local`, detached exact-SHA, cleanup.
| Command | Status | Exit | Duration |
|---|---|---:|---:|
| git_clone_no_local | PASS | 0 | 7001.412 ms |
| git_checkout_exact_sha | PASS | 0 | 1637.061 ms |
| uv_sync_all_groups_packages | PASS | 0 | 12534.821 ms |
| migration_upgrade_head | PASS | 0 | 7338.303 ms |
| clean_room | PASS | 0 | 6844.912 ms |
| quickstart_cli | PASS | 0 | 1076.642 ms |
| lineage_replay | PASS | 0 | 5423.287 ms |
| playable_e2e | PASS | 0 | 773.06 ms |
| studio_socket_smoke | PASS | 0 | 5754.126 ms |
| api_surface | PASS | 0 | 5817.859 ms |
| openapi_export | PASS | 0 | 1787.863 ms |
| sdk_baseline | PASS | 0 | 2603.051 ms |
| kernel_guard | PASS | 0 | 514.277 ms |
| python_quality | PASS | 0 | 415024.451 ms |
| postgres_profile | EXTERNAL_BLOCKED | 0 | 1977.316 ms |
| pnpm_install | EXTERNAL_BLOCKED | 127 | 4.857 ms |
| ts_lint | EXTERNAL_BLOCKED | 127 | 4.53 ms |
| ts_typecheck | EXTERNAL_BLOCKED | 127 | 4.285 ms |
| ts_test | EXTERNAL_BLOCKED | 127 | 4.206 ms |
| ts_build | EXTERNAL_BLOCKED | 127 | 4.486 ms |
Coverage: install, migration, CLI, replay, Playable, Studio, API, SDK, Python, kernel,
PostgreSQL, TypeScript.
External: browser/PG/pnpm gaps are EXTERNAL_BLOCKED only with prerequisite evidence; other non-zero
results FAIL.
Boundaries: IMPLEMENTED runtime; VALIDATED PASS; EXPERIMENTAL/BOUNDED provider;
NOT_PROVEN live customer/production/hardware.
Evidence: artifacts/v55_stable/m100/clean_clone.json
Reproduce: uv run python scripts/m100_clean_clone.py
