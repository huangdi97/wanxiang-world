# M39 — Studio & Experience Qualification
## 前置 Goal
- G42A PASS — Studio Source/Corpus/Candidate Review
- G42B PASS — Studio Character/Relation/Canon Workspace
- G42C PASS — Studio Spatial/Schedule/Institution Workspace
- G42D PASS — Experience 世界/Scenario/角色入口
- G42E PASS — Experience 2D Living World
- G42F PASS — Embodiment Leave/Return + Branch Compare
- G42G PASS — M39 Product Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M39_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
