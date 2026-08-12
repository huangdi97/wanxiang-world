# Continuous Execution and Resume Protocol

## Purpose

Codex may compact context, restart, or be interrupted during the 55-Goal continuation. Progress must be recoverable from repository state rather than chat memory.

## Authoritative resume state

On every start/resume, read in order:
1. `STATUS.md`
2. `PLAN.md`
3. `reports/ACCEPTANCE_MATRIX.md`
4. latest milestone acceptance report
5. latest Goal report
6. `git status`
7. `git log --oneline --decorate -n 30`
8. open blockers/known failures
9. current Goal file

Do not infer “where we were” from conversation memory.

## Status convention

Each Goal should be one of:
- NOT_STARTED
- ACTIVE
- PASS
- FAIL
- EXTERNAL_BLOCKED (only where Goal explicitly permits a real external slice)
- SUPERSEDED (only by documented ADR/spec change)

Each Milestone:
- NOT_STARTED
- QUALIFYING
- PASS
- FAIL

## Atomic progress

- A work-in-progress Goal may have intermediate local commits only if repository convention allows; the formal Goal checkpoint occurs after PASS.
- Never mark PASS before the evidence report is complete.
- If interrupted mid-Goal, leave `STATUS.md` ACTIVE and record remaining work in the Goal report or `PLAN.md`.
- On resume, rerun the current Goal's narrow regression before continuing.

## Context compaction

Before a long context compaction or tool restart, update:
- exact current Goal/work package;
- tests currently passing/failing;
- files changed;
- unresolved design decision;
- next executable step.

Repository documents are the memory boundary.

## Regression-first resume

If the last Goal is PASS:
- verify its acceptance command(s);
- if still green, start the next Goal;
- if not, repair the regression before advancing.

If the last milestone is PASS, do not rerun its full expensive long-run suite on every single Goal. Maintain a fast stable regression subset and rerun full milestone qualification at later milestones according to the acceptance standard.

## External blockers

A blocked real source/integration never becomes an invitation to fabricate. Record:
- exact missing file/credential/hardware/service;
- why it is necessary;
- which internal interface/fake/tests are complete;
- which acceptance line remains blocked;
- whether later independent Goals can continue.

## End condition

The controller stops after M9 final reports and local checkpoint. It must not push, deploy, or invent post-M9 work without a new user instruction.
