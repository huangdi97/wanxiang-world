# M37 Qualification — Full Semantic World

## Status
**M37 Milestone Gate PASS (mechanism)**

Real《红楼梦》full text remains EXTERNAL_BLOCKED (G35A); the full semantic-world
MECHANISM is certified on synthetic content, honestly labeled.

## Goal status (M37)
| Goal | Status |
|---|---|
| G40A Full World Definition | PASS |
| G40B Household Society Domain 深化 | PASS |
| G40C Historical China Narrative Domain 深化 | PASS |
| G40D 全人物 Character Package | PASS |
| G40E 完整 Spatial World | PASS |
| G40F 物质 书信 礼物 药物绑定 | PASS |
| G40G Schedule Body Social Life Completion | PASS |
| G40H M37 Semantic World Qualification | PASS (this report) |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | 956 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED); architecture PASS |
| SDK baseline | routes=17 ts=5 py=1126; contract PASS |
| ruff / format / pyright | PASS (0 errors) |
| Core proper-noun scan | empty (Kernel purity) |

## Key invariants verified (M37)
- Full world definition composed with constitution/genesis/evolution refs.
- persona (interpretive) vs state (current) separated per character.
- secret/scene/arc are propose-only; reputation/norm/duty/permission generic.
- Multi-scenario dry-run without committing; Core free of domain names.

## Honest boundary
- Real-corpus semantic world requires a legal, traceable edition (BLOCKERS.md).

## Local checkpoint
- G40 mechanism committed; M37 gate certified; tag `m37-semantic-world`.
