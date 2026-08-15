# Goal G37D Acceptance Report — 红楼梦 Replay Crash Recovery Chaos

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/chaos.py` (new):
   - `snapshot_restart()` — snapshot -> primitive -> restart, same hash.
   - `detect_stream_corruption()` — corrupted stream changes hash.
   - `duplicate_command_rejected()` — duplicate/stale commit rejected.
   - `reconnect_embodiment()` — lease release + reacquire (client reconnect).
   - `provider_failure_isolated()` — failing provider leaves world unchanged.
   - `run_chaos_checks()` — aggregated `ChaosReport`.
2. `tests/unit/substrate/test_rc001_chaos.py` (6 tests): each check + aggregate.

## Reuse
- runtime snapshot/state round-trip; CommitAuthority; G36F embodiment.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_chaos.py -q` | 6 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g37d: 红楼梦 Replay Crash Recovery Chaos`
