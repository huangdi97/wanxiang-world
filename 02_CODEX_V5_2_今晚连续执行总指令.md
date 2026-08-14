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
