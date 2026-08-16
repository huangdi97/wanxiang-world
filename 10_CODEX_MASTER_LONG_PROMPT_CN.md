# Codex 长连续执行总指令：Wanxiang v5.3 M43–M50

继续当前已经完成 M42 的万相仓库，不新建项目，不从零重写。

## 总目标
今晚连续完成 `G46A → G53J`，对应 `M43 → M50`。完成 Multiverse Runtime、Interworld、Hybrid Genesis、Cross-world Distillation、Multiverse Studio/Experience、World Intelligence Provider Boundary、v5.3 Final Certification，并在最终认证后把 feature branch 推到 GitHub。

## 必读
1. README_FIRST.md
2. 00_PROGRAM_ARCHITECTURE.md
3. 01_KERNEL_FREEZE_AND_MINIMAL_CODE_POLICY.md
4. 02_GITHUB_DELIVERY_POLICY.md
5. 03_INTERWORLD_SEMANTICS.md
6. 04_HYBRID_GENESIS_STANDARD.md
7. 05_WORLD_INTELLIGENCE_BOUNDARY.md
8. 06_FINAL_RELEASE_EVIDENCE.md
9. 07_GOALS_INDEX.md
10. 08_MILESTONE_GATES.md
11. 09_RESUME_PROTOCOL.md
12. 仓库 M42/v5.2 reports + AGENTS/PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG + Git + tests + migrations
然后读完全部 `goals/` 与 `milestones/`。

## 连续执行
每个 Goal：盘点复用 → 实现 → 测试/负向/回放/迁移 → 文档/证据 → PASS 后本地 commit → 自动下一个。每个 Milestone 运行 Gate，FAIL 自己修，PASS 自动继续，不询问用户。

## 硬约束
- Kernel v1 默认冻结。
- 所有世界变更仍走唯一 Commit Boundary。
- Branch/Worldline/Lineage 复用已有历史模型。
- Interworld/Hybrid 不改写 parent history。
- World Intelligence 只能 Prediction/Plan/Candidate/ProposedDelta。
- 具体世界/provider 名称不得进入 Kernel。
- 核心测试不依赖外部 LLM/API。
- 不新增重复 Manager/Registry/Engine/State/Event/Branch。
- 不得提交 secrets/private data/restricted corpus/model cache。
- 不得 skip/delete tests 或 hardcode PASS。

## GitHub 授权与规则
用户明确授权最终正常 `git push`。先遵循 `02_GITHUB_DELIVERY_POLICY.md`。不 force push、不删除历史、不提交 secret/private/restricted corpus。优先 feature branch。remote/auth 可用则 push 并记录最终 SHA；`gh` 可用且权限允许可建 PR；最终认证 PASS 后才可选 push `v5.3.0-rc1` tag/release。若 remote/auth/permission 客观不可用，记录 EXTERNAL_BLOCKED，不伪造成功。

## 最终停止
只有内部 M50 条件全部 PASS，且 GitHub push 已 PASS 或有明确外部阻塞报告后，生成最终报告并停止。禁止自行开始 v5.4。


---

# 【最高优先级补充】Public GitHub + CI 自动发布闭环

用户已经明确授权：本轮完成后**直接开源**，自动创建 GitHub public repository、push，并建立/验证 CI。

因此从 G53G 起，旧的“只 push feature branch/可选公开”策略被本补充覆盖。严格读取：

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- 新版 G53G–G53L

最终必须连续执行：

```text
G53F 本地 Final Certification
→ G53G Open-source Readiness / history safety
→ G53H OSS license/docs/governance
→ G53I GitHub Actions CI preparation
→ G53J gh repo create PUBLIC + push
→ G53K gh run 查询远端 CI；失败则修复并再次 push，直到核心 CI 全绿
→ G53L tag v5.3.0-rc1 + GitHub Release Candidate + final report
→ STOP
```

默认 repo：`wanxiang-world`；冲突时使用 `wanxiang-world-os` / `wanxiang-world-engine`。

若当前仓库没有 LICENSE，默认代码许可证使用 Apache-2.0；但代码许可证绝不能覆盖或暗示覆盖第三方/受限数据与资产。

特别注意完整《红楼梦》：只有 rights metadata 明确允许公开再分发的 corpus 才能进入公开 Git history。否则公开仓库只保留 Source/Import/Manifest/Parser/Fixture/Documentation，底本文本保留在 ignored local data storage，不删除用户本地原件。

远端 CI 是 Acceptance：不得在 CI 失败时停止，也不得通过 disable workflow、skip test、删测试制造假绿。必须读日志、修复、push，直到 final commit 的核心 GitHub Actions 全绿。
