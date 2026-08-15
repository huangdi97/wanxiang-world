# G43G — M40 Long-Horizon Qualification
> Milestone：**M40**

## 目标
证明世界能长期演化并生出世界。

## 必读
- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- 00_PROGRAM_ARCHITECTURE.md
- 01_KERNEL_FREEZE_POLICY.md
- 02_CODEX_MASTER_PROMPT.md
- 03_FULL_RED_CHAMBER_ACCEPTANCE.md
- 04_CROSS_DOMAIN_AND_RELEASE_STANDARD.md
- 05_GOALS_INDEX.md
- 06_MILESTONE_GATES.md
- 07_RESUME_PROTOCOL.md
- 08_FINAL_EVIDENCE_STANDARD.md
- 现有 AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- M34/v5.2 最终 reports、Git、tests、migrations

## Implementation Tasks
1. year run + promotion + lineage compare。

## 架构硬约束
- M35 后 Kernel v1 默认冻结。
- 唯一 Commit/Ledger/Branch-Worldline/Package/Capability 机制继续复用。
- 具体领域不得进入 Kernel。
- Provider/LLM/UI/Simulator 只能 Proposal。
- Source ≠ Fact；Completion/Generated 不冒充 E0/Canon。
- 无 LLM key 必须可跑 deterministic core/long-run。
- Population Resolution 优先。
- 不得新增重复 Manager/Registry/Engine/State/Event/Branch。
- persisted schema 变化必须 migration+compatibility。
- 不 skip/delete 关键测试，不 hardcode PASS。
- 不自动 push/deploy。

## Tests / Acceptance
- original Definition unchanged
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43g: M40 Long-Horizon Qualification`，然后自动继续。
