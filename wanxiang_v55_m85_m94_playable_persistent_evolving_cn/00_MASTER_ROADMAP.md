# v5.5 M85–M94 Master Roadmap

## M85 — Playable World Experience Shell
把 v5.4 的 WorldPackage / Living Instance 变成普通用户可以“选世界 → 选角色/创建角色 → 进入 → 自由行动 → 看见后果”的产品。

## M86 — Character / Goal / Memory / StateDiff
建立长期人物连续性：ActorGoalStack、EpistemicMemory、Belief revision、Goal reprioritization、Relationship state 与 Character Passport。

## M87 — World Workshop + Prompt Genesis + Publishing
把 Studio 从 Source Importer 扩展为 World Creator：From Source / From Prompt / Hybrid，保持 E0–E5、Rights、Provenance；支持 ExperiencePackage 与发布边界。

## M88 — World Pressure / Opportunity / Director Modes
建立 PressureProfile、Opportunity/Challenge 和 CANON / DIRECTED / LIVING / EXPERIMENT 模式；Director 只能提出 Proposal，不拥有 Commit 权。

## M89 — Long-Horizon Runtime + SimulationLOD
让世界真正跑 24h / 7d / 30d / 90d，并支持 selected 1-year accelerated；解决 scheduler、background simulation、checkpoint、compaction、recovery、LOD 和成本预算。

## M90 — Actor / Relationship / Organization Evolution
把 State / Belief / Relationship / Capability / Persona / Organization 变化分离，形成可追溯、可解释、可回滚的长期演化。

## M91 — Emergence / Institution / Culture
把 Event → Pattern → Habit → Norm → Institution → World Structure 变成 evidence-backed Candidate / Promotion 管线，而不是自动宣布“涌现”。

## M92 — World Laboratory
提供 WorldRunArtifact、Experiment Registry、fork/replay/intervention、batch worldlines、multi-provider/mixed-population 比较和 ValidationProfile。

## M93 — Physical / Visual World Provider Bridge
实现外部物理/视觉世界 ABI；Semantic Canonical Reality 与视觉/物理 rollout 严格分离；至少有可测试 reference provider，不以外部大模型为 CI 硬依赖。

## M94 — v5.5 Certification
真实产品 + 长周期 + Evolution/Emergence + Lab + clean-room/CI。只有全部关键 Gate 通过才允许发布 `v5.5.0-rc1`，否则保持 NOT_ACCEPTED。
