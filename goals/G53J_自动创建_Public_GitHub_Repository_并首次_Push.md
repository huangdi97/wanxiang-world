# G53J — 自动创建 Public GitHub Repository 并首次 Push

> Milestone：M50

## Objective

在所有本地工程/开源门通过后，从现有本地 Git 仓库自动创建公开 GitHub 仓库并推送。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 检查 gh auth status、git remote、current branch。
2. 优先仓库名 wanxiang-world；冲突则使用允许的 fallback，绝不覆盖现有仓库。
3. 使用当前 Git history 创建 public repo，不重新生成一个无历史项目。
4. 设置 origin。
5. 推送 main/stable branch 与 feature/wanxiang-v5.3-multiverse（存在时）。
6. 设置 description/topics（权限支持时）。
7. 记录 repository URL、default branch、remote SHA。

## Tests / Verification

- GitHub repository visibility=PUBLIC。
- 远端可读取最终公开 commit。
- 本地/远端 SHA 对应。
- Git remote 配置正确。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53J_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
