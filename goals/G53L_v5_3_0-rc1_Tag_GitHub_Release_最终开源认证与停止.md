# G53L — v5.3.0-rc1 Tag、GitHub Release、最终开源认证与停止

> Milestone：M50

## Objective

在远端 CI 全绿后发布 RC tag/release，并完成最终交付证明。

## Required Reading

- `11_OPEN_SOURCE_GITHUB_CI_POLICY.md`
- `12_GITHUB_ACTIONS_CI_SPEC.md`
- `06_FINAL_RELEASE_EVIDENCE.md`
- `02_GITHUB_DELIVERY_POLICY.md`
- M50 前序 Goal reports
- 当前 `.github/`、README、LICENSE、gitignore、Git history、tracked files、remote/auth 状态

## Implementation Tasks

1. 重新确认 final certification 与 working tree clean。
2. 创建 annotated tag v5.3.0-rc1（若名称未被占用且指向当前认证 commit）。
3. push tag。
4. 触发并验证 release workflow。
5. 使用 gh release create 或等价方式创建 GitHub Release Candidate，附 release notes；只上传可公开 artifacts。
6. 记录 repo URL、tag、release URL、final SHA、CI run URLs。
7. 更新 STATUS/PLAN/CHANGELOG，生成最终开源认证并停止；不开始 v5.4。

## Tests / Verification

- Tag 指向最终认证 SHA。
- Release 公开可见。
- Release workflow PASS。
- GITHUB_DELIVERY_REPORT 与 V5_3_FINAL_CERTIFICATION 完整。

## Acceptance

- 所有内部项有真实证据；不得用文件存在代替执行。
- 不提交 secret/private/restricted corpus。
- 不 force push。
- 更新 `reports/G53L_REPORT.md` 和 `reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md`。
- PASS 后本地 commit 并继续。
