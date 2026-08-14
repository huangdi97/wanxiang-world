# M30 — Promotion / Cross-world Distillation Milestone Gate

## 前置条件

- G33A PASS — 统一 Abstraction Ladder
- G33B PASS — Worldline 到 Derived World Promotion Pipeline
- G33C PASS — Promotion 可重放与可撤销控制
- G33D PASS — Cross-world Distillation
- G33E PASS — 平台反哺 Sandbox Benchmark Approval
- G33F PASS — Lineage 与 Promotion API Studio
- G33G PASS — M30 Promotion Cross-world 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M30=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M30_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
