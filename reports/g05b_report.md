# Goal G05B Acceptance Report
## Status
PASS
## Objective
Sessions, controller identity and embodiment leases with one primary controller
per actor.
## Delivered
- `wanxiang_substrate.session`: Session, EmbodimentLease, SessionService,
  LeaseService (acquire/renew/release/expire; one primary per actor).
## Test evidence
- unit/integration: one-primary enforcement, observe-mode blocked, release frees
  actor, expire releases controller.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Exactly one primary controller per actor | PASS | LeaseConflict tests |
| Lease lifecycle explicit | PASS | renew/release/expire tests |
| Sessions do not duplicate actor state | PASS | model review |
## External blockers
None.
## Final checkpoint
- commit: `goal g05b: session, embodiment & lease`