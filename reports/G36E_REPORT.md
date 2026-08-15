# Goal G36E Acceptance Report — Perception Belief Memory 与消息传播

## Status
PASS (mechanism) — synthetic corpus; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/epistemic/propagation.py` (new):
   - `PerceptionEnvelope` — observation wrapper (channel/confidence/visibility).
   - `perceive()` — perception forms an observation memory (epistemic model).
   - `propagate_message()` — message chain with deterministic rumour
     distortion + confidence decay (misunderstanding).
   - `rumour_distortion()` — deterministic distortion marker.
   - `propagatable_claims()` — propagation candidates = G35E runtime view
     only (FutureCanon never propagates).
2. `tests/unit/substrate/test_rc001_perception_propagation.py` (4 tests):
   perception -> observation memory; deterministic propagation with decay;
   deterministic rumour distortion; future canon never propagates.

## Reuse
- G03B epistemic memory model; G35E CompiledCanon runtime view (imported);
  observation model. Only propagation is new.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_perception_propagation.py -q` | 4 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36e: Perception Belief Memory 与消息传播`
