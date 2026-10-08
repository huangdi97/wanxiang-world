# G91F — Quest Projection Adapter

Date: 2026-08-26  
Status: PASS

## Result

`QuestProjectionAdapter` provides an optional task/quest view over an existing
Opportunity. Required objectives are derived from the Opportunity's explicit
completion-evidence refs; optional objectives can be supplied by the
experience layer. Progress is computed only from `CommittedStateEvidence`
state/event refs. Narrative text is rejected as a progress source.

The resulting `QuestProjection` is explicitly `projection_only`, preserves
Opportunity status and refs, and has no commit/write path. An ignored
Opportunity remains ignored even when its evidence refs are present.

## Evidence

- `tests/unit/substrate/test_g91f_quest_projection.py`: 3 passed.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91F is complete and committed. M88 Gates 19-20 remain pending until G91H
qualification; G91G is next and v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`.
No model training or v5.6 work was performed.
