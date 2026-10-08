# Wanxiang · Immersive World Visual Player V1 (Experimental)

Date: 2026-10-08. Source of truth remains R7 canonical master and `reports/r7/15_R7_FINAL_CLOSURE_REPORT.md`. This document is an opt-in product/renderer expansion, **not** a R7 gate replacement, M95 human PASS, v5.5 Stable authorization, or v5.6 release.

## Motivation / current code truth

`player_ui_asset.py` currently presents region/time/location/weather, narrative and event cards. `player_projection.py` returns player-safe server observations but not a grounded navigable map. `projection3d.ts` composes example transforms by index, which cannot be mistaken for a spatial fact. The G96 reference visual provider produces structured data and not a browser rendering engine.

**North star:** the player perceives, enters and influences a world, not a dashboard. The default target is embodied 3D exploration; a diorama overview and accessible 2D atlas are companion views, not competing canonical worlds.

## Four trust layers

1. **Canonical state**: worldline identity, rule, history, committed entities and events. Written exclusively by existing authority.
2. **SceneManifest**: independently versioned geometry, coordinates, places, portal connectivity, asset digests/rights/provenance; never automatically considered canonical truth.
3. **Perceived Scene Projection**: server filtered by rights, actor knowledge and line-of-sight; only visible entities/actions/revisions; no invented placement for unknown entities.
4. **Ephemeral client presentation**: camera, local ambient motion, lighting, particles, uncommitted UI. Not a second world state.

```text
World + Commit History + Perception/Rights
      -> Player-safe Observation (existing)
      -> Versioned Spatial SceneManifest + filtered DynamicSceneProjection (NEW)
      -> Renderer (Babylon Web / Godot Native / Atlas 2D)
      -> Input / target selection -> existing Action/Proposal/Authority
      -> committed/rejected response -> visual reconciliation
```

## Current minimal code experiment

- `/experience/visual?instance_id=<existing Player instance>` is excluded from OpenAPI and is **not** exposed as a default release route.
- The Chinese Player offers an opt-in link only for the named Jiangnan reference world and only after joining a real Player instance.
- `immersive_player_ui.py` draws original procedural geometry of a Chinese canal town using **actual Babylon.js/WebGL**: streets, buildings, bridges, gate, river, workshop, trees and waterwheel. It has orbit and walking cameras, picking, and read-only world observation binding.
- Visual markers and camera movement are **illustrative**. They are explicitly not verified canonical coordinates or character movement. Current player observation has no normalized 3D spatial truth; do not invent it.
- Only the existing `/experience/player/instances/{id}/action` can submit an action. The renderer refreshes from its server response; no writes to canonical state are introduced.
- No instance ID, wrong world name, WebGL dependency failure, or server failure results in a typed/visible non-claim; a 2D illustrative fallback exists.
- The pinned UMD Babylon **CDN is prototype-only**; production must switch to locked `@babylonjs/core` package and self-hosted signed assets, test no-network fallback and content-security policy.

This is **VISUAL_SPIKE (UNQUALIFIED)** until the actual app boots, browser navigation/tests and scene screenshots have been observed. Current Python tests are structural, not GPU or human evidence. Do not advertise as a shipped 3D game.

## Next implementation: spatial truth, not more empty polish

Define `SceneManifest v1` with `world_profile_id`, `manifest_version`, `coordinate_system`, places/bounds, walkable routes, obstacles, visual anchor ↔ canonical entity mapping, asset digests/licenses, evidence scope and creator approval. Define `DynamicSceneProjection v1` with canonical revision, worldline, actor/right scope, visible entities/events, state cues, interaction affordances and delta reconciliation. Server must reject leaking invisible objects, unknown locations, stale revisions or unapproved spatial mappings. Unknown is displayed as unknown, not made-up scenery.

Use `潮汐门 -> 沉水巷 -> 机关桥` as one author-reviewed walking block. Produce at least eight traced assets, three server-grounded interactions, fixed-worldline reentry and event/replay evidence. Switch from sample geometry to traceable scene assets; add collision/navigation, third-person avatar, day-night/audio and mobile control. Do not confuse ambient decorative NPCs with World actors.

## Required visual acceptance (new gates, do not touch Stable Gates 62–66)

- VIS-A: actual 3D GPU runtime, never just CSS or a background screenshot.
- VIS-B: browser camera and 3 target picks on desktop + touch.
- VIS-C: server-filtered rights/knowledge and grounded actor/asset identities.
- VIS-D: committed/rejected distinction; no front-end-generated canonical history.
- VIS-E: server revision drives world changes; refresh/leave/continue reproduce them.
- VIS-F: visual camera/session state not canonical actor location.
- VIS-G: renderer/network/audio unavailable -> honest accessible 2D/semantic fallback.
- VIS-H: asset provenance, digest, license, rights, original reference clear.
- VIS-I: Playwright real browser desktop/mobile screenshots, console, performance, server/replay checks and exact-SHA CI.
- VIS-J: actual human can identify where they are, what they changed and how to return. Must be independently completed by human, no agent rating.

**Status in this commit:** Visual V0 scaffold is implemented on a feature branch. VIS-A–J remain **NOT_PROVEN** until run-specific evidence. Existing R7 PASS and v5.5 WAITING_HUMAN are unchanged.

See the user-facing extended Chinese master: `WANXIANG_IMMERSIVE_WORLD_PLAYER_V1_DESIGN_AND_EXECUTION_2026-10-08.md` delivered alongside this work. Avoid copying a 16k-line design into the production repo solely for documentation churn.
