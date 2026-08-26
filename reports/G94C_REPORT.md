# G94C — Habit / Skill Candidate

Date: 2026-08-27  
Milestone: M91  
Status: **PASS**

## Delivered scope

`HabitCandidate`/`SkillCandidate` records are actor-local, immutable candidate
views created only from a qualified `PatternDetection`. They retain the
detector id, pattern key, evidence window, committed event refs, occurrence and
window counts, support, stability, and base/decayed confidence. A
`HabitPromotionPolicy` supplies explicit floors for evidence, stability,
confidence, and maximum age; `HabitEvaluation` reports reasons without
performing a promotion or canonical write.

Decay is deterministic, bounded, and computed from elapsed evidence windows.
Repeated evaluation does not compound decay against an already-decayed value;
the candidate retains its original detector confidence. Unqualified patterns,
wrong actors, insufficient evidence, and stale/low-confidence candidates are
rejected or remain ineligible rather than becoming automatic truth.

## Evidence

- Unit tests: `tests/unit/substrate/test_g94c_habit_candidate.py` — 2 passed.
  They cover eligible habit/skill candidates, event provenance, stability,
  non-compounding decay, unqualified/wrong-actor/early guards, and policy
  evaluation.
- Integration test:
  `tests/integration/test_g94c_habit_candidate_product_chain.py` — 1 passed.
  A private rights-approved source traversed
  `OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime`; repeated committed actor actions formed a skill candidate and
  evaluation while canonical hash and replay remained unchanged.
- Focused quality: `3 passed, 1 warning`; Ruff, format, and target Pyright
  passed.
- M91 minimality now records 10 bounded abstractions across the observation,
  detector, and candidate layers. No second history, registry, runtime, or
  Commit Authority was introduced.

## Acceptance boundary

G94C proves candidate evidence-window/stability/decay behavior only. It does
not claim automatic skill truth, social norms, institutions, culture,
universal emergence, or a v5.5 release. G94D-G94H and later M92-M94 gates
remain required.

## Commit

Required commit: `g94c: Habit / Skill Candidate`.
