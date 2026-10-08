# v5.5 Final Acceptance — RC1 Hard Gate

只有全部 required 条件满足才允许 `v5.5.0-rc1`：

## Playable
1. PlayableWorldProfile 可由 v5.4 world 构建。
2. World Plaza / Continue / My Worlds / My Characters E2E。
3. Character/Observer/Embodiment 权限正确。
4. Free Action → ActionProposal → Commit 闭环。
5. StateDiff 由 committed state 计算。
6. Leave / Continue 保持同一世界连续性。

## Character Continuity
7. ActorGoalStack 可持久、可回放。
8. Memory / Belief / Truth 分离。
9. Secret / rumor / future knowledge 隔离。
10. RelationshipState 有时间/事件来源。
11. 7-day Actor continuity PASS。

## Workshop
12. From Source regression PASS。
13. From Prompt 产生 E5 Candidate/WorldDraft。
14. Hybrid Genesis 保持 E0–E5 provenance。
15. public/private/unlisted/family-private publish gates 正确。

## Director / Pressure
16. PressureProfile 不进入 Kernel。
17. CANON/DIRECTED/LIVING/EXPERIMENT 模式可运行。
18. Director 无 Commit 权。
19. Opportunity 可被 Actor 忽略。
20. Intervention 只存在于实验 branch/artifact。

## Long Horizon
21. 24h PASS。
22. 7d PASS。
23. 30d literary PASS。
24. 90d selected-world PASS。
25. checkpoint/resume/crash recovery PASS。
26. compaction 后 replay equality。
27. SimulationLOD transition state-continuous。
28. cost/storage/memory growth 有量化报告。

## Evolution
29. State/Belief/Relationship/Capability/Persona/Organization Delta 分离。
30. 30d Actor/Relationship/Organization 非零合理演化。
31. Evolution 可解释并可回放。
32. source/canon definition 未被运行时演化污染。

## Emergence
33. Pattern detector 有 positive + negative benchmark。
34. 至少一个 evidence-backed Habit/Norm/Institution Candidate。
35. 高层晋升有更严格证据/审批。
36. false-positive controls PASS。
37. 不声称 universal emergence。

## World Lab
38. WorldRunArtifact 完整可复验。
39. ExperimentRegistry 可恢复。
40. fork/intervention parent isolation。
41. 至少 4 条 parallel worldlines。
42. multi-provider/policy or mixed-population comparison。
43. WorldlineComparator 输出 trajectory/cost differences。
44. ValidationProfile V0–V7 实现；unknown != pass。

## Provider Bridge
45. Physical Provider ABI contract PASS。
46. Visual Provider ABI contract PASS。
47. reference physical provider E2E。
48. reference visual projection E2E。
49. multi-perspective privacy/knowledge isolation。
50. visual/physical output 不可直接写 reality。

## Product / Release
51. Browser Experience/Studio E2E。
52. security/private source/UGC package scan PASS。
53. v5.4 critical regression PASS。
54. full Python/TS quality PASS。
55. clean-clone PASS。
56. remote SHA == local HEAD。
57. GitHub required Actions success。
58. working tree clean。
59. final evidence 把 IMPLEMENTED / EXPERIMENTAL / RESEARCH_NOT_PROVEN 分开。
60. 仅上述 Gate ACCEPTED 才创建 annotated `v5.5.0-rc1` + GitHub prerelease；否则保持 NOT_ACCEPTED 并 STOP。
