# G90B — Prompt Genesis Contract

Milestone：**M87**

## Objective

把自然语言创作意图变成 E5 Candidate/WorldDraft，而不是直接 World Truth。

## Required Reading

- `README_FIRST.md`
- `00_MASTER_ROADMAP.md`
- `01_ARCHITECTURE_CONTRACTS.md`
- `02_PRODUCT_EXPERIENCE_SPEC.md`
- `03_LONG_HORIZON_EVOLUTION_SPEC.md`
- `04_WORLD_LAB_SPEC.md`
- `05_GITHUB_RELEASE_POLICY.md`
- `06_CODEX_MASTER_PROMPT_CN.md`
- 当前仓库 `STATUS.md / PLAN.md / CHANGELOG.md / reports/ / tests/ / migrations/ / OpenAPI / Studio / CI`
- v5.4 stable release evidence 和当前真实源码

## Implementation Tasks

1. CreatorIntent
2. constraint extraction
3. domain suggestions
4. E5 provenance
5. review gates


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


## Required Tests / Evidence

- prompt injection/data separation
- all generated facts marked E5

并执行所有适用的 unit / contract / property / integration / migration / replay / security / architecture / frontend E2E / lint / typecheck / build。

## Acceptance

- Scope 内部项真实实现。
- 真实产品链/长周期链有可复现 evidence。
- 无 authority bypass。
- 无 world-specific Kernel 污染。
- 无静默假成功。
- 更新 `reports/G90B_REPORT.md` 和 `reports/V55_ACCEPTANCE_MATRIX.md`。
- PASS 后 commit：`g90b: Prompt Genesis Contract`。
- 自动继续下一 Goal。
