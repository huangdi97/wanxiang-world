# G49G — Hybrid Genesis Reference World

> Milestone：M46

## 目标

两个 compatible synthetic parents → child。

## 必读

- `README_FIRST.md`
- `00_PROGRAM_ARCHITECTURE.md`
- `01_KERNEL_FREEZE_AND_MINIMAL_CODE_POLICY.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- `03_INTERWORLD_SEMANTICS.md`
- `04_HYBRID_GENESIS_STANDARD.md`
- `05_WORLD_INTELLIGENCE_BOUNDARY.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `07_GOALS_INDEX.md`
- `08_MILESTONE_GATES.md`
- `09_RESUME_PROTOCOL.md`
- 仓库 M42/v5.2 reports + AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG + Git + tests + migrations

## 实施任务

1. compile/approve/instantiate/run/replay。

## 架构硬约束

- Kernel v1 默认冻结。
- 所有世界变更仍走唯一 Commit Boundary。
- Branch/Worldline/Lineage 复用已有历史模型。
- Interworld/Hybrid 不改写 parent history。
- World Intelligence 只能 Prediction/Plan/Candidate/ProposedDelta。
- 具体世界/provider 名称不得进入 Kernel。
- 核心测试不依赖外部 LLM/API。
- 不新增重复 Manager/Registry/Engine/State/Event/Branch。
- 不得提交 secrets/private data/restricted corpus/model cache。
- 不得 skip/delete tests 或 hardcode PASS。

## 测试

- parent hashes unchanged。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49G_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49g: Hybrid Genesis Reference World`，然后自动继续。
