# Goal G37B Acceptance Report — Canon 用户 无干预三世界线比较

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/worldlines.py` (new):
   - `run_worldlines()` — three worldlines (canonical_replay/soft_canon/
     living_open) from a shared parent with deterministic divergence.
   - `compare_worldlines()` — compare state hashes / items / beliefs /
     relations; divergence + parent hash verification.
   - `verify_parent_hash()` — children never mutate the parent.
2. `tests/unit/substrate/test_rc001_worldlines.py` (4 tests): three runs;
   comparison divergence + parent verified; parent hash unchanged; canonical
   replay matches parent baseline.

## Reuse
- G36G strategies; G37A reference run.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_worldlines.py -q` | 4 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g37b: Canon 用户 无干预三世界线比较`
