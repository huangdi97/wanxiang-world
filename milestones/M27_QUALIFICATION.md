# M27 — Reality Root / Constitution / Semantic ISA Milestone Gate

## 前置条件

- G30A PASS — Reality Root 语义契约
- G30B PASS — World Constitution 模型与版本
- G30C PASS — Constitution 执行与不可越权
- G30D PASS — World Semantic ISA 最小类型
- G30E PASS — ISA 到现有用例与 Commit 管线映射
- G30F PASS — 三类 World Commit 收敛
- G30G PASS — Fact Scope 与 Authority Partition
- G30H PASS — Event Snapshot 版本上下文升级
- G30I PASS — M27 Root Constitution ISA 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M27=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M27_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
