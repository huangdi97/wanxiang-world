# Playable Product Experience Spec

## 普通用户入口

```text
World Plaza
├─ Continue
├─ Explore Worlds
├─ My Worlds
├─ My Characters
└─ Create World
```

用户不应先看到 Candidate / Coverage / WorldPackage 等工程对象。

## 进入世界

```text
World Card
→ Select Scenario
→ Choose Existing Character / Create Character / Observer
→ Acquire Embodiment or Presence
→ Enter
```

## Play HUD 最低产品面

- 当前时间 / 地点；
- 当前角色；
- 可感知对象/人物；
- 自由行动输入；
- suggested affordances；
- Memory / Goal / Relationship（按权限）；
- StateDiff；
- Timeline / recent events；
- Pause / Continue / Leave；
- Branch / Experiment（有权限时）。

## StateDiff

每个 Commit 后至少可表示：
- actor state changes；
- location changes；
- relation changes；
- item custody/ownership changes；
- task/opportunity changes；
- knowledge/belief changes（按 actor 权限显示）；
- organization/role changes；
- explicit no-change where useful。

StateDiff 从 committed events/projections 计算，不直接信任 LLM 自述。
