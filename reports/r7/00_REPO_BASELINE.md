# R7 00 — Repository Baseline (read-only verification)

Captured 2026-09-25 before any R7 implementation work. Every value below is a
verbatim command result, not a summary of documentation.

## Repository identity

```text
git rev-parse --show-toplevel   E:/AI/wanxiang
git branch --show-current       feature/r7-cordis-native (created from release/v5.5-stable-certification)
git rev-parse HEAD              48b3402242264f320070499319050286f5cca4f6
git status --short              (empty)
git remote -v                   origin https://github.com/huangdi97/wanxiang-world.git (fetch/push)
```

Recent history at capture time:

```text
48b3402 goal m95r: close Gate 79 on real evidence and record the honest Stable state
a9be096 fix(m100): let clean_room see its own runner's in-flight evidence
f2932a4 fix(m100): decode child process output as UTF-8 in the evidence runners
ce64ba4 fix(m100): actually execute the TypeScript gates in the local evidence runners
5b38d56 fix(m100): make the Gate 79 required-CI predicate satisfiable and derived
946fdbb docs(r7): track R7 execution entry documents
```

## Tags and releases

Local newest tags: `v5.5.0-rc1`, `v5.4.0`, `v5.4.0-rc2`, `v5.4.0-rc1`, then the
M-series tags. `git ls-remote --tags origin` shows the same published set.

* `v5.4.0` — Stable, published, unchanged.
* `v5.5.0-rc1` — GitHub prerelease, unchanged.
* `v5.5.0` — **does not exist**, locally or on the remote.

## Remote CI

Workflow `.github/workflows/ci.yml`, six required jobs: `safety`, `python`,
`postgres`, `api-sdk`, `ts`, `release-smoke`. Display names differ from job ids
for `safety`, `postgres` and `release-smoke`; the Gate 79 predicate now derives
both from the workflow file.

Verified runs on `release/v5.5-stable-certification`:

| Run | SHA | Result |
|---|---|---|
| 36133534654 | `946fdbb` | success, all six jobs green |
| 36194471592 | `a9be096` | success, all six jobs green |
| 36196736517 | `48b3402` | success, all six jobs green |

## v5.5 Stable gate state at capture time

Evidence-derived by `scripts/m100_stable_gate_aggregate.py`
(`artifacts/v55_stable/m100/stable_gate_aggregate.json`, ledger consistency
`PASS`):

| Gate | Status |
|---|---|
| 61 | PASS |
| 62–66 | USER_INPUT_REQUIRED (`WAITING_HUMAN`, no genuine human evidence) |
| 67–77 | PASS |
| 78 | EXTERNAL_BLOCKED (no supported Godot executable on this host) |
| 79 | PASS (regression, semantic/safety, exact-SHA clean clone, remote CI) |
| 80 | LOCKED (`blocking_gates = 62,63,64,65,66`; no `v5.5.0` tag) |

`Gates 62–66` require a real tester to complete
`reports/M95_PLAYER_TEST_PACKET_ZH_CN.md`; no human value is invented here.

## Toolchain on this host

```text
python 3.13.14 (uv 0.9.18)      node v22.15.0      pnpm on PATH via %APPDATA%\npm\pnpm.cmd
```

TypeScript tooling runs through pnpm; the evidence runners resolve `pnpm` via
`shutil.which` so the Windows `.cmd` shim is actually executed.

## What R7 must not assume

Per the design master, none of the following existed in the repository at
capture time, and this baseline finds no evidence otherwise:

```text
Cordis runtime or any composition host
RealityProfile / WorldProfile / RuntimeLock
versioned service seams
CommitCapability / monotonic guard
Execution Fabric / untrusted extension host
DSH bridge
Capability Foundry
shadow-replay profile migration
```

`reports/r7/` and `artifacts/r7/` did not exist. R7 is implemented from this
baseline forward, and every R7 claim in later reports must point at a
reproducible command or artifact.
