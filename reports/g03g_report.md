# Goal G03G Acceptance Report

## Status
PASS

## Pre-goal state
- branch: master
- commit: 6006fd2 (G03F checkpoint)
- working-tree notes: clean before G03G work

## Objective
Model bounded capability change from practice/evidence and connect it to skills
without conflating personality or knowledge with capability.

## Delivered
- `wanxiang_substrate.capability`: CapabilityState/PracticeRecord/
  AssessmentEvidence/CapabilityDelta/LearnerState model, versioned
  `capability.state` component + practice/assessment record components,
  deterministic LearningPolicy (bounded, clamped, evidence-merged), pure
  CapabilityQuery, and resolvers (`capability.record_practice`,
  `capability.record_assessment`, `capability.apply_delta`) through the M1
  authority.
- Skill integration: `SkillRuntime._check_step_capability` rejects steps whose
  declared `requires_capability="name:min_level"` is unmet before commit.
- M3 vertical: `tests/integration/test_m3_qualification.py` (observation ->
  belief -> correction -> multi-step skill -> bounded capability change, with
  knowledge isolation).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run python scripts/quality.py` (full gate) | 265 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests (`tests/integration/test_capability_learning.py`, 9 tests):
- unit: bounded practice -> level gain with accumulated evidence;
- unit: passing assessment raises mastery/confidence, not level;
- negative: unsupported assessment cannot create mastery (state unchanged);
- negative: direct delta without evidence is rejected;
- unit: LearnerState aggregate + biography ordering;
- property: capability stays within declared scale/invariants under many
  updates;
- integration: learning biography reconstructs (replay hash equality);
- integration: skill step with `requires_capability` is rejected until the
  capability is earned, then executes;
- unit: policy clamps regression to the scale floor.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard + review |
| Goal + regression tests PASS | PASS | 265 tests incl. M1/M2/G03A-F |
| Lint/type/architecture PASS | PASS | full quality gate |
| Schema change has migration/compat test | NOT_APPLICABLE | versioned components, no new table |
| Canonical mutation via Validate/Resolve/Commit | PASS | resolvers produce deltas only; replay stable |
| Skill prerequisites integrated | PASS | skill step capability gate test |
| No new forbidden dependency | PASS | architecture guard |

## Key decisions
- Capability is a bounded measurement separate from knowledge/persona;
  evidence-backed deltas only (ADR-0024).

## Known limitations
- Only deterministic reference learning policy; adaptive/LLM-based learning is
  a replaceable future port.

## External blockers
None.

## Final checkpoint
- commit: `goal g03g: capability & learning`