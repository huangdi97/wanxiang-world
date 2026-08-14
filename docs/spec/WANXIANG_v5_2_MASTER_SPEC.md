# 万相世界 · Semantic Persistent Open-Ended Co-Evolutionary World OS v5.2-R1

> **完整平台设计、Reality Root、本体论、创世语义、世界蒸馏、多元宇宙、世界谱系、开放式多尺度共演化、可组合运行时与多领域工程母版**  
> **版本**：v5.2-R1  
> **日期**：2026-08-14  
> **状态**：Reality Root / 世界谱系 / 共演化架构收敛版；设计 Source of Truth；Codex Goal 在独立工程对话中另行制定  
> **目标读者**：产品设计者、架构师、AI/Agent 工程师、游戏开发者、数字人文研究者、博物馆与文化遗产机构、历史研究者、家谱研究者、Codex/Claude Code 等编码智能体

---

## 文档说明

本文件是在《万相世界 · Mythos Forge》原始设计和 Persistent Living World OS v3.0-R1 基础上的再次收敛与重构。原设计中的“角色工坊、析影、定型、拾遗、捏角、拓界、剧团、布景库、群戏、推演、密语、代笔、登台、赋形、生平、铸魂、同台、集市、记忆殿堂”等产品入口仍可保留，但它们不再被视为底层架构本身，而是同一 World OS 上的创作、运行、体验和管理界面。

v5.2-R1 以 v5.1-R1 为完整基础，不删减家谱、博物馆、文物、红楼梦、辽沈战役、Reality-Coupled World、开放世界、世界模型、Co-Simulation、DeepSeek Harness / Cordis、World Reality Calculus、Genesis 与 Distillation Fabric 等既有设计，并进一步整合“万相本身与万相所创造世界如何分别进化”“世界如何从世界中产生”“多元宇宙与世界谱系如何建立”“所有世界之下共同的最底层究竟是什么”等讨论。新增与修订重点如下：

1. **从“世界状态内核”下沉到 World Reality Calculus（世界现实演算）**：把万相的最深层定义为“区分—关系—变化—承诺”的现实生成语义，而不是某个数据库、ECS、LLM 或 Agent 框架。
2. **世界形式化升级为 `W_t = (Σ_t, H_t, Γ_t, Ω_t; Λ)`**：Σ 表示当前可区分的语义/本体空间，H 表示已承诺历史，Γ 表示当前有效规律与约束，Ω 表示当前可能性空间，Λ 表示本体、规律和可能性空间本身如何合法演化的元规则。
3. **引入 Genesis Semantics（创世语义）**：支持 Designer Genesis、True Genesis、Evolutionary Genesis；世界可从极简初始条件开始，通过稳定结构、粗粒化和涌现逐步长出新的实体类型、规律层级和高阶组织。
4. **正式区分三类 Commit**：`StateCommit` 改变状态事实，`OntologyCommit` 扩展 Σ，`LawCommit` 改变/扩展 Γ；任何 Commit 都必须经过可审计的合法性边界。
5. **把“蒸馏”升级为 Distillation Fabric / Meaning Engine**：从小说、史料、家谱、档案、博物馆、视频、现实观测和世界运行历史中发现 Identity、Relation、Event、Rule、Skill、Persona、Institution、Ontology 等候选结构；蒸馏负责发现，Commit 负责承认。
6. **新增 Evolutionary Distillation（演化蒸馏）**：世界运行后可从长历史中提炼新的技能、关系模式、人物阶段、制度和本体候选；这些只能作为 Candidate，经验证后通过 Capability/Ontology/Law Commit 进入世界。
7. **新增 Capability Fabric（能力织网）**：吸收 Cordis 的服务依赖、作用域、可逆运行时副作用和动态组合思想，使 LLM、Agent Harness、Domain、Simulation、Projection、Sensor、Storage Adapter 等能力可安装、替换、卸载和回滚。
8. **Authority Microkernel 进一步收敛**：一切能力可以组合，但世界现实的承诺语义不可被任意插件替代；世界变化必须通过唯一 Mutation/Commit Boundary。
9. **DeepSeek Harness 不作为万相本体底座，而作为 Agent Harness Provider 候选**：万相保留独立的 World Authority；DSH/OpenStory/Native/Human 等都通过统一 Actor/Agent Harness ABI 接入。
10. **新增三重 Ledger**：World Ledger 记录世界发生了什么；Actor Trajectory Ledger 记录主体为何如此决策；Runtime Control Ledger 记录运行时安装/卸载了哪些 Provider、模型、规则和配置。
11. **新增 World Invariant Registry 与 Bounded Runtime Evolution**：世界能力可以演化，但核心现实语义、Branch 隔离、Evidence/Rights 契约和 Commit Authority 不允许普通 Agent 自修改；新能力必须经过 Sandbox/Shadow World/Invariant/Regression/Evaluation 后才可事务式激活。
12. **重新定义三大引擎**：Meaning Engine（理解/蒸馏/编译）、Reality Engine（承诺/运行/演化）、Experience Engine（显化/接管/交互）；它们构成“资料→世界→历史→体验→再蒸馏”的闭环。
13. **工程路线与设计路线彻底分工**：本母版只作为产品、研究与架构 Source of Truth。原 G0–G12 保留为方向性阶段划分，不再视为最终 Codex 可执行 Goal；具体 Goal、Milestone、Acceptance 与代码指令应在独立工程规划对话中重新审查后生成。
14. **新增 Reality Root（世界现实根）**：明确万相最底层不是某个具体宇宙、物理规律、Agent、Harness、World Model 或数据库，而是所有可运行世界共享的最小现实语义基岩：Distinction、Relation、Transition、Commitment 与 History。
15. **World Constitution 与具体世界规则分层**：Reality Root 只定义“如何成为现实”，Constitution 决定某一世界族允许哪些基础规律、身份连续性、因果与演化边界；物理、魔法、轮回、梦境等都属于具体 Constitution/Domain，而不是万相最底层。
16. **对象层级升级为世界谱系体系**：从 `Wanxiang → Reality Root → Constitution → Genesis → World Definition → World Instance → Worldline/Branch → Derived World` 组织世界；Worldline 可以在满足 Promotion 条件后固化成新的 World Definition，形成真正的世界家谱。
17. **新增 Multiverse Runtime / World Lineage Graph**：多个世界不再只是文件列表，而是具有 parent、fork point、inherited history、constitution version、evolution policy 和 descendants 的世界谱系 DAG；未来支持受控 Hybrid Genesis / World Merge。
18. **新增 Wanxiang Evolution Stack**：区分 Constitution Evolution、Platform Evolution、Domain Evolution、World Definition Evolution、World Instance Evolution、In-world Evolution 与 Cross-world Evolution；各层可以反馈，但写权限、验证门和升级方式严格隔离。
19. **新增 Multi-scale Co-Evolution（多尺度共演化）**：Actor、Relation、Capability、Organization、Institution、Culture、Economy、Ecology、Ontology 与 World 可在不同时间尺度上共同演化；微观行为可涌现为宏观制度，宏观制度又反向塑造个体。
20. **新增 Evolution Promotion Pipeline / Abstraction Ladder**：Event → Pattern → Habit/Capability → Group Pattern → Institution → World Structure → Cross-world Pattern → Domain Capability → Platform Improvement；越高层的晋升越不能自动 Commit。
21. **重新确定万相的系统身份**：万相整体不是 Agent 或 Harness，而是 `World OS + World Compiler + World Hypervisor + Evolution System`；工程上进一步收敛为 `Wanxiang Kernel + Wanxiang Runtime + Wanxiang Forge + Experiences`。
22. **新增 World Semantic ISA 思想**：世界上层语言、World Pack、Domain Action 与 Agent Intent 最终都应可编译为极少数底层语义操作，如 DECLARE/ASSERT/PROPOSE/VALIDATE/COMMIT/FORK；这是实现无关的世界语义指令集，而不是某种具体数据库 API。

本母版继续保留原始“析影、定型、拾遗、捏角、拓界、剧团、布景库、群戏、推演、密语、代笔、登台、赋形、生平、铸魂、同台、集市、记忆殿堂”等产品概念，但它们现在分别归入 Distillation/Genesis、Studio、Experience、Projection、Evaluation 等上层能力，不再决定世界本体。

---

# 第零篇：世界本体论、现实演算与创世语义

## 0.1 为什么还要再往下挖一层

“Entity / Event / WorldState / Branch”已经足以描述工程对象，但如果万相目标是成为长期 World OS，最底层不应绑定 2026 年某种实现范式。ECS、关系数据库、事件存储、知识图谱、Agent、LLM、游戏引擎都可能变化；更稳定的是世界本身需要满足的现实语义。

万相因此采用两层表达：

- **本体论层**：区分（Distinction）、关系（Relation）、变化（Transition）、承诺（Commitment）；
- **工程语义层**：Identity、Fact、Event、Constraint、Commit、Ledger、Branch、Projection。

最高原则：

> **World = committed history, not generated text.**  
> 世界是被承诺的历史，而不是模型生成的一段文本。

> **Creativity before Commit; consistency after Commit.**  
> 承诺之前最大化创造，承诺之后最大化一致。

> **Everything may evolve except the semantics of becoming real.**  
> 一切能力都可以演化，唯“什么叫成为这个世界的现实”的语义不能被普通能力绕过。

## 0.2 四个本体原语

### 0.2.1 Distinction：区分

一个东西要成为世界中的对象，首先必须能够与“非它”区分。Identity 是 Distinction 的工程实现，而不是更根本的哲学起点。

例如：同名祖先不能因为字符串相同就被合并；一封家书从家庭传入博物馆以后仍应保持同一 Object Identity；红楼梦的某个角色实例与另一个分支里的同一角色必须共享来源身份、但拥有不同分支状态。

### 0.2.2 Relation：关系

孤立 Identity 不能构成世界。世界是可区分对象之间的结构化关系：空间、时间、亲缘、所有权、组织、因果、知识、证据、权限、社会身份等。

家谱树只是 Kinship Relation 的一种 Projection；地图只是 Spatial Relation 的一种 Projection；关系图也不是世界本体，而是 Fact Space 的一种视图。

### 0.2.3 Transition：变化

如果关系永不改变，系统只是知识库。世界必须允许 Before → After，并且每次变化必须能说明旧状态、触发、约束、结果和影响范围。

### 0.2.4 Commitment：世界承诺

“有人说发生了”“LLM 认为发生了”“模拟器给出一个结果”“角色想做某事”都不等于世界事实。只有通过 Commit Boundary 的变化，才成为该 World Instance / Branch 的现实。

因此：

```text
Proposal / Observation / Claim / Simulation Result
                    ↓
                Validate
                    ↓
                Resolve
                    ↓
                 Commit
                    ↓
             Committed History
```

Commitment 是 Authority、Ledger、Time、Branch、Provenance 和 Invariant 等工程契约的共同根。

## 0.3 世界的形式化：W_t = (Σ_t, H_t, Γ_t, Ω_t; Λ)

万相在设计层采用：

```text
W_t = (Σ_t, H_t, Γ_t, Ω_t; Λ)
```

其中：

- **Σ_t — Semantic / Ontology Space**：这个世界在 t 时刻能够区分和表达什么；包含类型、关系、状态变量、可观测量和高阶结构。
- **H_t — Committed History**：到 t 为止已经被世界承诺的事件历史。
- **Γ_t — Effective Laws / Constraints**：当前有效的基本约束、领域规律、制度、权限、机制模型和场景规则。
- **Ω_t — Possibility Space**：在当前事实与规律下，尚未成为现实但允许成为现实的候选状态、行动和未来。
- **Λ — Genesis / Meta-Law**：Σ、Γ、Ω 本身如何合法扩展、收缩、分层和演化的元规则。

当前状态并不需要被视为最终真理载体，而可理解为：

```text
CurrentState_t = Project / Fold(H_t, Σ_t, Γ_t)
```

这使 Event Ledger、Replay、Branch、Counterfactual 和多种 Projection 在概念上自然统一。

## 0.4 Fact Space：把 Canonical、Belief、Hypothesis 统一起来

工程上 `Fact` 是一个有作用域的语义断言，而不只是数据库字段：

```text
Fact(subject, predicate, object/value, scope, valid_time, provenance)
```

`scope` 至少可以是：

- `canonical`：世界当前承诺的现实；
- `public`：公开传播的知识；
- `organization:<id>`：组织内部知识；
- `actor:<id>`：个人 Belief；
- `hypothesis:<id>`：尚未承诺的可能世界；
- `reconstruction:<id>`：历史/文物重建假设。

由此，“宝玉真实在哪里”“黛玉认为宝玉在哪里”“研究者推测宝玉可能在哪里”可以使用同一事实语义、不同作用域，而不需要四套互不兼容的数据哲学。

## 0.5 三类 Commit

### StateCommit

改变既有 Σ/Γ 下的事实，例如移动、转移物品、形成关系、产生伤害、提交实验结果。

### OntologyCommit

改变 Σ：正式承认新的实体类型、关系类型、稳定高层结构或概念。例如从低层状态中识别出“Ocean”“Organism”“Institution”这类可持续区分对象。

### LawCommit

改变或扩展 Γ。例如一个社会建立新制度、世界安装新的领域规则版本、Scenario 添加约束。基础 World Constitution 不属于普通 LawCommit 的可修改范围。

## 0.6 Genesis：世界怎样出生

正式定义 `GenesisPackage`：

```text
GenesisPackage
├── SemanticSeed / Σ0
├── InitialConditions / B0
├── InitialLaws / Γ0
├── InitialPossibilityPolicy / Ω0
├── MetaLaws / Λ
├── ResolutionPolicy
├── RandomnessPolicy
├── Source / Creator / Rights
└── GenesisEvent
```

万相支持三类创世：

1. **Designer Genesis**：作者直接给出成熟世界的主要类型、关系、规则和背景历史，例如原创仙侠世界。
2. **True Genesis**：从极简物理/机制层的初始条件开始，例如宇宙或原始地球模拟。
3. **Evolutionary Genesis**：初始 ontology 很贫乏，世界运行后通过稳定模式、粗粒化、蒸馏和验证逐渐形成新的高层实体、制度和规律。

万相不要求所有世界都从宇宙起点模拟。红楼梦可直接从社会/人物尺度的 Genesis Package 启动；家族世界可从资料世界启动；战役世界可从历史快照启动。关键是底层允许不同抽象层级而不改变“现实如何被承诺”的语义。

## 0.7 Emergence 与 Ontology Expansion

真正的新生世界不能假设所有类型事先存在。万相因此允许：

```text
low-level committed history
        ↓
pattern / stability detection
        ↓
Distillation
        ↓
OntologyCandidate
        ↓
Validation / Coarse-graining tests
        ↓
OntologyCommit
        ↓
Σ_t → Σ_{t+1}
```

“涌现”在万相中不是 LLM 总结一句“出现了国家/生命/宗教”，而是从运行历史中提出高阶结构候选，并经过稳定性、可解释性、反事实、领域验证或人工审核后才成为正式世界结构。

## 0.8 Γ 是分层的有效规律，而不是一张平面规则表

Γ 至少应区分：

```text
Fundamental / Constitution Constraints
Effective Mechanistic Laws
Biological / Ecological Rules
Social / Institutional Rules
Domain Rules
Scenario Constraints
```

不同层拥有不同修改权限。社会法律可被角色与组织行动改变；Scenario 约束可由导演修改；普通 Agent 不能修改 Branch 隔离、Commit Authority、Evidence/Rights 契约等世界宪法。

## 0.9 Ω：创造发生的地方

Ω 保存当前可能但尚未承诺的未来。LLM、玩家、Agent、世界模型、规划器和程序生成器都可以在 Ω 中提出大量 Proposal；严格一致性只在 Commit 之后生效。

因此万相不压制创造，而是把创造与现实分离：

```text
自由 Proposal Space Ω
      ↓
Constraint / Simulation / Review
      ↓
Commit
      ↓
Committed History H
```

## 0.10 三大引擎

在产品/架构层，万相可进一步压缩为三个互相闭环的大引擎：

### Meaning Engine

负责 Source / Reality / History → Understand → Distill → Candidate World Structure。核心实现是 Distillation Fabric、World Compiler、Evidence Binding 和 Completion。

### Reality Engine

负责 Candidate / Intent / Simulation → Validate → Resolve → Commit → History。核心实现是 Authority Microkernel、World Reality Bus、Living Runtime、Co-Simulation、Branch/Replay。

### Experience Engine

负责 World → Observation / Projection / Embodiment → Human/Agent Experience，并将人类或 Agent 的行为重新提交为 Proposal。

完整闭环：

```text
Source / Existing Reality
        ↓
Meaning Engine
        ↓
World Definition
        ↓
Reality Engine
        ↓
Committed World History
        ↓
Experience Engine
        ↓
Human / Agent Action
        ↓
Proposal → Reality Engine
        ↓
History
        ↓
Meaning Engine re-distills long-term structure
```

## 0.11 Authority Microkernel 的最小职责

万相最深的工程内核不需要知道“林黛玉”“锦州”“GEDCOM”“青铜器”。它只需要守住：

- 稳定 Identity / World / Instance / Branch Identity；
- Fact/Event 的不可歧义引用；
- Mutation/Commit Boundary；
- Transition Contract；
- Committed Ledger；
- 因果/时间顺序契约；
- Branch/Fork 隔离；
- Invariant 执行边界；
- Evidence/Provenance 必须可引用的契约；
- Snapshot / Replay 的可重建性。

这些是“世界何以保持同一世界”的最低语义，而不是某种具体技术栈。

## 0.12 极简原则与工程原则必须分开

本体极简不等于把所有代码塞进三个类。推荐分层：

```text
Ontology:
Distinction / Relation / Transition / Commitment

Semantic Calculus:
Identity / Fact / Event / Constraint / Commit

Engineering Runtime:
Ledger / Snapshot / Projection / Branch / Transaction / Persistence

World Capabilities:
Space / Time / Object / Actor / Memory / Simulation / Domain

Products / Instances:
Red Chamber / Family / Museum / Campaign / Science / Original World
```

这样既保持哲学极简，也允许工程清晰、可测试、可替换。

## 0.13 家谱、博物馆、红楼梦和战役为什么在最底层相同

它们最终都可表达成：

```text
Identity + Relation + Event + Claim + Source + Constraint + Commit
```

- 家谱树 = Kinship Relation Projection；
- 人生时间线 = Person Event Projection；
- 文物生命史 = Object Event Projection；
- 战役态势图 = Unit/Place/Resource Fact Projection；
- 角色主观认知 = Actor-scoped Fact Space；
- 小说正典 = Source-grounded Canonical Claims + Committed Scenario History。

差别由 Domain Pack、Σ、Γ 和 World Pack 内容决定，而不是重新造一套 Core。

## 0.14 Reality Root：所有世界之下的本体基岩

`W_t = (Σ_t, H_t, Γ_t, Ω_t; Λ)` 描述的是一个已经可以被定义和运行的世界；再往下一层，需要回答“为什么不同宇宙即使拥有完全不同的物理、魔法、社会制度和本体，仍然都能被万相称为世界”。本母版把这一层正式定义为 **Reality Root / 世界现实根**。

Reality Root 不是一个具体世界，也不是某种“主宇宙”。它不预设引力、光速、生命、人物、空间维数或魔法是否存在，而只规定所有万相世界共享的最低现实语义：

```text
Distinction   —— 能够区分 A 与非 A
Relation      —— 可区分者之间能够形成结构
Transition    —— 结构能够从 Before 变为 After
Commitment    —— 某个合法变化被这个世界正式承认
History       —— 被承认的变化形成不可静默改写的连续历史
```

工程上可投影为：

```text
Identity
Fact / Relation
Event / Transition
Constraint
Commit
Ledger / History
Branch / Lineage
```

这里的关键原则是：**物理规律不是万相最底层；“规则必须被定义、变化必须经过合法过程、历史必须可追溯”才是。** 因而现实主义世界、仙侠世界、梦境世界、抽象数学世界和 Reality-Coupled World 可以共享 Reality Root，却拥有完全不同的 Constitution、Γ 与 Λ。

## 0.15 World Constitution：世界族的“宪法”而不是世界事实

Reality Root 之上是 **World Constitution**。它定义某一类世界可以采用怎样的根规则、哪些规则层可变、哪些身份与因果语义必须保持、哪些本体扩张方式被允许。

示例：

```text
Realistic Constitution
  strict causality
  ordinary biological death irreversible
  magic capability unavailable

Xianxia Constitution
  ordinary causality retained
  qi/spiritual-energy ontology enabled
  cultivation and reincarnation may be legal domain mechanisms

Dream Constitution
  spatial continuity may be weak
  symbolic transformations may be legal
  identity merging may be explicitly permitted
```

Constitution 仍必须服从 Reality Root：即使一个世界允许时间回溯、身份复制或轮回，这些现象也必须以该 Constitution 明确定义的 Event / Commit / Branch 语义发生，不能通过未记录的直接数据库修改实现。

## 0.16 Genesis Root、Root World 与 Reality Root 必须区分

三个概念不得混淆：

- **Wanxiang**：实现整套世界创建、运行、演化和托管能力的软件/World OS；
- **Reality Root**：所有万相世界共享的最低现实语义，不属于任何具体世界；
- **Root World / Genesis World**：某个具体世界谱系的祖先世界，例如某个原创宇宙的 Genesis，或《红楼梦》世界族的 Canonical Genesis。

因此：

```text
Wanxiang
  implements Reality Root

Reality Root
  supports many Constitutions / Genesis families

Genesis World
  is only one ancestor inside a particular world lineage
```

这避免把“万相主宇宙”误认为整个系统的最底层。

## 0.17 World Semantic ISA：世界语义指令集

为了让底层不绑定 SQL、ECS、RDF、Property Graph、Event Store 或某个游戏引擎，本母版引入 **World Semantic ISA** 概念。它不是给用户直接编程的机器指令，而是 World Compiler、Domain Pack、Agent Action 与 Runtime 最终都可归约到的最小语义操作集合。

概念性操作包括：

```text
DECLARE     创建/声明一个可持续引用的 Identity
ASSERT      提议或建立一条带作用域的 Fact / Relation
RETRACT     通过合法 Event 终止某条当前有效 Fact
PROPOSE     提出一次状态/本体/规则变化
VALIDATE    在 Constitution、Γ、权限和 Invariant 下验证
COMMIT      把合法变化写入 Committed History
FORK        从历史前缀产生隔离的新 Worldline
PROMOTE     把成熟 Worldline / Pattern 晋升为新世界或上层能力候选
```

`结婚、烧信、部队移动、创建公司、发明货币、形成星球、建立宗教` 等上层 Action 都不应成为 Reality Root 的硬编码指令，而是由 Domain/Compiler 映射为这些更底层的语义变化。

## 0.18 世界不是孤立实例，而可以形成谱系

Reality Root 与 Branch 语义使世界天然具有“血统”。同一个 Genesis 可以产生多个独立 Worldline，某条长期演化的 Worldline 又可以被固化为新的 World Definition，继续产生后代世界。因此世界结构长期应被视为 **World Lineage Graph**，而不是扁平的 World Pack 列表。

```text
Reality Root
    ↓
Constitution
    ↓
Genesis / Root World
    ├── Worldline A
    │     ├── A1
    │     └── A2 → Promote → Derived World D
    │                         ├── D1
    │                         └── D2
    └── Worldline B
```

在最简单情况下它是一棵树；当未来支持 `Hybrid Genesis / World Merge` 时，它将成为 DAG。任何 Merge 都必须显式解决 Identity、History、Ontology、Law 与 Rights 冲突，不能做无语义的“世界 git merge”。

## 0.19 开放式多尺度共演化是运行原则，不是单一 Feature

万相的“进化”不只发生在角色，也不只发生在平台。它是跨尺度原则：

```text
Actor ↔ Relation ↔ Group ↔ Organization ↔ Institution ↔ Society ↔ World
                                                         ↕
                                                    Domain / Wanxiang
```

一个人的重复选择可以形成习惯；多人稳定重复的模式可以形成规范；规范经过组织合法化可以形成制度；制度又反向改变个体的机会、奖励、惩罚与认知。世界运行的大量历史又可以跨实例蒸馏出可复用 Domain Capability，经过独立验证后改进下一代万相。

因此应区分两类反馈回路：

```text
Living World Loop:
World → Event → Commit → History → Distill → Adapt/Emerge → World

Wanxiang Evolution Loop:
Many Worlds → Evaluation/Distillation → Capability Candidate
→ Sandbox/Benchmark/Approval → Domain/Runtime vNext → Future Worlds
```

二者可以共演化，但绝不共享直接写权限。

## 0.20 设计宪法（扩展版）

本母版后续所有模块必须服从以下五条最高设计宪法：

1. **世界是被承诺的历史，不是生成文本。**
2. **承诺前创造最大化，承诺后一致性最大化。**
3. **一切世界能力可以演化，唯“什么叫成为现实”的语义不能被普通能力绕过。**
4. **世界可以无限向上分化、演化和繁衍，但所有后代必须能够追溯其 Reality Root、Constitution、Genesis 与历史血统。**
5. **万相与万相世界可以共演化，但任何世界实例都不是万相 Core 的管理员；世界经验只能通过 Distill → Candidate → Evaluate → Promote 的受控路径反哺平台。**


---

# 第一篇：总纲与产品定义

## 1. 最终定位

### 1.1 一句话定位

> **万相世界是一套以 Reality Root 为共同现实基岩，把文学、历史、家谱、档案、博物馆藏品、地图、现实数据与原创设定蒸馏、编译或创生为持久、可执行、可证据追溯的世界，并让人物、关系、组织、制度、文化、能力、世界实例与世界谱系在受控边界内开放式多尺度共演化，再投射到文字、2D、3D、数字人、AR/VR、沙盘和现实空间中的 Semantic Persistent Open-Ended Co-Evolutionary World OS。**

### 1.2 万相解决的根问题

当前很多 AI 世界产品分别解决了局部问题：角色卡告诉模型“这个人是谁”，Lorebook 告诉模型“这个世界有什么”，游戏引擎负责“画面和物理”，Agent 框架负责“谁来思考”，世界模型负责“下一帧可能长什么样”。但仍缺少统一回答下列问题的基础设施：

- 世界里什么东西真实存在？
- 这个实体现在在哪里、属于谁、是什么状态？
- 哪个角色知道什么、不知道什么、误解什么？
- 一个角色想做某件事，世界是否允许？
- 行动成功与否由谁决定？
- 行动之后哪些实体、关系、资源、认知、记忆必须同步变化？
- 一个月、一年以后，世界还能不能自洽？
- 历史事实、模型推断、体验重建、用户虚构如何分开？
- 一个世界如何被安装、实例化、分支、回放、多人进入和跨终端显示？

万相的核心职责就是回答这些问题。

### 1.3 万相不是什么

万相不是单纯的：

- 角色扮演聊天工具；
- SillyTavern 的替代 UI；
- 小说续写器；
- 多 Agent 群聊框架；
- 3D 游戏引擎；
- 视频世界模型；
- 博物馆 CMS；
- 家谱管理软件；
- 兵棋软件；
- 数字人平台。

这些都可以成为万相的客户端、适配器、领域包或世界实例。

### 1.4 用户侧五大产品面

万相长期可以形成五个主要产品面，但它们共享同一底层：

| 产品面 | 主要用户 | 作用 |
|---|---|---|
| 万相工坊 Studio | 创作者、研究者、策展人、开发者 | 编译、编辑、审核、调试和发布世界 |
| 万相世界 Experience | 普通用户、玩家 | 进入和生活在已发布世界中 |
| 万相演策 Strategy | 研究者、培训者、决策者 | 沙盘、反事实、批量实验和复盘 |
| 万相展境 Heritage | 博物馆、纪念馆、科技馆、教育机构 | 数字藏品、历史现场、互动展览和数字人物 |
| 万相人生 / 家史 Family | 个人、家庭、家族研究者 | 家谱、人生史、迁徙史、口述史和数字传承 |

---

## 2. 最重要的对象层级：从 Reality Root 到世界谱系

万相必须严格区分“系统本身”“所有世界共享的现实语义”“某类世界的宪法”“创世定义”“领域机制”“世界母本”“正在运行的世界”“世界线”和“体验会话”。新的完整层级如下：

```text
Wanxiang World OS
        ↓ implements
Reality Root / World Reality Calculus
        ↓ constrains
World Constitution / Meta-Law Family
        ↓ + Domain Packs + Genesis Specification
World Definition / World Pack
        ↓ + Scenario
World Instance
        ↓
Worldline / Branch
        ↓ long-horizon evolution
Derived World Candidate
        ↓ Promotion (optional)
New World Definition / Child World Lineage
        ↓
Session / Human / AI Controller
        ↓
Projection / Text / 2D / 3D / Digital Human / XR / Reality
```

其中 `Domain Pack` 是横向能力组合，不是世界谱系中的祖先节点；同一 Constitution 和 World Definition 可以安装不同 Domain/Runtime Profile，同一个 World Pack 也可以实例化出无数相互隔离的 World Instance。

### 2.1 Reality Root

Reality Root 是所有世界共享的最低语义基岩，只定义 Distinction、Relation、Transition、Commitment、History 及其工程投影。它不包含任何具体人物、时代、物理定律、魔法设定或世界专名。

### 2.2 World Constitution

Constitution 定义一个世界族允许怎样的根规则、哪些规律层可变、哪些身份/因果/时间语义成立，以及 Ontology/Law Evolution 的边界。现实主义、仙侠、梦境、战役复现、现实耦合世界可以使用不同 Constitution。

### 2.3 Domain Pack

Domain Pack 描述可复用机制，不包含具体世界专名。例如：

- Narrative Domain：人物弧、秘密、伏笔、场景、叙事张力；
- Household Society Domain：家庭、主仆、长幼、职责、起居、宴会、探病、赠礼；
- Historical China Domain：中国历史时代、时辰、身份、礼制、官职、交通、货币；
- Campaign Domain：部队、指挥、命令、后勤、战斗、战争迷雾；
- Genealogy Domain：血缘/婚姻/收养关系、人生事件、家户、迁徙、来源、谱系；
- Heritage Domain：藏品、部件、材料、制作、使用、收藏、修复、展陈、权利、文化协议；
- City / Economy / Science / Ecology / Civilization / Learning Domain 等。

Domain 可以独立版本化和演化，但不能静默重写已有世界的 Committed History。

### 2.4 Genesis Specification / Genesis World

Genesis 定义某个世界谱系的出生条件，可以是极简初始条件、成熟的历史快照或已有 Canon。它包含 Semantic Seed、Initial Conditions、Initial Laws、Evolution Policy、Randomness/Resolution Policy 与 Provenance。

`Genesis World` 是某个具体谱系的祖世界，不等于 Reality Root。

### 2.5 World Pack / World Definition

World Pack 是具体世界的只读、版本化定义，例如：

- `dream_of_the_red_chamber`；
- `liaoshen_campaign_1948`；
- `my_family_1850_2026`；
- `museum_x_collection_world`；
- `artifact_bronze_vessel_001`；
- `original_xianxia_world`。

它回答“这个世界出生时是什么”，而不是“它运行多年以后变成什么”。

### 2.6 Scenario

同一个 World Pack 可以有多个合法起点。例如《红楼梦》可以有“黛玉初入贾府”“海棠诗社”“某一章回快照”；家族世界可以有“1937 年故乡”“1985 年家庭聚会”；博物馆可以有“当前展厅”“文物原使用场景”“修复前状态”。

### 2.7 World Instance

Instance 是真正会变化的运行世界，拥有自己的 `W_t = (Σ_t, H_t, Γ_t, Ω_t; Λ)`、时间、人物状态、物品位置、关系、秘密、制度、日程、事件、运行时配置和 Ledger。

### 2.8 Worldline / Branch

Worldline 是某个 World Instance 的一条连续历史。Branch 从任意历史前缀或快照分出新的世界线；Parent 不受 Child 反向污染。Canon Replay、用户接管、AI 自主、反事实实验都可以是不同 Worldline。

### 2.9 Derived World / World Promotion

当某条 Worldline 长期演化后已经形成稳定的新人物代际、制度、组织、文化、Ontology 或 Law，可以经过 `Evolution Promotion Pipeline` 固化为新的 World Definition：

```text
Parent World Definition
  ↓ instantiate
Worldline A
  ↓ 50 years evolution
Stable new world structure
  ↓ Distill / Validate / Promote
Derived World Definition
  ↓
new child instances / worldlines
```

这让“世界可以生出世界”成为一等能力，而不是把每个分支永远当作临时存档。

### 2.10 World Lineage Graph / 世界家谱

所有父世界、子世界、Fork、Promotion 与 Hybrid Genesis 构成 World Lineage Graph。每个节点/边必须至少保存：

```text
world_definition_id
parent_world_definition_ids
origin_instance / origin_worldline
fork_or_promotion_event
inherited_history_ref
constitution_version
domain_versions
runtime_profile_version
evolution_policy_version
rights/provenance
```

单父系时可以投影成“世界树”；支持多父世界派生后应使用 DAG。世界家谱本身也是万相 Studio/Research 的重要 Projection。

### 2.11 Session 与 Projection

Session 只是某个人类或 AI 此次进入某条 Worldline 的控制/观察上下文；Projection 只是该世界在文本、2D、3D、数字人、AR/VR、博物馆展陈或现实空间中的显化。二者都不拥有世界权威。

---

# 第二篇：总体架构

## 3. 五个平面、十六个核心内核

万相的正式底层架构为 **5 Planes / 16 Kernels**。五个平面解决五类不同问题：世界从哪里来、世界实际上是什么、主体如何认知和行动、事件如何被编排与干预、世界如何长期托管并投影到各种终端。

```text
┌──────────────────────────────────────────────────────────────┐
│ E. Hosting & Experience Plane                               │
│ 15 World Host / Lifecycle / Multiplayer Kernel             │
│ 16 Projection / Rendering / Network Gateway                │
├──────────────────────────────────────────────────────────────┤
│ D. Orchestration & Control Plane                            │
│ 13 Opportunity–Challenge–Event Kernel                      │
│ 14 Embodiment / Director / Experiment Kernel               │
├──────────────────────────────────────────────────────────────┤
│ C. Agency & Capability Plane                                │
│ 09 Perception–Belief–Memory Kernel                         │
│ 10 Actor / Organization Runtime                            │
│ 11 Skill–Action–Affordance Kernel                          │
│ 12 Capability & Learning Kernel                            │
├──────────────────────────────────────────────────────────────┤
│ B. World Reality Plane                                      │
│ 04 Canonical State Kernel                                   │
│ 05 Living World Substrate                                   │
│ 06 Physical Context / Reality Bridge                        │
│ 07 Co-Simulation Fabric                                     │
│ 08 Event / Branch / Temporal Kernel                         │
├──────────────────────────────────────────────────────────────┤
│ A. World Definition Plane                                   │
│ 01 Source / Evidence Kernel                                 │
│ 02 World Compiler & Completion Compiler                     │
│ 03 Package / Schema / Dependency Registry                   │
└──────────────────────────────────────────────────────────────┘

Cross-cutting control planes:
Rights & Provenance | Security & Privacy | Evaluation & Observability |
Model Routing & Cost | Persistence & Versioning | Safety & Governance
```

这十六个 Kernel 是**逻辑边界**，不是要求首版拆成十六个微服务。G0–G8 采用模块化单体；只有性能、隔离、团队和部署证明有必要时，才把 World Host、Co-Simulation Worker、Asset Pipeline 等拆成独立进程或服务。

---

## 4. World Definition Plane：世界从哪里来

### 4.1 Source / Evidence Kernel

负责所有进入万相的资料登记：文本、图片、视频、音频、地图、表格、数据库、家谱、IIIF Manifest、3D 扫描、口述史、现实传感流等。

每一个来源至少记录：

```text
SourceRecord
- source_id
- title
- creator / institution
- source_type
- version / edition
- original_uri / local_asset
- checksum
- acquisition_method
- date_range
- language
- rights
- access_policy
- cultural_protocol
- reliability_note
- review_status
```

**来源不等于事实。** 来源产生 `Claim`；不同来源可以提出互相冲突的 Claim，系统保留其出处、版本、时间和审核状态。历史、家族、博物馆、现实传感均遵循同一规则。

### 4.2 World Compiler & Completion Compiler

世界编译器在 v5.1 中被正式拆为 **Distillation Fabric + Completion Compiler + Package Assembler**。Distillation 不只是“角色抽取”，而是从高维、冗余、噪声和长历史中发现可复用、可证据支持的世界结构候选。

Distiller 类型包括：

```text
Identity / Entity Distiller
Relation Distiller
Event / Timeline Distiller
Character / Persona / Arc Distiller
Knowledge-Boundary / Belief Distiller
Rule / Institution Distiller
Skill / Behaviour Distiller
Place / Spatial Distiller
Claim / Evidence Distiller
Ontology Distiller
```

所有输出首先是 `Candidate`，不是 Canonical Fact。至少区分：`EXPLICIT`、`INFERRED`、`INTERPRETIVE`、`RECONSTRUCTED`、`GENERATED`。候选只有经过证据绑定、冲突检查、规则/一致性验证和必要的人工审核，才允许进入 World Definition 或相应 Commit 流程。


静态资料经过：

```text
Source Registry
→ Parse / Segment / Media Analysis
→ Entity Resolution
→ Event–Time–Space Extraction
→ Relation / Organization Extraction
→ Character / Institution Compilation
→ Rule / Skill / Affordance Compilation
→ Evidence Binding
→ World Completion Candidate Generation
→ Validation / Human Review
→ World Pack
```

World Completion 专门补齐“要让世界运行而资料没有显式写出”的部分，并强制标注来源等级：

- E0：直接证据；
- E1：多来源支持的重建；
- E2：时代/领域规则推导；
- E3：运行必需的系统默认值；
- E4：体验性生成；
- E5：用户虚构。

补全结果永远不能静默升级为 E0。

### 4.3 Package / Schema / Dependency Registry

正式包类型：

```text
DomainPackage
WorldPackage
ScenarioPackage
CharacterPackage
OrganizationPackage
SkillPackage
EvidencePackage
AssetPackage
RightsPackage
ExperiencePackage
EvaluationPackage
ConnectorPackage
```

每个包必须声明：`package_id`、SemVer、Schema 版本、依赖、兼容范围、来源、许可证、完整性哈希、迁移策略、签名/发布者和可选的安全审计状态。

具体世界永远不进入 Core：

```text
Wanxiang Core
  + HistoricalChina Domain
  + HouseholdSociety Domain
  + Narrative Domain
  + DreamOfTheRedChamber World Pack
  + Scenario
  = RedChamber World Instance
```

---

## 5. World Reality Plane：世界实际上是什么

### 5.1 Canonical State Kernel

`Canonical World State` 是唯一权威真相源。LLM、客户端、Director、数字人、传感器和外部模拟器均不得绕过 Commit Authority。

一等对象至少包括：

```text
Entity / Component / Relation / Event / Claim / Evidence
Rule / Constraint / Observation / ActionIntent / Action / Order
Adjudication / WorldDelta / WorldState / Snapshot / Run / Branch
Artifact / Metric / Assumption / ValidityEnvelope
```

基础不变量：唯一 ID、时间单调、事件不可静默篡改、位置/容器/所有权一致、资源守恒、权限校验、认知隔离、父子分支隔离、随机种子与规则版本可复现、正典锁定不可被普通动作覆盖。

### 5.2 Living World Substrate

“真正虚拟世界”的公共生活基质包括：

1. **Spatial Substrate**：区域、建筑、房间、门户、路径、视线、声音、容量和访问控制；
2. **Temporal Substrate**：时间、日历、时辰、季节、节庆、期限、周期；
3. **Schedule System**：人物、组织、设备、地点的日程和预约；
4. **Material/Object System**：物品、部件、容器、所有权、保管、可见性、信息内容；
5. **Body/Condition System**：健康、疲劳、疼痛、饥饿、疾病、行动能力和状态；
6. **Institution/Society System**：身份、职责、权限、义务、声誉、礼制、组织和制裁；
7. **Population Resolution**：核心人物、轻量 NPC、职责 NPC、群体/人口聚合的多分辨率；
8. **Autonomous Scheduler**：玩家不输入时，世界仍能按规则和事件继续推进。

真正的“活”来自 **Agent + 物质 + 制度 + 资源流 + 环境机制** 的系统涌现，而不是只有多角色聊天。

### 5.3 Physical Context / Reality Bridge

Reality-Coupled World 通过现实桥接入外部观察：

```text
GPS / Camera / Microphone / Weather / Calendar
Phone Sensors / BLE / IoT / open environmental data
AR Anchors / Maps / Robots / Human Reports
                      ↓
             PhysicalObservation
                      ↓
     source + timestamp + accuracy + confidence
                      ↓
            Validation / Fusion
                      ↓
             World Reality Bus
```

**PhysicalObservation 不是 Canonical Truth。** GPS 可能漂移、CV 可能识别错误、天气数据可能延迟、口述可能冲突。Reality Bridge 负责单位、时间、坐标、来源和置信度标准化，Validator 才决定它是否形成 Canonical Delta、待确认 Claim 或仅作为临时 Observation。

### 5.4 Co-Simulation Fabric

万相不重造所有专业模型。专业模拟器通过统一 `SimulationAdapter` 接入：

```text
initialize(world_slice)
ingest_state(snapshot)
advance(t0, t1)
emit_events()
emit_proposed_deltas()
checkpoint()
restore()
describe_assumptions()
describe_validity_envelope()
```

战役可接后勤、交通、战斗；城市可接交通、经济、人口；文物可接结构、光照、材料老化；科学世界可接 ODE/PDE、物理或机器人仿真。调度采用 **Multi-Rate + Event-Driven**，不要求整个世界一个固定 Tick。

### 5.5 Event / Branch / Temporal Kernel

采用事件溯源：

```text
Initial Snapshot + Ordered Event Log = Current State
```

支持 checkpoint、replay、fork、branch compare、time-travel debugging、correction event、worldline diff、deterministic seed。正式系统中“修改过去”优先创建修正事件或新分支，而不是直接改历史行。

---

## 6. Agency & Capability Plane：谁知道什么、想做什么、会做什么

### 6.1 Perception–Belief–Memory Kernel

严格分离：

```text
Canonical Truth
Public Knowledge
Group Knowledge
Individual Observation
Individual Belief
Private Memory
Rumour / Misinformation
Later Historical Record
```

记忆使用 **Temporal Epistemic Graph** 而非“聊天记录 + 向量库”：

```text
Event
→ ObservedBy
→ Interpretation
→ Emotion / Salience
→ Belief Update
→ Relationship Delta
→ Later Correction / Forgetting / Reinterpretation
```

同一事件可被不同角色形成不同记忆。事实记忆与 persona-conditioned interpretation 分离，防止长期人格被通用摘要抹平。

### 6.2 Actor / Organization Runtime

Actor 的控制器可以是 LLM、规则、状态机、小模型、人类、外部 Agent 或混合 Policy。Organization 必须显式建模成员、角色、权限、资源、派系、命令流、信息流和执行偏差，不能把国家、家族或军队简化为“大号聊天角色”。

### 6.3 Skill–Action–Affordance Kernel

统一决策链：

```text
Goal → Intent → Plan → Skill → Action → Affordance
     → Rule / Simulation → Outcome → WorldDelta
```

Skill 是可复用程序化能力，例如请安、探病、传话、写信、调查来源、修复器物、调动部队、组织运输、做实验。Skill 定义前置条件、权限、所需能力/知识、步骤、时间、成本、失败模式、可观察性、副作用与验证方式。

Affordance 决定实体在**当前状态**下允许什么动作。一封信可以 read/seal/hide/deliver/burn；馆藏文物可以 inspect/annotate/measure，但可能禁止 destructive_test。

### 6.4 Capability & Learning Kernel

Learning 不是教育独占，而是所有主体的能力演化：

```text
Knowledge
Skill
Misconception
Mastery
Confidence
Experience
Practice
Habit
Transfer
Capability
```

学生学习对称性、NPC 学会剑术、指挥 Agent 掌握新的情报分析流程，本质上都通过 `CapabilityDelta` 更新。

对于学习场景，增加 `LearnerState`、`LearningArtifact`、`PracticeRecord` 和 `AssessmentEvidence`。长期形成 `Learning Worldline / Learning Biography`，而不是只有积分或分数。

---

## 7. Orchestration & Control Plane：为什么此刻发生这件事、谁在控制谁

### 7.1 Opportunity–Challenge–Event Kernel

把“动态任务”提升为通用内核：

```text
WorldState + ActorState + Context + Affordances + Goals + Rules
                              ↓
                    Opportunity Detection
                              ↓
                      Event Candidate
                              ↓
                  Planner / Composer
                              ↓
                 Safety / Rule Validator
                              ↓
                    Executable Event
                              ↓
                 Action / Evidence / Outcome
```

核心对象分开：`Opportunity`、`ChallengeSpec`、`Action`、`Event`、`Outcome`。

同一个内核可以产生：

- 红楼梦中的探访、误会、诗社机会；
- 战役中的补给危机、侦察任务；
- 博物馆中的纹饰调查、物件生命史探索；
- 家族世界中的“识别旧照片人物”调查；
- 现实社区里的雨水、叶片、风、桥梁、声音等科学挑战。

LLM 只负责开放式组合和表达；科学正确性、安全、材料、地点、权限、可行性由规则/知识图/专业模型验证。

### 7.2 Embodiment / Director / Experiment Kernel

正式控制模式：Observer、Player Avatar、Embodiment、Co-Embodiment、Director、Curator、Experimenter、External Agent。

`EmbodimentLease` 保证同一 Actor 同时只有一个主控制器。接管原著人物时，原 AI 主策略暂停，ShadowPolicy 只负责角色化表达、知识边界提示、微动作和可选建议。用户退出后 AI 必须继承接管期间的真实后果。

Experiment Runtime 负责分支、参数扫描、随机种子、多轮运行、敏感性分析、消融、因果干预和 ValidityEnvelope；推演结果表达为“在这些假设下的分布”，不冒充确定预测。

---

## 8. Hosting & Experience Plane：世界怎样长期存在、怎样被看见

### 8.1 World Host / Lifecycle / Multiplayer Kernel

World Host 是真正的世界服务器，负责：Instance 生命周期、Scheduler、Agent 激活、Co-Simulation、Session、Snapshot、Multiplayer、故障恢复、资源预算、持久化和审计。

生命周期与用户 Session 解耦：

```text
PAUSED
REALTIME
ACCELERATED
EVENT_DRIVEN
BACKGROUND_SIMULATION
FULL_AUTONOMY
BATCH_SIMULATION
```

`World Authority != API Server != Game Client != LLM Agent`。多人客户端只提交命令和接收经过权限/认知过滤的 Projection。

### 8.2 Projection / Rendering / Network Gateway

Projection 不拥有真相：

```text
Canonical World
→ Perception / Rights Filter
→ World Projection Bus
→ Text / SillyTavern Adapter
→ React/Phaser 2D
→ Godot Native 2D/3D
→ Babylon.js Web 3D/WebXR
→ Digital Human
→ Museum Kiosk
→ Wargame UI
→ Generated Video / Perceptual World Model
```

3D 资产优先使用 glTF；复杂组合场景可用 OpenUSD；大规模地理 3D 可用 3D Tiles；博物馆媒体使用 IIIF；生成式世界模型输出只进入 Asset/Projection Candidate，**不能直接 Commit Canonical State**。

---

## 9. 三条核心总线与 Asset Foundry

### 9.1 World Reality Bus

所有会改变世界的系统只能提交 Proposed Delta：

```text
Actor / Rule / Physics / Battle / Economy / Sensor Fusion / Conservation
                              ↓
                    Proposed WorldDelta
                              ↓
                 Validation + Adjudication
                              ↓
                      Commit Authority
                              ↓
                  Canonical World State
```

### 9.2 World Projection Bus

所有终端读取经过认知、权限、隐私和文化协议过滤后的 Projection；同一存档可同时投影成文字、2D、3D、数字人、博物馆大屏或战棋。

### 9.3 Evidence / Context Bus

Source、Claim、现实 Observation、模型推断、人工审核之间通过统一 Evidence/Context Envelope 传递，保留来源和置信度，避免“RAG 找到一句话”直接变成世界真相。

### 9.4 World Asset Foundry

世界编译器输出语义场景规格，Asset Foundry 可调用传统 DCC、3D 扫描、摄影测量或 3D 世界生成模型产生 `AssetCandidate`：

**Asset Foundry 流程**：Semantic Scene Spec → Asset Generator / Scan / Reconstruction → Mesh / 3DGS / Texture / Animation Candidate → Geometry Validation → Semantic Binding → Rights & Human Review → Asset Pack。

Asset Foundry 负责“世界看起来像什么”；Canonical Kernel 负责“世界实际上是什么”。

---
## 9.5 Capability Fabric：一切能力可组合，唯现实承诺有唯一边界

自 v5.1 起，在 5 Planes / 16 Kernels 外再引入一个横向 Meta Runtime：`Wanxiang Capability Fabric`。它不拥有世界事实，而负责动态组合世界运行所需的能力。

能力包括：

典型能力包括：LLM/Embedding/Retrieval、Agent Harness、Domain/Rule/Skill、Navigation/Physics、Simulation/Co-Simulation、Projection/Rendering、Voice/Digital Human、Reality Connector/Sensor、Storage/Search/Vector DB、Evaluation/Safety/Audit。

统一使用 Service Definition → Provider → Consumer：消费者依赖能力契约，不 import 具体实现。例如 MoveResolver 只依赖 `NavigationService`；其 Provider 可以是 Godot、Recast 或 GridNavigation。

运行时能力必须声明：

- `capability_id` / contract version；
- provided services / required services；
- scope；
- permissions；
- network / file / model access；
- runtime side effects；
- disposer / teardown；
- health / readiness；
- schema compatibility；
- deterministic/replay characteristics；
- security and rights requirements。

Capability Fabric 的核心原则来自现代插件运行时的时空可组合思想：依赖应声明式表达，注册副作用必须可逆，加载/卸载/替换应有生命周期和作用域，而不是形成全局单例和隐式 import 网。

## 9.6 Runtime Effect 与 World Effect 必须绝对分离

`Runtime Effect` 可以被卸载/回滚：监听器、Provider、Worker、Timer、缓存、连接、Prompt Hook、Tool Schema、UI Extension 等。

`World Effect` 是已被 Commit 的历史：人物移动、物品焚毁、命令送达、家庭成员出生、文物修复、某制度成立等。

核心约束：`plugin.dispose()` **不等于** `undo committed world history`。

撤销 World Effect 必须通过 Correction/Reversal Event 或从历史节点 Fork 新 Branch，不能通过卸载插件静默改写过去。

## 9.7 Agent Harness Provider ABI

Agent Harness 不是世界。万相定义统一 `AgentHarnessProvider`，可接：

Provider 可包括 `NativeWanxiangProvider`、`DeepSeekHarnessProvider`、`OpenStoryProvider`、`ConcordiaProvider`、`RuleBasedProvider`、`HumanPlayerProvider` 与未来实现。

Provider 接收的是 Wanxiang 生成的 `PerceptionEnvelope`、角色 Fact Space、允许 Skill/Action、Memory Retrieval 结果和 Context Policy；输出只能是 `Intent / Plan / Tool/Skill Request / Dialogue`，不得直接获得 Canonical Mutable State。

标准关系：

标准链路：Wanxiang World → PerceptionEnvelope → Agent Harness Provider → Actor Intent → World Reality Bus → Validate / Resolve / Commit → WorldDelta。

## 9.8 DeepSeek Harness / Cordis 的正式位置

官方 `deepseek-ai/deepseek-harness` 将自身定义为由 DeepSeek AI 开发的开源 Agent Harness，并采用 “Everything is a Plugin” 架构；底层 Cordis 使用稳定 Service key、声明式依赖、类型化事件和可逆注册副作用。该项目截至 2026-08-14 仍明确处于 Developer Preview，存在破坏兼容性的快速变化。

因此万相不以 DSH fork 作为 World OS 基座，而采用两层策略：

1. **吸收原则**：Service/Provider、Context Scope、Declarative Dependency、Reversible Runtime Effects、Profile/Bundle/Patch、Transactional Reload 等进入 Capability Fabric 设计；
2. **Provider 接入**：DSH 作为 Agent Harness Provider 候选，与 Native/OpenStory/Human 等并列；
3. **保持解耦**：Authority Microkernel、Committed Ledger、Branch、Evidence/Rights 不依赖 DSH/Cordis 的具体实现；即使未来替换 Harness，World Instance 的历史仍然有效。

## 9.9 三重 Ledger

### World Ledger

记录“世界发生了什么”：Committed Event、WorldDelta、世界时间、分支、来源、裁决和结果。

### Actor Trajectory Ledger

记录“主体为什么这样做”：Observation、Retrieved Memory、Belief、模型可见上下文摘要/哈希、Provider/Model 版本、Tool/Skill、Plan、Intent、Adjudication、Outcome。

### Runtime Control Ledger

记录“当时系统是怎样配置的”：Provider 安装/卸载、Domain/Rule/Simulation 版本、Profile/Patch、模型切换、权限、参数和迁移。

三者组合才能真正重现“某个世界在某时刻为什么得到这个结果”。

## 9.10 World Invariant Registry

Invariant 分三层：

- **Kernel Invariants**：禁止绕过 Commit、Entity/World ID 语义、Committed Event 不可静默改写、Branch 隔离、Replay 契约等；
- **Domain Invariants**：家庭证据冲突不得自动抹平、战役资源不得无源生成、博物馆 Reconstruction 不得覆盖 Physical Evidence 等；
- **World Invariants**：某一具体世界/版本的正典、权限、文化协议、Scenario 限制。

Invariant 必须在 Commit 前执行，并能在测试、回放、插件升级和 World Migration 中复用。

## 9.11 Bounded Runtime Evolution

万相允许世界运行时提出新 Skill、Rule、Simulation Adapter、Memory Policy、Event Generator、Projection 或 Domain Capability，但必须是受限演化：

受限演化链路：Capability Proposal → Sandbox → Shadow World / Branch Clone → Invariant Tests → Regression / Security / Cost / Determinism Tests → Simulation Evaluation → Approval Policy → Transactional Activate → Runtime Control Ledger → Observe / Rollback if needed。

普通 Agent 不得修改：Commit Authority、Branch 语义、Evidence/Rights 契约、World Identity、核心安全边界。

---

# 第三篇：世界包与运行协议

## 9. World Package 标准结构

```text
world_package/
├── manifest.yaml
├── dependencies.yaml
├── sources/
├── evidence/
├── rights/
├── entities/
├── components/
├── relations/
├── organizations/
├── spaces/
├── objects/
├── timelines/
├── rules/
├── skills/
├── schedules/
├── scenarios/
├── canon/
├── assets/
├── simulations/
├── projections/
└── evals/
```

World Pack 不是数据库备份，而是可移植、可审查、可实例化的世界定义。

## 10. Instance 协议

创建世界实例：

```text
select WorldPack(version)
+ resolve Domain dependencies
+ select Scenario
+ apply overrides
+ seed
→ instantiate()
→ WorldInstance
```

World Instance 必须记录：world_pack_version、domain_versions、schema_version、model_bundle、random_seed、created_by、rights_scope。

## 11. 运行循环

统一循环：

```text
Snapshot
→ Observe
→ Deliberate / Propose
→ Skill Expansion
→ Validate
→ Resolve / Co-Simulate
→ Commit WorldDelta
→ Update Belief / Memory
→ Director / Experiment Hooks
→ Render / Project
→ Audit
```

这条循环是文学世界、战争世界、家族世界、博物馆世界共用的最小语义协议。

---

# 第四篇：与 SillyTavern / 酒馆类产品的关系

## 12. 核心差异

酒馆类系统的中心通常是：Character Card + Persona + Lorebook / World Info + Chat History + RAG → Prompt → LLM → Response。

万相的中心是：

```text
World Pack
→ Canonical World State
→ Perception
→ Action
→ Rule / Simulator
→ WorldDelta
→ Persistent History
```

因此差异不是“角色卡更长”，而是：

- Lorebook 主要是给模型看的背景；万相的 World State 是系统权威事实；
- 酒馆中一封信通常存在于上下文里；万相中信件是有位置、所有者、可见性和知识传播状态的 Entity；
- 酒馆的“世界变化”主要通过文本延续；万相变化必须经过验证、裁决和 Commit；
- 酒馆的聊天 Session 是主要体验；万相的 World Instance 可脱离聊天持续运行。

## 13. 兼容关系

万相不必排斥酒馆。可以提供 `SillyTavernAdapter`：

```text
Wanxiang World Server
→ Perception Envelope
→ SillyTavern / Chat Client
→ Player Text Intent
→ Wanxiang Action Compiler
→ Runtime
```

SillyTavern 角色卡和 World Info 可以作为 CharacterPackage / WorldKnowledge Candidate 导入，但必须经过 Schema 编译、证据绑定和知识边界校验，不能直接等同于万相 World Pack。

---

# 第五篇：典型世界实例

## 14. 《红楼梦》：文学活世界实例

### 14.1 正确对象关系

```text
Narrative Domain
+ Household Society Domain
+ Historical China Domain
+ DreamOfRedChamber World Pack
+ Scenario
→ RedChamber World Instance
```

### 14.2 World Pack 内容

- 原著版本和章节来源；
- 人物、别名和人生阶段；
- 贾府/荣国府/宁国府等组织；
- 大观园空间图；
- 人物关系、主观认知和秘密；
- 物品、书信、礼物、药物、服饰；
- 日常作息、礼仪、职责；
- 正典时间线；
- 体验补全层；
- 2D/3D/数字人资产映射。

### 14.3 真正扮演林黛玉

用户选择世界版本、Scenario 和人生阶段，获得 `EmbodimentLease`。系统给用户的不是上帝状态，而是林黛玉的 Perception Envelope。用户可使用移动、说话、观察、委托、写信、赠礼、探病等世界动作；影子 Agent 只负责角色化建议，不替用户作重大决定。退出后 AI 继承用户留下的世界后果。

### 14.4 七日活世界验收

至少验证：日夜和日程自动推进；物品持续存在；秘密不会自动泄露；轻量 NPC 可按职责行动；用户退出后角色 AI 继续；分支不污染正典；七日后状态可由事件日志重建。

---

## 15. 辽沈战役：历史战役实例

```text
Historical China Domain
+ Campaign Domain
+ Logistics Domain
+ Command Organization Domain
+ Liaoshen Campaign World Pack
→ Liaoshen World Instance
```

World Pack 保存历史地图、道路铁路、部队序列、指挥体系、命令、电报、后勤、历史快照、情报和来源争议。指挥者只能看到当时可获得的信息，Agent 只能提出命令，移动/后勤/战斗由专业模型或规则裁决。历史模式、参与模式、反事实模式必须分开。

---

# 第六篇：家谱与“家族活世界”

## 16. 家谱为什么不能只做成一棵树

传统家谱软件主要回答“谁是谁的什么关系”。万相要回答的是：

> **这个家庭在什么时间、什么地点、什么社会环境里生活；每个人经历了什么；哪些资料支持这些经历；家人如何迁徙、工作、相识、分离、传承；今天的家庭成员怎样进入、观察和保护这些记忆。**

所以万相中的家谱应升级为：

> **Family World Pack + Family World Instance。**

家谱树只是其中一个 Projection。

## 17. 家族世界的数据输入

### 17.1 标准谱系数据

优先支持 FamilySearch GEDCOM 7.x 的导入与导出，并支持 GEDZIP 媒体封装；同时可通过 Adapter 与 Gramps/Gramps Web 数据互操作。GEDCOM 适合保存个人、家庭、事件、来源、仓储和多媒体链接，但万相内部仍要转换为自己的 Claim / Event / Evidence 模型。

### 17.2 非结构化家庭资料

- 老照片；
- 相册页；
- 身份证件、出生/婚姻/死亡证明；
- 族谱扫描页；
- 日记、家书；
- 录音、录像；
- 口述史访谈；
- 房产/学校/工作资料；
- 墓碑、祠堂、祖居照片；
- 地图和迁徙记录；
- 家庭物品及其故事。

这些资料不应被“抽取成一个确定事实”后丢掉原件；必须保留原始数字对象、定位到页/区域/时间段，并生成可追溯 Claim。

## 18. 家族世界核心模型

```text
PersonEntity
KinshipRelation
HouseholdEntity
LifeEvent
ResidenceEvent
MigrationEvent
EducationEvent
OccupationEvent
Marriage / Partnership
Parenthood / Adoption
Death / Burial
FamilyObject
MediaAsset
OralHistory
Claim
SourceCitation
ConsentRecord
LegacyInstruction
PrivacyPolicy
```

### 18.1 关系不是永恒静态边

家庭关系必须带时间和来源。例如“同住”“抚养”“监护”“继亲”“收养”“断联”“离异”都不能仅用 parent/child 两个字段表示。

### 18.2 家庭事实必须 Claim 化

不同亲属对同一事件可能说法不同：

```text
EventCandidate: 1958 年迁往某地
Claim A: 外祖母口述，1958 年春
Claim B: 户籍材料，1958 年 8 月
Claim C: 叔父回忆，1959 年
```

万相保存三个 Claim 和证据，不强行把模型猜测写成“1958-03-01”。

## 19. Family World Pack

```text
family_world/
├── manifest.yaml
├── gedcom/
├── people/
├── households/
├── kinship/
├── life_events/
├── places/
├── migrations/
├── family_objects/
├── photos/
├── audio_video/
├── oral_histories/
├── claims/
├── sources/
├── consent/
├── privacy/
├── legacy_instructions/
├── scenarios/
└── assets/
```

## 20. 家族世界如何“活起来”

### 20.1 时间地图

用户不仅看到族谱，还可以拖动时间轴：

```text
1900 → 1930 → 1950 → 1980 → 2026
```

地图上显示当时的家庭成员、住址、迁徙、学校、工作地、重大事件和家庭物品所在位置。

### 20.2 家庭场景重建

例如“1986 年春节祖居”。系统根据照片、口述史、房屋资料和时代数据创建场景，但所有内容分层显示：

- 确认存在；
- 资料支持重建；
- 时代合理补全；
- 体验性生成。

用户可以以自己、父母、祖辈或观察者身份进入。

### 20.3 家庭物品是世界实体

一块手表、一封信、一张毕业照、一件军装可以有自己的 Object Biography：谁拥有过、在哪出现、被谁拍摄、有什么修复、什么时候转交给下一代。

### 20.4 家族故事不是自动“美化”

系统允许冲突记忆并存。不同家庭成员可以对同一事件保留不同叙述，并通过“谁说的、何时说的、依据是什么”呈现，而不是由 AI 合并成唯一版本。

## 21. 生前主动蒸馏：Living Archive

家族世界最有价值的能力之一，是让仍在世的人主动建立自己的数字人生档案：

- 定期访谈；
- 回忆关键人生事件；
- 给照片补人物、地点和故事；
- 记录价值观、语言习惯、常用表达；
- 指定哪些内容公开、仅家人可见、死后若干年可见或永不公开；
- 指定是否允许未来生成式数字人物使用自己的声音、外貌和文字。

这不是“训练一个数字灵魂”，而是形成带来源和许可的 `Personal Legacy Package`。

## 22. 数字祖先 / 家族数字人应该分三种模式

### 22.1 Evidence Mode

只根据本人原话、已知事实、资料和明确记忆回答；资料不足直接说不知道。适合纪念、教育、研究。

### 22.2 Reconstructed Persona Mode

系统可以在明确标记“推断/重建”的前提下，依据人生经历、时代、语言材料和关系生成合理回应。不能冒充真实录音或本人确切观点。

### 22.3 Creative Legacy Mode

家庭成员主动允许后，可以进行更自由的文学化互动；必须始终显示这是创作版本。

## 23. 家族隐私与伦理是底层能力

家庭世界默认应该是 Private / Family-Only，而不是公开社区。每一条资料都可以设：

- owner；
- controller；
- allowed_viewers；
- allowed_generation；
- allowed_training；
- allowed_export；
- posthumous_release；
- deletion / revocation；
- biometric_restriction；
- voice_likeness_permission。

对仍在世者的脸、声音、联系方式、病历、基因、身份证件等必须采用更高权限层。系统不应该提供无约束的公开人脸“寻亲”功能。

## 24. 家族世界的用户产品

一个完整 Family UI 可以同时有：

- 族谱图；
- 人生时间线；
- 家族地图和迁徙；
- 相册/文档档案馆；
- 家庭物品博物馆；
- 口述史播放器；
- 2D 可探索祖居；
- 家族人物页；
- 证据/争议页；
- 数字人物；
- 私密权限中心；
- 世界分支和“如果当年……”的家庭历史体验（仅标为创作/反事实）。

## 25. 家谱 MVP

第一版不做全家族“复活”，而做：

- 导入 GEDCOM 7；
- 20–100 人谱系；
- 照片和口述史上传；
- 5–10 个地点；
- 人生事件和迁徙图；
- Claim + Evidence；
- 家庭权限；
- 一个祖居 2D 场景；
- 1 个经许可的数字人物；
- Evidence/Reconstruction 两种回答模式。

达到这一步，万相家谱已经明显超越“家谱树+相册”。

---

# 第七篇：博物馆、文化遗产与文物虚拟模拟

## 26. 博物馆在万相里是什么

博物馆也不应成为一套独立底层。它是：

```text
Heritage Domain Pack
+ Museum Collection Pack
+ Exhibition / Scenario Pack
→ Museum World Instance
```

其中单件文物也可以单独成为 `HeritageObject Pack`，被装入不同 Museum World、历史重建世界或教育场景中。

## 27. 一个文物绝不等于一个 3D 模型

必须区分四种对象：

### 27.1 Physical Heritage Object

现实中真实存在的原件：馆藏号、尺寸、材质、当前状态、保管地点、权利、修复记录。

### 27.2 Digital Surrogate

摄影、扫描、摄影测量、LiDAR、CT、光谱、音频等形成的数字替身。它只是测量/记录结果。

### 27.3 Semantic Heritage Twin

万相中的语义文物实体：把 Digital Surrogate 与 CIDOC/Linked Art 风格的制作、人物、地点、事件、所有权、修复、部件、材料、证据和权利绑定起来。

### 27.4 Reconstruction / Simulation Model

基于研究假设创建的“原貌重建”“功能模型”“材料模型”“机械模型”。必须与实物数字替身分开，不能把推测的原貌冒充扫描结果。

## 28. 文化遗产数据模型

推荐内部对象至少包括：

```text
HeritageObject
ObjectPart
Material
Dimension
ProductionEvent
CreationEvent
UseEvent
Transfer / Acquisition
Ownership / Custody
LocationEvent
Excavation / Discovery
ConditionAssessment
ConservationTreatment
ExhibitionEvent
DigitalCapture
DigitalSurrogate
ReconstructionHypothesis
Annotation
Rights
CulturalProtocol
Evidence
```

CIDOC CRM 的核心价值正是用事件式语义连接对象、人物、地点、时间、活动和证据；Linked Art 可以作为更工程友好的 JSON-LD 互操作层。

## 29. 博物馆资料接入

### 29.1 2D/音视频：IIIF

IIIF Presentation API 可将一个复杂数字对象组织为 Manifest、Canvas、Range 和 Annotation，并关联图像、音频、视频、文本或 3D rendering。万相可将 IIIF Manifest 作为 `CollectionAssetSource` 导入，保留原 URI、版权和 Annotation。

### 29.2 馆藏语义：CIDOC CRM / Linked Art

万相不需要完整复制所有 CIDOC 类，而应建立内部简化模型并提供双向 Adapter：

```text
CIDOC / Linked Art
↕
Wanxiang Heritage Schema
```

### 29.3 3D：glTF / OpenUSD / 3D Tiles

- 单件运行时 3D 模型：glTF/GLB；
- 复杂展厅、分层资产、制作管线：OpenUSD；
- 大型遗址、城市或超大点云/摄影测量：3D Tiles；
- 原始高精度档案：保留摄影测量、点云、LiDAR 等原始数据和处理链。

### 29.4 3D 原始数据的保存

OpenHeritage3D 一类实践说明，文化遗产 3D 不应该只保存“给网页看的轻量模型”，还应保存具有研究价值的原始/高精度采集数据、元数据和处理过程。

## 30. 文物数字化流水线

```text
馆藏登记
→ 权利/文化协议检查
→ 2D/3D/光谱/CT 等采集
→ 原始数据归档
→ 数据处理与多精度资产生成
→ 语义绑定
→ 部件/材质标注
→ 状态和修复记录
→ Evidence Binding
→ Asset Validation
→ HeritageObject Pack
```

所有自动识别结果都应是 Candidate，不能直接覆盖馆员权威记录。

## 31. “文物虚拟模拟”到底包括哪些层次

### 31.1 Virtual Inspection

最基础：放大、旋转、切换光照、查看高分辨率细节、剖面、标注、尺寸、部件和材质。这属于数字查看，不是真正模拟。

### 31.2 Contextual Re-Embedding

把文物放回可能的历史环境：

- 青铜器放回礼制/宴飨场景；
- 壁画放回原建筑；
- 兵器放回装备体系；
- 工具放回生产场景；
- 服装穿回特定身份数字人。

环境必须区分“确认背景”和“体验性重建”。

### 31.3 Object Biography Simulation

以时间轴重放文物的生命史：

```text
制作
→ 使用
→ 转移
→ 埋藏/收藏
→ 发现
→ 入藏
→ 修复
→ 展览
→ 当前状态
```

用户可以在每一阶段查看当时位置、相关人物、来源证据和不确定性。

### 31.4 Functional Simulation

对“怎么用”的文物建立可执行功能模型，例如机械装置、乐器、工具、交通工具、容器、武器或科学仪器。此时必须由 Heritage Domain 挂接专门机制模型，而不是让 LLM 猜结果。

### 31.5 Reconstruction Simulation

对残缺建筑、器物、颜色、纹样或结构提出多种重建假设：A/B/C 版本并存，分别绑定依据和置信度；用户可以切换版本，不应只给一个“AI 修复完成图”。

### 31.6 Conservation Simulation

在有可靠材料参数和专家模型时，可以模拟：

- 光照暴露；
- 湿度/温度；
- 腐蚀或老化趋势；
- 结构应力；
- 包装运输；
- 修复方案影响。

这类结果必须显示模型版本、输入参数和 Validity Envelope，不得当作真实文保结论替代专业人员。

### 31.7 Counterfactual / Educational Simulation

例如“如果不进行某次修复会怎样”“不同保存条件对长期状态的影响”，用于教学和研究假设。必须与正式馆藏档案分支隔离。

## 32. Heritage Object Pack

```text
heritage_object_pack/
├── manifest.yaml
├── catalog_record/
├── sources/
├── evidence/
├── rights/
├── cultural_protocols/
├── object/
├── parts/
├── materials/
├── dimensions/
├── provenance/
├── production/
├── use_history/
├── condition/
├── conservation/
├── exhibitions/
├── captures/
├── assets/
│   ├── images/
│   ├── iiif/
│   ├── gltf/
│   ├── usd/
│   └── high_fidelity/
├── reconstructions/
├── simulations/
├── annotations/
└── evals/
```

## 33. 一个青铜器实例如何运行

假设某馆有一件青铜礼器：

1. 现实藏品作为 `PhysicalObject`；
2. 馆藏系统记录尺寸、材质、纹饰、来源和修复；
3. 3D 扫描生成 `DigitalSurrogate-v1`；
4. 纹饰和铭文在 3D 表面形成 Annotation；
5. 制作年代、出土地点等分别作为带证据 Claim；
6. 研究人员提出两个“原始使用场景” Reconstruction；
7. 万相生成两个独立 Scenario；
8. 用户进入其中一个历史场景，查看器物在当时空间、人物和礼仪中的位置；
9. 用户可触发“倒入液体”等教育性交互，真正液体行为由物理/流体近似模型处理；
10. 系统始终标明哪些是实物记录、哪些是推断、哪些是交互模拟。

## 34. 博物馆世界的四种实例

### 34.1 Current Museum Instance

重建当前展厅，文物位置与展签、路线、导览一致。适用于线上展馆、数字孪生、无障碍访问。

### 34.2 Historical Context Instance

将选定文物放入一个历史时期世界中，结合人物、社会制度、建筑和其他器物，提供“回到使用现场”的体验。

### 34.3 Object Biography Instance

整个世界围绕一件物品的生命周期组织，用户沿时间进入不同阶段。

### 34.4 Conservation Lab Instance

面向研究和教育，展示扫描、检测、修复记录、材料状态和方案模拟。

## 35. 文化协议与敏感材料

博物馆不能只有 Copyright。某些知识、影像、遗骸、仪式物品或传统知识具有社区特定的使用条件。万相的 Rights Layer 应支持：

- 法律权利；
- 机构授权；
- 社区文化协议；
- 季节性访问；
- 性别/身份限制；
- 非商业；
- 社区内部；
- 禁止生成式改编；
- 禁止训练；
- 归属和社区话语。

可通过 Local Contexts TK/BC Labels 和类似文化协议机制作为 Adapter。文化协议和版权不是同一回事，两者应并列保存。

## 36. 博物馆与数字人物

馆员、历史人物或虚拟讲解员只是 Projection + Actor，并不拥有馆藏事实。数字人物回答时只能访问其权限范围内的 Heritage Knowledge View，并把“馆藏记录”“研究观点”“体验重建”清楚区分。

## 37. 博物馆 MVP

第一版建议只做一个小型展览：

- 10–30 件藏品；
- 每件有馆藏元数据、图片和来源；
- 3–5 件带 3D；
- IIIF Manifest 导入；
- Linked Art/CIDOC 映射；
- 1 个 2D/3D 展厅；
- 1 个 Object Biography；
- 1 个历史背景重建 Scenario；
- 1 个数字讲解员；
- 权利和 Evidence 标签；
- 正式馆藏与重建内容严格分层。

---

# 第八篇：家谱、博物馆、历史世界为什么可以共享同一底层

## 38. 共通本质

三者表面完全不同，但底层其实都是：

```text
Entity
+ Event
+ Time
+ Place
+ Relation
+ Claim
+ Evidence
+ Rights
+ Asset
+ World State
```

家谱中的“祖父 1952 年搬家”、博物馆中的“文物 1930 年被某机构收藏”、历史中的“某人物 1948 年调任”都可以表达为 Event + Actor + Place + Time + Evidence。

区别只在 Domain Pack 和运行方式。

## 39. 家庭物品与博物馆文物可以直接互通

一个家族物品未来捐入博物馆：

```text
FamilyObject
→ TransferEvent
→ MuseumAcquisition
→ HeritageObject
```

它的家族记忆、照片、口述史可以成为博物馆 provenance 的 Evidence；博物馆的修复和展陈又成为这个物品后续 Object Biography。

这会形成万相非常独特的“People–Object–Place–Event World Graph”。

---

# 第九篇：工程架构

## 40. 首阶段采用模块化单体

不建议从第一天拆二十个微服务。推荐：

```text
wanxiang-world/
├── apps/
│   ├── api/
│   ├── studio-web/
│   ├── player-web/
│   └── worker/
├── packages/
│   ├── domain-core/
│   ├── world-definition/
│   ├── world-runtime/
│   ├── living-substrate/
│   ├── agency/
│   ├── cognition/
│   ├── skills/
│   ├── simulation/
│   ├── embodiment/
│   ├── projection/
│   ├── evidence/
│   ├── rights/
│   ├── persistence/
│   ├── adapters/
│   └── evals/
├── domains/
│   ├── narrative/
│   ├── household/
│   ├── genealogy/
│   ├── heritage/
│   └── campaign/
├── worlds/
├── tests/
└── docs/
```

### 40.1 推荐技术栈

- 后端：Python 3.12+、FastAPI、Pydantic v2、SQLAlchemy、Alembic；
- 主数据库：PostgreSQL；本地开发 SQLite；
- 对象存储：S3 兼容；
- 向量检索：pgvector 或独立向量库，仅作检索，不作世界真相；
- 图查询：先以 PostgreSQL relation/event tables + materialized projections 实现，规模需要时再接图数据库；
- 消息/任务：首版可内进程 Event Bus；后期 Redis/NATS/Kafka；
- 前端：React + TypeScript；
- 2D：Phaser；
- 3D：Godot 或 Babylon.js；
- 测试：pytest、Hypothesis、Vitest、Playwright；
- 部署：Docker Compose 起步。

## 41. 数据持久化分层

```text
PostgreSQL
- 世界定义元数据
- Entity / Component / Relation
- Event Log
- Claims / Evidence / Rights
- Branch / Run / Session

Object Storage
- 原始文档
- 图片 / 音频 / 视频
- 3D / 点云 / USD / glTF
- 模型输出

Search Index
- 文本全文检索
- 向量检索

Derived Projections
- 时间线
- 关系图
- 地图索引
- 家谱树
- 馆藏检索
```

Derived Projection 永远可以从权威数据重建，不应成为唯一真相。

## 42. API 基线

```text
POST /world-packs/import
POST /worlds/instantiate
GET  /worlds/{id}/snapshot
POST /worlds/{id}/observe
POST /worlds/{id}/actions
POST /worlds/{id}/advance
POST /worlds/{id}/checkpoint
POST /worlds/{id}/branch
GET  /worlds/{id}/events
GET  /worlds/{id}/diff

POST /embodiment/acquire
POST /embodiment/release

POST /sources/import
GET  /claims/{id}/evidence

POST /family/gedcom/import
GET  /family/{id}/pedigree
GET  /family/{id}/timeline

POST /heritage/iiif/import
POST /heritage/linked-art/import
GET  /heritage/objects/{id}
POST /heritage/objects/{id}/scenario
```

## 43. World Environment API

为 Agent 训练和评测提供：

```text
create_world(package)
reset(snapshot=None)
observe(actor_id)
legal_actions(actor_id)
step(action_bundle)
advance(time)
checkpoint()
restore()
branch()
metrics()
close()
```

可做 Gymnasium / PettingZoo Adapter，使万相世界同时成为 AI Agent 环境。

---

# 第十篇：标准与开放生态策略

## 44. 不自创已有标准

| 领域 | 优先标准 / 生态 | 万相中的定位 |
|---|---|---|
| 家谱交换 | FamilySearch GEDCOM 7.x / GEDZIP | Import/Export Adapter |
| 家谱协作 | Gramps / Gramps Web | 兼容与迁移参考 |
| 文化遗产语义 | CIDOC CRM 7.1.3 / ISO 21127:2023 | Heritage Semantic Adapter |
| 艺术馆 Linked Data | Linked Art JSON-LD | 面向开发者的文化遗产交换 |
| 数字藏品呈现 | IIIF 3.x | 图像/音视频/复合对象 Manifest |
| 3D 运行资产 | glTF 2.0 | Asset Pack |
| 复杂 3D 场景 | OpenUSD | 3D Pipeline / Scene Composition |
| 大型空间 3D | OGC 3D Tiles 1.1 | 遗址、城市、点云流式加载 |
| 社区文化协议 | Local Contexts TK/BC Labels | Cultural Protocol Adapter |
| AI 环境 | Gymnasium / PettingZoo | Eval / Agent Adapter |

## 45. 研究和实现依据（基础部分；完整目录见附录 C，截至 2026-08-11）

本架构参考但不等同于以下标准和实践：

- FamilySearch GEDCOM 7.0.x：谱系数据交换、来源、媒体和 GEDZIP；
- Gramps Web：授权用户协作编辑人物、家庭、事件、地点、来源、引用、媒体和笔记；
- IIIF Presentation API 3.0：Manifest/Canvas/Annotation 的数字对象呈现；
- CIDOC CRM：文化遗产异构信息集成的事件式概念模型；
- Linked Art：基于 CIDOC CRM 子集的 JSON-LD 开发者模型；
- Smithsonian 3D：3D 扫描、教育、注释、保护状态对比的博物馆实践；
- OpenHeritage3D：文化遗产高精度 3D 原始数据开放、元数据和长期保存实践；
- glTF、OpenUSD、3D Tiles：3D 资产、复杂场景和大规模空间数据互操作；
- Local Contexts：社区特定文化知识的来源、访问和使用协议。

---

# 第十一篇：权利、隐私、可信度与治理

## 46. 统一 Rights Envelope

任何 Entity / Asset / Claim / World / Character 都可附：

```text
legal_rights
copyright
privacy_class
personal_data_class
biometric_policy
training_permission
generation_permission
commercial_use
redistribution
community_protocol
access_conditions
posthumous_policy
revocation_policy
```

## 47. 内容真实性标签

所有输出都应可显示：

```text
事实/馆藏记录
来源记载
本人自述
他人回忆
研究者解释
模型推断
历史/文化重建
反事实模拟
用户虚构
```

## 48. 数字人物治理

现实或近现代人物数字化必须区分：

- 本人授权；
- 家属/权利方授权；
- 公共历史人物资料使用；
- 纯教育性重建；
- 禁止仿声/仿脸；
- 禁止以第一人称制造无来源观点。

家族数字人尤其应支持撤销、继承和身后公开策略。

---

# 第十二篇：评测体系

## 49. Core Invariant Tests

- 守恒；
- 权限；
- 时间单调；
- 空间可达；
- 容器一致性；
- 信息隔离；
- 分支隔离；
- Replay；
- Determinism。

## 50. Character / Society Tests

- 人格一致性；
- 人生阶段；
- 知识越界；
- 记忆冲突；
- 关系更新；
- 组织命令执行；
- Cognitive LOD 升降级。

## 51. Family Tests

- GEDCOM round-trip；
- 谱系关系合法性；
- 来源引用不丢失；
- living-person 隐私；
- 同一事件冲突 Claim 共存；
- 家庭媒体权限；
- 数字人物 Evidence Mode 不虚构。

## 52. Heritage Tests

- IIIF Manifest round-trip/引用；
- Linked Art / CIDOC 映射；
- 实物、数字替身和重建版本不混淆；
- 3D asset semantic binding；
- 权利和文化协议 enforcement；
- 修复/状态历史可追溯；
- 模拟结果带模型版本和假设。

---

# 第十三篇：分阶段实施路线（Codex G0–G12）

> **v5.2 说明**：本篇保留原 v5.0 的阶段性工程顺序，便于理解依赖，但从本版本开始它只属于“设计路线参考”，不再作为可直接复制给 Codex 的最终 Goal。Capability Fabric、Authority Microkernel、Distillation Fabric、Genesis/Ontology Commit 等新增内容需要在独立工程规划对话中进行 Gap Analysis 后重构 Goal、Acceptance 与 Milestone。


这条路线的原则是：**每个 Goal 都交付可运行、可测试、可回放的纵向闭环；不得用 TODO、Mock UI 或静态 JSON 冒充完成。** 真实文学、历史、家族和馆藏数据均设 Source Gate。

## 53. G0：Repository & Engineering Foundation

建立 monorepo、AGENTS.md、架构决策记录、Python/TypeScript 工具链、CI、测试、Docker、本地配置、日志、错误模型、Schema versioning。此阶段没有业务假实现。

## 54. G1：Authoritative World Kernel

Entity、Component、Relation、Event、Claim、Rule、WorldState、WorldDelta、Snapshot、Replay、Branch、Run、Commit Authority、deterministic fixtures 与基础 API。

## 55. G2：Living World Substrate

层级空间、门户、可见/可听、时间、日历、日程、物品/容器/所有权、身体状态、权限/制度、Background NPC、multi-rate scheduler。

## 56. G3：Agency, Cognition & Skills

Observation、Belief、Memory、Temporal Epistemic Graph、Actor/Organization、Skill–Action–Affordance、Action Validator、Resolver、Cognitive LOD、DeterministicPolicy 与可选 LLMPolicy。

## 57. G4：World Compiler, Packages & Evidence

Domain/World/Scenario/Character/Organization/Skill/Evidence/Asset/Rights/Experience 包协议，Source Registry、Compiler、Completion Ledger、Dependency/Schema Registry、import/export、审核工作流。

## 58. G5：Embodiment + Studio + 2D Vertical Slice

HumanPolicy、ShadowPolicy、EmbodimentLease、第一人称感知、接管/释放、React Studio、Phaser 2D Player、分支比较和调试视图。使用完全合成的小世界验收。

## 59. G6：Persistent World Host & Multiplayer Lifecycle

后台运行、暂停/加速/Event-driven、故障恢复、checkpoint、session、多客户端、command queue、rate limit、cost budget、world lifecycle；前端与世界权威彻底分离。

## 60. G7：Reality Bridge + Opportunity/Challenge + Capability

GPS/天气/传感器的模拟 Adapter、PhysicalObservation、Context Envelope、ChallengeSpec、Opportunity Detector、Safety Validator、Capability/LearnerState、LearningArtifact 和现实社区科学世界的合成演示。真实传感器连接作为 Adapter，不影响离线测试。

## 61. G8：Literature World Validation

先做“合成府邸生活世界”，再通过 Source Gate 接入《红楼梦》最小 World Pack；验证七日持续运行、角色接管、信件/物品、礼制/职责、消息传播、正典/补全/分支隔离。

## 62. G9：Family World

GEDCOM 7/GEDZIP Adapter、人物/家庭/事件/地点/来源/媒体、冲突 Claim、家族迁徙、Family Object Biography、Living Archive、数字人物三模式、隐私和身后权限。

## 63. G10：Heritage / Museum World

IIIF、CIDOC CRM/Linked Art Adapter、HeritageObject Pack、Physical Object / Digital Surrogate / Semantic Twin / Reconstruction 分层、3D asset semantic binding、Object Biography、展厅/历史背景/文保实验室实例。

## 64. G11：Co-Simulation & Strategy

SimulationAdapter、FMI-inspired scheduler、synthetic campaign、命令/情报/后勤/移动/战斗、战争迷雾、批量实验、ValidityEnvelope；之后才允许通过受审史料构建辽沈战役 World Pack。

## 65. G12：Hardening, SDK, Research Environment & Advanced Projection

30 日/1000+ Tick 稳定性、性能、权限、备份/迁移、Package SDK、Gymnasium/PettingZoo Adapter、Godot/Babylon 接口、Asset Foundry seam、数字人/AR/VR接口、私有部署、完整参考文档和最终验收报告。

---

# 第十四篇：关键研究问题

## 66. 世界补全与事实边界

资料天然不完整。解决方案不是禁止补全，而是让每次补全成为带 EvidenceClass、模型、规则、审核状态和可替换版本的一等对象。

## 67. 人格守恒与成长

角色采用 Identity Kernel + Life Arc + Mid-term State + Short-term Affect + Persona-conditioned Memory；重大变化必须由事件链支持并产生版本化 CharacterDelta。Persona Graph、动态人格一致性和匿名评测进入角色评测基线。

## 68. 长期记忆代谢与“谁知道什么”

解决 Social Memory Stacking 的关键不是扩大向量库，而是对事实记忆、个人解释、关系状态、遗忘、纠正和重解释分别建模，并确保 Role–Location–Plot 对齐。

## 69. 大世界成本与认知 LOD

采用 L0 Aggregate → L1 Population → L2 Rule NPC → L3 Light Agent → L4 Rich Agent → L5 Focal Character，多分辨率调度、稀疏激活和模型路由。只有焦点、高价值、非确定性决策进入强 LLM。

## 70. 多模型协同与因果

专业模型通过 Co-Simulation 接入。因果结论来自对同一快照做受控干预和重复运行，而不是让 LLM 对一次结果“讲原因”。每个 Finding 必须携带 Assumptions、metrics、seed set 和 ValidityEnvelope。

## 71. 现实观测不确定性

传感器、CV、GPS、人工报告都可能错误。PhysicalObservation 保留来源、时间、精度和置信度，通过 fusion/validation 后才能进入 Canonical State；不能让“识别到一棵树”变成不可质疑的事实。

## 72. 能力增长与人格变化的边界

Skill/Knowledge 可以快速学习；价值观、身份和长期人格变化速度不同。CapabilityDelta 与 PersonaDelta 分开，避免“学会一个技能”导致人物性格被重写。

## 73. 历史/文化真实性与沉浸体验

高保真画面不等于历史可信。所有重建需显示事实、来源记载、推断、体验补全、反事实和虚构等级；3D生成模型只生成可审资产候选，不制造正典。

## 74. 家庭多重记忆与数字人物伦理

家庭回忆冲突是正常数据，不自动裁决。数字人物分 Evidence / Reconstructed Persona / Creative Legacy，并执行 living-person consent、biometric、voice/image、posthumous、training/generation 权限。

## 75. 开放世界“自由”与系统约束

真正开放不等于动作无限。开放世界依赖稳定 Skill/Action/Affordance、规则、资源、空间和后果；自然语言入口只是把人类意图编译成结构化动作。

---

# 第十五篇：原始产品模块如何归位

| 原始模块 | v5 中的位置 |
|---|---|
| 析影 | World Compiler / Character Compiler |
| 定型、拾遗、捏角 | Character Package Authoring |
| 拓界 | Studio / World Definition / Asset Foundry |
| 剧团 | Character Package Registry |
| 布景库 | World / Asset Registry |
| 群戏 | Experience Projection + Agency Runtime |
| 推演 | Experiment Kernel / Strategy / Co-Simulation |
| 密语 | Text Projection / SillyTavern-compatible Experience |
| 代笔 | Narrative Projection / Exporter |
| 登台 | Embodiment / Co-Embodiment |
| 赋形 | Projection / Asset Foundry |
| 生平 | Character / Family / Learning Worldline Projection |
| 铸魂 | Training / Evaluation Export（受 Rights Envelope 约束） |
| 同台 | Multiplayer / World Host |
| 集市 | Package Marketplace（后期） |
| 记忆殿堂 | Temporal Epistemic Graph Debugger |

---

# 第十六篇：最终架构图与不可破坏原则

## 76. 最终逻辑架构：Root → Forge → Runtime → Worlds → Experiences

5 Planes / 16 Kernels 继续作为工程模块图，但万相更高层、长期更稳定的结构应表达为：

```text
┌──────────────────────────────────────────────────────────────┐
│                     WORLD ECOSYSTEM                          │
│ World Families · Multiverse · World Lineage DAG · Marketplace│
│ 红楼梦 / Family / Heritage / Campaign / Civilization / Reality│
├──────────────────────────────────────────────────────────────┤
│                       EXPERIENCES                            │
│ Studio · Player · Strategy · Heritage · Family · Learn · SDK │
│ Text · 2D · 3D · Digital Human · AR/VR · Reality Projection  │
├──────────────────────────────────────────────────────────────┤
│                    WANXIANG RUNTIME                          │
│ World Host · Time · Space · Actor · Organization · Sim      │
│ Capability Fabric · Agent Harness · Reality Bridge · Co-Sim  │
├──────────────────────────────────────────────────────────────┤
│                      WANXIANG FORGE                          │
│ Genesis · Distill · Compile · Emerge · Evolve · Promote     │
│ World Compiler · Ontology Distiller · World Lineage Manager  │
├──────────────────────────────────────────────────────────────┤
│                    WORLD CONSTITUTION                        │
│ Γ layers · Λ Evolution Policy · Domain Laws · Rights Policy  │
├══════════════════════════════════════════════════════════════┤
│                       REALITY ROOT                           │
│ Distinction · Relation · Transition · Commitment · History   │
│ World Semantic ISA · Commit Boundary · Ledger · Branch       │
└══════════════════════════════════════════════════════════════┘
```

`Wanxiang Kernel` 实现 Reality Root / Authority；`Wanxiang Runtime` 让世界长期活着；`Wanxiang Forge` 负责把资料/设定变成世界、让世界从历史中长出新结构并进行 Promotion；Experiences 负责人与世界的入口。Capability Fabric 横向贯穿 Runtime/Forge，但不能越过 Reality Root 的 Commit Boundary。

## 77. 不可破坏原则：五条宪法 + 十八条工程约束

### 77.1 五条最高宪法

1. **世界是被承诺的历史，不是生成文本。**
2. **承诺之前最大化创造，承诺之后最大化一致。**
3. **一切能力都可以演化，唯“什么叫成为现实”的语义不能被普通能力绕过。**
4. **世界可以无限分叉、繁衍和演化，但必须保持 Reality Root、Constitution、Genesis 与 World Lineage 可追溯。**
5. **万相与世界可以共演化，但世界只能以经验/候选的方式反哺平台，不能直接修改平台宪法或其他世界。**

### 77.2 十八条工程约束

1. 具体世界永远是 World Pack / World Instance，不进入 Core。
2. LLM、Agent、Director、Sensor、Simulation 只能产生 Observation、Claim、Intent、Candidate 或 ProposedDelta，不能直接拥有 Canonical Mutation Authority。
3. Canonical Reality 只能通过唯一 Commit Boundary 产生新的已承诺事实。
4. Committed History 不可静默改写；修正使用新 Event，分歧使用 Branch。
5. Child Branch 不能反向修改 Parent。
6. Identity、Event、Claim、Source、World/Instance/Branch 的引用语义必须稳定。
7. 角色只能读取经过 Perception、作用域和权限过滤的 Fact Space。
8. 客户端、2D、3D、数字人和生成视频只是 Projection。
9. 真实传感数据也是 Observation，不直接等于 Canonical Truth。
10. 专业机制由规则/领域模型/Co-Simulation 负责，不用自然语言替代物理和数量规律。
11. 来源、推断、重建、模拟、假设和虚构必须可区分、可回溯。
12. Runtime Effect 可以卸载；Committed World Effect 不能通过 plugin.dispose() 撤销。
13. Capability Fabric 可以热替换 Provider，但必须保持 Stable World ABI 和 Invariant。
14. 新 Skill/Rule/Institution/Ontology/Law 只能由候选→验证→相应 Commit 进入世界。
15. World Pack / World Definition 永远是版本化出生定义；运行历史只进入 Instance/Worldline，不能静默写回母本。
16. Worldline 只有经过 Distill → Validate → Promotion 才能晋升为 Derived World Definition。
17. Platform/Domain/Runtime 升级必须通过 Runtime Control Ledger 记录，并从升级时点影响未来，默认不得回算改写过去。
18. 先验证小而真实、可回放的世界，再追求大地图、写实数字人和大规模生成世界。

## 78. 最终定义

> **万相世界是一套以 Reality Root / World Reality Calculus 定义“什么叫成为现实”，以 Wanxiang Forge 把文学、历史、现实数据、个人记忆、文化遗产与原创设定蒸馏、创生和编译为世界，以 Living World Runtime 持续承载其 Committed History，并允许 Actor、关系、能力、组织、制度、文化、Ontology、Worldline 与 Derived World 在分层 Evolution Policy 下开放式多尺度共演化的 Semantic Persistent Open-Ended Co-Evolutionary World OS。**

从系统分类上，万相整体可概括为：

```text
World OS
+ World Compiler / Forge
+ World Hypervisor / Host
+ Multiverse & World Lineage Runtime
+ Evolution / Promotion System
```

它不是一个 Agent，也不是一个 Harness；Agent/Harness/World Model/Game Engine/Simulator 都是万相可以编排的能力。万相真正拥有的是世界身份、历史连续性、现实承诺、分支隔离、世界谱系与演化晋升语义。

最简工程分解：

```text
Wanxiang Kernel   —— 世界如何成为现实
Wanxiang Runtime  —— 世界如何长期活着
Wanxiang Forge    —— 世界如何被创造、蒸馏、进化并产生新世界
Experiences       —— 人如何进入、观察、控制和投射世界
```

万相不是制造某一个虚拟世界，而是提供“世界这种东西如何出生、存在、变化、分化、传承和产生后代世界”的运行基础设施。

---
# 第十七篇：Reality-Coupled World、科学学习与现实开放世界

## 79. Reality-Coupled World 的正式定义

除纯模拟世界外，万相支持现实耦合世界：现实持续产生 Observation，数字世界实例维护经验证的语义状态，AI/人类再基于该状态产生挑战、解释、记录和行动。

```text
Physical Reality
      ↕ observations/actions
Physical Reality Bridge
      ↕ validated context
Wanxiang World Instance
      ↕
Opportunity / Challenge / Actors
      ↕
Human Actions / Evidence / Artifacts
```

典型实例包括：社区科学世界、校园、自然教育基地、科技馆、博物馆户外扩展、城市记忆、Citizen Science、现场工程训练。

## 80. “小区科学馆”不是任务 App，而是现实开放世界

一个 Community Science World Pack 可把现实地点映射为语义实体：树木、池塘、道路、草地、建筑、公共设施、传感器节点、危险区域和允许活动区域。Experience Pack 决定用户以何种目标进入同一个世界。

同一社区可以安装：

- 7–12 岁科学探索 Experience；
- 社区历史 Experience；
- 家庭记忆 Experience；
- 公民科学 Experience；
- 建筑/生态导览 Experience。

**世界与体验分离。** 世界保存地点、对象和现实上下文；Experience 定义用户目标、UI、Challenge、反馈和评测。

## 81. PhysicalObservation 与现实可信度

```yaml
observation_id: obs_weather_001
source_type: weather_api
observed_at: 2026-08-11T16:20:00+08:00
subject: community_zone_A
measurements:
  temperature_c: 22.1
  humidity_pct: 87
confidence: 0.94
accuracy_note: provider_reported
provenance:
  connector: weather_adapter_v1
```

摄像头识别、用户报告、BLE、IoT、GPS 同样采用统一 Envelope。冲突 Observation 进入 Fusion/Review，不允许 last-write-wins 覆盖。

## 82. ChallengeSpec：事件必须可执行、可验证

```yaml
challenge_id: leaf_symmetry_001
learning_goals:
  - bilateral_symmetry
  - observation
  - composition
context_requirements:
  location_type: [park, courtyard]
required_affordances: [fallen_leaves]
weather_constraints:
  rain: false
  extreme_wind: false
materials:
  source: on_site
  living_plants_must_not_be_damaged: true
actions: [collect, classify, arrange, explain]
success_criteria:
  - recognizable_bilateral_structure
  - learner_explains_symmetry_axis
evidence_required: [final_photo, voice_explanation]
estimated_duration_minutes: 15
safety: [no_road_area, no_climbing, fallen_materials_only]
cleanup_required: true
```

Challenge 不只是生成的一段话；它有前置条件、可用材料、动作、成功标准、证据、安全规则、时长和清理义务。

## 83. Opportunity Detection：让现实每天产生不同事件

例如：

```text
地点：社区公园
刚下过雨
地面潮湿
风弱
附近有树、排水沟
Learner 最近做过 3 次绘画但未做水流实验
                         ↓
Opportunity Detector
                         ↓
“追踪三条雨水路径，预测雨更大时哪里先积水”
```

大风时则禁止容易倾倒的搭塔 Challenge，转成风向、声音、叶片阻力或安全结构实验。两名学生同时在场时，可把单人 Challenge 编译为协作任务。

## 84. Learning Artifact：成果是世界资产

```yaml
artifact_id: artifact_bridge_20260811
creator: learner_001
challenge: bridge_natural_materials_004
location: community_park
materials: [branches, stones, leaves]
evidence: [photo_v1, photo_v2, voice_reflection]
attempts:
  - v1_failed_center_sag
  - v2_stable
concepts: [load_distribution, balance, structure]
reflection: "第一次中央下沉，所以第二次增加了两侧支撑。"
collaborators: [learner_002]
```

Artifact、Attempt、Reflection、Evidence 和 CapabilityDelta 构成长程 `Learning Worldline`。这比“完成任务 +30 经验”更符合万相的证据与人生线架构。

## 85. 科学与创客 Adapter

可通过 Connector/Experience Adapter 对接：

- 手机实验与传感：phyphox；
- 环境开放传感：openSenseMap/senseBox；
- Web AR：AR.js / WebXR；
- 交互 STEM 仿真：PhET；
- 机器人与图形化编程：Open Roberta；
- 学习活动记录：xAPI/LRS；
- 可验证技能凭证：Open Badges；
- 未来的真实机器人、ESP32、micro:bit、ROS2 等。

这些系统提供专门能力，万相只负责统一 World Entity、Context、Challenge、Evidence、Capability 和 Rights。

## 86. 学习隐私、安全与未成年人治理

Reality-Coupled Learning 必须默认最小化采集：精确位置、照片、声音、生物特征和同伴数据按高敏感等级处理；对未成年人设置监护授权、保留期、用途、导出/删除、训练许可、公开范围。安全规则必须在 LLM 之前和之后双重校验，危险环境/材料/攀爬/道路/水体等进入硬约束。

---

# 第十八篇：开放世界、游戏引擎、世界模型与生态边界

## 87. 万相与传统游戏引擎

Godot、Babylon.js、O3DE、OpenMW、RobustToolbox 等解决渲染、物理、场景、网络或具体游戏内容的问题；万相不重造这些能力，而提供更上层的 Semantic World Authority。

```text
Wanxiang Semantic World
        ↓ Projection / Command API
Game / Rendering Engine
        ↓
pixels, animation, physics, input
```

推荐首阶段：React + Phaser 验证 2D；后续 Godot 作为原生 2D/3D 客户端，Babylon.js 作为 Web 3D/WebXR 客户端。O3DE 只在高保真仿真/机器人场景确有需要时接入。

## 88. 从 OpenMW、Space Station 14、Luanti 学什么

重点不是复制代码，而是吸收：

- **Engine 与 Content 分离**；
- 世界/游戏/Mod 通过数据与包安装；
- 深系统交互比纯剧情脚本更能产生涌现；
- 服务器权威和持久对象必须独立于 UI；
- 许可证与资产许可证必须单独评估。

这直接对应万相的 Core / Domain Pack / World Pack / Experience Pack 分层。

## 89. 与 OpenStory、Agent-Kernel、Concordia 的关系

OpenStory/Agent-Kernel 已经证明多 Agent 的感知、计划、执行、反思、动态增删、地图前端和故事推演可以工程化；Concordia 使用 Agent 提出意图、Game Master/Engine 观察、调度和解析结果。万相把它们视为 **Agent Runtime Reference / Adapter Candidate**，而不是重写所有 Agent 基础设施。

万相自己的边界是：Canonical State、物质世界、认知隔离、证据、跨世界包、Co-Simulation、长期 World Host、现实桥和可审计 Commit。

## 90. 与 SillyTavern/酒馆的最终关系

SillyTavern 强项是 Character Card、Persona、World Info/Lorebook、RAG 和 Chat/Group Chat 的交互编排。万相不靠“更长角色卡”竞争，而将其定位为可选 Text Projection Client：

```text
Wanxiang Character/World State
→ Perception Envelope
→ SillyTavern Adapter
→ Prompt / Chat UI
```

酒馆的 Character Card 可导入为 CharacterPackage Candidate；Lorebook 可导入为 Knowledge/Claim Candidate；经过编译和验证后才成为 World Pack 的部分。

## 91. 四种 World Model 必须区分

```text
Canonical Semantic World Model   世界实际上是什么
Mechanistic World Model          世界如何变化
Cognitive World Model            每个主体认为世界是什么
Perceptual/Generative World Model 世界看起来/听起来是什么
```

生成式视频世界模型和 3D 世界生成模型可以极大降低显化和资产成本，但不能自动承担权威状态、所有权、知识边界和因果记录。

## 92. 3D 世界生成进入 Asset Foundry，而不是 Core

例如 HY-World 2.0 一类模型可将文本/图片/视频生成或重建成 mesh/3DGS，适合成为 `World Asset Foundry Adapter`：

```text
World Compiler semantic scene
→ 3D generation / reconstruction
→ candidate mesh / 3DGS
→ semantic binding + collision/navigation validation
→ rights/human review
→ Asset Pack
```

AlayaWorld 等视频 world model 可做沉浸预览、cinematic projection、dream/remote scene 等视觉投影。其生成画面不直接修改 Canonical World。

## 93. World Environment API 与 AI 研究

正式环境接口：

```text
create_world(package)
reset(snapshot=None)
observe(actor_id)
legal_actions(actor_id)
step(action_bundle)
advance(time)
checkpoint()
restore()
branch()
metrics()
close()
```

实现 Gymnasium Adapter（单 Agent）与 PettingZoo AEC/Parallel Adapter（多 Agent），使万相既是产品平台，也能成为 Agent 长程规划、社交、记忆、角色一致性和群体协作的可重复 Benchmark 环境。

---

# 第十九篇：研究证据如何转化为万相设计约束

## 94. BookWorld：小说不是角色卡集合

BookWorld 表明从小说构建多 Agent 社会时，需要动态人物、世界观和地理约束。万相进一步把这些对象落到 World Pack、Canonical State 和 World Compiler，而非停留在生成故事层。

## 95. EvolvingWorld：角色和世界必须共同演化

角色变化不能只有 Memory 更新；世界位置、关系、资源和场景也要形成持久 Delta。因此万相同时保存 CharacterDelta 与 WorldDelta，并把 trajectory-level evaluation 纳入长期评测。

## 96. EvoSpark：长期世界必须解决记忆堆积和空间叙事脱节

直接对应万相的 Memory Metabolism、关系冲突消解、Cognitive LOD、Role–Location–Plot alignment 和场景激活器。

## 97. Narrative World Model：普通 RAG 不足以回答“谁何时知道什么”

万相采用 Temporal Epistemic Graph / Narrative Temporal Graph，并保留事件发生时间、揭示时间、角色观察时间、关系阶段和信息传播路径。

## 98. ThinkPersona、Memory-Driven RP、RoleMemo、PersonaForge

共同提示：Persona 需要人生轨迹/价值/关系/事件结构；记忆要检索、边界化、角色化解释；事实记忆和 persona insight 分离；长期人格要主动检测漂移。万相把这些落实为 Persona Graph、Identity Kernel、Life Arc、Dual Memory、RoleFidelityReport 与匿名决策测试。

## 99. Orchestrated Reality：自由文本不能拥有世界状态

其 canonical JSON state、参数化动作和 Plan–Diff–Validate–Apply 思路与万相“Intent → Structured Action → Validate → Resolve → Commit”高度一致。万相进一步把规则、专业模拟器、Evidence、Rights 与多人 World Host 纳入同一 Commit Authority。

## 100. 教育研究与 Reality-Coupled Learning

OpenMAIC 表明多 Agent 课堂正在加入 3D、仿真、游戏、项目式学习；AgentSchool 等研究把学习者知识、误区和过程建模成显式状态转移。万相不复制 AI 课堂，而把 Context、Challenge、Capability、Artifact 和现实世界状态做成通用世界机制。

---

# 第二十篇：Distillation Fabric、Meaning Engine 与世界自我生长

## 101. 蒸馏的正式定义

万相中的 Distillation 与模型参数蒸馏不是同一概念。这里的定义是：

> **从资料、感知或长期运行历史中，发现足够稳定、可复用、可证据支持的 Identity、Relation、Event、Rule、Skill、Persona、Institution、Concept 或 Ontology 候选结构。**

蒸馏负责“发现”，Commit 负责“承认”。

```text
Raw Source / World History / Physical Observation
        ↓
Parse / Observe
        ↓
Extraction
        ↓
Distillation
        ↓
Candidate Structure
        ↓
Evidence / Stability / Consistency / Safety Validation
        ↓
Commit or Reject
```

## 102. 两个方向的蒸馏

### 102.1 Foundational Distillation：Source → World

用于：小说、剧本、史书、县志、战史、电报、家谱、照片、口述史、博物馆记录、3D 扫描、现实数据。

输出可用于构建 World Pack / Character Pack / Skill Pack / Evidence Pack。

### 102.2 Evolutionary Distillation：World History → New Structure

世界运行后，从数千/数百万 Event 中提炼：

- 长期人物关系；
- 习惯与偏好；
- 新 Skill；
- 人物阶段；
- 稳定组织模式；
- 新制度候选；
- 新概念/本体候选；
- 高阶宏观状态。

Evolutionary Distillation 不允许把“模型总结”直接写回现实。它只能提交 Candidate，随后进入 Capability/Ontology/Law Commit 的验证流程。

## 103. Character Distillation：从角色卡升级为人物世界模型

角色蒸馏至少输出：

```text
Identity
Life Trajectory / Character Arc
Persistent Dispositions
Current State
Values / Goals
Relations
Beliefs / Interpretations
Knowledge Boundary
Memories
Capabilities / Skills
Action Tendencies
Language / Performance
Evidence / Counter-evidence
Uncertainty / Canon Distance
```

人物不应只是一张静态 `personality` 卡，而是随 Observation 与 Event 演化的轨迹。原著人物、历史人物、现实人物必须采用不同的证据和自由度策略。

## 104. Canonical Distillation 与 Interpretive Distillation

同一来源必须至少拆成两层：

- **Canonical / Explicit**：原文、档案、观测明确支持什么；
- **Interpretive**：这些材料可能意味着什么。

Interpretive 结果必须保留推断链、置信度和可替代解释，不能静默升级为 Canon。

## 105. Relation / Rule / Skill / Institution Distillation

关系不是单一好感度；规则不是一次出现的行为；Skill 不是一句自然语言总结；Institution 不是 LLM 命名即可成立。

例如从大量历史中发现一个 Skill：

```text
repeated behaviour episodes
→ pattern clustering
→ skill candidate
→ precondition / steps / failure / cost / observability
→ validation
→ Capability Commit
```

制度候选需要更高门槛：持续时间、参与者认可、行为影响、反事实稳定性、领域证据和必要的人工审核。

## 106. 红楼梦 Distillation Profile

```text
SourceParser
CharacterDistiller
DialogueDistiller
RelationDistiller
EventDistiller
LocationDistiller
SocialRuleDistiller
KnowledgeBoundaryDistiller
CharacterArcDistiller
CanonVerifier
CompletionCandidateGenerator
```

最终输出的是 `RedChamber World Pack Candidate`，而不是直接运行世界。

## 107. Family Distillation Profile

```text
GEDCOMAdapter
OCR / Document Parser
PersonResolver
KinshipDistiller
LifeEventDistiller
PlaceResolver
FamilyObjectDistiller
OralHistoryClaimDistiller
EvidenceBinder
PrivacyClassifier
```

冲突 Claim 必须并存，Resolution 只是当前采用视图，不得删除来源差异。

## 108. Heritage Distillation Profile

```text
CollectionMetadataAdapter
IIIFAdapter
ObjectResolver
MaterialDistiller
ObjectBiographyDistiller
ProvenanceDistiller
ConservationDistiller
ScholarshipClaimDistiller
ReconstructionClassifier
```

Digital Surrogate、Physical Object、Semantic Twin、Reconstruction 必须保持不同身份和事实作用域。

## 109. Campaign Distillation Profile

输入：战史、命令、电报、地图、部队序列、回忆录、研究论文和统计资料。

输出：人物、组织、单位、地点、交通、命令时间、接收时间、情报、补给、资源、战斗 Event、争议 Claim、不同来源及 Validity Envelope 所需参数。

## 110. Ontology Distillation 与 Emergent Ontology Engine

对于真正的新生/自演化世界，Distillation Fabric 可从低层历史中提出 `OntologyCandidate`。候选需回答：

- 该模式是否具有持续身份？
- 是否能用较低维结构稳定解释/预测大量底层事实？
- 是否跨多个时间窗口重复出现？
- 是否只是观察分辨率造成的幻象？
- 引入新类型是否减少描述复杂度并保持可追溯性？
- 领域专家/规则是否认可？

通过后才可 `OntologyCommit`。

## 111. 世界自我蒸馏

万相的长期目标之一可以是：

> **世界从自己的历史中蒸馏自己的下一层结构。**

形式上：

```text
H_t
→ Distillation / Pattern Discovery
→ StructureCandidate
→ Meta Validation under Λ
→ OntologyCommit / LawCommit / CapabilityCommit
→ Σ_{t+1} / Γ_{t+1}
```

这提供“世界生长”的路径，但必须保持人类可审计、可冻结、可回滚运行时配置，以及不改写既有 Committed History 的原则。

---

# 第二十一篇：可组合运行时、DeepSeek Harness / Cordis 与万相的边界

## 112. 为什么这一类 Harness 值得吸收

随着万相同时拥有 Agent、Domain、Simulation、Projection、Sensor、Storage、Digital Human、Reality Bridge 等能力，如果继续以静态 import、全局单例和手工启动顺序扩展，最终会形成巨大耦合系统。可组合运行时提供了另一条路线：能力通过稳定 Service Contract 接入，显式声明依赖和作用域，运行时副作用能够成对安装/释放，Provider 可动态替换。

## 113. DeepSeek Harness 的定位

截至 2026-08-14，官方 `deepseek-ai/deepseek-harness` 是 DeepSeek AI 开源的 Agent Harness，README 明确采用 “Everything is a Plugin”，由 Cordis 提供插件运行时；官方同时明确其仍为 Developer Preview，未来会出现破坏兼容性的变化。

万相的判断：

- **不把万相建立成 DSH fork**；
- **不让 Agent Harness 拥有 Canonical World State**；
- **把 DSH 作为 AgentHarnessProvider 一等候选**；
- **吸收 Cordis 的可组合原则到 Wanxiang Capability Fabric**；
- **保持 Stable World ABI，使未来替换 Cordis/DSH 不影响世界历史。**

## 114. Cordis 的关键启发

Cordis 文档/论文强调两种组合性：

- **Temporal composability**：组件被卸载时，其运行时注册和副作用能够撤销；
- **Spatial composability**：组件声明所需能力，并随上下文/依赖变化被运行时组合。

万相吸收为：

```text
Capability Service
Provider / Consumer
Context / Scope
Declarative Dependency
Typed Runtime Events
Reversible Runtime Effects
Transactional Reload
Profile / Bundle / Patch
```

但“世界语义历史”不是 reversible runtime effect。

## 115. Runtime Profile 与 World Pack 必须分开

- `World Pack`：世界是什么；
- `Runtime Profile`：运行这个世界需要哪些能力。

例如红楼梦 World Pack 只保存人物、地点、物品、正典、关系、证据等；`RedChamberRuntimeProfile` 才声明 Narrative、Household、HistoricalChina、Cognition、AgentHarness、Projection 等 Provider。

## 116. Stable World ABI

Capability Fabric 与 Authority Microkernel 之间必须有极窄 ABI：

```text
ReadOnlyWorldSnapshot
PerceptionEnvelope
Action/Intent Proposal
SimulationRequest
ProposedDelta
ValidationResult
CommittedEventRef
CapabilityHealth
```

任何 Provider 不能拿到绕过 Commit Boundary 的 ORM/数据库写权限。

## 117. Runtime Evolution Lab

允许开发者/AI 提出新能力，但只能在受控实验室中演化：Sandbox → Shadow Branch → Invariant / Regression / Security / Cost / Determinism Test → Approval → Transactional Activate。

这是一种“Bounded Runtime Evolution”，不是让 Agent 自己重写 World Constitution。

## 118. 三重可观测性

系统调试必须能够同时回答：

1. **World**：世界到底发生了什么？
2. **Actor**：主体为什么做出这个决定？
3. **Runtime**：当时到底安装了哪些能力和模型？

因此三重 Ledger 必须互相引用，但不混成一个无边事件表。

## 119. 与 SillyTavern / OpenStory / Godot 的最终关系

```text
Wanxiang Authority / Reality
        ↑↓ Stable ABI
Capability Fabric
        ├── DSH / Native / OpenStory Agent Harness
        ├── Domain / Simulation Providers
        ├── Godot / Babylon / Phaser Projection
        ├── SillyTavern Text Client Adapter
        └── Sensor / Heritage / Family / Reality Adapters
```

万相负责“什么是真的”；Harness 负责“Actor 如何思考”；游戏引擎负责“如何计算/渲染身体和空间”；酒馆类客户端负责“如何以文本和角色交互”。

## 120. 本轮架构结论

v5.2 不推翻 5 Planes / 16 Kernels，而是在其上下明确两个更稳定的边界：

```text
Meaning / Experience / Agency / Simulation capabilities
                  ↓
          Capability Fabric
                  ↓
          World Reality Bus
                  ↓
        Authority Microkernel
                  ↓
       Committed World Ledger
```

上层能力可以快速变化；底层现实承诺语义保持稳定。

---

# 第二十二篇：World Evolution Stack、多元宇宙与世界谱系

## 121. “万相进化”与“万相创造的世界进化”不是同一种进化

万相存在多个不同写权限和验证强度的 Evolution Layer。必须区分：

- **E0 — Reality Root / Constitution Semantics**：Commit、Branch、Identity 等协议级语义；自主程度极低，只能通过人工治理、形式验证、迁移与兼容机制升级；不得直接重写既有世界历史。
- **E1 — Wanxiang Platform**：Runtime、Compiler、Memory、Harness、Evaluation 等平台能力；可受控自动化演进，但不能追溯性改写既有 Committed History。
- **E2 — Domain / Capability**：Family、Campaign、Social 等领域能力；版本化升级，只能从某个世界明确采用新版本的时点开始影响未来。
- **E3 — World Definition / Pack**：新资料、新考据、新 Genesis 版本；通过新版本发布，旧版本和由旧版本出生的世界继续保留。
- **E4 — World Instance / Worldline**：状态、历史、人物命运、制度与环境；允许高度自主演化，但只影响自身 Worldline。
- **E5 — In-world Structures**：人物、Skill、组织、规范、文化、Ontology；允许在 `Λworld` 约束下演化，只能通过合法 Commit。
- **E6 — Cross-world Knowledge**：从大量世界中发现可复用模式；只能产生候选，不直接修改任何世界或平台。

因此“万相与世界一起进化”的准确说法是 **Wanxiang ↔ Worlds Co-Evolution**：世界给万相提供经验和评测数据；万相只能通过跨世界蒸馏、候选、Sandbox、Benchmark、Approval 与版本发布吸收这些经验。

## 122. World Instance 的五级进化

一个活世界内部至少存在五级变化：

### E4.1 State Evolution

位置、资源、身体、物品、天气、秘密、任务、即时情绪等普通 Fact 变化，主要通过 `StateCommit` 发生。

### E4.2 Actor Evolution

人物不是冻结角色卡。长期经历可以通过：

```text
Event → Immediate State → Repeated Pattern → Distillation
→ CharacterChangeCandidate → Consistency Validation → Commit
```

改变 Belief、Goal、Habit、Skill、Relation、Life Arc 与有限范围的长期倾向。**人格守恒不是人格冻结；变化必须能从其历史解释。**

### E4.3 Social / Institutional Evolution

微观互动可以积累为群体模式，再形成规范和制度：

```text
individual behavior
→ habit
→ repeated group pattern
→ norm
→ institution
```

例如一个新诗社、商会、宗教组织、军政机构或社区规则，应该由稳定历史模式和合法社会过程生长出来，而不是 LLM 一句话直接创造。

### E4.4 Capability / Cultural Evolution

主体可以通过实践、失败、成功和协作真正获得新 Skill；群体可以逐渐形成语言习惯、审美、传统、节庆、禁忌和知识体系。Skill/Norm/Culture 进入持久结构前必须经过长期证据与 Distillation。

### E4.5 Ontology / Law Evolution

当稳定模式形成新的世界级存在类别或可执行制度时，可以修改 `Σ` 或 `Γ`：

```text
History
→ Pattern Detection
→ StructureCandidate
→ Stability / Evidence / Counterfactual Evaluation
→ OntologyCommit / LawCommit
→ Σ_{t+1} / Γ_{t+1}
```

物理/宪法层默认极难或不可由普通世界主体改变；社会、组织、制度和 Scenario 规则可以有更高可变性。

## 123. Evolution Policy Stack：Λ 必须分层

单个 `Λ` 在工程上应展开为 Evolution Policy Stack：

```text
WorldEvolutionPolicy
├── ActorEvolutionPolicy
├── CapabilityEvolutionPolicy
├── SocialEvolutionPolicy
├── InstitutionEvolutionPolicy
├── OntologyEvolutionPolicy
├── LawEvolutionPolicy
└── PromotionPolicy

PlatformEvolutionPolicy
├── Model/ProviderPolicy
├── PluginPolicy
├── DomainPromotionPolicy
├── RuntimeUpgradePolicy
└── ConstitutionMigrationPolicy
```

World Policy 与 Platform Policy 必须严格隔离。一个世界可以在自己的 `Λworld` 内高度开放，但永远不能自行获得修改 `Λplatform` 或 Reality Root 的权限。

## 124. 《红楼梦》只是一个实例：Living Red Chamber 如何进化

`dream_of_the_red_chamber` World Pack 只定义 Genesis/Canon/人物/空间/制度/来源和默认 Evolution Policy。实例化后：

```text
RedChamber World Definition
        ↓ Scenario
World Instance RC-001
        ↓
Worldline A / B / C ...
```

不同玩家选择、AI 行为、环境、失败/成功和随机过程造成不同 H。数日后是不同关系与认知；数月后可能产生新习惯和人物阶段；数年后可以形成新组织、制度、家庭与后代；数十年后某条 Worldline 可以与原著高度不同，但仍完整追溯到同一 Genesis。

原著本身不被修改。`Canonical Replay`、`Soft Canon`、`Living/Open` 应使用不同 Evolution Policy：前者限制大尺度偏离，后者允许真正开放演化。

## 125. World Promotion：什么时候一个分支不再只是“存档”

Branch/Worldline 默认只是同一实例的替代历史。只有当它形成稳定、独立、可再实例化的新世界结构时，才有资格 Promotion：

```text
Worldline
→ Long-horizon Distillation
→ Stable World Structure
→ Source/Rights/Invariant Review
→ Freeze Genesis Snapshot
→ Compile World Pack Candidate
→ Promotion Approval
→ Derived World Definition
```

Promotion 后产生新的 World Definition ID，并记录完整派生关系；Parent Definition 与原 Worldline 保持不变。

## 126. World Genealogy：世界也有家谱

世界谱系必须是一等数据结构。一个 Derived World 至少知道：

- 父世界/祖世界；
- 从哪个 Snapshot/Event/Worldline 派生；
- 继承哪些历史；
- 哪些 Ontology/Rule 被增加、删除或改写；
- 使用何种 Constitution / Domain / Runtime / Evolution Policy 版本；
- 产生了哪些子世界。

这允许 Studio 提供“万界树/世界谱系图”，也允许科研场景比较两个世界的共同祖先和差异路径。

## 127. Multiverse Runtime：从世界树到世界谱系 DAG

最初可把世界关系实现为树：一个世界线从一个 Parent Fork。长期应允许受控多父派生：

```text
World A ──┐
          ├─ Hybrid Genesis → World C
World B ──┘
```

但 World Merge 不能复制 Git 文本合并。必须显式执行：

```text
Compatibility Analysis
→ Constitution Compatibility
→ Identity Resolution
→ Ontology Mapping
→ History Inheritance Policy
→ Rights / Provenance Resolution
→ Law Conflict Resolution
→ Genesis Compilation
→ New World
```

当多个来源世界不可兼容时，系统应拒绝 Merge 或要求用户选择“翻译/门户/投影”而不是强行合并现实。

## 128. Interworld Identity 与跨世界旅行

跨世界移动必须保持 Origin Identity：

```text
ActorIdentity: A:character_001
origin_world = World A
presence_world = World B
```

在 B 的经历默认只进入 B 的 Worldline，不自动写回 A；返回、同步或人格合并必须由显式 Interworld Policy 决定。这样才能避免跨世界角色复制导致身份、记忆和历史污染。

## 129. Cross-world Distillation：世界怎样反过来让万相成长

世界经验可通过跨世界蒸馏形成上层知识，但只能作为候选：

```text
Many World Histories
→ anonymized/authorized telemetry + evaluation
→ Cross-world Pattern Discovery
→ Domain/Capability Candidate
→ Research Sandbox
→ Benchmark / Ablation / Invariant / Security Test
→ Human/Policy Approval
→ New Domain or Runtime Version
```

因此世界是“经验来源”，不是“平台管理员”。这一原则同时保护系统稳定性、隐私、版权和不同世界的自治。

## 130. Evolution Promotion Pipeline 与 Abstraction Ladder

万相应建立统一的抽象晋升阶梯：

```text
L0 Event
↓
L1 Repeated State Pattern
↓
L2 Individual Habit / Skill / Capability
↓
L3 Group Pattern / Social Norm
↓
L4 Institution / Organization Rule
↓
L5 World Structure / Ontology
↓
L6 Cross-world Pattern
↓
L7 Reusable Domain Capability
↓
L8 Wanxiang Runtime / Compiler Improvement
```

每升一级，证据数量、稳定性、跨场景验证、权限和人工治理要求都必须提高。自动化最强的区域应在 L0-L3；越接近 L7-L8 和 Constitution，越需要严格验证和显式批准。

## 131. Wanxiang 不是 Agent 或 Harness：系统身份最终收敛

万相整体的技术身份：

> **Semantic Persistent Open-Ended Co-Evolutionary World OS**

它同时具备四种系统角色：

```text
World OS          —— 管理世界现实、身份、历史、时间、分支和权限
World Compiler    —— 把 Source / Genesis / Domain 编译为可运行 World Pack
World Hypervisor  —— 隔离并承载多个 World Instance / Worldline / Runtime Profile
Evolution System  —— 让世界生长、蒸馏、涌现、晋升并形成世界谱系
```

DeepSeek Harness、OpenStory、Agent、World Model、Godot、Simulator 都位于 Capability/Runtime/Projection 层；它们可以被替换，而 World Reality / Lineage 语义必须持续稳定。

## 132. Kernel / Runtime / Forge：工程总分解

未来工程和文档应优先使用下面三大核心，而不是把每个新概念都提升成平行“大系统”：

### Wanxiang Kernel

负责“世界如何成为现实”：Reality Root、World Semantic ISA、Identity、Fact、Event、Constraint、Commit、Ledger、Branch、Lineage Identity、Invariant。

### Wanxiang Runtime

负责“世界如何长期活着”：World Host、Clock、Space、Body、Objects、Actor、Organization、Perception/Belief/Memory、Simulation、Capability Fabric、Reality Bridge、Multiplayer、Co-Simulation。

### Wanxiang Forge

负责“世界如何被创造和继续长出来”：Source/Evidence、Distillation、Genesis、World Compiler、Completion、Emergence Detection、Ontology/Rule/Skill/Institution Distillation、Evolution、Promotion、World Lineage Compilation。

Experiences / Studio / Player / Strategy / Heritage / Family / Learn 都建立在这三者之上。

## 133. 最终的世界生命周期

一个世界不再只拥有“创建→运行→保存”三步，而是完整生命周期：

```text
Genesis
→ Instantiate
→ Live
→ Experience
→ Propose
→ Commit
→ History
→ Distill
→ Adapt
→ Emerge
→ Evolve
→ Branch
→ Inherit
→ Promote
→ Derived World
→ Recreate / Continue Living
```

万相自己则运行另一个更慢、更严格的生命周期：

```text
Worlds
→ Observe/Evaluate
→ Cross-world Distill
→ Capability Candidate
→ Sandbox/Benchmark/Review
→ Versioned Upgrade
→ Better Future Worlds
```

这两条循环形成共演化，但不会混成一个“AI 随意自修改”的黑箱。

## 134. 本轮收敛结论

本轮设计将“多元宇宙”从叙事概念变成系统结构：**万相不是世界树中的某个世界，而是实现 Reality Root、World Constitution、Forge、Runtime、Lineage 与 Promotion 的 World OS。**

世界可以无限向上分叉、分化、繁衍、混合和产生后代世界；世界内部的人物、组织、制度与文化也可以在不同时间尺度上演化；大量世界又能以受控方式帮助下一代 Domain/Runtime 进步。但所有这些复杂性最终必须回落到同一个最小基岩：

> **可区分的存在，通过受约束、可追溯的变化，被正式承诺成历史。**

这就是万相所有“万界”之下共同的 Reality Root。

---

# 附录 A：Family Person 示例

```yaml
person_id: p_001
names:
  - value: 张某
    source: source_birth_record
life_status: deceased
birth:
  claims:
    - value: 1932-05
      evidence: [birth_record_01]
      confidence: high
relationships:
  - type: parent_child
    target: p_002
    valid_time: 1958-2020
    evidence: [family_register_03]
privacy:
  default: family_only
legacy:
  allow_persona_reconstruction: true
  allow_voice_clone: false
```

# 附录 B：Heritage Object 示例

```yaml
object_id: h_001
object_type: ritual_bronze
physical_record:
  museum_id: M-2020-18
  current_location: storage_room_3
materials:
  - bronze
captures:
  - type: photogrammetry
    asset: scans/h001/high.glb
    capture_date: 2026-06-01
claims:
  - predicate: production_date
    value: late_bronze_age
    evidence: [catalog_01, paper_22]
reconstructions:
  - id: recon_a
    confidence: medium
    label: hypothesis
rights:
  public_view: true
  generation: limited
```

# 附录 C：参考资料、标准、开源项目与研究论文（工程导向目录）

> 本目录用于 Codex/工程设计查阅。收录并不意味着建议直接复制代码；必须单独检查许可证、数据/资产许可、商用条款和版本。访问日期：2026-08-14。

## C.1 角色、多 Agent 与叙事世界

1. **OpenStory / 万象谱** — 多智能体互动故事世界，《红楼梦》《西部世界》示例，Agent-Kernel、Tick、地图和分支。  
   https://github.com/ZJU-LLMs/OpenStory
2. **Agent-Kernel** — 动态 Agent、Controller、行为验证、插件化微内核、Standalone/Distributed。  
   https://github.com/ZJU-LLMs/Agent-Kernel
3. **Google DeepMind Concordia** — Entity/Component/Engine/Game Master 的生成式社会模拟。  
   https://github.com/google-deepmind/concordia
4. **SillyTavern Documentation** — Character Cards、World Info、Group Chats、Data Bank/RAG；用于 Text Projection/兼容研究。  
   https://docs.sillytavern.app/
5. **BOOKWORLD (ACL 2025)** — 从小说到互动 Agent Society。  
   https://aclanthology.org/2025.acl-long.773/
6. **EvoSpark (ACL 2026)** — 长程叙事中的 social memory stacking 与 narrative-spatial dissonance。  
   https://aclanthology.org/2026.acl-long.1480/
7. **EvolvingWorld (2026)** — Character/World co-evolution、open schema、trajectory evaluation。  
   https://arxiv.org/abs/2607.17250
8. **Narrative World Model (2026)** — narratology-grounded typed temporal-state graph。  
   https://arxiv.org/abs/2607.05577
9. **ThinkPersona (ACL 2026)** — Persona Graph：人生轨迹、价值、关系与事件。  
   https://aclanthology.org/2026.acl-long.449/
10. **Memory-Driven Role-Playing (ACL Findings 2026)** — Anchoring/Selecting/Bounding/Enacting 与 MRBench。  
    https://aclanthology.org/2026.findings-acl.1175/
11. **RoleMemo / DualMem (2026)** — factual cognition 与 persona-conditioned insight 分离。  
    https://arxiv.org/abs/2605.25693
12. **PersonaForge (ACL Findings 2026)** — 长对话人格一致性、选择性双过程。  
    https://aclanthology.org/2026.findings-acl.386/
13. **Dynamic Persona Coherence (ACL 2026)** — 静态 persona 之外的动态一致性。  
    https://aclanthology.org/2026.acl-long.1336/
14. **Orchestrated Reality (2026)** — canonical JSON state、parameterized action、Plan-Diff-Validate-Apply。  
    https://arxiv.org/abs/2606.16014

## C.2 开放世界、游戏引擎与持久世界

15. **Godot Engine** — MIT，跨平台 2D/3D；推荐原生客户端候选。  
    https://godotengine.org/  
    https://docs.godotengine.org/en/stable/about/introduction.html
16. **Babylon.js** — WebGL/WebGPU、WebXR、3D Tiles、Large World Rendering；Web 3D 候选。  
    https://www.babylonjs.com/  
    https://www.babylonjs.com/specifications/
17. **Open 3D Engine (O3DE)** — 开源 3D 游戏/仿真引擎，ROS 2/机器人仿真；高保真仿真候选。  
    https://www.o3de.org/  
    https://docs.o3de.org/docs/user-guide/interactivity/robotics/
18. **OpenMW** — 开源开放世界 RPG 引擎与 Content Editor；重点研究 Engine/Content 分离。  
    https://github.com/OpenMW/openmw
19. **Space Station 14 / RobustToolbox** — multiplayer engine + content pack 深系统交互范例。  
    https://github.com/space-wizards/space-station-14  
    https://github.com/space-wizards/RobustToolbox
20. **Luanti** — voxel game-creation platform、games/mods/content。  
    https://github.com/luanti-org/luanti
21. **Evennia** — Python 持久文字虚拟世界/MUD 框架；World Host/持久对象参考。  
    https://www.evennia.com/  
    https://github.com/evennia/evennia
22. **OpenRA** — RTS engine/mod/rules/maps；战略世界与 Mod 结构参考。  
    https://www.openra.net/  
    https://github.com/OpenRA/OpenRA

## C.3 世界模型、3D 生成与显化

23. **HY-World 2.0** — 文本/图片/视频到可导航 3DGS/mesh 世界；用于 Asset Foundry 研究。  
    https://github.com/Tencent-Hunyuan/HY-World-2.0  
    https://arxiv.org/abs/2604.14268
24. **AlayaWorld** — 长程、可交互视频世界模型；适合作为生成式 Projection 研究，不作为 Canonical State。  
    https://github.com/AlayaLab/AlayaWorld  
    https://arxiv.org/abs/2607.18367
25. **glTF 2.0** — Khronos 运行时 3D 资产交换。  
    https://registry.khronos.org/glTF/
26. **OpenUSD** — 复杂场景组合、layering、非破坏式制作管线。  
    https://openusd.org/
27. **OGC 3D Tiles 1.1** — 大规模地理 3D 内容流式加载。  
    https://www.ogc.org/standards/3DTiles/
28. **CityGML 3.0** — 语义 3D 城市模型与数字孪生互操作。  
    https://www.ogc.org/standards/citygml/
29. **OpenHistoricalMap** — 开放历史地理数据，可作为历史空间连接器之一。  
    https://www.openhistoricalmap.org/

## C.4 协同仿真与 Agent 环境

30. **FMI 3.0.2** — Model Exchange / Co-Simulation / Scheduled Execution；万相 Co-Simulation Fabric 的重要设计参考。  
    https://fmi-standard.org/docs/3.0.2/
31. **Gymnasium** — 单 Agent RL Environment API。  
    https://github.com/Farama-Foundation/Gymnasium
32. **PettingZoo** — 多 Agent AEC/Parallel Environment API。  
    https://pettingzoo.farama.org/

## C.5 家谱与个人/家庭世界

33. **FamilySearch GEDCOM 7.0.18** — 人物、家庭、事件、来源/引用、研究/权利元数据和 GEDZIP。  
    https://gedcom.io/specifications/FamilySearchGEDCOMv7.html
34. **GEDCOM Specifications Portal**  
    https://gedcom.io/specs/
35. **Gramps / Gramps Web** — 谱系协作、事件、地点、来源、媒体和权限生态。  
    https://www.gramps-project.org/  
    https://www.grampsweb.org/

## C.6 博物馆、文物与文化遗产

36. **IIIF Presentation API 3.0** — 数字图像/音频/视频/复合对象 Manifest/Canvas/Annotation。  
    https://iiif.io/api/presentation/3.0/
37. **CIDOC CRM** — 文化遗产事件式语义模型，ISO 21127 生态。  
    https://cidoc-crm.org/
38. **Linked Art** — 基于 CIDOC CRM 的开发者友好 JSON-LD profile。  
    https://linked.art/model/
39. **Smithsonian 3D / Voyager** — 3D 文化遗产浏览、注释、测量、切面、WebXR 和保护实践。  
    https://3d.si.edu/  
    https://smithsonian.github.io/dpo-voyager/
40. **OpenHeritage3D** — 高精度文化遗产 3D 原始数据、元数据与保存实践。  
    https://openheritage3d.org/
41. **Local Contexts** — TK/BC Labels/Notices；社区特定文化协议与来源治理。  
    https://localcontexts.org/

## C.7 Reality-Coupled Science / Learning

42. **OpenMAIC** — 多 Agent 互动课堂，2026 年加入 3D、模拟、游戏、编程、PBL；用于 Learning Experience 研究。  
    https://github.com/THU-MAIC/OpenMAIC
43. **phyphox** — 手机传感器实验、数据导出、远程控制、BLE；Reality Bridge 科学实验 Adapter 候选。  
    https://phyphox.org/  
    https://phyphox.org/source/
44. **openSenseMap / senseBox API** — 环境 IoT/open data；现实环境 Observation Adapter 候选。  
    https://github.com/sensebox/openSenseMap-API
45. **AR.js** — Web image/marker/location-based AR。  
    https://github.com/AR-js-org/AR.js
46. **Open Roberta Lab** — Apache-2.0，图形化机器人/传感器编程与真实设备连接。  
    https://github.com/OpenRoberta/openroberta-lab
47. **PhET Interactive Simulations** — STEM 交互仿真生态；适合 Experience/Simulation Adapter。  
    https://phet.colorado.edu/
48. **ADL LRS / xAPI 2.0** — 学习活动记录存储与 Experience API 互操作。  
    https://github.com/adlnet/ADL_LRS
49. **1EdTech Open Badges 3.0** — 带标准元数据与证据的可验证学习成果/技能凭证。  
    https://www.1edtech.org/standards/open-badges

## C.8 使用这些资料时的许可证原则

- 官方标准可按其规范许可实现，但商标、示例资产和第三方内容仍需分别检查；
- GPL/AGPL 项目可用于研究架构，直接链接、衍生和分发代码前必须做许可证评估；
- “开源代码”不代表模型权重、训练数据、游戏资产、声音、字体、3D 资产或具体 IP 自动可商用；
- OpenStory/Agent-Kernel/Concordia 等可考虑 Adapter/Reference；OpenMW/SS14 等优先研究设计思想，不把代码复制作为首选；
- 真实《红楼梦》版本、辽沈战役史料、家族隐私和博物馆馆藏的内容许可与来源门禁必须单独记录。

## C.9 可组合 Agent Runtime、Harness 与世界本体论新增参考（2026-08-14）

50. **DeepSeek Harness（官方）** — DeepSeek AI 开源 Agent Harness；“Everything is a Plugin”，由 Cordis 驱动；截至 2026-08-14 官方明确为 Developer Preview。用于 Agent Harness Provider 与 Capability Fabric 架构参考，不作为 Wanxiang Authority Kernel 直接依赖。  
    https://github.com/deepseek-ai/deepseek-harness  
    https://deepseek.com/harness
51. **DeepSeek Harness Architecture / Cordis Primer** — Service key、inject 依赖、typed events、可逆注册副作用、作用域和插件生命周期。  
    https://deepseek-harness.github.io/deepseek-harness/reference/cordis-primer
52. **A Programming Paradigm for Spatiotemporal Composability（Cordis, draft 2026-08-13）** — temporal composability / spatial composability、revertible effects、reactive coeffects；论文为持续修订中的预印本，工程采用时必须锁版本并验证。  
    https://github.com/cordiverse/paper
53. **W3C PROV-O** — Entity / Activity / Agent provenance ontology；用于 Evidence/Provenance Adapter，而非强行替代万相内部事实/历史模型。  
    https://www.w3.org/TR/prov-o/
54. **KurrentDB / Event Sourcing Documentation** — append-only event stream、projection/read model、重建与审计的工程参考；用于 Ledger/Projection 思想，不等于万相完整世界本体。  
    https://docs.kurrent.io/getting-started/introduction

---
# 附录 D：核心世界模型与角色运行详细规范

> 本附录保留 v3.0-R1 中已经细化的世界对象、认知、角色、组织、编译和运行时工程约束，并按 v5.2-R1 解释。若本附录出现“领域插件”等旧称，v5 中对应 **Domain Pack / Simulation Adapter / Co-Simulation Fabric**；若与正文存在命名冲突，以正文 v5.2 架构为准。

### 6. 一等领域对象

万相不把所有对象都强行做成 LLM Agent。底层至少有以下对象。

#### 6.1 Entity

世界中具有稳定身份的对象，例如：

- 人物、用户化身；
- 家族、组织、部队、国家；
- 文物、书信、武器、商品；
- 建筑、城市、道路、河流、房间；
- 任务、命令、合同；
- 数据源或数字资产。

#### 6.2 Component

实体的能力与状态由可组合组件组成。常见组件：

- `IdentityComponent`
- `PersonaComponent`
- `LifeArcComponent`
- `BeliefComponent`
- `MemoryComponent`
- `GoalComponent`
- `RelationshipComponent`
- `LocationComponent`
- `InventoryComponent`
- `HealthComponent`
- `AuthorityComponent`
- `OrganizationComponent`
- `SupplyComponent`
- `MobilityComponent`
- `AppearanceComponent`
- `RightsComponent`

组件必须具有版本、更新时间和来源。领域插件可注册新组件，但不能破坏核心 ID、事件和快照规则。

#### 6.3 Relation

实体之间具有时间有效范围的关系，例如亲属、任职、拥有、敌对、师生、指挥、道路连接和信息来源。

#### 6.4 Event

世界中已经发生并被提交的事实。事件是世界历史的基本单位，至少包含：

- 世界时间；
- 参与实体；
- 地点；
- 事件类型；
- 前置状态引用；
- 产生的 WorldDelta；
- 观察者；
- 证据或运行来源；
- 分支与 Run ID。

#### 6.5 Claim

某个主体持有的陈述，不一定是真实。Claim 用于：

- 角色信念；
- 传闻；
- 历史争议；
- 组织判断；
- 模型推断；
- 用户假设。

#### 6.6 Rule

规则描述动作是否允许、需要什么条件、产生什么影响，以及由哪个裁决器执行。规则分为：

- 核心不变量；
- 物理与空间规则；
- 社会、制度与权限规则；
- 领域规则；
- 正典/史实锁定规则；
- 安全与内容规则；
- 场景临时规则。

#### 6.7 Evidence

证据指向原始资料、抽取活动、人工审核或运行记录，用于支撑事实或推断。

#### 6.8 RightsManifest

记录资产来源与许可，包括：

- 版权与公版状态；
- 可见范围；
- 商业使用；
- 模型训练；
- 声音与肖像；
- 二次改编；
- 跨世界迁移；
- 删除与撤销；
- 文化协议与家庭权限。

#### 6.9 Observation

某个主体在某时刻能够获得的感知或信息，不等于世界真相。

#### 6.10 Intent / Action / Order

- `Intent`：角色或组织想达成什么；
- `Action`：在动作空间内提交的具体行动；
- `Order`：具有权限链、接收者和有效期的组织命令。

#### 6.11 Adjudication

裁决记录包括：

- 输入行动；
- 使用规则和模型；
- 参数、随机种子；
- 冲突处理；
- 结果概率或确定性判断；
- 专家干预；
- 生成的 WorldDelta。

#### 6.12 Snapshot / Run / Branch

- `Snapshot`：某个世界时间和事件序号下的权威状态；
- `Run`：一次可复现实验或体验；
- `Branch`：从某个快照产生的新世界线；
- `Experiment`：多个 Run 的组合；
- `Finding`：跨 Run 得出的暂定结论；
- `ValidityEnvelope`：结论成立的条件与限制。

---

### 7. 权威世界与多重主观世界

#### 7.1 Canonical World State

只有权威世界内核可以保存“当前真实状态”。包括：

- 时间；
- 实体存在性；
- 位置；
- 物品和资源；
- 已发生事件；
- 有效规则；
- 正在执行的命令；
- 当前分支；
- 被锁定的正典或史实事实。

#### 7.2 Public Knowledge

公开报道、公告、常识和广泛传播的信息。

#### 7.3 Group Knowledge

家庭、组织、部队、政府、门派或研究团队内部共享的信息。

#### 7.4 Individual Belief

个人：

- 亲眼看到的；
- 听说的；
- 推断的；
- 误解的；
- 被欺骗后相信的；
- 已经遗忘或压抑的；
- 知道但选择隐瞒的。

#### 7.5 Historical Record

后世史书、档案、回忆录和研究者对过去的记录。它们是 Claim 与 Evidence 的集合，不自动等于 Canonical Truth。

#### 7.6 运行原则

- 角色 Agent 永远不能直接读取全部 Canonical State；
- Observation Builder 根据位置、权限、时间、传播渠道和视野生成输入；
- 模型已在预训练中知道的未来事实不能自动进入角色决策；
- 知识越界审计器应检查输出是否引用当前角色不可能知道的信息；
- 历史模式中必须显示“历史资料”“模型重建”“用户分支”的区别。

---

### 8. 时间、空间与版本

#### 8.1 时间

系统同时支持：

- 精确时间；
- 日期或年代；
- 近似时间；
- 不确定时间；
- 开放区间；
- 叙述顺序与事件真实顺序；
- 多时间粒度；
- 世界时钟与场景局部时钟。

历史数据建议兼容 EDTF 表达不确定和近似日期。

#### 8.2 空间

地点不是永久不变的一组坐标。应支持：

- 不同时期名称；
- 行政归属变化；
- 点、线、面和区域；
- 地点之间的通行网络；
- 可见性、距离和移动成本；
- 建筑内部层级；
- 不确定或争议地理范围。

#### 8.3 世界版本

任何世界修改都应可追溯：

- 资料版本；
- 编译版本；
- 规则版本；
- 角色包版本；
- 运行时版本；
- 模型与 Prompt 版本；
- 世界分支；
- 正典与非正典标记。

---

## 第三篇　角色、组织与记忆

### 9. 角色核 Character Kernel

角色核不是一句 System Prompt，而是结构化、版本化、可评测的行为资产。

#### 9.1 Identity Kernel

相对稳定的内容：

- 身份认同；
- 核心价值；
- 基本欲望和恐惧；
- 道德边界；
- 依恋与关系模式；
- 长期创伤；
- 自我叙事；
- 不能无理由改变的核心约束。

#### 9.2 Life Arc

角色在不同人生阶段的：

- 身份；
- 知识；
- 关系；
- 信念；
- 能力；
- 重大转折；
- 允许变化的范围。

#### 9.3 Mid-term State

持续数日、数月或若干场景的状态：

- 压力；
- 未完成目标；
- 关系张力；
- 信念冲突；
- 身份危机；
- 组织责任。

#### 9.4 Short-term Affect

当前情绪、疲劳、疼痛、恐惧、愤怒、兴奋、注意力和冲动。

#### 9.5 Behaviour Policy

描述在不同风险、诱惑、冲突和权力关系下的决策倾向，而非仅用性格形容词。

#### 9.6 Perspective Boundary

角色在当前时间点：

- 能够感知什么；
- 知道什么；
- 不知道什么；
- 误以为什么；
- 对哪些来源信任；
- 哪些秘密不能泄露。

#### 9.7 Speech and Performance

语言、动作、语音、表情和视觉外形属于“表演组件”，不能与内在角色核混为一体。

#### 9.8 Evidence Ledger

每个重要人格结论绑定：

- 原文、史料或访谈来源；
- 直接行为、言语、心理或他人评价；
- 支持和反例；
- 置信度；
- 人工审核；
- 所属人生阶段。

---

### 10. 有界成长与人格守恒

#### 10.1 双层人格

- **身份不变量层**：只有重大、持续且有因果链的经历才能修改；
- **可塑层**：信念、目标、关系、技能和世界解释可以变化。

#### 10.2 变化流程

```text
事件
→ 角色观察到的部分
→ 当时的主观解释
→ 情绪与短期反应
→ 与旧信念冲突检测
→ 中期状态变化
→ 多次重复或重大转折
→ 提议长期 CharacterDelta
→ 漂移审计
→ 提交或拒绝
```

#### 10.3 人格漂移控制

- 定期匿名情境测试；
- 与历史检查点比较；
- 显示漂移来源；
- 允许导演锁定属性；
- 允许回滚到某个人生阶段；
- 不把“更讨用户喜欢”当作人物成长。

---

### 11. 记忆代谢 Memory Metabolism

#### 11.1 记忆不是日志堆积

每条记忆至少包含：

- 客观事件引用；
- 角色实际观察；
- 当时解释；
- 当时情绪；
- 重要性；
- 是否仍相信；
- 是否被后续证据纠正；
- 对行为和关系的影响；
- 可见范围与隐私。

#### 11.2 记忆类型

- 短期工作记忆；
- 第一人称情景记忆；
- 语义信念；
- 关系记忆；
- 技能与程序记忆；
- 创伤或高权重记忆；
- 群体共享记忆；
- 公共记录；
- 传闻与错误记忆。

#### 11.3 代谢过程

- 提取；
- 去重；
- 冲突检测；
- 归并；
- 重新解释；
- 遗忘与压缩；
- 重要记忆固化；
- 关系状态更新；
- 人物弧候选更新。

#### 11.4 记忆访问

检索不能只依赖向量相似度，还应结合：

- 时间；
- 参与人物；
- 地点；
- 关系；
- 当前目标；
- 可见范围；
- 信念状态；
- 证据强度；
- 人生阶段。

---

### 12. 组织与群体

#### 12.1 组织不是“大号人物”

家族、公司、军队、政府和门派应包含：

- 目标与制度；
- 资源；
- 权限层级；
- 成员和派系；
- 信息流；
- 命令流；
- 执行能力；
- 内部冲突；
- 对外关系。

#### 12.2 命令生命周期

```text
起草 → 审批 → 发送 → 延迟 → 接收 → 理解 → 再规划 → 执行 → 汇报
```

任何环节都可以发生误解、冲突、延迟或部分执行。

#### 12.3 多分辨率运行

- 宏观群体：统计或系统动力学；
- 中观组织：群体 Agent 与规则；
- 微观普通 NPC：状态机、小模型或模板；
- 焦点角色：完整角色 Agent。

---

## 第四篇　世界编译器

### 13. 世界编译器的职责

世界编译器把资料转为 `World Package`，不直接决定世界运行结果。

#### 13.1 输入

- TXT、Markdown、PDF、DOCX、EPUB；
- 图片、地图、扫描件；
- 音频、视频、字幕；
- 结构化 CSV/JSON/XML/RDF；
- IIIF Manifest；
- GEDCOM/Gramps；
- API、数据库与用户手工输入。

#### 13.2 编译流水线

```text
Source Registry
→ Parse & Segment
→ Entity Resolution
→ Event / Time / Space Extraction
→ Relation & Knowledge Boundary
→ Character / Organization Compilation
→ World & Rule Compilation
→ Scenario Assembly
→ Evidence / Rights Binding
→ Validation
→ Human Review
→ Package Build
```

---

### 14. Source Registry

每个来源记录：

- 唯一 ID；
- 标题、作者、机构；
- 文件哈希；
- 版本和日期；
- 语言与文字体系；
- 来源类型；
- 权利；
- 可信等级；
- 适用范围；
- 是否允许进入模型；
- 是否允许公开显示原文。

---

### 15. 文档与多媒体解析

长期能力包括：

- 文档结构、章节、卷、回目、场景；
- OCR 和古籍版面；
- 对话、旁白和引用；
- 图片区域和人物；
- 音频转写和说话人；
- 地图要素；
- 文物图像与说明；
- 多版本对齐。

v0.1 只支持 UTF-8 TXT/Markdown 与结构化 JSON/YAML，不做 OCR、PDF 全量解析和视频理解。

---

### 16. 实体消歧

需要处理：

- 同一人物多个称呼；
- 同名异人；
- 化名、封号、官职和亲属称呼；
- 古今地名；
- 组织更名和拆分；
- 文物编号与名称；
- 不同资料中的部队番号；
- 家谱中的字辈和重复姓名。

所有自动合并必须保留置信度与可撤销记录。

---

### 17. 事件—时间—空间编译器

输出：

- 事件候选；
- 参与实体；
- 时间及不确定性；
- 地点及历史版本；
- 前因后果候选；
- 谁见证、谁知道；
- 资料支持；
- 叙述顺序与事件顺序。

事件候选在人工确认前不能进入“正典事实”。

---

### 18. 人物编译器

#### 18.1 输出

- 身份和别名；
- 人生时间线；
- 人生阶段；
- 关系变化；
- 知识边界；
- 人格与行为策略；
- 语言和表演特征；
- 证据和反例；
- 匿名评测用例；
- 世界迁移规则。

#### 18.2 小说人物、历史人物和现实人物的差异

##### 小说人物

强调原著一致性、人物弧和文本证据。

##### 历史人物

强调史料版本、争议、时代限制和“历史真实决定/模型重建决定/用户替代决定”分离。

##### 现实与家族人物

强调本人或家属授权、隐私、记忆主观性、不可伪造新观点和删除权。

---

### 19. 世界与规则编译器

世界背景必须转成可执行规则，而不是只有自然语言描述。

输出可包括：

- 时间制度；
- 地理和交通；
- 技术与物理能力；
- 法律、礼仪和组织权限；
- 货币、资源和生产；
- 身份与阶层；
- 信息传播；
- 可用动作；
- 禁止动作；
- 正典锁定；
- 领域模型配置。

---

### 20. 场景编译器

`Scenario Package` 至少包含：

- 起始 Snapshot；
- 用户身份；
- 参与角色和组织；
- 可见信息；
- 目标；
- 约束；
- 动作空间；
- 时间范围；
- 结束条件；
- 评价指标；
- 正典/参与/反事实/自由模式；
- 表现配置。

---

### 21. 人机协同审核

全自动编译不是产品终点。Studio 必须提供：

- 原文与结果并排；
- 实体合并与拆分；
- 事件确认；
- 时间和地名修正；
- 人物结论证据查看；
- 争议资料并列；
- 权利和公开范围设置；
- 变更历史与审核人；
- 未确认数据的显式标志。

---

## 第五篇　权威世界内核

### 22. 世界内核的职责边界

世界内核只负责：

- 保存合法状态；
- 提交事件和 Delta；
- 维护快照、Run 和 Branch；
- 执行核心不变量；
- 提供查询与回放；
- 管理插件注册。

它不负责：

- 直接调用 LLM 写故事；
- 决定具体领域的战斗公式；
- 渲染地图和数字人；
- 自动认定史料真假；
- 让 Agent 绕过裁决器改状态。

---

### 23. 核心不变量

至少保证：

- 实体 ID 唯一；
- 世界时间不倒退，除非切换分支/回放；
- 事件只追加，不静默修改；
- Delta 应用前可验证；
- 不存在的实体不能行动；
- 位置、物品和资源不能凭空变化；
- 权限不足不能下达有效命令；
- 角色私有信息不能被其他角色直接读取；
- 同一 Run 与随机种子可重复；
- 分支不修改父分支历史；
- 正典锁定事件不能在受限模式下被覆盖。

---

### 24. 事件溯源与世界 Git

#### 24.1 事件流

世界当前状态由初始快照和事件流计算。

#### 24.2 快照

为提高性能，在固定事件间隔或关键节点保存快照。

#### 24.3 分支

从任意快照创建：

- 用户人生分支；
- 剧情重拍；
- 历史反事实；
- 实验参数变体；
- 不同模型 Run。

#### 24.4 比较

比较两条分支：

- 实体状态差异；
- 关键事件差异；
- 角色信念差异；
- 资源与指标差异；
- 人物弧差异；
- 证据和假设差异。

---

### 25. 插件模型

#### 25.1 插件类型

- Component 插件；
- Action 插件；
- Rule 插件；
- Resolver 插件；
- Observation 插件；
- Actor Policy 插件；
- Compiler 插件；
- Renderer 插件；
- Eval 插件；
- Import/Export Adapter。

#### 25.2 插件约束

- 只能通过公共接口读取或提交状态；
- 不能直接写数据库；
- 必须声明版本、依赖、权限和可重复性；
- 必须提供最小测试；
- 领域插件不得改变核心不变量。

---

## 第六篇　运行时

### 26. 标准运行循环

```text
1. Snapshot   读取权威世界快照
2. Schedule   选择本轮激活的实体和系统
3. Observe    为各主体构造不同观察
4. Deliberate 角色/组织根据人格、目标和信念推理
5. Propose    提交 Intent、Action 或 Order
6. Validate   检查权限、前置条件、空间与规则
7. Resolve    领域模型处理冲突、资源和概率
8. Commit     原子提交 Event 与 WorldDelta
9. Remember   更新主观记忆、信念与关系
10. Direct    导演决定焦点、节奏或下一场景条件
11. Render    输出文字、地图、2D、数字人等表现
12. Audit     检查一致性、越界、成本和安全
```

只有第 8 步可以修改权威世界。

---

### 27. 调度与激活

#### 27.1 不应每 Tick 调用所有 Agent

角色层级：

- 休眠实体：只保存状态；
- 背景实体：统计或规则更新；
- 轻量 NPC：状态机、小模型或事件驱动；
- 主要角色：完整认知运行；
- 焦点角色：强模型与深度记忆。

#### 27.2 激活条件

- 收到重要信息；
- 目标受阻；
- 进入焦点场景；
- 与用户或主要角色接触；
- 遭遇重大事件；
- 关系或身份发生变化；
- 导演或实验计划要求。

---

### 28. Observation Builder

根据以下条件构造观察：

- 位置与视野；
- 声音和通信范围；
- 组织权限；
- 信息延迟；
- 可靠度；
- 传播渠道；
- 欺骗、审查和误报；
- 当前角色的语言和认知能力；
- 时间知识墙。

Observation 必须记录来源与可见范围。

---

### 29. Actor Policy

#### 29.1 策略接口

Actor Policy 接收：

- ActorSnapshot；
- ObservationSet；
- 目标与约束；
- 可用动作；
- 记忆检索结果；
- 成本和延迟预算。

输出结构化候选：

- 判断；
- 意图；
- 行动；
- 命令；
- 对话；
- 不确定性；
- 使用的信息依据。

#### 29.2 实现类型

- ScriptedPolicy；
- RulePolicy；
- SmallModelPolicy；
- LLMPolicy；
- HumanPolicy；
- HybridPolicy。

所有测试必须有不依赖外部 API 的 DeterministicPolicy。

---

### 30. Action Validator

检查：

- Actor 是否存在、存活和激活；
- 是否具有权限；
- 动作是否在动作空间；
- 地点是否可达；
- 物品、资源与时间是否满足；
- 是否违反正典、时代、物理或安全规则；
- 是否引用不可见信息；
- 参数是否符合 schema。

失败返回结构化错误，而不是让 LLM 重新自由发挥。

---

### 31. Resolver

#### 31.1 混合裁决

- 核心规则：确定性；
- 领域公式：数值或概率；
- 开放社会行为：Agent 或专家；
- 叙事呈现：LLM；
- 高风险现实分析：人工参与。

#### 31.2 裁决输出

- 结果状态；
- 影响范围；
- 使用规则；
- 参数和随机种子；
- 不确定性；
- 解释；
- 可观察者；
- 审计标签。

---

### 32. Director Runtime

导演分三层。

#### 32.1 世界导演

管理时间推进、场景切换、焦点地点和外部事件。

#### 32.2 戏剧导演

管理主题、冲突、信息揭示、人物弧、必须/禁止事件和场景目标。

#### 32.3 表演导演

管理镜头、语气、动作、节奏、视觉和声音，不改变角色真实决定。

#### 32.4 约束分级

- Hard Constraints：不能违反；
- Narrative Goals：希望达到；
- Attractors：增加机会；
- Free Space：角色自主决策区域。

导演不能直接写入角色的爱、恨、信念或成长，只能改变外部条件或提出候选 CharacterDelta，后者需通过角色逻辑与审计。

---

### 33. Experiment Runtime

支持：

- 固定初始快照；
- 参数变体；
- 多随机种子；
- 多模型；
- 多角色策略；
- 批量运行；
- 对照和消融；
- 敏感性分析；
- 反事实干预；
- 指标计算；
- Finding 与 ValidityEnvelope。

LLM 可以提出值得测试的变量并解释结果，但不能仅凭语言生成因果结论。

---

---

# 附录 E：世界 IDE、显化、工程和部署详细规范

## 第八篇　显化与世界 IDE

### 40. 万相世界 IDE

Studio 不是单一无限画布，而是多个同步视图。

#### 40.1 世界画布

人物、组织、地点、事件、物品、规则和证据。

#### 40.2 关系视图

关系在不同时间点的变化、方向和主观差异。

#### 40.3 时间线

事件顺序、人物弧、历史分支和 Run。

#### 40.4 地图/游戏视图

位置、移动、视野、触发区、任务和 2D 小人。

#### 40.5 舞台视图

当前场景的角色、动作、台词、镜头、声音和数字人。

#### 40.6 调试视图

- 角色输入了什么；
- 调用了哪些记忆；
- 为什么选择行动；
- 哪条规则拒绝或裁决；
- 哪个模型和 Prompt；
- Token、成本和延迟；
- 是否越界或人格漂移。

#### 40.7 数据关系

数据库和事件日志是权威数据；画布和游戏只是投影。任何编辑通过命令和 API 提交，不能直接修改前端本地对象后视为世界事实。

---

### 41. 2D/2.5D 作为第一表现层

#### 41.1 为什么优先

- 比写实 3D 成本低；
- 适合多角色和地图；
- 可在 Web 与展馆设备运行；
- 便于表达位置、任务和世界状态；
- 适合导演模式和历史沙盘；
- 可以逐步升级到 Live2D、3D 和数字人。

#### 41.2 显化等级

| 等级 | 方式 |
|---|---|
| L0 | 头像、文字、状态卡 |
| L1 | 地图棋子与图标 |
| L2 | 像素/手绘 2D 小人 |
| L3 | Live2D/Spine 与语音 |
| L4 | 低模 3D |
| L5 | 写实数字人 |
| L6 | 自动生成章节视频 |

后台大量角色保持 L0/L1，只有焦点角色升级。

---

### 42. 数字人网关

数字人是角色的一个身体适配器。

输入：

- 角色身份与当前状态；
- 台词；
- 情绪与动作意图；
- 视觉资产与声音授权；
- 终端能力。

输出：

- TTS；
- 口型；
- 表情；
- 动作；
- 2D/3D 渲染；
- 实时流或视频。

数字人网关不得保存独立的“另一套人格真相”。

---

## 第九篇　数据协议与互操作

### 43. 万相包协议

#### 43.1 World Package

- Manifest；
- Entities/Components；
- Relations；
- Events/Timeline；
- Geography；
- Rules；
- Actors/Organizations；
- Scenarios；
- Evidence；
- Rights；
- Assets；
- Evals；
- Version/Dependencies。

#### 43.2 Character Package

- Identity Kernel；
- Life Arc；
- Beliefs；
- Memories；
- Goals；
- Relationships；
- Behaviour Policy；
- Knowledge Boundary；
- Performance；
- Evidence；
- Rights；
- Evaluation Cases。

#### 43.3 Scenario Package

- Initial Snapshot；
- Actors；
- User Role；
- Rules；
- Goals；
- Action Space；
- Constraints；
- Metrics；
- End Conditions；
- Display Config。

#### 43.4 Experience Package

组合世界、场景、前端主题、地图资产、声音、数字人和部署配置。

---

### 44. 外部兼容

#### 44.1 角色与叙事

- SillyTavern 角色卡、世界书和聊天记录；
- OpenStory/Agent-Kernel 适配器；
- 通用 JSON/YAML；
- 剧本与文本导出。

#### 44.2 文化遗产

- IIIF Manifest；
- CIDOC CRM 映射；
- PROV-O 来源；
- EDTF 时间；
- RDF/JSON-LD。

#### 44.3 家谱

- GEDCOM；
- Gramps 数据导入导出。

#### 44.4 3D 与终端

- glTF 作为运行时资产；
- 后期 OpenUSD 作为复杂制作与组合场景；
- Web、Godot、Unity、Unreal 通过 SDK 读取同一 API。

---

## 第十篇　证据、权利与安全

### 45. 信息真实性标签

所有对用户展示的历史、现实和文化内容都标记：

- 直接证据；
- 资料记载；
- 主观回忆；
- 学术或系统推断；
- 情境重建；
- 用户虚构；
- 模拟结果。

---

### 46. 权利模型

至少支持：

- 所有人可见；
- 项目成员；
- 家庭成员；
- 指定角色或组织；
- 仅本人；
- 到期开放；
- 身后开放；
- 特定地点/展览可见；
- 禁止训练；
- 禁止声音/肖像生成；
- 禁止公开分享；
- 允许/禁止商业化；
- 撤销和删除。

---

### 47. 安全边界

- API 密钥不入库、不入日志；
- 文件类型、大小和恶意内容校验；
- Prompt 注入与来源内容隔离；
- 模型工具权限最小化；
- 角色私有记忆严格授权；
- 审计日志不可由普通用户删除；
- 现实人物和未成年人保护；
- 生成数字人明确标识；
- 专业沙盘结果显示适用范围和不确定性；
- 禁止把娱乐模拟作为现实作战、医疗、法律或投资决策结论。

---

## 第十一篇　评测与可信度

### 48. 角色评测

- 人格一致性；
- 动态成长合理性；
- 知识边界；
- 关键选择；
- 语言与行为风格；
- 匿名人物测试；
- 长期漂移；
- 关系归属；
- 证据覆盖率。

---

### 49. 世界评测

- 时间单调；
- 空间可达；
- 物品和资源守恒；
- 权限；
- 秘密隔离；
- 正典锁定；
- 事件回放；
- 分支隔离；
- 同随机种子复现；
- 无幽灵实体和非法状态。

---

### 50. 历史与文化评测

- 来源覆盖；
- 不确定时间处理；
- 地名与时代一致；
- 历史人物未来知识泄漏；
- 史实、重建和虚构分层；
- 争议资料保留；
- 专家盲审。

---

### 51. 沙盘与实验评测

#### 51.1 Verification

软件是否按设计正确执行规则、状态和随机过程。

#### 51.2 Validation

模型是否对明确用途具有足够代表性。

#### 51.3 Accreditation / Usage Approval

由项目或机构决定某一版本是否可用于某种教学、展示或分析目的。

#### 51.4 结果表达

输出必须包含：

- 假设；
- 数据范围；
- 模型版本；
- 随机种子和运行数；
- 结果分布；
- 敏感变量；
- 不能支持的结论；
- ValidityEnvelope。

---

### 52. 工程评测

- 单 Tick 延迟；
- 角色调用数量；
- Token 与成本；
- 缓存命中；
- 状态提交失败率；
- 回放一致性；
- API 错误率；
- UI 可访问性；
- 数据迁移；
- 备份与恢复。

---

## 第十二篇　工程架构

### 53. 技术选择原则

- 核心领域层不依赖 Web 框架、数据库和 LLM SDK；
- 所有外部能力通过 Port/Adapter；
- 先做模块化单体，不提前拆微服务；
- SQLite 本地开发，PostgreSQL 生产兼容；
- 所有 LLM 都可替换，测试不依赖外部模型；
- Web UI 与 2D 运行共享 API；
- 事件和快照作为第一等数据；
- 类型、schema、迁移和测试优先于页面数量。

---

### 54. 推荐技术栈

#### 54.1 后端

- Python 3.12（可兼容 3.11）；
- FastAPI；
- Pydantic v2 作为 API 与包 schema；
- SQLAlchemy 2 + Alembic；
- SQLite 本地、PostgreSQL 生产；
- pgvector 作为后期可选向量能力；
- structlog 或标准 JSON 日志；
- OpenTelemetry 后期接入。

#### 54.2 前端

- TypeScript；
- React + Vite；
- TanStack Query；
- React Router；
- React Flow 或等价 MIT 画布组件；
- Phaser 作为 2D 地图/小人运行视图；
- Vitest + Playwright。

#### 54.3 工程

- `uv` 管理 Python；
- `pnpm` 管理前端；
- Docker Compose；
- Ruff、Pyright/Mypy、pytest、Hypothesis；
- ESLint、Prettier、TypeScript strict；
- GitHub Actions。

技术选择是首版实现建议，不是协议的一部分。未来可以增加 Godot、Unity、Unreal 和外部分布式 Agent 适配器。

---

### 55. 推荐仓库结构

```text
wanxiang-world/
├── AGENTS.md
├── README.md
├── LICENSE
├── pyproject.toml
├── pnpm-workspace.yaml
├── docker-compose.yml
├── .env.example
├── apps/
│   ├── api/
│   │   └── src/wanxiang_api/
│   └── web/
│       └── src/
├── packages/
│   ├── domain/          # 纯领域模型与不变量
│   ├── application/     # 用例、命令、查询、服务
│   ├── runtime/         # 调度、观察、验证、裁决、提交
│   ├── compiler/        # 文本/结构化世界编译
│   ├── actors/          # 策略接口与实现
│   ├── evidence/        # 来源、权利与审核
│   ├── persistence/     # SQLAlchemy 和仓储适配
│   ├── plugins/
│   │   ├── narrative/
│   │   └── campaign_lite/
│   └── sdk-ts/
├── worlds/
│   ├── floating_lantern_town/
│   └── northern_ridge_campaign/
├── docs/
│   ├── spec/
│   ├── architecture/
│   ├── decisions/
│   ├── runbook/
│   └── research/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
└── scripts/
```

---

### 56. 代码质量约束

- 小文件、小类、小函数；
- 单一职责；
- 领域模型不可依赖 FastAPI/SQLAlchemy；
- 禁止全局可变单例；
- 禁止在路由里写业务逻辑；
- 禁止在组件中直接访问数据库；
- 外部 API 必须有接口和 fake；
- 所有错误使用显式领域异常；
- 所有公共函数与类型有类型标注；
- 复杂分支写测试后再重构；
- 不以“以后再重构”为理由制造巨型模块；
- 单文件建议不超过 300 行，超过需拆分或在 DECISIONS 中解释；
- 不复制粘贴 schema；Python 与 TypeScript 通过 OpenAPI 或生成流程同步；
- 不把 Prompt 字符串散落在业务代码中；
- 不提交密钥、真实隐私数据和大模型缓存。

---

### 57. 核心 API 草案

#### 世界包

- `POST /world-packages/import`
- `GET /world-packages`
- `GET /world-packages/{id}`
- `GET /world-packages/{id}/export`

#### 世界实例

- `POST /worlds`
- `GET /worlds/{id}`
- `GET /worlds/{id}/state`
- `GET /worlds/{id}/entities`
- `GET /worlds/{id}/events`

#### 运行

- `POST /worlds/{id}/step`
- `POST /worlds/{id}/run`
- `POST /worlds/{id}/pause`
- `POST /worlds/{id}/actions`
- `POST /worlds/{id}/branches`
- `POST /worlds/{id}/replay`

#### 编译

- `POST /compiler/jobs`
- `GET /compiler/jobs/{id}`
- `GET /compiler/jobs/{id}/candidates`
- `POST /compiler/jobs/{id}/approve`

#### 调试

- `GET /worlds/{id}/traces`
- `GET /worlds/{id}/actors/{actor_id}/context`
- `GET /worlds/{id}/branches/compare`

---

### 58. 数据库边界

建议核心表：

- source_records；
- evidence_records；
- rights_manifests；
- world_packages；
- world_instances；
- entities；
- components；
- relations；
- rules；
- events；
- snapshots；
- runs；
- branches；
- actor_memories；
- actor_beliefs；
- compiler_jobs；
- audit_traces。

组件可使用 JSONB 保存可扩展内容，但身份、版本、时间、索引、关系与事件序号保持结构化字段。

---

### 59. 部署模式

#### 本地单机

SQLite + 本地文件 + 可选本地模型，适合开发、家庭和离线展馆。

#### 云端协作

PostgreSQL + 对象存储 + API 服务 + Web 前端。

#### 机构私有部署

Docker Compose 或 Kubernetes，提供模型网关、审计、备份和访问控制。

G0 只保证本地 Docker Compose 和无需 Docker 的开发运行；它是完整实施计划的地基，不等于最终活世界。

---

---

# 附录 F：真正虚拟世界的运行细化与长期自治

## 第十七篇　真正虚拟世界：活世界基质、角色接管与《红楼梦》参考实现

### 78. “真正世界”的工程判定

一个世界不能仅因为具有地图、角色头像和多 Agent 对话，就被称为真正虚拟世界。万相采用以下判定：

1. **持久性**：用户离开或停止输入时，世界状态不会丢失；在设定策略下可以暂停、自治推进或由 AI 代管。
2. **时空连续性**：人物、物品和事件存在于可计算的地点与时间中；移动、可见、可听和到达均受约束。
3. **物质连续性**：物品、容器、所有权、损坏、转移和信息载荷遵守守恒。
4. **生活连续性**：人物有身体、日程、职责、休息、饮食、健康、约会和被打断的计划。
5. **社会连续性**：身份、长幼、主仆、组织、制度、权限、义务、名誉和制裁影响行动。
6. **认知连续性**：每个人只能根据自己看到、听到、被告知、推断或误解的信息行动。
7. **因果连续性**：行动通过规则和领域模型产生后果，不能由叙述器任意跳过。
8. **角色连续性**：人格可以变化，但变化有事件链、版本和可回滚依据。
9. **控制连续性**：人类接管角色时，AI 不与用户争夺同一身体；退出后 AI 继承接管期间的后果。
10. **正典连续性**：原著事实、未来正典、体验补全和用户分支严格分层。
11. **可验证性**：世界能够从事件日志重建，同一快照与随机种子可以复现。
12. **可显化性**：同一世界可被呈现为文字、地图、2D、3D或数字人，但显化层不改变真相。

若缺少其中多数能力，系统更接近“交互叙事应用”；只有这些机制形成闭环，才接近 Persistent Living World。

---

### 79. 活世界基质的模块边界

#### 79.1 Spatial Substrate

核心对象：

- `WorldRegion`；
- `Place`；
- `Room`；
- `Portal`；
- `PathEdge`；
- `SpatialOccupancy`；
- `VisibilityZone`；
- `AcousticZone`；
- `AccessPolicy`。

必要能力：

- 层级空间与图结构并存；
- 门窗开闭、锁定与权限；
- 路径成本和移动时间；
- 空间容量、拥挤和私密性；
- 视线、声音和隔墙传播；
- 角色是否知道某地点以及是否能规划前往；
- 位置更新通过事件和 Delta 提交。

空间不应仅用 `(x, y)` 表示。2D 坐标服务于显示，拓扑、权限和可供性才服务于世界运行。

#### 79.2 Temporal Substrate

核心对象：

- `WorldClock`；
- `Calendar`；
- `TimeScale`；
- `Schedule`；
- `Appointment`；
- `Deadline`；
- `RecurringEvent`；
- `TimeWindowConstraint`。

支持：

- 当前场景分钟级推进；
- 附近人物小时级推进；
- 背景群体日级推进；
- 暂停、倍速、跳转和事件驱动；
- 由快照恢复；
- 不能无故倒退世界时间。

#### 79.3 Body and Need Substrate

核心组件：

- `HealthState`；
- `EnergyState`；
- `SleepState`；
- `PainState`；
- `IllnessState`；
- `MedicationState`；
- `MobilityCapability`；
- `AppearanceState`。

身体状态不等于简单生存游戏数值。它的用途是约束可行动作、日程、表演和他人反应，并由人物认知层解释主观体验。

#### 79.4 Material and Ownership Substrate

核心对象：

- `Item`；
- `Container`；
- `Ownership`；
- `Custody`；
- `Possession`；
- `InformationPayload`；
- `Transfer`；
- `Consumption`；
- `DamageState`。

一封信同时具有物质实体和信息载荷。角色获得信件，不代表已经阅读；阅读后才形成 Observation 和 Memory。

#### 79.5 Affordance and Action Substrate

动作不是无限自然语言。每个领域注册结构化 `ActionDefinition`：

```yaml
id: deliver_message
actor_requirements:
  - can_speak
parameters:
  target_actor: actor_ref
  content: text
preconditions:
  - same_acoustic_zone
privacy:
  overhearing: possible
resolver: social.deliver_message
```

自然语言只负责把用户或 Agent 意图映射为动作候选。Validator 和 Resolver 决定动作是否允许以及产生什么后果。

#### 79.6 Institution and Social Substrate

核心对象：

- `SocialRole`；
- `AuthorityGrant`；
- `Duty`；
- `Obligation`；
- `Norm`；
- `Permission`；
- `Sanction`；
- `Reputation`；
- `Household`；
- `Faction`。

制度不只是 Prompt 背景，而应进入动作验证、观察、关系和后果计算。

#### 79.7 Population Resolution Substrate

角色分为：

- 核心角色：完整角色核和长期记忆；
- 活跃场景角色：轻量规划和对话；
- 职责 NPC：日程、状态机和少量个性；
- 背景群体：统计状态；
- 被持续关注者：可升级为更高分辨率实体。

升级过程必须保存来源：正典角色不能由模型擅自重写；合成 NPC 必须标为生成实体。

#### 79.8 Autonomous World Loop

```text
Schedule due events
→ Activate affected entities
→ Build observations
→ Request only necessary decisions
→ Validate and resolve
→ Commit events and deltas
→ Update memories and beliefs
→ Aggregate background state
→ Produce summaries and alerts
```

自治循环必须允许无 LLM 模式运行，以便测试、回放、成本控制和离线展馆部署。

---

### 80. 人类—角色共驾平面

#### 80.1 核心对象

##### PlayerSession

绑定用户、世界实例、分支、视角和权限。

##### EmbodimentLease

确保一个角色身体在同一时刻只有一个主控制器：AI、人类、脚本或系统代管。

##### PerceptionEnvelope

只包含该角色当前允许看见、听见、记得和推断的信息，以及可执行动作。

##### PlayerIntent

保存用户真正意图；公开语言、内心和动作分开。

##### ShadowPolicy

负责角色化表达、微动作建议、知识边界提醒和人格偏离报告，不得替用户做重大决定。

##### ControlHandoffEvent

记录接管、恢复、暂停、超时代管、角色切换和所有权冲突。

#### 80.2 四种模式

1. **观察模式**：AI 控制，用户仅观看。
2. **意图模式**：用户给出目标，ShadowPolicy 转为符合角色的动作和表达候选。
3. **共驾模式**：用户决定重大选择，AI 管理惯例、微动作和非关键事务。
4. **完全接管**：用户控制所有重要动作，AI 仅做校验、提示和表达辅助。

#### 80.3 角色偏离不是简单分数

`CanonDistance` 至少由以下维度构成：

- 身份与价值边界；
- 当前人生阶段；
- 语言与社交策略；
- 知识边界；
- 已有关系；
- 历史决策证据；
- 偏离事件数量与持续时间。

系统应解释偏离来源并建立分支角色版本，而不是以单一“相似度”强迫用户服从原著。

#### 80.4 防止跨角色偷看

普通角色体验模式中，用户切换人物后获得的信息不得自动回流给之前的角色。导演模式可查看全局，但该分支应标记为“拥有跨视角知识，不再属于严格角色体验”。

---

### 81. 领域世界模型与领域包

#### 81.1 领域包的职责

领域包不是内容 MOD，也不是一组 Prompt，而是可版本化的可执行语义包。它可以注册：

- 组件 schema；
- 动作和 Affordance；
- 规则和约束；
- 裁决器；
- 制度和组织模板；
- 日程模板；
- 世界补全器；
- 编译器扩展；
- 视图和数字人映射；
- 测试、评测和迁移。

#### 81.2 插件安全

- 插件不能直接访问 ORM 会话修改权威表；
- 所有变化返回 `ProposedDelta`；
- 核心内核验证后才能 Commit；
- 插件必须声明权限、版本和兼容范围；
- 插件必须有单元、合同和回放测试；
- 插件升级需要 migration 和世界包兼容策略。

#### 81.3 红楼梦领域包不应包含什么

- 不应把整部小说放入一个 System Prompt；
- 不应让所有角色共享同一个向量库；
- 不应把文学人物压缩成几个性格标签；
- 不应让未来正典直接进入人物当前上下文；
- 不应把世界补全当作原著事实；
- 不应让 LLM 决定物品、空间和权限的全部结果。

---

### 82. 《红楼梦》世界包的分层结构

```text
red_chamber_world/
├── manifest.yaml
├── source_registry/
├── canon/
│   ├── editions/
│   ├── chapters/
│   ├── scenes/
│   ├── events/
│   └── future_canon/
├── entities/
│   ├── characters/
│   ├── organizations/
│   ├── places/
│   ├── items/
│   └── roles/
├── domain/
│   ├── institutions/
│   ├── schedules/
│   ├── actions/
│   ├── norms/
│   └── resolvers/
├── perspectives/
├── evidence/
├── completion/
├── visuals/
├── scenarios/
├── evals/
└── rights/
```

#### 82.1 正典三层

- `PastCanon`：当前时间点已经发生的事实；
- `CharacterCanon`：人物身份、经历、关系和人格边界；
- `FutureCanon`：原著未来事件，只供正典控制平面使用，禁止注入当前人物观察。

#### 82.2 三种运行模式

##### 原著重演

关键正典节点被锁定，用户只能在软空白中互动。若用户试图破坏锁定事件，系统明确解释该模式约束。

##### 软正典

未来事件表现为吸引子和条件图；只要产生足够强且可审计的因果链，就可改变。

##### 自由分支

从分支点起，未来正典仅作为比较基线，不再强制。

#### 82.3 世界补全账本

每个补全项保存：

```yaml
completion_id: completion_001
category: era_grounded_reconstruction
supports:
  - source_ref_12
  - source_ref_34
confidence: 0.72
review_status: pending
can_enter_canon: false
usage:
  - experience
  - background_simulation
```

---

### 83. 《红楼梦》最小活世界参考范围

第一版不要做整部《红楼梦》，而应做一个具有完整世界机制的小切片。

#### 83.1 空间

- 潇湘馆及其必要室内、廊下和出入口；
- 怡红院及其必要室内、廊下和出入口；
- 两地之间的公共路径；
- 一个公共会面或过渡空间；
- 空间访问、可见、可听和私密规则。

#### 83.2 人物

- 林黛玉；
- 贾宝玉；
- 紫鹃；
- 另外两名依据所选时间点和来源确认的主要人物；
- 10-20 名职责型 NPC。

#### 83.3 物品

- 信件或诗稿；
- 礼物；
- 药物；
- 服饰或首饰；
- 房间陈设；
- 容器、钥匙和保管关系。

#### 83.4 动作

- 移动、观察、等待；
- 交谈、试探、隐瞒、传话；
- 请安、访友、探病；
- 写信、读信、藏信、交付；
- 赠礼、拒礼、转交；
- 赴约、回避、邀请；
- 休息、服药、用饭；
- 写诗或参与经领域包定义的活动。

#### 83.5 七日验收场景

1. 世界由固定快照启动；
2. 第一日用户接管林黛玉；
3. 用户委托紫鹃传话；
4. 紫鹃有权接受、改变方式或拒绝；
5. 消息按真实路径传播，其他人不能自动知道；
6. 信件拥有持续位置、保管和阅读状态；
7. 人物按日程生活并受身体、职责和邀请影响；
8. 用户第三日退出，AI 恢复控制；
9. 第三日建立分支，父分支保持不变；
10. 第七日可回放所有事件并重建世界；
11. 可以比较 Canon、用户分支和无人干预分支；
12. 每个正典事实、补全内容和模型生成内容均可识别。

---

### 84. 世界自治、离线与在线策略

用户不在线时提供三种策略：

- `PAUSED`：世界时间暂停，适合单人剧情；
- `BACKGROUND_SIMULATION`：背景日程和低成本规则继续，关键决策等待用户；
- `FULL_AUTONOMY`：AI 或脚本代管角色并继续世界，仅适合用户明确授权的分支。

接管人物离线时还需配置：

- 关键决策是否阻塞；
- 可代管动作白名单；
- 代管时长；
- 恢复时摘要；
- 用户可否回滚代管事件。

---

### 85. 数据存储与事件流更新

建议在现有核心表之外增加：

- `spaces`、`portals`、`spatial_occupancy`；
- `world_clocks`、`schedules`、`appointments`；
- `items`、`containers`、`ownerships`、`custodies`；
- `affordance_definitions`、`action_definitions`；
- `social_roles`、`authority_grants`、`duties`、`norms`；
- `player_sessions`、`embodiment_leases`、`control_handoffs`；
- `completion_records`、`canon_constraints`、`canon_distances`；
- `agent_activation_records`、`background_aggregates`。

所有可变状态仍然通过 Event/Delta 更新。关系数据库中的派生当前状态可以重建，不能成为无法追溯的唯一事实。

---

### 86. API 补充

```text
POST   /worlds/{world_id}/instances/{instance_id}/advance
POST   /instances/{instance_id}/embodiment/acquire
POST   /instances/{instance_id}/embodiment/release
GET    /instances/{instance_id}/perception
POST   /instances/{instance_id}/player-intents
GET    /instances/{instance_id}/available-actions
GET    /instances/{instance_id}/spaces
GET    /instances/{instance_id}/schedules
GET    /instances/{instance_id}/items
POST   /instances/{instance_id}/branches
GET    /instances/{instance_id}/canon-distance
GET    /world-packages/{id}/completion-ledger
POST   /domain-packs/install
GET    /domain-packs
```

API 返回不得包含未授权私有认知。调试端点必须受 Studio/Director 权限控制。

---

### 87. 评测矩阵

| 维度 | 核心问题 | 自动测试示例 |
|---|---|---|
| 空间 | 人物是否能穿墙、瞬移、隔院听见 | 路径、门户、声学属性测试 |
| 时间 | 日程和事件时间是否一致 | 单调时间、冲突约会、重放 |
| 物品 | 一封信能否同时在两处 | 守恒、转移、容器、阅读状态 |
| 制度 | 角色能否越权调动资源 | Permission/Authority 合同测试 |
| 认知 | 是否知道未见或未来信息 | Perspective leakage 测试 |
| 人格 | 新情境行为是否符合阶段 | 匿名决策集和偏离解释 |
| 接管 | AI 是否与用户争夺身体 | Lease 唯一性和 handoff 测试 |
| 分支 | 子世界是否污染父世界 | Snapshot/Branch 隔离测试 |
| 正典 | 体验补全是否冒充原文 | Provenance/category 强制测试 |
| 自治 | 七日后世界是否崩坏 | 长期运行、内存、循环、死锁 |
| 成本 | 背景角色是否频繁调用强模型 | Router/activation 预算测试 |
| 显化 | UI 是否与权威状态一致 | API 合同和 E2E 回放测试 |

---

### 88. 技术实现原则补充

1. **模块化单体优先**：G0-G5 不拆微服务；先用清晰 package 和 Port/Adapter 边界。
2. **确定性核心优先**：基础时空、物品、权限、控制权和回放必须脱离 LLM 可运行。
3. **LLM 可替换**：角色策略和世界编译可使用 LLM adapter，但测试使用 DeterministicPolicy。
4. **前端不是权威源**：Phaser、React Flow 和数字人只提交命令、读取视图。
5. **领域包版本化**：每个世界记录依赖的领域包版本。
6. **数据门禁**：真实文学、历史和家庭内容必须通过 Source Registry 和审核状态。
7. **小文件、低耦合、高内聚**：领域模型、用例、适配器、UI 分离；禁止巨型 manager 和 utility 文件。
8. **可回放先于“智能”**：无法回放和解释的智能行为不能进入权威运行链。
9. **人类可接管和撤销**：任何代管、自动生成或角色接管都具有明确权限和日志。
10. **不声称灵魂复制或历史预测**：系统只构建证据约束的角色策略和假设世界。

---

---

# 附录 G：新对话 / Codex 工程交接说明

## G.1 新对话的唯一上下文原则

新对话不依赖旧聊天记忆。把以下文件置于代码仓库根目录，并要求 Codex 先读完再执行：

```text
MASTER_PROGRAM.md
AGENTS.md
PLAN.md
STATUS.md
DECISIONS.md
BLOCKERS.md
KNOWN_FAILURES.md
CHANGELOG.md
docs/spec/WANXIANG_v5_MASTER_SPEC.md
docs/architecture/ARCHITECTURE.md
docs/acceptance/ACCEPTANCE.md
docs/references/REFERENCE_CATALOG.md
```

## G.2 Codex 开工顺序

1. 盘点仓库状态和 Git 历史；
2. 读取所有 required docs；
3. 建立/更新 PLAN、STATUS；
4. 从当前最早未通过的 Goal 开始；
5. 每个 Goal：实现 → 单测 → 集成 → E2E → lint/typecheck/build → 文档 → acceptance evidence；
6. 通过 Gate 后本地 commit；
7. 遇外部数据门禁写入 BLOCKERS，但继续所有不依赖该数据的任务；
8. G12 结束时生成 `reports/FINAL_REPORT.md` 和 `reports/ACCEPTANCE_EVIDENCE.md`。

## G.3 明确禁止

- 不得把静态 UI、写死 JSON、TODO、NotImplemented、空函数或仅 prompt 演示视为完成；
- 不得为了测试通过删除/skip 关键测试；
- 不得让 LLM、浏览器或外部模拟器直接 UPDATE Canonical State；
- 不得凭模型记忆编造《红楼梦》正典、辽沈战役史实、家族事实或馆藏事实；
- 不得把合成 demo 改名冒充真实世界；
- 不得在 G0–G8 过早拆微服务；
- 不得把 API Key 作为基础测试运行的必要条件；
- 不得自动 push 远程仓库，除非明确授权。

## G.4 完成判定

“完成万相”在本工程程序中指：**G0–G12 所有可自动完成的 acceptance criteria 已有可复现证据，外部资料/授权阻塞被明确记录，系统能在无 LLM Key 情况下运行确定性核心测试和合成 demo，并能在配置 LLM 后替换策略而不改变权威状态协议。**

---

**文档结束。**
