# G95C — Fork / Intervention Runner

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

G95C adds an explicit fork/intervention evidence layer over the existing
authoritative `WorldRuntime.create_branch` operation. A fork records the
parent head revision/event count/hash, the selected fork revision/event
sequence, the runtime-created fork snapshot reference, child branch, trigger,
and linked artifact. Event triggers resolve only against a committed event in
the parent history; time triggers remain explicit metadata. The intervention
itself remains a proposal and never becomes a second commit path.

`InterventionLedger` is schema-versioned, thread-safe, append-only evidence.
`ForkInterventionRunner.resume` resumes only the child branch and verifies its
current state against authoritative replay before appending a resume record.
Parent event history and canonical hash remain unchanged.

## Evidence

- Unit: `tests/unit/substrate/test_g95c_fork_intervention_runner.py` — 2
  passed, including immutable ledger entries and contiguous snapshot
  round-trip.
- Integration: `tests/integration/test_g95c_fork_intervention_runner_product_chain.py`
  — 1 passed through private rights-approved source → OneClickAuthoring →
  WorldPackage → Preview → PlayableService → SQLite WorldRuntime. Explicit
  event and snapshot-revision forks, child commit, parent isolation, and
  replay-verified resume all passed.
- Regression: existing G91E/G91H intervention and playable qualification
  tests passed.
- Full quality: 1398 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  architecture, SDK compatibility, duplicate-abstraction, and minimality
  checks pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED
  profile.

## Boundary

The runner delegates branch creation to the existing runtime and does not own
canonical state, event history, branch persistence, or Commit Authority. No
source bytes or model-training path is introduced. Gate 40 is accepted;
G95D-G97J and the remaining M92-M94 gates remain pending, so v5.5 remains
NOT_ACCEPTED.
