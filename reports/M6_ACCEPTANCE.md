# M6 Acceptance ? Reality-Coupled Context and Controlled Experiments Work Safely

## Verdict
PASS

## Scope
P6 (G07A?G07E) delivered on top of verified M1-M5. The mandatory scenario ran
over real internal paths (bridge + fusion + challenge + director + experiment +
world commit).

## Mandatory scenario (tests/integration/test_m6_qualification.py)
1. Deterministic fake physical observations (duplicates + conflicts) are fed
   into the Reality Bridge.
2. Fusion deduplicates consistent inputs and retains conflicts as a conflict
   set with provenance; outputs are claims/proposals only.
3. An opportunity is detected and compiled into a ChallengeSpec with
   prerequisites, safety/rights/evidence requirements and verifiable end
   conditions.
4. A WorldDirector proposes an external event; the proposal traverses normal
   validation/commit and becomes a committed event (no direct director commit).
5. A multi-seed experiment runs from the fixed baseline; the same spec
   reproduces identical results; the baseline hash is unchanged; findings carry
   assumptions and a ValidityEnvelope.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| PhysicalObservation remains observation, never direct truth | PASS | bridge readings are bus data with provenance |
| Fusion preserves conflicting inputs/provenance; claims/proposals only | PASS | conflict-set test + outcome tests |
| ChallengeSpec includes prerequisites, safety/rights/evidence, outcomes | PASS | spec test + vertical |
| Director layers cannot directly commit or rewrite actors | PASS | no-commit + DirectorReview tests |
| Experiment branches never mutate baseline | PASS | baseline hash-stable test |
| Results include run/seed/version metrics, assumptions, ValidityEnvelope | PASS | finding + envelope tests |
| Same deterministic spec reproduces same result set | PASS | determinism test |
| Proposals traverse normal validation/adjudication/commit | PASS | vertical director->commit |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1 commit/event/replay/branch/idempotency/stale-revision | PASS | full suite |
| M2 72h living-world | PASS | full suite |
| M3 bounded-agent vertical | PASS | full suite |
| M4 author/install/instantiate vertical | PASS | full suite |
| M5 hosted world + lifecycle/recovery | PASS | full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | full suite |
| Rights/projection leakage | PASS | full suite |
| No-LLM deterministic profile | PASS | full suite |
| Lint/typecheck | PASS | ruff + pyright clean |

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed (349 tests).
- Checkpoint commit: `m6: qualify milestone`
- Milestone tag: `m6-reality-experiments`