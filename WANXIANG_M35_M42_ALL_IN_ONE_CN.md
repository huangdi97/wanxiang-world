# WANXIANG M35–M42 ALL-IN-ONE 中文执行包


---

<!-- README_FIRST.md -->

# 万相世界 M35–M42 中文全量执行包
本包接续已经完成的 M0–M34。目标不是继续重写底层，而是冻结 v5.2 Kernel v1，把《红楼梦》最小参考实例扩展为 Full Living Red Chamber，再以 Family / Heritage / Campaign 验证同一 Core 的通用性，最后完成 SDK、Package 生态、生产部署和 v5.2 Release Qualification。

使用：
1. 合并到当前万相仓库根目录，不删除现有源码、Git、迁移、tests、reports。
2. 以 `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md` 为设计 Source of Truth。
3. 新开 Codex 对话，复制 `CODEX_COPY_PASTE_M35_M42_CN.txt`。
4. 从 G38A 连续执行到 G45H；每个 Goal PASS 后本地 commit，每个 Milestone PASS 后自动继续。
5. 禁止自动 push / force-push / 生产部署 / 擅自进入 v5.3。


---

<!-- 00_PROGRAM_ARCHITECTURE.md -->

# M35–M42 总程序
- **M35**：Post-M34 Independent Audit + Kernel v1 Freeze
- **M36**：Full Red Chamber Source Corpus + Canon Graph
- **M37**：Full Red Chamber Semantic World
- **M38**：Full Living Runtime + Long-Horizon
- **M39**：Full Studio + Experience
- **M40**：Scaling + Evolution + Derived Worlds
- **M41**：Cross-Domain Generality（Family / Heritage / Campaign）
- **M42**：SDK / Package Ecosystem / Production Release / Final Certification

最终系统继续保持：
`Wanxiang Kernel → Wanxiang Runtime → Wanxiang Forge → Experiences`
具体世界只存在于 Domain/World/Scenario/Experience Package。


---

<!-- 01_KERNEL_FREEZE_POLICY.md -->

# Kernel v1 冻结政策
M35 PASS 后，以下视为 Stable Kernel v1：Reality Root、Identity、Fact、Event、Constraint、State/Ontology/Law Commit、Commit Boundary、World Ledger、Snapshot/Replay、Branch/Worldline 隔离、Lineage Identity、Evidence/Provenance 引用契约、Stable World ABI。

M36–M42 默认禁止：
- 为《红楼梦》、Family、Heritage、Campaign 添加 Kernel 专名/特判；
- 创建第二套 Canonical State / Commit Authority / Event Store / Branch-Worldline 系统；
- 把 Domain 规则下沉到 Reality Root；
- 因一个世界的需求扩大 Stable ABI。

只有“至少两个无关领域均无法表达 + Domain/Provider/Package 无法解决 + 有失败测试 + 有兼容方案 + 重跑 M34 金样通过”时，才允许正式 Kernel Change Proposal。


---

<!-- 02_CODEX_MASTER_PROMPT.md -->

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


---

<!-- 03_FULL_RED_CHAMBER_ACCEPTANCE.md -->

# Full Living Red Chamber 完成定义
## Source / Canon
必须有合法可追溯完整底本、Chapter/Segment/Scene locator、Source→Claim→Evidence、PastCanon/CharacterCanon/FutureCanon、冲突/版本保留、Completion E0–E5。

## Semantic World
主要人物/别名/人生阶段、家族/主仆/组织/角色、地点/路径/访问、物品/信件/礼物/药物/服饰、关系/秘密/知识边界、事件/时间线/日程、Norm/Duty/Permission/Sanction/Reputation、Skill/Action/Affordance、Canon constraints/attractors/completion。

“完整”按可运行语义覆盖和证据覆盖验收，不要求逐句强行结构化。

## Runtime
Core actor / active actor / duty NPC / background population 四级分辨率；支持升降格并保持 Identity/关键历史。无 LLM 模式可跑。用户离开后按 PAUSED/BACKGROUND/FULL_AUTONOMY 运行。

## 长程
继承 M34 7-day；新增 30-day long run、1-year accelerated run、worldline compare、长期 Distillation、Promotion Candidate、Derived World Definition。

## 产品
Studio：Source→Distill→Review→World/Scenario→Run→Debug→Publish。
Experience：选世界/Scenario→进入→观察/行动/接管→离开→世界继续→返回→Fork/Compare。


---

<!-- 04_CROSS_DOMAIN_AND_RELEASE_STANDARD.md -->

# Cross-Domain / Ecosystem / Release 标准
## Family
GEDCOM/GEDZIP、冲突 Claim、Kinship/LifeEvent/Place/Source、Privacy/Consent、Living/Deceased Persona、Family Object Biography。

## Heritage
IIIF、Linked Art/CIDOC selected profile、Physical Object/Digital Surrogate/Semantic Twin/Reconstruction、Provenance、Conservation、Object Biography、3D Asset 只作为 Projection。

## Campaign
Command/Logistics/Movement/Resources/Fog-of-War、Orders/Receipt Time、SimulationAdapter、ValidityEnvelope、Batch Experiment。

三领域都必须复用同一 Identity/Fact/Event/Commit/Ledger/Branch/Source/Package/Host/Projection；若需要 Kernel 特判则 M41 FAIL。

## Ecosystem
第三方只能使用 public SDK/CLI 完成 create→validate→test→certify→build→install→instantiate→run，不允许 import internals。

## Release
fresh clone、SQLite、本地文件、PostgreSQL、对象存储 adapter、migration、backup/restore、observability、security/rights、SDK 文档、RedChamber 用户/作者/运维文档、benchmark、release readiness。


---

<!-- 05_GOALS_INDEX.md -->

# M35–M42 Goal 总索引

## M35
- **G38A** — 独立复核 M34 — `goals/G38A_独立复核_M34.md`
- **G38B** — Kernel v1 ABI 清单 — `goals/G38B_Kernel_v1_ABI_清单.md`
- **G38C** — Kernel Change Guard — `goals/G38C_Kernel_Change_Guard.md`
- **G38D** — Full Red Chamber Gap Audit — `goals/G38D_Full_Red_Chamber_Gap_Audit.md`
- **G38E** — 代码最小性清理 — `goals/G38E_代码最小性清理.md`
- **G38F** — 大 Corpus 流水线容量基线 — `goals/G38F_大_Corpus_流水线容量基线.md`
- **G38G** — API/DB/Package/性能基线冻结 — `goals/G38G_API_DB_Package_性能基线冻结.md`
- **G38H** — M35 资格验收 — `goals/G38H_M35_资格验收.md`

## M36
- **G39A** — 完整底本 Source Gate — `goals/G39A_完整底本_Source_Gate.md`
- **G39B** — 章节/段落稳定定位器 — `goals/G39B_章节_段落稳定定位器.md`
- **G39C** — Scene Boundary 与场景候选 — `goals/G39C_Scene_Boundary_与场景候选.md`
- **G39D** — 全人物 Identity/Alias/Role Graph — `goals/G39D_全人物_Identity_Alias_Role_Graph.md`
- **G39E** — 地点/物品/组织 Source Graph — `goals/G39E_地点_物品_组织_Source_Graph.md`
- **G39F** — Event/Timeline/Relation Graph — `goals/G39F_Event_Timeline_Relation_Graph.md`
- **G39G** — Canon Graph / Edition Conflict — `goals/G39G_Canon_Graph_Edition_Conflict.md`
- **G39H** — M36 Full Corpus Qualification — `goals/G39H_M36_Full_Corpus_Qualification.md`

## M37
- **G40A** — Full World Definition — `goals/G40A_Full_World_Definition.md`
- **G40B** — Household Society Domain 深化 — `goals/G40B_Household_Society_Domain_深化.md`
- **G40C** — Historical China + Narrative Domain 深化 — `goals/G40C_Historical_China_Narrative_Domain_深化.md`
- **G40D** — 全人物 Character Package — `goals/G40D_全人物_Character_Package.md`
- **G40E** — 完整 Spatial World — `goals/G40E_完整_Spatial_World.md`
- **G40F** — 物质/书信/礼物/药物绑定 — `goals/G40F_物质_书信_礼物_药物绑定.md`
- **G40G** — Schedule/Body/Social Life + Completion — `goals/G40G_Schedule_Body_Social_Life_Completion.md`
- **G40H** — M37 Semantic World Qualification — `goals/G40H_M37_Semantic_World_Qualification.md`

## M38
- **G41A** — 多 Scenario 实例化 — `goals/G41A_多_Scenario_实例化.md`
- **G41B** — Population Resolution — `goals/G41B_Population_Resolution.md`
- **G41C** — Autonomous World Loop — `goals/G41C_Autonomous_World_Loop.md`
- **G41D** — 大规模认知/消息传播 — `goals/G41D_大规模认知_消息传播.md`
- **G41E** — 长期 Persona/Capability/Relation 演化 — `goals/G41E_长期_Persona_Capability_Relation_演化.md`
- **G41F** — 社会/制度演化 — `goals/G41F_社会_制度演化.md`
- **G41G** — 30 日 + 1 年加速长稳 — `goals/G41G_30_日_1_年加速长稳.md`
- **G41H** — M38 Living World Qualification — `goals/G41H_M38_Living_World_Qualification.md`

## M39
- **G42A** — Studio Source/Corpus/Candidate Review — `goals/G42A_Studio_Source_Corpus_Candidate_Review.md`
- **G42B** — Studio Character/Relation/Canon Workspace — `goals/G42B_Studio_Character_Relation_Canon_Workspace.md`
- **G42C** — Studio Spatial/Schedule/Institution Workspace — `goals/G42C_Studio_Spatial_Schedule_Institution_Workspace.md`
- **G42D** — Experience 世界/Scenario/角色入口 — `goals/G42D_Experience_世界_Scenario_角色入口.md`
- **G42E** — Experience 2D Living World — `goals/G42E_Experience_2D_Living_World.md`
- **G42F** — Embodiment Leave/Return + Branch Compare — `goals/G42F_Embodiment_Leave_Return_Branch_Compare.md`
- **G42G** — M39 Product Qualification — `goals/G42G_M39_Product_Qualification.md`

## M40
- **G43A** — 长期 Distillation — `goals/G43A_长期_Distillation.md`
- **G43B** — Habit/Norm/Culture/Institution Candidate — `goals/G43B_Habit_Norm_Culture_Institution_Candidate.md`
- **G43C** — Living/Open 长期社会与人物演化 — `goals/G43C_Living_Open_长期社会与人物演化.md`
- **G43D** — Worldline Promotion Candidate — `goals/G43D_Worldline_Promotion_Candidate.md`
- **G43E** — Derived Red Chamber World — `goals/G43E_Derived_Red_Chamber_World.md`
- **G43F** — 100/1000/聚合人口 Benchmark — `goals/G43F_100_1000_聚合人口_Benchmark.md`
- **G43G** — M40 Long-Horizon Qualification — `goals/G43G_M40_Long-Horizon_Qualification.md`

## M41
- **G44A** — Generality Harness + Kernel Lock — `goals/G44A_Generality_Harness_Kernel_Lock.md`
- **G44B** — Family World Qualification — `goals/G44B_Family_World_Qualification.md`
- **G44C** — Heritage World Qualification — `goals/G44C_Heritage_World_Qualification.md`
- **G44D** — Campaign World Qualification — `goals/G44D_Campaign_World_Qualification.md`
- **G44E** — 四领域同 Core 对照 — `goals/G44E_四领域同_Core_对照.md`
- **G44F** — 第三方黑盒 World Pack — `goals/G44F_第三方黑盒_World_Pack.md`
- **G44G** — M41 Generality Qualification — `goals/G44G_M41_Generality_Qualification.md`

## M42
- **G45A** — Public SDK / Package API Freeze — `goals/G45A_Public_SDK_Package_API_Freeze.md`
- **G45B** — CLI / Scaffolder / Certification — `goals/G45B_CLI_Scaffolder_Certification.md`
- **G45C** — Package Install/Upgrade/Migration — `goals/G45C_Package_Install_Upgrade_Migration.md`
- **G45D** — Full Red Chamber Release Bundle — `goals/G45D_Full_Red_Chamber_Release_Bundle.md`
- **G45E** — 生产部署/备份/恢复/观测 — `goals/G45E_生产部署_备份_恢复_观测.md`
- **G45F** — Security/Rights/Supply Chain Final — `goals/G45F_Security_Rights_Supply_Chain_Final.md`
- **G45G** — Release 长稳/容量/文档 — `goals/G45G_Release_长稳_容量_文档.md`
- **G45H** — v5.2 Production Final Certification — `goals/G45H_v5_2_Production_Final_Certification.md`


---

<!-- 06_MILESTONE_GATES.md -->

# M35–M42 Milestone Gates

- **M35** — Post-M34 Audit & Kernel Freeze — `milestones/M35_QUALIFICATION.md`
- **M36** — Full Corpus & Canon Graph — `milestones/M36_QUALIFICATION.md`
- **M37** — Full Semantic World — `milestones/M37_QUALIFICATION.md`
- **M38** — Full Living Runtime — `milestones/M38_QUALIFICATION.md`
- **M39** — Studio & Experience — `milestones/M39_QUALIFICATION.md`
- **M40** — Long-Horizon & Derived Worlds — `milestones/M40_QUALIFICATION.md`
- **M41** — Cross-Domain Generality — `milestones/M41_QUALIFICATION.md`
- **M42** — Production Release — `milestones/M42_QUALIFICATION.md`


---

<!-- 07_RESUME_PROTOCOL.md -->

# 连续执行与恢复协议
中断/压缩/重启后按顺序读取：
1. STATUS.md
2. PLAN.md
3. reports/M35_M42_ACCEPTANCE_MATRIX.md
4. 最近 Milestone qualification
5. 最近 Goal report
6. git status
7. git log --oneline --decorate -30
8. 当前 Goal 文件
9. 当前 failing tests / blockers

从最早 ACTIVE/FAIL Goal 恢复。先跑最窄 regression，再继续。不得凭聊天记忆重新规划，不重做已有可复现 PASS。


---

<!-- 08_FINAL_EVIDENCE_STANDARD.md -->

# M42 最终证据标准
最终至少需要：
- reports/M35_BASELINE_INDEPENDENT_AUDIT.md
- reports/FULL_RED_CHAMBER_GAP_MATRIX.md
- reports/RED_CHAMBER_FULL_SOURCE_GATE.md
- reports/M36_FULL_CORPUS_QUALIFICATION.md
- reports/FULL_RED_CHAMBER_SEMANTIC_COVERAGE.md
- reports/FULL_RED_CHAMBER_30_DAY_STABILITY.md
- reports/FULL_RED_CHAMBER_1_YEAR_ACCELERATED.md
- reports/RED_CHAMBER_PRODUCT_E2E.md
- reports/RED_CHAMBER_DERIVED_WORLD_ACCEPTANCE.md
- reports/CROSS_DOMAIN_GENERALITY_MATRIX.md
- reports/EXTERNAL_PACKAGE_AUTHOR_TEST.md
- reports/PACKAGE_ECOSYSTEM_ACCEPTANCE.md
- reports/PRODUCTION_DEPLOYMENT_QUALIFICATION.md
- reports/FINAL_SECURITY_RIGHTS_REPORT.md
- reports/FINAL_PERFORMANCE_CAPACITY_REPORT.md
- reports/M35_M42_ACCEPTANCE_MATRIX.md
- reports/M42_FINAL_CERTIFICATION.md
- docs/RELEASE_READINESS_V5_2.md

M42 PASS：Kernel freeze、Full Source/Canon、Full Semantic World、30-day + 1-year、Studio→Experience、Derived World、Family/Heritage/Campaign、external pack、package lifecycle、clean deployment、security/rights、final docs 全部通过。若完整红楼梦来源/授权客观不可得，不得声称 FULL_RED_CHAMBER_COMPLETE。


---

<!-- goals/G38A_独立复核_M34.md -->

# G38A — 独立复核 M34
> Milestone：**M35**

## 目标
重新验证 v5.2 与 RedChamber Reference 的真实完成状态。

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
1. 读取 M34/v5.2 final reports 与 Git。
2. 重跑 Commit/Replay/Branch/Lineage/Promotion/7-day。
3. 冻结 Event/Snapshot/WorldPack/API/DB 金样。

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
- M34 金样 hash 一致
- 无未解释 P0/P1
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38a: 独立复核 M34`，然后自动继续。


---

<!-- goals/G38B_Kernel_v1_ABI_清单.md -->

# G38B — Kernel v1 ABI 清单
> Milestone：**M35**

## 目标
冻结底层稳定契约。

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
1. 枚举 stable types/schemas/versions。
2. 生成 ABI golden fixtures。

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
- ABI fixture roundtrip
- 旧客户端核心 contract 通过
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38b: Kernel v1 ABI 清单`，然后自动继续。


---

<!-- goals/G38C_Kernel_Change_Guard.md -->

# G38C — Kernel Change Guard
> Milestone：**M35**

## 目标
把冻结政策自动化。

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
1. import/path/AST guard。
2. 禁止领域专名进入 Kernel。
3. 禁止新 direct mutation path。

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
- 故意违规能被捕获
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38c: Kernel Change Guard`，然后自动继续。


---

<!-- goals/G38D_Full_Red_Chamber_Gap_Audit.md -->

# G38D — Full Red Chamber Gap Audit
> Milestone：**M35**

## 目标
从完整世界定义反查当前最小切片缺口。

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
1. Corpus/Canon gap。
2. Semantic/Runtime/Product/Long-horizon gap。
3. 形成 owner/acceptance matrix。

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
- 所有 gap 可执行
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38d: Full Red Chamber Gap Audit`，然后自动继续。


---

<!-- goals/G38E_代码最小性清理.md -->

# G38E — 代码最小性清理
> Milestone：**M35**

## 目标
在扩大内容前删掉重复抽象。

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
1. 扫描 Manager/Registry/Engine/State。
2. 删除 dead compatibility path。
3. 合并重复 UI/schema helper。

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
- 全回归
- 抽象数量不无故增加
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38e: 代码最小性清理`，然后自动继续。


---

<!-- goals/G38F_大_Corpus_流水线容量基线.md -->

# G38F — 大 Corpus 流水线容量基线
> Milestone：**M35**

## 目标
证明 Forge 可增量处理全书级数据。

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
1. synthetic large corpus。
2. incremental parse/distill/cache/resume。
3. profile memory/disk。

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
- 不整本一次加载
- 局部重跑稳定
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38f: 大 Corpus 流水线容量基线`，然后自动继续。


---

<!-- goals/G38G_API_DB_Package_性能基线冻结.md -->

# G38G — API/DB/Package/性能基线冻结
> Milestone：**M35**

## 目标
为后续变化建立可比基线。

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
1. OpenAPI snapshot。
2. migration head。
3. package goldens。
4. performance benchmark。

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
- diff 可自动检测
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38g: API/DB/Package/性能基线冻结`，然后自动继续。


---

<!-- goals/G38H_M35_资格验收.md -->

# G38H — M35 资格验收
> Milestone：**M35**

## 目标
正式冻结 Kernel v1。

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
1. 运行 M35 Gate。
2. 生成 baseline/freeze report。

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
- M35 全 PASS
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G38H_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g38h: M35 资格验收`，然后自动继续。


---

<!-- goals/G39A_完整底本_Source_Gate.md -->

# G39A — 完整底本 Source Gate
> Milestone：**M36**

## 目标
登记合法、可追溯的完整《红楼梦》底本。

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
1. 复用/升级 M32 source。
2. 完整 checksum/edition/rights/chapter inventory。

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
- Source Gate PASS
- 无模型记忆替代
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39a: 完整底本 Source Gate`，然后自动继续。


---

<!-- goals/G39B_章节_段落稳定定位器.md -->

# G39B — 章节/段落稳定定位器
> Milestone：**M36**

## 目标
建立可重复 chapter/segment IDs。

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
1. parse chapters。
2. stable locator/offset。
3. incremental resume。

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
- 重复解析 ID 稳定
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39b: 章节/段落稳定定位器`，然后自动继续。


---

<!-- goals/G39C_Scene_Boundary_与场景候选.md -->

# G39C — Scene Boundary 与场景候选
> Milestone：**M36**

## 目标
将章节分解为可审查 Scene Candidate。

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
1. time/place/participant cues。
2. 跨段/跨章 scene policy。

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
- Scene candidate 不自动变 Canon
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39c: Scene Boundary 与场景候选`，然后自动继续。


---

<!-- goals/G39D_全人物_Identity_Alias_Role_Graph.md -->

# G39D — 全人物 Identity/Alias/Role Graph
> Milestone：**M36**

## 目标
编译人物、称谓、社会角色和身份冲突。

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
1. identity distillation。
2. alias evidence。
3. role/life-stage。

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
- 同名不误合并
- 别名可回源
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39d: 全人物 Identity/Alias/Role Graph`，然后自动继续。


---

<!-- goals/G39E_地点_物品_组织_Source_Graph.md -->

# G39E — 地点/物品/组织 Source Graph
> Milestone：**M36**

## 目标
编译空间、物品、组织与证据。

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
1. Place containment/connectivity claims。
2. Item identity/custody。
3. Organization membership。

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
- E0/Completion 分层正确
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39e: 地点/物品/组织 Source Graph`，然后自动继续。


---

<!-- goals/G39F_Event_Timeline_Relation_Graph.md -->

# G39F — Event/Timeline/Relation Graph
> Milestone：**M36**

## 目标
建立全书事件、相对时间和关系图。

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
1. before/after/uncertain。
2. participants/place/evidence。
3. relation valid_time。

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
- 不伪造精确日期
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39f: Event/Timeline/Relation Graph`，然后自动继续。


---

<!-- goals/G39G_Canon_Graph_Edition_Conflict.md -->

# G39G — Canon Graph / Edition Conflict
> Milestone：**M36**

## 目标
完成 Past/Character/Future Canon 与版本冲突。

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
1. canon category。
2. edition views。
3. contradictory claims。

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
- FutureCanon 不进 Actor context
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39g: Canon Graph / Edition Conflict`，然后自动继续。


---

<!-- goals/G39H_M36_Full_Corpus_Qualification.md -->

# G39H — M36 Full Corpus Qualification
> Milestone：**M36**

## 目标
验收完整 Corpus 增量编译和追溯。

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
1. coverage report。
2. source→claim traceability。
3. resume/retry。

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
- 关键 Canon 可追溯
- 无大面积 parser gap
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G39H_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g39h: M36 Full Corpus Qualification`，然后自动继续。


---

<!-- goals/G40A_Full_World_Definition.md -->

# G40A — Full World Definition
> Milestone：**M37**

## 目标
从完整 Corpus 生成正式 WorldPack。

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
1. manifest/deps/constitution/genesis/evolution/source/rights。
2. package build。

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
- validate/export/import
- 无运行状态 dump
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40a: Full World Definition`，然后自动继续。


---

<!-- goals/G40B_Household_Society_Domain_深化.md -->

# G40B — Household Society Domain 深化
> Milestone：**M37**

## 目标
补齐家族、主仆、礼制、职责、权限、声誉、制裁。

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
1. 通用 schemas/rules/resolvers。
2. Duty/Norm/Permission/Reputation。

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
- 无红楼梦专名
- synthetic contract
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40b: Household Society Domain 深化`，然后自动继续。


---

<!-- goals/G40C_Historical_China_Narrative_Domain_深化.md -->

# G40C — Historical China + Narrative Domain 深化
> Milestone：**M37**

## 目标
补齐时代生活机制与叙事辅助。

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
1. 时间/身份/交通/生活规则。
2. secret/scene/arc propose-only。

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
- 可被其他 world 复用
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40c: Historical China + Narrative Domain 深化`，然后自动继续。


---

<!-- goals/G40D_全人物_Character_Package.md -->

# G40D — 全人物 Character Package
> Milestone：**M37**

## 目标
构建动态、证据约束角色。

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
1. Identity/LifeArc/Goals/Relations/Knowledge/Capabilities/Evidence。
2. persona vs state。

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
- 匿名选择
- 知识边界
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40d: 全人物 Character Package`，然后自动继续。


---

<!-- goals/G40E_完整_Spatial_World.md -->

# G40E — 完整 Spatial World
> Milestone：**M37**

## 目标
生成可运行府邸/园林/院落/路径拓扑。

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
1. rooms/portals/routes。
2. visibility/acoustic/access/privacy。

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
- path/access/visibility negative tests
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40e: 完整 Spatial World`，然后自动继续。


---

<!-- goals/G40F_物质_书信_礼物_药物绑定.md -->

# G40F — 物质/书信/礼物/药物绑定
> Milestone：**M37**

## 目标
将叙事物件映射通用 Material Substrate。

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
1. Item/Container/Ownership/Custody/InformationPayload。
2. actions。

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
- 守恒
- 获得不等于阅读
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40f: 物质/书信/礼物/药物绑定`，然后自动继续。


---

<!-- goals/G40G_Schedule_Body_Social_Life_Completion.md -->

# G40G — Schedule/Body/Social Life + Completion
> Milestone：**M37**

## 目标
生成长期生活框架和补全账本。

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
1. daily schedules。
2. body/illness/meal/rest/visit。
3. E0-E5 completion。

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
- 无用户可推进
- E1-E5 不升级 E0
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40g: Schedule/Body/Social Life + Completion`，然后自动继续。


---

<!-- goals/G40H_M37_Semantic_World_Qualification.md -->

# G40H — M37 Semantic World Qualification
> Milestone：**M37**

## 目标
证明 Full World 可安装/实例化且 Kernel 无特判。

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
1. multi-scenario dry-run。
2. Core 专名扫描。

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
- 卸载 RedChamber 后 Kernel tests 通过
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G40H_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g40h: M37 Semantic World Qualification`，然后自动继续。


---

<!-- goals/G41A_多_Scenario_实例化.md -->

# G41A — 多 Scenario 实例化
> Milestone：**M38**

## 目标
从同一 WorldPack 建多个合法起点。

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
1. reference + representative scenarios。
2. 固定 Genesis snapshots。

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
- 共享同一 WorldPack
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41a: 多 Scenario 实例化`，然后自动继续。


---

<!-- goals/G41B_Population_Resolution.md -->

# G41B — Population Resolution
> Milestone：**M38**

## 目标
实现 core/active/duty/background 四级运行。

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
1. promotion/demotion。
2. activation budgets。
3. identity/history preservation。

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
- 焦点升降不丢历史
- 背景不频繁调强模型
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41b: Population Resolution`，然后自动继续。


---

<!-- goals/G41C_Autonomous_World_Loop.md -->

# G41C — Autonomous World Loop
> Milestone：**M38**

## 目标
完整世界在无人输入时持续生活。

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
1. scheduler/events。
2. affected entity activation。
3. deterministic fallback。

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
- 无 LLM 30-day 可跑
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41c: Autonomous World Loop`，然后自动继续。


---

<!-- goals/G41D_大规模认知_消息传播.md -->

# G41D — 大规模认知/消息传播
> Milestone：**M38**

## 目标
验证秘密、传言、书信、误解不会全局同步。

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
1. scoped facts。
2. propagation graph。
3. correction/forgetting。

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
- 跨角色/未来知识不泄漏
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41d: 大规模认知/消息传播`，然后自动继续。


---

<!-- goals/G41E_长期_Persona_Capability_Relation_演化.md -->

# G41E — 长期 Persona/Capability/Relation 演化
> Milestone：**M38**

## 目标
让角色变化来自历史。

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
1. trajectory distillation。
2. CapabilityDelta vs PersonaDelta。
3. relation evolution。

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
- 技能变化不自动改人格
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41e: 长期 Persona/Capability/Relation 演化`，然后自动继续。


---

<!-- goals/G41F_社会_制度演化.md -->

# G41F — 社会/制度演化
> Milestone：**M38**

## 目标
从重复群体模式形成规范/制度候选。

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
1. pattern→norm→institution candidate。
2. LawCommit gate。

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
- 单次事件不创建制度
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41f: 社会/制度演化`，然后自动继续。


---

<!-- goals/G41G_30_日_1_年加速长稳.md -->

# G41G — 30 日 + 1 年加速长稳
> Milestone：**M38**

## 目标
验证长期世界与多分辨率。

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
1. 30-day full run。
2. 1-year accelerated。
3. checkpoint/crash/recovery。

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
- 无 ghost/deadlock/runaway queue
- deterministic reference
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41g: 30 日 + 1 年加速长稳`，然后自动继续。


---

<!-- goals/G41H_M38_Living_World_Qualification.md -->

# G41H — M38 Living World Qualification
> Milestone：**M38**

## 目标
验收 Worldness 与长期连续性。

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
1. 12 类 worldness matrix。
2. long-run report。

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
- 无 P0/P1 worldness gap
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G41H_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g41h: M38 Living World Qualification`，然后自动继续。


---

<!-- goals/G42A_Studio_Source_Corpus_Candidate_Review.md -->

# G42A — Studio Source/Corpus/Candidate Review
> Milestone：**M39**

## 目标
让创作者审查来源、解析、候选和 Completion。

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
1. source browser。
2. locator。
3. candidate approve/reject。
4. conflict/evidence view。

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
- 审批经 backend
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42a: Studio Source/Corpus/Candidate Review`，然后自动继续。


---

<!-- goals/G42B_Studio_Character_Relation_Canon_Workspace.md -->

# G42B — Studio Character/Relation/Canon Workspace
> Milestone：**M39**

## 目标
提供人物/关系/Canon/知识边界编辑审查。

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
1. graph/timeline。
2. evidence drawer。
3. future canon permission。

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
- 无越权
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42b: Studio Character/Relation/Canon Workspace`，然后自动继续。


---

<!-- goals/G42C_Studio_Spatial_Schedule_Institution_Workspace.md -->

# G42C — Studio Spatial/Schedule/Institution Workspace
> Milestone：**M39**

## 目标
编辑空间、日程、角色职责和制度。

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
1. map topology。
2. schedule。
3. norm/duty editor。

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
- 业务规则不复制到前端
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42c: Studio Spatial/Schedule/Institution Workspace`，然后自动继续。


---

<!-- goals/G42D_Experience_世界_Scenario_角色入口.md -->

# G42D — Experience 世界/Scenario/角色入口
> Milestone：**M39**

## 目标
普通用户选择世界、模式、起点和人物。

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
1. catalog。
2. scenario/canon mode。
3. embodiment entry。

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
- rights/access filter
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42d: Experience 世界/Scenario/角色入口`，然后自动继续。


---

<!-- goals/G42E_Experience_2D_Living_World.md -->

# G42E — Experience 2D Living World
> Milestone：**M39**

## 目标
完成 React/Phaser 主体验。

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
1. map/actors/items/actions/dialogue/perception/time。

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
- UI 只读 Projection
- 刷新可恢复
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42e: Experience 2D Living World`，然后自动继续。


---

<!-- goals/G42F_Embodiment_Leave_Return_Branch_Compare.md -->

# G42F — Embodiment Leave/Return + Branch Compare
> Milestone：**M39**

## 目标
完整接管、退出、返回、Fork/Compare。

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
1. lease UX。
2. background policy。
3. return summary。
4. timeline/lineage/canon distance。

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
- Playwright E2E
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42f: Embodiment Leave/Return + Branch Compare`，然后自动继续。


---

<!-- goals/G42G_M39_Product_Qualification.md -->

# G42G — M39 Product Qualification
> Milestone：**M39**

## 目标
完成 Studio→Publish→Experience 黑盒纵切。

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
1. fresh user flow。
2. basic accessibility。

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
- 无 mock-only UI
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G42G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g42g: M39 Product Qualification`，然后自动继续。


---

<!-- goals/G43A_长期_Distillation.md -->

# G43A — 长期 Distillation
> Milestone：**M40**

## 目标
从月/年级历史增量发现稳定模式。

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
1. windowed distill。
2. dedupe/origin/evidence。
3. cost budget。

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
- summary 不直接 Commit
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43a: 长期 Distillation`，然后自动继续。


---

<!-- goals/G43B_Habit_Norm_Culture_Institution_Candidate.md -->

# G43B — Habit/Norm/Culture/Institution Candidate
> Milestone：**M40**

## 目标
实现抽象阶梯 L1-L4。

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
1. multi-window stability。
2. counterfactual checks。
3. approval。

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
- 禁止越级 promotion
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43b: Habit/Norm/Culture/Institution Candidate`，然后自动继续。


---

<!-- goals/G43C_Living_Open_长期社会与人物演化.md -->

# G43C — Living/Open 长期社会与人物演化
> Milestone：**M40**

## 目标
验证组织、制度、人物阶段持续变化。

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
1. new organization/institution。
2. character stage。
3. generated entities 标记。

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
- 不进入 original Canon
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43c: Living/Open 长期社会与人物演化`，然后自动继续。


---

<!-- goals/G43D_Worldline_Promotion_Candidate.md -->

# G43D — Worldline Promotion Candidate
> Milestone：**M40**

## 目标
从稳定 worldline 冻结/蒸馏派生世界候选。

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
1. freeze genesis snapshot。
2. rights/invariant review。
3. package candidate。

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
- 源 worldline hash 不变
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43d: Worldline Promotion Candidate`，然后自动继续。


---

<!-- goals/G43E_Derived_Red_Chamber_World.md -->

# G43E — Derived Red Chamber World
> Milestone：**M40**

## 目标
创建至少一个批准后的可实例化后代世界。

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
1. new Definition ID。
2. lineage edge。
3. inherited history ref。

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
- child 可 instantiate
- parent immutable
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43e: Derived Red Chamber World`，然后自动继续。


---

<!-- goals/G43F_100_1000_聚合人口_Benchmark.md -->

# G43F — 100/1000/聚合人口 Benchmark
> Milestone：**M40**

## 目标
量化 Population Resolution scaling。

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
1. 100 actor。
2. 1000 duty/background mix。
3. aggregate population。

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
- 记录 CPU/memory/tick/model calls
- 不为 benchmark 提前分布式
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G43F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g43f: 100/1000/聚合人口 Benchmark`，然后自动继续。


---

<!-- goals/G43G_M40_Long-Horizon_Qualification.md -->

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


---

<!-- goals/G44A_Generality_Harness_Kernel_Lock.md -->

# G44A — Generality Harness + Kernel Lock
> Milestone：**M41**

## 目标
建立跨领域共用验收并锁 Kernel。

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
1. shared acceptance。
2. kernel diff guard。

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
- 各 domain 可独立运行
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44a: Generality Harness + Kernel Lock`，然后自动继续。


---

<!-- goals/G44B_Family_World_Qualification.md -->

# G44B — Family World Qualification
> Milestone：**M41**

## 目标
验证 GEDCOM/Claim/Privacy/Persona/Living Archive。

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
1. GEDCOM/GEDZIP。
2. conflicting claims。
3. privacy/consent。
4. family object biography。

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
- 不 last-write-wins
- 不改 Kernel
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44b: Family World Qualification`，然后自动继续。


---

<!-- goals/G44C_Heritage_World_Qualification.md -->

# G44C — Heritage World Qualification
> Milestone：**M41**

## 目标
验证 IIIF/Object Twin/Reconstruction/Provenance。

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
1. IIIF。
2. Linked Art/CIDOC mapping。
3. object biography/conservation。
4. 3D asset binding。

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
- 身份层不混淆
- 3D 非真相
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44c: Heritage World Qualification`，然后自动继续。


---

<!-- goals/G44D_Campaign_World_Qualification.md -->

# G44D — Campaign World Qualification
> Milestone：**M41**

## 目标
验证 Command/Logistics/Fog/CoSim。

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
1. orders/receipt times。
2. resources/movement。
3. fog。
4. SimulationAdapter。
5. ValidityEnvelope。

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
- Simulator 无 Commit 权限
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44d: Campaign World Qualification`，然后自动继续。


---

<!-- goals/G44E_四领域同_Core_对照.md -->

# G44E — 四领域同 Core 对照
> Milestone：**M41**

## 目标
形成 RedChamber/Family/Heritage/Campaign 共性矩阵。

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
1. Identity/Fact/Event/Commit/Ledger/Package/Host/Projection compare。

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
- Kernel diff 为空或仅获批 proposal
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44e: 四领域同 Core 对照`，然后自动继续。


---

<!-- goals/G44F_第三方黑盒_World_Pack.md -->

# G44F — 第三方黑盒 World Pack
> Milestone：**M41**

## 目标
模拟外部开发者只用 Public SDK 开发第四个 synthetic world。

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
1. temp dir。
2. no internal import。
3. build/certify/install/run。

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
- black-box PASS
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44f: 第三方黑盒 World Pack`，然后自动继续。


---

<!-- goals/G44G_M41_Generality_Qualification.md -->

# G44G — M41 Generality Qualification
> Milestone：**M41**

## 目标
证明万相不是文学专用引擎。

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
1. 四领域 + external pack gate。

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
- 全部 PASS
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G44G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g44g: M41 Generality Qualification`，然后自动继续。


---

<!-- goals/G45A_Public_SDK_Package_API_Freeze.md -->

# G45A — Public SDK / Package API Freeze
> Milestone：**M42**

## 目标
冻结第三方 World/Domain/Scenario/Experience/Eval Author API。

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
1. public types/versioning/examples。
2. compat policy。

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
- examples 不 import internals
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45A_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45a: Public SDK / Package API Freeze`，然后自动继续。


---

<!-- goals/G45B_CLI_Scaffolder_Certification.md -->

# G45B — CLI / Scaffolder / Certification
> Milestone：**M42**

## 目标
完成 create→validate→test→certify→build→install→run。

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
1. CLI/scaffold。
2. certification gates。

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
- fresh temp black-box
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45B_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45b: CLI / Scaffolder / Certification`，然后自动继续。


---

<!-- goals/G45C_Package_Install_Upgrade_Migration.md -->

# G45C — Package Install/Upgrade/Migration
> Milestone：**M42**

## 目标
完成包生命周期并保持旧世界可 Replay。

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
1. dependency/version pin。
2. upgrade migration。
3. disable/uninstall policy。

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
- 旧 instance history 可 replay
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45C_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45c: Package Install/Upgrade/Migration`，然后自动继续。


---

<!-- goals/G45D_Full_Red_Chamber_Release_Bundle.md -->

# G45D — Full Red Chamber Release Bundle
> Milestone：**M42**

## 目标
生成完整 World/Domain/Experience 发布包。

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
1. hashes/rights/source metadata。
2. scenario catalog。
3. release notes。

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
- fresh install/instantiate/play
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45D_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45d: Full Red Chamber Release Bundle`，然后自动继续。


---

<!-- goals/G45E_生产部署_备份_恢复_观测.md -->

# G45E — 生产部署/备份/恢复/观测
> Milestone：**M42**

## 目标
完成 local/PostgreSQL/private deployment qualification。

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
1. fresh clone。
2. SQLite/PG。
3. object storage adapter。
4. OTel/logs。
5. backup/restore。

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
- clean environment smoke
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45E_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45e: 生产部署/备份/恢复/观测`，然后自动继续。


---

<!-- goals/G45F_Security_Rights_Supply_Chain_Final.md -->

# G45F — Security/Rights/Supply Chain Final
> Milestone：**M42**

## 目标
完成最终安全与权利测试。

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
1. prompt injection。
2. malicious package。
3. RBAC。
4. SBOM/dependency/secret scan。

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
- 无 P0/P1 security
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45F_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45f: Security/Rights/Supply Chain Final`，然后自动继续。


---

<!-- goals/G45G_Release_长稳_容量_文档.md -->

# G45G — Release 长稳/容量/文档
> Milestone：**M42**

## 目标
完成 30+ 日 RC、容量和完整文档。

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
1. 30-day RC。
2. 1000+ cycles。
3. operator/user/author docs。
4. troubleshooting。

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
- 资源增长有界
- 文档命令可运行
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45G_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45g: Release 长稳/容量/文档`，然后自动继续。


---

<!-- goals/G45H_v5_2_Production_Final_Certification.md -->

# G45H — v5.2 Production Final Certification
> Milestone：**M42**

## 目标
Clean-room 黑盒验收并冻结 release。

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
1. clean install。
2. external author。
3. external user。
4. backup restore。
5. 最终 traceability/report/local tag。

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
- M35-M42 全 PASS
- 不自动 push/deploy
- 运行适用 unit/contract/integration/replay/migration/E2E/architecture/lint/type/build。
- 不得存在影响本 Goal 的 placeholder/mock-only production path。
- 生成 `reports/G45H_REPORT.md`，记录 changed files、commands、results、limitations。
- 更新 STATUS/PLAN/CHANGELOG 与 `reports/M35_M42_ACCEPTANCE_MATRIX.md`。
- 只有真实外部授权/数据/硬件/凭证才可 EXTERNAL_BLOCKED。

## Git
PASS 后本地 commit：`g45h: v5.2 Production Final Certification`，然后自动继续。


---

<!-- milestones/M35_QUALIFICATION.md -->

# M35 — Post-M34 Audit & Kernel Freeze Qualification
## 前置 Goal
- G38A PASS — 独立复核 M34
- G38B PASS — Kernel v1 ABI 清单
- G38C PASS — Kernel Change Guard
- G38D PASS — Full Red Chamber Gap Audit
- G38E PASS — 代码最小性清理
- G38F PASS — 大 Corpus 流水线容量基线
- G38G PASS — API/DB/Package/性能基线冻结
- G38H PASS — M35 资格验收

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M35_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。


---

<!-- milestones/M36_QUALIFICATION.md -->

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


---

<!-- milestones/M37_QUALIFICATION.md -->

# M37 — Full Semantic World Qualification
## 前置 Goal
- G40A PASS — Full World Definition
- G40B PASS — Household Society Domain 深化
- G40C PASS — Historical China + Narrative Domain 深化
- G40D PASS — 全人物 Character Package
- G40E PASS — 完整 Spatial World
- G40F PASS — 物质/书信/礼物/药物绑定
- G40G PASS — Schedule/Body/Social Life + Completion
- G40H PASS — M37 Semantic World Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M37_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。


---

<!-- milestones/M38_QUALIFICATION.md -->

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


---

<!-- milestones/M39_QUALIFICATION.md -->

# M39 — Studio & Experience Qualification
## 前置 Goal
- G42A PASS — Studio Source/Corpus/Candidate Review
- G42B PASS — Studio Character/Relation/Canon Workspace
- G42C PASS — Studio Spatial/Schedule/Institution Workspace
- G42D PASS — Experience 世界/Scenario/角色入口
- G42E PASS — Experience 2D Living World
- G42F PASS — Embodiment Leave/Return + Branch Compare
- G42G PASS — M39 Product Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M39_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。


---

<!-- milestones/M40_QUALIFICATION.md -->

# M40 — Long-Horizon & Derived Worlds Qualification
## 前置 Goal
- G43A PASS — 长期 Distillation
- G43B PASS — Habit/Norm/Culture/Institution Candidate
- G43C PASS — Living/Open 长期社会与人物演化
- G43D PASS — Worldline Promotion Candidate
- G43E PASS — Derived Red Chamber World
- G43F PASS — 100/1000/聚合人口 Benchmark
- G43G PASS — M40 Long-Horizon Qualification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M40_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。


---

<!-- milestones/M41_QUALIFICATION.md -->

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


---

<!-- milestones/M42_QUALIFICATION.md -->

# M42 — Production Release Qualification
## 前置 Goal
- G45A PASS — Public SDK / Package API Freeze
- G45B PASS — CLI / Scaffolder / Certification
- G45C PASS — Package Install/Upgrade/Migration
- G45D PASS — Full Red Chamber Release Bundle
- G45E PASS — 生产部署/备份/恢复/观测
- G45F PASS — Security/Rights/Supply Chain Final
- G45G PASS — Release 长稳/容量/文档
- G45H PASS — v5.2 Production Final Certification

## Gate
- 跑本阶段全部 unit/contract/integration/E2E。
- 重跑 M34 Kernel/Replay/Branch/Lineage 金样。
- 跑 architecture conformance、lint、typecheck、build。
- 涉及 schema 时跑 migration/old fixture/backup restore。
- 涉及真实资料时跑 Source/Rights gate。
- 更新 code minimality / Kernel freeze report。
- 生成 `reports/M42_QUALIFICATION.md`。

内部失败必须修复。核心完成项被真实外部条件阻塞时，本 Milestone 不得伪装 PASS。
PASS 后自动继续。
