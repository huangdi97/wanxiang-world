# G91B — Opportunity / Challenge

Date: 2026-08-26  
Status: PASS

## Result

The existing `reality.challenge.Opportunity` now has an immutable,
schema-versioned lifecycle. Explicit eligibility can require an actor and
world-state refs; availability and expiry are tick-bounded; reward, risk,
completion-evidence, and world-state refs remain attached to the proposal.
`OpportunityLifecycle` returns new records for eligible, offered, accepted,
ignored, declined, expired, and completed transitions.

Ignoring an opportunity is a valid terminal decision. No lifecycle object has a
commit method, no transition writes an actor goal, and no transition mutates
the existing world or event history. Completion requires the declared evidence
refs rather than narrative text.

## Evidence

- `tests/unit/substrate/test_g91b_opportunity.py`: 3 passed.
- Existing G07C challenge/director/experiment regression remains green.
- `uv run ruff check`, format check, and `uv run pyright` on the changed
  implementation/tests: PASS.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91B is complete and committed. M88 Gate 19 remains pending until G91H
exercises ignore through a real playable world; v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`. No model training or v5.6 work was performed.
