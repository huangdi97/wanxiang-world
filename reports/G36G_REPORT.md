# Goal G36G Acceptance Report — Canonical Replay Soft Canon Living Open 三策略

## Status
PASS (mechanism) — synthetic facts only; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/strategies.py` (new):
   - `WorldStrategy` + `StrategyConfig` + `strategy_for()` — three policy
     configs (canonical_replay / soft_canon / living_open).
   - `CanonLocks` — immutable canon-lock set; locked facts reject mutation
     (CanonLocked).
   - `SoftAttractor` — deterministic soft-canon pull toward a target under a
     condition.
   - `compare_to_baseline()` — open-branch baseline comparison (matches,
     revision_delta).
2. `tests/unit/substrate/test_rc001_strategies.py` (5 tests): three strategy
   configs; canonical lock rejects mutation; soft attractor pull; open branch
   divergence; replay strategy pins baseline.

## Reuse
- G04D CanonLocked error; no new registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_strategies.py -q` | 5 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36g: Canonical Replay Soft Canon Living Open 三策略`
