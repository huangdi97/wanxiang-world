# Codex M35–M42 连续执行总指令
你继续当前万相世界仓库。先验证 M34 真实状态，不接受聊天里的“完成”作为证据。

## 必读
`docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
`README_FIRST.md`
`00_PROGRAM_ARCHITECTURE.md`
`01_KERNEL_FREEZE_POLICY.md`
`03_FULL_RED_CHAMBER_ACCEPTANCE.md`
`04_CROSS_DOMAIN_AND_RELEASE_STANDARD.md`
`05_GOALS_INDEX.md`
`06_MILESTONE_GATES.md`
`07_RESUME_PROTOCOL.md`
`08_FINAL_EVIDENCE_STANDARD.md`
全部 `goals/`、`milestones/`，以及当前 AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG、reports、Git、源码、tests、migrations。

## 连续执行
严格按 G38A→G45H 执行。每 Goal：盘点复用→实现→单测→合同/集成→负向→Replay/迁移→前端 E2E（适用）→报告→本地 commit→自动继续。
Milestone PASS 后自动继续，不询问用户。

## 不可破坏
- M35 后 Kernel v1 默认冻结。
- Source ≠ Fact；模型记忆不能成为《红楼梦》Canon。
- Completion/Generated 不能冒充 E0。
- Population Resolution 优先，禁止所有 NPC 持续调用大模型。
- World/Domain/LLM/UI/Simulator 只能 Proposal，不能直接改权威状态。
- Canonical Replay / Soft Canon / Living-Open 共用一套 Runtime。
- 禁止重复 Manager/Registry/Engine/State/Event/Branch 系统。
- 内部 bug、测试、类型、迁移、性能问题必须自己修复，不是停止理由。
- 只有真实外部授权/数据/硬件/凭证可 EXTERNAL_BLOCKED。
- 不自动 push/deploy，不开始 v5.3。

只有 M42 最终标准全部满足时停止。
