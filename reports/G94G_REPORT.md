# G94G — Promotion Ladder Enforcement

Date: 2026-08-27
Milestone: M91
Status: **PASS**
Commit: `g94g: Promotion Ladder Enforcement`

## Delivered scope

G94G reuses the existing L0-L8 promotion ladder, `PlatformFeedbackLab`, and
`PromotionControlLedger`. No second policy stack, sandbox, release registry,
rollback history, or Commit Authority was introduced.

`LevelRequirement` and `PromotionEvidence` now carry policy-version binding,
world-count, normalized benchmark score, sandbox result, rollback readiness,
and high-level review evidence. The default M91 L0-L5 ladder requires
increasing evidence counts `[0, 1, 2, 3, 4, 5]` and world counts
`[1, 1, 1, 1, 2, 3]`. L4 requires benchmark and sandbox evidence; L5 adds
rollback readiness and explicit high-level review. A level skip, stale policy
version, missing sandbox/rollback evidence, or insufficient review is rejected.

## Evidence

- New unit coverage: `tests/unit/substrate/test_g94g_promotion_ladder_enforcement.py` — 2 passed.
- Product-chain control coverage: `tests/integration/test_g94g_promotion_ladder_product_chain.py` — 1 passed.
- Regression coverage: existing promotion ladder and platform feedback tests —
  7 passed; focused total `10 passed, 1 warning`.
- Full quality: `1384 passed, 1 skipped, 2 warnings`; Ruff, format, Pyright,
  pytest, and architecture conformance all pass. The PostgreSQL skip remains
  the documented `EXTERNAL_BLOCKED` live profile.
- The integration path used the real SQLite WorldRuntime and its canonical
  Commit/Replay path, then ran the existing sandbox, versioned release,
  rollback, and append-only promotion withdrawal controls.
- Canonical state hash, event history, and restore/replay hash stayed equal;
  rollback changes installability/control status only and never rewrites world
  events.
- Negative coverage rejects insufficient worlds, missing high-level review,
  stale policy version, and existing sandbox gate failures.

## Acceptance boundary

G94G is complete and locally verified. It enforces promotion controls but does
not qualify universal emergence or release v5.5. G94H-G97J and the remaining
M91-M94 acceptance gates remain pending.
