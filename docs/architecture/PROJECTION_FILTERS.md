# Projection API, Perspective & Rights Filters (G05D)

Ownership: `wanxiang_substrate.projection` (server-composed DTOs).

## Contracts

`ProjectionRequest` (session/actor/branch/mode) and `ProjectionSnapshot`
(DTO items, never raw canonical state) are separate from canonical types.

## Server-side filters

`ProjectionService.compose` applies, in order:
- mode gate: debug projection requires explicit privileged authorization;
- privacy: sealed info payloads are redacted (`sealed_payload`);
- knowledge: private beliefs/memories of other actors never leak;
- rights: restricted places are redacted without the `enter` permission;
- truth labels: beliefs = model_inference, memories = reconstruction, payloads
  = source_backed, world state = canon.

## Guarantees

- Raw canonical state is never returned by default.
- Client-side filtering cannot protect secrets; filtering is server-side.
- Projection DTOs are not coupled to ORM models.