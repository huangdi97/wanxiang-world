# M68 — Minimal Human Review / Active Review Studio Qualification

## Required Goals

- G71A PASS
- G71B PASS
- G71C PASS
- G71D PASS
- G71E PASS
- G71F PASS
- G71G PASS
- G71H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M68_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。
