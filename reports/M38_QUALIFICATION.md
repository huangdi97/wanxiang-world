# M38 Qualification — Full Living Runtime

## Status
**M38 Milestone Gate PASS (mechanism)**

Real《红楼梦》full text remains EXTERNAL_BLOCKED (G35A); the full living-runtime
MECHANISM is certified on synthetic content, honestly labeled.

## Goal status (M38)
| Goal | Status |
|---|---|
| G41A 多 Scenario 实例化 | PASS |
| G41B Population Resolution | PASS |
| G41C Autonomous World Loop | PASS |
| G41D 大规模认知/消息传播 | PASS |
| G41E 长期 Persona/Capability/Relation 演化 | PASS |
| G41F 社会/制度演化 (LawCommit gate) | PASS |
| G41G 30日+1年加速长稳 | PASS |
| G41H M38 Living World Qualification | PASS (this report) |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | 963 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED); architecture PASS |
| SDK baseline | routes=17 ts=5 py=1140; contract PASS |
| ruff / format / pyright | PASS (0 errors) |

## Key invariants verified (M38)
- Population promotion/demotion under activation budget; identity preserved.
- Autonomous loop deterministic with affected-entity activation + fallback.
- Propagation corrections/forgetting never delete history.
- CapabilityDelta vs PersonaDelta separated; LawCommit gate respected.
- 30-day + 1-year accelerated long-run stable; 12-class worldness matrix.

## Honest boundary
- Real-corpus long-run acceptance requires a legal, traceable edition.

## Local checkpoint
- G41 mechanism committed; M38 gate certified; tag `m38-living-world`.
