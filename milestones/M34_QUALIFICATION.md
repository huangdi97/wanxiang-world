# M34 — 七日活世界 + Lineage/Promotion + v5.2 最终认证 Milestone Gate

## 前置条件

- G37A PASS — 红楼梦七日场景自动化执行
- G37B PASS — Canon 用户 无干预三世界线比较
- G37C PASS — 红楼梦长时演化与 Promotion Candidate
- G37D PASS — 红楼梦 Replay Crash Recovery Chaos
- G37E PASS — v5.2 全仓最小代码与架构终审
- G37F PASS — 全量回归与最终追溯矩阵
- G37G PASS — v5.2 与 RedChamber 最终认证并停止

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M34=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M34_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
