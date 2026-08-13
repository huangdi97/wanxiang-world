# M5 Acceptance ? Human Can Enter a Persistent World Without Becoming the Authority

## Verdict
PASS

## Scope
P5 (G05A?G05F + G06A?G06C) delivered on top of verified M1-M4. The mandatory
hosted-world scenario ran over real internal paths (host + sessions + leases +
handoff + projections + lifecycle + command queue + recovery + SQLite restart
replay).

## Mandatory scenario (tests/integration/test_m5_qualification.py)
1. Hosted synthetic world with Studio and Phaser sessions.
2. Studio session acquires an embodiment lease on Alice; ControlHandoff takes
   over the actor (human_control).
3. The human commits a spatial move through the command API; it becomes normal
   world history.
4. Shadow can only advise; committing raises ShadowCannotCommit.
5. Control is released; the deterministic controller resumes (autonomous) with
   a resume ref; no active lease remains.
6. All clients disconnect (host registry shutdown) while the world continues.
7. The process restarts on the same SQLite DB: replay of persisted events
   reproduces the identical canonical semantic hash.
8. A reconnected Phaser session reconstructs the view from a fresh server
   projection at the same revision.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| WorldHost is orchestration, not a second Commit Authority | PASS | host submits -> authority; no direct mutation |
| Exactly one primary embodiment controller per actor | PASS | LeaseConflict tests |
| ShadowPolicy cannot compete for authoritative body control | PASS | ShadowCannotCommit + handoff tests |
| Projection filters enforce knowledge/rights server-side | PASS | projection filter tests |
| Studio/Phaser use command APIs; local state not canonical truth | PASS | TS client submit tests + design |
| Lifecycle modes persist independently of sessions | PASS | G06A: lifecycle entity persists; test_m5_g06_proofs restart restores mode |
| Multi-client retries/conflicts idempotent + revision-safe | PASS | G06B: command queue dedup/conflict; M1 idempotency regression |
| Crash/lease recovery + scheduler restoration preserve hash | PASS | G06C: RecoveryService + test_m5_g06_proofs restart replay hash |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1 commit/event/replay/branch/idempotency/stale-revision | PASS | full suite |
| M2 72h living-world | PASS | full suite |
| M3 bounded-agent vertical | PASS | full suite |
| M4 author/install/instantiate vertical | PASS | full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | full suite |
| Rights/projection leakage | PASS | projection + source/observation tests |
| No-LLM deterministic profile | PASS | full suite |
| Lint/typecheck (Python + TS) | PASS | ruff/pyright + tsc/eslint/vitest |
| TODO/placeholder + secret scan | PASS | architecture guard |

## EXTERNAL_BLOCKED items
- React Studio rendering app and Phaser canvas rendering: EXTERNAL_BLOCKED
  (no network to install React/Vite/Phaser; no browser in this environment).
  The typed view models + Vitest deterministic tests are committed as the
  renderer contract (G05E/G05F reports).

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed (335 tests).
- `packages/sdk_ts`: tsc --noEmit, eslint, vitest 14 passed.
- G06 proofs: `tests/integration/test_m5_g06_proofs.py` (lifecycle persistence,
  multi-client queue idempotency/conflict, crash-restart hash, budget).
- Checkpoint commit: `m5: re-qualify with lifecycle & recovery`
- Milestone tag: `m5-human-in-world-without-authority` (moved to final M5 commit)