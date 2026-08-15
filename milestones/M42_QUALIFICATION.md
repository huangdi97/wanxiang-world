# M42 — Production Release Qualification
## 前置 Goal
- G45A PASS — Public SDK / Package API Freeze
- G45B PASS — CLI / Scaffolder / Certification
- G45C PASS — Package Install/Upgrade/Migration
- G45D PASS — Full Red Chamber Release Bundle
- G45E PASS — 生产部署/备份/恢复/观测
- G45F PASS — Security/Rights/Supply Chain Final
- G45G PASS — Release 长稳/容量/文档
- G45H PASS — v5.2 Production Final Certification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M42_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
