# G53I — GitHub Actions CI / Code Quality / Supply-chain 自动化

> Milestone：M50

## Objective

在创建远端前把可执行 CI workflow 写好并尽可能本地验证。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 创建主 CI workflow，覆盖 Python lint/format/type/test、Kernel/Replay/Lineage contracts、integration/migrations、Web lint/type/test/build、E2E smoke、packaging（按仓库真实能力）。
2. 配置最小 workflow permissions。
3. 如适用增加 CodeQL。
4. 如适用增加 Dependabot 配置。
5. 创建 tag/release workflow，但不得自动发布 PyPI/npm。
6. 验证 YAML、脚本和 CI commands 在本地等价执行 PASS。

## Tests / Verification

- 所有 workflow 配置语法可验证。
- 本地执行 CI 对应命令全部 PASS。
- 核心 CI 无外部 LLM key 依赖。
- fork PR 不获得不必要 write/secrets。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53I_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
