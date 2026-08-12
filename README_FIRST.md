# Wanxiang M2→M9 Remaining Engineering Execution Pack

This package continues the previously completed M0/M1 batch.

## What this pack contains

- `05_CODEX_REMAINING_PROGRAM_MASTER_PROMPT.md` — continuous controller from G02A through G12H.
- `06_REMAINING_GOALS_INDEX.md` — exact order of all 55 remaining Goals.
- `07_MILESTONE_GATES_M2_M9.md` — summary of M2–M9 system qualification.
- `08_CONTINUOUS_EXECUTION_AND_RESUME_PROTOCOL.md` — recovery from context compaction/restart.
- `09_RELEASE_AND_QUALITY_CONSTITUTION_ADDENDUM.md` — maintainability/upgrade/security rules for later phases.
- `goals/` — 55 detailed executable Goal contracts.
- `milestones/` — 8 integrated milestone qualification contracts.
- `CODEX_COPY_PASTE_CONTINUE.txt` — the shortest startup message to give Codex.
- `WANXIANG_REMAINING_M2_M9_ALL_IN_ONE.md` — merged reference copy.
- `baseline_reference/` — copies of the earlier program standards and v5 master spec for reference; do not overwrite newer repository copies blindly.

## How to use

Copy/merge the new controller/index/protocol/Goal/milestone documents into the existing Wanxiang repository that already passed M1. Preserve the repository's existing ledgers, Git history and implementation.

Then start a new Codex Desktop conversation and paste the contents of `CODEX_COPY_PASTE_CONTINUE.txt`.

Codex must verify the actual M1 repository state first, then execute continuously through M9 with local checkpoints. It must not push/deploy without a separate instruction.
