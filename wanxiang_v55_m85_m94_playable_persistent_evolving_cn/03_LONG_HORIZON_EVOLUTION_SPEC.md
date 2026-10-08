# Long-Horizon & Evolution Spec

## 时间跨度

本轮至少建立：
- 24h smoke；
- 7d qualification；
- 30d long-run；
- 90d selected-world certification；
- selected 1-year accelerated research run（若成本/时间允许；不能伪装为 required PASS）。

## 必须解决

- recurring scheduler；
- background simulation；
- sleep/wake/availability；
- actor activation/deactivation；
- checkpoint/resume；
- snapshot/compaction；
- crash recovery；
- deterministic/reproducible reference profile；
- provider budget / token/call/time budgets；
- storage growth；
- memory growth；
- LOD transitions；
- no silent history rewrite。

## Evolution Delta Types

必须分离：
- StateDelta
- BeliefDelta
- RelationshipDelta
- CapabilityDelta
- PersonaDelta
- OrganizationDelta
- InstitutionCandidate
- OntologyCandidate

禁止一个“CharacterEvolutionBlob”吞掉所有变化。

## Emergence Ladder

```text
L0 Event
→ L1 Repeated Pattern
→ L2 Habit / Skill
→ L3 Social Norm
→ L4 Institution
→ L5 World Structure / Ontology
```

每一级都要有 evidence、confidence、window、counterevidence、review/promotion policy。
