# Product Surface Architecture (G18A)

## Product faces -> server truth
All surfaces consume the SAME authoritative server world through the API; there is no per-surface
backend truth store. Renderers remain EXTERNAL_BLOCKED; server-composed projections + typed view models
are the qualified surface contract.

| Surface | Server use-cases (routes) | Notes |
|---|---|---|
| Studio / World IDE | create world, branches, state, events, actions | author + debug |
| Experience Player | projection, actions, session | visual-first Living World Stage; one server truth; low-cost T0/T1 asset projection |
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


## Experience Player visual boundary

The Player's Living World Stage is a projection surface. Source-grounded scene
assets, narrative atlas, HUD, live narrative and action dock may change visual
presentation without creating a second world state. T0 deterministic SVG is the
zero-cost baseline; optional T1 image providers remain rights/network/cost
governed and share the authoring/player cache. See
`docs/source_to_living_world/PLAYER_VISUAL_STAGE.md`.

A graphical projection is not Canonical World Truth. Real 3D/GPU engines remain
external capabilities until separately evidenced.
