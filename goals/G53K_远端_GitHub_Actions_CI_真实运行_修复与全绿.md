# G53K — 远端 GitHub Actions CI 真实运行、修复与全绿

> Milestone：M50

## Objective

把远端 CI run 本身作为正式 Acceptance，而不是只确认 workflow 文件已提交。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 使用 gh run list/view 查询刚 push 触发的 workflow。
2. 等待核心 CI workflow 完成。
3. 若失败，获取失败 job/log，定位真实原因。
4. 修复代码/workflow，运行本地验证，commit + push。
5. 重复直到所有 required/core workflows PASS。
6. 生成 GITHUB_CI_REPORT，记录 run IDs/URLs/SHA/失败与修复历史。

## Tests / Verification

- 最终 commit 对应的核心 CI conclusion=success。
- 无通过取消/disable workflow/删除测试制造的假绿。
- 远端 CI 与本地认证 commit 对应。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53K_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
