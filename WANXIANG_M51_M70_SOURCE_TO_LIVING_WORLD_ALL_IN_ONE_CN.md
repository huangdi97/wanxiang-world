# WANXIANG M51–M70 SOURCE → LIVING WORLD — ALL-IN-ONE


---

<!-- FILE: README_FIRST.md -->

# Wanxiang M51–M70：Source → Living World 全量连续工程执行包

本包**取代**此前单独的 M51–M59 包。不要把两套 Goal 叠加执行；从本包开始，以本包为唯一工程执行 Source of Truth。

## 最终目标

不是只做到“能导入一本书”，而是一次把后续阶段接上：

```text
Book / GEDCOM / JSON / CSV / DOCX / text-PDF / Assets / Multi-source Bundle
→ Source Registry
→ Parse / Segment / Stable Locator
→ Multi-pass Distillation
→ Candidate / Claim / Evidence / Rights
→ Cross-source Fusion / Conflict Preservation
→ Domain Inference / Composition
→ WorldDraft
→ Constraint-backed Completion
→ Scenario / Genesis Authoring
→ WorldPackageDraft
→ Preview Instance
→ Worldness Validation
→ Repair / Completion Loop
→ Publishable World Package
→ Living World Instance
```

## M51–M59：World Creation Foundation

把统一的 Source→WorldDraft→Preview 底层做实。

## M60–M70：Autonomous World Authoring & Genesis

继续把 Preview 初稿推进到：
- 长文本世界理解；
- 多版本/多来源融合；
- 多模态/外部 Source 能力；
- Domain 自动推断与组合；
- 约束驱动的世界补全；
- Scenario/Genesis 自动生成；
- Worldness 自动验证；
- 自动修补循环；
- 最小人工审核；
- 一键 Source→Living World；
- GitHub CI + RC 发布。

## 关键边界

- **不训练 Wanxiang 自有基础模型。**
- LLM / embedding / OCR / ASR / vision / world model 都是可替换 Provider。
- 没有 API Key 时，核心 deterministic/reference E2E 仍必须通过。
- 模型输出永远是 Candidate / Proposal，不拥有 Commit Authority。
- 不为《红楼梦》、家谱或任何单一领域修改 Kernel。
- “任意一本书自动得到 100% 正确完整世界”不是可诚实承诺的验收标准；本包要求的是**有证据、有不确定性、有补全等级、有验证闭环的自动世界创作系统**。


---

<!-- FILE: 00_MASTER_ROADMAP.md -->

# M51–M70 总路线

## Phase A — World Creation Foundation

- **M51** Post-v5.3 Audit & Forge Baseline
- **M52** Source Registry & Adapter Foundation
- **M53** Parse / Segment / Stable Locator
- **M54** Distillation & Candidate Fabric
- **M55** Evidence / Rights / Review / Completion Core
- **M56** Domain Matching & WorldDraft
- **M57** World Compiler / Package / Preview
- **M58** Studio Create World Wizard + API / CLI
- **M59** Cross-source E2E / Hardening

## Phase B — Autonomous World Authoring & Genesis

- **M60** Book-scale Semantic World Understanding
- **M61** Multi-source / Multi-version Fusion
- **M62** Multimodal & External Source Expansion
- **M63** Domain Inference / Composition / Gap Packs
- **M64** Constraint-backed Completion & Consistency
- **M65** Scenario / Genesis Auto Authoring
- **M66** Worldness Validation & Simulation Closure
- **M67** Autonomous Authoring Orchestrator
- **M68** Minimal Human Review / Active Review Studio
- **M69** One-click Source → Living World E2E
- **M70** Production Hardening / GitHub CI / v5.4 RC

## 终局停止条件

M70 PASS 后必须停止，不自行进入：
- World Foundation Model 训练；
- 大规模 GPU 训练；
- 自修改 Kernel；
- v5.5；
- 任意新大型领域实例。


---

<!-- FILE: 01_ARCHITECTURE_BOUNDARIES.md -->

# 架构边界与不可破坏原则

## 万相工程总分解

```text
Wanxiang Kernel
  Reality Root / Semantic ISA / Identity / Fact / Event / Constraint
  Commit / Ledger / Snapshot / Replay / Branch / Worldline / Lineage / Invariant

Wanxiang Runtime
  World Host / Clock / Space / Body / Objects / Actors / Organizations
  Perception / Belief / Memory / Action / Simulation / Capability Fabric

Wanxiang Forge
  Source / Evidence / Distillation / Completion / Genesis / Compiler
  WorldDraft / Domain Composition / Emergence / Evolution / Promotion

Experiences
  Studio / Player / Strategy / Heritage / Family / Learn / SDK
```

## 本轮修改集中区域

主要修改：Forge + Studio + adapters + infra + tests。

Kernel 语义默认冻结。

## 十条禁止

1. 禁止创建第二套 Canonical State。
2. 禁止创建第二套 Commit pipeline。
3. 禁止创建第二套 Package Registry。
4. 禁止每种 Source 做一套独立世界编译流程。
5. 禁止 per-domain Runtime fork。
6. 禁止 LLM/Agent/Parser 直接写 Canon。
7. 禁止前端 local state 成为世界权威。
8. 禁止 WorldDraft 演化成第二个 Runtime State。
9. 禁止以 giant WorldManager / ForgeManager / Utils 聚合全部逻辑。
10. 禁止为了本轮需求改 Reality Root，除非跨领域不可表达且有失败证据与 Kernel Change Proposal。


---

<!-- FILE: 02_SOURCE_TO_LIVING_WORLD_PIPELINE.md -->

# Source → Living World 正式管线

```text
[1] SOURCE
    ↓
[2] SourceRegistry + Rights + Version + Checksum
    ↓
[3] SourceAdapter
    ↓
[4] ParsedDocument / StructuredRecords / AssetReferences
    ↓
[5] Segment + StableLocator
    ↓
[6] Multi-pass Distillation
    ↓
[7] CandidateEnvelope / Claim / Evidence
    ↓
[8] Identity Resolution + Cross-source Alignment
    ↓
[9] Conflict Preservation + Review Decisions
    ↓
[10] Domain Inference / Dependency Resolution
    ↓
[11] WorldDraft
    ↓
[12] Missingness Graph / Completion Plan
    ↓
[13] Completion Candidate E0–E5
    ↓
[14] Consistency / Constraint Validation
    ↓
[15] Scenario Candidate / Genesis Plan
    ↓
[16] WorldPackageDraft
    ↓
[17] Preview Instance
    ↓
[18] Worldness Evaluation
    ↓
[19] Repair Proposal / Completion Loop
    ↓
[20] Publishable WorldPackage
    ↓
[21] Living World Instance
```

### 统一原则

任何环节都只能增加：来源、候选、审核、补全、编译产物或 Proposal。
只有 Runtime 的唯一 Commit Boundary 可以产生运行历史。


---

<!-- FILE: 03_SOURCE_ADAPTER_MATRIX.md -->

# Source Adapter Matrix

## Foundation 必须支持

| 类型 | 本轮最低能力 |
|---|---|
| TXT / Markdown | 结构化文本导入、标题/段落、稳定 locator |
| EPUB | spine / href / chapter / text |
| DOCX | paragraph / heading / table locator |
| text-PDF | page-aware text；扫描版显式 OCR_REQUIRED |
| JSON / YAML | JSON Pointer / path |
| CSV | row/column locator |
| GEDCOM | xref/tag path；Family source |
| Generic Asset | 图片/音频/视频登记为 AssetReference |

## Phase B 扩展

- OCR Provider：扫描 PDF / 古籍图片。
- Image Understanding Provider：人物、物体、场景、地图辅助候选。
- ASR Provider：音频/视频转写。
- Subtitle / Transcript Adapter。
- IIIF / web/API connector port。
- Multi-source bundle manifest。

所有 Provider 都必须可缺省；缺 Provider 时明确返回 capability requirement，不伪装成功。


---

<!-- FILE: 04_SEMANTIC_DISTILLATION_SPEC.md -->

# 多轮世界语义蒸馏规范

## Candidate 类型

- Identity / Alias
- Character / Persona / LifeArc
- Relation
- Organization / Role
- Event / Timeline / Causality Candidate
- Time / Temporal Uncertainty
- Place / Space / Topology
- Object / Object Biography
- Knowledge Boundary / Witness / Secret
- Rule / Norm / Institution
- Skill / Behaviour / Affordance
- Scenario
- Ontology

## 多轮蒸馏

```text
Pass 0 Structure
Pass 1 Identity
Pass 2 Event-Time-Space
Pass 3 Relation-Organization
Pass 4 Character-Knowledge
Pass 5 Object-Rule-Skill
Pass 6 Cross-chapter/Coreference
Pass 7 Contradiction/Gap
Pass 8 World Assembly Candidates
```

每一轮必须：
- versioned；
- resumable；
- source-locatable；
- deterministic reference path 可测试；
- 可被更强 Provider 替换。

LLM 可以提高 recall，但不得绕过 Candidate/Evidence/Review。


---

<!-- FILE: 05_WORLD_DRAFT_SCHEMA.md -->

# WorldDraft 正式定位

WorldDraft 是 Forge 的**可编辑编译中间产物**，不是运行世界，不拥有 Commit Authority。

## 必备结构

- draft_id / revision
- source_refs / source_versions
- constitution_ref
- selected_domains / dependency_lock
- entities / aliases
- character_profiles
- organizations / roles
- relations
- places / topology
- objects / biographies
- events / timeline
- knowledge_boundaries
- rules / norms / institutions
- skills / affordances
- completion_items
- unresolved_conflicts
- unresolved_rights
- scenario_candidates
- genesis_candidates
- coverage / uncertainty / quality metrics
- compiler metadata

## Draft lifecycle

```text
CREATED
→ INGESTING
→ DISTILLING
→ FUSING
→ REVIEW_REQUIRED
→ COMPLETION_REQUIRED
→ VALIDATING
→ READY_TO_COMPILE
→ PREVIEWABLE
→ PUBLISHABLE
```


---

<!-- FILE: 06_AUTONOMOUS_WORLD_AUTHORING_SPEC.md -->

# Autonomous World Authoring

目标不是“让一个 Agent 自由写世界”，而是让 Orchestrator 自动驱动**受约束的编译闭环**。

```text
Assess Draft
↓
Find Missing / Conflict / Low Confidence
↓
Choose Tool / Distiller / Retrieval / Domain Rule / Completion Provider
↓
Generate Candidate / Proposed Repair
↓
Evidence + Rights + Constraint Check
↓
Auto-approve only low-risk policy class
↓
Rebuild Draft
↓
Preview
↓
Worldness Evaluate
↓
Repeat until stop criteria
```

## 自动停止条件

- 无 P0 blocking gap；
- publish-required rights PASS；
- critical identities resolved；
- initial scenario instantiate PASS；
- replay/determinism PASS；
- worldness minimum thresholds PASS；
- remaining uncertainty is explicitly labeled rather than fabricated。

## 自动化绝不能做

- 把模型幻觉提升成 E0；
- 把冲突来源消成单一“真相”；
- 改写源文件；
- 直接改 Kernel；
- 为通过分数而硬编码 benchmark fixture。


---

<!-- FILE: 07_COMPLETION_CONSISTENCY_SPEC.md -->

# Completion / Consistency / Missingness

## Missingness Graph

系统必须能表达“世界为什么还不能稳定运行”，例如：
- Actor 缺初始 location；
- location 不连通；
- object ownership 未知；
- scenario 缺初始时间；
- rule 缺 resolver；
- character knowledge boundary 缺失；
- schedule 缺关键时段；
- Domain requirement 未满足。

## Completion 分级

- E0 直接证据
- E1 多来源支持重建
- E2 领域/时代规则推导
- E3 运行必需系统默认
- E4 体验性生成
- E5 用户虚构

任何 E1–E5 永远不能静默升级为 E0。

## Consistency

至少验证：
- temporal consistency
- identity consistency
- topology connectivity
- ownership/custody consistency
- knowledge non-leakage
- organization/role validity
- scenario completeness
- package dependency consistency
- rights compatibility


---

<!-- FILE: 08_WORLDNESS_VALIDATION_SPEC.md -->

# Worldness Validation

Preview 不是“能启动进程”就算世界。

## 最低 Worldness 指标

1. Persistence：物品/人物/关系状态跨 tick 持续存在。
2. Temporal Causality：事件顺序和前置条件有效。
3. Epistemic Isolation：角色不知道未观察/未传播的信息。
4. Spatial Coherence：移动必须经过可达空间关系。
5. Action Consequence：行动产生真实、可回放后果。
6. Autonomous Continuation：无用户时至少参考策略可推进。
7. Branch Isolation：Preview/Branch 不污染母本。
8. Replayability：事件日志可重建状态。
9. Provenance：关键世界定义能回到 Source/Completion。
10. Uncertainty Honesty：未知保持未知，不用生成内容伪装事实。

## 自动验证循环

```text
Preview Run
→ Detect Worldness Failure
→ Gap / Repair Candidate
→ Review Policy
→ Draft Revision
→ Recompile
→ New Preview
```

Preview simulation 永远不能直接回写 Source 或 Canon World Definition。


---

<!-- FILE: 09_STUDIO_ONE_CLICK_SPEC.md -->

# Studio 一键创建世界

## Basic Flow

```text
Create World
→ Drop Sources
→ Choose rights / privacy
→ Start Auto Authoring
→ Watch Progress
→ Review only required items
→ Preview
→ Publish World
→ Start Living Instance
```

## 进度页必须显示

- ingest status
- parse coverage
- semantic passes
- entities/relations/events/places/objects counts
- evidence coverage
- conflicts
- rights blocks
- domain suggestions
- missingness
- completion classes
- worldness score breakdown
- current authoring loop
- cost/provider usage
- remaining human decisions

## Review UX

默认只要求用户处理：
- identity ambiguity with high downstream impact；
- source contradiction with canon impact；
- rights/consent；
- E4/E5 high-impact generation；
- constitution/domain policy decisions；
- publish gate。


---

<!-- FILE: 10_MODEL_PROVIDER_POLICY.md -->

# Model / AI Provider Policy

本轮**不训练自有模型**。

## 可接入能力

- LLM Provider
- Embedding / Reranker
- OCR
- ASR
- Vision / VLM
- Entity linking
- Temporal parser
- Retrieval
- Optional world predictor / planner

## Provider 输出权限

仅允许：
- Observation
- ParsedCandidate
- CandidateEnvelope
- Claim
- Prediction
- CompletionCandidate
- RepairProposal
- AssetCandidate

禁止：
- direct ORM canonical write
- direct Commit
- mutation of source
- mutation of Constitution

## 无 API Key 基准

CI 与 reference E2E 必须使用 deterministic/rule/synthetic Provider 可通过。
真实模型 E2E 可标 optional integration。


---

<!-- FILE: 11_GITHUB_CI_RELEASE_POLICY.md -->

# GitHub / CI / Release Policy

使用现有公开 `wanxiang-world` 仓库，不新建 repo。

## 分支

优先：`feature/source-to-living-world`

## 每个 Milestone

- 本地 qualification PASS；
- commit；
- 自动继续。

## 最终 M70

1. secret/private/copyright corpus scan；
2. full local CI；
3. push feature branch；
4. 查询真实 GitHub Actions；
5. CI FAIL → 读日志 → 修 → commit → push；
6. required CI 全绿；
7. 可创建 PR；
8. 若 release policy 与权限允许，打 `v5.4.0-rc1`；
9. 生成 GitHub Release Candidate；
10. 记录 final SHA / workflow runs / release evidence。

禁止 force push、泄露真实 family data、上传受限书籍 corpus、重指已发布 tag。


---

<!-- FILE: 12_CODEX_MASTER_PROMPT_CN.md -->

# CODEX MASTER PROMPT — M51–M70

继续当前 `wanxiang-world` 仓库。

## Mission

把万相连续推进到：

> **用户可以给系统一本书、一个 GEDCOM、结构化数据或多来源资料包；系统自动完成 Source 登记、解析、蒸馏、多来源融合、Domain 组合、WorldDraft、约束补全、Scenario/Genesis、WorldPackage、Preview、Worldness 验证与修补，并在需要少量关键人工审核后发布为可持续运行的 Living World。**

## Execution

严格按 `13_GOALS_INDEX.md` 从 M51 第一个 Goal 执行到 M70 最后一个 Goal。

- 不等待用户确认“是否继续”。
- 每 Goal PASS 后 commit。
- 每 Milestone qualification PASS 后自动继续。
- 内部失败必须修；不能用 EXTERNAL_BLOCKED 逃避。
- 只有真实第三方授权、账号登录、缺失私人数据、硬件或外部服务不可取得时可 EXTERNAL_BLOCKED。
- 外部 Provider 缺失时优先用 deterministic/reference provider 继续内部工程。

## Kernel Freeze

Reality Root / Commit / Ledger / Snapshot / Replay / Branch / Worldline / Lineage 核心语义默认冻结。

任何 Kernel change 必须满足：
1. 至少两个不同 Domain 的相同不可表达失败；
2. 最小失败测试；
3. compatibility/migration 分析；
4. Kernel Change Proposal；
5. regression gate。

## No Model Training

本轮不训练 Wanxiang 自有 Foundation Model。
所有 AI 通过 Capability Fabric / Provider 接入。

## Final GitHub Delivery

最后推送现有公开仓库 feature branch，查询真实 GitHub Actions；失败则读取日志、修复、commit、push，直到 required CI 全绿。
若权限允许按仓库 release policy 创建 v5.4.0-rc1 RC。
然后生成最终报告并 STOP。


---

<!-- FILE: 13_GOALS_INDEX.md -->

# Goal Index

## M51 — Post-v5.3 Audit & Forge Baseline
- **G54A** — Repository truth audit — `goals/G54A_Repository_truth_audit.md`
- **G54B** — Kernel freeze goldens — `goals/G54B_Kernel_freeze_goldens.md`
- **G54C** — Forge gap graph — `goals/G54C_Forge_gap_graph.md`
- **G54D** — Duplicate abstraction cleanup — `goals/G54D_Duplicate_abstraction_cleanup.md`
- **G54E** — Job/resume baseline — `goals/G54E_Job_resume_baseline.md`
- **G54F** — M51 qualification — `goals/G54F_M51_qualification.md`

## M52 — Source Registry & Adapter Foundation
- **G55A** — SourceRecord convergence — `goals/G55A_SourceRecord_convergence.md`
- **G55B** — Blob asset reference — `goals/G55B_Blob_asset_reference.md`
- **G55C** — SourceAdapter ABI — `goals/G55C_SourceAdapter_ABI.md`
- **G55D** — Book adapters — `goals/G55D_Book_adapters.md`
- **G55E** — Structured adapters — `goals/G55E_Structured_adapters.md`
- **G55F** — Asset adapter — `goals/G55F_Asset_adapter.md`
- **G55G** — Ingestion security — `goals/G55G_Ingestion_security.md`
- **G55H** — M52 qualification — `goals/G55H_M52_qualification.md`

## M53 — Parse / Segment / Stable Locator
- **G56A** — ParsedDocument model — `goals/G56A_ParsedDocument_model.md`
- **G56B** — Structural parsing — `goals/G56B_Structural_parsing.md`
- **G56C** — Segment model — `goals/G56C_Segment_model.md`
- **G56D** — Stable locator — `goals/G56D_Stable_locator.md`
- **G56E** — Incremental parsing — `goals/G56E_Incremental_parsing.md`
- **G56F** — Checkpoint resume — `goals/G56F_Checkpoint_resume.md`
- **G56G** — Diagnostics API — `goals/G56G_Diagnostics_API.md`
- **G56H** — M53 qualification — `goals/G56H_M53_qualification.md`

## M54 — Distillation & Candidate Fabric
- **G57A** — CandidateEnvelope convergence — `goals/G57A_CandidateEnvelope_convergence.md`
- **G57B** — Distiller protocol — `goals/G57B_Distiller_protocol.md`
- **G57C** — Identity alias — `goals/G57C_Identity_alias.md`
- **G57D** — Event time space — `goals/G57D_Event_time_space.md`
- **G57E** — Relation organization — `goals/G57E_Relation_organization.md`
- **G57F** — Character knowledge — `goals/G57F_Character_knowledge.md`
- **G57G** — Object rule skill — `goals/G57G_Object_rule_skill.md`
- **G57H** — Candidate clustering — `goals/G57H_Candidate_clustering.md`
- **G57I** — M54 qualification — `goals/G57I_M54_qualification.md`

## M55 — Evidence / Rights / Review / Completion Core
- **G58A** — Evidence binding — `goals/G58A_Evidence_binding.md`
- **G58B** — Claim conflict — `goals/G58B_Claim_conflict.md`
- **G58C** — Rights gate — `goals/G58C_Rights_gate.md`
- **G58D** — Review decisions — `goals/G58D_Review_decisions.md`
- **G58E** — Completion E0-E5 — `goals/G58E_Completion_E0_E5.md`
- **G58F** — Completion planner — `goals/G58F_Completion_planner.md`
- **G58G** — Review APIs — `goals/G58G_Review_APIs.md`
- **G58H** — M55 qualification — `goals/G58H_M55_qualification.md`

## M56 — Domain Matching & WorldDraft
- **G59A** — Domain capability manifest — `goals/G59A_Domain_capability_manifest.md`
- **G59B** — Reference recommender — `goals/G59B_Reference_recommender.md`
- **G59C** — Dependency resolver — `goals/G59C_Dependency_resolver.md`
- **G59D** — WorldDraft v1 — `goals/G59D_WorldDraft_v1.md`
- **G59E** — Coverage missingness — `goals/G59E_Coverage_missingness.md`
- **G59F** — Scenario candidates — `goals/G59F_Scenario_candidates.md`
- **G59G** — Genesis draft — `goals/G59G_Genesis_draft.md`
- **G59H** — M56 qualification — `goals/G59H_M56_qualification.md`

## M57 — World Compiler / Package / Preview
- **G60A** — Compiler boundary — `goals/G60A_Compiler_boundary.md`
- **G60B** — Package assembler — `goals/G60B_Package_assembler.md`
- **G60C** — Package validation — `goals/G60C_Package_validation.md`
- **G60D** — Incremental rebuild — `goals/G60D_Incremental_rebuild.md`
- **G60E** — Preview install — `goals/G60E_Preview_install.md`
- **G60F** — Preview instantiate — `goals/G60F_Preview_instantiate.md`
- **G60G** — Preview smoke — `goals/G60G_Preview_smoke.md`
- **G60H** — M57 qualification — `goals/G60H_M57_qualification.md`

## M58 — Studio Create World Wizard + API / CLI
- **G61A** — Creation API — `goals/G61A_Creation_API.md`
- **G61B** — Draft review API — `goals/G61B_Draft_review_API.md`
- **G61C** — CLI workflow — `goals/G61C_CLI_workflow.md`
- **G61D** — Studio upload parse — `goals/G61D_Studio_upload_parse.md`
- **G61E** — Studio distill review — `goals/G61E_Studio_distill_review.md`
- **G61F** — Studio domain completion — `goals/G61F_Studio_domain_completion.md`
- **G61G** — Studio draft preview — `goals/G61G_Studio_draft_preview.md`
- **G61H** — M58 qualification — `goals/G61H_M58_qualification.md`

## M59 — Cross-source E2E / Hardening
- **G62A** — Book E2E — `goals/G62A_Book_E2E.md`
- **G62B** — GEDCOM E2E — `goals/G62B_GEDCOM_E2E.md`
- **G62C** — Structured E2E — `goals/G62C_Structured_E2E.md`
- **G62D** — Idempotency resume — `goals/G62D_Idempotency_resume.md`
- **G62E** — Large source performance — `goals/G62E_Large_source_performance.md`
- **G62F** — Security rights — `goals/G62F_Security_rights.md`
- **G62G** — Backward compatibility — `goals/G62G_Backward_compatibility.md`
- **G62H** — M59 qualification — `goals/G62H_M59_qualification.md`

## M60 — Book-scale Semantic World Understanding
- **G63A** — Long-range identity resolution — `goals/G63A_Long_range_identity_resolution.md`
- **G63B** — Temporal narrative separation — `goals/G63B_Temporal_narrative_separation.md`
- **G63C** — Character life arc — `goals/G63C_Character_life_arc.md`
- **G63D** — Knowledge propagation graph — `goals/G63D_Knowledge_propagation_graph.md`
- **G63E** — Spatial topology assembly — `goals/G63E_Spatial_topology_assembly.md`
- **G63F** — Object biography — `goals/G63F_Object_biography.md`
- **G63G** — Institution norm extraction — `goals/G63G_Institution_norm_extraction.md`
- **G63H** — Semantic quality metrics — `goals/G63H_Semantic_quality_metrics.md`
- **G63I** — M60 qualification — `goals/G63I_M60_qualification.md`

## M61 — Multi-source / Multi-version Fusion
- **G64A** — Source family model — `goals/G64A_Source_family_model.md`
- **G64B** — Cross-source alignment — `goals/G64B_Cross_source_alignment.md`
- **G64C** — Claim provenance graph — `goals/G64C_Claim_provenance_graph.md`
- **G64D** — Source policy — `goals/G64D_Source_policy.md`
- **G64E** — Conflict workbench — `goals/G64E_Conflict_workbench.md`
- **G64F** — Incremental supplemental source — `goals/G64F_Incremental_supplemental_source.md`
- **G64G** — Rights interaction — `goals/G64G_Rights_interaction.md`
- **G64H** — M61 qualification — `goals/G64H_M61_qualification.md`

## M62 — Multimodal & External Source Expansion
- **G65A** — OCR provider port — `goals/G65A_OCR_provider_port.md`
- **G65B** — Image understanding port — `goals/G65B_Image_understanding_port.md`
- **G65C** — ASR transcript port — `goals/G65C_ASR_transcript_port.md`
- **G65D** — Subtitle transcript adapter — `goals/G65D_Subtitle_transcript_adapter.md`
- **G65E** — IIIF/API connector port — `goals/G65E_IIIF_API_connector_port.md`
- **G65F** — Bundle manifest — `goals/G65F_Bundle_manifest.md`
- **G65G** — Media rights/privacy — `goals/G65G_Media_rights_privacy.md`
- **G65H** — M62 qualification — `goals/G65H_M62_qualification.md`

## M63 — Domain Inference / Composition / Gap Packs
- **G66A** — Domain fingerprint — `goals/G66A_Domain_fingerprint.md`
- **G66B** — Composite domain planning — `goals/G66B_Composite_domain_planning.md`
- **G66C** — Domain gap detection — `goals/G66C_Domain_gap_detection.md`
- **G66D** — DomainCapabilityCandidate — `goals/G66D_DomainCapabilityCandidate.md`
- **G66E** — Gap pack scaffold — `goals/G66E_Gap_pack_scaffold.md`
- **G66F** — Cross-world reuse check — `goals/G66F_Cross_world_reuse_check.md`
- **G66G** — Domain validation sandbox — `goals/G66G_Domain_validation_sandbox.md`
- **G66H** — M63 qualification — `goals/G66H_M63_qualification.md`

## M64 — Constraint-backed Completion & Consistency
- **G67A** — Missingness graph — `goals/G67A_Missingness_graph.md`
- **G67B** — Completion candidate generator — `goals/G67B_Completion_candidate_generator.md`
- **G67C** — Spatial completion — `goals/G67C_Spatial_completion.md`
- **G67D** — Schedule social completion — `goals/G67D_Schedule_social_completion.md`
- **G67E** — Object continuity completion — `goals/G67E_Object_continuity_completion.md`
- **G67F** — Consistency solver — `goals/G67F_Consistency_solver.md`
- **G67G** — Uncertainty calibration — `goals/G67G_Uncertainty_calibration.md`
- **G67H** — M64 qualification — `goals/G67H_M64_qualification.md`

## M65 — Scenario / Genesis Auto Authoring
- **G68A** — Scenario mining — `goals/G68A_Scenario_mining.md`
- **G68B** — Initial snapshot builder — `goals/G68B_Initial_snapshot_builder.md`
- **G68C** — Activation set — `goals/G68C_Activation_set.md`
- **G68D** — Canon policy — `goals/G68D_Canon_policy.md`
- **G68E** — Runtime profile — `goals/G68E_Runtime_profile.md`
- **G68F** — Genesis plan — `goals/G68F_Genesis_plan.md`
- **G68G** — Reproducible seed — `goals/G68G_Reproducible_seed.md`
- **G68H** — M65 qualification — `goals/G68H_M65_qualification.md`

## M66 — Worldness Validation & Simulation Closure
- **G69A** — Worldness evaluator — `goals/G69A_Worldness_evaluator.md`
- **G69B** — Bounded simulation — `goals/G69B_Bounded_simulation.md`
- **G69C** — Failure localization — `goals/G69C_Failure_localization.md`
- **G69D** — Repair proposal — `goals/G69D_Repair_proposal.md`
- **G69E** — Recompile loop — `goals/G69E_Recompile_loop.md`
- **G69F** — Branch isolation — `goals/G69F_Branch_isolation.md`
- **G69G** — Determinism envelope — `goals/G69G_Determinism_envelope.md`
- **G69H** — M66 qualification — `goals/G69H_M66_qualification.md`

## M67 — Autonomous Authoring Orchestrator
- **G70A** — Authoring DAG — `goals/G70A_Authoring_DAG.md`
- **G70B** — Stage policy — `goals/G70B_Stage_policy.md`
- **G70C** — Provider routing — `goals/G70C_Provider_routing.md`
- **G70D** — Auto-loop — `goals/G70D_Auto_loop.md`
- **G70E** — Stopping criteria — `goals/G70E_Stopping_criteria.md`
- **G70F** — Budget guard — `goals/G70F_Budget_guard.md`
- **G70G** — Crash resume — `goals/G70G_Crash_resume.md`
- **G70H** — M67 qualification — `goals/G70H_M67_qualification.md`

## M68 — Minimal Human Review / Active Review Studio
- **G71A** — Impact scoring — `goals/G71A_Impact_scoring.md`
- **G71B** — Auto-approval policy — `goals/G71B_Auto_approval_policy.md`
- **G71C** — Review inbox — `goals/G71C_Review_inbox.md`
- **G71D** — Batch review — `goals/G71D_Batch_review.md`
- **G71E** — Impact preview — `goals/G71E_Impact_preview.md`
- **G71F** — Audit provenance — `goals/G71F_Audit_provenance.md`
- **G71G** — Review UX E2E — `goals/G71G_Review_UX_E2E.md`
- **G71H** — M68 qualification — `goals/G71H_M68_qualification.md`

## M69 — One-click Source → Living World E2E
- **G72A** — One-click book — `goals/G72A_One_click_book.md`
- **G72B** — One-click family — `goals/G72B_One_click_family.md`
- **G72C** — One-click structured world — `goals/G72C_One_click_structured_world.md`
- **G72D** — Mixed-source world — `goals/G72D_Mixed_source_world.md`
- **G72E** — Living world acceptance — `goals/G72E_Living_world_acceptance.md`
- **G72F** — Studio product flow — `goals/G72F_Studio_product_flow.md`
- **G72G** — CLI/API product flow — `goals/G72G_CLI_API_product_flow.md`
- **G72H** — M69 qualification — `goals/G72H_M69_qualification.md`

## M70 — Production Hardening / GitHub CI / v5.4 RC
- **G73A** — Clean-room clone — `goals/G73A_Clean_room_clone.md`
- **G73B** — Security corpus audit — `goals/G73B_Security_corpus_audit.md`
- **G73C** — Performance recovery — `goals/G73C_Performance_recovery.md`
- **G73D** — Docs SDK examples — `goals/G73D_Docs_SDK_examples.md`
- **G73E** — CI matrix — `goals/G73E_CI_matrix.md`
- **G73F** — GitHub delivery — `goals/G73F_GitHub_delivery.md`
- **G73G** — RC release — `goals/G73G_RC_release.md`
- **G73H** — M70 final certification — `goals/G73H_M70_final_certification.md`


---

<!-- FILE: 14_MILESTONE_GATES.md -->

# Milestone Gates

- **M51** — Post-v5.3 Audit & Forge Baseline — `milestones/M51_QUALIFICATION.md`
- **M52** — Source Registry & Adapter Foundation — `milestones/M52_QUALIFICATION.md`
- **M53** — Parse / Segment / Stable Locator — `milestones/M53_QUALIFICATION.md`
- **M54** — Distillation & Candidate Fabric — `milestones/M54_QUALIFICATION.md`
- **M55** — Evidence / Rights / Review / Completion Core — `milestones/M55_QUALIFICATION.md`
- **M56** — Domain Matching & WorldDraft — `milestones/M56_QUALIFICATION.md`
- **M57** — World Compiler / Package / Preview — `milestones/M57_QUALIFICATION.md`
- **M58** — Studio Create World Wizard + API / CLI — `milestones/M58_QUALIFICATION.md`
- **M59** — Cross-source E2E / Hardening — `milestones/M59_QUALIFICATION.md`
- **M60** — Book-scale Semantic World Understanding — `milestones/M60_QUALIFICATION.md`
- **M61** — Multi-source / Multi-version Fusion — `milestones/M61_QUALIFICATION.md`
- **M62** — Multimodal & External Source Expansion — `milestones/M62_QUALIFICATION.md`
- **M63** — Domain Inference / Composition / Gap Packs — `milestones/M63_QUALIFICATION.md`
- **M64** — Constraint-backed Completion & Consistency — `milestones/M64_QUALIFICATION.md`
- **M65** — Scenario / Genesis Auto Authoring — `milestones/M65_QUALIFICATION.md`
- **M66** — Worldness Validation & Simulation Closure — `milestones/M66_QUALIFICATION.md`
- **M67** — Autonomous Authoring Orchestrator — `milestones/M67_QUALIFICATION.md`
- **M68** — Minimal Human Review / Active Review Studio — `milestones/M68_QUALIFICATION.md`
- **M69** — One-click Source → Living World E2E — `milestones/M69_QUALIFICATION.md`
- **M70** — Production Hardening / GitHub CI / v5.4 RC — `milestones/M70_QUALIFICATION.md`


---

<!-- FILE: 15_RESUME_PROTOCOL.md -->

# Resume Protocol

会话压缩/重启后：

1. 读取 STATUS.md / PLAN.md / 当前 branch。
2. 读取 reports/SOURCE_TO_LIVING_WORLD_ACCEPTANCE_MATRIX.md。
3. 读取最近 milestone qualification。
4. 读取最近 Goal report。
5. `git status`、`git log --oneline --decorate -40`。
6. 定位最早 ACTIVE / FAIL Goal。
7. 从该 Goal 恢复；不要重做已可复现 PASS。
8. 若当前 job 有 checkpoint，从 checkpoint 恢复，不重新 ingest。
9. 不因上下文丢失重新设计 Kernel。


---

<!-- FILE: 16_FINAL_ACCEPTANCE.md -->

# M70 Final Acceptance

最终必须同时满足：

1. v5.3 核心 Commit/Replay/Branch/Worldline/Package regression PASS。
2. TXT/MD/EPUB/DOCX/text-PDF/JSON/YAML/CSV/GEDCOM foundation adapters PASS。
3. 扫描 PDF 在无 OCR Provider 时明确 OCR_REQUIRED。
4. Stable Locator 能把关键 Candidate/Evidence 回到来源。
5. 长书跨章节 identity/event/time/relation/knowledge candidate 能工作。
6. 多来源/多版本冲突可以并存且可解释。
7. Rights/consent 不被自动绕过。
8. Domain 推荐、组合、版本锁定与 gap detection 工作。
9. WorldDraft 可保存、恢复、revision、重编。
10. Completion E0–E5 不混淆；未知可保持未知。
11. Scenario/Genesis 可自动提出并实例化至少三个候选起点。
12. WorldPackageDraft 复用正式 package schema。
13. Preview Instance 可以执行动作、Commit、Replay、Branch。
14. Worldness evaluator 覆盖 persistence/causality/epistemic/spatial/consequence/autonomy/branch/replay/provenance。
15. 至少一个 benchmark 经过自动 repair loop 从 FAIL 到 PASS。
16. Autonomous Authoring Orchestrator 可 unattended 跑完整 reference pipeline。
17. 用户不需要逐条审核全部 Candidate，只处理 policy-required high-impact items。
18. 一键 Book → Living World E2E PASS。
19. 一键 GEDCOM → Family Living Preview PASS。
20. JSON/CSV → Living World E2E PASS。
21. Mixed-source bundle E2E PASS。
22. no-API deterministic/reference CI PASS。
23. 可选真实 AI Provider 不拥有 Commit Authority。
24. 大书 ingest/parse/distill 可 checkpoint/resume/idempotent。
25. malicious source / archive / prompt injection / path traversal / secret leakage tests PASS。
26. private family/copyright corpus 不进入 Git history。
27. Studio Create→Auto Author→Review→Preview→Publish→Enter World E2E PASS。
28. CLI/API 等价流程 PASS。
29. clean-room clone/bootstrap/migrate/test/sample authoring PASS。
30. GitHub feature branch 已 push，remote SHA == local final SHA。
31. required GitHub Actions completed/success。
32. 若 release policy/权限允许，v5.4.0-rc1 tag 与 RC release 已创建。
33. reports/SOURCE_TO_LIVING_WORLD_FINAL_REPORT.md 完整。
34. working tree clean。
35. 不把 EXPERIMENTAL / RESEARCH_NOT_PROVEN 伪装成 production proven。


---

<!-- FILE: 17_RED_CHAMBER_IMPORT_REFERENCE.md -->

# 《红楼梦》参考验收路径（非硬编码需求）

该实例只用于验证通用架构，不允许红楼梦专名进入 Kernel/通用 Forge。

```text
合法测试底本/用户本地 Source
→ book parsing
→ characters/aliases
→ places/organizations
→ events/timeline
→ relations/knowledge boundaries
→ objects/rules/social norms
→ HistoricalChina + HouseholdSociety + Narrative domain suggestions
→ completion gaps
→ scenario candidates
→ WorldDraft
→ Preview
→ 7-day bounded worldness run
→ publishable package (若 rights permit)
```

验收重点：
- 不把补全冒充原著；
- 秘密不自动泄露；
- 分支不污染 Canon；
- Source locator 可回原文；
- 同一人物多称谓不盲合并；
- 用户本地受限文本默认不进 Git。


---

<!-- FILE: 18_FAMILY_IMPORT_REFERENCE.md -->

# Family World 参考验收路径

```text
Synthetic GEDCOM + synthetic photos/notes
→ Source Registry
→ GEDCOM identities/families/events/places
→ Family Domain
→ Claim conflict preservation
→ privacy/consent
→ migration/life-event timeline
→ Family WorldDraft
→ scenario candidate
→ Preview
```

验收重点：
- 家谱树只是 Projection；
- conflicting claims 共存；
- living-person privacy；
- digital persona 不得越过 consent；
- 反事实分支不能回写 Evidence History。


---

<!-- FILE: 19_NON_GOALS_AND_RESEARCH_BOUNDARIES.md -->

# Non-goals / Research Boundaries

M70 PASS 不代表：
- 任意文学作品都能零误差自动理解；
- 任意扫描古籍 OCR 100% 正确；
- 自动推断的历史空间就是史实；
- 世界里所有人物达到人类级自治；
- 已训练出 World Foundation Model；
- 开放式演化问题已经科学解决。

必须用状态标记区分：
- IMPLEMENTED
- VALIDATED_ON_BENCHMARK
- OPTIONAL_PROVIDER
- EXPERIMENTAL
- RESEARCH_NOT_PROVEN

禁止把“接口存在”写成“研究问题解决”。


---

<!-- FILE: goals/G54A_Repository_truth_audit.md -->

# G54A — Repository truth audit

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

审计 v5.3 真实源码、reports、migrations、CI、package/runtime/forge/studio，建立 KEEP/EXTEND/MERGE/DELETE/ADD 矩阵。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G54B_Kernel_freeze_goldens.md -->

# G54B — Kernel freeze goldens

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

冻结 Commit/Replay/Branch/Worldline/Package 关键 golden 与 architecture guards。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G54C_Forge_gap_graph.md -->

# G54C — Forge gap graph

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

建立 Source→Living World 端到端 capability/gap graph。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G54D_Duplicate_abstraction_cleanup.md -->

# G54D — Duplicate abstraction cleanup

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

清理重复 registry/job/candidate/review/package abstractions。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G54E_Job_resume_baseline.md -->

# G54E — Job/resume baseline

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

复用或建立统一 Import/Authoring Job checkpoint/resume/idempotency。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G54F_M51_qualification.md -->

# G54F — M51 qualification

Milestone: **M51 — Post-v5.3 Audit & Forge Baseline**

## Objective

生成基线报告并通过 v5.3 regression。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G54F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55A_SourceRecord_convergence.md -->

# G55A — SourceRecord convergence

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

统一 SourceRecord/version/checksum/rights/access/reliability/schema。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55B_Blob_asset_reference.md -->

# G55B — Blob asset reference

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

建立 content-addressed source/blob/asset reference，避免业务表存原始大 bytes。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55C_SourceAdapter_ABI.md -->

# G55C — SourceAdapter ABI

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

统一 can_handle/inspect/ingest/resume 与 typed failures。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55D_Book_adapters.md -->

# G55D — Book adapters

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

实现 TXT/MD/EPUB/DOCX/text-PDF。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55E_Structured_adapters.md -->

# G55E — Structured adapters

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

实现 JSON/YAML/CSV/GEDCOM。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55F_Asset_adapter.md -->

# G55F — Asset adapter

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

图片/音频/视频可登记为 GenericAsset，语义理解 capability 可缺省。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55G_Ingestion_security.md -->

# G55G — Ingestion security

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

zip bomb/path traversal/size/encoding/encrypted/corrupt/rights gate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G55H_M52_qualification.md -->

# G55H — M52 qualification

Milestone: **M52 — Source Registry & Adapter Foundation**

## Objective

adapter matrix + idempotency + resume 全通过。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G55H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56A_ParsedDocument_model.md -->

# G56A — ParsedDocument model

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

统一 DocumentMetadata/StructuralNode/AssetRef 中间表示。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56B_Structural_parsing.md -->

# G56B — Structural parsing

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

章/节/段/对话/table/record 统一结构。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56C_Segment_model.md -->

# G56C — Segment model

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

stable id/content hash/parent/ordinal/parser+segmenter version。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56D_Stable_locator.md -->

# G56D — Stable locator

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

EPUB/DOCX/PDF/GEDCOM/JSON/CSV 可回源 locator。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56E_Incremental_parsing.md -->

# G56E — Incremental parsing

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

cache/version invalidation/局部重跑。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56F_Checkpoint_resume.md -->

# G56F — Checkpoint resume

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

大文件 parse 中断恢复、原子发布。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56G_Diagnostics_API.md -->

# G56G — Diagnostics API

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

结构预览、warning、error、locator preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G56H_M53_qualification.md -->

# G56H — M53 qualification

Milestone: **M53 — Parse / Segment / Stable Locator**

## Objective

跨格式 locator round-trip。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G56H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57A_CandidateEnvelope_convergence.md -->

# G57A — CandidateEnvelope convergence

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

统一候选外壳、origin/confidence/source/evidence/distiller version。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57B_Distiller_protocol.md -->

# G57B — Distiller protocol

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

统一多轮 Distiller DAG 与 provider boundary。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57C_Identity_alias.md -->

# G57C — Identity alias

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

entity/alias/coreference candidate，不 destructive merge。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57D_Event_time_space.md -->

# G57D — Event time space

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

event/participant/time uncertainty/place candidates。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57E_Relation_organization.md -->

# G57E — Relation organization

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

relation/role/membership/organization candidates。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57F_Character_knowledge.md -->

# G57F — Character knowledge

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

persona/life arc/goal/belief/knowledge boundary candidates。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57G_Object_rule_skill.md -->

# G57G — Object rule skill

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

object/rule/norm/skill/affordance candidates。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57H_Candidate_clustering.md -->

# G57H — Candidate clustering

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

merge/split suggestions、reversible decisions。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G57I_M54_qualification.md -->

# G57I — M54 qualification

Milestone: **M54 — Distillation & Candidate Fabric**

## Objective

book/GEDCOM/structured deterministic candidate E2E。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G57I_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58A_Evidence_binding.md -->

# G58A — Evidence binding

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

candidate↔source locator/evidence support/contradict 双向追踪。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58B_Claim_conflict.md -->

# G58B — Claim conflict

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

conflict set、不 last-write-wins。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58C_Rights_gate.md -->

# G58C — Rights gate

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

model/display/export/package inclusion 权限检查。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58D_Review_decisions.md -->

# G58D — Review decisions

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

approve/reject/edit/merge/split/defer/request evidence。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58E_Completion_E0_E5.md -->

# G58E — Completion E0-E5

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

CompletionLedger、origin、can_enter_canon default false。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58F_Completion_planner.md -->

# G58F — Completion planner

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

missing runtime requirements 与 keep-unknown 选项。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58G_Review_APIs.md -->

# G58G — Review APIs

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

高影响优先、批量操作、server authority。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G58H_M55_qualification.md -->

# G58H — M55 qualification

Milestone: **M55 — Evidence / Rights / Review / Completion Core**

## Objective

冲突/rights/rollback/审计 PASS。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G58H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59A_Domain_capability_manifest.md -->

# G59A — Domain capability manifest

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

Domain provides/requires/schema/actions/rules/compat。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59B_Reference_recommender.md -->

# G59B — Reference recommender

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

基于 source/candidate features 推荐 Domain 且可解释。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59C_Dependency_resolver.md -->

# G59C — Dependency resolver

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

复用 package resolver 处理版本/冲突。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59D_WorldDraft_v1.md -->

# G59D — WorldDraft v1

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

持久化、revision、candidate selections、sources/domains/completion/scenarios。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59E_Coverage_missingness.md -->

# G59E — Coverage missingness

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

coverage/unknown/blocking/rights/conflict 指标。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59F_Scenario_candidates.md -->

# G59F — Scenario candidates

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

从 timeline/source 产生起点候选。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59G_Genesis_draft.md -->

# G59G — Genesis draft

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

constitution/domain/world/scenario/seed/runtime profile plan。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G59H_M56_qualification.md -->

# G59H — M56 qualification

Milestone: **M56 — Domain Matching & WorldDraft**

## Objective

book/GEDCOM/structured 均形成可恢复 Draft。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G59H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60A_Compiler_boundary.md -->

# G60A — Compiler boundary

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

仅吃 Reviewed WorldDraft，pin revisions/versions。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60B_Package_assembler.md -->

# G60B — Package assembler

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

复用正式 WorldPackage schema。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60C_Package_validation.md -->

# G60C — Package validation

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

dependency/evidence/rights/unresolved gap/publish vs preview gate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60D_Incremental_rebuild.md -->

# G60D — Incremental rebuild

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

按 section/content hash 重编。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60E_Preview_install.md -->

# G60E — Preview install

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

隔离 preview registry/scope，不污染 published catalog。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60F_Preview_instantiate.md -->

# G60F — Preview instantiate

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

复用 Genesis/World Host 创建 preview instance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60G_Preview_smoke.md -->

# G60G — Preview smoke

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

实体/关系/时空/动作/commit/replay 最小世界性。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G60H_M57_qualification.md -->

# G60H — M57 qualification

Milestone: **M57 — World Compiler / Package / Preview**

## Objective

Draft→Package→Preview 两类 source 通过。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G60H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61A_Creation_API.md -->

# G61A — Creation API

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

create/add source/start/cancel/resume/status。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61B_Draft_review_API.md -->

# G61B — Draft review API

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

candidate/conflict/completion/domain/scenario/revision endpoints。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61C_CLI_workflow.md -->

# G61C — CLI workflow

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

world create/import/status/review/build/preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61D_Studio_upload_parse.md -->

# G61D — Studio upload parse

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

拖拽、rights、adapter、progress、parse preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61E_Studio_distill_review.md -->

# G61E — Studio distill review

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

candidate filters、merge/split、evidence drawer、conflict。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61F_Studio_domain_completion.md -->

# G61F — Studio domain completion

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

domain cards、dependency conflict、E0-E5、keep unknown。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61G_Studio_draft_preview.md -->

# G61G — Studio draft preview

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

coverage、compile、scenario、preview launch。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G61H_M58_qualification.md -->

# G61H — M58 qualification

Milestone: **M58 — Studio Create World Wizard + API / CLI**

## Objective

GUI/CLI 共用 backend use cases，Playwright PASS。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G61H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62A_Book_E2E.md -->

# G62A — Book E2E

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

EPUB/TXT → Preview 完整链。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62B_GEDCOM_E2E.md -->

# G62B — GEDCOM E2E

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

GEDCOM → Family Draft → Preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62C_Structured_E2E.md -->

# G62C — Structured E2E

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

JSON/CSV → WorldDraft → Preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62D_Idempotency_resume.md -->

# G62D — Idempotency resume

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

重复导入/kill/retry/changed bytes source version。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62E_Large_source_performance.md -->

# G62E — Large source performance

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

大 synthetic book 的流式/缓存/内存/恢复。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62F_Security_rights.md -->

# G62F — Security rights

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

malicious source/prompt injection/private corpus leakage。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62G_Backward_compatibility.md -->

# G62G — Backward compatibility

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

v5.3 package/runtime/multiverse critical regression。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G62H_M59_qualification.md -->

# G62H — M59 qualification

Milestone: **M59 — Cross-source E2E / Hardening**

## Objective

Foundation 完整证据矩阵。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G62H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63A_Long_range_identity_resolution.md -->

# G63A — Long-range identity resolution

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

跨章节 alias/coreference/阶段身份解析，保持可撤销。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63B_Temporal_narrative_separation.md -->

# G63B — Temporal narrative separation

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

叙述顺序与事件顺序、相对时间、时间范围。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63C_Character_life_arc.md -->

# G63C — Character life arc

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

人物阶段/关系变化/目标/信念随时间的候选轨迹。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63D_Knowledge_propagation_graph.md -->

# G63D — Knowledge propagation graph

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

见证/阅读/转述/秘密传播候选。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63E_Spatial_topology_assembly.md -->

# G63E — Spatial topology assembly

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

place containment/connectivity/access 候选图，不伪造坐标。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63F_Object_biography.md -->

# G63F — Object biography

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

物品 ownership/custody/location/transfer 的候选历史。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63G_Institution_norm_extraction.md -->

# G63G — Institution norm extraction

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

组织/角色/礼制/规范/惩罚候选。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63H_Semantic_quality_metrics.md -->

# G63H — Semantic quality metrics

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

precision/recall proxy、conflict/unknown/coverage/calibration。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G63I_M60_qualification.md -->

# G63I — M60 qualification

Milestone: **M60 — Book-scale Semantic World Understanding**

## Objective

多章节 synthetic novel 全书级一致性验收。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G63I_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64A_Source_family_model.md -->

# G64A — Source family model

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

edition/version/commentary/supplement/translation/source family。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64B_Cross_source_alignment.md -->

# G64B — Cross-source alignment

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

entity/event/place/quote locator 对齐。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64C_Claim_provenance_graph.md -->

# G64C — Claim provenance graph

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

support/contradict/refine/derivative provenance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64D_Source_policy.md -->

# G64D — Source policy

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

canon preference/authority/reliability policy，但不消灭异议。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64E_Conflict_workbench.md -->

# G64E — Conflict workbench

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

版本差异、互斥 claim、影响范围。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64F_Incremental_supplemental_source.md -->

# G64F — Incremental supplemental source

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

新增资料后仅重跑受影响部分。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64G_Rights_interaction.md -->

# G64G — Rights interaction

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

不同来源 rights 冲突与 package inclusion。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G64H_M61_qualification.md -->

# G64H — M61 qualification

Milestone: **M61 — Multi-source / Multi-version Fusion**

## Objective

两版本书+补充资料的 fusion E2E。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G64H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65A_OCR_provider_port.md -->

# G65A — OCR provider port

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

扫描 PDF/image OCR provider + OCR_REQUIRED fallback。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65B_Image_understanding_port.md -->

# G65B — Image understanding port

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

图像/地图/场景 candidate provider，输出 Asset/Observation Candidate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65C_ASR_transcript_port.md -->

# G65C — ASR transcript port

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

音频/视频转写 provider 与 stable time locator。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65D_Subtitle_transcript_adapter.md -->

# G65D — Subtitle transcript adapter

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

字幕/转写作为可追踪 Source。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65E_IIIF_API_connector_port.md -->

# G65E — IIIF/API connector port

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

远端资源 manifest/connector contract。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65F_Bundle_manifest.md -->

# G65F — Bundle manifest

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

文本+图片+音频+结构化资料作为一个 source bundle。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65G_Media_rights_privacy.md -->

# G65G — Media rights/privacy

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

biometric/voice/image/public display model-use 权限。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G65H_M62_qualification.md -->

# G65H — M62 qualification

Milestone: **M62 — Multimodal & External Source Expansion**

## Objective

有 provider/无 provider 两种路径均诚实可恢复。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G65H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66A_Domain_fingerprint.md -->

# G66A — Domain fingerprint

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

从 source/candidate 生成领域需求 fingerprint。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66B_Composite_domain_planning.md -->

# G66B — Composite domain planning

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

多 Domain 组合、dependency lock、冲突解释。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66C_Domain_gap_detection.md -->

# G66C — Domain gap detection

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

发现现有 Domain 无法表达的通用能力缺口。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66D_DomainCapabilityCandidate.md -->

# G66D — DomainCapabilityCandidate

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

缺口只形成候选，不自动改 Kernel。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66E_Gap_pack_scaffold.md -->

# G66E — Gap pack scaffold

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

在 sandbox 生成小型 Domain extension/package 草案。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66F_Cross_world_reuse_check.md -->

# G66F — Cross-world reuse check

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

优先匹配已有 Domain/Capability，避免 per-world duplication。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66G_Domain_validation_sandbox.md -->

# G66G — Domain validation sandbox

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

schema/actions/rules/invariants benchmark。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G66H_M63_qualification.md -->

# G66H — M63 qualification

Milestone: **M63 — Domain Inference / Composition / Gap Packs**

## Objective

book/family/structured 三类 domain planning 通过。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G66H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67A_Missingness_graph.md -->

# G67A — Missingness graph

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

把缺 actor/space/time/object/rule/scenario/domain requirement 结构化。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67B_Completion_candidate_generator.md -->

# G67B — Completion candidate generator

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

规则/检索/可选模型生成 E1-E5 completion candidates。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67C_Spatial_completion.md -->

# G67C — Spatial completion

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

路径/containment/access/travel-time 只按等级补全。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67D_Schedule_social_completion.md -->

# G67D — Schedule social completion

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

作息/职责/访问规范/轻量 NPC needs。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67E_Object_continuity_completion.md -->

# G67E — Object continuity completion

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

初始位置/ownership/custody 缺口。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67F_Consistency_solver.md -->

# G67F — Consistency solver

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

temporal/topology/identity/ownership/knowledge/role constraints。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67G_Uncertainty_calibration.md -->

# G67G — Uncertainty calibration

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

不确定度与 evidence class 对齐，未知可保留。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G67H_M64_qualification.md -->

# G67H — M64 qualification

Milestone: **M64 — Constraint-backed Completion & Consistency**

## Objective

completion 不伪造 E0，constraint failures 可解释。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G67H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68A_Scenario_mining.md -->

# G68A — Scenario mining

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

从事件/阶段/地点发现可运行起点。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68B_Initial_snapshot_builder.md -->

# G68B — Initial snapshot builder

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

生成 actor/place/object/time initial snapshot candidate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68C_Activation_set.md -->

# G68C — Activation set

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

前台 actor / duty NPC / background population activation plan。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68D_Canon_policy.md -->

# G68D — Canon policy

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

Canon/Soft Canon/Living/Counterfactual mode。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68E_Runtime_profile.md -->

# G68E — Runtime profile

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

clock/scheduler/agent/provider/budget profile。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68F_Genesis_plan.md -->

# G68F — Genesis plan

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

constitution/domain/package/scenario/seed/rights 组合。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68G_Reproducible_seed.md -->

# G68G — Reproducible seed

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

同 seed/reference providers 可重建 preview genesis。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G68H_M65_qualification.md -->

# G68H — M65 qualification

Milestone: **M65 — Scenario / Genesis Auto Authoring**

## Objective

至少三个自动 Scenario 可 instantiate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G68H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69A_Worldness_evaluator.md -->

# G69A — Worldness evaluator

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

Persistence/Causality/Epistemic/Spatial/Consequence/Autonomy/Branch/Replay/Provenance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69B_Bounded_simulation.md -->

# G69B — Bounded simulation

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

7-day reference run；复杂 world 可 accelerated。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69C_Failure_localization.md -->

# G69C — Failure localization

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

把 worldness failure 映射到 draft/missingness/domain/completion。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69D_Repair_proposal.md -->

# G69D — Repair proposal

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

simulation feedback 只产生 repair candidate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69E_Recompile_loop.md -->

# G69E — Recompile loop

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

draft revision→package→new preview 自动迭代。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69F_Branch_isolation.md -->

# G69F — Branch isolation

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

验证 preview/repair branches 不污染 source/definition。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69G_Determinism_envelope.md -->

# G69G — Determinism envelope

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

记录 seed/providers/nondeterminism/validity。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G69H_M66_qualification.md -->

# G69H — M66 qualification

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

worldness repair loop 至少收敛一个有缺口 benchmark。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70A_Authoring_DAG.md -->

# G70A — Authoring DAG

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

统一 ingest→parse→distill→fuse→domain→complete→scenario→compile→preview→evaluate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70B_Stage_policy.md -->

# G70B — Stage policy

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

每阶段 precondition/postcondition/retry/timeout/cost。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70C_Provider_routing.md -->

# G70C — Provider routing

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

按能力/隐私/成本/确定性选择 provider。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70D_Auto_loop.md -->

# G70D — Auto-loop

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

依据 gap/worldness 选择下一动作，不由自由聊天 Agent 控制。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70E_Stopping_criteria.md -->

# G70E — Stopping criteria

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

blocking gap、rights、worldness、uncertainty honesty。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70F_Budget_guard.md -->

# G70F — Budget guard

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

token/network/storage/time budgets。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70G_Crash_resume.md -->

# G70G — Crash resume

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

任意阶段中断恢复，不重复副作用。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G70H_M67_qualification.md -->

# G70H — M67 qualification

Milestone: **M67 — Autonomous Authoring Orchestrator**

## Objective

one command unattended reference authoring E2E。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G70H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71A_Impact_scoring.md -->

# G71A — Impact scoring

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

按 downstream impact/uncertainty/conflict/rights 排审核优先级。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71B_Auto_approval_policy.md -->

# G71B — Auto-approval policy

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

仅低风险、可撤销、非 rights/canon critical 项允许批量自动确认。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71C_Review_inbox.md -->

# G71C — Review inbox

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

用户只看真正需要处理的少量 items。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71D_Batch_review.md -->

# G71D — Batch review

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

approve/reject/merge/split/keep unknown。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71E_Impact_preview.md -->

# G71E — Impact preview

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

审核变更会影响哪些 entities/events/scenarios/package sections。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71F_Audit_provenance.md -->

# G71F — Audit provenance

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

人/AI/规则每次决定可追踪。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71G_Review_UX_E2E.md -->

# G71G — Review UX E2E

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

断线恢复、并发 revision conflict、撤销。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G71H_M68_qualification.md -->

# G71H — M68 qualification

Milestone: **M68 — Minimal Human Review / Active Review Studio**

## Objective

benchmark 中无需逐条点数千候选即可完成 publish gate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G71H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72A_One_click_book.md -->

# G72A — One-click book

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

合法 synthetic/public book → publishable package → living instance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72B_One_click_family.md -->

# G72B — One-click family

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

synthetic GEDCOM bundle → private family living preview。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72C_One_click_structured_world.md -->

# G72C — One-click structured world

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

JSON/CSV source bundle → living instance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72D_Mixed_source_world.md -->

# G72D — Mixed-source world

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

book+image+structured supplement bundle。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72E_Living_world_acceptance.md -->

# G72E — Living world acceptance

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

time advance/object persistence/knowledge isolation/autonomy/branch/replay。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72F_Studio_product_flow.md -->

# G72F — Studio product flow

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

Create→Auto Author→Review Required→Preview→Publish→Enter World。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72G_CLI_API_product_flow.md -->

# G72G — CLI/API product flow

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

单命令启动、status、resume、publish、instantiate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G72H_M69_qualification.md -->

# G72H — M69 qualification

Milestone: **M69 — One-click Source → Living World E2E**

## Objective

四条 E2E 全部生成证据与可回放 instance。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G72H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73A_Clean_room_clone.md -->

# G73A — Clean-room clone

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

全新 clone/bootstrap/migrate/test/sample authoring。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73A_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73B_Security_corpus_audit.md -->

# G73B — Security corpus audit

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

secret/private/rights/source cache/artifact publication。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73C_Performance_recovery.md -->

# G73C — Performance recovery

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

大书/并发 jobs/cache/restart/backup restore。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73C_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73D_Docs_SDK_examples.md -->

# G73D — Docs SDK examples

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

World Creation Quickstart、Provider SDK、Domain extension、rights guide。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73D_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73E_CI_matrix.md -->

# G73E — CI matrix

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

backend/frontend/package/e2e/security/architecture/source fixtures。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73E_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73F_GitHub_delivery.md -->

# G73F — GitHub delivery

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

push feature branch，读取 Actions 直到 required CI green。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73F_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73G_RC_release.md -->

# G73G — RC release

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

若权限/流程允许，tag v5.4.0-rc1 + GitHub Release Candidate。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73G_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: goals/G73H_M70_final_certification.md -->

# G73H — M70 final certification

Milestone: **M70 — Production Hardening / GitHub CI / v5.4 RC**

## Objective

生成最终矩阵、SHA、CI、release evidence，STOP。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G73H_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。


---

<!-- FILE: milestones/M51_QUALIFICATION.md -->

# M51 — Post-v5.3 Audit & Forge Baseline Qualification

## Required Goals

- G54A PASS
- G54B PASS
- G54C PASS
- G54D PASS
- G54E PASS
- G54F PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M51_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M52_QUALIFICATION.md -->

# M52 — Source Registry & Adapter Foundation Qualification

## Required Goals

- G55A PASS
- G55B PASS
- G55C PASS
- G55D PASS
- G55E PASS
- G55F PASS
- G55G PASS
- G55H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M52_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M53_QUALIFICATION.md -->

# M53 — Parse / Segment / Stable Locator Qualification

## Required Goals

- G56A PASS
- G56B PASS
- G56C PASS
- G56D PASS
- G56E PASS
- G56F PASS
- G56G PASS
- G56H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M53_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M54_QUALIFICATION.md -->

# M54 — Distillation & Candidate Fabric Qualification

## Required Goals

- G57A PASS
- G57B PASS
- G57C PASS
- G57D PASS
- G57E PASS
- G57F PASS
- G57G PASS
- G57H PASS
- G57I PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M54_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M55_QUALIFICATION.md -->

# M55 — Evidence / Rights / Review / Completion Core Qualification

## Required Goals

- G58A PASS
- G58B PASS
- G58C PASS
- G58D PASS
- G58E PASS
- G58F PASS
- G58G PASS
- G58H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M55_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M56_QUALIFICATION.md -->

# M56 — Domain Matching & WorldDraft Qualification

## Required Goals

- G59A PASS
- G59B PASS
- G59C PASS
- G59D PASS
- G59E PASS
- G59F PASS
- G59G PASS
- G59H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M56_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M57_QUALIFICATION.md -->

# M57 — World Compiler / Package / Preview Qualification

## Required Goals

- G60A PASS
- G60B PASS
- G60C PASS
- G60D PASS
- G60E PASS
- G60F PASS
- G60G PASS
- G60H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M57_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M58_QUALIFICATION.md -->

# M58 — Studio Create World Wizard + API / CLI Qualification

## Required Goals

- G61A PASS
- G61B PASS
- G61C PASS
- G61D PASS
- G61E PASS
- G61F PASS
- G61G PASS
- G61H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M58_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M59_QUALIFICATION.md -->

# M59 — Cross-source E2E / Hardening Qualification

## Required Goals

- G62A PASS
- G62B PASS
- G62C PASS
- G62D PASS
- G62E PASS
- G62F PASS
- G62G PASS
- G62H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M59_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M60_QUALIFICATION.md -->

# M60 — Book-scale Semantic World Understanding Qualification

## Required Goals

- G63A PASS
- G63B PASS
- G63C PASS
- G63D PASS
- G63E PASS
- G63F PASS
- G63G PASS
- G63H PASS
- G63I PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M60_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M61_QUALIFICATION.md -->

# M61 — Multi-source / Multi-version Fusion Qualification

## Required Goals

- G64A PASS
- G64B PASS
- G64C PASS
- G64D PASS
- G64E PASS
- G64F PASS
- G64G PASS
- G64H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M61_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M62_QUALIFICATION.md -->

# M62 — Multimodal & External Source Expansion Qualification

## Required Goals

- G65A PASS
- G65B PASS
- G65C PASS
- G65D PASS
- G65E PASS
- G65F PASS
- G65G PASS
- G65H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M62_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M63_QUALIFICATION.md -->

# M63 — Domain Inference / Composition / Gap Packs Qualification

## Required Goals

- G66A PASS
- G66B PASS
- G66C PASS
- G66D PASS
- G66E PASS
- G66F PASS
- G66G PASS
- G66H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M63_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M64_QUALIFICATION.md -->

# M64 — Constraint-backed Completion & Consistency Qualification

## Required Goals

- G67A PASS
- G67B PASS
- G67C PASS
- G67D PASS
- G67E PASS
- G67F PASS
- G67G PASS
- G67H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M64_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M65_QUALIFICATION.md -->

# M65 — Scenario / Genesis Auto Authoring Qualification

## Required Goals

- G68A PASS
- G68B PASS
- G68C PASS
- G68D PASS
- G68E PASS
- G68F PASS
- G68G PASS
- G68H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M65_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M66_QUALIFICATION.md -->

# M66 — Worldness Validation & Simulation Closure Qualification

## Required Goals

- G69A PASS
- G69B PASS
- G69C PASS
- G69D PASS
- G69E PASS
- G69F PASS
- G69G PASS
- G69H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M66_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M67_QUALIFICATION.md -->

# M67 — Autonomous Authoring Orchestrator Qualification

## Required Goals

- G70A PASS
- G70B PASS
- G70C PASS
- G70D PASS
- G70E PASS
- G70F PASS
- G70G PASS
- G70H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M67_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M68_QUALIFICATION.md -->

# M68 — Minimal Human Review / Active Review Studio Qualification

## Required Goals

- G71A PASS
- G71B PASS
- G71C PASS
- G71D PASS
- G71E PASS
- G71F PASS
- G71G PASS
- G71H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M68_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M69_QUALIFICATION.md -->

# M69 — One-click Source → Living World E2E Qualification

## Required Goals

- G72A PASS
- G72B PASS
- G72C PASS
- G72D PASS
- G72E PASS
- G72F PASS
- G72G PASS
- G72H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M69_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。


---

<!-- FILE: milestones/M70_QUALIFICATION.md -->

# M70 — Production Hardening / GitHub CI / v5.4 RC Qualification

## Required Goals

- G73A PASS
- G73B PASS
- G73C PASS
- G73D PASS
- G73E PASS
- G73F PASS
- G73G PASS
- G73H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M70_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。
