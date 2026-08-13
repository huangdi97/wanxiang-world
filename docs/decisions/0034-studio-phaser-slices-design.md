# ADR-0034: Studio & Phaser Client Slices Design (G05E, G05F)

- Status: accepted
- Date: 2026-08-13

## Context

G05E/G05F need deterministic client vertical slices (Studio debug views and a
Phaser 2D player) that consume server projections and submit commands, without
letting rendered/local state become canonical truth.

## Decision

1. Client slices are typed view models in `packages/sdk_ts` consuming
   server-composed projections; commands are submitted through the generated
   client and server acceptance is authoritative.
2. Map/display coordinates are derived from projection metadata only.
3. Browser rendering layers (React/Phaser) are EXTERNAL_BLOCKED in this
   environment (no network to install them, no browser); the typed view models
   plus Vitest deterministic tests are the committed contract.

## Consequences

- Renderer independence is documented; reconnect reconstructs from server
  projection; no client-local truth can enter the world.