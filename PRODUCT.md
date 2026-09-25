# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Inferred from the explicit M95 remediation brief and the current repository:
an embedded FastAPI-served Player surface using HTML/CSS/JavaScript, with the
existing `/experience/*` API and `PlayableService` as its only world interaction
path. The repository has no `apps/web`; no separate frontend runtime is added
in this remediation.

## Users

The primary user is an ordinary first-time player opening Wanxiang in a
browser to enter, inhabit, and return to a persistent world. A secondary user
is a creator or developer using the separate Studio surface to author, review,
debug, and publish worlds.

## Product Purpose

Wanxiang lets people create worlds, enter worlds, act through a character, see
what the world actually changed, and return to the same living thread later.
M95 succeeds when a first-time player can understand the invitation quickly
and complete the real World Plaza → world/scenario → character → enter → free
action → response → world change → leave → continue journey without facing
engineering internals.

## Positioning

Wanxiang's distinct mechanism is that a player's action travels through the
existing Proposal → Validate/Resolve → Commit Authority → StateDiff →
Projection path, so the world response is grounded in append-only canonical
history rather than a client-side narrative or local fake state.

## Operating Context

The M95 human test runs locally in a browser against the current v5.5
candidate, an isolated SQLite profile, the FastAPI backend, and the existing
PlayableService. The first-run path starts at a Player Experience home or
World Plaza, not Studio. The prepared fixture is creator-owned and rights-safe
synthetic qualification content; automated checks are readiness evidence and
never human acceptance.

## Capabilities and Constraints

- The Player and Studio surfaces must have distinct entries and information
  architectures.
- Player-visible labels, empty states, loading states, errors, confirmations,
  world copy, actions, and world changes default to `zh-CN`; `en-US` may be an
  explicit optional fallback.
- Player UI must not expose WorldPackage, Candidate, Coverage, Worldness,
  Commit, Ledger, Provider, RuntimeProfile, schema, hash, raw JSON, or debug
  identifiers. Technical detail belongs in Studio or a developer/debug area.
- The Player surface submits actions only through the existing API and
  PlayableService. It may not hold Commit Authority or invent local world
  state.
- Responsive desktop-first web behavior, semantic accessibility, readable
  contrast, and keyboard-friendly controls are required.
- Reality Root, Commit Authority, canonical history, replay, branch isolation,
  rights/privacy controls, and provider proposal-only boundaries are frozen.

## Brand Commitments

- Product name: 万相 / Wanxiang.
- Player-facing promise: “创造世界，进入世界，让世界继续发生。”
- Player voice is natural, calm, and idiomatic Simplified Chinese; obvious
  Chinese-English mixing and unexplained engineering terminology are not
  acceptable.

## Evidence on Hand

- Existing M95 route and packet: `reports/M95_PLAYER_TEST_PACKET.md`.
- Existing real API routes: `apps/api/src/wanxiang_api/playable_routes.py`.
- Existing embedded Studio/player controls: `apps/api/src/wanxiang_api/studio_ui_routes.py`.
- Existing M95 creator-owned synthetic route evidence is readiness evidence
  only; it does not prove human comprehension, agency, or Stable acceptance.
- No customer outcome, production-capacity, scientific-validity, or live-world
  claim may be fabricated from the local fixture.

## Product Principles

1. Canonical reality is the source of every player-visible world change.
2. A first-time player should understand the next meaningful action before
   seeing implementation detail.
3. Player Experience and Studio are different products with different
   vocabularies and responsibilities.
4. Chinese clarity is a default product behavior, not a translation afterthought.
5. Evidence boundaries remain visible to operators without burdening players.

## Accessibility & Inclusion

The Player surface must work at desktop and narrow mobile widths, preserve
keyboard focus and logical reading order, expose semantic labels for controls,
avoid color-only meaning, and provide sufficient contrast and explicit loading,
empty, error, and confirmation states.
