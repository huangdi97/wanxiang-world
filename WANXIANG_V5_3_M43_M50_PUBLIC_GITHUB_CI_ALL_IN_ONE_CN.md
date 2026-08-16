# WANXIANG v5.3 M43–M50 + Public GitHub + CI ALL-IN-ONE 中文最终版


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


## Public Open-source / CI 新增强制证据

- reports/OPEN_SOURCE_READINESS_AUDIT.md
- reports/OSS_LICENSE_AND_RIGHTS_AUDIT.md
- reports/GITHUB_CI_REPORT.md
- reports/GITHUB_DELIVERY_REPORT.md
- public GitHub repository URL
- final commit SHA
- final GitHub Actions run IDs/URLs
- v5.3.0-rc1 tag
- GitHub Release URL（若权限可用）

M50 的远端发布完成必须以 GitHub 实际状态为准，不能只以本地命令返回 0 推断。


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

### M50 开源发布扩展（替换旧 G53G–G53J）
- **G53G** — Open-source Readiness 与公开历史安全审计 — `goals/G53G_Open-source_Readiness_与公开历史安全审计.md`
- **G53H** — 开源治理、License、README 与贡献者入口 — `goals/G53H_开源治理_License_README_与贡献者入口.md`
- **G53I** — GitHub Actions CI / Code Quality / Supply-chain 自动化 — `goals/G53I_GitHub_Actions_CI_Code_Quality_Supply-chain_自动化.md`
- **G53J** — 自动创建 Public GitHub Repository 并首次 Push — `goals/G53J_自动创建_Public_GitHub_Repository_并首次_Push.md`
- **G53K** — 远端 GitHub Actions CI 真实运行、修复与全绿 — `goals/G53K_远端_GitHub_Actions_CI_真实运行_修复与全绿.md`
- **G53L** — v5.3.0-rc1 Tag、GitHub Release、最终开源认证与停止 — `goals/G53L_v5_3_0-rc1_Tag_GitHub_Release_最终开源认证与停止.md`


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

# 【最高优先级补充】Public GitHub + CI 自动发布闭环

用户已经明确授权：本轮完成后**直接开源**，自动创建 GitHub public repository、push，并建立/验证 CI。

因此从 G53G 起，旧的“只 push feature branch/可选公开”策略被本补充覆盖。严格读取：

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- 新版 G53G–G53L

最终必须连续执行：

```text
G53F 本地 Final Certification
→ G53G Open-source Readiness / history safety
→ G53H OSS license/docs/governance
→ G53I GitHub Actions CI preparation
→ G53J gh repo create PUBLIC + push
→ G53K gh run 查询远端 CI；失败则修复并再次 push，直到核心 CI 全绿
→ G53L tag v5.3.0-rc1 + GitHub Release Candidate + final report
→ STOP
```

默认 repo：`wanxiang-world`；冲突时使用 `wanxiang-world-os` / `wanxiang-world-engine`。

若当前仓库没有 LICENSE，默认代码许可证使用 Apache-2.0；但代码许可证绝不能覆盖或暗示覆盖第三方/受限数据与资产。

特别注意完整《红楼梦》：只有 rights metadata 明确允许公开再分发的 corpus 才能进入公开 Git history。否则公开仓库只保留 Source/Import/Manifest/Parser/Fixture/Documentation，底本文本保留在 ignored local data storage，不删除用户本地原件。

远端 CI 是 Acceptance：不得在 CI 失败时停止，也不得通过 disable workflow、skip test、删测试制造假绿。必须读日志、修复、push，直到 final commit 的核心 GitHub Actions 全绿。


---

<!-- FILE: 11_OPEN_SOURCE_GITHUB_CI_POLICY.md -->

# M50 开源发布、GitHub 自动建仓与 CI 正式政策

## 1. 本轮最终交付不是“本地代码完成”

M50 的最终完成链必须是：

```text
M43–M49 全部 PASS
→ M50 本地全量回归 PASS
→ Open-source Readiness Audit
→ 清除/排除不能公开的内容
→ 完成开源元数据与治理文件
→ 完成 GitHub Actions CI
→ 创建 public GitHub repository
→ push 所有可公开代码与 Git 历史
→ GitHub Actions 真实触发
→ 查询远端 workflow run
→ 若 CI 失败则定位、修复、commit、再次 push
→ 远端 required CI 全绿
→ tag v5.3.0-rc1
→ GitHub Release Candidate
→ GITHUB_DELIVERY_REPORT
→ M50 PASS
```

## 2. 默认公开仓库

优先仓库名：`wanxiang-world`。

若当前 GitHub 账号已存在同名仓库，依次尝试：

1. `wanxiang-world-os`
2. `wanxiang-world-engine`

不得因为名称冲突覆盖或删除已有仓库。

仓库 visibility：**public**。

Description：

`Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS`

推荐 topics：

`world-model`, `world-os`, `multi-agent`, `simulation`, `digital-humanities`, `generative-agents`, `python`, `typescript`, `fastapi`, `react`

## 3. License

若仓库已有明确 LICENSE：保留，不自动改变。

若没有 LICENSE：本执行程序默认采用 **Apache License 2.0** 作为代码许可证，并在 README 清楚说明：

- Apache-2.0 只覆盖本仓库明确标记的原创代码/文档；
- 第三方依赖遵循各自许可证；
- 文学底本、现代校注本、图片、声音、模型、3D 资产、博物馆数据、家庭数据等不因代码开源自动获得 Apache-2.0 授权；
- 只有 rights metadata 明确允许再分发的示例数据才可进入公开 Git history。

新增 `DATA_AND_ASSET_RIGHTS.md` 说明数据与资产权利边界。

## 4. 开源前必须存在的仓库文件

至少：

- `README.md`
- `README_EN.md` 或 README 中完整英文摘要
- `LICENSE`
- `NOTICE`（若项目使用 Apache-2.0 且有需声明事项）
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `DATA_AND_ASSET_RIGHTS.md`
- `CHANGELOG.md`
- `.gitignore`
- `.gitattributes`
- `.env.example`（只能有占位符）
- `docs/architecture/` 的公开架构入口
- `docs/quickstart/` 或等价 Quickstart
- `docs/package-authoring/` 或等价第三方 World/Domain Pack 教程

## 5. 绝不能公开提交的内容

push 前必须自动检查并排除：

- `.env`、API key、token、credential、cookie、SSH private key；
- 本地数据库、生产数据库 dump；
- 真实个人/家庭隐私数据；
- 未明确允许公开再分发的《红楼梦》现代电子底本/校注本；
- 博物馆受限图像/3D/内部资料；
- 模型权重/缓存；
- 大型 build/cache/temp 文件；
- 用户本地路径、调试日志中的凭证；
- `.venv`, `node_modules`, generated caches；
- 未获得再分发权的第三方素材。

不得通过“删用户本地文件”来解决：优先 `.gitignore`、取消 tracking、迁移到 ignored/local data directory；保留本地原件。

## 6. Git 历史安全

如果 secret/私有数据曾经进入历史：

- 在公开前必须识别；
- 不得只从最新 commit 删除就认为安全；
- 如必须清理 Git history，先创建本地备份 tag/branch，并在报告中记录；
- 不对已有远端做 force push（本仓库尚未存在远端时，可以在首次公开前安全清理本地历史）；
- 任何已泄露 credential 必须视为需要撤销/轮换，不能只改 Git。

## 7. GitHub 创建与 push

只有本地工程、开源审核和 CI 文件全部通过后才创建远端。

若 `gh auth status` PASS 且账号具有建仓权限，可非交互创建：

```bash
gh repo create wanxiang-world --public --source=. --remote=origin --push \
  --description "Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS"
```

具体命令应根据现有 remote/branch 状态安全调整，不机械重复 `origin`。

## 8. Main 与 feature branch

- 不 force push。
- 若本地已有稳定 `main`，首次建仓应推送它。
- 本轮 `feature/wanxiang-v5.3-multiverse` 也要推送。
- 如果 M50 的认证 commit 在 feature branch，优先创建 PR 到 main。
- 只有仓库历史与测试明确适合时才自动 merge；否则保留 PR，不冒险 merge。

## 9. 远端 CI 是正式验收的一部分

“`.github/workflows/ci.yml` 存在”不等于 CI 完成。

Codex 必须：

1. push；
2. 使用 `gh run list` / `gh run view` 查询 workflow；
3. 等待/轮询到 workflow 结束；
4. 对失败 job 获取日志；
5. 修复代码或 workflow；
6. commit + push；
7. 直到核心 workflow PASS；
8. 把 run URL/ID、commit SHA、结论写入报告。

如果 GitHub 服务/权限客观不可用才允许 `EXTERNAL_BLOCKED`。


---

<!-- FILE: 12_GITHUB_ACTIONS_CI_SPEC.md -->

# GitHub Actions CI / Open-source Automation 规范

## 1. CI 触发

主 CI 至少对：

- push 到 `main` / feature branches；
- pull_request 到 `main`；

触发。

可对 docs-only changes 使用 path filtering，但不得因此漏掉会影响构建的配置改动。

## 2. CI Jobs

根据仓库真实技术栈实现，不要写不存在的命令。至少覆盖：

### A. repository-safety

- 基础 secret pattern scan / 已有 secret scanner；
- 禁止提交 `.env`、DB dump、known private corpus path；
- 检查超大非必要 tracked files；
- license / required OSS metadata sanity。

### B. python-quality

- 安装仓库指定 Python（至少当前主版本；若项目明确兼容 3.11/3.12，可 matrix）；
- dependency install；
- Ruff/lint；
- format check；
- typecheck；
- unit tests。

### C. core-contracts

- architecture conformance；
- Commit Boundary tests；
- Replay / Branch / Worldline / Lineage；
- deterministic reference tests；
- Kernel freeze guard。

### D. integration

- SQLite integration；
- PostgreSQL service container（若仓库生产支持 PostgreSQL）；
- migrations upgrade；
- API contract / OpenAPI；
- package install/upgrade smoke。

### E. web-quality

若存在 web workspace：

- pnpm install --frozen-lockfile（按真实 lockfile 调整）；
- lint；
- TypeScript typecheck；
- unit tests；
- production build。

### F. e2e-smoke

- 启动必要 backend/frontend；
- Playwright 或现有 E2E；
- 至少跑不依赖真实 LLM key 的 deterministic smoke。

### G. packaging

- Python package/build（如果项目可打包）；
- TS SDK build；
- World/Domain package certification smoke；
- 检查生成 artifacts 能在 clean environment 使用。

## 3. 可拆分 workflow

推荐：

```text
.github/workflows/
  ci.yml
  codeql.yml              # 若适用
  release.yml             # tag/release 构建
  docs.yml                # 仅项目已有文档站时
```

不要为了“看起来专业”建立大量重复 workflow。

## 4. Action 安全

- 优先 GitHub 官方或公认维护良好的 actions；
- 使用当前受支持 major version，并在实现时验证；
- 第三方 action 必须必要且来源可信；
- 最小 `permissions:`；
- PR workflow 不给不需要的 write 权限；
- 不把 repository secrets 暴露给不可信 fork PR。

## 5. 无外部模型依赖

CI 必须在没有 OpenAI/Anthropic/DeepSeek 等 API key 时通过核心测试。

外部 provider tests 使用 fake/deterministic adapters；真实在线模型测试只能是 opt-in/non-required workflow。

## 6. Dependabot / Supply Chain

如果仓库使用 GitHub Dependabot，创建 `.github/dependabot.yml`，至少覆盖实际使用的 package ecosystems（例如 pip/uv、npm/pnpm、github-actions）。

不要创建与仓库不匹配的 ecosystem。

## 7. CodeQL

公开仓库可增加 GitHub CodeQL workflow；但它是补充，不代替普通 CI。

只配置仓库实际存在且 CodeQL 支持的语言。

## 8. Release workflow

`v*` tag 可触发 release build/check：

- 重跑最小 release gate；
- 构建 package artifacts；
- 生成 checksums；
- 不自动发布到 PyPI/npm，除非后续用户明确授权 registry publishing；
- GitHub Release 可以附 release notes 与安全可公开 artifacts。

## 9. CI 成功标准

必须以 GitHub 远端 workflow run 的 conclusion 为准，而不是本地推测。

报告至少记录：

- workflow name；
- run ID / URL；
- commit SHA；
- jobs；
- result；
- 首次失败原因（若有）；
- 修复 commit；
- 最终 PASS run。


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

<!-- FILE: goals/G53G_Open-source_Readiness_与公开历史安全审计.md -->

# G53G — Open-source Readiness 与公开历史安全审计

> Milestone：M50

## Objective

把当前生产仓库变成可以安全公开的源码仓库，而不是直接 git add/push。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 盘点全部 tracked/untracked/ignored 文件与 Git history。
2. 扫描 secret/token/private key/credential。
3. 扫描 DB dump、个人数据、受限文学 corpus、博物馆受限资产、模型缓存和大文件。
4. 检查历史中是否曾提交不应公开内容；必要时在首次远端创建前安全清理本地 Git history，并保留本地备份引用。
5. 生成 OPEN_SOURCE_FILE_ALLOWLIST / DENYLIST 或等价机器可检查规则。
6. 确认所有公开示例数据的 rights metadata。

## Tests / Verification

- fresh git clone-equivalent export 不包含 denylist 内容。
- secret scan PASS。
- public tracked-file audit PASS。
- M42/M50 本地回归不因清理被破坏。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53G_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


---

<!-- FILE: goals/G53H_开源治理_License_README_与贡献者入口.md -->

# G53H — 开源治理、License、README 与贡献者入口

> Milestone：M50

## Objective

补齐真正开源项目需要的许可证、治理、说明和数据权利边界。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 若已有 LICENSE 则保留；若无则加入 Apache-2.0。
2. 完善 README 中文主入口与英文摘要/README_EN。
3. 创建/完善 CONTRIBUTING、CODE_OF_CONDUCT、SECURITY。
4. 创建 DATA_AND_ASSET_RIGHTS，明确代码与 corpus/assets 权利分离。
5. 补 Quickstart、Architecture、Package Authoring、Development Setup。
6. 确保 .env.example 只有占位符。

## Tests / Verification

- README 中所有核心 quickstart 命令在 clean environment 可执行。
- LICENSE/rights 文档不存在互相冲突声明。
- 不存在真实 credential。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53H_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


---

<!-- FILE: goals/G53I_GitHub_Actions_CI_Code_Quality_Supply-chain_自动化.md -->

# G53I — GitHub Actions CI / Code Quality / Supply-chain 自动化

> Milestone：M50

## Objective

在创建远端前把可执行 CI workflow 写好并尽可能本地验证。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 创建主 CI workflow，覆盖 Python lint/format/type/test、Kernel/Replay/Lineage contracts、integration/migrations、Web lint/type/test/build、E2E smoke、packaging（按仓库真实能力）。
2. 配置最小 workflow permissions。
3. 如适用增加 CodeQL。
4. 如适用增加 Dependabot 配置。
5. 创建 tag/release workflow，但不得自动发布 PyPI/npm。
6. 验证 YAML、脚本和 CI commands 在本地等价执行 PASS。

## Tests / Verification

- 所有 workflow 配置语法可验证。
- 本地执行 CI 对应命令全部 PASS。
- 核心 CI 无外部 LLM key 依赖。
- fork PR 不获得不必要 write/secrets。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53I_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


---

<!-- FILE: goals/G53J_自动创建_Public_GitHub_Repository_并首次_Push.md -->

# G53J — 自动创建 Public GitHub Repository 并首次 Push

> Milestone：M50

## Objective

在所有本地工程/开源门通过后，从现有本地 Git 仓库自动创建公开 GitHub 仓库并推送。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 检查 gh auth status、git remote、current branch。
2. 优先仓库名 wanxiang-world；冲突则使用允许的 fallback，绝不覆盖现有仓库。
3. 使用当前 Git history 创建 public repo，不重新生成一个无历史项目。
4. 设置 origin。
5. 推送 main/stable branch 与 feature/wanxiang-v5.3-multiverse（存在时）。
6. 设置 description/topics（权限支持时）。
7. 记录 repository URL、default branch、remote SHA。

## Tests / Verification

- GitHub repository visibility=PUBLIC。
- 远端可读取最终公开 commit。
- 本地/远端 SHA 对应。
- Git remote 配置正确。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53J_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


---

<!-- FILE: goals/G53K_远端_GitHub_Actions_CI_真实运行_修复与全绿.md -->

# G53K — 远端 GitHub Actions CI 真实运行、修复与全绿

> Milestone：M50

## Objective

把远端 CI run 本身作为正式 Acceptance，而不是只确认 workflow 文件已提交。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 使用 gh run list/view 查询刚 push 触发的 workflow。
2. 等待核心 CI workflow 完成。
3. 若失败，获取失败 job/log，定位真实原因。
4. 修复代码/workflow，运行本地验证，commit + push。
5. 重复直到所有 required/core workflows PASS。
6. 生成 GITHUB_CI_REPORT，记录 run IDs/URLs/SHA/失败与修复历史。

## Tests / Verification

- 最终 commit 对应的核心 CI conclusion=success。
- 无通过取消/disable workflow/删除测试制造的假绿。
- 远端 CI 与本地认证 commit 对应。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53K_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


---

<!-- FILE: goals/G53L_v5_3_0-rc1_Tag_GitHub_Release_最终开源认证与停止.md -->

# G53L — v5.3.0-rc1 Tag、GitHub Release、最终开源认证与停止

> Milestone：M50

## Objective

在远端 CI 全绿后发布 RC tag/release，并完成最终交付证明。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 重新确认 final certification 与 working tree clean。
2. 创建 annotated tag v5.3.0-rc1（若名称未被占用且指向当前认证 commit）。
3. push tag。
4. 触发并验证 release workflow。
5. 使用 gh release create 或等价方式创建 GitHub Release Candidate，附 release notes；只上传可公开 artifacts。
6. 记录 repo URL、tag、release URL、final SHA、CI run URLs。
7. 更新 STATUS/PLAN/CHANGELOG，生成最终开源认证并停止；不开始 v5.4。

## Tests / Verification

- Tag 指向最终认证 SHA。
- Release 公开可见。
- Release workflow PASS。
- GITHUB_DELIVERY_REPORT 与 V5_3_FINAL_CERTIFICATION 完整。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53L_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。


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

# M50 — Release Qualification + Public GitHub + Remote CI

## Required Goals

- G53A PASS — `G53A_v5.3_Backward_Compatibility_Full_Regression.md`
- G53B PASS — `G53B_Multi-world_30-day_Stability.md`
- G53C PASS — `G53C_Security_Rights_Interworld_Isolation_Final.md`
- G53D PASS — `G53D_SDK_Docs_Examples_v5.3.md`
- G53E PASS — `G53E_Release_Notes_Migration_Guide.md`
- G53F PASS — `G53F_Final_Acceptance_Matrix_Certification.md`
- G53G PASS — Open-source Readiness 与公开历史安全审计
- G53H PASS — 开源治理、License、README 与贡献者入口
- G53I PASS — GitHub Actions CI / Code Quality / Supply-chain 自动化
- G53J PASS — 自动创建 Public GitHub Repository 并首次 Push
- G53K PASS — 远端 GitHub Actions CI 真实运行、修复与全绿
- G53L PASS — v5.3.0-rc1 Tag、GitHub Release、最终开源认证与停止

## Final Gate

M50 只有在以下条件全部满足时才 PASS：

1. v5.3 内部 final certification PASS；
2. Open-source Readiness PASS；
3. Public GitHub repository 已创建；
4. final commit 已 push；
5. GitHub Actions 核心 CI 在远端对 final commit 实际 PASS；
6. v5.3.0-rc1 tag/release 成功，或 GitHub 权限/服务明确 EXTERNAL_BLOCKED；
7. 不存在 secret/private/restricted corpus 泄漏；
8. reports/GITHUB_DELIVERY_REPORT.md 和 reports/GITHUB_CI_REPORT.md 完整。

如果 GitHub auth/permission/service 客观阻塞，可标 GITHUB_DELIVERY=EXTERNAL_BLOCKED，但不得把 M50 伪装成“远端发布完成”。
