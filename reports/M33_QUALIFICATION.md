# M33 Qualification — 红楼梦实例化与生活运行

## Status
**M33 Milestone Gate PASS (mechanism / platform-level)**

Real《红楼梦》full-text remains EXTERNAL_BLOCKED (G35A); this gate certifies
the RC-001 INSTANTIATION + LIVING-WORLD MECHANISM layer (synthetic anonymized
content). It does NOT certify real-corpus canon (tracked in BLOCKERS.md).

## Goal status (M33)
| Goal | Status |
|---|---|
| G36A 实例化 RC-001 与固定世界快照 | PASS |
| G36B 空间可见可听私密运行 | PASS |
| G36C 人物职责 NPC 日程身体与社会制度 | PASS |
| G36D 信件诗稿礼物药物的物质与信息连续性 | PASS |
| G36E Perception Belief Memory 与消息传播 | PASS |
| G36F 林黛玉 Embodiment ShadowPolicy Handoff | PASS |
| G36G Canonical Replay Soft Canon Living Open 三策略 | PASS |
| G36H 红楼梦 Experience Studio 最小可用面 | PASS |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` (pytest) | 911 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED) |
| SDK baseline drift (additive M33 symbols) | regenerated; `test_g17a_sdk_contract` 3/3 PASS (routes=17 ts=5 py=1070) |
| ruff / format / pyright | PASS (0 errors) |
| architecture_check.py | Architecture conformance: PASS |

## Key invariants verified (M33)
- RC-001 instantiation through the single Commit Authority (1 genesis event);
  fixed reproducible snapshot; lineage root recorded.
- Spatial run: visibility/acoustic/privacy/access + movement time.
- NPC deterministic schedule composing duty/visit/body; population resolution.
- Material continuity: read forms observation memory; hide/gift/medicine.
- Perception/propagation with rumour/misunderstanding; future canon never
  propagates.
- Embodiment with intent/co-drive/full-control modes + handoff events; Shadow
  never makes major decisions.
- Three strategies (canonical replay / soft canon / living open) with canonical
  locks, soft attractor, baseline comparison.
- Experience Studio read-only surface (map/characters/actions/events/source/
  completion/branch).

## Honest boundary / carry-forward
- Real RedChamber 7-day acceptance remains EXTERNAL_BLOCKED until a legal,
  traceable edition is available. M33 is certified as the living-world
  mechanism layer.

## Local checkpoint
- Goals committed g36a..g36h; M33 gate certified in this report.
