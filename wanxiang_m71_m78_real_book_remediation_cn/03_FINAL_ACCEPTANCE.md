# Final Acceptance — M71–M78

以下全部满足才允许判定 ACCEPTED：

1. real book parse/segment 非空；
2. distillation batches 非空且可追踪；
3. no-key 模式不静默 0 candidate 假成功；
4. 无 provider 时显式 `SEMANTIC_PROVIDER_REQUIRED`；
5. 有合法 provider 时 candidate_count > 0；
6. Character/Place/Event/Relation 至少形成真实候选，或逐类给出可验证的不适用理由；
7. accepted Candidate 可回 Source Locator；
8. cross-chapter entity merge 可撤销；
9. rights 已拆成不同 gate；
10. external-model processing 权限单独可控；
11. review inbox/audit 对真实候选有效；
12. coverage 来源于真实数据；
13. empty Draft 不生成 misleading Scenario；
14. job 失败有 terminal state/error/checkpoint；
15. expected domain state 不用 HTTP 500；
16. WorldPackage 真实生成；
17. Preview 真实生成；
18. Worldness 有真实 dimensions/measurements/evidence；
19. Worldness 不使用默认常量冒充；
20. repair/re-evaluate loop 可执行；
21. Living World Instance 真实生成；
22. instance/branch/snapshot/event head 可查；
23. 至少一项 action 完成 propose→validate→commit；
24. replay proof PASS；
25. branch 不污染 World Definition；
26. CLI lifecycle 完整；
27. API lifecycle 完整；
28. Browser Studio 可启动并走核心流程；
29. 真实网络 socket smoke 在可配置端口通过；
30. 原始书未修改；
31. 原始书未进入 Git；
32. 小说文本始终 data channel；
33. 未训练自有模型；
34. Provider 无 Commit authority；
35. 原有 1201+ 与新增 tests 全绿；
36. GitHub required Actions completed/success；
37. remote SHA == local HEAD；
38. working tree clean；
39. 新的 Real Book Acceptance 报告结论为 `ACCEPTED`；
40. 只有 39 成立才允许创建 `v5.4.0-rc2`。
