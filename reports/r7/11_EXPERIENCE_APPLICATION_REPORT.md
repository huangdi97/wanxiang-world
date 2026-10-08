# R7 11 — Experience / Application Fabric

Status: `IMPLEMENTED / VALIDATED` for contract and shared-reality reference
scope.

Implemented:
- ExperienceBlueprint;
- InteractionProfile;
- ProjectionProfile;
- DistributionAdapter;
- deterministic DistributionBuild;
- WorldExperienceCard;
- read-only ObserverExperience.

Projection and distribution own no canonical storage and no write authority.

The Original/Fiction integration uses Player and Observer Experiences over the
same WorldRuntime. Player commits advance the Observer view because both derive
from the same committed worldline. Child branches diverge as worldlines, not as
Experience-owned copies.

The existing M95-R player product path remains zh-CN-first, Player/Studio
separated, and Leave->Continue preserves committed identity/state. Channel
vocabulary such as Steam/VR is not called a shipped product without its own
adapter/application evidence.


## Explicit ExperienceRuntime (2026-10-08)

`wanxiang_api.experience_runtime.ExperienceRuntime` now implements the
master-spec coordinator boundary explicitly. It binds one ExperienceBlueprint,
InteractionProfile and exact DistributionAdapter set, then delegates
entry/continue/action/projection to the existing ExperiencePlayerService.

It owns no canonical state, event store or commit method. Interaction-profile
violations and stale revisions fail closed. Leave/continue reads the same
worldline, and distribution builds remain deterministic references rather than
parallel state stores.

This closes the remaining gap between having Experience contracts and having an
actual ExperienceRuntime coordination object while preserving
`World != Experience != Projection != Distribution`.
