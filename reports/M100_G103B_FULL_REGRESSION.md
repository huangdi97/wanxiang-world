# M100 G103B Full Regression

Conclusion: PASS. 18/
18 commands were executed from candidate SHA
`a74e0f162d0dfe4911d38b77bae8f874f47bfe23`. The artifact is written after every command, so
an interrupted run remains explicitly incomplete rather than appearing green.
Python quality includes the full pytest suite, Ruff, Pyright, and architecture
check. The SDK snapshot was reviewed for additive M97/M98 symbols; its targeted
contract test passed before this matrix.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
| clean_room | PASS | 0 | 2368.692 ms |
| python_quality | EXTERNAL_BLOCKED | 1 | 400454.091 ms |
| kernel_guard | PASS | 0 | 404.292 ms |
| release_build | PASS | 0 | 175.387 ms |
| playable_e2e | PASS | 0 | 534.802 ms |
| studio_socket_smoke | PASS | 0 | 1918.229 ms |
| structured_mixed_smoke | PASS | 0 | 475.758 ms |
| sdk_baseline | PASS | 0 | 756.456 ms |
| openapi_export | PASS | 0 | 1755.09 ms |
| security_reliability | PASS | 0 | 71690.781 ms |
| security_forensics | PASS | 0 | 742.181 ms |
| blackbox_acceptance | PASS | 0 | 2681.625 ms |
| postgres_profile | EXTERNAL_BLOCKED | 0 | 1944.263 ms |
| pnpm_install | EXTERNAL_BLOCKED | 127 | 6.718 ms |
| ts_lint | EXTERNAL_BLOCKED | 127 | 5.195 ms |
| ts_typecheck | EXTERNAL_BLOCKED | 127 | 5.595 ms |
| ts_test | EXTERNAL_BLOCKED | 127 | 5.21 ms |
| ts_build | EXTERNAL_BLOCKED | 127 | 5.146 ms |

PostgreSQL is reported as EXTERNAL_BLOCKED when the real service is skipped or
unreachable. The browser Studio chain is reported as EXTERNAL_BLOCKED only when
the sole failure is Playwright's real Windows `WinError 5` process-pipe denial.
Other command failures remain FAIL in the machine-readable artifact.

Machine-readable evidence: artifacts/v55_stable/m100/full_regression.json
Reproduce with: uv run python scripts/m100_regression.py
