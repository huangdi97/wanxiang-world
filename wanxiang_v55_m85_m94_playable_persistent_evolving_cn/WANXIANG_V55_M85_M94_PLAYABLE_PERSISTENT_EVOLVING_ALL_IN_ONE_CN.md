# WANXIANG v5.5 M85–M94 ALL-IN-ONE 中文执行包


---

<!-- FILE: README_FIRST.md -->

# Wanxiang v5.5 / M85–M94 — Playable, Persistent, Evolving Living Worlds

本执行包以：

`万相世界_v5.4-STABLE-R2_Playable_Persistent_Evolving_Living_World_OS_完整母版_2026-08-26.md`

为当前设计 Source of Truth。

## v5.4 已完成的前置事实

本轮不得重复证明以下能力：

- Reality Root / Commit / Ledger / Replay / Branch / Worldline / Lineage；
- Source Registry / Parse / Segment / Locator；
- Semantic Distillation / Candidate / Evidence / Rights / Completion；
- WorldDraft / WorldPackage / Preview / Worldness / Living Instance；
- CLI / API / Studio 的 Source → Living World；
- 两本真实中文长书（TXT + EPUB）泛化；
- 公共历史 GEDCOM Family E2E + GEDCOM 7 smoke；
- Structured / Mixed Source；
- v5.4.0 Stable / GitHub Release / clean-clone / required CI。

## 本轮唯一核心命题

> **万相已经能“造世界”；v5.5 必须证明：世界能够被普通用户直接进入和游玩，能够长期持续运行，Actor/关系/组织能够在约束下演化，世界能够产生可审查的 Emergence，并能通过 World Lab 进行复验、分叉、干预和比较。**

## 双主线

### Track A — Playable Living World

- Experience Shell；
- PlayableWorldProfile；
- World Plaza / Continue / My Worlds / My Characters；
- Character Creation / Embodiment；
- Free Action；
- StateDiff；
- ActorGoalStack / EpistemicMemory；
- Workshop / Prompt Genesis / Hybrid Genesis；
- Publishing / Marketplace；
- Pressure / Opportunity / Director Modes。

### Track B — Persistent & Evolving World

- Long-Horizon Runtime；
- SimulationLOD；
- Actor / Belief / Relationship / Organization Evolution；
- Emergence / Institution / Culture Candidates；
- Capability Growth；
- WorldRunArtifact / Experiment Registry；
- fork/replay/intervention/batch worldline；
- Physical / Visual Provider Bridge；
- 30/90-day real certification。

## 不训练模型

本轮不训练 Wanxiang 自有模型。LLM、Local Model、Agent Harness、Simulation、Renderer、Visual World Model 都仍然是 Provider。


---

<!-- FILE: 00_MASTER_ROADMAP.md -->

# v5.5 M85–M94 Master Roadmap

## M85 — Playable World Experience Shell
把 v5.4 的 WorldPackage / Living Instance 变成普通用户可以“选世界 → 选角色/创建角色 → 进入 → 自由行动 → 看见后果”的产品。

## M86 — Character / Goal / Memory / StateDiff
建立长期人物连续性：ActorGoalStack、EpistemicMemory、Belief revision、Goal reprioritization、Relationship state 与 Character Passport。

## M87 — World Workshop + Prompt Genesis + Publishing
把 Studio 从 Source Importer 扩展为 World Creator：From Source / From Prompt / Hybrid，保持 E0–E5、Rights、Provenance；支持 ExperiencePackage 与发布边界。

## M88 — World Pressure / Opportunity / Director Modes
建立 PressureProfile、Opportunity/Challenge 和 CANON / DIRECTED / LIVING / EXPERIMENT 模式；Director 只能提出 Proposal，不拥有 Commit 权。

## M89 — Long-Horizon Runtime + SimulationLOD
让世界真正跑 24h / 7d / 30d / 90d，并支持 selected 1-year accelerated；解决 scheduler、background simulation、checkpoint、compaction、recovery、LOD 和成本预算。

## M90 — Actor / Relationship / Organization Evolution
把 State / Belief / Relationship / Capability / Persona / Organization 变化分离，形成可追溯、可解释、可回滚的长期演化。

## M91 — Emergence / Institution / Culture
把 Event → Pattern → Habit → Norm → Institution → World Structure 变成 evidence-backed Candidate / Promotion 管线，而不是自动宣布“涌现”。

## M92 — World Laboratory
提供 WorldRunArtifact、Experiment Registry、fork/replay/intervention、batch worldlines、multi-provider/mixed-population 比较和 ValidationProfile。

## M93 — Physical / Visual World Provider Bridge
实现外部物理/视觉世界 ABI；Semantic Canonical Reality 与视觉/物理 rollout 严格分离；至少有可测试 reference provider，不以外部大模型为 CI 硬依赖。

## M94 — v5.5 Certification
真实产品 + 长周期 + Evolution/Emergence + Lab + clean-room/CI。只有全部关键 Gate 通过才允许发布 `v5.5.0-rc1`，否则保持 NOT_ACCEPTED。


---

<!-- FILE: 01_ARCHITECTURE_CONTRACTS.md -->

# v5.5 Architecture Contracts

## 1. Experience Shell

```text
WorldPackage
+ Scenario
+ RuntimeProfile
+ ExperiencePackage
+ ProjectionProfile
→ PlayableWorldProfile
```

Experience Shell 负责产品入口，不拥有 Canonical Reality。

## 2. Free Action

```text
Player Text / UI Action
→ IntentCompiler
→ ActionProposal
→ Validator
→ Resolver / Simulator
→ ProposedDelta
→ CommitAuthority
→ CommittedDelta
→ StateDiff
→ Narrative / Visual Projection
```

禁止 Narrative Generator 直接写状态。

## 3. ActorGoalStack

```text
LifeMotive
→ LongTermGoal
→ MediumPlan
→ ShortTermGoal
→ CurrentIntent
→ ActionProposal
```

所有 Goal / Plan 都属于 Actor cognition，不等于 World Truth。

## 4. EpistemicMemory

```text
World Truth
→ Perception
→ EpisodicMemory
→ Belief
→ Reflection
→ Goal / Plan
```

必须保持：Memory ≠ Belief ≠ World Truth。

## 5. PressureProfile

属于 Scenario/Domain/Experience：
- resource scarcity
- competing goals
- private information
- duties / obligations
- authority
- rewards / sanctions
- reputation
- time pressure
- environmental risk
- social norms

不得进入 Kernel。

## 6. Director Modes

- CANON：尽量维持 source/canon attractor；
- DIRECTED：允许 Director 提议叙事机会/挑战；
- LIVING：Director 只提供环境机会，不控制人物选择；
- EXPERIMENT：显式 Intervention，必须进入实验日志。

Director 永远无 Commit Authority。

## 7. SimulationLOD

- L0 Focal Actor：完整 cognition / provider；
- L1 Active Actor：简化 reasoning；
- L2 Background Actor：policy + memory summary；
- L3 Cohort：aggregate simulation；
- L4 Population：flow/statistical model。

状态仍由 World 拥有，Agent worker 尽量 stateless。

## 8. WorldRunArtifact

一次运行至少记录：
- WorldPackage/Domain/Scenario/Constitution versions；
- seed / RuntimeProfile / Provider versions；
- Runtime Control Ledger refs；
- commits / snapshots / branch graph；
- actor trajectories；
- interventions；
- Worldness / ValidationProfile results；
- cost / latency / storage metrics。

## 9. ValidationStack

Worldness ≠ Scientific Validity。

至少区分：
- V0 Structural Validity
- V1 Source Fidelity
- V2 Behavioral Validity
- V3 Mechanism Validity
- V4 Macro Validity
- V5 Long-Horizon Stability
- V6 Counterfactual Validity
- V7 External Calibration（有外部数据时）

## 10. Visual / Physical Provider Boundary

外部 Provider 可输出：
- ObservationCandidate
- PhysicsResolution
- SceneProjection
- PerceptionFrame
- AssetCandidate
- Prediction

不得直接 Commit Canonical Reality。


---

<!-- FILE: 02_PRODUCT_EXPERIENCE_SPEC.md -->

# Playable Product Experience Spec

## 普通用户入口

```text
World Plaza
├─ Continue
├─ Explore Worlds
├─ My Worlds
├─ My Characters
└─ Create World
```

用户不应先看到 Candidate / Coverage / WorldPackage 等工程对象。

## 进入世界

```text
World Card
→ Select Scenario
→ Choose Existing Character / Create Character / Observer
→ Acquire Embodiment or Presence
→ Enter
```

## Play HUD 最低产品面

- 当前时间 / 地点；
- 当前角色；
- 可感知对象/人物；
- 自由行动输入；
- suggested affordances；
- Memory / Goal / Relationship（按权限）；
- StateDiff；
- Timeline / recent events；
- Pause / Continue / Leave；
- Branch / Experiment（有权限时）。

## StateDiff

每个 Commit 后至少可表示：
- actor state changes；
- location changes；
- relation changes；
- item custody/ownership changes；
- task/opportunity changes；
- knowledge/belief changes（按 actor 权限显示）；
- organization/role changes；
- explicit no-change where useful。

StateDiff 从 committed events/projections 计算，不直接信任 LLM 自述。


---

<!-- FILE: 03_LONG_HORIZON_EVOLUTION_SPEC.md -->

# Long-Horizon & Evolution Spec

## 时间跨度

本轮至少建立：
- 24h smoke；
- 7d qualification；
- 30d long-run；
- 90d selected-world certification；
- selected 1-year accelerated research run（若成本/时间允许；不能伪装为 required PASS）。

## 必须解决

- recurring scheduler；
- background simulation；
- sleep/wake/availability；
- actor activation/deactivation；
- checkpoint/resume；
- snapshot/compaction；
- crash recovery；
- deterministic/reproducible reference profile；
- provider budget / token/call/time budgets；
- storage growth；
- memory growth；
- LOD transitions；
- no silent history rewrite。

## Evolution Delta Types

必须分离：
- StateDelta
- BeliefDelta
- RelationshipDelta
- CapabilityDelta
- PersonaDelta
- OrganizationDelta
- InstitutionCandidate
- OntologyCandidate

禁止一个“CharacterEvolutionBlob”吞掉所有变化。

## Emergence Ladder

```text
L0 Event
→ L1 Repeated Pattern
→ L2 Habit / Skill
→ L3 Social Norm
→ L4 Institution
→ L5 World Structure / Ontology
```

每一级都要有 evidence、confidence、window、counterevidence、review/promotion policy。


---

<!-- FILE: 04_WORLD_LAB_SPEC.md -->

# World Laboratory Spec

## 目标

把“世界运行”变成可复验的实验对象。

## ExperimentDefinition

至少：
- experiment_id
- world_package/version
- scenario/version
- seed(s)
- provider matrix
- population policy
- interventions
- run horizon
- metrics
- validation profile
- stop conditions

## 能力

- fork from snapshot/event；
- intervention at explicit time/event；
- replay；
- batch worldlines；
- multi-provider parallel worlds；
- mixed-population worlds；
- compare trajectories；
- compare actor/relationship/institution outcomes；
- cost/latency/storage compare；
- export sanitized RunArtifact。

## 不允许

- 用一次随机 run 宣称科学结论；
- 用 Worldness 代替 ValidationStack；
- 把实验 intervention 静默写回 canonical source world；
- 通过 provider-specific hidden state 破坏 replayability。


---

<!-- FILE: 05_GITHUB_RELEASE_POLICY.md -->

# GitHub / Release Policy

继续现有公开仓库 `wanxiang-world`。

建议 feature branch：
`feature/v5.5-playable-persistent-evolving`

若当前分支上已有合法 v5.5 work，则复用，不制造无意义分支。

每个 Goal PASS 后：
- local commit；
- milestone gate；
- 自动继续。

M94 前：
- secret/private-source scan；
- no copyrighted raw source；
- no private family data；
- full local quality；
- push feature branch；
- required GitHub Actions；
- FAIL → logs → fix → commit → push → rerun；
- remote SHA == local HEAD。

只有 M94 real certification ACCEPTED 才允许：
- annotated tag `v5.5.0-rc1`；
- GitHub prerelease；
- post-release clean-clone verification。

禁止 force push，禁止移动/覆盖 `v5.4.0` stable tag。


---

<!-- FILE: 06_CODEX_MASTER_PROMPT_CN.md -->

# Codex Master Prompt — Wanxiang v5.5 M85–M94

继续当前 `wanxiang-world` 仓库。以 v5.4-STABLE-R2 完整母版为 Source of Truth。

## 任务

从 G88A 连续执行到 G97J，构建：

> **Playable, Persistent, Evolving Living Worlds**

不是重新做 Source→World，不训练模型，不进入 v5.6。

## 先做真实仓库审计

开工前：
- git status / log / remote / tags；
- v5.4.0 release / clean-room evidence；
- 当前 Kernel/Runtime/Forge/Studio/Experience 实现；
- KEEP / EXTEND / MERGE / DELETE / ADD matrix；
- 禁止按 Goal 文档机械新建重复系统。

## 顺序

M85 G88A–G88H
→ M86 G89A–G89H
→ M87 G90A–G90H
→ M88 G91A–G91H
→ M89 G92A–G92H
→ M90 G93A–G93H
→ M91 G94A–G94H
→ M92 G95A–G95H
→ M93 G96A–G96H
→ M94 G97A–G97J

每 Goal：读取真实代码 → 实现 → 测试 → 报告 → commit → 自动继续。
每 Milestone：qualification FAIL 就修，不问用户是否继续。

## 最终真实验收

必须至少证明：

1. Playable product：World Plaza→Character→Enter→Free Action→Committed StateDiff→Leave→Continue；
2. 7d actor continuity；
3. 30d literary long-run；
4. 90d selected-world long-run；
5. Actor/Belief/Relationship/Organization evolution；
6. evidence-backed emergence candidate + false-positive controls；
7. WorldRunArtifact + ExperimentRegistry + 4+ parallel worldlines + intervention + comparison；
8. ValidationStack 不是 Worldness 别名；
9. reference Physical/Visual Provider bridge；
10. clean-clone + GitHub required CI 全绿。

只有以上关键 Gate ACCEPTED 才创建 `v5.5.0-rc1` prerelease。

## 外部能力

如果 Godot/Unreal/SimWorld/Genie-class/外部模型在环境不可用：
- 完成 ABI、reference provider、contract tests、docs；
- 只把具体外部 adapter 真实运行标为 EXTERNAL_BLOCKED；
- 不得因此阻塞所有内部 M93/M94；
- 不得伪造通过。

## STOP

G97J 后停止。不得自动进入 v5.6、True Genesis、自训练模型或十万 Agent 项目。


---

<!-- FILE: 07_GOALS_INDEX.md -->

# M85–M94 Goal Index

## M85
- **G88A** — v5.4 Stable Baseline & v5.5 Branch — `goals/G88A_v5_4_Stable_Baseline_v5_5_Branch.md`
- **G88B** — PlayableWorldProfile v1 — `goals/G88B_PlayableWorldProfile_v1.md`
- **G88C** — ExperiencePackage v1 — `goals/G88C_ExperiencePackage_v1.md`
- **G88D** — World Plaza / My Worlds / Continue — `goals/G88D_World_Plaza_My_Worlds_Continue.md`
- **G88E** — My Characters / Character Entry — `goals/G88E_My_Characters_Character_Entry.md`
- **G88F** — Free Action Intent Compiler — `goals/G88F_Free_Action_Intent_Compiler.md`
- **G88G** — Committed StateDiff v1 — `goals/G88G_Committed_StateDiff_v1.md`
- **G88H** — M85 Playable E2E Qualification — `goals/G88H_M85_Playable_E2E_Qualification.md`

## M86
- **G89A** — ActorGoalStack v1 — `goals/G89A_ActorGoalStack_v1.md`
- **G89B** — Goal Reprioritization — `goals/G89B_Goal_Reprioritization.md`
- **G89C** — EpistemicMemory v1 — `goals/G89C_EpistemicMemory_v1.md`
- **G89D** — Belief Revision — `goals/G89D_Belief_Revision.md`
- **G89E** — RelationshipState v1 — `goals/G89E_RelationshipState_v1.md`
- **G89F** — Character Passport — `goals/G89F_Character_Passport.md`
- **G89G** — Actor Continuity Projection — `goals/G89G_Actor_Continuity_Projection.md`
- **G89H** — M86 Character Continuity Qualification — `goals/G89H_M86_Character_Continuity_Qualification.md`

## M87
- **G90A** — Workshop Information Architecture — `goals/G90A_Workshop_Information_Architecture.md`
- **G90B** — Prompt Genesis Contract — `goals/G90B_Prompt_Genesis_Contract.md`
- **G90C** — Prompt Genesis Provider — `goals/G90C_Prompt_Genesis_Provider.md`
- **G90D** — Hybrid Genesis — `goals/G90D_Hybrid_Genesis.md`
- **G90E** — Scenario / Experience Editor — `goals/G90E_Scenario_Experience_Editor.md`
- **G90F** — Publishing Profiles — `goals/G90F_Publishing_Profiles.md`
- **G90G** — World Registry / Marketplace Baseline — `goals/G90G_World_Registry_Marketplace_Baseline.md`
- **G90H** — M87 Workshop Qualification — `goals/G90H_M87_Workshop_Qualification.md`

## M88
- **G91A** — PressureProfile v1 — `goals/G91A_PressureProfile_v1.md`
- **G91B** — Opportunity / Challenge — `goals/G91B_Opportunity_Challenge.md`
- **G91C** — DirectorPolicy Modes — `goals/G91C_DirectorPolicy_Modes.md`
- **G91D** — Canon Attractor Policy — `goals/G91D_Canon_Attractor_Policy.md`
- **G91E** — Experiment Intervention — `goals/G91E_Experiment_Intervention.md`
- **G91F** — Quest Projection Adapter — `goals/G91F_Quest_Projection_Adapter.md`
- **G91G** — Pressure Behavior Benchmark — `goals/G91G_Pressure_Behavior_Benchmark.md`
- **G91H** — M88 Director/Pressure Qualification — `goals/G91H_M88_Director_Pressure_Qualification.md`

## M89
- **G92A** — Long-Horizon Scheduler — `goals/G92A_Long-Horizon_Scheduler.md`
- **G92B** — Background Simulation — `goals/G92B_Background_Simulation.md`
- **G92C** — Checkpoint / Resume / Crash Recovery — `goals/G92C_Checkpoint_Resume_Crash_Recovery.md`
- **G92D** — Snapshot / Compaction Policy — `goals/G92D_Snapshot_Compaction_Policy.md`
- **G92E** — SimulationLOD Runtime — `goals/G92E_SimulationLOD_Runtime.md`
- **G92F** — Resource / Cost Budget — `goals/G92F_Resource_Cost_Budget.md`
- **G92G** — 24h / 7d Long Run — `goals/G92G_24h_7d_Long_Run.md`
- **G92H** — 30d Qualification — `goals/G92H_30d_Qualification.md`

## M90
- **G93A** — Evolution Delta Taxonomy — `goals/G93A_Evolution_Delta_Taxonomy.md`
- **G93B** — Capability Growth — `goals/G93B_Capability_Growth.md`
- **G93C** — Persona Adaptation — `goals/G93C_Persona_Adaptation.md`
- **G93D** — Relationship Evolution — `goals/G93D_Relationship_Evolution.md`
- **G93E** — Organization Lifecycle — `goals/G93E_Organization_Lifecycle.md`
- **G93F** — Reputation / Social Role — `goals/G93F_Reputation_Social_Role.md`
- **G93G** — Evolution Explainability — `goals/G93G_Evolution_Explainability.md`
- **G93H** — M90 30d Evolution Qualification — `goals/G93H_M90_30d_Evolution_Qualification.md`

## M91
- **G94A** — Pattern Observation Store — `goals/G94A_Pattern_Observation_Store.md`
- **G94B** — Repeated Pattern Detector — `goals/G94B_Repeated_Pattern_Detector.md`
- **G94C** — Habit / Skill Candidate — `goals/G94C_Habit_Skill_Candidate.md`
- **G94D** — Social Norm Candidate — `goals/G94D_Social_Norm_Candidate.md`
- **G94E** — Institution Candidate — `goals/G94E_Institution_Candidate.md`
- **G94F** — Culture / Ontology Candidate — `goals/G94F_Culture_Ontology_Candidate.md`
- **G94G** — Promotion Ladder Enforcement — `goals/G94G_Promotion_Ladder_Enforcement.md`
- **G94H** — M91 Emergence Qualification — `goals/G94H_M91_Emergence_Qualification.md`

## M92
- **G95A** — WorldRunArtifact v1 — `goals/G95A_WorldRunArtifact_v1.md`
- **G95B** — Experiment Registry — `goals/G95B_Experiment_Registry.md`
- **G95C** — Fork / Intervention Runner — `goals/G95C_Fork_Intervention_Runner.md`
- **G95D** — Batch Worldlines — `goals/G95D_Batch_Worldlines.md`
- **G95E** — Multi-provider / Mixed-population — `goals/G95E_Multi-provider_Mixed-population.md`
- **G95F** — Worldline Comparator — `goals/G95F_Worldline_Comparator.md`
- **G95G** — ValidationProfile v1 — `goals/G95G_ValidationProfile_v1.md`
- **G95H** — M92 Lab Qualification — `goals/G95H_M92_Lab_Qualification.md`

## M93
- **G96A** — PhysicalWorldProvider ABI — `goals/G96A_PhysicalWorldProvider_ABI.md`
- **G96B** — VisualWorldProvider ABI — `goals/G96B_VisualWorldProvider_ABI.md`
- **G96C** — Multi-perspective Projection — `goals/G96C_Multi-perspective_Projection.md`
- **G96D** — Reference Physical Provider — `goals/G96D_Reference_Physical_Provider.md`
- **G96E** — Reference Visual Projection Provider — `goals/G96E_Reference_Visual_Projection_Provider.md`
- **G96F** — External Engine Adapter Audit — `goals/G96F_External_Engine_Adapter_Audit.md`
- **G96G** — Projection/Reality Consistency — `goals/G96G_Projection_Reality_Consistency.md`
- **G96H** — M93 Provider Bridge Qualification — `goals/G96H_M93_Provider_Bridge_Qualification.md`

## M94
- **G97A** — Certification Matrix Freeze — `goals/G97A_Certification_Matrix_Freeze.md`
- **G97B** — Literary 30d/90d Certification — `goals/G97B_Literary_30d_90d_Certification.md`
- **G97C** — Non-literary Long-run Certification — `goals/G97C_Non-literary_Long-run_Certification.md`
- **G97D** — Parallel Worldline Certification — `goals/G97D_Parallel_Worldline_Certification.md`
- **G97E** — Experience Product E2E — `goals/G97E_Experience_Product_E2E.md`
- **G97F** — Security / Safety / Cost / Storage — `goals/G97F_Security_Safety_Cost_Storage.md`
- **G97G** — Clean Clone + GitHub CI — `goals/G97G_Clean_Clone_GitHub_CI.md`
- **G97H** — v5.5.0-rc1 Release Gate — `goals/G97H_v5_5_0-rc1_Release_Gate.md`
- **G97I** — Final Evidence & Status — `goals/G97I_Final_Evidence_Status.md`
- **G97J** — STOP — `goals/G97J_STOP.md`


---

<!-- FILE: 08_MILESTONE_GATES.md -->

# Milestone Gates

- `M85` — `milestones/M85_QUALIFICATION.md`
- `M86` — `milestones/M86_QUALIFICATION.md`
- `M87` — `milestones/M87_QUALIFICATION.md`
- `M88` — `milestones/M88_QUALIFICATION.md`
- `M89` — `milestones/M89_QUALIFICATION.md`
- `M90` — `milestones/M90_QUALIFICATION.md`
- `M91` — `milestones/M91_QUALIFICATION.md`
- `M92` — `milestones/M92_QUALIFICATION.md`
- `M93` — `milestones/M93_QUALIFICATION.md`
- `M94` — `milestones/M94_QUALIFICATION.md`


---

<!-- FILE: 09_USER_ACTIONS.md -->

# 用户需要做什么

本轮默认可以尽量全自动执行。

## 通常不需要用户提供

- 新的真实书；
- GEDCOM；
- 训练数据；
- 自训练模型；
- 新 GitHub 仓库。

v5.4 已经有真实 Source-created worlds，可以直接作为 v5.5 long-horizon / playable / lab 的验收对象。

## 只有以下情况需要用户介入

1. GitHub/远端再次要求授权；
2. 你明确希望验证某个外部 Godot/Unreal/SimWorld/在线模型 Provider，而环境需要安装或凭证；
3. 需要决定公开世界/UGC 的产品政策或法律条款；
4. 某个真实 Source rights 需要新的用户授权。

否则 Codex 应自动完成到 M94。


---

<!-- FILE: 10_FINAL_ACCEPTANCE.md -->

# v5.5 Final Acceptance — RC1 Hard Gate

只有全部 required 条件满足才允许 `v5.5.0-rc1`：

## Playable
1. PlayableWorldProfile 可由 v5.4 world 构建。
2. World Plaza / Continue / My Worlds / My Characters E2E。
3. Character/Observer/Embodiment 权限正确。
4. Free Action → ActionProposal → Commit 闭环。
5. StateDiff 由 committed state 计算。
6. Leave / Continue 保持同一世界连续性。

## Character Continuity
7. ActorGoalStack 可持久、可回放。
8. Memory / Belief / Truth 分离。
9. Secret / rumor / future knowledge 隔离。
10. RelationshipState 有时间/事件来源。
11. 7-day Actor continuity PASS。

## Workshop
12. From Source regression PASS。
13. From Prompt 产生 E5 Candidate/WorldDraft。
14. Hybrid Genesis 保持 E0–E5 provenance。
15. public/private/unlisted/family-private publish gates 正确。

## Director / Pressure
16. PressureProfile 不进入 Kernel。
17. CANON/DIRECTED/LIVING/EXPERIMENT 模式可运行。
18. Director 无 Commit 权。
19. Opportunity 可被 Actor 忽略。
20. Intervention 只存在于实验 branch/artifact。

## Long Horizon
21. 24h PASS。
22. 7d PASS。
23. 30d literary PASS。
24. 90d selected-world PASS。
25. checkpoint/resume/crash recovery PASS。
26. compaction 后 replay equality。
27. SimulationLOD transition state-continuous。
28. cost/storage/memory growth 有量化报告。

## Evolution
29. State/Belief/Relationship/Capability/Persona/Organization Delta 分离。
30. 30d Actor/Relationship/Organization 非零合理演化。
31. Evolution 可解释并可回放。
32. source/canon definition 未被运行时演化污染。

## Emergence
33. Pattern detector 有 positive + negative benchmark。
34. 至少一个 evidence-backed Habit/Norm/Institution Candidate。
35. 高层晋升有更严格证据/审批。
36. false-positive controls PASS。
37. 不声称 universal emergence。

## World Lab
38. WorldRunArtifact 完整可复验。
39. ExperimentRegistry 可恢复。
40. fork/intervention parent isolation。
41. 至少 4 条 parallel worldlines。
42. multi-provider/policy or mixed-population comparison。
43. WorldlineComparator 输出 trajectory/cost differences。
44. ValidationProfile V0–V7 实现；unknown != pass。

## Provider Bridge
45. Physical Provider ABI contract PASS。
46. Visual Provider ABI contract PASS。
47. reference physical provider E2E。
48. reference visual projection E2E。
49. multi-perspective privacy/knowledge isolation。
50. visual/physical output 不可直接写 reality。

## Product / Release
51. Browser Experience/Studio E2E。
52. security/private source/UGC package scan PASS。
53. v5.4 critical regression PASS。
54. full Python/TS quality PASS。
55. clean-clone PASS。
56. remote SHA == local HEAD。
57. GitHub required Actions success。
58. working tree clean。
59. final evidence 把 IMPLEMENTED / EXPERIMENTAL / RESEARCH_NOT_PROVEN 分开。
60. 仅上述 Gate ACCEPTED 才创建 annotated `v5.5.0-rc1` + GitHub prerelease；否则保持 NOT_ACCEPTED 并 STOP。


---

<!-- FILE: 11_RESUME_PROTOCOL.md -->

# Resume Protocol

上下文压缩/重启后读取：

1. `STATUS.md`
2. `PLAN.md`
3. `reports/V55_ACCEPTANCE_MATRIX.md`
4. 最近 `Mxx_QUALIFICATION.md`
5. 最近 `Gxx_REPORT.md`
6. `git status`
7. `git log --oneline --decorate -40`
8. 当前 Goal 文件
9. failing tests / CI logs

从最早 ACTIVE / FAIL / BLOCKED Goal 恢复。

不要重跑已有可复现 PASS；不要重新设计 v5.5 总架构；不要因为上下文丢失重做 v5.4。


---

<!-- FILE: goals/G88A_v5_4_Stable_Baseline_v5_5_Branch.md -->

# G88A — v5.4 Stable Baseline & v5.5 Branch

Milestone：**M85**

## Objective

建立 v5.5 开工基线，复验 stable tag，冻结 Kernel。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 从 v5.4.0 clean baseline/当前开发分支核对 Git 状态
2. 运行 critical regression 与 architecture guard
3. 创建/切换 feature/v5.5-playable-persistent-evolving
4. 建立 v5.5 STATUS/PLAN/acceptance matrix


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- v5.4 critical regression PASS
- Kernel guard PASS
- working tree clean before feature work

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88a: v5.4 Stable Baseline & v5.5 Branch`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88B_PlayableWorldProfile_v1.md -->

# G88B — PlayableWorldProfile v1

Milestone：**M85**

## Objective

把 Package/Scenario/Runtime/Experience/Projection 收敛成可玩的世界入口。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 定义 schema/version
2. 兼容现有 WorldPackage/Scenario
3. profile validation
4. public/private visibility
5. default scenario/runtime selection


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- schema roundtrip
- invalid refs reject
- backward compatibility

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88b: PlayableWorldProfile v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88C_ExperiencePackage_v1.md -->

# G88C — ExperiencePackage v1

Milestone：**M85**

## Objective

正式建立体验层配置，不污染 World Definition。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 入口/controls/UI capabilities
2. embodiment policy
3. projection profile refs
4. allowed actions
5. state-diff policy
6. visibility


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- package validator
- rights/visibility negative tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88c: ExperiencePackage v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88D_World_Plaza_My_Worlds_Continue.md -->

# G88D — World Plaza / My Worlds / Continue

Milestone：**M85**

## Objective

提供普通用户世界发现与继续入口。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. world cards
2. recent sessions
3. continue last instance
4. private/public filters
5. server-side authorization


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- API contracts
- browser E2E
- unauthorized access negative

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88d: World Plaza / My Worlds / Continue`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88E_My_Characters_Character_Entry.md -->

# G88E — My Characters / Character Entry

Milestone：**M85**

## Objective

提供已有角色、创建角色、Observer/Embodiment 入口。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. character list
2. presence vs embodiment
3. lease acquisition/release
4. compatibility checks


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- double-controller rejection
- resume after leave
- observer cannot mutate

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88e: My Characters / Character Entry`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88F_Free_Action_Intent_Compiler.md -->

# G88F — Free Action Intent Compiler

Milestone：**M85**

## Objective

用户自由文本/结构化动作进入统一 ActionProposal。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. text intent adapter
2. affordance lookup
3. proposal schema
4. ambiguity/clarification result
5. no direct commit


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- malicious prompt/data tests
- unsupported action typed result

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88f: Free Action Intent Compiler`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88G_Committed_StateDiff_v1.md -->

# G88G — Committed StateDiff v1

Milestone：**M85**

## Objective

从 Commit/Event 计算用户可见状态变化。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. location/state/relation/item/task/knowledge/org diff
2. permission filter
3. narrative rendering adapter


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- LLM narrative disagreement cannot alter diff
- replay produces same diff

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88g: Committed StateDiff v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G88H_M85_Playable_E2E_Qualification.md -->

# G88H — M85 Playable E2E Qualification

Milestone：**M85**

## Objective

完成“选世界→角色→进入→自由行动→看到 StateDiff→退出→继续”。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 至少一个 v5.4 source-created world
2. CLI/API/browser shared backend
3. record UX evidence


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- full playable E2E PASS
- no authority bypass

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G88H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g88h: M85 Playable E2E Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89A_ActorGoalStack_v1.md -->

# G89A — ActorGoalStack v1

Milestone：**M86**

## Objective

建立一等长期目标栈。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. LifeMotive/LongTerm/Medium/Short/Intent types
2. priority/dependency/deadline
3. goal provenance
4. goal revision events


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- goal stack serialization
- no goal == world fact

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89a: ActorGoalStack v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89B_Goal_Reprioritization.md -->

# G89B — Goal Reprioritization

Milestone：**M86**

## Objective

事件与 Belief 更新可改变目标优先级，但需策略化和可审计。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. policy interface
2. deterministic reference policy
3. optional provider proposal
4. reason/evidence refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- same seed deterministic reference
- provider cannot commit

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89b: Goal Reprioritization`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89C_EpistemicMemory_v1.md -->

# G89C — EpistemicMemory v1

Milestone：**M86**

## Objective

区分 Observation/EpisodicMemory/Belief/Reflection。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. memory records
2. source perception refs
3. decay/reinforcement hooks
4. belief confidence
5. contradiction


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- secret isolation
- memory != truth tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89c: EpistemicMemory v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89D_Belief_Revision.md -->

# G89D — Belief Revision

Milestone：**M86**

## Objective

新证据可修正、保留或冲突化 Belief。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. support/contradict/refine
2. confidence update
3. unknown state
4. false-belief preservation where valid


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- rumor not truth
- future knowledge leak tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89d: Belief Revision`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89E_RelationshipState_v1.md -->

# G89E — RelationshipState v1

Milestone：**M86**

## Objective

关系从静态 edge 升级为有维度/时间/事件来源的状态。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. trust/affection/hostility/debt/loyalty/dependency/authority/reputation
2. valid_from/to
3. event refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- relation evolution replay
- no global omniscience

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89e: RelationshipState v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89F_Character_Passport.md -->

# G89F — Character Passport

Milestone：**M86**

## Objective

为原创/用户角色提供可携带资料，但跨世界由 translation policy 决定。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. portable identity profile
2. memory/skill/item portability flags
3. origin world refs
4. interworld compatibility


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- cannot silently import impossible skill/item
- privacy

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89f: Character Passport`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89G_Actor_Continuity_Projection.md -->

# G89G — Actor Continuity Projection

Milestone：**M86**

## Objective

前端可查看 Goal/Memory/Belief/Relationship 的权限化时间变化。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. timeline views
2. why-action explanation refs
3. private cognition visibility


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- actor-only vs observer access

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89g: Actor Continuity Projection`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G89H_M86_Character_Continuity_Qualification.md -->

# G89H — M86 Character Continuity Qualification

Milestone：**M86**

## Objective

至少 7 天加速运行，证明 Goal/Memory/Belief/Relationship 持续且 Replay。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. source-created literary world
2. multiple actors
3. leave/re-enter continuity


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- 7-day actor continuity PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G89H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g89h: M86 Character Continuity Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90A_Workshop_Information_Architecture.md -->

# G90A — Workshop Information Architecture

Milestone：**M87**

## Objective

把现有 Studio 组织为 Source/Prompt/Hybrid 三种创建方式。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. Create World home
2. advanced authoring panels
3. shared draft backend
4. no duplicate editors


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- browser E2E
- existing Source import regression

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90a: Workshop Information Architecture`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90B_Prompt_Genesis_Contract.md -->

# G90B — Prompt Genesis Contract

Milestone：**M87**

## Objective

把自然语言创作意图变成 E5 Candidate/WorldDraft，而不是直接 World Truth。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. CreatorIntent
2. constraint extraction
3. domain suggestions
4. E5 provenance
5. review gates


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- prompt injection/data separation
- all generated facts marked E5

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90b: Prompt Genesis Contract`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90C_Prompt_Genesis_Provider.md -->

# G90C — Prompt Genesis Provider

Milestone：**M87**

## Objective

复用现有 provider boundary，生成结构化 candidates。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. local/reference provider path
2. schema constrained output
3. retry/checkpoint
4. no provider commit


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no-key typed provider-required or baseline behavior

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90c: Prompt Genesis Provider`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90D_Hybrid_Genesis.md -->

# G90D — Hybrid Genesis

Milestone：**M87**

## Objective

Source evidence + Prompt intent 在一个 Draft 中融合。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. E0-E5 conflict policy
2. source precedence configurable
3. generated completion traceability


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- generated claim cannot overwrite explicit source silently

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90d: Hybrid Genesis`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90E_Scenario_Experience_Editor.md -->

# G90E — Scenario / Experience Editor

Milestone：**M87**

## Objective

作者可编辑 Scenario/ExperiencePackage/Projection/allowed actions。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. versioned draft edits
2. validation
3. preview without publish


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- revision/concurrency tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90e: Scenario / Experience Editor`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90F_Publishing_Profiles.md -->

# G90F — Publishing Profiles

Milestone：**M87**

## Objective

公开/私有/未列出/家庭私有/研究世界的发布边界。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. visibility
2. rights summary
3. package metadata
4. moderation/safety extension points


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- private world never Plaza
- rights blocked publish

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90f: Publishing Profiles`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90G_World_Registry_Marketplace_Baseline.md -->

# G90G — World Registry / Marketplace Baseline

Milestone：**M87**

## Objective

实现 World Registry 与搜索/分类/版本，而非商业交易系统。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. official/community labels
2. categories/tags
3. version/compatibility
4. install/open


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- package provenance
- untrusted package safety

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90g: World Registry / Marketplace Baseline`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G90H_M87_Workshop_Qualification.md -->

# G90H — M87 Workshop Qualification

Milestone：**M87**

## Objective

From Source / From Prompt / Hybrid 都能生成可 Preview 的 Playable World。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 三条 E2E
2. E5 evidence audit
3. public/private publish checks


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- Workshop E2E PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90h: M87 Workshop Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91A_PressureProfile_v1.md -->

# G91A — PressureProfile v1

Milestone：**M88**

## Objective

把社会压力/资源/风险作为 Scenario/Domain 可组合能力。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. scarcity/goals/private info/obligation/authority/reward/sanction/reputation/time/risk/norm
2. schema/version


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- kernel has no pressure-specific types

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91a: PressureProfile v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91B_Opportunity_Challenge.md -->

# G91B — Opportunity / Challenge

Milestone：**M88**

## Objective

世界可提出机会和挑战，但它们不等于强制剧情。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. opportunity lifecycle
2. eligibility
3. expiry
4. rewards/risks
5. evidence/world state refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- actor may ignore
- no direct goal overwrite

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91b: Opportunity / Challenge`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91C_DirectorPolicy_Modes.md -->

# G91C — DirectorPolicy Modes

Milestone：**M88**

## Objective

实现 CANON/DIRECTED/LIVING/EXPERIMENT 四种策略。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. mode contract
2. allowed proposal types
3. mode transitions
4. audit


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- Director cannot call CommitAuthority directly

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91c: DirectorPolicy Modes`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91D_Canon_Attractor_Policy.md -->

# G91D — Canon Attractor Policy

Milestone：**M88**

## Objective

CANON 模式通过 opportunity/constraint/score 引导，不硬写人物选择。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. canon distance metrics
2. soft/hard constraints
3. branch on major divergence


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- user free will preserved according policy

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91d: Canon Attractor Policy`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91E_Experiment_Intervention.md -->

# G91E — Experiment Intervention

Milestone：**M88**

## Objective

EXPERIMENT 模式显式 Intervention 并进入 WorldRunArtifact。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. intervention types
2. time/event trigger
3. branch isolation
4. reversible experiment setup


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- intervention cannot rewrite parent history

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91e: Experiment Intervention`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91F_Quest_Projection_Adapter.md -->

# G91F — Quest Projection Adapter

Milestone：**M88**

## Objective

如需要任务式体验，把 Opportunity 投影为 Quest，不让 Quest 成为 Kernel truth。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. quest view
2. progress from committed state
3. optional objectives


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no fake progress from narrative text

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91f: Quest Projection Adapter`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91G_Pressure_Behavior_Benchmark.md -->

# G91G — Pressure Behavior Benchmark

Milestone：**M88**

## Objective

有压力/无压力两组 worldline 比较行为差异。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. same seed/profile
2. metrics
3. no scientific overclaim


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- repeatability

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91g: Pressure Behavior Benchmark`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G91H_M88_Director_Pressure_Qualification.md -->

# G91H — M88 Director/Pressure Qualification

Milestone：**M88**

## Objective

真实 playable world 中 Director modes/Pressure/Opportunity 全部可运行且权限正确。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. mode switch
2. ignore opportunity
3. experiment branch


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- M88 PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G91H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g91h: M88 Director/Pressure Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92A_Long-Horizon_Scheduler.md -->

# G92A — Long-Horizon Scheduler

Milestone：**M89**

## Objective

支持持续 world time / recurring schedules / actor availability。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. recurring events
2. priority queue
3. calendar/time zones if domain requires
4. catch-up


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- deterministic scheduler tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92a: Long-Horizon Scheduler`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92B_Background_Simulation.md -->

# G92B — Background Simulation

Milestone：**M89**

## Objective

用户离线后世界按 RuntimeProfile 继续或暂停。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. pause/realtime/accelerated/background/full autonomy
2. session independence


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- leave/re-enter world state continuity

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92b: Background Simulation`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92C_Checkpoint_Resume_Crash_Recovery.md -->

# G92C — Checkpoint / Resume / Crash Recovery

Milestone：**M89**

## Objective

长运行中断可恢复。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. periodic checkpoint
2. atomic cursor
3. job/runtime resume
4. crash injection


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no duplicate commits after resume

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92c: Checkpoint / Resume / Crash Recovery`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92D_Snapshot_Compaction_Policy.md -->

# G92D — Snapshot / Compaction Policy

Milestone：**M89**

## Objective

控制 event/memory/storage 增长且保持 replay。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. snapshot cadence
2. event compaction refs
3. memory summary refs
4. archive


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- golden replay before/after compaction

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92d: Snapshot / Compaction Policy`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92E_SimulationLOD_Runtime.md -->

# G92E — SimulationLOD Runtime

Milestone：**M89**

## Objective

实现 L0-L4 activation/transition。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. actor activity scoring
2. LOD transition
3. cohort aggregation
4. promotion back to active


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- state continuity across LOD

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92e: SimulationLOD Runtime`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92F_Resource_Cost_Budget.md -->

# G92F — Resource / Cost Budget

Milestone：**M89**

## Objective

每世界/Actor/Provider 有预算与降级策略。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. call/token/time/storage budgets
2. backpressure
3. LOD degradation
4. alerts


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- budget exhaustion graceful

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92f: Resource / Cost Budget`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92G_24h_7d_Long_Run.md -->

# G92G — 24h / 7d Long Run

Milestone：**M89**

## Objective

建立快速长期运行测试。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 24h reference
2. 7d multiple actors
3. metrics


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- replay/recovery/storage PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92g: 24h / 7d Long Run`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G92H_30d_Qualification.md -->

# G92H — 30d Qualification

Milestone：**M89**

## Objective

至少一个 source-created world 30 天加速持续运行。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. actor activation
2. memory growth
3. cost/storage
4. checkpoint/recovery


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- 30d no P0/P1 logical corruption

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G92H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g92h: 30d Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93A_Evolution_Delta_Taxonomy.md -->

# G93A — Evolution Delta Taxonomy

Milestone：**M90**

## Objective

正式分离不同类型演化 Delta。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. State/Belief/Relationship/Capability/Persona/Organization
2. schema/version
3. commit/provenance policy


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no generic evolution blob

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93a: Evolution Delta Taxonomy`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93B_Capability_Growth.md -->

# G93B — Capability Growth

Milestone：**M90**

## Objective

经验/练习/组合可形成 CapabilityCandidate。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. prerequisites
2. practice evidence
3. success/failure
4. validation
5. promotion to actor skill


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- cannot learn impossible capability without domain support

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93b: Capability Growth`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93C_Persona_Adaptation.md -->

# G93C — Persona Adaptation

Milestone：**M90**

## Objective

长期经历可提出 PersonaDelta，但需慢变量与证据。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. trait dimensions
2. windowed evidence
3. bounded change
4. review/policy


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- one event cannot rewrite full persona

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93c: Persona Adaptation`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93D_Relationship_Evolution.md -->

# G93D — Relationship Evolution

Milestone：**M90**

## Objective

事件→关系变化→未来行为反馈。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. delta rules/provider proposals
2. clamps/invariants
3. history


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- replay equality

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93d: Relationship Evolution`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93E_Organization_Lifecycle.md -->

# G93E — Organization Lifecycle

Milestone：**M90**

## Objective

创建/加入/退出/角色/权限/解散/分裂。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. organization state
2. membership
3. roles
4. authority
5. resources


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- orphan permissions removed

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93e: Organization Lifecycle`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93F_Reputation_Social_Role.md -->

# G93F — Reputation / Social Role

Milestone：**M90**

## Objective

声誉/角色通过 evidence-backed social events 更新。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. local/global scope
2. observer-specific reputation where applicable


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- rumor/belief separation

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93f: Reputation / Social Role`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93G_Evolution_Explainability.md -->

# G93G — Evolution Explainability

Milestone：**M90**

## Objective

为什么 Actor/关系/组织变成现在这样可查询。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. trajectory ledger links
2. delta reasons
3. source/events
4. projection


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no hidden provider state as sole reason

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93g: Evolution Explainability`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G93H_M90_30d_Evolution_Qualification.md -->

# G93H — M90 30d Evolution Qualification

Milestone：**M90**

## Objective

30 天运行出现非零且合理的 Actor/Relationship/Organization 变化。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. baseline vs evolved compare
2. no source canon mutation


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- evolution evidence PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G93H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g93h: M90 30d Evolution Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94A_Pattern_Observation_Store.md -->

# G94A — Pattern Observation Store

Milestone：**M91**

## Objective

从 committed history 产生可查询 pattern observations，不做第二套 history。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. windowed queries
2. feature/statistics
3. event refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- derived cache rebuildable

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94a: Pattern Observation Store`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94B_Repeated_Pattern_Detector.md -->

# G94B — Repeated Pattern Detector

Milestone：**M91**

## Objective

检测重复行为/关系/交换/组织模式。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. deterministic reference algorithms
2. thresholds
3. confidence
4. counterexamples


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- false-positive fixtures

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94b: Repeated Pattern Detector`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94C_Habit_Skill_Candidate.md -->

# G94C — Habit / Skill Candidate

Milestone：**M91**

## Objective

Actor 级模式晋升为 Habit/Skill candidate。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. evidence window
2. stability
3. decay
4. promotion policy


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- not automatic truth

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94c: Habit / Skill Candidate`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94D_Social_Norm_Candidate.md -->

# G94D — Social Norm Candidate

Milestone：**M91**

## Objective

群体重复模式产生 NormCandidate。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. population support
2. exceptions
3. sanction/reward correlation
4. scope


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- small-sample guard

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94d: Social Norm Candidate`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94E_Institution_Candidate.md -->

# G94E — Institution Candidate

Milestone：**M91**

## Objective

稳定组织/规范结构产生 InstitutionCandidate。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. rule/role/resource/process structure
2. provenance
3. review


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no single manager auto-commit

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94e: Institution Candidate`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94F_Culture_Ontology_Candidate.md -->

# G94F — Culture / Ontology Candidate

Milestone：**M91**

## Objective

跨较长时间的共享符号/习惯/分类可产生高层 Candidate。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. strict high threshold
2. cross-window evidence
3. human/review gate


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- cannot silently change Constitution

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94f: Culture / Ontology Candidate`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94G_Promotion_Ladder_Enforcement.md -->

# G94G — Promotion Ladder Enforcement

Milestone：**M91**

## Objective

L0-L5 晋升越高需要更多证据/世界/审批。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. policy stack
2. sandbox
3. benchmark
4. rollback


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- high-level promotion negative tests

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94g: Promotion Ladder Enforcement`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G94H_M91_Emergence_Qualification.md -->

# G94H — M91 Emergence Qualification

Milestone：**M91**

## Objective

受控长期世界出现至少一种可复验 Pattern，并证明候选/晋升链和 false-positive control。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. positive/negative worlds
2. replay


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no claim of universal emergence

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G94H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g94h: M91 Emergence Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95A_WorldRunArtifact_v1.md -->

# G95A — WorldRunArtifact v1

Milestone：**M92**

## Objective

把一次运行的环境、版本、历史与指标封装为可复验 Artifact。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. manifest
2. world/scenario/provider/seed
3. commit/snapshot refs
4. metrics
5. privacy sanitization


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- artifact roundtrip
- tamper/hash checks

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95a: WorldRunArtifact v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95B_Experiment_Registry.md -->

# G95B — Experiment Registry

Milestone：**M92**

## Objective

版本化保存 ExperimentDefinition 和 runs。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. status
2. parameters
3. owners
4. rights
5. run refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- concurrent run safety

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95b: Experiment Registry`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95C_Fork_Intervention_Runner.md -->

# G95C — Fork / Intervention Runner

Milestone：**M92**

## Objective

从明确 snapshot/event fork，按时间/事件注入 intervention。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. branch provenance
2. intervention ledger
3. resume


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- parent isolation

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95c: Fork / Intervention Runner`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95D_Batch_Worldlines.md -->

# G95D — Batch Worldlines

Milestone：**M92**

## Objective

同一实验多 seed / parameter 批量运行。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. queue
2. parallelism limits
3. checkpoint
4. aggregation


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- reproducible seeds

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95d: Batch Worldlines`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95E_Multi-provider_Mixed-population.md -->

# G95E — Multi-provider / Mixed-population

Milestone：**M92**

## Objective

比较不同 Agent/LLM/Policy Provider 或混合人群。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. provider assignment policy
2. same world inputs
3. runtime control ledger


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- provider output still proposal only

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95e: Multi-provider / Mixed-population`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95F_Worldline_Comparator.md -->

# G95F — Worldline Comparator

Milestone：**M92**

## Objective

比较 Actor/Relation/Institution/Macro/Cost trajectories。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. alignment
2. diff metrics
3. visual/API report


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no cherry-picked single metric

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95f: Worldline Comparator`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95G_ValidationProfile_v1.md -->

# G95G — ValidationProfile v1

Milestone：**M92**

## Objective

正式实现 V0-V7 profile/schema/report。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. worldness mapping
2. source fidelity
3. behavior/mechanism/macro/long horizon/counterfactual/external


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- unknown != pass

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95g: ValidationProfile v1`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G95H_M92_Lab_Qualification.md -->

# G95H — M92 Lab Qualification

Milestone：**M92**

## Objective

至少完成一个 4+ worldline batch + intervention + comparison + RunArtifact。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. one literary/one structured or family-like experiment
2. sanitized evidence


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- M92 PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G95H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g95h: M92 Lab Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96A_PhysicalWorldProvider_ABI.md -->

# G96A — PhysicalWorldProvider ABI

Milestone：**M93**

## Objective

定义外部物理/空间模拟 Provider contract。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. readonly snapshot input
2. simulation request
3. resolution/proposed delta
4. health/version


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- contract tests
- no commit access

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96a: PhysicalWorldProvider ABI`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96B_VisualWorldProvider_ABI.md -->

# G96B — VisualWorldProvider ABI

Milestone：**M93**

## Objective

定义视觉生成/渲染 Provider contract。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. scene state
2. actor perspective
3. projection frames
4. asset refs
5. events


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- projection cannot mutate reality

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96b: VisualWorldProvider ABI`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96C_Multi-perspective_Projection.md -->

# G96C — Multi-perspective Projection

Milestone：**M93**

## Objective

ABI 天然支持多个 Actor 不同视角。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. actor-specific perception
2. occlusion/rights filters
3. frame refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- A view cannot leak B private knowledge

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96c: Multi-perspective Projection`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96D_Reference_Physical_Provider.md -->

# G96D — Reference Physical Provider

Milestone：**M93**

## Objective

实现可 CI 的轻量 deterministic reference adapter，验证桥接链。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. simple navigation/collision or existing sim adapter
2. resolution evidence


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- replay deterministic

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96d: Reference Physical Provider`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96E_Reference_Visual_Projection_Provider.md -->

# G96E — Reference Visual Projection Provider

Milestone：**M93**

## Objective

实现可 CI 的 non-generative scene/state projection reference。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. structured scene frame
2. actor views
3. state/event refs


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no external GPU/model dependency

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96e: Reference Visual Projection Provider`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96F_External_Engine_Adapter_Audit.md -->

# G96F — External Engine Adapter Audit

Milestone：**M93**

## Objective

如仓库已有 Godot/Phaser/other bridge 则适配 ABI；否则只提供 adapter port + docs，不伪称外部引擎已验证。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. capability discovery
2. EXTERNAL_BLOCKED semantics


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no fake pass

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96f: External Engine Adapter Audit`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96G_Projection_Reality_Consistency.md -->

# G96G — Projection/Reality Consistency

Milestone：**M93**

## Objective

视觉/物理输出与 Canonical Reality divergence 可检测。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. consistency checker
2. stale frame/version checks
3. reconciliation proposal


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- visual hallucination cannot become fact

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96g: Projection/Reality Consistency`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G96H_M93_Provider_Bridge_Qualification.md -->

# G96H — M93 Provider Bridge Qualification

Milestone：**M93**

## Objective

reference physical + visual providers 通过 E2E；外部重型 provider 只在环境可用时验收。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. playable world integration
2. multi-perspective smoke


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- M93 PASS

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G96H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g96h: M93 Provider Bridge Qualification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97A_Certification_Matrix_Freeze.md -->

# G97A — Certification Matrix Freeze

Milestone：**M94**

## Objective

冻结 v5.5 rc1 验收矩阵，禁止为通过而降低阈值。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. playable/product
2. long horizon
3. evolution
4. emergence
5. lab
6. provider bridge
7. security
8. performance


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- matrix reviewed in repo

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97A_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97a: Certification Matrix Freeze`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97B_Literary_30d_90d_Certification.md -->

# G97B — Literary 30d/90d Certification

Milestone：**M94**

## Objective

使用 v5.4 已创建的真实文学世界进行长期加速验收，不提交原书。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. 30d required
2. 90d required selected profile
3. checkpoint/recovery
4. actor/relationship drift


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- replay/branch/storage/cost

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97b: Literary 30d/90d Certification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97C_Non-literary_Long-run_Certification.md -->

# G97C — Non-literary Long-run Certification

Milestone：**M94**

## Objective

至少一个 structured/family-like/public world 长周期运行。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. different domain
2. same runtime substrate


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no literary-specific runtime path

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97C_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97c: Non-literary Long-run Certification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97D_Parallel_Worldline_Certification.md -->

# G97D — Parallel Worldline Certification

Milestone：**M94**

## Objective

至少 multi-provider/policy 4 条平行 worldlines + comparator。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. same initial state/seed policy
2. record differences
3. no scientific overclaim


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- RunArtifacts complete

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97D_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97d: Parallel Worldline Certification`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97E_Experience_Product_E2E.md -->

# G97E — Experience Product E2E

Milestone：**M94**

## Objective

World Plaza→Character→Play→StateDiff→Leave→Continue→Workshop→Publish/Private 全链。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. browser/API/CLI where applicable
2. rights


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- Playwright/product E2E

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97E_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97e: Experience Product E2E`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97F_Security_Safety_Cost_Storage.md -->

# G97F — Security / Safety / Cost / Storage

Milestone：**M94**

## Objective

长周期和 UGC 输入的安全/预算/隐私/包安全验收。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. prompt/data injection
2. untrusted package
3. resource exhaustion
4. source privacy
5. secret scan


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no P0/P1

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97F_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97f: Security / Safety / Cost / Storage`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97G_Clean_Clone_GitHub_CI.md -->

# G97G — Clean Clone + GitHub CI

Milestone：**M94**

## Objective

clean clone 全量安装、迁移、Python/TS/Studio/long-run smoke，push并修到 Actions 绿。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. remote SHA == local HEAD
2. working tree clean


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- all required jobs success

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97G_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97g: Clean Clone + GitHub CI`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97H_v5_5_0-rc1_Release_Gate.md -->

# G97H — v5.5.0-rc1 Release Gate

Milestone：**M94**

## Objective

只有真实 Certification ACCEPTED 才创建 rc1 prerelease。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. annotated tag
2. GitHub prerelease
3. release notes boundaries
4. post-release clean clone


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- tag/release verification

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97H_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97h: v5.5.0-rc1 Release Gate`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97I_Final_Evidence_Status.md -->

# G97I — Final Evidence & Status

Milestone：**M94**

## Objective

生成可机器读取 final evidence 和已实现/实验/未证明边界。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. STATUS/CHANGELOG/acceptance reports
2. research_not_proven list


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- evidence complete

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97I_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97i: Final Evidence & Status`。
- 自动继续下一 Goal。


---

<!-- FILE: goals/G97J_STOP.md -->

# G97J — STOP

Milestone：**M94**

## Objective

发布/不发布结论后停止，不自动开始 v5.6 或模型训练。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. preserve checkpoint if blocked


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Required Tests / Evidence

- no scope creep

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G97J_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g97j: STOP`。
- 自动继续下一 Goal。


---

<!-- FILE: milestones/M85_QUALIFICATION.md -->

# M85 — Playable World Experience Shell Qualification

必须先完成：
- G88A v5.4 Stable Baseline & v5.5 Branch
- G88B PlayableWorldProfile v1
- G88C ExperiencePackage v1
- G88D World Plaza / My Worlds / Continue
- G88E My Characters / Character Entry
- G88F Free Action Intent Compiler
- G88G Committed StateDiff v1
- G88H M85 Playable E2E Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M85_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M86_QUALIFICATION.md -->

# M86 — Character / Goal / Memory / StateDiff Qualification

必须先完成：
- G89A ActorGoalStack v1
- G89B Goal Reprioritization
- G89C EpistemicMemory v1
- G89D Belief Revision
- G89E RelationshipState v1
- G89F Character Passport
- G89G Actor Continuity Projection
- G89H M86 Character Continuity Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M86_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M87_QUALIFICATION.md -->

# M87 — World Workshop + Prompt Genesis + Publishing Qualification

必须先完成：
- G90A Workshop Information Architecture
- G90B Prompt Genesis Contract
- G90C Prompt Genesis Provider
- G90D Hybrid Genesis
- G90E Scenario / Experience Editor
- G90F Publishing Profiles
- G90G World Registry / Marketplace Baseline
- G90H M87 Workshop Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M87_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M88_QUALIFICATION.md -->

# M88 — World Pressure / Opportunity / Director Modes Qualification

必须先完成：
- G91A PressureProfile v1
- G91B Opportunity / Challenge
- G91C DirectorPolicy Modes
- G91D Canon Attractor Policy
- G91E Experiment Intervention
- G91F Quest Projection Adapter
- G91G Pressure Behavior Benchmark
- G91H M88 Director/Pressure Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M88_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M89_QUALIFICATION.md -->

# M89 — Long-Horizon Runtime + SimulationLOD Qualification

必须先完成：
- G92A Long-Horizon Scheduler
- G92B Background Simulation
- G92C Checkpoint / Resume / Crash Recovery
- G92D Snapshot / Compaction Policy
- G92E SimulationLOD Runtime
- G92F Resource / Cost Budget
- G92G 24h / 7d Long Run
- G92H 30d Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M89_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M90_QUALIFICATION.md -->

# M90 — Actor / Relationship / Organization Evolution Qualification

必须先完成：
- G93A Evolution Delta Taxonomy
- G93B Capability Growth
- G93C Persona Adaptation
- G93D Relationship Evolution
- G93E Organization Lifecycle
- G93F Reputation / Social Role
- G93G Evolution Explainability
- G93H M90 30d Evolution Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M90_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M91_QUALIFICATION.md -->

# M91 — Emergence / Institution / Culture Qualification

必须先完成：
- G94A Pattern Observation Store
- G94B Repeated Pattern Detector
- G94C Habit / Skill Candidate
- G94D Social Norm Candidate
- G94E Institution Candidate
- G94F Culture / Ontology Candidate
- G94G Promotion Ladder Enforcement
- G94H M91 Emergence Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M91_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M92_QUALIFICATION.md -->

# M92 — World Laboratory Qualification

必须先完成：
- G95A WorldRunArtifact v1
- G95B Experiment Registry
- G95C Fork / Intervention Runner
- G95D Batch Worldlines
- G95E Multi-provider / Mixed-population
- G95F Worldline Comparator
- G95G ValidationProfile v1
- G95H M92 Lab Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M92_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M93_QUALIFICATION.md -->

# M93 — Physical / Visual World Provider Bridge Qualification

必须先完成：
- G96A PhysicalWorldProvider ABI
- G96B VisualWorldProvider ABI
- G96C Multi-perspective Projection
- G96D Reference Physical Provider
- G96E Reference Visual Projection Provider
- G96F External Engine Adapter Audit
- G96G Projection/Reality Consistency
- G96H M93 Provider Bridge Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M93_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。


---

<!-- FILE: milestones/M94_QUALIFICATION.md -->

# M94 — v5.5 Certification Qualification

必须先完成：
- G97A Certification Matrix Freeze
- G97B Literary 30d/90d Certification
- G97C Non-literary Long-run Certification
- G97D Parallel Worldline Certification
- G97E Experience Product E2E
- G97F Security / Safety / Cost / Storage
- G97G Clean Clone + GitHub CI
- G97H v5.5.0-rc1 Release Gate
- G97I Final Evidence & Status
- G97J STOP


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M94_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。
