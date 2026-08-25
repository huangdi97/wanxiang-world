# Wanxiang M71–M78 Real Book → Living World 验收驱动修复

本包针对 2026-08-25 真实中文长书验收 `NOT_ACCEPTED`。

已确认问题：真实 323,815 字中文 TXT 能产生 WorldDraft，但 `candidate_count=0 / coverage=0.0`；即使 rights-approved 诊断变体仍为 0，因此核心根因在**真实长书语义蒸馏链未工作**，而不是 rights gate。其后 WorldPackage、Preview、Worldness、Living World 都没有真实输入。

本轮目标不是 v5.5 扩张，也不是训练模型，而是：

> 让当前 Wanxiang v5.4 RC 在不修改原书、不写书名专用逻辑、不绕过产品 API、不伪造 Candidate 的情况下，真实完成中文长书 → Candidates → WorldDraft → WorldPackage → Preview → Worldness → Living World Instance。

核心原则：
- Kernel/Commit/Ledger/Branch/Lineage 继续冻结。
- 不训练自有模型。
- Deterministic pipeline 负责 parse/segment/locator/CI/reference baseline，不假装能完整理解任意长篇文学。
- 真正语义理解通过可替换 Semantic Distillation Provider；现成 LLM、本地模型或未来 NLP Provider 都只是 Capability Provider。
- Provider 输出只能进入 Candidate，永远无 Commit 权。
- 无 Provider 时必须明确 `SEMANTIC_PROVIDER_REQUIRED`，不能继续显示模糊 `draft has zero coverage` 或空结果假成功。
- 私有原书绝不提交 Git。
