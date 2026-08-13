# ADR-0024: Capability & Learning Design (G03G)

- Status: accepted
- Date: 2026-08-13

## Context

G03G needs bounded capability change from practice/evidence, connected to skill
prerequisites, without conflating capability with knowledge or persona and
without a gamified score-only system.

## Decision

1. Capability is a bounded measurement per (actor, capability): level 0..10,
   mastery 0..1, confidence 0..1, persisted as a versioned `capability.state`
   component with evidence provenance.
2. All capability changes are `CapabilityDelta`s computed by a deterministic
   reference `LearningPolicy` from declared `PracticeRecord` /
   `AssessmentEvidence`; direct deltas require evidence refs.
3. Capability changes flow through resolvers -> ProposedWorldDelta -> Commit
   Authority; no second mutation path.
4. Skill steps may declare a required capability level; `SkillRuntime` rejects
   steps whose prerequisite is unmet before committing anything.
5. Unsupported assessment types and outcomes are rejected; capability stays
   bounded by clamping, so no score inflation or unbounded regression.

## Consequences

- Learning biographies are replayable; capability never leaves its declared
  scale; skills and capability are decoupled from knowledge and persona.