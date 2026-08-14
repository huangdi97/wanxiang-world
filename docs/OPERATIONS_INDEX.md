# Operations Index (G16J)

## Runbooks
| Operation | Reference |
|---|---|
| Deploy a fresh private/staging environment | `scripts/ops_deploy.py` + docs/RELEASE_PROCESS.md |
| Initialize (migrate + seed reference world) | deploy flow; docs/RELEASE_PROCESS.md |
| Configure + secrets | docs/PRODUCTION_TOPOLOGY.md |
| Monitor (traces/metrics/logs) | docs/OBSERVABILITY_RUNBOOK.md |
| Backup / restore | docs/DISASTER_RECOVERY_RUNBOOK.md |
| Upgrade + rollback | docs/RELEASE_PROCESS.md + backup runbook |
| Diagnose failures | observability runbook + preflight (scripts/release_build.py) |

## Operator prerequisites (checked by deploy; fails clearly)
- `WANXIANG_DATABASE_URL` set (production default rejected).
- `uv` and `node` on PATH.
- Required production secrets (e.g., `WANXIANG_SECRET_KEY`).

## Security baseline (enabled by default in production)
- Production config validation (fail-fast), rate limiting, payload size guard, secret redaction,
  source-gate/rights enforcement.
