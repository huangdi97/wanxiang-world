# Director Runtime (G07D)
Ownership: `wanxiang_substrate.reality.director`.

## Layers
- WorldDirector: focus/time/event scheduling proposals.
- NarrativeDirector: goals/attractors as scoring signals (projection-only).
- PerformanceDirector: directives as projection-only metadata.

## Boundaries
Directors propose (`DirectorProposal`); they never commit directly. Every
world-changing proposal traverses normal validation/commit. Character/persona
delta candidates require actor-logic review (`DirectorReview`).