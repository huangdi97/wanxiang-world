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
