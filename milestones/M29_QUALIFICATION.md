# M29 — Evolution Policy Stack / 多尺度共演化 Milestone Gate

## 前置条件

- G32A PASS — Evolution Policy Stack
- G32B PASS — 多尺度演化调度
- G32C PASS — Actor Capability 与 Persona 演化分离
- G32D PASS — Relation Group Social Pattern Distillation
- G32E PASS — Institution Organization Rule 晋升
- G32F PASS — Ontology Law 多尺度演化
- G32G PASS — Evolution Telemetry 与隐私权利
- G32H PASS — M29 多尺度共演化资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M29=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M29_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
