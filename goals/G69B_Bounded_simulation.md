# G69B — Bounded simulation

Milestone: **M66 — Worldness Validation & Simulation Closure**

## Objective

7-day reference run；复杂 world 可 accelerated。

## Required Reading

- 本执行包 README / Roadmap / Architecture / Pipeline / Contracts / Acceptance
- 当前仓库 AGENTS.md、STATUS.md、PLAN.md、DECISIONS.md、BLOCKERS.md、KNOWN_FAILURES.md、CHANGELOG.md（存在则读）
- 当前 Git history、migrations、package schemas、OpenAPI、CI workflows
- M50/v5.3 与上一阶段实际 reports（存在则读）
- 当前 Goal 直接涉及的源码与测试


## Mandatory workflow

1. 先审计真实实现，不信任“之前说做完了”。
2. 对相关代码做 KEEP / EXTEND / MERGE / DELETE / ADD 判断。
3. 复用现有边界，禁止平行新系统。
4. 实现最小完整闭环，不用 TODO/placeholder/mock-only 冒充完成。
5. 增加 unit / contract / integration / negative / migration / architecture tests。
6. 涉及 UI 时增加 Playwright 或现有等价 E2E。
7. 涉及长任务时测试 checkpoint/resume/idempotency。
8. 涉及模型时必须有 no-API deterministic/reference path。
9. 更新 reports/G69B_REPORT.md 与总 acceptance matrix。
10. PASS 后 commit，然后自动进入下一个 Goal。

## Architecture constraints

- Kernel stable semantics 默认冻结。
- Source ≠ Claim ≠ Candidate ≠ Completion ≠ Canonical World State。
- WorldDraft 只是 Forge 编译产物。
- 模型/Agent/Parser/Studio 不拥有 Commit Authority。
- world/domain-specific 逻辑不得进入 Kernel。
- 真实版权文本、family 私密资料、token、数据库、模型缓存不得进入 Git。
- 内部工程问题不得标 EXTERNAL_BLOCKED。

## Acceptance

- 本 Goal 的行为有真实代码、测试、报告证据。
- 失败路径显式；不静默 fallback 成“成功”。
- backward compatibility 未被破坏，或有 migration + compatibility report。
- 工作树中无与本 Goal 无关的大规模 churn。
