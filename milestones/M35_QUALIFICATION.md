# M35 — Post-M34 Audit & Kernel Freeze Qualification
## 前置 Goal
- G38A PASS — 独立复核 M34
- G38B PASS — Kernel v1 ABI 清单
- G38C PASS — Kernel Change Guard
- G38D PASS — Full Red Chamber Gap Audit
- G38E PASS — 代码最小性清理
- G38F PASS — 大 Corpus 流水线容量基线
- G38G PASS — API/DB/Package/性能基线冻结
- G38H PASS — M35 资格验收

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M35_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
