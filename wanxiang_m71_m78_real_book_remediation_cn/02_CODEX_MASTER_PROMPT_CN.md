# Codex Master Prompt — Real Book Remediation

继续当前 `wanxiang-world` 仓库。不要新建仓库，不要开始 v5.5，不要训练模型。

先读取仓库内 2026-08-25 `Real Book → Living World` NOT_ACCEPTED 报告，以及本执行包全部文件。把真实验收报告视为本轮 Source of Truth。

严格连续执行：
M71 G74A→G74G
M72 G75A→G75G
M73 G76A→G76J
M74 G77A→G77H
M75 G78A→G78H
M76 G79A→G79H
M77 G80A→G80H
M78 G81A→G81J

关键要求：
1. 第一优先级是解释并修复真实书 `0 candidates / coverage=0.0`；rights-approved 诊断仍 0，所以不要把 rights 当唯一根因。
2. Deterministic reference pipeline 不再承担“完整理解任意 30 万字中文小说”的虚假职责。
3. 真实语义理解使用可替换 Semantic Distillation Provider；不训练自有模型。
4. 优先复用现有 Provider/Capability Fabric；不得创建第二套 provider registry。
5. Provider 只能生成 Candidate，无 Commit 权。
6. 无 Provider 时返回明确 `SEMANTIC_PROVIDER_REQUIRED`；不得返回空候选假成功。
7. 有 Provider 时真实书必须产生非零且有 source locator 的 Candidate。
8. 修复 job terminal state、empty scenario、expected 500、coverage、review inbox。
9. WorldDraft→WorldPackage→Preview→Worldness→Living Instance 必须是真实闭环。
10. 补齐 CLI/API/browser Studio 用户生命周期。
11. 最终必须重新使用同一份原始本地私有书验收；不得修改原书、不得提交 Git、不得调用内部 helper 绕过产品面。
12. 每个 Goal：读代码→KEEP/EXTEND/MERGE/DELETE 分析→实现→tests→report→commit→自动继续。
13. 内部缺陷不得标 EXTERNAL_BLOCKED；只有真实第三方 Provider 凭证/用户权利声明/外部服务等才允许。
14. 只有最终真实验收报告变成 `ACCEPTED` 才允许 tag/release `v5.4.0-rc2`。
15. push 到现有 GitHub feature branch，查询真实 GitHub Actions；失败就修再 push，直到 required CI 全绿。
16. STOP，不进入下一阶段。
