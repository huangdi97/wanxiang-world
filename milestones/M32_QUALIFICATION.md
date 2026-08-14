# M32 — 《红楼梦》Source Gate 与 World Definition 编译 Milestone Gate

## 前置条件

- G35A PASS — 红楼梦来源策略与合法版本登记
- G35B PASS — 章节分段与可引用 Source Locator
- G35C PASS — 人物与别名 Identity Distillation
- G35D PASS — 空间组织物品 Distillation
- G35E PASS — Past Character Future Canon 编译
- G35F PASS — Narrative Household HistoricalChina Domain 复用与补齐
- G35G PASS — Character Relation Knowledge Boundary Distillation
- G35H PASS — Completion Ledger 与审核
- G35I PASS — 编译 RedChamber World Definition 与 Scenario

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M32=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M32_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
