# Goal G18G Acceptance Report — Learn / Challenge Experience Completion

## Status
PASS

## Objective
Complete learning/challenge product flows using LearnerState, PracticeRecord, AssessmentEvidence, capability progression and Opportunity/Challenge runtime rather than isolated quizzes.

## Delivered
- `apps/api/src/wanxiang_api/learn_service.py` — challenge discovery, practice/assessment with capability deltas, biography.
- `tests/integration/test_g18g_learn_challenge.py` — 3 tests.
- `reports/LEARN_CHALLENGE_QUALIFICATION.md`, `reports/G18G_REPORT.md`.

## Findings
- Learning evidence is traceable (evidence_refs provenance); capability changes are separated from persona.
- Challenges affect the world through the normal action/commit path.

## Evidence
- 3 tests passed; ruff/pyright clean; architecture guard PASS.

## Remaining limitations
- A live React learn renderer is EXTERNAL_BLOCKED; the evidence-aware service contract is qualified.

## Final checkpoint
- commit: `g18g: learn / challenge experience completion`
