# M79–M84 Goals

## M79 — Second Real Book Generalization

### G82A 第二本真实书 Source Gate
- 读取用户指定第二本真实书；
- 不修改原文件；
- 不复制进 Git；
- 记录 raw bytes/hash 仅本地证据；
- 明确 private analysis / model-processing / package / public-export rights。

### G82B Format/Structure Generalization
- 尽量使用与第一本不同格式（优先 EPUB/DOCX；若只有 TXT 也可）；
- 验证 chapter/section/segment/locator；
- 禁止书名/作者专用 parser hack。

### G82C Semantic Distillation Generalization
- 使用同一 SemanticDistillationService；
- candidate kinds、provider provenance、locator 均真实；
- 禁止 source-specific if/else。

### G82D Cross-chapter Identity/Alias
- 专门检查同人多称谓、同名异人、跨章 alias；
- 自动 merge 只能是可撤销 suggestion；
- 记录 merge precision 样本。

### G82E Event/Time/Place/Relation Generalization
- 验证事件、时间不确定性、地点、关系、组织和对象；
- 叙述顺序不得直接等于事件顺序。

### G82F Second Book → Living World E2E
- Source → Candidates → Draft → Package → Preview → Worldness → Living Instance；
- Commit / Replay / Branch isolation。

### G82G M79 Qualification
- 第二本真实书 ACCEPTED；
- 若失败，保留真实失败并修，不得换书规避。

## M80 — Semantic Quality Benchmark

### G83A Gold Sampling Protocol
从真实书 Candidates 中进行：随机抽样、高影响抽样、低置信抽样、冲突/merge 抽样。

### G83B Identity/Alias Benchmark
至少评估：Identity precision、Alias merge precision、False merge rate、Duplicate rate、Missing-evidence rate。

### G83C Event/Temporal Benchmark
至少评估：Event precision、participant correctness、temporal ordering、uncertainty honesty、narration-vs-event distinction。

### G83D Relation/Place/Organization Benchmark
评估 relation/place/organization precision 与 evidence traceability。

### G83E Knowledge Boundary Benchmark
检查人物不会知道未观察信息；speech/rumor/belief 不直接升为 truth；future knowledge leakage。

### G83F Evidence Traceability Benchmark
所有 sampled accepted candidate：Candidate → Evidence → Locator → Source 必须可回溯。

### G83G Benchmark Regression Suite
把匿名化/合成后的质量用例固化为 regression；不得提交原书版权文本。

### G83H M80 Qualification
生成 `reports/SEMANTIC_QUALITY_BENCHMARK.md`，不得只写 candidate_count。

## M81 — Worldness Calibration

### G84A Worldness Formula Audit
逐维解释当前 Worldness：persistence、identity、temporal、spatial、causality、epistemic isolation、object persistence、evidence traceability、uncertainty honesty、replay/branch readiness。

### G84B Adversarial Broken Worlds
构造受控坏世界：teleportation、secret leakage、duplicate object、temporal reversal、unsupported fact、replay mismatch、identity split/merge corruption。

### G84C Sensitivity Calibration
坏世界必须显著降分；修复后分数应恢复。

### G84D Anti-Gaming Guards
禁止 endpoint 成功直接加分、固定默认 0.99、缺失维度自动满分。

### G84E Threshold Policy
区分 previewable / publishable / living-ready，而非一个总分包打天下。

### G84F M81 Qualification
生成 Worldness calibration report + adversarial evidence。

## M82 — Real Family World

### G85A Private GEDCOM Source Gate
- 使用用户本地 GEDCOM；
- 不进入 Git；
- living-person privacy 默认高保护。

### G85B GEDCOM → Family Candidates
真实抽取 Person、Household/Family、Kinship、Birth/Marriage/Death、Residence/Migration、Places、Sources。

### G85C Claim Conflict Preservation
同一人生事件多来源冲突不得 last-write-wins。

### G85D Consent/Privacy/Legacy
验证 allowed_viewers、generation、training、export、posthumous、biometric/voice likeness。

### G85E Family WorldDraft/Package
推荐并组合 Family/Kinship/LifeHistory 相关 Domain；形成 WorldDraft、Package、Preview。

### G85F Family Living World
至少验证时间轴、人物/地点、迁徙/人生事件、Evidence；Branch 不污染 Evidence history。

### G85G M82 Qualification
证明同一 Kernel/Forge/Runtime 能创建 Family Living World。

## M83 — Structured & Mixed Source

### G86A Structured Source World
用 JSON/CSV 创建 entities、places、organizations、events、relations，形成 WorldDraft/Package/Preview。

### G86B Structured Locator/Evidence
JSON Pointer / CSV row+column locator 可回源。

### G86C Mixed Source Bundle
至少组合一份 Book Source、一份 JSON/CSV supplement、可选 map metadata，形成 ONE source bundle。

### G86D Cross-source Identity Alignment
同一实体在不同 Source 中对齐；冲突保留 provenance。

### G86E Cross-source Conflict
support/contradict/refine/alternative 不被覆盖。

### G86F ONE WorldDraft
多来源最终仍产出一个 WorldDraft，不是平行世界数据库。

### G86G M83 Qualification
Structured + Mixed Source 两条均 PASS。

## M84 — v5.4 Stable Certification

### G87A Clean Clone Certification
从 GitHub clean clone：install → migrate → bootstrap → tests → Studio/CLI/API smoke。

### G87B Full Regression
包括 v5.3 critical、M51–M78、M79–M83、package/replay/branch、security/rights。

### G87C Source Safety
确认无真实版权书籍原文、private GEDCOM、照片/身份证/私有数据、token/.env/db/model cache。

### G87D Stable Release Notes
准确写明已验证范围、不保证任意 Source 100% 自动正确、model provider optional/replaceable、evidence/review/uncertainty boundaries。

### G87E GitHub Delivery
push final branch；required Actions 全绿；remote SHA == local HEAD；working tree clean。

### G87F v5.4.0 Stable Tag
仅在 M79–M83 全部 PASS 后：annotated tag `v5.4.0`、push tag、GitHub Release（非 prerelease）。

### G87G Post-release Verification
验证 tag SHA、release artifact、clean install、quickstart、CI/release workflow。

### G87H STOP
完成后 STOP，不自动进入 v5.5，不训练模型。
