# Autonomous World Authoring

目标不是“让一个 Agent 自由写世界”，而是让 Orchestrator 自动驱动**受约束的编译闭环**。

```text
Assess Draft
↓
Find Missing / Conflict / Low Confidence
↓
Choose Tool / Distiller / Retrieval / Domain Rule / Completion Provider
↓
Generate Candidate / Proposed Repair
↓
Evidence + Rights + Constraint Check
↓
Auto-approve only low-risk policy class
↓
Rebuild Draft
↓
Preview
↓
Worldness Evaluate
↓
Repeat until stop criteria
```

## 自动停止条件

- 无 P0 blocking gap；
- publish-required rights PASS；
- critical identities resolved；
- initial scenario instantiate PASS；
- replay/determinism PASS；
- worldness minimum thresholds PASS；
- remaining uncertainty is explicitly labeled rather than fabricated。

## 自动化绝不能做

- 把模型幻觉提升成 E0；
- 把冲突来源消成单一“真相”；
- 改写源文件；
- 直接改 Kernel；
- 为通过分数而硬编码 benchmark fixture。
