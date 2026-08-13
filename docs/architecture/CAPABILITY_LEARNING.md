# Capability & Learning (G03G)

Ownership: `wanxiang_substrate.capability` (bounded capability change from
evidence, connected to skill prerequisites).

## Model

- `CapabilityState`: bounded measurement per (actor, capability): level 0..10,
  mastery 0..1, confidence 0..1, with evidence provenance and an updated
  revision counter.
- `PracticeRecord` / `AssessmentEvidence`: declared practice/assessment records
  with a required evidence ref; assessment types are a fixed supported set
  (`practical`, `theoretical`, `performance`) and outcomes are `pass`/`fail`.
- `CapabilityDelta`: evidence-backed bounded change (level/mastery/confidence
  deltas) with a reason; a no-op delta is rejected.
- `LearnerState`: read-model aggregate with capabilities, record counts and the
  ordered learning biography.

## Policy

`LearningPolicy` is a pure deterministic reference policy:
- practice maps to bounded level gain (`practice_count // 3`) plus small
  mastery/confidence gains;
- a passing assessment raises mastery/confidence; a failing assessment causes a
  small bounded regression;
- `apply` clamps every value to the declared scale and merges evidence refs
  (sorted), so capability never leaves its bounds and never loses provenance.

## Commit path

All capability changes go through resolvers (`capability.record_practice`,
`capability.record_assessment`, `capability.apply_delta`) that produce
`ProposedWorldDelta`; Commit Authority persists them as ordered events.
A direct delta without evidence is rejected (`EvidenceRequired`), and an
unsupported assessment type cannot create mastery (`UnsupportedAssessment`).

## Skill integration

Skill steps may declare `requires_capability="<name>[:<min_level>]"`;
`SkillRuntime` checks the actor's capability via `CapabilityQuery.requires`
before submitting the step. Missing capability marks the skill instance
`failed` with `SkillPrerequisiteError` and never commits the step.

## Separation of concerns

- Capability is separate from knowledge (epistemic) and persona: no capability
  update rewrites actor identity or knowledge.
- Practice/assessment records are entities; the learning biography is a derived
  read-model; replay reconstructs identical capability state.