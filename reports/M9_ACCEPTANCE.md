# M9 Acceptance ? Release-qualified Wanxiang Platform Foundation

## Verdict
PASS

## Scope
P9 (G12A?G12H) delivered on top of verified M1-M8. Complete release
qualification: long-run stability, backup/restore/migration, SDK/OpenAPI/TS
generation, research/projection/foundry/gateway adapters, and local/private
deployment security checks.

## Mandatory scenario (proofs)
| Proof | Status | Evidence |
|---|---|---|
| 30 in-world days + 1000+ commit/scheduler cycles, bounded growth | PASS | test_g12a_stability |
| Backup restored into clean env reproduces canonical hashes; migrations replay | PASS | test_g12b_backup |
| OpenAPI/TS SDK generation reproducible; API vocabulary/version policy documented | PASS | openapi.ts + packages.sdk + 21 TS tests |
| Gym/PettingZoo adapters preserve authority + epistemic filtering | PASS | research tests |
| Godot/Babylon/Asset Foundry/Digital Human remain non-authoritative | PASS | contracts + tests |
| Rights prevent unauthorized asset/voice/face generation | PASS | gateway rights tests |
| Security: secrets/uploads/injection/admin/audit | PASS | test_g12h_security |
| Fresh-clone startup/runbook; external-only env checks explicitly labeled | PASS | docs/RELEASE_READINESS + EXTERNAL_BLOCKED labels |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1-M8 milestone gates | PASS | full suite (385 Python + 21 TS tests) |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | full suite |
| Rights/projection leakage | PASS | full suite |
| No-LLM deterministic profile | PASS | full suite |
| Lint/typecheck/build | PASS | ruff/pyright + tsc/eslint/vitest |
| TODO/placeholder + secret scan | PASS | architecture guard |

## EXTERNAL_BLOCKED items
- Real Red Chamber / Liaoshen data, real IIIF endpoints, Gymnasium/PettingZoo
  optional packages, React/Phaser/Godot/Babylon renderers, Docker/PostgreSQL/
  browser environment checks: all labeled EXTERNAL_BLOCKED with interfaces,
  fakes, negative gates and local behavior complete.

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed (385 tests).
- `packages/sdk_ts`: tsc --noEmit, eslint, vitest 21 passed.
- Checkpoint commit: `m9: qualify milestone`
- Milestone tag: `m9-release-qualified`