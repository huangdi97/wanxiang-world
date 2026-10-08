# M89 — Long-Horizon Runtime + SimulationLOD Qualification

必须先完成：
- G92A Long-Horizon Scheduler
- G92B Background Simulation
- G92C Checkpoint / Resume / Crash Recovery
- G92D Snapshot / Compaction Policy
- G92E SimulationLOD Runtime
- G92F Resource / Cost Budget
- G92G 24h / 7d Long Run
- G92H 30d Qualification


## 共同架构铁律

- 当前 Source of Truth 是 v5.4-STABLE-R2 完整母版。
- Kernel / Reality Root / Commit / Ledger / Branch / Lineage stable semantics 默认冻结。
- 不创建第二套 Canonical State、Event Store、Branch、Package Registry、Source Registry、Candidate System。
- Experience/UI/Director/Agent/Provider 均不得拥有 Commit Authority。
- Narrative/visual/model output 只能是 Proposal/Candidate/Projection/Prediction。
- World Truth、Actor Belief、Memory、Rumor、Reflection 必须分离。
- World-specific 概念进入 Domain/World/Scenario/Experience，不进入 Kernel。
- Worldness ≠ Scientific Validity；ValidationStack 独立存在。
- 不训练自有 World Foundation Model / Video World Model。
- 不把 10k/100k LLM NPC 作为本轮目标；先做 SimulationLOD。
- 不上传私有 Source、版权原文、private family data、secret/token/model cache。
- 每个 persisted schema 变化必须有 migration/compatibility。
- TODO / placeholder / mock-only / hardcoded PASS 不算完成。
- 每 Goal PASS 后 commit并继续；Milestone FAIL 必须修，不要询问是否继续。


## Gate

- 运行本 Milestone 所有适用测试。
- 运行 v5.4 critical regression。
- 运行 architecture/Kernal freeze guard。
- 检查重复 abstraction / giant manager / hidden authority。
- 生成 `reports/M89_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。
