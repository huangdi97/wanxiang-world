# Source → Living World 正式管线

```text
[1] SOURCE
    ↓
[2] SourceRegistry + Rights + Version + Checksum
    ↓
[3] SourceAdapter
    ↓
[4] ParsedDocument / StructuredRecords / AssetReferences
    ↓
[5] Segment + StableLocator
    ↓
[6] Multi-pass Distillation
    ↓
[7] CandidateEnvelope / Claim / Evidence
    ↓
[8] Identity Resolution + Cross-source Alignment
    ↓
[9] Conflict Preservation + Review Decisions
    ↓
[10] Domain Inference / Dependency Resolution
    ↓
[11] WorldDraft
    ↓
[12] Missingness Graph / Completion Plan
    ↓
[13] Completion Candidate E0–E5
    ↓
[14] Consistency / Constraint Validation
    ↓
[15] Scenario Candidate / Genesis Plan
    ↓
[16] WorldPackageDraft
    ↓
[17] Preview Instance
    ↓
[18] Worldness Evaluation
    ↓
[19] Repair Proposal / Completion Loop
    ↓
[20] Publishable WorldPackage
    ↓
[21] Living World Instance
```

### 统一原则

任何环节都只能增加：来源、候选、审核、补全、编译产物或 Proposal。
只有 Runtime 的唯一 Commit Boundary 可以产生运行历史。
