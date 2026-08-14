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

