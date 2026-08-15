# Goal G35E Acceptance Report — Past Character Future Canon 编译

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A);
canon compilation verified on an explicitly-labeled synthetic corpus (NOT canon).

## Objective
At a concrete Scenario time point, compile source-backed canon claims into
PastCanon (before the scenario), CharacterCanon (character-bound claims up to
and including the scenario) and FutureCanon (after the scenario). FutureCanon
must be visible ONLY on the control plane, never to the running world.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/canon.py`:
   - `ScenarioPoint` — concrete scenario time point (chapter/segment locator).
   - `CanonClaim` — source-backed claim with temporal bucket (past/present/
     future), evidence locators, optional character_key.
   - `CompiledCanon` — past/character/future buckets; `runtime_view` = Past +
     Character (Future NEVER visible to the world); `control_plane_view` =
     Past + Character + Future; `character_canon(key)` per-character canon.
   - `scenario_at()` — choose a concrete scenario at the first segment of a
     chapter.
   - `CanonCompiler` — deterministic, pure compilation (caller-supplied claim
     rules; edition-agnostic); classifies segments before/at/after the
     scenario point. No write path.
   - Exported via `wanxiang_substrate.sources` (SDK baseline +7 non-breaking).
2. `tests/unit/substrate/test_canon_compilation.py` (6 tests, synthetic):
   past/character/future classification at a chosen scenario; FutureCanon
   excluded from runtime_view and present in control_plane_view; per-character
   canon filters by key and never leaks future; scenario selection; claims
   carry resolvable evidence; deterministic compile.

## Reuse (no duplicate abstraction)
- G35B `SourceLocator` / `segment_source` / `source_slice`.
- No new registry/engine/store; canon is compiled candidates only; SourceGate
  (G04B) still guards source eligibility before compile.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_canon_compilation.py tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_identity_distillation.py -q` | 21 passed |
| `uv run pytest tests/integration/test_g17a_sdk_contract.py -q` | 3 passed (baseline) |
| `uv run ruff check` / `ruff format --check` (changed files) | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=986 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Scenario time point selection | PASS (tested) |
| PastCanon claims | PASS (tested) |
| CharacterCanon (per-character) | PASS (tested) |
| FutureCanon control-plane-only (never runtime) | PASS (tested) |
| Evidence locators on every claim | PASS (tested) |
| Determinism | PASS (tested) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- Real canon compilation requires a legal, traceable edition; claim rules are
  caller-supplied so the mechanism is edition-agnostic.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/sources/canon.py,
  tests/unit/substrate/test_canon_compilation.py, reports/G35E_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/sources/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md,
  DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35e: Past Character Future Canon 编译`
