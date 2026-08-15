# M38 — Full Living Runtime Qualification
## 前置 Goal
- G41A PASS — 多 Scenario 实例化
- G41B PASS — Population Resolution
- G41C PASS — Autonomous World Loop
- G41D PASS — 大规模认知/消息传播
- G41E PASS — 长期 Persona/Capability/Relation 演化
- G41F PASS — 社会/制度演化
- G41G PASS — 30 日 + 1 年加速长稳
- G41H PASS — M38 Living World Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M38_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
