# 新 Agent 开头：Wanxiang R7 全量连续执行

我继续做 Wanxiang / 万相。请把以下两个文件作为本轮执行入口：

1. `万相世界_v5.5-RC1-R7_Cordis_Native_Versioned_Reality_Profile_完整母版_截至2026-09-24.md` —— 当前唯一 canonical design master。
2. `WANXIANG_R7_FULL_EXECUTION_GOAL_2026-09-25.md` —— 当前唯一全量连续执行 Goal。

不要从旧版本重新推断，不要只做规划，也不要假设 R7 已实现。

先只读核验真实仓库 HEAD、branch、worktree、tags、release、CI、STATUS、PLAN、BLOCKERS、V55 Stable acceptance/release evidence。真实 repo evidence 高于文档里的旧状态。

本轮用户已明确授权：如果 `v5.5.0` Stable 尚未收口，先真实完成 M95-R / 真人 Gate / Gate79/80 / Stable；完成后不再因旧 Goal 的 STOP 规则结束，而继续实现 R7，但仍不得自动命名/发布 v5.6。

R7 核心方向：直接采用 Cordis 作为第一代 Composition Runtime；Reality 通过 Versioned RealityProfile + versioned service seams + replaceable providers 组合；Worldline pin RealityProfile / WorldProfile / RuntimeLock；Cordis Context 只承载 capability graph，不承载 canonical world state；Cordis reversible effect 不得撤销 committed world history；Authority/CommitCapability 必须显式且普通插件不可获得 canonical write；DSH 优先通过 SDK/JSON-RPC 独立 Provider 接入；不可信/第三方/生成能力进入隔离 Execution Fabric；Paper2Agent 思路进入 Capability Foundry；RealityProfile major upgrade 必须 checkpoint + shadow replay + migrate/fork。

按 Goal 连续执行，不要每阶段问下一步。每完成一阶段：测试 → evidence → STATUS/PLAN/BLOCKERS → coherent commit → 自动进入下一个未 PASS Gate。只在真实真人/secret/外部基础设施 blocker 时暂停，且不得伪造 PASS。

现在开始执行，不要只回复方案。
