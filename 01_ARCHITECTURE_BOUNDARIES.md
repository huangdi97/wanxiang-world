# 架构边界与不可破坏原则

## 万相工程总分解

```text
Wanxiang Kernel
  Reality Root / Semantic ISA / Identity / Fact / Event / Constraint
  Commit / Ledger / Snapshot / Replay / Branch / Worldline / Lineage / Invariant

Wanxiang Runtime
  World Host / Clock / Space / Body / Objects / Actors / Organizations
  Perception / Belief / Memory / Action / Simulation / Capability Fabric

Wanxiang Forge
  Source / Evidence / Distillation / Completion / Genesis / Compiler
  WorldDraft / Domain Composition / Emergence / Evolution / Promotion

Experiences
  Studio / Player / Strategy / Heritage / Family / Learn / SDK
```

## 本轮修改集中区域

主要修改：Forge + Studio + adapters + infra + tests。

Kernel 语义默认冻结。

## 十条禁止

1. 禁止创建第二套 Canonical State。
2. 禁止创建第二套 Commit pipeline。
3. 禁止创建第二套 Package Registry。
4. 禁止每种 Source 做一套独立世界编译流程。
5. 禁止 per-domain Runtime fork。
6. 禁止 LLM/Agent/Parser 直接写 Canon。
7. 禁止前端 local state 成为世界权威。
8. 禁止 WorldDraft 演化成第二个 Runtime State。
9. 禁止以 giant WorldManager / ForgeManager / Utils 聚合全部逻辑。
10. 禁止为了本轮需求改 Reality Root，除非跨领域不可表达且有失败证据与 Kernel Change Proposal。
