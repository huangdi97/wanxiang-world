# Wanxiang M79–M84：Generalization & v5.4 Stable Certification

当前前置状态：

- M71–M78 已完成；
- 真实中文长书 Book → Living World 已 ACCEPTED；
- 同一真实书产生 3,918 节点/Segment、11,549 Candidates、coverage≈0.8333；
- WorldPackage / Preview / Worldness / Living Instance / Commit / Replay / Branch isolation 已通过；
- CLI/API/Studio 已打通；
- v5.4.0-rc2 已创建并且 required GitHub Actions 全绿（以当前仓库远端事实为准）。

本轮不扩 Kernel，不训练模型，不做 v5.5。

唯一目标：

> 证明 v5.4 的 Source → Living World 能力不是“只对一本书有效”，建立语义质量基准、Worldness 校准、Family/Structured/Mixed Source 泛化证据，并在全部通过后发布 v5.4.0 stable。


---

# M79–M84 Master Roadmap

## M79 — Second Real Book Generalization
换一本真实书，尽量换格式/文风/结构，完整走 Book → Living World。

## M80 — Semantic Quality Benchmark
建立人工抽样 Gold Set，评估 Identity/Alias/Event/Relation/Place/KnowledgeBoundary/Evidence 质量，而不是只看 candidate_count。

## M81 — Worldness Calibration & Adversarial Validation
验证 Worldness 真能识别坏世界，不允许“接口全通就接近 1.0”。

## M82 — Real Family World
使用本地私有 GEDCOM（可加少量照片 metadata/地点/事件）真实创建 Family Living World，证明不是 Novel Engine。

## M83 — Structured & Mixed Source Generalization
用 JSON/CSV 构建 Structured World，再验证 Book + JSON/CSV/Map metadata 多来源融合为 ONE WorldDraft。

## M84 — v5.4 Stable Certification
clean clone、全量 CI、回归、rights/security、第二本书/Family/Structured/Mixed 全通过后，才创建 v5.4.0 stable release。


---

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


---

# Codex Master Prompt — M79–M84

继续当前 `wanxiang-world` 仓库。

前置事实：
- M71–M78 已 ACCEPTED；
- 第一份真实中文长书已完成 Source → Living World；
- v5.4.0-rc2 已存在且 CI 全绿（以当前 remote 为准）。

不要重跑 M51–M78，不重新设计 Kernel，不训练模型。

严格执行：
M79 G82A–G82G
→ M80 G83A–G83H
→ M81 G84A–G84F
→ M82 G85A–G85G
→ M83 G86A–G86G
→ M84 G87A–G87H

规则：
1. 第二本书必须是真实独立 Source，不得为了 PASS 换成 synthetic。
2. 私有 Source 不进 Git。
3. 质量不再用 candidate_count 代替。
4. 建立 Semantic Quality Benchmark。
5. Worldness 必须经 adversarial calibration。
6. Family 必须走同一 Kernel/Forge/Runtime。
7. Structured/Mixed Source 必须收敛为 ONE WorldDraft。
8. LLM/local model 仍只是 Provider，无 Commit Authority。
9. 不训练模型。
10. 每 Goal：实现→测试→报告→commit→继续。
11. 最终 GitHub required CI 不绿就继续修。
12. 只有全部 Generalization Gate PASS 才创建 v5.4.0 stable。
13. 发布后 STOP。


---

# 用户需要做什么

## 必做 1：准备第二本真实书

推荐：
- 与第一本不同作者/文风；
- 最好格式也不同；
- 优先 EPUB，其次 DOCX/TXT/MD；
- 不需要上传 GitHub，只放本机。

把本地路径告诉 Codex，例如：
`D:\books\second_book.epub`

并明确：
- 允许本地私有解析：是/否
- 允许发送到当前 semantic provider：是/否
- 允许打包进本地 WorldPackage：是/否
- 允许公开原文：通常否
- 允许训练：默认否

## 必做 2：准备一个 GEDCOM

可以是真实家谱导出，也可以是你自己创建的测试家谱。真实家谱必须 private/local，不进 public Git。

路径例如：
`D:\family\my_family.ged`

如果暂时没有 GEDCOM：可以让 Codex 先做 M79–M81 和 M83，M82 标记 USER_INPUT_REQUIRED，不能伪造“真实 Family 验收”。

## 必做 3：准备结构化测试数据

最简单三份即可：
- people.csv
- places.csv
- events.csv 或 events.json

可以自己构造 10–50 条，不涉及隐私。

## 其余不用你做

Codex 应自动完成：代码修改、benchmark、tests、Studio/API/CLI、Git commits、push、GitHub Actions、修 CI、reports、stable tag/release。

仅当 GitHub 再次要求授权、semantic provider 需要凭证/确认、Family privacy/rights 需要授权选择时，才需要你人工介入。


---

# M79–M84 Final Acceptance

v5.4.0 stable 前必须同时满足：

1. 第一份真实书验收仍 PASS；
2. 第二本真实书 Source → Living World PASS；
3. 第二本书不是 source-specific hack；
4. Semantic Quality Benchmark 已建立；
5. Identity/Alias quality 有量化结果；
6. Event/Temporal quality 有量化结果；
7. Relation/Place/Org quality 有量化结果；
8. Knowledge Boundary 有量化/抽样结果；
9. Evidence traceability PASS；
10. Worldness adversarial calibration PASS；
11. 坏世界显著低于正常世界；
12. Worldness 不由 endpoint 成功硬编码；
13. preview/publish/living threshold 分离；
14. Real Family GEDCOM → Family World PASS，若用户未提供则 stable 不得声称 Family real validation；
15. living-person privacy gate PASS；
16. Structured JSON/CSV World PASS；
17. Mixed Source Bundle PASS；
18. 多来源最终 ONE WorldDraft；
19. Source conflict/provenance 不丢；
20. clean clone PASS；
21. full CI PASS；
22. security/rights PASS；
23. private/版权 Source 未入 Git；
24. remote SHA == local HEAD；
25. working tree clean；
26. GitHub required Actions success；
27. `v5.4.0` annotated tag 创建；
28. GitHub stable Release 创建；
29. clean install from tag PASS；
30. STOP，不进入 v5.5。


---

继续当前 `wanxiang-world` 仓库。

当前 M71–M78 已完成，真实中文长书 Source → Living World 已 ACCEPTED，v5.4.0-rc2 与 required CI 已完成。不要重新执行 M51–M78，不训练模型，不进入 v5.5。

完整读取本执行包：
README_FIRST.md
00_MASTER_ROADMAP.md
01_M79_M84_GOALS.md
02_CODEX_MASTER_PROMPT_CN.md
03_USER_ACTIONS.md
04_FINAL_ACCEPTANCE.md
以及仓库当前 STATUS/PLAN/CHANGELOG/reports/tests/OpenAPI/CLI/Studio/CI。

然后严格执行 M79–M84。

如果用户尚未给第二本真实书路径或 GEDCOM 路径：
- 不要伪造真实验收；
- 继续完成所有不依赖该输入的内部工程与 benchmark 基础设施；
- 将唯一缺失输入标为 USER_INPUT_REQUIRED；
- 一旦用户提供路径，从 checkpoint 继续，不重复已完成工作。

当路径已经提供：
- 原始文件只作为 private local source；
- 不复制进 Git；
- 不修改；
- 不走 source-specific shortcut；
- 完整执行真实 E2E。

最后只有 M79–M83 全部 PASS 才创建 v5.4.0 stable，GitHub required Actions 必须全绿；发布后 STOP。
