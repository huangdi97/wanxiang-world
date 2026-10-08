# 多轮世界语义蒸馏规范

## Candidate 类型

- Identity / Alias
- Character / Persona / LifeArc
- Relation
- Organization / Role
- Event / Timeline / Causality Candidate
- Time / Temporal Uncertainty
- Place / Space / Topology
- Object / Object Biography
- Knowledge Boundary / Witness / Secret
- Rule / Norm / Institution
- Skill / Behaviour / Affordance
- Scenario
- Ontology

## 多轮蒸馏

```text
Pass 0 Structure
Pass 1 Identity
Pass 2 Event-Time-Space
Pass 3 Relation-Organization
Pass 4 Character-Knowledge
Pass 5 Object-Rule-Skill
Pass 6 Cross-chapter/Coreference
Pass 7 Contradiction/Gap
Pass 8 World Assembly Candidates
```

每一轮必须：
- versioned；
- resumable；
- source-locatable；
- deterministic reference path 可测试；
- 可被更强 Provider 替换。

LLM 可以提高 recall，但不得绕过 Candidate/Evidence/Review。
