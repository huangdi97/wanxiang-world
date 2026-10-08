# Worldness Validation

Preview 不是“能启动进程”就算世界。

## 最低 Worldness 指标

1. Persistence：物品/人物/关系状态跨 tick 持续存在。
2. Temporal Causality：事件顺序和前置条件有效。
3. Epistemic Isolation：角色不知道未观察/未传播的信息。
4. Spatial Coherence：移动必须经过可达空间关系。
5. Action Consequence：行动产生真实、可回放后果。
6. Autonomous Continuation：无用户时至少参考策略可推进。
7. Branch Isolation：Preview/Branch 不污染母本。
8. Replayability：事件日志可重建状态。
9. Provenance：关键世界定义能回到 Source/Completion。
10. Uncertainty Honesty：未知保持未知，不用生成内容伪装事实。

## 自动验证循环

```text
Preview Run
→ Detect Worldness Failure
→ Gap / Repair Candidate
→ Review Policy
→ Draft Revision
→ Recompile
→ New Preview
```

Preview simulation 永远不能直接回写 Source 或 Canon World Definition。
