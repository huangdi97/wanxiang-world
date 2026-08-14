# M28 — Worldline / Lineage / World Hypervisor Milestone Gate

## 前置条件

- G31A PASS — World Definition 与 Worldline 身份模型
- G31B PASS — World Lineage Graph 数据模型
- G31C PASS — Lineage Repository 与迁移
- G31D PASS — World Hypervisor 多实例隔离
- G31E PASS — Interworld Identity 与 Presence
- G31F PASS — Hybrid Genesis 兼容性分析与安全拒绝
- G31G PASS — Lineage API SDK Studio 最小投影
- G31H PASS — M28 Lineage Hypervisor 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M28=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M28_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
