# M3 Acceptance ? Bounded Agents Can Live Inside the World

## Verdict
PASS

## Scope
P3 (G03A?G03G) delivered on top of verified M1/M2. This gate ran the mandatory
deterministic synthetic scenario and the full regression suite.

## Mandatory scenario (tests/integration/test_m3_qualification.py)
Two actors (Alice, Bob) and one organization (courier guild):
1. Organization + membership exist; Alice is granted the `deliver` permission.
2. Alice learns `delivery` from declared practice evidence (6 practices ->
   level 2), before the skill gate allows her to run the courier skill.
3. Bob moves to the hub; Alice observes a private/partial movement event; the
   sealed letter payload never leaks into observations.
4. Alice adopts a private belief, then receives a correction; the temporal
   epistemic graph preserves the correction lineage (supersedes link, history
   length 2).
5. Bob never receives the private knowledge: no belief, no memory ref, no
   capability Alice earned.
6. Alice executes a multi-step courier skill (take -> move -> hand_over) whose
   steps require `delivery:2`; custody ends at the recipient and Alice arrives
   at the recipient house.
7. The completed run is recorded as evidence-backed practice: capability grows
   to level 3 and remains bounded.
8. ActionValidator rejects Bob reading the sealed letter payload he never
   observed (`no_knowledge`).
9. Replay of all events reconstructs the identical canonical state hash.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| Observation/belief/memory/canonical truth separate | PASS | vertical test steps 3-4; observation is derived, beliefs are `epistemic.belief` entities |
| Epistemic graph preserves contradiction/correction lineage | PASS | `belief_history` length 2, supersedes link |
| Actors/organizations propose through policies; no policy owns Commit Authority | PASS | all changes via commands; replay hash equal |
| Affordances/validator reject unreachable/unauthorized/epistemic-impossible | PASS | `no_knowledge` rejection of sealed payload read |
| Resolver adjudication provenance (version/seed) | PASS | G03E regression (seeded adjudication tests) green |
| Skill resumable; every step passes normal validation | PASS | courier skill 3 steps through authoritative path |
| Capability change requires evidence and stays bounded | PASS | practice/assessment gates + bounds assertion |
| Knowledge-leakage and deterministic policy tests pass | PASS | vertical + G03A/B/D regression green |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1 commit/event/replay/branch/idempotency/stale-revision | PASS | test_m1_acceptance.py in full suite |
| M2 72h living-world | PASS | test_m2_qualification.py in full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | persistence + migration tests green |
| Rights/projection leakage | PASS | observation/epistemic tests green |
| No-LLM deterministic profile | PASS | full suite has no LLM dependency |
| Lint/typecheck | PASS | ruff + pyright clean |
| TODO/placeholder scan + secret scan | PASS | architecture guard |

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed.
- 265 tests passed, 0 errors, architecture PASS.
- Checkpoint commit: `goal g03g: capability & learning`
- Milestone tag: `m3-bounded-agents`