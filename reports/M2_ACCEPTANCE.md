# M2 ? Deterministic Living World Exists

- Date: 2026-08-13
- Verdict: **PASS**
- Milestone gate: `milestones/M2_QUALIFICATION.md`
- Evidence: `tests/integration/test_m2_qualification.py` (72h integrated run), 212 tests green.

## Mandatory scenario

A source-neutral synthetic house/micro-town ran for **72 in-world hours** with
multiple actors, rooms/portals, schedules (world clock), material objects
(sealed letter), body constraints, duties/permissions and background population
scheduling ? with **no user input after instantiation**.

## Required proofs

| Requirement | Status | Evidence |
|---|---|---|
| World time monotonic; pause/advance without wall-clock | PASS | temporal substrate + scheduler advances to 72*DAY |
| Spatial reachability/access/capacity/occupancy invariants hold | PASS | post-run SpatialQuery checks |
| Material custody/container conserved; sealed message not read by holder | PASS | custody + payload sealed checks |
| Body/condition state blocks otherwise valid action | PASS | fatigued actor move rejected (BodyConstraintViolation) |
| Institution roles/duties/permissions affect allowed actions | PASS | member enters restricted study; non-member rejected |
| Scheduler advances deterministically under budgets | PASS | 72h run; peak_tick_events <= 8; budget tests |
| Snapshot/replay/branch/idempotency/stale-revision (M1) remain green | PASS | full suite includes M1 A1-A10 |
| Same initial snapshot + seed + versions -> identical final hash | PASS | scheduler determinism test |

## Regression

- `uv run python scripts/quality.py` -> PASS (lint, pyright 0 errors, pytest 212 passed, architecture conformance).
- M1 authoritative commit/event/replay/branch/idempotency/stale-revision suite: green.
- Architecture guards, migration/replay compatibility, no-LLM profile: green.
- File-size/cohesion/placeholder/secret scans: green.

## Milestone checkpoint

- Local annotated tag `m2-deterministic-living-world` created at PASS.
