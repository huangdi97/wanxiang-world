# M50 — Release Qualification + Public GitHub + Remote CI

## Required Goals

- G53A PASS — `G53A_v5.3_Backward_Compatibility_Full_Regression.md`
- G53B PASS — `G53B_Multi-world_30-day_Stability.md`
- G53C PASS — `G53C_Security_Rights_Interworld_Isolation_Final.md`
- G53D PASS — `G53D_SDK_Docs_Examples_v5.3.md`
- G53E PASS — `G53E_Release_Notes_Migration_Guide.md`
- G53F PASS — `G53F_Final_Acceptance_Matrix_Certification.md`
- G53G PASS — Open-source Readiness 与公开历史安全审计
- G53H PASS — 开源治理、License、README 与贡献者入口
- G53I PASS — GitHub Actions CI / Code Quality / Supply-chain 自动化
- G53J PASS — 自动创建 Public GitHub Repository 并首次 Push
- G53K PASS — 远端 GitHub Actions CI 真实运行、修复与全绿
- G53L PASS — v5.3.0-rc1 Tag、GitHub Release、最终开源认证与停止

## Final Gate

M50 只有在以下条件全部满足时才 PASS：

1. v5.3 内部 final certification PASS；
2. Open-source Readiness PASS；
3. Public GitHub repository 已创建；
4. final commit 已 push；
5. GitHub Actions 核心 CI 在远端对 final commit 实际 PASS；
6. v5.3.0-rc1 tag/release 成功，或 GitHub 权限/服务明确 EXTERNAL_BLOCKED；
7. 不存在 secret/private/restricted corpus 泄漏；
8. reports/GITHUB_DELIVERY_REPORT.md 和 reports/GITHUB_CI_REPORT.md 完整。

如果 GitHub auth/permission/service 客观阻塞，可标 GITHUB_DELIVERY=EXTERNAL_BLOCKED，但不得把 M50 伪装成“远端发布完成”。
