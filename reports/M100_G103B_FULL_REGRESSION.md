# M100 G103B Full Regression

Conclusion: PASS. 18/
18 commands were executed from candidate SHA
`a9be096ba0cda3b9c05d039e61e27cd529ca6b45`. The artifact is written after every command, so
an interrupted run remains explicitly incomplete rather than appearing green.
Python quality includes the full pytest suite, Ruff, Pyright, and architecture
check. The SDK snapshot was reviewed for additive M97/M98 symbols; its targeted
contract test passed before this matrix.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
| clean_room | PASS | 0 | 2470.582 ms |
| python_quality | PASS | 0 | 412353.248 ms |
| kernel_guard | PASS | 0 | 414.594 ms |
| release_build | PASS | 0 | 170.707 ms |
| playable_e2e | PASS | 0 | 523.376 ms |
| studio_socket_smoke | PASS | 0 | 2032.998 ms |
| structured_mixed_smoke | PASS | 0 | 486.456 ms |
| sdk_baseline | PASS | 0 | 709.625 ms |
| openapi_export | PASS | 0 | 1776.312 ms |
| security_reliability | PASS | 0 | 69817.423 ms |
| security_forensics | PASS | 0 | 772.195 ms |
| blackbox_acceptance | PASS | 0 | 2550.938 ms |
| postgres_profile | EXTERNAL_BLOCKED | 0 | 1727.259 ms |
| pnpm_install | PASS | 0 | 928.742 ms |
| ts_lint | PASS | 0 | 2728.458 ms |
| ts_typecheck | PASS | 0 | 1660.348 ms |
| ts_test | PASS | 0 | 2078.884 ms |
| ts_build | PASS | 0 | 1607.177 ms |

PostgreSQL is reported as EXTERNAL_BLOCKED when the real service is skipped or
unreachable. The browser Studio chain is reported as EXTERNAL_BLOCKED only when
the sole failure is Playwright's real Windows `WinError 5` process-pipe denial.
Other command failures remain FAIL in the machine-readable artifact.

Machine-readable evidence: artifacts/v55_stable/m100/full_regression.json
Reproduce with: uv run python scripts/m100_regression.py
