# M94 — v5.5 Certification Qualification

必须先完成：
- G97A Certification Matrix Freeze
- G97B Literary 30d/90d Certification
- G97C Non-literary Long-run Certification
- G97D Parallel Worldline Certification
- G97E Experience Product E2E
- G97F Security / Safety / Cost / Storage
- G97G Clean Clone + GitHub CI
- G97H v5.5.0-rc1 Release Gate
- G97I Final Evidence & Status
- G97J STOP


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
- 生成 `reports/M94_QUALIFICATION.md`。
- FAIL 必须修复，PASS 自动继续。
