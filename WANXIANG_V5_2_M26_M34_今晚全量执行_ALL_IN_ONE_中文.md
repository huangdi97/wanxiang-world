# 万相世界 v5.2-R1 M26–M34 今晚全量执行包 ALL-IN-ONE（中文）



---

<!-- FILE: README_FIRST_V5_2_CN.md -->

# 万相世界 v5.2-R1 今晚全量工程执行包（中文）

本执行包用于已经完成 v5.0/v5.1 工程阶段的万相仓库。目标是在**尽量复用既有代码、删除重复实现、保持最小永久 Core**的前提下，把最新 v5.2-R1 的 Reality Root、World Constitution、World Semantic ISA、World Lineage、World Hypervisor、Evolution Policy Stack、多尺度共演化、Promotion/Cross-world Distillation 全部落地，并最终完成一个经过 Source Gate 的《红楼梦》最小活世界实例及七日验收。

## 使用方式

1. 将本目录内容合并到当前万相仓库根目录，不要覆盖或删除现有 Git 历史、源码、迁移、测试和报告。
2. 把 `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md` 作为新的设计 Source of Truth。
3. 新开 Codex Desktop 对话，把 `CODEX_直接复制启动_中文.txt` 全文发送给 Codex。
4. Codex 必须先验证旧基线，再从 G29A 连续执行至 G37G。
5. 每个 Goal 都必须通过自己的测试/验收后才能创建本地 checkpoint。
6. 每个 Milestone 必须运行 `milestones/` 下对应 Gate；PASS 后自动继续，直到 M34。
7. 不自动 push、不自动生产部署。

## 目标不是增加最多代码

本程序的关键指标是：
- 旧实现能复用则不重写；
- 重复 Registry/Manager/State/Event/Branch/Engine 必须合并；
- 新概念优先成为类型、策略、数据、薄 façade 或已有管线的扩展；
- 只有承载不可约新语义时才允许新增核心抽象；
- 红楼梦实例不得硬编码进 Core。

## Goal 编号说明

上一批 v5.1 Minimal-Core Program 已使用到 `G28I`。为避免仓库中 Goal ID 冲突，本批 v5.2 虽然对应新的工程 Milestone `M26–M34`，但具体可执行 Goal 从 `G29A` 连续编号到 `G37G`。Milestone 编号表示整个万相长期工程阶段；Goal 编号仅用于唯一标识可执行任务。



---

<!-- FILE: 00_V5_2_代码处置与复用矩阵.md -->

# v5.2 代码处置与复用矩阵

## 总结

v5.2 并不推翻 M0–M25，而是把已经形成的 Commit/Event/Replay/Branch、Living Runtime、Distillation、Capability Fabric、Triple Ledger 等进一步收敛到 `Kernel / Runtime / Forge / Experiences`，并新增世界 Constitution、语义 ISA、Lineage、Promotion 与多尺度 Evolution。

## A. 默认保留（KEEP）

| 既有能力 | 处理 | v5.2 中的位置 |
|---|---|---|
| Commit Authority | 保留并适配 | Wanxiang Kernel / Reality Root |
| Event Store / World Ledger | 保留 | History / Ledger |
| Snapshot / Replay / deterministic seed | 保留 | Kernel |
| Branch/Fork/parent isolation | 保留 | Worldline 基础 |
| Idempotency / expected revision / concurrency | 保留 | Commit Boundary |
| Persistence / Alembic / SQLite / PostgreSQL | 保留 | Infrastructure |
| Source/Evidence/Rights | 保留 | Forge |
| Package Registry | 保留并扩展 | Forge |
| Distillation Fabric / Candidate | 保留并扩展 | Forge |
| Runtime Capability Fabric | 保留并收敛 | Runtime/Forge 横向组合 |
| Stable World ABI | 保留并扩展 | Kernel↔Provider 边界 |
| Triple Ledger | 保留 | World/Actor/Runtime 三重可追踪 |
| Living World Space/Time/Object/Body/Society | 保留 | Runtime |
| World Host / Scheduler / background autonomy | 保留 | Runtime/Hypervisor |
| Perception/Belief/Memory | 保留 | Runtime |
| Actor/Organization/Skill/Affordance | 保留 | Runtime |
| EmbodimentLease / ShadowPolicy | 保留 | Experiences |
| Projection / React / Phaser | 保留 | Experiences |
| Co-Simulation / Reality Bridge | 保留 | Runtime |
| Security / Rights / Chaos / Backup | 保留 | Cross-cutting |
| SDK / OpenAPI / package tooling | 保留 | Experiences/SDK |

## B. 合并并改造（MERGE + ADAPT）

1. `Canonical State`：保留为可重建 Materialized View；权威语义明确落在 Committed History。
2. `CommitAuthority`：不重写，只扩展 Constitution/ISA/version context；一个 Commit Pipeline 支持 State/Ontology/Law 三种 payload。
3. `Branch`：不创建第二套 Worldline 引擎；Branch 成为 Worldline 的 fork 操作/历史节点语义。
4. `WorldPack`：增加 constitution_ref、genesis_spec、evolution_policy_ref、lineage metadata，不创建第二套 Genesis Package Registry。
5. `Compiler`：并入 Forge，继续复用 parser/entity resolver/evidence binder/completion；上层统一为 Distill→Candidate→Validate→Assemble/Commit。
6. `Runtime Evolution Lab`：复用现有 Shadow Branch/Experiment/Invariant/Chaos，扩展为 World Promotion 与 Platform Promotion。
7. `Package Registry + Provider Registry`：保持两个不同问题——Package 安装和 Runtime Provider 组合；删除其余重复 Registry。
8. `Audit/Trace`：并入 Triple Ledger 的引用/Projection，不保留重复巨型 audit event 体系。
9. `API/SDK`：兼容扩展 lineage、promotion、constitution、worldline，不复制第二套 API namespace。
10. `Frontend`：一个 Web 应用共享 timeline/graph/map/evidence/rights/projection 组件，不为红楼梦复制整套基础设施。

## C. 必须删除/禁止（DELETE / DO NOT CREATE）

- 第二套 Canonical State 或第二个 Commit Authority。
- `RealityRootEngine`、`WorldRealityCalculusEngine` 之类只为哲学名词存在的 God Object。
- 独立 `StateCommitEngine / OntologyCommitEngine / LawCommitEngine` 三套管线。
- `CapabilityCommit` 作为第四类 World Commit。
- 独立 Genesis Package Registry/Installer/Manager（Genesis 是 World Definition/Scenario 的规范输入）。
- 独立 Branch 系统与 Worldline 系统并存。
- `WorldLineageManager` 巨型 God Object；谱系应由薄服务 + repository + graph query 构成。
- 为每个 Distiller 建一套 Pipeline。
- 为每个 Provider 建独立 Registry/Manager。
- DSH/Cordis fork 作为万相底座。
- Domain/World 直接访问 ORM 或 Canonical mutation。
- 红楼梦专用 `if world == red_chamber` 进入 Core。
- UI/Phaser 维护另一套权威状态。
- 巨型 `manager.py / service.py / utils.py / helpers.py`。
- 仅为了“架构好看”而增加无第二实现、无隔离价值、无不可约语义的 Port/Interface。

## D. 仅实验/研究（EXPERIMENTAL）

- True Genesis 的真实科学创世。
- Hybrid Genesis / World Merge 的自动合并；首版必须支持 compatibility analysis 与安全拒绝，不能强行 merge。
- Cross-world 自动晋升到 Platform Runtime；首版只产生 Candidate + Sandbox/Approval。
- 大规模分布式 World Host；性能数据证明必要前保持模块化单体。


---

<!-- FILE: 01_V5_2_全量工程程序架构.md -->

# 万相世界 v5.2-R1 全量工程程序架构（M26–M34）

## 1. 总目标

从当前已完成 M0–M25 的仓库出发，完成 v5.2 的最小代码升级，并以《红楼梦》最小活世界证明：

`Reality Root → Constitution → Genesis/World Definition → Instance → Worldline → Living Runtime → Distillation/Evolution → Promotion/Lineage → Experience`

是一条真实、可持久化、可回放、可审计、可扩展的统一链。

## 2. 新阶段

- **M26：旧代码真实盘点与最小核心收敛**
- **M27：Reality Root / Constitution / Semantic ISA**
- **M28：Worldline / Lineage / World Hypervisor**
- **M29：Evolution Policy Stack / 多尺度共演化**
- **M30：Promotion / Cross-world Distillation / 平台反哺隔离**
- **M31：Kernel / Runtime / Forge / Experiences 收敛与向后兼容**
- **M32：《红楼梦》Source Gate、蒸馏、Domain/World Pack 编译**
- **M33：《红楼梦》Living World、接管、自治与三种 Evolution Policy**
- **M34：《红楼梦》七日验收 + Lineage/Promotion + v5.2 最终认证**

## 3. 最终物理架构

顶层长期只允许围绕以下稳定边界演化：

```text
packages/
  kernel/       # Reality Root / ISA / Authority / Ledger / Branch-Lineage identity
  runtime/      # Host / living substrate / actors / cognition / sim / capability
  forge/        # Source / Distill / Genesis / Compile / Evolve / Promote
  experiences/  # Session / Embodiment / Projection / Studio-facing use cases
  infrastructure/
```

这是物理代码收敛目标，不要求一次性搬动所有稳定文件。迁移必须以测试和依赖收益为依据；若大规模搬目录只增加 churn，则保留旧物理路径并通过边界/namespace 收敛。

## 4. 关键复用关系

- Reality Root → 复用现有 Identity/Fact/Event/Constraint/Commit/Ledger/Branch。
- Semantic ISA → 复用现有 commands/proposals/deltas/commit pipeline，作为薄语义归约。
- Worldline → 复用 Branch/Event stream。
- Lineage → 在 World Definition 与 Worldline 上新增父子/晋升图，不复制事件流。
- Promotion → 复用 Distillation + Snapshot + Package Assembler + Source/Rights/Invariant Gate。
- Multi-scale Co-Evolution → 复用 Scheduler + Actor/Organization + Distillation；新增 Policy 和升阶规则。
- World Hypervisor → 复用 World Host 多实例能力，补隔离/资源/RuntimeProfile/Lineage awareness。
- 红楼梦 → 只作为 Domain/World/Scenario/Experience 内容，不进入 Kernel。

## 5. 今晚连续执行策略

Codex 不在普通 Goal 或 Milestone 后等待确认。每个 Goal PASS 后本地 commit 并继续。只有无法通过本地代码、测试、合成数据、已有仓库内容或合法公开来源解决的外部数据/授权/硬件阻塞，才允许标记 EXTERNAL_BLOCKED；并继续其余不依赖任务。

## Goal 编号说明

上一批 v5.1 Minimal-Core Program 已使用到 `G28I`。为避免仓库中 Goal ID 冲突，本批 v5.2 虽然对应新的工程 Milestone `M26–M34`，但具体可执行 Goal 从 `G29A` 连续编号到 `G37G`。Milestone 编号表示整个万相长期工程阶段；Goal 编号仅用于唯一标识可执行任务。



---

<!-- FILE: 02_CODEX_V5_2_今晚连续执行总指令.md -->

# Codex v5.2-R1 今晚连续执行总指令

你现在继续当前万相世界仓库的正式工程开发。本轮设计 Source of Truth 是：

`docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`

用户说明此前 M0–M25 已完成，但你不得仅凭说明相信；先按 G29A 对当前 Git、代码、测试、迁移和报告做真实验证。

## 总目标

连续完成：

`G29A → ... → G37G`

即：

`M26 → M27 → M28 → M29 → M30 → M31 → M32 → M33 → M34`

最终目标是在**尽量复用旧代码、删除重复抽象、保持最小永久核心**的前提下：

1. 完成 Reality Root / World Constitution / World Semantic ISA；
2. 完成 Worldline / World Lineage Graph / World Hypervisor；
3. 完成 Evolution Policy Stack / 多尺度共演化；
4. 完成 Worldline→Derived World Promotion；
5. 完成 Cross-world Distillation 与平台反哺隔离；
6. 完成 Kernel / Runtime / Forge / Experiences 收敛；
7. 保持 v5.0/v5.1 Event/Snapshot/WorldPack/Branch 向后兼容；
8. 通过 Source Gate 编译一个真实、可追溯的《红楼梦》最小 World Definition；
9. 实例化并运行《红楼梦》Living World；
10. 完成林黛玉接管、紫鹃传话、物品/秘密/日程/职责/认知连续性；
11. 完成 Canonical Replay / Soft Canon / Living-Open 三种 Evolution Policy；
12. 完成七日活世界验收、世界线比较、Replay/Recovery；
13. 生成 RedChamber Promotion Candidate / Derived World，证明世界谱系能力；
14. 完成 v5.2 最终独立认证。

## 必读顺序

1. `README_FIRST_V5_2_CN.md`
2. `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
3. `00_V5_2_代码处置与复用矩阵.md`
4. `01_V5_2_全量工程程序架构.md`
5. `03_最小代码工程宪法.md`
6. `04_V5_2_架构裁决与歧义消解.md`
7. `05_M0_M25到V5_2迁移映射.md`
8. `06_M26_M34_GOAL总索引.md`
9. `07_M26_M34_Milestone验收门.md`
10. `08_连续执行与中断恢复协议.md`
11. `09_红楼梦SourceGate与实例验收标准.md`
12. `10_V5_2最终验收证据标准.md`
13. 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
14. 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）
15. `goals/` 全部 Goal 与 `milestones/` 全部 Gate

读完后再开始改 production code。

## 连续执行规则

- 每个 Goal：实现 → 单测/负向测试 → 集成/E2E → 架构/类型/迁移/回放检查 → 报告 → ledgers → 本地 commit → 下一个 Goal。
- 每个 Milestone：执行对应 Qualification；PASS 后自动进入下一 Milestone。
- 不在普通 Goal/Milestone 后询问用户是否继续。
- M34 完成前不停止，除非出现真正无法隔离的外部阻塞。
- 普通内部 bug、失败测试、类型错误、迁移错误、性能问题、设计实现难度都不是停止理由。

## 最少代码硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

特别禁止：
- 因为 v5.2 新增名词就创建 RealityRootEngine、SemanticISAEngine、WorldlineEngine、LineageManager、EvolutionManager 等巨型平行系统；
- 复制现有 Event/Branch/Commit/Distillation/Capability 机制；
- 为红楼梦写 Core 特判；
- 为三种 Canon 模式复制三套 Runtime；
- 把 World Merge 实现成无语义的 Git merge；
- 用模型记忆填红楼梦 Canon。

## 红楼梦数据门禁

真实《红楼梦》内容必须读取 `09_红楼梦SourceGate与实例验收标准.md`。

优先使用仓库/用户已有合法可追溯文本；若执行环境允许网络，可取得明确可合法使用的公开版本，但必须记录来源、checksum、版本、rights 与 review status。

如果无法取得合法/可追溯来源：
- `G35A` 标 EXTERNAL_BLOCKED；
- 禁止把 synthetic 数据改名冒充红楼梦；
- 继续完成所有不依赖真实文本的通用任务；
- 最终不得把 `RED_CHAMBER_COMPLETE` 或 `M34` 标 PASS。

## 最终停止

只有 `10_V5_2最终验收证据标准.md` 的全部 M34 PASS 条件满足后：
- 生成最终报告；
- 创建本地 checkpoint；
- 可选创建本地 tag `v5.2-redchamber-qualified`；
- 不 push；
- 不 deploy；
- 不自行开始 v5.3；
- 停止并向用户汇报。


---

<!-- FILE: 03_最小代码工程宪法.md -->

# v5.2 最小代码工程宪法

## 一、最少代码不是“少做功能”

最少代码定义为：**最少的永久架构机制 + 最大的数据/策略/包/Provider 复用**。不得通过省略错误处理、测试、迁移、权限或可观测性来减少行数。

## 二、九个 One 原则

1. One Reality：一个权威世界现实。
2. One Commit Boundary：一个 CommitAuthority/Mutation Boundary。
3. One Event Semantics：一套 Committed History。
4. One Branch/Worldline Semantics：分支与世界线共享历史模型。
5. One Candidate Envelope：Distillation/Emergence/Promotion 共用候选语义。
6. One Package System：Genesis/Heritage/RedChamber 不另造包管理器。
7. One Runtime Composition：一个 Capability Fabric/Composition Root。
8. One Stable World ABI：外部 Agent/Simulator/Renderer/Sensor 通过统一 ABI。
9. One Schema Pipeline：Python/API/TypeScript schema 不人工复制。

## 三、禁止的抽象膨胀

新增 class/protocol/service/registry/manager 前必须在 `reports/V5_2_CODE_MINIMALITY_LEDGER.md` 回答：
- 承载哪项不可约新语义？
- 替代/合并了什么？
- 为什么函数/类型/配置不足？
- 是否存在至少两个真实 consumer/implementation，或明确的外部不稳定边界？

回答不成立则不得新增。

## 四、Port 的适用范围

只对真正外部或可替换边界使用 Port：数据库、LLM/Harness、模拟器、传感器、渲染器、资产存储、搜索、第三方 API。纯内部算法优先普通 typed function/class。

## 五、质量门

- Python：Ruff、format check、Pyright/Mypy、pytest、Hypothesis（适用时）。
- TS：ESLint、Prettier、TypeScript strict、Vitest、Playwright（适用时）。
- Architecture conformance test 必须持续运行。
- 所有 persisted schema 变化必须有 migration + rollback/compatibility strategy。
- 核心路径不得要求 LLM key/network。
- 任何优化不得破坏 replay/determinism/provenance。


---

<!-- FILE: 04_V5_2_架构裁决与歧义消解.md -->

# v5.2 架构裁决与歧义消解

1. **Reality Root 是语义基岩，不是新服务。** 通过现有 Identity/Fact/Event/Commit/Ledger/Branch 契约实现。
2. **World Semantic ISA 是薄语义层。** `DECLARE/ASSERT/RETRACT/PROPOSE/VALIDATE/COMMIT/FORK/PROMOTE` 最终编译/映射到现有 use case 与 Commit pipeline；不得变成平行 command bus。
3. **World Commit 只有 State/Ontology/Law 三类。** Runtime provider 变化属于 RuntimeControlTransaction。
4. **Branch 与 Worldline 不双写。** Worldline 是持续历史视角；Branch 是从历史前缀产生新 Worldline 的操作/关系。
5. **World Constitution 不等于 LawSet。** Constitution 限定 LawSet/Identity/causality/evolution 的合法空间，普通 LawCommit 不可修改 Reality Root。
6. **Genesis 不建立第二套 Package 生态。** 使用 GenesisSpec/GenesisSnapshot，作为 World Definition/Scenario 的输入。
7. **World Lineage Graph 存世界定义/世界线的派生关系，不复制世界历史。**
8. **Promotion 创建新 World Definition ID；Parent Definition 与源 Worldline 不变。**
9. **Hybrid Genesis 首版必须能分析并拒绝不兼容世界；不要求自动合并任意世界。**
10. **Cross-world Distillation 只输出授权后的 Candidate；世界经验不得直接升级平台。**
11. **Kernel/Runtime/Forge/Experiences 是物理/责任收敛目标，不是四个巨型 God Service。**
12. **红楼梦真实内容必须 Source Gate；模型记忆不能成为 Canon。**
13. **红楼梦第一版是完整机制小切片，不以“整部小说全量数字化”作为完成条件。**
14. **Canonical Replay / Soft Canon / Living-Open 是 Evolution Policy 配置，不复制三个 Runtime。**
15. **Current State 是可重建投影；Committed History 保持权威。**


---

<!-- FILE: 05_M0_M25到V5_2迁移映射.md -->

# M0–M25 → v5.2 迁移映射

| 旧阶段能力 | v5.2 处理 | 新归属 |
|---|---|---|
| M0 工程基础 | 原样保留 | 全局 |
| M1 Authority/Event/Replay/Branch | 保留+薄适配 | Kernel |
| M2 Living Substrate | 原样保留 | Runtime |
| M3 Agency/Cognition/Skill | 原样保留 | Runtime |
| M4 Source/Compiler/Package | 保留+归入 Forge | Forge |
| M5–M6 Host/Embodiment/Projection | 保留 | Runtime/Experiences |
| M7 Reality/Director/Experiment | 保留 | Runtime/Experiences |
| M8–M9 CoSim/Release/SDK | 保留 | Runtime/Infra/Experiences |
| M10–M17 Audit/Chaos/Production/SDK/Products | 作为回归基线 | 全局 |
| M18–M25 v5.1 Minimal Core | 保留；成为 v5.2 直接基础 | Kernel/Runtime/Forge |
| v5.1 Reality Calculus | 不另造 Engine | Kernel 语义 |
| v5.1 Genesis | 扩展 Constitution/Lineage | Forge |
| v5.1 Distillation | 扩展 Promotion/Cross-world | Forge |
| v5.1 Capability Fabric | 保留 | Runtime/Forge |
| v5.1 Triple Ledger | 保留+加 Lineage refs | Kernel/Runtime |
| v5.1 Bounded Runtime Evolution | 复用为 Promotion Sandbox | Forge/Runtime |

## 迁移完成标准

- 老 Event stream 在 v5.2 仍可 replay。
- 老 Snapshot 可 restore 或有明确、测试过的迁移。
- 老 WorldPack 可 import/upgrade。
- 老 Branch ID/历史语义不丢失。
- API/SDK 破坏性变化必须有 compatibility/deprecation。
- 不允许通过清空数据库或重新生成 fixtures 规避兼容性问题。


---

<!-- FILE: 06_M26_M34_GOAL总索引.md -->

# M26–M34 Goal 总索引

> 按此顺序连续执行。每个 Milestone Gate 必须 PASS 后才能继续。

## M26

- `G29A` — 冻结旧基线并验证 M25 真实状态 — `goals/G29A_冻结旧基线并验证 M25 真实状态.md`
- `G29B` — 全仓代码处置实际盘点 — `goals/G29B_全仓代码处置实际盘点.md`
- `G29C` — 合并重复 Registry 与 Manager — `goals/G29C_合并重复 Registry 与 Manager.md`
- `G29D` — 统一 State Event Audit 派生关系 — `goals/G29D_统一 State Event Audit 派生关系.md`
- `G29E` — 收敛物理包边界 — `goals/G29E_收敛物理包边界.md`
- `G29F` — 清理 Fake Placeholder 与旧实验残留 — `goals/G29F_清理 Fake Placeholder 与旧实验残留.md`
- `G29G` — 建立最小代码度量与预算 — `goals/G29G_建立最小代码度量与预算.md`
- `G29H` — M26 收敛资格验收 — `goals/G29H_M26 收敛资格验收.md`
- Milestone Gate — `milestones/M26_QUALIFICATION.md`

## M27

- `G30A` — Reality Root 语义契约 — `goals/G30A_Reality Root 语义契约.md`
- `G30B` — World Constitution 模型与版本 — `goals/G30B_World Constitution 模型与版本.md`
- `G30C` — Constitution 执行与不可越权 — `goals/G30C_Constitution 执行与不可越权.md`
- `G30D` — World Semantic ISA 最小类型 — `goals/G30D_World Semantic ISA 最小类型.md`
- `G30E` — ISA 到现有用例与 Commit 管线映射 — `goals/G30E_ISA 到现有用例与 Commit 管线映射.md`
- `G30F` — 三类 World Commit 收敛 — `goals/G30F_三类 World Commit 收敛.md`
- `G30G` — Fact Scope 与 Authority Partition — `goals/G30G_Fact Scope 与 Authority Partition.md`
- `G30H` — Event Snapshot 版本上下文升级 — `goals/G30H_Event Snapshot 版本上下文升级.md`
- `G30I` — M27 Root Constitution ISA 资格验收 — `goals/G30I_M27 Root Constitution ISA 资格验收.md`
- Milestone Gate — `milestones/M27_QUALIFICATION.md`

## M28

- `G31A` — World Definition 与 Worldline 身份模型 — `goals/G31A_World Definition 与 Worldline 身份模型.md`
- `G31B` — World Lineage Graph 数据模型 — `goals/G31B_World Lineage Graph 数据模型.md`
- `G31C` — Lineage Repository 与迁移 — `goals/G31C_Lineage Repository 与迁移.md`
- `G31D` — World Hypervisor 多实例隔离 — `goals/G31D_World Hypervisor 多实例隔离.md`
- `G31E` — Interworld Identity 与 Presence — `goals/G31E_Interworld Identity 与 Presence.md`
- `G31F` — Hybrid Genesis 兼容性分析与安全拒绝 — `goals/G31F_Hybrid Genesis 兼容性分析与安全拒绝.md`
- `G31G` — Lineage API SDK Studio 最小投影 — `goals/G31G_Lineage API SDK Studio 最小投影.md`
- `G31H` — M28 Lineage Hypervisor 资格验收 — `goals/G31H_M28 Lineage Hypervisor 资格验收.md`
- Milestone Gate — `milestones/M28_QUALIFICATION.md`

## M29

- `G32A` — Evolution Policy Stack — `goals/G32A_Evolution Policy Stack.md`
- `G32B` — 多尺度演化调度 — `goals/G32B_多尺度演化调度.md`
- `G32C` — Actor Capability 与 Persona 演化分离 — `goals/G32C_Actor Capability 与 Persona 演化分离.md`
- `G32D` — Relation Group Social Pattern Distillation — `goals/G32D_Relation Group Social Pattern Distillation.md`
- `G32E` — Institution Organization Rule 晋升 — `goals/G32E_Institution Organization Rule 晋升.md`
- `G32F` — Ontology Law 多尺度演化 — `goals/G32F_Ontology Law 多尺度演化.md`
- `G32G` — Evolution Telemetry 与隐私权利 — `goals/G32G_Evolution Telemetry 与隐私权利.md`
- `G32H` — M29 多尺度共演化资格验收 — `goals/G32H_M29 多尺度共演化资格验收.md`
- Milestone Gate — `milestones/M29_QUALIFICATION.md`

## M30

- `G33A` — 统一 Abstraction Ladder — `goals/G33A_统一 Abstraction Ladder.md`
- `G33B` — Worldline 到 Derived World Promotion Pipeline — `goals/G33B_Worldline 到 Derived World Promotion Pipeline.md`
- `G33C` — Promotion 可重放与可撤销控制 — `goals/G33C_Promotion 可重放与可撤销控制.md`
- `G33D` — Cross-world Distillation — `goals/G33D_Cross-world Distillation.md`
- `G33E` — 平台反哺 Sandbox Benchmark Approval — `goals/G33E_平台反哺 Sandbox Benchmark Approval.md`
- `G33F` — Lineage 与 Promotion API Studio — `goals/G33F_Lineage 与 Promotion API Studio.md`
- `G33G` — M30 Promotion Cross-world 资格验收 — `goals/G33G_M30 Promotion Cross-world 资格验收.md`
- Milestone Gate — `milestones/M30_QUALIFICATION.md`

## M31

- `G34A` — Kernel Runtime Forge Experiences 责任收敛 — `goals/G34A_Kernel Runtime Forge Experiences 责任收敛.md`
- `G34B` — WorldPack Definition schema v5.2 迁移 — `goals/G34B_WorldPack Definition schema v5.2 迁移.md`
- `G34C` — 数据库与 Ledger 兼容迁移 — `goals/G34C_数据库与 Ledger 兼容迁移.md`
- `G34D` — 旧 Event Snapshot Branch 向后回放 — `goals/G34D_旧 Event Snapshot Branch 向后回放.md`
- `G34E` — API SDK Client 兼容 — `goals/G34E_API SDK Client 兼容.md`
- `G34F` — 性能与复杂度回归 — `goals/G34F_性能与复杂度回归.md`
- `G34G` — M31 全平台兼容资格验收 — `goals/G34G_M31 全平台兼容资格验收.md`
- Milestone Gate — `milestones/M31_QUALIFICATION.md`

## M32

- `G35A` — 红楼梦来源策略与合法版本登记 — `goals/G35A_红楼梦来源策略与合法版本登记.md`
- `G35B` — 章节分段与可引用 Source Locator — `goals/G35B_章节分段与可引用 Source Locator.md`
- `G35C` — 人物与别名 Identity Distillation — `goals/G35C_人物与别名 Identity Distillation.md`
- `G35D` — 空间组织物品 Distillation — `goals/G35D_空间组织物品 Distillation.md`
- `G35E` — Past Character Future Canon 编译 — `goals/G35E_Past Character Future Canon 编译.md`
- `G35F` — Narrative Household HistoricalChina Domain 复用与补齐 — `goals/G35F_Narrative Household HistoricalChina Domain 复用与补齐.md`
- `G35G` — Character Relation Knowledge Boundary Distillation — `goals/G35G_Character Relation Knowledge Boundary Distillation.md`
- `G35H` — Completion Ledger 与审核 — `goals/G35H_Completion Ledger 与审核.md`
- `G35I` — 编译 RedChamber World Definition 与 Scenario — `goals/G35I_编译 RedChamber World Definition 与 Scenario.md`
- Milestone Gate — `milestones/M32_QUALIFICATION.md`

## M33

- `G36A` — 实例化 RC-001 与固定世界快照 — `goals/G36A_实例化 RC-001 与固定世界快照.md`
- `G36B` — 红楼梦空间可见可听私密运行 — `goals/G36B_红楼梦空间可见可听私密运行.md`
- `G36C` — 人物职责 NPC 日程身体与社会制度 — `goals/G36C_人物职责 NPC 日程身体与社会制度.md`
- `G36D` — 信件诗稿礼物药物的物质与信息连续性 — `goals/G36D_信件诗稿礼物药物的物质与信息连续性.md`
- `G36E` — Perception Belief Memory 与消息传播 — `goals/G36E_Perception Belief Memory 与消息传播.md`
- `G36F` — 林黛玉 Embodiment ShadowPolicy Handoff — `goals/G36F_林黛玉 Embodiment ShadowPolicy Handoff.md`
- `G36G` — Canonical Replay Soft Canon Living Open 三策略 — `goals/G36G_Canonical Replay Soft Canon Living Open 三策略.md`
- `G36H` — 红楼梦 Experience Studio 最小可用面 — `goals/G36H_红楼梦 Experience Studio 最小可用面.md`
- Milestone Gate — `milestones/M33_QUALIFICATION.md`

## M34

- `G37A` — 红楼梦七日场景自动化执行 — `goals/G37A_红楼梦七日场景自动化执行.md`
- `G37B` — Canon 用户 无干预三世界线比较 — `goals/G37B_Canon 用户 无干预三世界线比较.md`
- `G37C` — 红楼梦长时演化与 Promotion Candidate — `goals/G37C_红楼梦长时演化与 Promotion Candidate.md`
- `G37D` — 红楼梦 Replay Crash Recovery Chaos — `goals/G37D_红楼梦 Replay Crash Recovery Chaos.md`
- `G37E` — v5.2 全仓最小代码与架构终审 — `goals/G37E_v5.2 全仓最小代码与架构终审.md`
- `G37F` — 全量回归与最终追溯矩阵 — `goals/G37F_全量回归与最终追溯矩阵.md`
- `G37G` — v5.2 与 RedChamber 最终认证并停止 — `goals/G37G_v5.2 与 RedChamber 最终认证并停止.md`
- Milestone Gate — `milestones/M34_QUALIFICATION.md`


---

<!-- FILE: 07_M26_M34_Milestone验收门.md -->

# M26–M34 Milestone 验收门

- **M26** — 旧代码真实盘点与最小核心收敛 — `milestones/M26_QUALIFICATION.md`
- **M27** — Reality Root / Constitution / Semantic ISA — `milestones/M27_QUALIFICATION.md`
- **M28** — Worldline / Lineage / World Hypervisor — `milestones/M28_QUALIFICATION.md`
- **M29** — Evolution Policy Stack / 多尺度共演化 — `milestones/M29_QUALIFICATION.md`
- **M30** — Promotion / Cross-world Distillation — `milestones/M30_QUALIFICATION.md`
- **M31** — 平台收敛与向后兼容 — `milestones/M31_QUALIFICATION.md`
- **M32** — 《红楼梦》Source Gate 与 World Definition 编译 — `milestones/M32_QUALIFICATION.md`
- **M33** — 《红楼梦》Living World Runtime 与 Experience — `milestones/M33_QUALIFICATION.md`
- **M34** — 七日活世界 + Lineage/Promotion + v5.2 最终认证 — `milestones/M34_QUALIFICATION.md`


---

<!-- FILE: 08_连续执行与中断恢复协议.md -->

# Codex 连续执行与中断恢复协议

## 中断后恢复顺序

1. `STATUS.md`
2. `PLAN.md`
3. `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`（若存在）
4. 最近一个 Milestone report
5. 最近一个 Goal report
6. `git status`
7. `git log --oneline -20`
8. 当前 Goal 文件
9. 相关测试与失败日志

从最早 `IN_PROGRESS/FAIL` 的 Goal 继续，不重复已经有可复现 PASS 证据的工作。

## 内部失败处理

测试、类型、迁移、架构、数据模型、性能、代码质量等内部失败必须自己修复。不能用 `EXTERNAL_BLOCKED`。

## 外部阻塞

只允许：无法取得合法资料/授权、真实硬件、不可获得凭证或外部服务。即使出现外部阻塞，也要先完成 Port/Fake/Contract/Synthetic/Documentation。


---

<!-- FILE: 09_红楼梦SourceGate与实例验收标准.md -->

# 《红楼梦》Source Gate 与最小活世界验收标准

## 1. Source Gate

真实《红楼梦》实例必须：
- 明确选定版本/底本/电子文本来源；
- 保存来源 URI/文件、checksum、版本/版次说明、rights/licence/public-domain 依据；
- 章节/段落/人物/事件 Claim 可回链到来源位置；
- 不允许模型记忆补写 Canon；
- 无来源内容只能进入 Completion，且标 E1–E5；
- FutureCanon 不进入角色当前 Perception。

如果执行环境无法取得可合法使用且可追溯的文本：
- 真实 Source Goal 标 `EXTERNAL_BLOCKED`；
- 不得把 synthetic fixture 改名为《红楼梦》；
- 仍完成所有通用 Domain、Compiler、Runtime、UI、测试能力；
- 最终 M34 不得宣称真实红楼梦实例 PASS。

## 2. 第一版实例范围

空间：潇湘馆、怡红院、公共路径、一个公共/过渡空间，具备 access/visibility/acoustic/privacy。

人物：林黛玉、贾宝玉、紫鹃、2 名经来源确认的主要人物、10–20 名职责型 NPC。

物品：信/诗稿、礼物、药物、服饰/首饰、陈设、容器/钥匙/保管关系。

动作：移动、观察、等待、交谈、试探、隐瞒、传话、请安、访友、探病、写/读/藏/交付信件、赠礼/拒礼/转交、赴约/回避/邀请、休息、服药、用饭、写诗/领域活动。

## 3. 正典分层

- PastCanon：当前时点已发生。
- CharacterCanon：身份/经历/关系/人格边界。
- FutureCanon：只供正典控制，不注入当前人物观察。
- Completion：必须有类别、支持来源、置信度、review_status、can_enter_canon=false 默认。

## 4. 三种 Evolution Policy

- Canonical Replay：关键节点锁定。
- Soft Canon：未来事件为吸引子/条件图，可被强因果链改变。
- Living/Open：未来 Canon 仅比较基线，允许开放演化。

三个模式共享同一 Runtime，仅 Policy 不同。

## 5. 七日验收

1. 固定快照启动。
2. Day1 用户接管林黛玉。
3. 委托紫鹃传话。
4. 紫鹃可接受/改变方式/拒绝。
5. 消息按实际可达/可听/转交链传播，无全知泄漏。
6. 信件位置、保管、密封/阅读状态持续。
7. 人物按日程生活并受身体/职责/邀请约束。
8. Day3 用户退出，AI 按授权恢复控制。
9. Day3 Fork；Parent 不变化。
10. Day7 全事件可 replay 重建。
11. 比较 Canon / 用户 / 无人干预三条世界线。
12. 每条 Canon/Completion/Generated 内容可识别来源级别。
13. 运行中 WorldPack 母本不被修改。
14. 可从一条长期/加速 Worldline 生成 Promotion Candidate，但不得自动覆盖原著世界定义。


---

<!-- FILE: 10_V5_2最终验收证据标准.md -->

# v5.2 最终验收与证据标准

## 最终必须产生的证据

- `reports/V5_2_BASELINE_AUDIT.md`
- `reports/V5_2_CODE_DISPOSITION_ACTUAL.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`
- `reports/V5_2_ARCHITECTURE_CONFORMANCE.md`
- `reports/V5_2_BACKWARD_COMPATIBILITY.md`
- `reports/V5_2_LINEAGE_AND_PROMOTION.md`
- `reports/V5_2_EVOLUTION_POLICY_VALIDATION.md`
- `reports/RED_CHAMBER_SOURCE_GATE.md`
- `reports/RED_CHAMBER_WORLD_PACK_ACCEPTANCE.md`
- `reports/RED_CHAMBER_7_DAY_ACCEPTANCE.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_FINAL_CERTIFICATION.md`

## 最终判定

`M34 = PASS` 必须同时满足：
1. M26–M33 均 PASS；
2. v5.0/v5.1 关键 fixtures 在 v5.2 上可恢复/回放；
3. Reality Root/Constitution/ISA 没有第二套权威路径；
4. Lineage/Promotion 不复制/改写 Parent 历史；
5. World Policy 不能修改 Platform Policy/Reality Root；
6. 代码最小性审计无高优先级重复架构；
7. 红楼梦真实 Source Gate PASS；
8. 红楼梦最小 WorldPack 可安装/实例化；
9. 七日活世界全部验收；
10. 失败测试不得被 skip/删除；
11. working tree clean 或所有差异已解释；
12. 生成最终本地 checkpoint，但不 push。

若第 7 条因真实外部来源不可得而 EXTERNAL_BLOCKED，则平台工程可标 `V5_2_PLATFORM_PASS`，但 **M34 / RED_CHAMBER_COMPLETE 不得标 PASS**。


---

<!-- FILE: CODEX_直接复制启动_中文.txt -->

继续当前万相世界仓库，不要重开项目，不要从零重写。

首先完整阅读：
`README_FIRST_V5_2_CN.md`
`docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
`00_V5_2_代码处置与复用矩阵.md`
`01_V5_2_全量工程程序架构.md`
`02_CODEX_V5_2_今晚连续执行总指令.md`
`03_最小代码工程宪法.md`
`04_V5_2_架构裁决与歧义消解.md`
`05_M0_M25到V5_2迁移映射.md`
`06_M26_M34_GOAL总索引.md`
`07_M26_M34_Milestone验收门.md`
`08_连续执行与中断恢复协议.md`
`09_红楼梦SourceGate与实例验收标准.md`
`10_V5_2最终验收证据标准.md`
全部 `goals/`、`milestones/`，以及仓库当前 AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG、reports、Git、源码、测试和 migrations。

然后严格按 `02_CODEX_V5_2_今晚连续执行总指令.md` 连续执行：
G29A → G37G。
每个 Goal PASS 后本地 commit 并自动继续；每个 Milestone Gate PASS 后自动继续。
不要询问是否继续，不要自动 push/deploy，不要自行开始 v5.3。

核心原则：优先 KEEP/MERGE/ADAPT 旧代码，禁止因 v5.2 名词重造第二套 Commit/Event/Branch/Worldline/Registry/Engine。Reality Root 是语义基岩，World Semantic ISA 是薄归约层，Branch 与 Worldline 共享历史语义，Promotion 复用 Distillation/Snapshot/Package/Invariant，红楼梦永远是 World/Domain/Experience 内容而非 Core。

真实《红楼梦》必须过 Source Gate；不得凭模型记忆编 Canon。能够取得合法可追溯来源时必须把真实最小实例编译、运行并完成七日验收。若真实来源客观不可得，只能明确 EXTERNAL_BLOCKED，禁止假装完成。

最终只有 `10_V5_2最终验收证据标准.md` 全部满足时才允许 M34 PASS，然后生成最终认证、本地 checkpoint 并停止。


---

<!-- FILE: goals/G29A_冻结旧基线并验证 M25 真实状态.md -->

# G29A — 冻结旧基线并验证 M25 真实状态

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

在任何 v5.2 修改前冻结当前可复现基线，确认此前完成声明对应真实代码、迁移和测试证据。

## 2. 范围

- 读取 M17/M25 最终报告与 Git 历史，记录当前 commit/branch。
- 执行全量现有质量套件并记录命令与结果。
- 导出/固定至少一组旧 Event stream、Snapshot、WorldPack、Branch、API fixture 作为兼容性金样。
- 记录当前生产 LOC、包数量、Registry/Manager/Service/Engine 数量。
- 生成 v5.2 baseline manifest 与语义哈希。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/V5_2_BASELINE_AUDIT.md`
- `tests/fixtures/v5_2_baseline/`

## 7. 实施任务

1. 读取 M17/M25 最终报告与 Git 历史，记录当前 commit/branch。
2. 执行全量现有质量套件并记录命令与结果。
3. 导出/固定至少一组旧 Event stream、Snapshot、WorldPack、Branch、API fixture 作为兼容性金样。
4. 记录当前生产 LOC、包数量、Registry/Manager/Service/Engine 数量。
5. 生成 v5.2 baseline manifest 与语义哈希。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 旧全量测试必须通过或把既有失败精确记录为 PRE_EXISTING_FAILURE。
- 金样必须可重复加载并计算同一 semantic hash。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29a: 冻结旧基线并验证 M25 真实状态`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29B_全仓代码处置实际盘点.md -->

# G29B — 全仓代码处置实际盘点

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把当前仓库真实文件/模块按 KEEP、MERGE、ADAPT、DELETE、REPLACE、EXPERIMENTAL 分类。

## 2. 范围

- 扫描 production packages、apps、migrations、tests、scripts。
- 识别重复 State/Event/Branch/Registry/Provider/Manager/Service/Engine。
- 识别未使用 Interface/Port/Adapter 与 dead code。
- 识别世界专用逻辑是否泄漏到 Core。
- 为每项 DELETE/MERGE 给出调用方与迁移策略，不凭名字删除。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/V5_2_CODE_DISPOSITION_ACTUAL.md`

## 7. 实施任务

1. 扫描 production packages、apps、migrations、tests、scripts。
2. 识别重复 State/Event/Branch/Registry/Provider/Manager/Service/Engine。
3. 识别未使用 Interface/Port/Adapter 与 dead code。
4. 识别世界专用逻辑是否泄漏到 Core。
5. 为每项 DELETE/MERGE 给出调用方与迁移策略，不凭名字删除。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 静态依赖图生成成功。
- 删除候选必须证明无运行时 consumer 或已有替代路径。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29b: 全仓代码处置实际盘点`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29C_合并重复 Registry 与 Manager.md -->

# G29C — 合并重复 Registry 与 Manager

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

减少重复运行时目录和全局查找机制，保留 PackageRegistry 与 RuntimeCapabilityCatalog 两类核心注册职责。

## 2. 范围

- 合并功能重叠 Registry。
- 删除 global service locator 式调用，改 composition root/显式注入。
- 合并薄 Manager/Service，纯逻辑改为 typed function/class。
- 保持公开 API 兼容或提供 deprecation shim。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 合并功能重叠 Registry。
2. 删除 global service locator 式调用，改 composition root/显式注入。
3. 合并薄 Manager/Service，纯逻辑改为 typed function/class。
4. 保持公开 API 兼容或提供 deprecation shim。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 架构测试禁止新增全局 mutable registry。
- 旧功能回归。
- Registry/Manager 数量不增加。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29c: 合并重复 Registry 与 Manager`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29D_统一 State Event Audit 派生关系.md -->

# G29D — 统一 State Event Audit 派生关系

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

确保只有 Committed History 权威，CurrentState、Projection、Audit view 均可由历史/ledger 重建或引用。

## 2. 范围

- 确认 CurrentState 是 materialized projection。
- 删除第二套 authoritative state path。
- 把重复 audit event 写入改为 World/Actor/Runtime Ledger 引用。
- 验证 projection cache 可丢弃重建。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 确认 CurrentState 是 materialized projection。
2. 删除第二套 authoritative state path。
3. 把重复 audit event 写入改为 World/Actor/Runtime Ledger 引用。
4. 验证 projection cache 可丢弃重建。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 删除 derived state 后可恢复。
- 无 route/provider 直接更新 canonical tables。
- replay hash 不变。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29d: 统一 State Event Audit 派生关系`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29E_收敛物理包边界.md -->

# G29E — 收敛物理包边界

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

在不制造无意义搬目录的前提下，把责任收敛到 Kernel/Runtime/Forge/Experiences/Infrastructure。

## 2. 范围

- 建立依赖方向 ADR。
- 能低风险移动的模块归位；高 churn 稳定模块可暂保留路径但暴露明确 namespace/ownership。
- 禁止 Kernel 依赖 Runtime/Forge/Web/ORM。
- 禁止 World 内容进入 Kernel。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 建立依赖方向 ADR。
2. 能低风险移动的模块归位；高 churn 稳定模块可暂保留路径但暴露明确 namespace/ownership。
3. 禁止 Kernel 依赖 Runtime/Forge/Web/ORM。
4. 禁止 World 内容进入 Kernel。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- import graph 无新增环。
- architecture tests 覆盖方向约束。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29e: 收敛物理包边界`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29F_清理 Fake Placeholder 与旧实验残留.md -->

# G29F — 清理 Fake Placeholder 与旧实验残留

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

删除会被误认为生产能力的假实现与失效实验路径。

## 2. 范围

- 扫描 TODO/FIXME/NotImplemented/pass/dummy/static success。
- 区分合法 test fake 与 production fake。
- 删除/隔离废弃 research feature flag。
- 更新 KNOWN_FAILURES。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 扫描 TODO/FIXME/NotImplemented/pass/dummy/static success。
2. 区分合法 test fake 与 production fake。
3. 删除/隔离废弃 research feature flag。
4. 更新 KNOWN_FAILURES。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 生产路径无影响当前 Goal acceptance 的 placeholder。
- test fake 均实现真实 contract。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29f: 清理 Fake Placeholder 与旧实验残留`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29G_建立最小代码度量与预算.md -->

# G29G — 建立最小代码度量与预算

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把代码最小性变成持续验收指标。

## 2. 范围

- 创建代码最小性 ledger。
- 统计 LOC、public types、Ports、Registries、Managers、Engines、循环依赖、重复 schema。
- 为 M27–M34 建立每阶段增量预算说明，不设武断绝对 LOC 上限。
- 新增抽象必须写理由。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 创建代码最小性 ledger。
2. 统计 LOC、public types、Ports、Registries、Managers、Engines、循环依赖、重复 schema。
3. 为 M27–M34 建立每阶段增量预算说明，不设武断绝对 LOC 上限。
4. 新增抽象必须写理由。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- CI/本地脚本可重复生成指标。
- 不存在无法解释的同义抽象。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29g: 建立最小代码度量与预算`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G29H_M26 收敛资格验收.md -->

# G29H — M26 收敛资格验收

> **Milestone**：M26  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明 v5.2 开发开始前仓库已经完成减法基线且旧能力未被破坏。

## 2. 范围

- 运行 M26 milestone gate。
- 修复所有内部 FAIL。
- 冻结新的 architecture map 与 baseline hash。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G29H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 运行 M26 milestone gate。
2. 修复所有内部 FAIL。
3. 冻结新的 architecture map 与 baseline hash。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 旧全量回归通过。
- 最小性报告存在。
- 代码处置表无未分类核心模块。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G29H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g29h: M26 收敛资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30A_Reality Root 语义契约.md -->

# G30A — Reality Root 语义契约

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

用现有核心类型表达 Distinction/Relation/Transition/Commitment/History，不创建第二套引擎。

## 2. 范围

- 建立 RealityRootContract/文档级 protocol，映射到 Identity/Fact/Event/Transition/Commit/Ledger。
- 明确 Reality Root 不含物理/魔法/领域规则。
- 为五项语义写 invariants 与 contract tests。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 建立 RealityRootContract/文档级 protocol，映射到 Identity/Fact/Event/Transition/Commit/Ledger。
2. 明确 Reality Root 不含物理/魔法/领域规则。
3. 为五项语义写 invariants 与 contract tests。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 任何世界类型均可通过同一契约构造最小 synthetic world。
- 没有新的 authoritative store。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30a: Reality Root 语义契约`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30B_World Constitution 模型与版本.md -->

# G30B — World Constitution 模型与版本

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

引入可版本化 Constitution，限定世界族根规则、身份/因果/时间/演化边界。

## 2. 范围

- 定义 ConstitutionId/Version/Manifest。
- 定义 immutable 根约束与可变 law layers 的边界。
- World Definition 引用 constitution_ref。
- 保存 provenance/rights/evolution-policy compatibility。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 ConstitutionId/Version/Manifest。
2. 定义 immutable 根约束与可变 law layers 的边界。
3. World Definition 引用 constitution_ref。
4. 保存 provenance/rights/evolution-policy compatibility。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- Constitution schema round-trip。
- 不同 Constitution 不共享可变对象。
- 旧 WorldPack 使用默认 legacy constitution 兼容。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30b: World Constitution 模型与版本`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30C_Constitution 执行与不可越权.md -->

# G30C — Constitution 执行与不可越权

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让 Commit 前验证可执行 Constitution 约束。

## 2. 范围

- 把 Constitution check 接入现有 Invariant Registry。
- Kernel invariant 优先于 Domain/World override。
- 普通 LawCommit 不得修改 Reality Root。
- World policy 不得提升自身到 platform authority。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 把 Constitution check 接入现有 Invariant Registry。
2. Kernel invariant 优先于 Domain/World override。
3. 普通 LawCommit 不得修改 Reality Root。
4. World policy 不得提升自身到 platform authority。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 尝试 world-level 修改 commit boundary 必须拒绝且无 state mutation。
- override kernel invariant 测试失败。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30c: Constitution 执行与不可越权`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30D_World Semantic ISA 最小类型.md -->

# G30D — World Semantic ISA 最小类型

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

实现 DECLARE/ASSERT/RETRACT/PROPOSE/VALIDATE/COMMIT/FORK/PROMOTE 的最小 typed semantic instruction，不建立平行 command bus。

## 2. 范围

- 定义 ISA enum/discriminated payload。
- 记录 instruction schema/version。
- 把 ISA 作为 compiler/domain/action 的归约目标。
- 保持业务 action 在上层。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 ISA enum/discriminated payload。
2. 记录 instruction schema/version。
3. 把 ISA 作为 compiler/domain/action 的归约目标。
4. 保持业务 action 在上层。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- schema round-trip。
- 未知 ISA version 明确失败。
- 无直接 DB write。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30d: World Semantic ISA 最小类型`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30E_ISA 到现有用例与 Commit 管线映射.md -->

# G30E — ISA 到现有用例与 Commit 管线映射

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把语义指令复用现有 command/proposal/delta/commit/replay。

## 2. 范围

- DECLARE 映射 identity creation proposal。
- ASSERT/RETRACT 映射 fact/relation transition。
- PROPOSE/VALIDATE/COMMIT 复用现有 pipeline。
- FORK 复用 Branch。
- PROMOTE 只生成 promotion use case，不直接 commit parent。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. DECLARE 映射 identity creation proposal。
2. ASSERT/RETRACT 映射 fact/relation transition。
3. PROPOSE/VALIDATE/COMMIT 复用现有 pipeline。
4. FORK 复用 Branch。
5. PROMOTE 只生成 promotion use case，不直接 commit parent。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 相同业务动作走旧入口与 ISA 入口产生相同 semantic outcome。
- 无第二套 Event stream。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30e: ISA 到现有用例与 Commit 管线映射`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30F_三类 World Commit 收敛.md -->

# G30F — 三类 World Commit 收敛

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

一个 CommitAuthority 支持 State/Ontology/Law 三类 payload，并彻底消除 CapabilityCommit 歧义。

## 2. 范围

- 统一 CommitRequest kind。
- Ontology/Law delta 各自版本化。
- Runtime control 变化使用 RuntimeControlTransaction。
- 保证失败原子性。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 统一 CommitRequest kind。
2. Ontology/Law delta 各自版本化。
3. Runtime control 变化使用 RuntimeControlTransaction。
4. 保证失败原子性。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- State/Ontology/Law 正向与负向测试。
- Capability provider activate 不产生 WorldCommit。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30f: 三类 World Commit 收敛`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30G_Fact Scope 与 Authority Partition.md -->

# G30G — Fact Scope 与 Authority Partition

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

统一 Fact 语义但保持 canonical/public/org/actor/hypothesis/reconstruction 的写权限隔离。

## 2. 范围

- 复用 Fact schema 加 scope policy。
- 禁止仅改 scope 把 belief 升级为 canonical。
- canonical promotion 必须走 Commit。
- Projection/Perception 根据 scope 与 rights 过滤。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 复用 Fact schema 加 scope policy。
2. 禁止仅改 scope 把 belief 升级为 canonical。
3. canonical promotion 必须走 Commit。
4. Projection/Perception 根据 scope 与 rights 过滤。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- actor belief 不泄漏 canonical。
- 跨角色偷看失败。
- scope elevation 绕过 Commit 被拒绝。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30g: Fact Scope 与 Authority Partition`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30H_Event Snapshot 版本上下文升级.md -->

# G30H — Event Snapshot 版本上下文升级

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让历史在 Constitution、Σ、Γ 演化后仍可解释和 Replay。

## 2. 范围

- 事件引用 constitution_version、semantic_space_version、law_set_version、domain/runtime refs（按需要最小化存储）。
- Snapshot 固化必要版本引用。
- 旧事件提供 legacy adapter。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 事件引用 constitution_version、semantic_space_version、law_set_version、domain/runtime refs（按需要最小化存储）。
2. Snapshot 固化必要版本引用。
3. 旧事件提供 legacy adapter。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- v5.0/v5.1 fixture replay。
- 新 Law/Ontology 前后 replay deterministic。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30h: Event Snapshot 版本上下文升级`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G30I_M27 Root Constitution ISA 资格验收.md -->

# G30I — M27 Root Constitution ISA 资格验收

> **Milestone**：M27  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明新增语义没有制造第二套内核且旧权威路径仍唯一。

## 2. 范围

- 运行 M27 Gate。
- 做架构与 mutation-path 搜索。
- 生成 root/constitution/ISA acceptance report。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G30I_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 运行 M27 Gate。
2. 做架构与 mutation-path 搜索。
3. 生成 root/constitution/ISA acceptance report。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 所有 Commit 仍进入单一 authority。
- 旧回放仍 PASS。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G30I_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g30i: M27 Root Constitution ISA 资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31A_World Definition 与 Worldline 身份模型.md -->

# G31A — World Definition 与 Worldline 身份模型

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把 WorldPack/Definition、Instance、Worldline/Branch、DerivedWorld 的身份关系正式化。

## 2. 范围

- 定义稳定 IDs 与引用。
- Branch 被建模为 Worldline fork 关系而非第二套历史对象。
- World Definition 只读版本化。
- Instance 记录 definition/genesis/constitution/runtime refs。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义稳定 IDs 与引用。
2. Branch 被建模为 Worldline fork 关系而非第二套历史对象。
3. World Definition 只读版本化。
4. Instance 记录 definition/genesis/constitution/runtime refs。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- parent/child identity round-trip。
- WorldPack 不因运行而变化。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31a: World Definition 与 Worldline 身份模型`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31B_World Lineage Graph 数据模型.md -->

# G31B — World Lineage Graph 数据模型

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

建立世界定义/世界线派生关系 DAG 的一等存储与查询。

## 2. 范围

- 定义 lineage node/edge。
- 支持 fork/promotion origin、inherited history ref、constitution/domain/runtime/evolution versions、rights/provenance。
- 防止循环谱系。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 lineage node/edge。
2. 支持 fork/promotion origin、inherited history ref、constitution/domain/runtime/evolution versions、rights/provenance。
3. 防止循环谱系。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 树与 DAG fixture。
- cycle insertion 被拒绝。
- 谱系查询可找 ancestor/descendant/common ancestor。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31b: World Lineage Graph 数据模型`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31C_Lineage Repository 与迁移.md -->

# G31C — Lineage Repository 与迁移

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

以最少新表/索引持久化谱系，不复制 Event history。

## 2. 范围

- 评估复用现有 world_definitions/branches 表。
- 增加必要 lineage edges/metadata。
- Alembic migration + downgrade/compatibility。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 评估复用现有 world_definitions/branches 表。
2. 增加必要 lineage edges/metadata。
3. Alembic migration + downgrade/compatibility。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- SQLite/PostgreSQL-compatible migration tests。
- 旧 DB 升级后 branch history 不变。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31c: Lineage Repository 与迁移`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31D_World Hypervisor 多实例隔离.md -->

# G31D — World Hypervisor 多实例隔离

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

在现有 World Host 上建立多 Instance/Worldline/RuntimeProfile 隔离语义，不新建第二个 Host。

## 2. 范围

- 复用 Host lifecycle。
- 增加 instance/worldline routing、resource budget、runtime profile binding。
- 所有 command 带明确 world/instance/worldline。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 复用 Host lifecycle。
2. 增加 instance/worldline routing、resource budget、runtime profile binding。
3. 所有 command 带明确 world/instance/worldline。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 两个实例同 ID 局部实体不互相污染。
- 并发 command 定位正确。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31d: World Hypervisor 多实例隔离`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31E_Interworld Identity 与 Presence.md -->

# G31E — Interworld Identity 与 Presence

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

支持跨世界存在引用但默认不双向同步历史。

## 2. 范围

- 定义 OriginIdentity/PresenceRef。
- 进入另一世界生成明确 presence/translation policy。
- 返回/同步必须显式 policy。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 OriginIdentity/PresenceRef。
2. 进入另一世界生成明确 presence/translation policy。
3. 返回/同步必须显式 policy。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- B 世界经历不写回 A。
- 身份冲突明确拒绝或映射。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31e: Interworld Identity 与 Presence`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31F_Hybrid Genesis 兼容性分析与安全拒绝.md -->

# G31F — Hybrid Genesis 兼容性分析与安全拒绝

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

首版支持世界合并前的语义检查，并在无法安全处理时拒绝，而不是伪造 Git merge。

## 2. 范围

- Constitution compatibility。
- Identity/Ontology/Law/Rights/History policy 检查。
- 输出 MergePlan Candidate 或 Rejection。
- 不要求自动解决任意冲突。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. Constitution compatibility。
2. Identity/Ontology/Law/Rights/History policy 检查。
3. 输出 MergePlan Candidate 或 Rejection。
4. 不要求自动解决任意冲突。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 不兼容 constitution 拒绝。
- rights conflict 拒绝。
- parent histories 不被改写。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31f: Hybrid Genesis 兼容性分析与安全拒绝`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31G_Lineage API SDK Studio 最小投影.md -->

# G31G — Lineage API SDK Studio 最小投影

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

暴露谱系查询与世界树/DAG 调试视图，复用现有 Graph UI。

## 2. 范围

- API：ancestor/descendant/promotion origin。
- SDK types 从 OpenAPI 生成。
- Studio 使用共享 graph component。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. API：ancestor/descendant/promotion origin。
2. SDK types 从 OpenAPI 生成。
3. Studio 使用共享 graph component。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- API contract tests。
- UI 不持有 authority。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31g: Lineage API SDK Studio 最小投影`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G31H_M28 Lineage Hypervisor 资格验收.md -->

# G31H — M28 Lineage Hypervisor 资格验收

> **Milestone**：M28  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明多个世界、世界线和派生关系隔离且可追溯。

## 2. 范围

- 运行 M28 Gate。
- 生成 lineage graph fixture 与可视化证据。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G31H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 运行 M28 Gate。
2. 生成 lineage graph fixture 与可视化证据。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- parent 不被 child/promotion 修改。
- 多实例 replay 独立。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G31H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g31h: M28 Lineage Hypervisor 资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32A_Evolution Policy Stack.md -->

# G32A — Evolution Policy Stack

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把单一 Λ 展开为 World/Platform 分层策略并接入运行时。

## 2. 范围

- 定义 Actor/Capability/Social/Institution/Ontology/Law/Promotion policy。
- 定义 Platform Model/Plugin/Domain/Runtime/Constitution migration policy。
- World/Platform 权限独立。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 Actor/Capability/Social/Institution/Ontology/Law/Promotion policy。
2. 定义 Platform Model/Plugin/Domain/Runtime/Constitution migration policy。
3. World/Platform 权限独立。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- world policy 不能调用 platform mutation。
- policy version 可追溯。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32a: Evolution Policy Stack`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32B_多尺度演化调度.md -->

# G32B — 多尺度演化调度

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

复用 Scheduler，让 Actor/Relation/Group/Institution/World 以不同时间尺度评估变化。

## 2. 范围

- 定义 evolution cadence/policy。
- 避免每 tick 全量扫描。
- 只激活受影响实体/窗口。
- 背景聚合复用 Population Resolution。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 evolution cadence/policy。
2. 避免每 tick 全量扫描。
3. 只激活受影响实体/窗口。
4. 背景聚合复用 Population Resolution。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 同 seed/cadence deterministic。
- 长运行无指数任务爆炸。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32b: 多尺度演化调度`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32C_Actor Capability 与 Persona 演化分离.md -->

# G32C — Actor Capability 与 Persona 演化分离

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

保证学会技能不会自动重写人格。

## 2. 范围

- 复用 CapabilityDelta/PersonaDelta。
- 不同 evolution policy/cadence。
- 记录 trajectory provenance。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 复用 CapabilityDelta/PersonaDelta。
2. 不同 evolution policy/cadence。
3. 记录 trajectory provenance。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- skill gain 不改变 persona hash（除显式 persona event）。
- 长期人格变化有事件链。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32c: Actor Capability 与 Persona 演化分离`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32D_Relation Group Social Pattern Distillation.md -->

# G32D — Relation Group Social Pattern Distillation

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

从重复行为历史生成关系/群体/规范候选，不直接写 Canon。

## 2. 范围

- 复用 Evolutionary Distillation。
- 窗口化 pattern detection。
- 输出 CandidateEnvelope + origin/provenance。
- 稳定性阈值由 policy 控制。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 复用 Evolutionary Distillation。
2. 窗口化 pattern detection。
3. 输出 CandidateEnvelope + origin/provenance。
4. 稳定性阈值由 policy 控制。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 单次行为不能升级制度。
- 多窗口稳定 pattern 可形成 candidate。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32d: Relation Group Social Pattern Distillation`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32E_Institution Organization Rule 晋升.md -->

# G32E — Institution Organization Rule 晋升

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

实现从群体模式到制度候选、验证、LawCommit 的受控链。

## 2. 范围

- 定义 institution candidate evidence。
- 接入 counterfactual/stability tests。
- 人工/政策 approval hook。
- 成功后 LawCommit。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 institution candidate evidence。
2. 接入 counterfactual/stability tests。
3. 人工/政策 approval hook。
4. 成功后 LawCommit。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 未批准 candidate 不改变 Γ。
- LawCommit 可 replay。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32e: Institution Organization Rule 晋升`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32F_Ontology Law 多尺度演化.md -->

# G32F — Ontology Law 多尺度演化

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把 v5.1 Ontology/Law Evolution 接入 Constitution 与 Policy。

## 2. 范围

- OntologyCandidate 稳定性/复杂度/可解释性。
- LawCandidate 权限与 scope。
- Constitution 决定哪些层可变。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. OntologyCandidate 稳定性/复杂度/可解释性。
2. LawCandidate 权限与 scope。
3. Constitution 决定哪些层可变。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- Realistic constitution 禁止非法根规则。
- branch-local ontology/law 不污染 parent。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32f: Ontology Law 多尺度演化`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32G_Evolution Telemetry 与隐私权利.md -->

# G32G — Evolution Telemetry 与隐私权利

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

为跨世界学习准备最小授权数据面，不采集不必要敏感内容。

## 2. 范围

- 定义 telemetry envelope。
- 默认 metadata/hash/aggregate；敏感 actor trajectory 受 retention/rights。
- opt-in/consent/rights policy。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 telemetry envelope。
2. 默认 metadata/hash/aggregate；敏感 actor trajectory 受 retention/rights。
3. opt-in/consent/rights policy。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 未授权世界数据不进入 cross-world dataset。
- 删除/撤销策略测试。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32g: Evolution Telemetry 与隐私权利`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G32H_M29 多尺度共演化资格验收.md -->

# G32H — M29 多尺度共演化资格验收

> **Milestone**：M29  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明微观→宏观候选→制度/本体变更可受控运行，平台权力仍隔离。

## 2. 范围

- 构造 synthetic 社会长运行。
- 验证 habit→norm→institution candidate。
- 运行 M29 Gate。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G32H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 构造 synthetic 社会长运行。
2. 验证 habit→norm→institution candidate。
3. 运行 M29 Gate。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 没有自动跨越高层 Gate。
- Replay/Branch 仍确定。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G32H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g32h: M29 多尺度共演化资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33A_统一 Abstraction Ladder.md -->

# G33A — 统一 Abstraction Ladder

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

实现 L0 Event→L8 Platform Improvement 的候选等级与证据要求。

## 2. 范围

- 定义 promotion level/value object。
- 每级最小证据、稳定性、跨场景、审批 requirement。
- L0-L3 可更自动，L7-L8 强制显式批准。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 定义 promotion level/value object。
2. 每级最小证据、稳定性、跨场景、审批 requirement。
3. L0-L3 可更自动，L7-L8 强制显式批准。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 越级 promotion 被拒绝。
- policy 可版本化。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33a: 统一 Abstraction Ladder`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33B_Worldline 到 Derived World Promotion Pipeline.md -->

# G33B — Worldline 到 Derived World Promotion Pipeline

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把成熟 Worldline 安全冻结/蒸馏为新 World Definition。

## 2. 范围

- Long-horizon distill。
- Source/Rights/Invariant review。
- freeze Genesis snapshot。
- Package Assembler 编译 candidate。
- approval 后创建新 Definition ID 与 lineage edge。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. Long-horizon distill。
2. Source/Rights/Invariant review。
3. freeze Genesis snapshot。
4. Package Assembler 编译 candidate。
5. approval 后创建新 Definition ID 与 lineage edge。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- Parent definition/source worldline hash 不变。
- derived world 可重新 instantiate。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33b: Worldline 到 Derived World Promotion Pipeline`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33C_Promotion 可重放与可撤销控制.md -->

# G33C — Promotion 可重放与可撤销控制

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让 promotion 决策可审计，撤销发布不改写源世界历史。

## 2. 范围

- promotion record 写 Runtime/Forge control ledger。
- 取消/撤回仅影响可安装性/registry status。
- 不删除源 history。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. promotion record 写 Runtime/Forge control ledger。
2. 取消/撤回仅影响可安装性/registry status。
3. 不删除源 history。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- withdraw derived definition 不影响 parent replay。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33c: Promotion 可重放与可撤销控制`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33D_Cross-world Distillation.md -->

# G33D — Cross-world Distillation

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

从多个授权世界历史形成 Domain/Runtime Candidate。

## 2. 范围

- 只读取授权 telemetry/evaluation。
- 跨世界 pattern discovery 使用 CandidateEnvelope。
- 保留世界来源与匿名/权限策略。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 只读取授权 telemetry/evaluation。
2. 跨世界 pattern discovery 使用 CandidateEnvelope。
3. 保留世界来源与匿名/权限策略。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 无授权数据被过滤。
- candidate 不直接 activate。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33d: Cross-world Distillation`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33E_平台反哺 Sandbox Benchmark Approval.md -->

# G33E — 平台反哺 Sandbox Benchmark Approval

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

复用现有 Runtime Evolution Lab 验证跨世界候选。

## 2. 范围

- shadow/sandbox run。
- benchmark/ablation/invariant/security/cost/determinism。
- approval policy。
- 通过后 versioned Domain/Runtime release。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. shadow/sandbox run。
2. benchmark/ablation/invariant/security/cost/determinism。
3. approval policy。
4. 通过后 versioned Domain/Runtime release。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- world instance 不拥有批准平台升级权限。
- rollback 不改写过去 World Events。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33e: 平台反哺 Sandbox Benchmark Approval`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33F_Lineage 与 Promotion API Studio.md -->

# G33F — Lineage 与 Promotion API Studio

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

提供 Promote、Derived World、Lineage Compare 的最小使用面。

## 2. 范围

- thin API use cases。
- Studio 显示 candidate/approval/lineage diff。
- 权限控制。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. thin API use cases。
2. Studio 显示 candidate/approval/lineage diff。
3. 权限控制。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 无权限 promote 被拒绝。
- UI action 经 backend authority。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33f: Lineage 与 Promotion API Studio`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G33G_M30 Promotion Cross-world 资格验收.md -->

# G33G — M30 Promotion Cross-world 资格验收

> **Milestone**：M30  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明世界能生出世界，世界经验能产生平台候选，但无直接写权限。

## 2. 范围

- synthetic worldline promotion end-to-end。
- cross-world candidate end-to-end。
- 运行 M30 Gate。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G33G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. synthetic worldline promotion end-to-end。
2. cross-world candidate end-to-end。
3. 运行 M30 Gate。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- derived definition 可实例化。
- platform candidate 未审批不生效。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G33G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g33g: M30 Promotion Cross-world 资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34A_Kernel Runtime Forge Experiences 责任收敛.md -->

# G34A — Kernel Runtime Forge Experiences 责任收敛

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

完成最终责任边界，避免 v5.2 概念继续增加平行大系统。

## 2. 范围

- 更新 architecture docs/import rules。
- Reality Root/ISA/Authority 属 Kernel。
- Host/Living/Agent/Sim 属 Runtime。
- Source/Distill/Genesis/Evolve/Promote 属 Forge。
- Session/Embodiment/Projection 属 Experiences。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 更新 architecture docs/import rules。
2. Reality Root/ISA/Authority 属 Kernel。
3. Host/Living/Agent/Sim 属 Runtime。
4. Source/Distill/Genesis/Evolve/Promote 属 Forge。
5. Session/Embodiment/Projection 属 Experiences。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 依赖图符合边界。
- 不存在新 God Engine。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34a: Kernel Runtime Forge Experiences 责任收敛`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34B_WorldPack Definition schema v5.2 迁移.md -->

# G34B — WorldPack Definition schema v5.2 迁移

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

增加 Constitution/Genesis/Evolution/Lineage refs，同时保持旧包可导入。

## 2. 范围

- schema version bump。
- legacy adapter。
- package migration CLI/use case。
- checksum/signature 规则更新。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. schema version bump。
2. legacy adapter。
3. package migration CLI/use case。
4. checksum/signature 规则更新。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 旧包 round-trip。
- 新包 export/import semantic equivalence。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34b: WorldPack Definition schema v5.2 迁移`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34C_数据库与 Ledger 兼容迁移.md -->

# G34C — 数据库与 Ledger 兼容迁移

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

完成 v5.2 持久化升级且不丢历史。

## 2. 范围

- Alembic migrations。
- lineage/constitution/evolution metadata。
- 索引与唯一约束。
- 备份/恢复路径。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. Alembic migrations。
2. lineage/constitution/evolution metadata。
3. 索引与唯一约束。
4. 备份/恢复路径。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 旧 DB copy 升级。
- downgrade/restore strategy。
- event count/hash 不变。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34c: 数据库与 Ledger 兼容迁移`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34D_旧 Event Snapshot Branch 向后回放.md -->

# G34D — 旧 Event Snapshot Branch 向后回放

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

用 M26 金样证明 v5.2 对旧世界历史兼容。

## 2. 范围

- restore old snapshot。
- replay old events。
- fork old branch under v5.2。
- 新字段通过 legacy defaults/adapter。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. restore old snapshot。
2. replay old events。
3. fork old branch under v5.2。
4. 新字段通过 legacy defaults/adapter。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- semantic hash 与 baseline 一致。
- 无数据清空捷径。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34d: 旧 Event Snapshot Branch 向后回放`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34E_API SDK Client 兼容.md -->

# G34E — API SDK Client 兼容

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

为 v5.2 新资源扩展 API，同时避免破坏已用客户端。

## 2. 范围

- 新增 constitution/lineage/promotion endpoints。
- 生成 TS SDK。
- 保留旧 world/branch endpoints 或 deprecation adapter。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 新增 constitution/lineage/promotion endpoints。
2. 生成 TS SDK。
3. 保留旧 world/branch endpoints 或 deprecation adapter。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- OpenAPI diff review。
- 旧 client smoke tests。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34e: API SDK Client 兼容`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34F_性能与复杂度回归.md -->

# G34F — 性能与复杂度回归

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

确保 v5.2 抽象没有显著增加普通 world tick/commit/replay 开销。

## 2. 范围

- 基线比较 commit/replay/tick。
- lineage query 单独计量。
- 删掉不必要 middleware/indirection。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 基线比较 commit/replay/tick。
2. lineage query 单独计量。
3. 删掉不必要 middleware/indirection。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 关键路径无无法解释的大幅退化。
- code minimality ledger 更新。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34f: 性能与复杂度回归`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G34G_M31 全平台兼容资格验收.md -->

# G34G — M31 全平台兼容资格验收

> **Milestone**：M31  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

冻结可用于真实参考世界的 v5.2 平台。

## 2. 范围

- 运行全测试、迁移、replay、architecture、SDK、security。
- 生成 backward compatibility report。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G34G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 运行全测试、迁移、replay、architecture、SDK、security。
2. 生成 backward compatibility report。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- M26 baseline 全部可解释通过。
- 无 P0/P1 架构 GAP。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G34G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g34g: M31 全平台兼容资格验收`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35A_红楼梦来源策略与合法版本登记.md -->

# G35A — 红楼梦来源策略与合法版本登记

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

取得并登记一个可合法使用、可追溯、可校验的《红楼梦》文本版本，作为真实 WorldPack Source Gate。

## 2. 范围

- 优先使用用户已有合法文本；否则在执行环境允许时取得明确 public-domain/合法授权版本。
- 保存 source record、URI/文件、checksum、版本/版次、rights note。
- 禁止模型记忆代替文本。
- 若完全无法取得则记录 EXTERNAL_BLOCKED 并继续通用任务。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/RED_CHAMBER_SOURCE_GATE.md`

## 7. 实施任务

1. 优先使用用户已有合法文本；否则在执行环境允许时取得明确 public-domain/合法授权版本。
2. 保存 source record、URI/文件、checksum、版本/版次、rights note。
3. 禁止模型记忆代替文本。
4. 若完全无法取得则记录 EXTERNAL_BLOCKED 并继续通用任务。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- source checksum 可重复。
- rights/review_status 非空。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35a: 红楼梦来源策略与合法版本登记`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35B_章节分段与可引用 Source Locator.md -->

# G35B — 章节分段与可引用 Source Locator

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

把来源转换为可稳定引用的 chapter/segment locator，不破坏原始文本。

## 2. 范围

- parse/segment。
- 保留 source offsets/章节编号。
- 生成引用 locator。
- 原文不被自动改写。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. parse/segment。
2. 保留 source offsets/章节编号。
3. 生成引用 locator。
4. 原文不被自动改写。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 任意 Canon claim 可回链 source locator。
- 重跑 parser locator 稳定。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35b: 章节分段与可引用 Source Locator`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35C_人物与别名 Identity Distillation.md -->

# G35C — 人物与别名 Identity Distillation

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

基于来源生成林黛玉、贾宝玉、紫鹃和所选切片人物候选，解决别名/称谓而不合并不同身份。

## 2. 范围

- Entity/Identity Distiller。
- alias claims 带 evidence。
- 人工/规则 review gate。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. Entity/Identity Distiller。
2. alias claims 带 evidence。
3. 人工/规则 review gate。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 同名/别名解析测试。
- 无 evidence candidate 不进入 Canon。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35c: 人物与别名 Identity Distillation`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35D_空间组织物品 Distillation.md -->

# G35D — 空间组织物品 Distillation

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

为潇湘馆、怡红院、公共路径、组织、信件/药物/礼物等建立来源绑定候选。

## 2. 范围

- Place/Relation/Object distillers。
- 建立可运行所需拓扑 candidate。
- 无法直接证实的细节进入 Completion。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. Place/Relation/Object distillers。
2. 建立可运行所需拓扑 candidate。
3. 无法直接证实的细节进入 Completion。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- E0 与 E1-E5 分类正确。
- 空间补全不冒充原文。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35d: 空间组织物品 Distillation`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35E_Past Character Future Canon 编译.md -->

# G35E — Past Character Future Canon 编译

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

建立三层 Canon 并防止未来知识泄漏。

## 2. 范围

- 选择具体 Scenario 时点。
- PastCanon claims。
- CharacterCanon。
- FutureCanon 仅 control plane 可见。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 选择具体 Scenario 时点。
2. PastCanon claims。
3. CharacterCanon。
4. FutureCanon 仅 control plane 可见。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 角色 Perception 不含 FutureCanon。
- canon lock/soft/open policy contract tests。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35e: Past Character Future Canon 编译`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35F_Narrative Household HistoricalChina Domain 复用与补齐.md -->

# G35F — Narrative Household HistoricalChina Domain 复用与补齐

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

复用现有 Domain Pack，只补红楼梦切片真正需要的 action/rule/institution/schedule。

## 2. 范围

- 禁止创建 RedChamberCore。
- 缺失 action 定义在 Domain Pack。
- 礼制/职责/访问权限/传话/探病/书信 resolver。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 禁止创建 RedChamberCore。
2. 缺失 action 定义在 Domain Pack。
3. 礼制/职责/访问权限/传话/探病/书信 resolver。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- Domain 单元/合同/replay tests。
- 其他 synthetic world 可安装 Domain 而无红楼梦专名。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35f: Narrative Household HistoricalChina Domain 复用与补齐`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35G_Character Relation Knowledge Boundary Distillation.md -->

# G35G — Character Relation Knowledge Boundary Distillation

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

构建可运行角色模型而不是性格标签或共享向量库。

## 2. 范围

- 人物 life-stage/persona evidence。
- relation claims。
- knowledge boundary。
- 私密/公共事实 scope。
- Completion/Interpretive 分离。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 人物 life-stage/persona evidence。
2. relation claims。
3. knowledge boundary。
4. 私密/公共事实 scope。
5. Completion/Interpretive 分离。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 匿名关键选择 fixture。
- 知识泄漏测试。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35g: Character Relation Knowledge Boundary Distillation`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35H_Completion Ledger 与审核.md -->

# G35H — Completion Ledger 与审核

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

补齐运行所需但来源未明示的内容并全量标注 E0-E5。

## 2. 范围

- completion records。
- support refs/confidence/review status。
- can_enter_canon 默认 false。
- 批量审核 CLI/API/Studio use case。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G35H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. completion records。
2. support refs/confidence/review status。
3. can_enter_canon 默认 false。
4. 批量审核 CLI/API/Studio use case。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- E4/E5 永不自动升级 E0。
- 冲突 Claim 保留。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35h: Completion Ledger 与审核`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G35I_编译 RedChamber World Definition 与 Scenario.md -->

# G35I — 编译 RedChamber World Definition 与 Scenario

> **Milestone**：M32  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

通过正常 Forge/Package pipeline 生成可安装的 dream_of_the_red_chamber 最小 WorldPack 和固定 Scenario。

## 2. 范围

- PackageAssembler。
- constitution_ref 使用适合文学历史世界的 realistic/literary constitution。
- GenesisSpec。
- Evolution policies refs。
- 签名/哈希/依赖。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/RED_CHAMBER_WORLD_PACK_ACCEPTANCE.md`

## 7. 实施任务

1. PackageAssembler。
2. constitution_ref 使用适合文学历史世界的 realistic/literary constitution。
3. GenesisSpec。
4. Evolution policies refs。
5. 签名/哈希/依赖。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- package validate/install/export/import。
- 实例化 dry-run。
- 无 Core hardcode。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G35I_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g35i: 编译 RedChamber World Definition 与 Scenario`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36A_实例化 RC-001 与固定世界快照.md -->

# G36A — 实例化 RC-001 与固定世界快照

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

从真实 World Definition + Scenario 创建 RC-001，不使用手写当前状态。

## 2. 范围

- resolve domains/runtime profile。
- Genesis/instantiate。
- 生成 initial snapshot。
- 记录 lineage root。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36A_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. resolve domains/runtime profile。
2. Genesis/instantiate。
3. 生成 initial snapshot。
4. 记录 lineage root。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- initial semantic hash 稳定。
- WorldPack 文件未被 runtime 修改。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36a: 实例化 RC-001 与固定世界快照`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36B_红楼梦空间可见可听私密运行.md -->

# G36B — 红楼梦空间可见可听私密运行

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让潇湘馆、怡红院、路径和公共空间通过已有 Spatial Substrate 真实运行。

## 2. 范围

- portal/path/access。
- visibility/acoustic/privacy。
- 移动时间。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. portal/path/access。
2. visibility/acoustic/privacy。
3. 移动时间。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 穿墙/瞬移/隔院全听见负向测试。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36b: 红楼梦空间可见可听私密运行`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36C_人物职责 NPC 日程身体与社会制度.md -->

# G36C — 人物职责 NPC 日程身体与社会制度

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让 5 名主要人物与 10–20 名职责 NPC 能在无用户输入时按规则生活。

## 2. 范围

- 角色实例与 controllers。
- schedule/duty/body/meal/rest/visit。
- population resolution。
- deterministic background policy。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 角色实例与 controllers。
2. schedule/duty/body/meal/rest/visit。
3. population resolution。
4. deterministic background policy。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 无 LLM 模式七日可推进。
- 职责/权限越权被拒绝。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36c: 人物职责 NPC 日程身体与社会制度`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36D_信件诗稿礼物药物的物质与信息连续性.md -->

# G36D — 信件诗稿礼物药物的物质与信息连续性

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明红楼梦不是聊天上下文：物品有位置、保管、所有权和阅读状态。

## 2. 范围

- instantiate objects。
- delivery/hide/read/seal/gift/medicine actions。
- 阅读才形成 observation/memory。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. instantiate objects。
2. delivery/hide/read/seal/gift/medicine actions。
3. 阅读才形成 observation/memory。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 同一信件不能在两处。
- 获得信件不自动知道内容。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36d: 信件诗稿礼物药物的物质与信息连续性`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36E_Perception Belief Memory 与消息传播.md -->

# G36E — Perception Belief Memory 与消息传播

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让每个角色只能根据自身 observation/belief/memory 行动。

## 2. 范围

- PerceptionEnvelope。
- message propagation chain。
- rumour/misunderstanding。
- future canon isolation。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. PerceptionEnvelope。
2. message propagation chain。
3. rumour/misunderstanding。
4. future canon isolation。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 紫鹃传话后未接触者不能自动知道。
- 切换角色不回流私密知识。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36e: Perception Belief Memory 与消息传播`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36F_林黛玉 Embodiment ShadowPolicy Handoff.md -->

# G36F — 林黛玉 Embodiment ShadowPolicy Handoff

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

完成用户接管林黛玉、退出后 AI 接管、再进入恢复的完整控制链。

## 2. 范围

- acquire/release lease。
- intent/co-drive/full-control modes。
- ShadowPolicy 不替重大决定。
- ControlHandoffEvent。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. acquire/release lease。
2. intent/co-drive/full-control modes。
3. ShadowPolicy 不替重大决定。
4. ControlHandoffEvent。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 唯一 lease。
- AI 与用户不争夺身体。
- 退出后后果被 AI 继承。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36f: 林黛玉 Embodiment ShadowPolicy Handoff`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36G_Canonical Replay Soft Canon Living Open 三策略.md -->

# G36G — Canonical Replay Soft Canon Living Open 三策略

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

使用同一 Runtime、不同 EvolutionPolicy 支持三种红楼梦运行模式。

## 2. 范围

- policy configs。
- canonical locks。
- soft attractor/condition。
- open branch baseline comparison。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. policy configs。
2. canonical locks。
3. soft attractor/condition。
4. open branch baseline comparison。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 三个模式无复制 runtime。
- open mode 不修改 original World Definition。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36g: Canonical Replay Soft Canon Living Open 三策略`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G36H_红楼梦 Experience Studio 最小可用面.md -->

# G36H — 红楼梦 Experience Studio 最小可用面

> **Milestone**：M33  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

让用户可进入、观察、行动、查看时间线/分支/来源，而 UI 不拥有世界真相。

## 2. 范围

- 复用 web app/shared components。
- 地图/人物/可用动作/事件/来源/branch compare。
- Studio source/completion/debug view。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G36H_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 复用 web app/shared components。
2. 地图/人物/可用动作/事件/来源/branch compare。
3. Studio source/completion/debug view。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- Playwright E2E。
- 刷新/重连从 server projection 重建。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G36H_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g36h: 红楼梦 Experience Studio 最小可用面`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37A_红楼梦七日场景自动化执行.md -->

# G37A — 红楼梦七日场景自动化执行

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

完整执行设计规定的 Day1–Day7 场景并保留所有证据。

## 2. 范围

- 固定快照。
- Day1 接管黛玉并委托紫鹃传话。
- Day3 退出 AI 接管并 fork。
- 运行到 Day7。
- 保留 deterministic/no-LLM reference run 与可选 LLM run 分离。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/RED_CHAMBER_7_DAY_ACCEPTANCE.md`

## 7. 实施任务

1. 固定快照。
2. Day1 接管黛玉并委托紫鹃传话。
3. Day3 退出 AI 接管并 fork。
4. 运行到 Day7。
5. 保留 deterministic/no-LLM reference run 与可选 LLM run 分离。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 七日 14 项验收逐项 PASS。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37A_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37a: 红楼梦七日场景自动化执行`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37B_Canon 用户 无干预三世界线比较.md -->

# G37B — Canon 用户 无干预三世界线比较

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

证明同一 Genesis 可产生隔离历史并进行 semantic diff。

## 2. 范围

- 生成/保留三 worldlines。
- compare state/history/relations/beliefs/items。
- parent hash verification。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37B_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 生成/保留三 worldlines。
2. compare state/history/relations/beliefs/items。
3. parent hash verification。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- child mutation 不污染其他 worldline。
- diff 可追溯到 events。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37B_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37b: Canon 用户 无干预三世界线比较`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37C_红楼梦长时演化与 Promotion Candidate.md -->

# G37C — 红楼梦长时演化与 Promotion Candidate

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

用加速时间/合成长期窗口证明 Living/Open 世界可产生候选派生世界，但不改写原著。

## 2. 范围

- 长期运行或受控 time-acceleration。
- Distill stable relationship/habit/institution/world structure。
- 生成 promotion candidate。
- 仅在达到 policy gate 时创建 Derived World Definition。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37C_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 长期运行或受控 time-acceleration。
2. Distill stable relationship/habit/institution/world structure。
3. 生成 promotion candidate。
4. 仅在达到 policy gate 时创建 Derived World Definition。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 原 World Definition hash 不变。
- Derived world lineage 可追溯。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37C_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37c: 红楼梦长时演化与 Promotion Candidate`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37D_红楼梦 Replay Crash Recovery Chaos.md -->

# G37D — 红楼梦 Replay Crash Recovery Chaos

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

验证真实实例在崩溃、恢复、重复命令、stale revision 和回放下不破坏世界现实。

## 2. 范围

- snapshot/restart。
- corrupt stream detection。
- duplicate/stale tests。
- client reconnect。
- provider failure isolation。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37D_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. snapshot/restart。
2. corrupt stream detection。
3. duplicate/stale tests。
4. client reconnect。
5. provider failure isolation。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 恢复后 semantic hash 一致。
- 无半提交。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37D_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37d: 红楼梦 Replay Crash Recovery Chaos`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37E_v5.2 全仓最小代码与架构终审.md -->

# G37E — v5.2 全仓最小代码与架构终审

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

确认实现完整设计的同时没有因 v5.2 再膨胀出重复系统。

## 2. 范围

- 更新 LOC/abstract types/registry/manager/engine metrics。
- 检查循环依赖/giant files/dead interfaces。
- 对新增抽象逐项写 justification。
- 删除最终可删 compatibility 临时代码（仅在安全时）。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37E_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 更新 LOC/abstract types/registry/manager/engine metrics。
2. 检查循环依赖/giant files/dead interfaces。
3. 对新增抽象逐项写 justification。
4. 删除最终可删 compatibility 临时代码（仅在安全时）。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 无 P0/P1 duplication。
- 核心包依赖方向通过。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37E_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37e: v5.2 全仓最小代码与架构终审`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37F_全量回归与最终追溯矩阵.md -->

# G37F — 全量回归与最终追溯矩阵

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

从 v5.2 母版要求反查代码、测试、运行证据。

## 2. 范围

- 建立 design requirement→code→test→evidence。
- 运行 Python/TS/DB/API/E2E/security/replay/lineage/promotion/red chamber 全量套件。
- 记录外部阻塞。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37F_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 建立 design requirement→code→test→evidence。
2. 运行 Python/TS/DB/API/E2E/security/replay/lineage/promotion/red chamber 全量套件。
3. 记录外部阻塞。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- 所有内部项 PASS。
- 不得用文件存在代替运行证据。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37F_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37f: 全量回归与最终追溯矩阵`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: goals/G37G_v5.2 与 RedChamber 最终认证并停止.md -->

# G37G — v5.2 与 RedChamber 最终认证并停止

> **Milestone**：M34  
> **执行顺序**：按 `06_M26_M34_GOAL总索引.md`  
> **完成状态**：仅允许 `PASS / FAIL / EXTERNAL_BLOCKED / NOT_APPLICABLE`

## 1. 目标

在所有 Gate 通过后生成最终认证，本地 checkpoint，然后停止，不自行发明下一阶段。

## 2. 范围

- 生成 final certification/report。
- 确认 working tree。
- 创建本地 commit/tag（可选 tag）。
- 不 push、不 deploy。

## 3. 非目标

- 不重写与本 Goal 无语义冲突且已通过回归的稳定代码。
- 不提前实现后续 Goal 的完整功能。
- 不通过降低测试、跳过迁移或引入硬编码来快速“完成”。

## 4. 必读

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
- `00_V5_2_代码处置与复用矩阵.md`
- `01_V5_2_全量工程程序架构.md`
- `02_CODEX_V5_2_今晚连续执行总指令.md`
- `03_最小代码工程宪法.md`
- `04_V5_2_架构裁决与歧义消解.md`
- `05_M0_M25到V5_2迁移映射.md`
- `06_M26_M34_GOAL总索引.md`
- `07_M26_M34_Milestone验收门.md`
- `08_连续执行与中断恢复协议.md`
- `09_红楼梦SourceGate与实例验收标准.md`
- `10_V5_2最终验收证据标准.md`
- 仓库现有 `AGENTS.md / PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md`
- 现有 `reports/`、Git 历史、迁移、测试和 M17/M25 最终认证报告（若存在）

并读取：
- 当前 Goal 之前所有同 Milestone Goal 的报告；
- 与本 Goal 直接相关的现有源码、tests、migrations、ADR；
- `git status` 与最近至少 20 条 commit。

## 5. 架构硬约束

- 现有已通过测试的 M0–M25 能力默认 KEEP/ADAPT；除非有可复现证据证明语义冲突，不得重写。
- 唯一 Canonical Mutation Boundary 保持不变；LLM、Agent、UI、Compiler、Sensor、Simulator、Provider 都不得直接写权威状态。
- Reality Root 是语义基岩，不创建第二套状态内核、第二套事件存储或第二套 CommitAuthority。
- World Semantic ISA 是语义归约层，不允许演化成巨型解释器或平行数据库 API。
- Branch 与 Worldline 复用同一历史隔离机制；不得复制出第二套分支系统。
- World Definition/World Pack 是版本化出生定义；运行历史只进入 Instance/Worldline，不静默写回母本。
- Runtime Capability 变化写 Runtime Control Ledger，不创造 CapabilityCommit 作为第四类 World Commit。
- World Policy 与 Platform Policy 严格隔离；任何世界实例不得修改 Reality Root 或平台宪法。
- 模块化单体优先；逻辑 Kernel 不等于微服务。
- 默认生产源文件目标 ≤300 行；超出必须拆分或在 DECISIONS 中留下具体理由。
- 不得以 TODO、placeholder、mock-only、静态 JSON、硬编码成功路径冒充完成。
- 核心测试、Replay、Branch、Source Gate、红楼梦七日验收不得依赖外部 LLM key。

## 6. 交付物

- `reports/G37G_REPORT.md`
- 实现代码、测试、必要 migration/fixture、更新后的工程 ledgers

## 7. 实施任务

1. 生成 final certification/report。
2. 确认 working tree。
3. 创建本地 commit/tag（可选 tag）。
4. 不 push、不 deploy。

实现时必须先复用现有能力；若发现两个以上等价实现，优先合并，不得再新增第三个 abstraction。任何删除都必须先有测试/调用关系证据。

## 8. 测试

- M34 PASS 条件全部满足。
- 若 RedChamber Source Gate blocked，不得写 RED_CHAMBER_COMPLETE。

此外必须运行所有适用的：
- 与本模块相关的 unit / property / contract / integration / E2E；
- architecture conformance；
- replay / branch / determinism regression；
- migration compatibility；
- Ruff + format + typecheck；
- 前端存在改动时 lint + typecheck + unit + build + Playwright；
- 任何失败不得通过 skip、删除断言或改成 expected failure 掩盖。

## 9. 验收标准

- 本 Goal 的所有 Scope 已有真实实现或合法 `EXTERNAL_BLOCKED` 证据。
- 所有列出的 Tests 有可复现 PASS 证据。
- 不存在影响本 Goal 的 TODO/FIXME/placeholder/mock-only production path。
- 没有新增绕过 Commit Boundary 的写路径。
- 没有无理由增加重复 Registry/Manager/Engine/State/Event/Branch 系统。
- persisted schema 变化已有 migration/compatibility。
- 相关公开 API/类型有明确 schema/version。
- `reports/G37G_REPORT.md` 明确列出变更文件、命令、结果、风险、未完成项。
- `PLAN.md / STATUS.md / DECISIONS.md / BLOCKERS.md / KNOWN_FAILURES.md / CHANGELOG.md` 已更新。

## 10. 失败与阻塞处理

内部工程问题（实现、测试、类型、迁移、性能、依赖、架构）必须继续修复，不得标为 EXTERNAL_BLOCKED。

只有真实外部资料、授权、凭证、硬件或不可取得服务才可 `EXTERNAL_BLOCKED`。出现外部阻塞时，仍需完成所有可本地完成的 contract、fake、synthetic fixture、tests、docs，并继续下一个不依赖 Goal。

## 11. 文档更新

至少更新：
- `STATUS.md`
- `PLAN.md`
- `DECISIONS.md`（如有新架构裁决）
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- `reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md`
- `reports/V5_2_CODE_MINIMALITY_LEDGER.md`（若涉及新增/删除 abstraction）

## 12. Git 与检查点要求

仅当本 Goal Acceptance 全部 PASS 后创建本地 commit：

`g37g: v5.2 与 RedChamber 最终认证并停止`

禁止自动 push、force-push、rebase 用户历史或生产部署。


---

<!-- FILE: milestones/M26_QUALIFICATION.md -->

# M26 — 旧代码真实盘点与最小核心收敛 Milestone Gate

## 前置条件

- G29A PASS — 冻结旧基线并验证 M25 真实状态
- G29B PASS — 全仓代码处置实际盘点
- G29C PASS — 合并重复 Registry 与 Manager
- G29D PASS — 统一 State Event Audit 派生关系
- G29E PASS — 收敛物理包边界
- G29F PASS — 清理 Fake Placeholder 与旧实验残留
- G29G PASS — 建立最小代码度量与预算
- G29H PASS — M26 收敛资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M26=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M26_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M27_QUALIFICATION.md -->

# M27 — Reality Root / Constitution / Semantic ISA Milestone Gate

## 前置条件

- G30A PASS — Reality Root 语义契约
- G30B PASS — World Constitution 模型与版本
- G30C PASS — Constitution 执行与不可越权
- G30D PASS — World Semantic ISA 最小类型
- G30E PASS — ISA 到现有用例与 Commit 管线映射
- G30F PASS — 三类 World Commit 收敛
- G30G PASS — Fact Scope 与 Authority Partition
- G30H PASS — Event Snapshot 版本上下文升级
- G30I PASS — M27 Root Constitution ISA 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M27=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M27_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M28_QUALIFICATION.md -->

# M28 — Worldline / Lineage / World Hypervisor Milestone Gate

## 前置条件

- G31A PASS — World Definition 与 Worldline 身份模型
- G31B PASS — World Lineage Graph 数据模型
- G31C PASS — Lineage Repository 与迁移
- G31D PASS — World Hypervisor 多实例隔离
- G31E PASS — Interworld Identity 与 Presence
- G31F PASS — Hybrid Genesis 兼容性分析与安全拒绝
- G31G PASS — Lineage API SDK Studio 最小投影
- G31H PASS — M28 Lineage Hypervisor 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M28=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M28_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M29_QUALIFICATION.md -->

# M29 — Evolution Policy Stack / 多尺度共演化 Milestone Gate

## 前置条件

- G32A PASS — Evolution Policy Stack
- G32B PASS — 多尺度演化调度
- G32C PASS — Actor Capability 与 Persona 演化分离
- G32D PASS — Relation Group Social Pattern Distillation
- G32E PASS — Institution Organization Rule 晋升
- G32F PASS — Ontology Law 多尺度演化
- G32G PASS — Evolution Telemetry 与隐私权利
- G32H PASS — M29 多尺度共演化资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M29=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M29_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M30_QUALIFICATION.md -->

# M30 — Promotion / Cross-world Distillation Milestone Gate

## 前置条件

- G33A PASS — 统一 Abstraction Ladder
- G33B PASS — Worldline 到 Derived World Promotion Pipeline
- G33C PASS — Promotion 可重放与可撤销控制
- G33D PASS — Cross-world Distillation
- G33E PASS — 平台反哺 Sandbox Benchmark Approval
- G33F PASS — Lineage 与 Promotion API Studio
- G33G PASS — M30 Promotion Cross-world 资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M30=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M30_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M31_QUALIFICATION.md -->

# M31 — 平台收敛与向后兼容 Milestone Gate

## 前置条件

- G34A PASS — Kernel Runtime Forge Experiences 责任收敛
- G34B PASS — WorldPack Definition schema v5.2 迁移
- G34C PASS — 数据库与 Ledger 兼容迁移
- G34D PASS — 旧 Event Snapshot Branch 向后回放
- G34E PASS — API SDK Client 兼容
- G34F PASS — 性能与复杂度回归
- G34G PASS — M31 全平台兼容资格验收

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M31=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M31_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M32_QUALIFICATION.md -->

# M32 — 《红楼梦》Source Gate 与 World Definition 编译 Milestone Gate

## 前置条件

- G35A PASS — 红楼梦来源策略与合法版本登记
- G35B PASS — 章节分段与可引用 Source Locator
- G35C PASS — 人物与别名 Identity Distillation
- G35D PASS — 空间组织物品 Distillation
- G35E PASS — Past Character Future Canon 编译
- G35F PASS — Narrative Household HistoricalChina Domain 复用与补齐
- G35G PASS — Character Relation Knowledge Boundary Distillation
- G35H PASS — Completion Ledger 与审核
- G35I PASS — 编译 RedChamber World Definition 与 Scenario

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M32=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M32_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M33_QUALIFICATION.md -->

# M33 — 《红楼梦》Living World Runtime 与 Experience Milestone Gate

## 前置条件

- G36A PASS — 实例化 RC-001 与固定世界快照
- G36B PASS — 红楼梦空间可见可听私密运行
- G36C PASS — 人物职责 NPC 日程身体与社会制度
- G36D PASS — 信件诗稿礼物药物的物质与信息连续性
- G36E PASS — Perception Belief Memory 与消息传播
- G36F PASS — 林黛玉 Embodiment ShadowPolicy Handoff
- G36G PASS — Canonical Replay Soft Canon Living Open 三策略
- G36H PASS — 红楼梦 Experience Studio 最小可用面

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M33=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M33_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。


---

<!-- FILE: milestones/M34_QUALIFICATION.md -->

# M34 — 七日活世界 + Lineage/Promotion + v5.2 最终认证 Milestone Gate

## 前置条件

- G37A PASS — 红楼梦七日场景自动化执行
- G37B PASS — Canon 用户 无干预三世界线比较
- G37C PASS — 红楼梦长时演化与 Promotion Candidate
- G37D PASS — 红楼梦 Replay Crash Recovery Chaos
- G37E PASS — v5.2 全仓最小代码与架构终审
- G37F PASS — 全量回归与最终追溯矩阵
- G37G PASS — v5.2 与 RedChamber 最终认证并停止

## 必跑回归

- 本 Milestone 的 unit / property / contract / integration / E2E。
- Architecture conformance。
- Commit / Replay / Branch / Determinism。
- Migration / old fixture compatibility（适用时）。
- Security / Rights / Source Gate（适用时）。
- Code minimality audit。
- Python / TypeScript 全部质量检查。

## Gate 判定

只有所有内部验收 PASS 才可标 `M34=PASS`。不得因为“主流程能跑”忽略负向测试、兼容性或架构违规。

## 证据

生成 `reports/M34_QUALIFICATION.md`，包含：
- commit 范围；
- 测试命令与结果；
- acceptance matrix；
- 性能/代码复杂度变化；
- blockers；
- 已知限制；
- 下一 Milestone 前置状态。

PASS 后自动进入下一 Milestone，不等待用户确认。
