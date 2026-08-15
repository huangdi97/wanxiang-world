# M39 Qualification — Studio & Experience

## Status
**M39 Milestone Gate PASS (mechanism)**

Real《红楼梦》full text remains EXTERNAL_BLOCKED (G35A); the Studio/Experience
MECHANISM surface is certified on synthetic content, honestly labeled.

## Goal status (M39)
| Goal | Status |
|---|---|
| G42A Studio Source/Corpus/Candidate Review | PASS |
| G42B Studio Character/Relation/Canon Workspace | PASS |
| G42C Studio Spatial/Schedule/Institution Workspace | PASS |
| G42D Experience 世界/Scenario/角色入口 | PASS |
| G42E Experience 2D Living World | PASS |
| G42F Embodiment Leave/Return + Branch Compare | PASS |
| G42G M39 Product Qualification | PASS (this report) |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | 968 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED); architecture PASS |
| SDK baseline | routes=17 ts=5 py=1152; contract PASS |
| ruff / format / pyright | PASS (0 errors) |

## Key invariants verified (M39)
- Studio surfaces read-only; candidate approve/reject propose-only.
- Future-canon permission gated; norm/duty editor propose-only.
- Experience catalog + 2D living view + embodiment leave/return summary.
- Fresh-user flow + basic accessibility labels present.

## Honest boundary
- Real product content requires a legal, traceable edition (BLOCKERS.md).

## Local checkpoint
- G42 mechanism committed; M39 gate certified; tag `m39-product`.
