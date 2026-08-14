# M31 — 平台收敛与向后兼容 Milestone Gate

## 前置条件

- G34A PASS — Kernel Runtime Forge Experiences 责任收敛
- G34B PASS — WorldPack Definition schema v5.2 迁移
- G34C PASS — 数据库与 Ledger 兼容迁移
- G34D PASS — 旧 Event Snapshot Branch 向后回放
- G34E PASS — API SDK Client 兼容
- G34F PASS — 性能与复杂度回归
- G34G PASS — M31 全平台兼容资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M31=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M31_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
