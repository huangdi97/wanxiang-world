# Goal G07C Acceptance Report
## Status
PASS
## Objective
Opportunity / Challenge / Event compiler with executable specs.
## Delivered
- `wanxiang_substrate.reality.challenge`: Opportunity, ChallengeSpec
  (prerequisites/safety/rights/evidence/end conditions), deterministic
  OpportunityDetector, ChallengeCompiler.
## Test evidence
- detection from conditions; spec includes prerequisites/rights/outcomes.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Challenge includes prerequisites + outcome requirements | PASS | spec test |
| Domain-neutral composer port | PASS | detector protocol |
## Final checkpoint
- commit: `goal g07c: opportunity, challenge & event compiler`