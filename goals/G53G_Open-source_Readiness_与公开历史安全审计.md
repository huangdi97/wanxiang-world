# G53G — Open-source Readiness 与公开历史安全审计

> Milestone：M50

## Objective

把当前生产仓库变成可以安全公开的源码仓库，而不是直接 git add/push。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 盘点全部 tracked/untracked/ignored 文件与 Git history。
2. 扫描 secret/token/private key/credential。
3. 扫描 DB dump、个人数据、受限文学 corpus、博物馆受限资产、模型缓存和大文件。
4. 检查历史中是否曾提交不应公开内容；必要时在首次远端创建前安全清理本地 Git history，并保留本地备份引用。
5. 生成 OPEN_SOURCE_FILE_ALLOWLIST / DENYLIST 或等价机器可检查规则。
6. 确认所有公开示例数据的 rights metadata。

## Tests / Verification

- fresh git clone-equivalent export 不包含 denylist 内容。
- secret scan PASS。
- public tracked-file audit PASS。
- M42/M50 本地回归不因清理被破坏。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53G_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
