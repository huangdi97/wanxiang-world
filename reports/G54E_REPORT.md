# G54E Report — Job/Resume Baseline (M51)

## Status
**PASS** — Unified Import/Authoring Job with checkpoint/resume/idempotency
established as the Forge execution baseline (reused by M52-M70 pipeline work).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/jobs/` (new):
   - `model.py` — `Job` (id/kind/source_refs/version/status/stage), `JobCheckpoint`
     (stage + JSON-safe payload), ordered `JOB_STAGES` (registered → published).
   - `errors.py` — typed `JobError` taxonomy.
   - `store.py` — `JobStore`: idempotent create by (kind, source_refs, version)
     fingerprint (duplicate retries never duplicate effects), validated status
     transitions (append-only history), atomic checkpoint publish with
     stage-monotonic guard + JSON-safety validation.
   - `service.py` — `JobService`: create/start/checkpoint/resume/finish/fail/
     cancel/status/history. Resume: running → latest checkpoint; created →
     auto-start; done → no-op.
2. `tests/unit/substrate/test_job_resume.py` — 11 unit tests.

## Reuse
- Reuses `wanxiang_domain.errors.WanxiangError`; does NOT create a second
  registry/snapshot store. Runtime-state checkpoints (G06C recovery) remain
  separate; job progress is a different concern (no overlap, no duplicate).

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_job_resume.py -q` | 11 passed |
| ruff check / format | PASS |
| pyright | 0 errors |

## Idempotency/resume guarantees
- Same (kind, source_refs, version) → same job; no duplicate side effects.
- Changed source version → new job (incremental re-import trigger).
- Crash during running → resume from latest checkpoint, never redoes completed
  stages.
- Done job resume is a no-op; terminal states are immutable.
- Checkpoints are atomic (visible only after all validation) and JSON-safe.

## Local commit
- `goal g54e: Job/resume baseline (M51)`
