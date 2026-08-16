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
