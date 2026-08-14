# M26 — 旧代码真实盘点与最小核心收敛 Milestone Gate

## 前置条件

- G29A PASS — 冻结旧基线并验证 M25 真实状态
- G29B PASS — 全仓代码处置实际盘点
- G29C PASS — 合并重复 Registry 与 Manager
- G29D PASS — 统一 State Event Audit 派生关系
- G29E PASS — 收敛物理包边界
- G29F PASS — 清理 Fake Placeholder 与旧实验残留
- G29G PASS — 建立最小代码度量与预算
- G29H PASS — M26 收敛资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M26=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M26_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
