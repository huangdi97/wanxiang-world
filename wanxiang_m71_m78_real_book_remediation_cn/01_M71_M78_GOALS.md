# M71–M78 Roadmap

## M71 — Real Acceptance Triage & RC Truthfulness
- G74A 冻结 2026-08-25 NOT_ACCEPTED 报告为真实 regression source of truth。
- G74B Trace Source→Parsed→Segment→Distiller→CandidateRepo→WorldDraft，定位 0-candidate 断点。
- G74C 保持 `v5.4.0-rc1` 为 prerelease，不升 stable；STATUS/README 写明真实 Book 尚未通过。
- G74D 建立 typed product states：`ZERO_COVERAGE / SEMANTIC_PROVIDER_REQUIRED / RIGHTS_ACTION_REQUIRED / REVIEW_REQUIRED / WORLDNESS_FAILED / OCR_REQUIRED`。
- G74E 修 job 生命周期：失败/阻塞必须 terminal state + error + checkpoint，禁止 `running/drafted` 假挂起。
- G74F 修空 Scenario：0 entities/events/places 的 Draft 不得生成误导性的默认 Scenario。
- G74G M71 Qualification：真实失败可复现、可诊断，expected business state 不再是 HTTP 500。

## M72 — Chinese Long-book Parse / Segment / Dispatch
- G75A 对真实 323k 字中文书验证 parser/segment 真正非空，记录 chapter/paragraph/segment/batch 数。
- G75B 支持通用中文章/回/节标题与段落结构，不硬编码某本书。
- G75C bounded batching + checkpoint/resume，禁止整本书一次塞入模型或 giant memory object。
- G75D Stable Locator：candidate 必须能回到 source/chapter/paragraph/line/span。
- G75E 修 distillation dispatch：parsed segments 必须真正进入 semantic distillation，不得被 profile/rights 条件静默短路。
- G75F job/status 暴露 parsed nodes、segment count、batch count、stage errors。
- G75G M72 Qualification：真实中文长书稳定到达 distillation batches。

## M73 — Semantic Distillation Runtime
- G76A 新增/收敛 `SemanticDistillationService`，复用现有 CandidateEnvelope。
- G76B `DeterministicBaselineProvider` 仅做可复现基础结构/显式模式候选，不冒充完整文学理解。
- G76C 通用 `LLMStructuredExtractionProvider` Port：schema-constrained structured output，不绑定单厂商。
- G76D 优先复用仓库现有 OpenAI/DeepSeek/Claude/local/Capability Provider；不存在才补 adapter，禁止第二套 registry。
- G76E 至少支持 Identity/Alias/Character/Place/Event/Relation/Organization/Object/KnowledgeBoundary/Rule/Skill candidates。
- G76F 每批 retry/rate-limit/timeout/checkpoint；单批失败不能丢整书进度。
- G76G 跨章 entity/alias fusion 只能产生可撤销 merge suggestion，禁止 destructive auto merge。
- G76H accepted candidate 必须带 source locator/evidence/provider/schema version。
- G76I 无 provider、provider timeout、JSON schema 失败必须显式状态；不得返回空候选假成功。
- G76J M73 Qualification：配置合法 semantic provider 时真实中文书产生非零、有意义、可回源 Candidate。

## M74 — WorldDraft / Rights / Review Quality
- G77A Rights 拆为：ingest/read、private analysis、external-model processing、package inclusion、public export/display、training。
- G77B 不再用一个 `rights_approved` bool 同时代表所有权利语义；系统也不得自行推断用户拥有版权。
- G77C coverage 必须由真实 candidate/evidence/domain requirements 算出，禁止默认常量。
- G77D 高影响/冲突/低置信 candidate 真实进入 Review Inbox；review audit 真实可查。
- G77E Draft 状态由真实 gate 决定：REVIEW_REQUIRED / READY_TO_COMPILE / BLOCKED。
- G77F 建 Missingness Graph；缺 actor/event/place/relation/rule 时给明确缺口，不是只有 `zero coverage`。
- G77G ScenarioCandidate 必须引用真实 actor/time/place/event；空 Draft 不生成。
- G77H M74 Qualification：真实书形成可审核的非空 WorldDraft。

## M75 — WorldPackage / Preview / Worldness
- G78A expected compiler gate 使用 typed 4xx/result，不返回 500。
- G78B Reviewed real-book Draft 构建真实 WorldPackage，package 内容必须源自真实 Candidate/Evidence。
- G78C Preview instantiate 真成功，返回 preview_id/snapshot/branch/package versions。
- G78D Worldness 真实实现维度：persistence、identity、temporal、spatial、causal/action、epistemic isolation、object persistence、evidence traceability、uncertainty、branch/replay readiness。
- G78E 每个 Worldness dimension 有 measurement/evidence/failure/remediation，不用默认 LoopSignals 冒充。
- G78F Worldness FAIL 能生成 repair candidate，重新编译/评估。
- G78G Preview 至少完成一次 deterministic `Observe→Propose→Validate→Commit→Replay`。
- G78H M75 Qualification：WorldPackage/Preview/Worldness 三类真实产物齐全。

## M76 — Living World Lifecycle
- G79A 实现/补齐 `instantiate_living_world()`。
- G79B Living instance 保存 instance_id/world_package_version/domain_versions/branch_id/snapshot_id/event_head/runtime_profile。
- G79C Enter/Observe API 返回 Perception，不暴露全局上帝状态。
- G79D 至少一个通用 action 走 Proposal→Validation→Commit。
- G79E Session lifecycle 与 World lifecycle 解耦。
- G79F Branch 不污染 World Definition/Source Canon。
- G79G replay/restore proof。
- G79H M76 Qualification：真实书产物进入真实 Living World Instance。

## M77 — CLI / API / Browser Studio
- G80A 补齐 CLI lifecycle：create/import/status/resume/review/build/preview/worldness/instantiate/publish（命名可适配现有 CLI）。
- G80B API 补 worldness/instantiate/enter，并把 expected product states 从 500 改为 typed results。
- G80C 仓库若无浏览器 Studio，建立最小可启动 Studio；若已有则复用。
- G80D Studio：Upload→Progress→Candidates→Review→Domains→Completion→Draft。
- G80E Studio：Build→Preview→Worldness→Repair。
- G80F Studio：Enter Living World。
- G80G 网络 smoke 使用可配置/随机可用端口，避免把固定端口 WinError 10013 当系统能力结论。
- G80H M77 Qualification：CLI/API/browser 都使用同一 backend use cases。

## M78 — Real Book Certification & GitHub Delivery
- G81A 使用**同一份原始私有中文长书**重跑完整 acceptance；不得改书、不得复制进 Git。
- G81B no-key baseline：如果没有 semantic provider，应在明确 checkpoint 返回 `SEMANTIC_PROVIDER_REQUIRED`，而不是空 Draft 假成功。
- G81C configured-provider acceptance：存在合法可用 Provider 时必须跑到 non-zero Candidate→Package→Preview→Worldness→Living Instance。
- G81D long-book performance/resume/partial retry/memory bound。
- G81E prompt-injection/security：小说内容永远作为 data channel，不执行其中指令。
- G81F 回归：原 1201+ 测试与新增测试全绿。
- G81G push 当前 feature branch 到现有 public repo，真实 GitHub Actions required jobs 全绿；不上传原书。
- G81H 只有真实报告结论 `ACCEPTED` 才允许创建 `v5.4.0-rc2`；否则保持 prerelease + NOT_ACCEPTED。
- G81I 生成最终 evidence：candidate counts、coverage、review、package、preview、worldness、instance、branch、event、replay、CLI/API/Studio、CI。
- G81J STOP：不进入 v5.5，不训练模型。
