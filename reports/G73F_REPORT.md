# G73F Report — public feature branch and real GitHub Actions

**PASS (2026-08-25)**

The M51-M70 continuation was pushed to the existing public repository on the
feature branch requested for this execution. The first remote run exposed a
real cross-platform architecture-test defect; it was repaired and the second
remote run completed green.

| Gate | Result | Evidence |
|---|---|---|
| Public remote / branch | PASS | `origin` = `huangdi97/wanxiang-world`; `feature/source-to-living-world` pushed |
| Initial remote run | FAIL, repaired | run `32770711648` at `cc059cc`; Python had 1199 passed / 1 skipped and two duplicate-scan failures |
| Root cause | FIXED | `Path.rglob()` order differed between Windows and Ubuntu for an allowlisted `AssetGenerator` pair |
| Repair commit | PASS | `b2e8fa8`; duplicate scan sorts relative paths before allowlist comparison |
| Final remote CI | PASS | run `32771663283` at `b2e8fa8bbf882de8527a9d3dd28671e7cdfd9e64`; overall conclusion `success` |
| Repository safety | PASS | job `97573165514` |
| Python quality / kernel | PASS | job `97573165388`; lint, format, Pyright, 1201-test SQLite regression, quality, kernel guard |
| PostgreSQL service | PASS | job `97573165548`; migration + integration profile |
| API / package / SDK | PASS | job `97573165279`; generated-artifact drift clean |
| TypeScript SDK | PASS | job `97573165508`; lint, typecheck, test, build |
| Release smoke | PASS | job `97573165775`; release manifest + clean-room certification |

The only annotations were GitHub runner notices that actions currently target
deprecated Node.js 20 and are being forced to Node.js 24; they did not affect
job conclusions. The branch contains no copyrighted book bytes, family-private
records, credentials, provider/model artifacts, or training output.

This is a real CI qualification of the committed reference implementation,
not a claim that external rights, OCR providers, live production capacity, or
model training have been supplied.
