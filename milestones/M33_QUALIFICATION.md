# M33 — 《红楼梦》Living World Runtime 与 Experience Milestone Gate

## 前置条件

- G36A PASS — 实例化 RC-001 与固定世界快照
- G36B PASS — 红楼梦空间可见可听私密运行
- G36C PASS — 人物职责 NPC 日程身体与社会制度
- G36D PASS — 信件诗稿礼物药物的物质与信息连续性
- G36E PASS — Perception Belief Memory 与消息传播
- G36F PASS — 林黛玉 Embodiment ShadowPolicy Handoff
- G36G PASS — Canonical Replay Soft Canon Living Open 三策略
- G36H PASS — 红楼梦 Experience Studio 最小可用面

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M33=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M33_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
