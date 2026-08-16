# WANXIANG v5.3 M43–M50 ALL-IN-ONE 中文长执行包


---

<!-- FILE: README_FIRST.md -->

# Wanxiang v5.3 M43–M50 中文长执行包

本包接续已经完成的 M0–M42。目标是：冻结 v5.2 Kernel v1，在不重写 Reality Root / Commit / Ledger / Branch / Package System 的前提下，完成 Multiverse Runtime、Interworld、Hybrid Genesis、Cross-world Distillation、Multiverse Studio/Experience、World Intelligence Provider Boundary，并在最终认证后安全推送到 GitHub。

执行方式：把本目录合并到当前仓库，新开 Codex 对话，把 `CODEX_COPY_PASTE_LONG_CN.txt` 全文发送给 Codex。Codex 从 G46A 连续执行到 G53J，中间不询问是否继续。


---

<!-- FILE: 00_PROGRAM_ARCHITECTURE.md -->

# M43–M50 总程序架构

- **M43**：Post-M42 独立复核、v5.3 baseline、Kernel Freeze、Git 工作分支。
- **M44**：Multiverse Runtime / World Family / Lineage Operations / 多世界隔离。
- **M45**：Interworld Identity / Presence / Portal / Memory-Skill-Item Sync Policy。
- **M46**：Hybrid Genesis / Compatibility Analyzer / Mapping / Safe Reject / Child Definition。
- **M47**：Cross-world Distillation / Domain & Runtime Promotion / Sandbox & Benchmark。
- **M48**：Multiverse Studio / Experience / Portal UX / Lineage & Hybrid Review。
- **M49**：World Intelligence Provider Boundary：Predictor / Planner / World Model / Generative Scene 只产出 Candidate/Proposal。
- **M50**：全量 Release Qualification、Security/Rights、30-day multi-world stability、SDK/docs、GitHub push/tag/release candidate。

## 总原则

Kernel v1 冻结；世界可以无限增加，Core 不随世界增加。新能力默认通过 Policy / Provider / Forge / Experience 实现。


---

<!-- FILE: 01_KERNEL_FREEZE_AND_MINIMAL_CODE_POLICY.md -->

# Kernel Freeze 与最少代码政策

## 默认冻结
Reality Root、Identity/Fact/Event/Constraint、State/Ontology/Law Commit、唯一 Commit Boundary、World Ledger、Snapshot/Replay、Branch/Worldline isolation、World Definition/Instance/Lineage Identity、Evidence/Provenance 核心 envelope、Stable World ABI 核心 envelope。

## 禁止
- 第二套 Commit/Event/Branch/Lineage/Package/Capability 系统；
- `InterworldEngine` / `MultiverseManager` / `HybridGenesisManager` 之类巨型 God Object；
- 具体世界或 portal/provider 专名进入 Kernel；
- 为新功能修改历史事件语义而不提供兼容迁移；
- 为“以后可能有用”增加未使用 Port/Registry。

## Kernel Change Proposal 唯一准入
必须同时证明：跨至少两个领域无法上层表达、存在最小失败测试、无 Domain/Policy/Provider 方案、兼容性明确、M42 金样 replay 不破坏，并生成 `reports/KERNEL_CHANGE_PROPOSAL_<id>.md`。


---

<!-- FILE: 02_GITHUB_DELIVERY_POLICY.md -->

# GitHub Delivery Policy

用户已明确授权本轮完成后上传 GitHub。

## 上传前
1. `git status` / `git remote -v` / `git branch --show-current` / `git log --oneline -20`。
2. 若 `gh` 可用：`gh auth status`。
3. 执行 secret scan、tracked-files review、large-file/private-source scan。
4. 确认不提交 `.env`、token、数据库、用户隐私、受限 corpus、模型缓存、构建缓存、大型生成资产。

## 分支
若当前在 `main/master`，优先创建：`feature/wanxiang-v5.3-multiverse`。

## Push
M50 全部内部认证 PASS 后：
`git push -u origin feature/wanxiang-v5.3-multiverse`

如果权限允许，可创建 PR：`Wanxiang v5.3 Multiverse & Interworld Runtime`。

最终认证 PASS 后可选创建 annotated tag：`v5.3.0-rc1` 并 push。只有现有仓库流程允许且 `gh` 可用时才可选创建 GitHub Release。

## 禁止
不 force push、不删远端分支、不改写用户历史、不伪造 push 成功。

若 remote/auth/permission 缺失，记录 `GITHUB_PUSH=EXTERNAL_BLOCKED` 和本地最终 SHA；工程完成状态与 GitHub 外部阻塞分开判定。


---

<!-- FILE: 03_INTERWORLD_SEMANTICS.md -->

# Interworld Semantic Contract

跨世界 Actor 至少保留：`origin_identity / origin_world_definition / origin_worldline_ref / presence_world / presence_identity / translation_policy / sync_policy`。

默认规则：
- A 进入 B 后，B 中经历只写 B 的 Worldline；
- B 不可反向修改 A 历史；
- 记忆/物品/Skill 回写必须显式 Policy + Rights + Validation；
- Constitution/Ontology/Law 不兼容时允许拒绝、翻译或 projection-only；
- Presence 不是复制 Origin Identity；
- Portal 是 use case，不拥有 authority。


---

<!-- FILE: 04_HYBRID_GENESIS_STANDARD.md -->

# Hybrid Genesis 标准

Pipeline：Parent Worlds → Constitution Compatibility → Identity Resolution → Ontology Mapping → Law Conflict Analysis → History Inheritance Policy → Rights/Provenance Resolution → Package Compatibility → Hybrid Genesis Candidate → Validate → Approve → New Child World Definition。

首版必须支持：兼容 synthetic parent 正向合成 + 不兼容世界安全拒绝。

绝不允许：拼接两个 event log 冒充新历史、修改 parent definition、自动解决不可调和根规律、绕过 Rights/Source Gate。


---

<!-- FILE: 05_WORLD_INTELLIGENCE_BOUNDARY.md -->

# World Intelligence Provider Boundary

允许 Provider：WorldStatePredictor、WorldPlanner、EventProposer、WorldModelProvider、GenerativeSceneProvider、CounterfactualProvider、PopulationPolicyProvider、NarrativePlannerProvider。

允许输出：Observation / Prediction / Plan / Candidate / ProposedDelta / AssetCandidate / Confidence / ValidityEnvelope。

禁止：直接写 canonical DB、append WorldLedger、overwrite Snapshot、修改 World Definition、self-promote、修改 Kernel/Constitution。

必须提供：Deterministic/Fake Provider + Simple Offline Reference + External Adapter Contract。核心测试不依赖外部模型 key。


---

<!-- FILE: 06_FINAL_RELEASE_EVIDENCE.md -->

# M50 最终证据标准

最终至少生成：
- `reports/M43_BASELINE_AUDIT.md`
- `reports/MULTIVERSE_RUNTIME_ACCEPTANCE.md`
- `reports/INTERWORLD_IDENTITY_ACCEPTANCE.md`
- `reports/HYBRID_GENESIS_ACCEPTANCE.md`
- `reports/CROSS_WORLD_DISTILLATION_ACCEPTANCE.md`
- `reports/MULTIVERSE_STUDIO_E2E.md`
- `reports/WORLD_INTELLIGENCE_BOUNDARY_ACCEPTANCE.md`
- `reports/V5_3_BACKWARD_COMPATIBILITY.md`
- `reports/V5_3_SECURITY_RIGHTS_FINAL.md`
- `reports/V5_3_LONG_RUN_MULTI_WORLD.md`
- `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_3_FINAL_CERTIFICATION.md`
- `reports/GITHUB_DELIVERY_REPORT.md`
- `docs/RELEASE_READINESS_V5_3.md`

内部 M50 PASS 与 GitHub Push 分开：内部全部 PASS 后才能 push；GitHub 无权限可 EXTERNAL_BLOCKED，但不得伪造成功。


---

<!-- FILE: 07_GOALS_INDEX.md -->

# M43–M50 Goal Index

## M43
- **G46A** — M42 独立复核与 v5.3 基线冻结 — `goals/G46A_M42_独立复核与_v5.3_基线冻结.md`
- **G46B** — 创建 v5.3 工作分支与 Git 安全基线 — `goals/G46B_创建_v5.3_工作分支与_Git_安全基线.md`
- **G46C** — Kernel Freeze 自动 Guard — `goals/G46C_Kernel_Freeze_自动_Guard.md`
- **G46D** — v5.3 Delta Traceability — `goals/G46D_v5.3_Delta_Traceability.md`
- **G46E** — M43 Qualification — `goals/G46E_M43_Qualification.md`

## M44
- **G47A** — World Family / Multiverse Catalog — `goals/G47A_World_Family_Multiverse_Catalog.md`
- **G47B** — Multiverse Runtime Routing — `goals/G47B_Multiverse_Runtime_Routing.md`
- **G47C** — 多世界生命周期与资源隔离 — `goals/G47C_多世界生命周期与资源隔离.md`
- **G47D** — Lineage Query / Diff / Common Ancestor — `goals/G47D_Lineage_Query_Diff_Common_Ancestor.md`
- **G47E** — Multiverse Backup / Restore — `goals/G47E_Multiverse_Backup_Restore.md`
- **G47F** — M44 Multiverse Qualification — `goals/G47F_M44_Multiverse_Qualification.md`

## M45
- **G48A** — Interworld Identity / Presence — `goals/G48A_Interworld_Identity_Presence.md`
- **G48B** — Portal / Transfer Use Cases — `goals/G48B_Portal_Transfer_Use_Cases.md`
- **G48C** — Memory Sync Policy — `goals/G48C_Memory_Sync_Policy.md`
- **G48D** — Skill / Capability Mapping — `goals/G48D_Skill_Capability_Mapping.md`
- **G48E** — Item / Asset Interworld Semantics — `goals/G48E_Item_Asset_Interworld_Semantics.md`
- **G48F** — 跨世界因果与回写边界 — `goals/G48F_跨世界因果与回写边界.md`
- **G48G** — Interworld Reference Scenario — `goals/G48G_Interworld_Reference_Scenario.md`
- **G48H** — M45 Interworld Qualification — `goals/G48H_M45_Interworld_Qualification.md`

## M46
- **G49A** — Compatibility Analyzer — `goals/G49A_Compatibility_Analyzer.md`
- **G49B** — Identity Resolution Mapping — `goals/G49B_Identity_Resolution_Mapping.md`
- **G49C** — Ontology / Law Mapping — `goals/G49C_Ontology_Law_Mapping.md`
- **G49D** — History Inheritance Policy — `goals/G49D_History_Inheritance_Policy.md`
- **G49E** — Rights / Source Resolution — `goals/G49E_Rights_Source_Resolution.md`
- **G49F** — Hybrid Genesis Candidate Compiler — `goals/G49F_Hybrid_Genesis_Candidate_Compiler.md`
- **G49G** — Hybrid Genesis Reference World — `goals/G49G_Hybrid_Genesis_Reference_World.md`
- **G49H** — M46 Hybrid Qualification — `goals/G49H_M46_Hybrid_Qualification.md`

## M47
- **G50A** — Cross-world Telemetry Rights Gate — `goals/G50A_Cross-world_Telemetry_Rights_Gate.md`
- **G50B** — Cross-world Pattern Dataset — `goals/G50B_Cross-world_Pattern_Dataset.md`
- **G50C** — Domain Capability Candidate Distillation — `goals/G50C_Domain_Capability_Candidate_Distillation.md`
- **G50D** — Sandbox / Benchmark / Ablation — `goals/G50D_Sandbox_Benchmark_Ablation.md`
- **G50E** — Domain / Runtime Version Promotion — `goals/G50E_Domain_Runtime_Version_Promotion.md`
- **G50F** — M47 Cross-world Qualification — `goals/G50F_M47_Cross-world_Qualification.md`

## M48
- **G51A** — Multiverse Studio Family View — `goals/G51A_Multiverse_Studio_Family_View.md`
- **G51B** — Worldline / Derived World Compare — `goals/G51B_Worldline_Derived_World_Compare.md`
- **G51C** — Interworld Portal Experience — `goals/G51C_Interworld_Portal_Experience.md`
- **G51D** — Cross-world Actor Identity UX — `goals/G51D_Cross-world_Actor_Identity_UX.md`
- **G51E** — Hybrid Genesis Review UI — `goals/G51E_Hybrid_Genesis_Review_UI.md`
- **G51F** — Multiverse Experience E2E — `goals/G51F_Multiverse_Experience_E2E.md`
- **G51G** — M48 Qualification — `goals/G51G_M48_Qualification.md`

## M49
- **G52A** — World Intelligence Provider Contracts — `goals/G52A_World_Intelligence_Provider_Contracts.md`
- **G52B** — Deterministic Predictor Reference — `goals/G52B_Deterministic_Predictor_Reference.md`
- **G52C** — Planner / Event Proposer Reference — `goals/G52C_Planner_Event_Proposer_Reference.md`
- **G52D** — External World Model Adapter Seam — `goals/G52D_External_World_Model_Adapter_Seam.md`
- **G52E** — Generative Scene / Asset Candidate Boundary — `goals/G52E_Generative_Scene_Asset_Candidate_Boundary.md`
- **G52F** — World Intelligence Adversarial Tests — `goals/G52F_World_Intelligence_Adversarial_Tests.md`
- **G52G** — M49 Qualification — `goals/G52G_M49_Qualification.md`

## M50
- **G53A** — v5.3 Backward Compatibility Full Regression — `goals/G53A_v5.3_Backward_Compatibility_Full_Regression.md`
- **G53B** — Multi-world 30-day Stability — `goals/G53B_Multi-world_30-day_Stability.md`
- **G53C** — Security / Rights / Interworld Isolation Final — `goals/G53C_Security_Rights_Interworld_Isolation_Final.md`
- **G53D** — SDK / Docs / Examples v5.3 — `goals/G53D_SDK_Docs_Examples_v5.3.md`
- **G53E** — Release Notes / Migration Guide — `goals/G53E_Release_Notes_Migration_Guide.md`
- **G53F** — Final Acceptance Matrix / Certification — `goals/G53F_Final_Acceptance_Matrix_Certification.md`
- **G53G** — GitHub Pre-push Audit — `goals/G53G_GitHub_Pre-push_Audit.md`
- **G53H** — Push v5.3 Branch to GitHub — `goals/G53H_Push_v5.3_Branch_to_GitHub.md`
- **G53I** — Tag / GitHub Release Candidate — `goals/G53I_Tag_GitHub_Release_Candidate.md`
- **G53J** — M50 Final Stop — `goals/G53J_M50_Final_Stop.md`


---

<!-- FILE: 08_MILESTONE_GATES.md -->

# M43–M50 Milestone Gates

- **M43** — Post-M42 Verification & v5.3 Baseline — `milestones/M43_QUALIFICATION.md`
- **M44** — Multiverse Runtime & Lineage Operations — `milestones/M44_QUALIFICATION.md`
- **M45** — Interworld Identity / Presence / Portal — `milestones/M45_QUALIFICATION.md`
- **M46** — Hybrid Genesis / Compatibility Compiler — `milestones/M46_QUALIFICATION.md`
- **M47** — Cross-world Distillation & Promotion — `milestones/M47_QUALIFICATION.md`
- **M48** — Multiverse Studio / Experience — `milestones/M48_QUALIFICATION.md`
- **M49** — World Intelligence Provider Boundary — `milestones/M49_QUALIFICATION.md`
- **M50** — Release Qualification & GitHub Delivery — `milestones/M50_QUALIFICATION.md`


---

<!-- FILE: 09_RESUME_PROTOCOL.md -->

# Resume Protocol

上下文压缩/重启后依次读取：STATUS.md → PLAN.md → reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md → 最近 milestone → 最近 goal report → git status → git log -30 → 当前 Goal → failing tests。

从最早 ACTIVE/FAIL Goal 恢复，先跑最窄 regression，不重做已有可复现 PASS。


---

<!-- FILE: 10_CODEX_MASTER_LONG_PROMPT_CN.md -->

# Codex 长连续执行总指令：Wanxiang v5.3 M43–M50

继续当前已经完成 M42 的万相仓库，不新建项目，不从零重写。

## 总目标
今晚连续完成 `G46A → G53J`，对应 `M43 → M50`。完成 Multiverse Runtime、Interworld、Hybrid Genesis、Cross-world Distillation、Multiverse Studio/Experience、World Intelligence Provider Boundary、v5.3 Final Certification，并在最终认证后把 feature branch 推到 GitHub。

## 必读
1. README_FIRST.md
2. 00_PROGRAM_ARCHITECTURE.md
3. 01_KERNEL_FREEZE_AND_MINIMAL_CODE_POLICY.md
4. 02_GITHUB_DELIVERY_POLICY.md
5. 03_INTERWORLD_SEMANTICS.md
6. 04_HYBRID_GENESIS_STANDARD.md
7. 05_WORLD_INTELLIGENCE_BOUNDARY.md
8. 06_FINAL_RELEASE_EVIDENCE.md
9. 07_GOALS_INDEX.md
10. 08_MILESTONE_GATES.md
11. 09_RESUME_PROTOCOL.md
12. 仓库 M42/v5.2 reports + AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG + Git + tests + migrations
然后读完全部 `goals/` 与 `milestones/`。

## 连续执行
每个 Goal：盘点复用 → 实现 → 测试/负向/回放/迁移 → 文档/证据 → PASS 后本地 commit → 自动下一个。每个 Milestone 运行 Gate，FAIL 自己修，PASS 自动继续，不询问用户。

## 硬约束
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

## GitHub 授权与规则
用户明确授权最终正常 `git push`。先遵循 `02_GITHUB_DELIVERY_POLICY.md`。不 force push、不删除历史、不提交 secret/private/restricted corpus。优先 feature branch。remote/auth 可用则 push 并记录最终 SHA；`gh` 可用且权限允许可建 PR；最终认证 PASS 后才可选 push `v5.3.0-rc1` tag/release。若 remote/auth/permission 客观不可用，记录 EXTERNAL_BLOCKED，不伪造成功。

## 最终停止
只有内部 M50 条件全部 PASS，且 GitHub push 已 PASS 或有明确外部阻塞报告后，生成最终报告并停止。禁止自行开始 v5.4。


---

<!-- FILE: goals/G46A_M42_独立复核与_v5.3_基线冻结.md -->

# G46A — M42 独立复核与 v5.3 基线冻结

> Milestone：M43

## 目标

重新证明 v5.2 Production Release 可复现。

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

1. 读取 M42 final certification/Git/STATUS。
2. 运行 RedChamber/Family/Heritage/Campaign 关键回归。
3. 冻结 DB/package/event/API/performance goldens。

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

- 旧 semantic hash 一致。
- 无未解释 P0/P1。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G46A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g46a: M42 独立复核与 v5.3 基线冻结`，然后自动继续。


---

<!-- FILE: goals/G46B_创建_v5.3_工作分支与_Git_安全基线.md -->

# G46B — 创建 v5.3 工作分支与 Git 安全基线

> Milestone：M43

## 目标

建立安全连续提交与最终 GitHub 交付环境。

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

1. 检查 remote/current branch/auth。
2. main/master 上创建 feature/wanxiang-v5.3-multiverse。
3. 更新 gitignore/secret scan baseline。

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

- 无 secret tracked。
- branch/remote 状态记录。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G46B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g46b: 创建 v5.3 工作分支与 Git 安全基线`，然后自动继续。


---

<!-- FILE: goals/G46C_Kernel_Freeze_自动_Guard.md -->

# G46C — Kernel Freeze 自动 Guard

> Milestone：M43

## 目标

防止新功能污染 Kernel。

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

1. 加强 import/AST/path guard。
2. 禁止 interworld/hybrid/worldmodel 专名进入 Kernel。
3. 增加 approved proposal exception。

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

- 故意违规 fixture 可被捕获。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G46C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g46c: Kernel Freeze 自动 Guard`，然后自动继续。


---

<!-- FILE: goals/G46D_v5.3_Delta_Traceability.md -->

# G46D — v5.3 Delta Traceability

> Milestone：M43

## 目标

把新能力映射到旧系统。

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

1. Multiverse→Lineage/Host。
2. Interworld→Identity/Policy。
3. Hybrid→Forge。
4. World Intelligence→Capability Provider。

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

- 无新第二套系统。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G46D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g46d: v5.3 Delta Traceability`，然后自动继续。


---

<!-- FILE: goals/G46E_M43_Qualification.md -->

# G46E — M43 Qualification

> Milestone：M43

## 目标

冻结可开发基线。

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

1. 执行 M43 Gate。
2. 本地 commit。

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

- M42 金样 PASS。
- Kernel guard active。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G46E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g46e: M43 Qualification`，然后自动继续。


---

<!-- FILE: goals/G47A_World_Family_Multiverse_Catalog.md -->

# G47A — World Family / Multiverse Catalog

> Milestone：M44

## 目标

将 World Definition/Derived World 组织为可查询 family。

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

1. family IDs/root/descendants/promotion ancestry。
2. package/version refs。

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

- DAG 无环。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47a: World Family / Multiverse Catalog`，然后自动继续。


---

<!-- FILE: goals/G47B_Multiverse_Runtime_Routing.md -->

# G47B — Multiverse Runtime Routing

> Milestone：M44

## 目标

复用 World Host 支持多世界路由。

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

1. world/instance/worldline scoped commands。
2. runtime profile binding/resource budget。

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

- 同 local entity ID 不串世界。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47b: Multiverse Runtime Routing`，然后自动继续。


---

<!-- FILE: goals/G47C_多世界生命周期与资源隔离.md -->

# G47C — 多世界生命周期与资源隔离

> Milestone：M44

## 目标

并发运行多个 world instance。

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

1. per-instance pause/run/background。
2. quota/checkpoint independent。

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

- 一个 world crash 不破坏另一个。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47c: 多世界生命周期与资源隔离`，然后自动继续。


---

<!-- FILE: goals/G47D_Lineage_Query_Diff_Common_Ancestor.md -->

# G47D — Lineage Query / Diff / Common Ancestor

> Milestone：M44

## 目标

完善谱系操作。

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

1. ancestor/descendant/common ancestor。
2. definition/ontology/law/domain diff。

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

- 复杂 DAG 查询通过。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47d: Lineage Query / Diff / Common Ancestor`，然后自动继续。


---

<!-- FILE: goals/G47E_Multiverse_Backup_Restore.md -->

# G47E — Multiverse Backup / Restore

> Milestone：M44

## 目标

备份恢复保持 lineage。

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

1. selected/all worlds backup。
2. restore/lineage integrity。

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

- hash/ancestry 一致。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47e: Multiverse Backup / Restore`，然后自动继续。


---

<!-- FILE: goals/G47F_M44_Multiverse_Qualification.md -->

# G47F — M44 Multiverse Qualification

> Milestone：M44

## 目标

证明多世界并发隔离。

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

1. 4 个 world family fixture。
2. parallel lifecycle。

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

- 无 cross-world mutation leakage。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G47F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g47f: M44 Multiverse Qualification`，然后自动继续。


---

<!-- FILE: goals/G48A_Interworld_Identity_Presence.md -->

# G48A — Interworld Identity / Presence

> Milestone：M45

## 目标

实现 origin/presence identity。

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

1. typed refs/lifecycle/mapping provenance/rights refs。

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

- origin identity immutable。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48a: Interworld Identity / Presence`，然后自动继续。


---

<!-- FILE: goals/G48B_Portal_Transfer_Use_Cases.md -->

# G48B — Portal / Transfer Use Cases

> Milestone：M45

## 目标

实现跨世界 enter/return。

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

1. compatibility check/create presence/close presence。

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

- portal 不直接 mutate origin。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48b: Portal / Transfer Use Cases`，然后自动继续。


---

<!-- FILE: goals/G48C_Memory_Sync_Policy.md -->

# G48C — Memory Sync Policy

> Milestone：M45

## 目标

区分 local/portable/private memory。

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

1. sync policy/consent/redaction/return candidate。

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

- B 私密记忆不默认回 A。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48c: Memory Sync Policy`，然后自动继续。


---

<!-- FILE: goals/G48D_Skill_Capability_Mapping.md -->

# G48D — Skill / Capability Mapping

> Milestone：M45

## 目标

处理能力兼容。

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

1. skill mapping/disabled/translated/evidence。

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

- 不兼容 skill 被拒绝。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48d: Skill / Capability Mapping`，然后自动继续。


---

<!-- FILE: goals/G48E_Item_Asset_Interworld_Semantics.md -->

# G48E — Item / Asset Interworld Semantics

> Milestone：M45

## 目标

区分 transfer/copy/projection/token。

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

1. ownership/custody/rights/identity mapping。

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

- 同 physical item 不双重存在。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48e: Item / Asset Interworld Semantics`，然后自动继续。


---

<!-- FILE: goals/G48F_跨世界因果与回写边界.md -->

# G48F — 跨世界因果与回写边界

> Milestone：M45

## 目标

默认禁止反向污染。

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

1. explicit sync approval/conflict resolution。

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

- unauthorized reverse write fails。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48f: 跨世界因果与回写边界`，然后自动继续。


---

<!-- FILE: goals/G48G_Interworld_Reference_Scenario.md -->

# G48G — Interworld Reference Scenario

> Milestone：M45

## 目标

RedChamber actor → compatible synthetic world。

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

1. enter/act/return/compare。

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

- RedChamber origin unchanged。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48G_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48g: Interworld Reference Scenario`，然后自动继续。


---

<!-- FILE: goals/G48H_M45_Interworld_Qualification.md -->

# G48H — M45 Interworld Qualification

> Milestone：M45

## 目标

完成 identity/memory/skill/item/return 全链。

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

1. contract + E2E。

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

- 默认隔离全部 PASS。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G48H_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g48h: M45 Interworld Qualification`，然后自动继续。


---

<!-- FILE: goals/G49A_Compatibility_Analyzer.md -->

# G49A — Compatibility Analyzer

> Milestone：M46

## 目标

统一 Constitution/Identity/Ontology/Law/Rights 分析。

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

1. typed report/severity/mappings/rejection reasons。

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

- incompatible roots reject。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49a: Compatibility Analyzer`，然后自动继续。


---

<!-- FILE: goals/G49B_Identity_Resolution_Mapping.md -->

# G49B — Identity Resolution Mapping

> Milestone：M46

## 目标

显式处理 parent identities。

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

1. same/distinct/translated/collision/provenance。

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

- ambiguous requires review。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49b: Identity Resolution Mapping`，然后自动继续。


---

<!-- FILE: goals/G49C_Ontology_Law_Mapping.md -->

# G49C — Ontology / Law Mapping

> Milestone：M46

## 目标

生成 mapping candidate。

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

1. ontology map/law conflicts/domain compatibility。

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

- unresolved conflict blocks。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49c: Ontology / Law Mapping`，然后自动继续。


---

<!-- FILE: goals/G49D_History_Inheritance_Policy.md -->

# G49D — History Inheritance Policy

> Milestone：M46

## 目标

决定 child history refs。

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

1. reference vs seed/cutoff/no log concatenation。

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

- parents unchanged。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49d: History Inheritance Policy`，然后自动继续。


---

<!-- FILE: goals/G49E_Rights_Source_Resolution.md -->

# G49E — Rights / Source Resolution

> Milestone：M46

## 目标

多父来源权利解析。

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

1. rights intersection/exclusion/provenance union。

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

- rights conflict reject。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49e: Rights / Source Resolution`，然后自动继续。


---

<!-- FILE: goals/G49F_Hybrid_Genesis_Candidate_Compiler.md -->

# G49F — Hybrid Genesis Candidate Compiler

> Milestone：M46

## 目标

复用 Genesis/Package Assembler。

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

1. new ID/parent refs/mappings/genesis snapshot。

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

- candidate 不自动 publish。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49f: Hybrid Genesis Candidate Compiler`，然后自动继续。


---

<!-- FILE: goals/G49G_Hybrid_Genesis_Reference_World.md -->

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


---

<!-- FILE: goals/G49H_M46_Hybrid_Qualification.md -->

# G49H — M46 Hybrid Qualification

> Milestone：M46

## 目标

正向+拒绝路径。

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

1. positive/negative suites。

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

- 无无语义 merge。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G49H_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g49h: M46 Hybrid Qualification`，然后自动继续。


---

<!-- FILE: goals/G50A_Cross-world_Telemetry_Rights_Gate.md -->

# G50A — Cross-world Telemetry Rights Gate

> Milestone：M47

## 目标

授权后才可跨世界学习。

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

1. consent/filter/anonymization/retention。

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

- unapproved excluded。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50a: Cross-world Telemetry Rights Gate`，然后自动继续。


---

<!-- FILE: goals/G50B_Cross-world_Pattern_Dataset.md -->

# G50B — Cross-world Pattern Dataset

> Milestone：M47

## 目标

构建 domain-neutral dataset contract。

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

1. events/evals/metrics refs/versioned manifest。

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

- reproducible hash。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50b: Cross-world Pattern Dataset`，然后自动继续。


---

<!-- FILE: goals/G50C_Domain_Capability_Candidate_Distillation.md -->

# G50C — Domain Capability Candidate Distillation

> Milestone：M47

## 目标

从多个世界生成 reusable candidate。

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

1. pattern discovery/evidence/stability/candidate。

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

- 不自动 activate。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50c: Domain Capability Candidate Distillation`，然后自动继续。


---

<!-- FILE: goals/G50D_Sandbox_Benchmark_Ablation.md -->

# G50D — Sandbox / Benchmark / Ablation

> Milestone：M47

## 目标

复用 Runtime Evolution Lab。

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

1. shadow worlds/benchmark/ablation/security/cost/determinism。

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

- failed candidate reject。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50d: Sandbox / Benchmark / Ablation`，然后自动继续。


---

<!-- FILE: goals/G50E_Domain_Runtime_Version_Promotion.md -->

# G50E — Domain / Runtime Version Promotion

> Milestone：M47

## 目标

批准后形成新版本。

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

1. version release/runtime control ledger/future-only effect。

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

- 过去 replay 不变。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50e: Domain / Runtime Version Promotion`，然后自动继续。


---

<!-- FILE: goals/G50F_M47_Cross-world_Qualification.md -->

# G50F — M47 Cross-world Qualification

> Milestone：M47

## 目标

Worlds→Candidate→Sandbox→vNext。

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

1. multi-world synthetic evidence。

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

- world 不能 self-upgrade platform。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G50F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g50f: M47 Cross-world Qualification`，然后自动继续。


---

<!-- FILE: goals/G51A_Multiverse_Studio_Family_View.md -->

# G51A — Multiverse Studio Family View

> Milestone：M48

## 目标

显示 world family/lineage DAG。

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

1. reuse graph/filter/ancestor/diff/promotion refs。

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

- UI no authority。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51a: Multiverse Studio Family View`，然后自动继续。


---

<!-- FILE: goals/G51B_Worldline_Derived_World_Compare.md -->

# G51B — Worldline / Derived World Compare

> Milestone：M48

## 目标

比较世界差异。

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

1. facts/actors/ontology/laws/packages/history refs。

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

- diff traceable。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51b: Worldline / Derived World Compare`，然后自动继续。


---

<!-- FILE: goals/G51C_Interworld_Portal_Experience.md -->

# G51C — Interworld Portal Experience

> Milestone：M48

## 目标

用户合法进入另一世界。

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

1. eligibility/preview/enter/return UX。

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

- server-side permissions。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51c: Interworld Portal Experience`，然后自动继续。


---

<!-- FILE: goals/G51D_Cross-world_Actor_Identity_UX.md -->

# G51D — Cross-world Actor Identity UX

> Milestone：M48

## 目标

展示 origin/presence/memory/skill boundaries。

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

1. badges/sync choices/privacy warnings。

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

- no accidental leakage。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51d: Cross-world Actor Identity UX`，然后自动继续。


---

<!-- FILE: goals/G51E_Hybrid_Genesis_Review_UI.md -->

# G51E — Hybrid Genesis Review UI

> Milestone：M48

## 目标

审核 compatibility/mappings/rights/child。

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

1. review/approve-reject/preview lineage。

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

- permissions enforced。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51e: Hybrid Genesis Review UI`，然后自动继续。


---

<!-- FILE: goals/G51F_Multiverse_Experience_E2E.md -->

# G51F — Multiverse Experience E2E

> Milestone：M48

## 目标

A→portal→B→return→compare。

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

1. Playwright/reconnect/lineage view。

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

- histories intact。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51f: Multiverse Experience E2E`，然后自动继续。


---

<!-- FILE: goals/G51G_M48_Qualification.md -->

# G51G — M48 Qualification

> Milestone：M48

## 目标

产品面多元宇宙验收。

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

1. Studio+Experience gate。

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

- no mock-only flow。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G51G_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g51g: M48 Qualification`，然后自动继续。


---

<!-- FILE: goals/G52A_World_Intelligence_Provider_Contracts.md -->

# G52A — World Intelligence Provider Contracts

> Milestone：M49

## 目标

定义预测/规划/world model 契约。

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

1. interfaces/input/output/validity metadata。

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

- no mutable state handle。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52a: World Intelligence Provider Contracts`，然后自动继续。


---

<!-- FILE: goals/G52B_Deterministic_Predictor_Reference.md -->

# G52B — Deterministic Predictor Reference

> Milestone：M49

## 目标

提供离线 predictor。

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

1. simple forecast/confidence/seed。

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

- reproducible。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52b: Deterministic Predictor Reference`，然后自动继续。


---

<!-- FILE: goals/G52C_Planner_Event_Proposer_Reference.md -->

# G52C — Planner / Event Proposer Reference

> Milestone：M49

## 目标

提供 heuristic planner。

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

1. plan candidates/preconditions/no commit。

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

- invalid proposal rejected normally。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52c: Planner / Event Proposer Reference`，然后自动继续。


---

<!-- FILE: goals/G52D_External_World_Model_Adapter_Seam.md -->

# G52D — External World Model Adapter Seam

> Milestone：M49

## 目标

定义外部世界模型适配。

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

1. descriptor/schema/timeout/error/fallback。

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

- fake contract。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52d: External World Model Adapter Seam`，然后自动继续。


---

<!-- FILE: goals/G52E_Generative_Scene_Asset_Candidate_Boundary.md -->

# G52E — Generative Scene / Asset Candidate Boundary

> Milestone：M49

## 目标

视觉生成只成 AssetCandidate。

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

1. semantic binding/rights/review/projection package。

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

- 不能改 canonical facts。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52e: Generative Scene / Asset Candidate Boundary`，然后自动继续。


---

<!-- FILE: goals/G52F_World_Intelligence_Adversarial_Tests.md -->

# G52F — World Intelligence Adversarial Tests

> Milestone：M49

## 目标

测试越权/幻觉/injection。

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

1. malicious provider/future leak/self-promotion。

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

- 全部 blocked。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52f: World Intelligence Adversarial Tests`，然后自动继续。


---

<!-- FILE: goals/G52G_M49_Qualification.md -->

# G52G — M49 Qualification

> Milestone：M49

## 目标

世界智能可插拔且 authority 不变。

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

1. offline/fake/optional adapter。

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

- core tests no model key。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G52G_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g52g: M49 Qualification`，然后自动继续。


---

<!-- FILE: goals/G53A_v5.3_Backward_Compatibility_Full_Regression.md -->

# G53A — v5.3 Backward Compatibility Full Regression

> Milestone：M50

## 目标

重跑 v5.2 fixtures。

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

1. RedChamber/Family/Heritage/Campaign/old DB/package/event/SDK。

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

- critical regression PASS。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53A_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53a: v5.3 Backward Compatibility Full Regression`，然后自动继续。


---

<!-- FILE: goals/G53B_Multi-world_30-day_Stability.md -->

# G53B — Multi-world 30-day Stability

> Milestone：M50

## 目标

多个世界同时长稳。

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

1. 4+ instances/30 days/checkpoint/recovery/budgets。

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

- bounded growth。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53B_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53b: Multi-world 30-day Stability`，然后自动继续。


---

<!-- FILE: goals/G53C_Security_Rights_Interworld_Isolation_Final.md -->

# G53C — Security / Rights / Interworld Isolation Final

> Milestone：M50

## 目标

攻击跨世界与 Hybrid 权限。

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

1. rights leakage/identity spoof/portal escalation/malicious package/provider。

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

- no P0/P1。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53C_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53c: Security / Rights / Interworld Isolation Final`，然后自动继续。


---

<!-- FILE: goals/G53D_SDK_Docs_Examples_v5.3.md -->

# G53D — SDK / Docs / Examples v5.3

> Milestone：M50

## 目标

更新 public SDK/docs。

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

1. multiverse APIs/interworld examples/hybrid tutorial/world intelligence guide。

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

- examples no internal imports。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53D_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53d: SDK / Docs / Examples v5.3`，然后自动继续。


---

<!-- FILE: goals/G53E_Release_Notes_Migration_Guide.md -->

# G53E — Release Notes / Migration Guide

> Milestone：M50

## 目标

v5.2→v5.3 迁移。

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

1. features/breaking/deprecation/DB/package/API/rollback。

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

- clean clone instructions validated。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53E_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53e: Release Notes / Migration Guide`，然后自动继续。


---

<!-- FILE: goals/G53F_Final_Acceptance_Matrix_Certification.md -->

# G53F — Final Acceptance Matrix / Certification

> Milestone：M50

## 目标

spec→code→test→runtime evidence。

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

1. all milestones/limitations/kernel diff audit。

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

- all internal P0/P1 closed。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53F_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53f: Final Acceptance Matrix / Certification`，然后自动继续。


---

<!-- FILE: goals/G53G_GitHub_Pre-push_Audit.md -->

# G53G — GitHub Pre-push Audit

> Milestone：M50

## 目标

上传前安全检查。

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

1. status/tracked/secret/large/private/source scan/remote/auth/final tests。

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

- no unsafe tracked content。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53G_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53g: GitHub Pre-push Audit`，然后自动继续。


---

<!-- FILE: goals/G53H_Push_v5.3_Branch_to_GitHub.md -->

# G53H — Push v5.3 Branch to GitHub

> Milestone：M50

## 目标

推送认证分支。

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

1. git push -u origin feature/wanxiang-v5.3-multiverse。
2. 记录 remote/branch/SHA。
3. 可选 PR。

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

- remote contains final SHA 或明确 external blocked。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53H_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53h: Push v5.3 Branch to GitHub`，然后自动继续。


---

<!-- FILE: goals/G53I_Tag_GitHub_Release_Candidate.md -->

# G53I — Tag / GitHub Release Candidate

> Milestone：M50

## 目标

权限允许时发布 v5.3.0-rc1。

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

1. annotated tag/push tag/optional gh release。

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

- tag points certified commit。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53I_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53i: Tag / GitHub Release Candidate`，然后自动继续。


---

<!-- FILE: goals/G53J_M50_Final_Stop.md -->

# G53J — M50 Final Stop

> Milestone：M50

## 目标

最终报告并停止。

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

1. STATUS/PLAN/CHANGELOG/final report/working tree。

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

- certification exists；不开始 v5.4。

并运行所有适用 unit / contract / integration / property / replay / migration / architecture / security / E2E / lint / typecheck / build。

## Acceptance

- Scope 有真实实现与证据；
- 所列测试 PASS；
- 无 authority bypass；
- 无未批准 Kernel semantic change；
- 无重复核心系统；
- schema 变化有 migration/compatibility；
- 更新 `reports/G53J_REPORT.md` 与 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`；
- 内部工程问题不得标 EXTERNAL_BLOCKED；
- GitHub/auth/permission 仅可在 G53H/G53I 标 EXTERNAL_BLOCKED。

## Git

PASS 后本地 commit：`g53j: M50 Final Stop`，然后自动继续。


---

<!-- FILE: milestones/M43_QUALIFICATION.md -->

# M43 — Post-M42 Verification & v5.3 Baseline

## Required Goals

- G46A PASS — M42 独立复核与 v5.3 基线冻结
- G46B PASS — 创建 v5.3 工作分支与 Git 安全基线
- G46C PASS — Kernel Freeze 自动 Guard
- G46D PASS — v5.3 Delta Traceability
- G46E PASS — M43 Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M43_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M44_QUALIFICATION.md -->

# M44 — Multiverse Runtime & Lineage Operations

## Required Goals

- G47A PASS — World Family / Multiverse Catalog
- G47B PASS — Multiverse Runtime Routing
- G47C PASS — 多世界生命周期与资源隔离
- G47D PASS — Lineage Query / Diff / Common Ancestor
- G47E PASS — Multiverse Backup / Restore
- G47F PASS — M44 Multiverse Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M44_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M45_QUALIFICATION.md -->

# M45 — Interworld Identity / Presence / Portal

## Required Goals

- G48A PASS — Interworld Identity / Presence
- G48B PASS — Portal / Transfer Use Cases
- G48C PASS — Memory Sync Policy
- G48D PASS — Skill / Capability Mapping
- G48E PASS — Item / Asset Interworld Semantics
- G48F PASS — 跨世界因果与回写边界
- G48G PASS — Interworld Reference Scenario
- G48H PASS — M45 Interworld Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M45_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M46_QUALIFICATION.md -->

# M46 — Hybrid Genesis / Compatibility Compiler

## Required Goals

- G49A PASS — Compatibility Analyzer
- G49B PASS — Identity Resolution Mapping
- G49C PASS — Ontology / Law Mapping
- G49D PASS — History Inheritance Policy
- G49E PASS — Rights / Source Resolution
- G49F PASS — Hybrid Genesis Candidate Compiler
- G49G PASS — Hybrid Genesis Reference World
- G49H PASS — M46 Hybrid Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M46_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M47_QUALIFICATION.md -->

# M47 — Cross-world Distillation & Promotion

## Required Goals

- G50A PASS — Cross-world Telemetry Rights Gate
- G50B PASS — Cross-world Pattern Dataset
- G50C PASS — Domain Capability Candidate Distillation
- G50D PASS — Sandbox / Benchmark / Ablation
- G50E PASS — Domain / Runtime Version Promotion
- G50F PASS — M47 Cross-world Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M47_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M48_QUALIFICATION.md -->

# M48 — Multiverse Studio / Experience

## Required Goals

- G51A PASS — Multiverse Studio Family View
- G51B PASS — Worldline / Derived World Compare
- G51C PASS — Interworld Portal Experience
- G51D PASS — Cross-world Actor Identity UX
- G51E PASS — Hybrid Genesis Review UI
- G51F PASS — Multiverse Experience E2E
- G51G PASS — M48 Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M48_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M49_QUALIFICATION.md -->

# M49 — World Intelligence Provider Boundary

## Required Goals

- G52A PASS — World Intelligence Provider Contracts
- G52B PASS — Deterministic Predictor Reference
- G52C PASS — Planner / Event Proposer Reference
- G52D PASS — External World Model Adapter Seam
- G52E PASS — Generative Scene / Asset Candidate Boundary
- G52F PASS — World Intelligence Adversarial Tests
- G52G PASS — M49 Qualification

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M49_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。


---

<!-- FILE: milestones/M50_QUALIFICATION.md -->

# M50 — Release Qualification & GitHub Delivery

## Required Goals

- G53A PASS — v5.3 Backward Compatibility Full Regression
- G53B PASS — Multi-world 30-day Stability
- G53C PASS — Security / Rights / Interworld Isolation Final
- G53D PASS — SDK / Docs / Examples v5.3
- G53E PASS — Release Notes / Migration Guide
- G53F PASS — Final Acceptance Matrix / Certification
- G53G PASS — GitHub Pre-push Audit
- G53H PASS — Push v5.3 Branch to GitHub
- G53I PASS — Tag / GitHub Release Candidate
- G53J PASS — M50 Final Stop

## Gate
运行本 Milestone 全部 unit/contract/integration/E2E、Kernel freeze guard、Replay/Branch/Lineage regression、migration、security、lint/type/build。

生成 `reports/M50_QUALIFICATION.md`。内部 FAIL 必须修复；PASS 后自动继续。
