# Product Surface Architecture (G18A)

## Product faces -> server truth
All surfaces consume the SAME authoritative server world through the API; there is no per-surface
backend truth store. Renderers remain EXTERNAL_BLOCKED; server-composed projections + typed view models
are the qualified surface contract.

| Surface | Server use-cases (routes) | Notes |
|---|---|---|
| Studio / World IDE | create world, branches, state, events, actions | author + debug |
| Experience Player | projection, actions, session | player continuity |
| Strategy / Experiment | branches, diff, experiment run | workbench |
| Heritage / Museum | projection, rights-gated assets | heritage |
| Family Portal | projection, privacy modes | family |
| Learn / Challenge | projection, challenge | learn |
| Operator / Admin | admin-gated debug, security | ops |

## Shared context selectors
`world/instance/branch/session/perspective` are derived from the server response; surfaces never
maintain a second truth. Branch/session context switches re-fetch from server truth.

## State model
- Loading / error / empty / offline states are typed per surface (view models) and always rebuildable
  from server projections (projection owns no exclusive state).

## Type drift control
- Shared frontend domain types are frozen from the OpenAPI contract / SDK baseline
  (`reports/sdk_api_baseline.json`); the drift test regenerates + compares.
- No surface writes world state except through the command API (Commit Authority remains the only writer).
