# M41 — Cross-Domain Generality Qualification
## 前置 Goal
- G44A PASS — Generality Harness + Kernel Lock
- G44B PASS — Family World Qualification
- G44C PASS — Heritage World Qualification
- G44D PASS — Campaign World Qualification
- G44E PASS — 四领域同 Core 对照
- G44F PASS — 第三方黑盒 World Pack
- G44G PASS — M41 Generality Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M41_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
