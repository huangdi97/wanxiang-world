# Wanxiang / 万相 R7 全量连续执行 Goal
## Cordis-Native Composition Runtime + Versioned RealityProfile + Capability/Execution/Experience 全链收口

> **适用对象**：Codex / OpenCode / Claude Code / WorkBuddy / 其他可持续执行编码 Agent  
> **Canonical Design Source of Truth**：`万相世界_v5.5-RC1-R7_Cordis_Native_Versioned_Reality_Profile_完整母版_截至2026-09-24.md`  
> **Goal 日期**：2026-09-25  
> **执行模式**：连续执行、证据驱动、根因修复、不得伪造 Gate、不得以 TODO/Mock 冒充完成  
> **用户新增授权**：本 Goal 明确授权在完成 v5.5 Stable 收口后继续执行 R7 设计实现，不因旧文档中的“Stable 后 STOP”而结束；但**不得因此自动把软件版本命名为 v5.6、不得创建 v5.6 tag/release、不得声称 R7 已完成，直到本 Goal 的 Definition of Done 全部满足**。

---

# 0. 任务定义

你不是来“做几个 Cordis demo”或“补几个接口”的。

你的任务是：

> **在不破坏现有 v5.4/v5.5 历史证据、不伪造真人/外部证据、不进行 Big Bang Rewrite 的前提下，把当前 Wanxiang 从已有 Playable/Persistent/Evolving World OS 工程，渐进迁移并收敛到 R7 canonical architecture：Cordis 作为第一代 Composition Runtime；Worldline 绑定 Versioned RealityProfile / WorldProfile / RuntimeLock；历史、分支、证据、权利、Actor、执行、Forge、Experience 等能力通过 versioned service seams + replaceable providers 组合；canonical write 由显式 Authority/CommitCapability 守住；不可信/重计算能力进入隔离 Execution Fabric；DSH 作为独立 Agent Harness Provider；Paper2Agent 思路进入 Capability Foundry；世界历史与插件生命周期彻底分离。**

最终交付必须是一个：

- 可构建；
- 可测试；
- 可回放；
- 可迁移；
- 可扩展；
- 可审计；
- 中文玩家主链可用；
- clean-clone 可复现；
- 有完整设计/运行/发布证据；
- 没有用假 evidence 过 Gate；

的 Wanxiang R7 工程实现基线。

---

# 1. 开始前：真实仓库只读核验

不要根据本 Goal 或设计文档推测仓库已经做到什么程度。

第一步只读执行，并把结果写入：

`reports/r7/00_REPO_BASELINE.md`

至少核验：

```text
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git log --oneline --decorate -n 30
git tag --list --sort=-creatordate
git remote -v
```

读取实际存在的：

```text
AGENTS.md
README.md
STATUS.md
PLAN.md
BLOCKERS.md
V55_FINAL_RELEASE_REPORT.md
V55_STABLE_ACCEPTANCE_MATRIX.md
V55_STABLE_RELEASE_REPORT.md
M95 / M100 / release / gate reports
pyproject.toml
package.json / pnpm-workspace.yaml
docker-compose*.yml
.github/workflows/*
当前 architecture/spec/ADR 文档
```

核验：

```text
当前 HEAD
当前 branch
worktree clean/dirty
local/remote divergence
v5.4.0 tag/release
v5.5.0-rc1 tag/release
是否已经存在 v5.5.0 Stable
M95-R 是否已经实现
Gates 62–66 是否有人类证据
Gate79/80 是否已经 PASS
当前 CI
当前测试数量
当前真实 blocker
```

## 1.1 状态优先级

发生冲突时：

```text
真实 repo / git / CI / machine-readable artifacts
>
最新 authoritative qualification report
>
R7 canonical design master
>
旧设计 / 旧截图 / 旧聊天
```

设计文档说明“应该怎样”；仓库证据说明“已经怎样”。

## 1.2 禁止事项

- 不把 DESIGN/PLANNED 写成 IMPLEMENTED；
- 不因目录/类名存在就判定功能完成；
- 不因旧 PASS 就假设当前 HEAD 仍 PASS；
- 不删测试、降阈值、改 Gate 定义来过关；
- 不覆盖历史失败证据；
- 不 force push；
- 不改写已发布 tag；
- 不泄露 secrets；
- 不把 synthetic evidence 冒充真人/真实世界 evidence。

---

# 2. 总架构约束

R7 目标架构：

```text
USER / AGENT / EXTERNAL SYSTEM
              │
              ▼
Experience / Application / Distribution
              │
              ▼
Domain / Forge / Simulation / Capability
              │
              ▼
Versioned WORLD REALITY PROFILE
identity · observe · proposal · policy · authority
history · branch · lineage · evidence · rights · replay
              │
              ▼
WANXIANG BASE BUNDLE
WorldScope · Profile · RuntimeLock · SchemaRegistry
CapabilityBroker · AuthorityBootstrap · MigrationCoordinator
              │
              ▼
CORDIS
Context · Service · Inject · Fiber · Effect · Scope
Dependency · Lifecycle · Composition
        ┌─────┴─────┐
        │           │
Trusted plugins   External Execution Plane
                  proc / Wasm / container /
                  microVM / VM / GPU / remote
                        │
                  Python / DSH / Sim
```

## 2.1 永久不得混淆

```text
Cordis Effect        != World Event
Plugin Unload        != Undo Committed History
Cordis Context       != Canonical World State
Execution Success    != Canonical World Truth
ExecutionTrace       != World History
Sandbox Snapshot     != World Branch
Agent/LLM Output     != Commit
World                != Experience != Projection != Distribution
```

## 2.2 Everything is composable，不等于 Everything is trusted

插件分层：

```text
A. Trusted in-process Cordis plugins
B. Trusted out-of-process providers
C. Untrusted / third-party / generated capabilities
D. External systems with irreversible side effects
```

B/C/D 不得因“是插件”而拥有 canonical DB credential 或 commit capability。

---

# 3. 连续执行状态机

除非遇到真正需要人类/凭据/外部基础设施的 blocker，否则不要每做一点就询问用户。

```text
DISCOVER
→ BASELINE
→ CLOSE_V55_IF_NEEDED
→ R7_SPIKE
→ R7_CONTRACTS
→ R7_BASE_BUNDLE
→ R7_READ_PATH
→ R7_HISTORY_BRANCH_REPLAY
→ R7_AUTHORITY
→ R7_EXECUTION
→ R7_DSH
→ R7_CAPABILITY_FOUNDRY
→ R7_REALITY_MIGRATION
→ R7_EXPERIENCE_APPLICATION
→ R7_REFERENCE_WORLDS
→ R7_OBSERVABILITY_OPS
→ R7_FULL_QUALIFICATION
→ CLEAN_CLONE
→ DOCS_AND_EVIDENCE
→ FINAL_R7_CLOSURE
```

遇到 blocker：

```text
能修复 -> 修复
环境缺失但有等价本地路径 -> 用等价路径并明确证据边界
必须真人 -> 生成完整人工包，状态 HUMAN_INPUT_REQUIRED
必须 secret/账号/付费资源 -> EXTERNAL_BLOCKED，继续执行不依赖它的其他工作
无法证明 -> NOT_PROVEN
```

禁止把 `HUMAN_INPUT_REQUIRED / EXTERNAL_BLOCKED / NOT_PROVEN` 改写成 PASS。

---

# 4. Phase 0 — v5.5 Stable 优先

如果 `v5.5.0` Stable 已真实发布，核验证据后记录：

`V55_STABLE = VERIFIED_EXISTING`

不要重发，不改 tag，直接进入 Phase 1。

如果尚未 Stable：

```text
M95-R remediation
→ genuine human M95 acceptance
→ Gates 62–66
→ freeze final v5.5 candidate SHA
→ SHA-sensitive regressions
→ candidate branch push (no force)
→ required remote CI exact SHA green
→ Gate79 PASS
→ Gate80 predicate PASS
→ annotated tag v5.5.0
→ stable release
→ post-release verification
```

### 真人 Gate

AI 不允许代替真人填写：

```text
tester identity
ratings
confusion notes
human acceptance
```

如果唯一 blocker 是真人测试：

1. 启动真实本地 build；
2. 生成中文玩家测试包；
3. 给出浏览器 URL、推荐世界、角色和逐步路径；
4. 状态写为 `WAITING_HUMAN_M95`；
5. 不伪造 PASS；
6. 继续所有不依赖真人结论的工作。

用户本轮已明确授权：**v5.5 Stable 完成后继续执行 R7，不因旧文档中的 STOP 规则结束；但仍不得自动进入 v5.6 release identity。**

---

# 5. Phase 1 — Cordis Architecture Spike

禁止先重构整个仓库。

建立或核验：

`experiments/cordis-world-kernel/`

只实现最小闭环：

```text
Cordis
+ WorldProfile
+ RealityProfile
+ RuntimeLock
+ history-memory
+ authority-default
+ actor-rule
```

流程：

```text
Actor
→ Proposal
→ Policy
→ Authority
→ Commit
→ History revision
```

必须通过：

### S1 100 commit continuity
- 连续至少 100 次 Commit；
- revision 单调增长；
- 无静默覆盖；
- final state 可由 history 重建。

### S2 Actor unload continuity
- 卸载 actor-rule 后 history 不变；
- history head 不倒退；
- Cordis runtime effects 被清理；
- committed history 不被清理。

### S3 Actor replacement
- mount actor-rule-v2 后从同一 worldline 当前 revision 继续；
- 不创建第二套 canonical state；
- identity/worldline 不漂移。

### S4 Lifecycle leak
至少 1000 次 mount/unmount：
- no listener leak；
- no timer leak；
- no service ghost；
- no orphan fiber；
- no stale scoped provider。

### S5 Capability graph export
导出：
- resolved providers；
- required seams；
- consumer dependencies；
- scope ownership；
- exact versions。

落盘：

`artifacts/r7/composition/resolved_graph.json`

Spike 失败时先写根因报告，不得直接迁主干。

---

# 6. Phase 2 — Versioned Service Contracts

建立明确 contract packages，不让 consumer import provider 实现。

目标至少包括：

```text
wanxiang.identity@1
wanxiang.reality.observe@1
wanxiang.reality.proposal@1
wanxiang.reality.policy@1
wanxiang.authority@1
wanxiang.history@1
wanxiang.branch@1
wanxiang.lineage@1
wanxiang.replay@1
wanxiang.evidence@1
wanxiang.rights@1
wanxiang.execution@1
wanxiang.actor@1
wanxiang.model@1
wanxiang.capability@1
```

每个 Service Definition 必须包含：

```text
namespace
service_id
API version
schema version
request/response types
error semantics
scope
capabilities
compatibility rules
contract tests
```

## 6.1 Provider / Consumer 规则

采用：

```text
Service Definition
Provider
Consumer
```

Consumer 只能依赖 contract，禁止依赖 provider internals。

加入 architecture test 自动拦截。

## 6.2 版本规则

至少区分：

```text
Wanxiang software version
Cordis version
Service API version
Provider package version
Storage schema version
RealityProfile version
WorldProfile version
World Definition version
RuntimeLock version
```

---

# 7. Phase 3 — Wanxiang Base Bundle

实现或收敛：

```text
WorldScopeManager
ProfileManager
RuntimeLockManager
SchemaRegistry
CapabilityBroker
AuthorityBootstrap
MigrationCoordinator
```

## 7.1 World Scope

推荐 Context tree：

```text
Root
├─ Tenant
│  ├─ World
│  │  ├─ Worldline main
│  │  │  ├─ Actor scopes
│  │  │  └─ Experience scopes
│  │  └─ Worldline alt
│  └─ Other World
└─ shared global providers
```

必须验证：

```text
world A unload != world B affected
world A history != world B history
A branch cannot read B state
global provider only shared where policy permits
```

## 7.2 Context 只管理 capability graph

强制 guard：

`Cordis Context 中不得承载 Canonical World State`

Canonical state 必须来源于 History / Snapshot / Projection。

---

# 8. Phase 4 — RealityProfile / WorldProfile / RuntimeLock

## 8.1 RealityProfile

至少定义：

```yaml
reality_profile:
  id:
  version:
  identity_contract:
  observe_contract:
  proposal_contract:
  policy_contract:
  authority_contract:
  history_contract:
  branch_contract:
  lineage_contract:
  replay_contract:
  evidence_contract:
  rights_contract:
```

whether required/optional 由 profile 指定。

## 8.2 WorldProfile

描述：

```text
reality profile
runtime providers
time
space
actors
memory
simulation
capabilities
experience
projection
distribution
```

## 8.3 RuntimeLock

至少包含：

```text
world_id
world_definition_version
world_instance_id
worldline_id
reality_profile_id/version/hash
world_profile_id/version/hash
Cordis exact version/commit
service contract versions
provider package versions
artifact hashes
schema versions
migration lineage
runtime config hash
```

同一 lock 下 replay 结果必须稳定。

---

# 9. Phase 5 — History / Snapshot / Replay / Branch / Lineage

## 9.1 History seam

最小语义：

```text
append(expected_revision, events)
read(from_revision)
head()
checkpoint()
subscribe()
```

必须实际验证并发冲突：

```text
head=125
A append expected=125 -> success -> 126
B append expected=125 -> conflict
```

禁止 last-write-wins 静默覆盖。

## 9.2 Provider

至少：

```text
history-memory
history-sqlite 或现有 SQLite adapter
history-postgres（环境允许时）
```

live PostgreSQL 不可用时记录 `EXTERNAL_BLOCKED`，但 provider contract tests 和本地验证必须完成。

## 9.3 Replay

要求：
- snapshot 删除后仍可从完整 history 重建；
- same RuntimeLock replay state/hash 一致；
- replay 不调用不可控外部 LLM；
- snapshot 是 optimization，不是 truth source。

## 9.4 Branch

至少：

```text
fork(parent_worldline, at_revision)
head(worldline)
ancestor(a,b)
list_children(worldline)
```

证明：
- branch isolation；
- cross-worldline write denied；
- fork point 可审计；
- branch 不等于 sandbox snapshot。

## 9.5 Lineage

保持：

```text
Worldline
→ Distill / Validate / Promote
→ Derived World Definition
```

Branch 与 Derived World 不得混淆。

---

# 10. Phase 6 — Authority Hardening

这是风险最高迁移，必须在 read path/history/profile 稳定后做。

## 10.1 公共服务与私有 CommitCapability 分离

普通插件可以：

```text
observe
propose
policy.evaluate
```

不能获得：

```text
canonical append credential
CommitCapability
raw canonical DB credential
```

CommitCapability 只由 AuthorityBootstrap 授予受控 authority holder。

## 10.2 Monotonic Guard

Policy 可贡献：

```text
ALLOW
DENY
CONSTRAIN
TRANSFORM
```

但：

`HARD_DENY 一旦成立，后续 provider 不得变回 ALLOW`

至少覆盖：
- cross-world access；
- rights/privacy denial；
- invalid expected_revision；
- illegal branch write；
- missing mandatory evidence；
- forbidden external effect。

## 10.3 Direct DB bypass

加入静态+运行时 guard：
- 普通 Actor/Plugin 不可 import canonical repository write internals；
- untrusted extension 无 canonical DB credential；
- bypass test 必须失败。

## 10.4 最终流程

```text
Proposal
→ collect policy decisions
→ resolve constraints/transforms
→ final monotonic guards
→ verify expected_revision
→ authority commit
→ append history
→ publish committed observation
```

---

# 11. Phase 7 — Irreversible External Effect Boundary

Email、付款、机器人、链上交易、第三方写 API 等不能用 Cordis `dispose()` 假装撤销。

实现：

```text
Proposal
→ Validate
→ Commit ExternalIntent / Outbox
→ External Executor
→ idempotency key
→ actual external result
→ Observation
→ Reconciliation Commit
```

要求：
- outbox 持久化；
- idempotency；
- retry policy；
- duplicate execution guard；
- ambiguous result -> manual reconciliation；
- compensation 显式；
- external result 不直接改 canonical state。

---

# 12. Phase 8 — Execution Fabric

统一 execution class：

```text
function/process
isolated process
container
Wasm（若成熟）
microVM/VM（接口先行，基础设施按环境）
GPU
remote
```

## 12.1 ExecutionPolicy

路由至少考虑：

```text
trust level
filesystem needs
network needs
secret access
CPU/memory
GPU
duration
reproducibility
cost
side effects
```

## 12.2 ExecutionTrace

记录：

```text
execution_id
capability_id/version
runtime/provider
environment hash
input refs
commands/tool calls
output refs
exit status
resource stats
snapshot/resume refs
```

但：

`ExecutionTrace != World History`

## 12.3 不可信能力

默认：

```text
generated code
third-party capability
Paper2Agent-generated tool
user supplied code
```

不得 in-process trusted host 执行。

---

# 13. Phase 9 — DSH Agent Harness Bridge

首选：

```text
DSH 独立进程
→ SDK / JSON-RPC bridge
→ wanxiang-agent-dsh provider
```

DSH Provider 可以：

```text
observe world
query allowed history/context
propose action
receive committed consequences
```

不得：

```text
direct append
direct canonical DB write
mutate Worldline metadata
fake committed StateDiff
```

Acceptance 至少覆盖：

```text
observe
→ DSH decision
→ proposal
→ Wanxiang policy
→ commit/reject
→ DSH receives committed result
```

必须验证 reject path。

---

# 14. Phase 10 — Capability Foundry / Artifact2Capability

保持：

```text
Paper / Repo / API / Manual / Standard / Workflow
→ Capability Candidate
→ Environment
→ Interface
→ Verification
→ Verified Capability Package
→ Registry
```

Verified Capability Package 至少包含：

```text
capability_id
version
source artifacts
license/rights
interface
runtime requirements
execution class
environment lock/hash
golden cases
verification results
validity envelope
known limitations
security policy
provenance
```

## 14.1 Paper2Agent reference slice

做一个真实 reference integration：

```text
paper + repo
→ extracted/packaged capability
→ isolated execution
→ golden verification
→ registry
→ invoked from world
→ output becomes Observation/Proposal
```

失败 tool 不进入 VERIFIED。

Capability result 永远不能自动 Commit。

---

# 15. Phase 11 — RealityProfile Migration

## 15.1 v1/v2 共存

必须能同时存在：

```text
persistent-v1
persistent-v2
```

已有 worldline 明确 pin v1。

## 15.2 Major upgrade 禁止 silent hot swap

流程：

```text
quiesce worldline
→ checkpoint
→ capture old RuntimeLock
→ build candidate new lock
→ shadow replay
→ compare state/history/invariants
→ generate migration report
→ choose:
   A. migrate
   B. fork
   C. reject upgrade
```

## 15.3 Semantic drift detection

至少比较：

```text
world identity
entity identity
history head
canonical state hash / normalized projection
branch graph
lineage
rights/evidence invariants
declared domain invariants
```

## 15.4 Migration artifact

必须落盘：

```text
from_profile
to_profile
from_lock
to_lock
migration code/version
preconditions
diff
invariant results
human approval if required
lineage output
```

---

# 16. Phase 12 — Experience / Projection / Distribution Fabric

不得因为底层重构把 R5 产品层丢掉。

继续实现/核验：

```text
ExperienceBlueprint
InteractionProfile
ProjectionProfile
DistributionAdapter
Player / Studio 分离
zh-CN default
```

同一个 World 至少证明两个 Experience 共享同一 Canonical Reality，例如：

```text
roleplay experience
observer/research experience
```

不得各有独立 world state。

## 16.1 中文玩家体验

要求：
- 默认 zh-CN；
- 不露工程内部 ID；
- Player 与 Studio 分离；
- 世界广场、世界详情、角色进入、Play、世界变化、Leave→Continue 产品化；
- “世界变化”只能来自 committed StateDiff / canonical history；
- Continue 回同一 world/worldline/actor committed state。

---

# 17. Phase 13 — Reference Worlds / Applications

不要求把七类世界都做成大型商业产品，但必须证明架构不是只适合一个 demo。

至少：

## A. Original/Fiction World
验证：
`WorldProfile / Actor / free-form proposal / commit-reject / branch / continue`

## B. Heritage World
验证：
`evidence required / rights-provenance / source claim vs generated reconstruction / experience-projection separation`

## C. Agent World
验证：
`DSH or rule actor / execution trace / longer horizon / resource accounting / proposal-only agent`

## D. Science/Capability slice
验证：
`Verified Capability / isolated execution / result -> Observation/Proposal / validity envelope`

City/Family/Hybrid Reality 若已有真实工程则加入测试；否则保持 profile/schema/reference fixture，不得假装完整产品已实现。

---

# 18. Phase 14 — Observability / Ops / Resource Governance

至少提供：

```text
world_id/worldline_id/revision
runtime lock hash
profile ids/versions
provider graph
proposal count
commit/reject count
history append latency
replay duration
actor/model calls
execution jobs
token/cost where available
resource usage
migration status
outbox pending/retry
```

日志结构化、敏感数据脱敏。

加入：

```text
health
readiness
world host status
provider status
migration status
```

监控状态不得成为 canonical truth。

---

# 19. Phase 15 — 全量测试体系

## Contract Tests

```text
history
branch
replay
evidence
rights
execution
actor
model
```

## Composition Tests

```text
provider missing
provider activation
provider replacement
unload cleanup
scope isolation
deterministic profile resolution
resolved graph export
```

## World History Property Tests

```text
monotonic revision
no silent overwrite
same-lock deterministic replay
branch isolation
identity uniqueness
migration invariant preservation
```

## Security Tests

```text
ordinary actor cannot acquire commit capability
untrusted extension cannot access canonical DB
cross-worldline access denied
secret capability explicit
hard deny monotonic
external action uses outbox/idempotency
```

## Lifecycle Tests

`1000 mount/unmount cycles`

## Migration Tests

```text
v1/v2 coexist
shadow replay
semantic drift detection
migrate
fork
rollback/reject
```

## E2E

至少：

```text
Create/Load World
→ Actor Observe
→ Proposal
→ Policy
→ Commit
→ StateDiff/World Change
→ Leave
→ Continue
→ Replay
→ Branch
→ Provider swap where valid
```

以及：

```text
DSH Agent -> Proposal -> Commit/Reject
Capability -> Isolated Execution -> Observation -> Proposal
```

---

# 20. Phase 16 — Build / Lint / Type / Security / Clean Clone

最终候选 SHA 重新跑所有实际存在的：

```text
Python sync/install
ruff
format check
mypy/pyright
pytest full
Hypothesis/property tests
TypeScript lint
typecheck
Vitest
frontend build
Playwright
architecture guards
security tests
migration tests
profile/lock validation
```

再做 exact-SHA clean clone：

```text
fresh directory
checkout exact candidate SHA
install from lockfiles
run required qualification
```

记录：

```text
tool versions
OS/runtime
Node/Python versions
lock hashes
test counts
duration
known external blockers
```

---

# 21. Phase 17 — 文档、ADR、证据与最终收口

必须更新/生成：

```text
STATUS.md
PLAN.md
BLOCKERS.md
README.md
architecture docs
R7 ADRs
service contract docs
profile docs
migration docs
security model
execution model
DSH bridge docs
Capability Foundry docs
operator runbook
developer quickstart
player quickstart
```

生成：

```text
reports/r7/
artifacts/r7/
```

至少：

```text
00_REPO_BASELINE.md
01_V55_STABLE_VERIFICATION.md
02_CORDIS_SPIKE_REPORT.md
03_SERVICE_SEAMS_REPORT.md
04_SCOPE_COMPOSITION_REPORT.md
05_HISTORY_REPLAY_REPORT.md
06_AUTHORITY_SECURITY_REPORT.md
07_EXECUTION_FABRIC_REPORT.md
08_DSH_BRIDGE_REPORT.md
09_CAPABILITY_FOUNDRY_REPORT.md
10_REALITY_MIGRATION_REPORT.md
11_EXPERIENCE_APPLICATION_REPORT.md
12_REFERENCE_WORLDS_REPORT.md
13_FULL_REGRESSION_REPORT.md
14_CLEAN_CLONE_REPORT.md
15_R7_FINAL_CLOSURE_REPORT.md
```

---

# 22. Git / Commit / Push 策略

遵循仓库既有 `AGENTS.md` / release policy。

原则：

```text
no force push
no history rewrite
no released-tag mutation
small coherent commits
commit message explains evidence
```

建议 checkpoint：

```text
chore(r7): record repository baseline
feat(r7): add cordis minimal world spike
feat(r7): add versioned service contracts
feat(r7): add world scopes and runtime lock
feat(r7): add history branch replay providers
feat(r7): harden authority and commit capability
feat(r7): add execution fabric
feat(r7): bridge dsh agent provider
feat(r7): add capability foundry reference
feat(r7): add reality profile migration
feat(r7): integrate experience application fabric
test(r7): complete qualification gates
docs(r7): final closure evidence
```

有明确 push 授权则按 Gate push feature/candidate branch 并验证 CI；无明确授权则保留本地 commits，不自行假设。

---

# 23. Architecture Gates

## Gate A — Composition
PASS：
- provider 可替换；
- consumer 不 import provider internals；
- unload 清理 runtime effects；
- A/B world scope 不串；
- resolved graph 可导出。

## Gate B — Persistence
PASS：
- plugin unload 不删除 committed history；
- >=100 revisions replay 一致；
- expected_revision 防丢更新；
- snapshot 删除后可从 history replay。

## Gate C — Authority
PASS：
- ordinary Actor/Plugin 无 canonical append credential；
- HARD_DENY 不可被覆盖；
- cross-worldline write 拒绝；
- direct DB bypass guard/test 存在并通过。

## Gate D — Migration
PASS：
- RealityProfile v1/v2 共存；
- existing worldline pin v1；
- shadow replay 检测 drift；
- migrate/fork 有 lineage evidence。

## Gate E — External Execution
PASS：
- untrusted capability 不在 trusted host 直接执行；
- execution trace 与 history 分离；
- result 只能 Observation/Proposal；
- resource/timeout/failure 被治理。

## Gate F — DSH
PASS：
- DSH 通过明确 gateway；
- observe/propose 正常；
- reject path 正常；
- 无 direct canonical append。

## Gate G — Capability Foundry
PASS：
- 至少一个真实 Artifact→Capability reference；
- source/provenance/rights 明确；
- golden verification；
- validity/limitations；
- isolated execution；
- output 不自动 Commit。

## Gate H — Experience
PASS：
- 一个 World 至少两个 Experience 共享 canonical state；
- zh-CN 默认玩家端；
- Leave→Continue 连续；
- StateDiff/世界变化来源于 Commit。

## Gate I — Reliability
PASS：
- full regression；
- build/lint/type/security green；
- clean clone exact SHA 可复现；
- lifecycle leak tests green；
- no known P0/P1 architecture blocker。

## Gate J — Evidence Integrity
PASS：
- DESIGN / IMPLEMENTED / VALIDATED / EXTERNAL_BLOCKED / HUMAN_INPUT_REQUIRED 分离；
- 无伪造真人证据；
- 无 synthetic 冒充 real；
- 所有 PASS 有可复现 evidence path。

---

# 24. R7 Definition of Done

只有以下全部成立，才能写：

`R7_IMPLEMENTATION_COMPLETE`

1. 真实 repo baseline 已核验；
2. v5.5 Stable 已存在，或本轮按真实 Gate 完成并验证；
3. Cordis architecture spike 全部通过；
4. 核心 service seams 版本化；
5. WorldScope / RealityProfile / WorldProfile / RuntimeLock 已实现；
6. History/Replay/Branch/Lineage 通过 contract/property tests；
7. provider swap 至少在一个关键 seam 上真实完成；
8. Authority/CommitCapability/Monotonic Guard/expected_revision 安全闭环成立；
9. Context 不承载 canonical world state；
10. Cordis effect 不会撤销 committed history；
11. Execution Fabric 至少有可用本地隔离 provider；
12. DSH bridge 有真实 E2E；
13. Capability Foundry 有真实 reference slice；
14. RealityProfile v1→v2 shadow replay + migrate/fork 成立；
15. R5 Experience/Application Fabric 没被底层迁移破坏；
16. 中文玩家主链可用；
17. 至少 Original + Heritage + Agent + Science/Capability 四类 reference slice 可复现；
18. full regression / lint / type / build / security 通过；
19. exact-SHA clean clone 通过；
20. reports/artifacts/ADRs/STATUS/PLAN/BLOCKERS 已更新；
21. worktree clean；
22. 不存在未解释的 P0/P1 blocker；
23. external/human blockers 被诚实分类；
24. 未擅自发布 v5.6；
25. final closure report 能让下一个 Agent 从零复现当前状态。

---

# 25. 允许停止的唯一情况

## A. R7_IMPLEMENTATION_COMPLETE
Definition of Done 全部满足。

## B. WAITING_HUMAN
只有真人 Gate 阻塞，已生成完整测试包，其余可做项已完成。

## C. EXTERNAL_BLOCKED
确需 user secret / 外部付费资源 / 无替代基础设施，且 blocker 已证明、其它独立工作已完成。

## D. ARCHITECTURE_REJECTED
Cordis spike 以真实证据证明关键前提不成立。

此时必须生成：

`R7_ARCHITECTURE_REJECTION_REPORT.md`

包含：失败事实、可复现命令、根因、被证伪 ADR、替代架构建议、未破坏 Stable 的证据。

---

# 26. 自动续跑协议

每完成一个阶段：

```text
1. run tests
2. save evidence
3. update STATUS
4. update PLAN
5. update BLOCKERS
6. commit coherent checkpoint
7. inspect next unresolved Gate
8. continue
```

不要每阶段问“下一步做什么”。

会话中断时，新 Agent 读取：

```text
R7 canonical master
本 Goal
STATUS.md
PLAN.md
BLOCKERS.md
reports/r7/15_R7_FINAL_CLOSURE_REPORT.md（若存在）
git HEAD
```

然后从**第一个未 PASS 的 Gate**继续，不重做已通过且 SHA 未失效的证据。

---

# 27. 最终报告模板

```text
# Wanxiang R7 Final Closure Report

## 1. Branch / HEAD / Worktree
## 2. v5.5 Stable status
## 3. Cordis runtime exact version
## 4. WorldProfile / RealityProfile / RuntimeLock
## 5. Service seams and providers
## 6. History / Replay / Branch / Lineage
## 7. Authority / Security
## 8. Execution Fabric
## 9. DSH Bridge
## 10. Capability Foundry
## 11. RealityProfile Migration
## 12. Experience / Application
## 13. Reference Worlds
## 14. Tests / Build / Lint / Typecheck
## 15. Lifecycle / Security / Property tests
## 16. Clean Clone
## 17. Remote CI / Push status
## 18. Remaining BLOCKED / NOT_PROVEN
## 19. Architecture Gates A–J
## 20. Final Decision
```

Final Decision 只能是：

```text
R7_IMPLEMENTATION_COMPLETE
WAITING_HUMAN
EXTERNAL_BLOCKED
ARCHITECTURE_REJECTED
NOT_COMPLETE
```

---

# 28. 最后一条执行指令

**现在开始。不要只给计划。先核验真实仓库，然后按这个 Goal 连续执行；优先根因修复和真实证据，能做的就继续做，不要为了“看起来完成”降低 Gate。v5.5 Stable 若未收口就先收口；一旦完成，依据本次用户显式授权继续执行 R7，不自动进入 v5.6。直到 R7 Definition of Done 全部满足，或遇到唯一剩余且无法绕过的 HUMAN / EXTERNAL blocker，才允许停止。**
