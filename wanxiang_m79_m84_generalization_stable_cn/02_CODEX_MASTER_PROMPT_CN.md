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
