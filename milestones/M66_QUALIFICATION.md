# M66 — Worldness Validation & Simulation Closure Qualification

## Required Goals

- G69A PASS
- G69B PASS
- G69C PASS
- G69D PASS
- G69E PASS
- G69F PASS
- G69G PASS
- G69H PASS

## Qualification

- 运行本 milestone 相关 unit/contract/integration/security/migration/architecture tests。
- 运行所有受影响的既有 regression。
- 检查 schema/version/migration。
- 检查没有第二套 authority/registry/package/state。
- 检查 no-API reference path（适用时）。
- 检查 Source/Evidence/Rights 负向测试（适用时）。
- 生成 `reports/M66_QUALIFICATION.md`。

FAIL 必须修复后再继续；PASS 自动进入下一 Milestone，不询问用户。
