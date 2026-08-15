# M36 — Full Corpus & Canon Graph Qualification
## 前置 Goal
- G39A PASS — 完整底本 Source Gate
- G39B PASS — 章节/段落稳定定位器
- G39C PASS — Scene Boundary 与场景候选
- G39D PASS — 全人物 Identity/Alias/Role Graph
- G39E PASS — 地点/物品/组织 Source Graph
- G39F PASS — Event/Timeline/Relation Graph
- G39G PASS — Canon Graph / Edition Conflict
- G39H PASS — M36 Full Corpus Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M36_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
