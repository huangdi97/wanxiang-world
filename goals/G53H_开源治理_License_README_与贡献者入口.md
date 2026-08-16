# G53H — 开源治理、License、README 与贡献者入口

> Milestone：M50

## Objective

补齐真正开源项目需要的许可证、治理、说明和数据权利边界。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 若已有 LICENSE 则保留；若无则加入 Apache-2.0。
2. 完善 README 中文主入口与英文摘要/README_EN。
3. 创建/完善 CONTRIBUTING、CODE_OF_CONDUCT、SECURITY。
4. 创建 DATA_AND_ASSET_RIGHTS，明确代码与 corpus/assets 权利分离。
5. 补 Quickstart、Architecture、Package Authoring、Development Setup。
6. 确保 .env.example 只有占位符。

## Tests / Verification

- README 中所有核心 quickstart 命令在 clean environment 可执行。
- LICENSE/rights 文档不存在互相冲突声明。
- 不存在真实 credential。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53H_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
