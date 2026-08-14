# Goal G13G Acceptance Report — Maintainability, Complexity, Test Quality & Upgradeability Audit

## Status
PASS (one exception-swallowing defect found and fixed)

## Findings
- 239 production files / 19,369 lines; **0 files over the 300-line threshold**; 0 import cycles.
- 5 high-complexity hotspots (max cyclomatic complexity >= 15): `genealogy/gedcom.py` (25),
  `spatial/resolver.py` (21), `heritage/iiif.py` (19), `material/query.py` (19), `institution/query.py` (16).
  Classified as **P2 tracked closure candidates** (data-heavy parsers/query builders; within size limits; fully tested) —
  owner: substrate domain modules; rationale documented in MAINTAINABILITY_AUDIT.md.
- 9 public `Any`-typed parameters — all at external boundaries (`*_from_primitive` JSON decoding,
  SQLAlchemy connection helper); classified as justified, not escape hatches in domain logic.
- **Fixed**: `population/scheduler.py` silently swallowed `WanxiangError` on rejected scheduler actions
  (`except WanxiangError: pass`). Now rejections are counted and surfaced via `SchedulerRunResult.rejected_events`
  (additive contract field, deterministic). The final `population.record_run` marker remains best-effort by design,
  documented inline.
- Test quality: 428-test suite + property tests; no modules with <2 assertions.

## Delivered
- `scripts/maintainability_audit.py` + `reports/MAINTAINABILITY_AUDIT.md`, `reports/TEST_QUALITY_AUDIT.md`,
  `reports/UPGRADEABILITY_AUDIT.md`, `reports/maintainability_audit.json`, `reports/G13G_REPORT.md`.
- `tests/integration/test_g13g_maintainability.py` — 6 tests (no exception swallowing, no over-threshold files,
  no import cycles, no cross-package private imports, quality gate documented, scheduler rejection
  observability/determinism).
- Core fix: `packages/substrate/src/wanxiang_substrate/population/scheduler.py` + `model.py`.

## Evidence
| Check | Result |
|---|---|
| `uv run python scripts/maintainability_audit.py` | files=239 over300=0 hot=5 cycles=0 any=9 swallow=0 |
| `uv run python scripts/quality.py` | PASS — ruff/pyright, 428 pytest, architecture PASS |

## Remaining limitations
- Complexity hotspots are tracked P2 candidates, not blocking; refactors must preserve behavior (covered by tests).
- No forced dependency upgrades (locked uv/pnpm; freshness changes require documented reason).

## Final checkpoint
- commit: `g13g: maintainability, complexity, test quality & upgradeability audit`
