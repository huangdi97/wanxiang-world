# Goal G32C Acceptance Report ? Actor Capability ? Persona ????

## Status
PASS

## Objective
Ensure learned skills never silently rewrite a persona: separate capability
evolution from persona evolution with different policy/cadence and trajectory
provenance.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/actor_evolution.py`:
   - `PersonaDelta` ? explicit, reasoned persona change (never implied by skill
     gain).
   - `TrajectoryEntry` ? provenance record (seq/kind/detail/provenance_ref).
   - `ActorEvolutionState` ? separated capability + persona with trajectory;
     `capability_hash()` / `persona_hash()` (deterministic).
   - `ActorEvolutionTracker` ? `apply_capability` (reuses CapabilityDelta; only
     changes capability hash) / `apply_persona` (only changes persona hash);
     every change appends a provenance entry.
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +5 non-breaking).
2. `tests/unit/substrate/test_actor_evolution.py` (4 tests):
   - skill gain does not change persona hash;
   - explicit persona delta changes persona;
   - long-term persona change has an event chain (provenance refs);
   - trajectory mixes capability + persona entries with provenance.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_actor_evolution.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=914 (+5 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Reuse CapabilityDelta / new PersonaDelta | PASS |
| Different evolution policy/cadence for capability vs persona | PASS (separate channels, explicit persona only) |
| Trajectory provenance recorded | PASS (tested) |
| Skill gain does not change persona hash | PASS (tested) |
| Long-term persona change has event chain | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/actor_evolution.py,
  tests/unit/substrate/test_actor_evolution.py, reports/G32C_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32c: Actor Capability ? Persona ????`
