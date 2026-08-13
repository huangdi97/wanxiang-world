# Phaser 2D Player Vertical Slice (G05F)

Ownership: `packages/sdk_ts` (`phaser.ts`).

## Scope

Deterministic TypeScript scene state fed by the server projection API:
semantic places/portals -> display coordinates via projection metadata,
actor/object tokens, movement command submission, rejected-action surfacing
and reconnect reconstruction from a fresh server projection.

## Guarantees

- Rendered coordinates never become canonical topology.
- Movement is submitted through the generated client; the server decides.
- Reconnect rebuilds the view from the server projection (revision-pinned).

## Status

- Scene view models + Vitest deterministic tests: PASS (no browser required).
- Phaser canvas rendering: EXTERNAL_BLOCKED (no network to install Phaser; no
  browser in this environment). The view models are the deterministic contract
  a Phaser scene would render.