# M37 — Full Semantic World Qualification
## 前置 Goal
- G40A PASS — Full World Definition
- G40B PASS — Household Society Domain 深化
- G40C PASS — Historical China + Narrative Domain 深化
- G40D PASS — 全人物 Character Package
- G40E PASS — 完整 Spatial World
- G40F PASS — 物质/书信/礼物/药物绑定
- G40G PASS — Schedule/Body/Social Life + Completion
- G40H PASS — M37 Semantic World Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M37_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
