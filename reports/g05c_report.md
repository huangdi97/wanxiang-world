# Goal G05C Acceptance Report
## Status
PASS
## Objective
Human/Shadow policy control handoff; Shadow cannot compete for authoritative
body control.
## Delivered
- `wanxiang_substrate.session.control`: ControlHandoff state machine
  (autonomous -> human_control -> handing_back -> resuming_autonomous),
  ShadowPolicy advice-only channel.
## Test evidence
- handoff cycle test; shadow advice never changes control; shadow commit raises
  ShadowCannotCommit; resume ref preserved.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Shadow cannot choose canonical actions | PASS | ShadowCannotCommit test |
| Human commits are normal history | PASS | host+lease vertical |
| Deterministic controller resumes | PASS | handoff resume test |
## External blockers
None.
## Final checkpoint
- commit: `goal g05c: shadow & human policy control handoff`