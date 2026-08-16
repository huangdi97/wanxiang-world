# M43 — Post-M42 Verification & v5.3 Baseline

## Required Goals

- G46A PASS — M42 独立复核与 v5.3 基线冻结
- G46B PASS — 创建 v5.3 工作分支与 Git 安全基线
- G46C PASS — Kernel Freeze 自动 Guard
- G46D PASS — v5.3 Delta Traceability
- G46E PASS — M43 Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M43_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。
