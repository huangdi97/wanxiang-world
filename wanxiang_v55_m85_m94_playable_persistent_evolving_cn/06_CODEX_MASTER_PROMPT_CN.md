# Codex Master Prompt — Wanxiang v5.5 M85–M94

继续当前 `wanxiang-world` 仓库。以 v5.4-STABLE-R2 完整母版为 Source of Truth。

## 任务

从 G88A 连续执行到 G97J，构建：

> **Playable, Persistent, Evolving Living Worlds**

不是重新做 Source→World，不训练模型，不进入 v5.6。

## 先做真实仓库审计

开工前：
- git status / log / remote / tags；
- v5.4.0 release / clean-room evidence；
- 当前 Kernel/Runtime/Forge/Studio/Experience 实现；
- KEEP / EXTEND / MERGE / DELETE / ADD matrix；
- 禁止按 Goal 文档机械新建重复系统。

## 顺序

M85 G88A–G88H
→ M86 G89A–G89H
→ M87 G90A–G90H
→ M88 G91A–G91H
→ M89 G92A–G92H
→ M90 G93A–G93H
→ M91 G94A–G94H
→ M92 G95A–G95H
→ M93 G96A–G96H
→ M94 G97A–G97J

每 Goal：读取真实代码 → 实现 → 测试 → 报告 → commit → 自动继续。
每 Milestone：qualification FAIL 就修，不问用户是否继续。

## 最终真实验收

必须至少证明：

1. Playable product：World Plaza→Character→Enter→Free Action→Committed StateDiff→Leave→Continue；
2. 7d actor continuity；
3. 30d literary long-run；
4. 90d selected-world long-run；
5. Actor/Belief/Relationship/Organization evolution；
6. evidence-backed emergence candidate + false-positive controls；
7. WorldRunArtifact + ExperimentRegistry + 4+ parallel worldlines + intervention + comparison；
8. ValidationStack 不是 Worldness 别名；
9. reference Physical/Visual Provider bridge；
10. clean-clone + GitHub required CI 全绿。

只有以上关键 Gate ACCEPTED 才创建 `v5.5.0-rc1` prerelease。

## 外部能力

如果 Godot/Unreal/SimWorld/Genie-class/外部模型在环境不可用：
- 完成 ABI、reference provider、contract tests、docs；
- 只把具体外部 adapter 真实运行标为 EXTERNAL_BLOCKED；
- 不得因此阻塞所有内部 M93/M94；
- 不得伪造通过。

## STOP

G97J 后停止。不得自动进入 v5.6、True Genesis、自训练模型或十万 Agent 项目。
