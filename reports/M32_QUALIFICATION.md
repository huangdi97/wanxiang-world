# M32 Qualification — 红楼梦 Source Gate 与蒸馏机制

## Status
**M32 Milestone Gate PASS (mechanism / platform-level)**

Real《红楼梦》full-text remains EXTERNAL_BLOCKED (G35A): a legal, traceable
edition is not available in this environment. Per 10_V5_2 final evidence
standard, this gate certifies the SOURCE GATE + DISTILLATION MECHANISM layer;
it does NOT certify real-corpus canon completion (that remains gated on a
legal edition and is tracked in BLOCKERS.md).

## Goal status (M32)
| Goal | Status |
|---|---|
| G35A 来源策略与合法版本登记 | PASS (mechanism; real text EXTERNAL_BLOCKED) |
| G35B 章节分段与可引用 Source Locator | PASS |
| G35C 人物与别名 Identity Distillation | PASS |
| G35D 空间组织物品 Distillation | PASS |
| G35E Past Character Future Canon 编译 | PASS |
| G35F Narrative Household HistoricalChina Domain 复用与补齐 | PASS |
| G35G Character Relation Knowledge Boundary Distillation | PASS |
| G35H Completion Ledger 与审核 | PASS |
| G35I 编译 RedChamber World Definition 与 Scenario | PASS |
| reports/RED_CHAMBER_WORLD_PACK_ACCEPTANCE.md | created |

## Full quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | 878 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED) |
| ruff / format / pyright | PASS (0 errors) |
| architecture_check.py | Architecture conformance: PASS |
| SDK baseline | routes=17 ts=5 py=1028 |

## Key invariants verified
- No second Commit/Event/Branch/Worldline/Registry/Engine created; all M32
  modules are pure distillers / frozen records / read-only queries / thin
  resolvers over the single authority.
- No model memory used as《红楼梦》Canon (G35A test + BLOCKERS).
- FutureCanon is control-plane-only (G35E); character knowledge boundary
  prevents private-fact leaks (G35G); completion records default can_enter_canon
  FALSE with E4/E5 terminal semantics (G35H).
- Core packages contain no Red Chamber hardcode (G35I test).

## Honest boundary / carry-forward
- Real corpus compilation, real world pack content, and the 7-day RedChamber
  acceptance remain EXTERNAL_BLOCKED until a legal, traceable edition is
  available. M32 is certified as the source-gate/distillation MECHANISM layer.

## Local checkpoint
- Goals committed g35a..g35i; M32 gate certified in this report.
