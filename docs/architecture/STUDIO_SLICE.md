# Studio Debug Vertical Slice (G05E)

Ownership: `packages/sdk_ts` (`studio.ts`).

## Scope

Deterministic TypeScript view models for the Studio client: world/branch/
entity/event views, entity inspector rows, a bounded command form
(`STUDIO_ACTIONS`), branch comparison and validation/conflict surfacing. All
consumed projections are server-composed; the client never treats local state
as world truth.

## Status

- View models + Vitest deterministic tests: PASS (no browser required).
- React/Vite rendering application: EXTERNAL_BLOCKED (no network to install
  React/Vite; no browser in this environment). The typed view models are the
  deterministic contract a React renderer would consume.