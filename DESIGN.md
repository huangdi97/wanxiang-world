# Player Experience design record

<!-- impeccable:design-record 1 -->

This record captures the M95 Player surface after the remediation pass. It is
an experience layer over the existing playable API; Studio remains the
technical authoring surface.

## Direction

- Surface seed: `7abaadc8`, structural candidate 3.
- Direction seed: `19e29434`, grounded candidate 7.
- Thesis: the first meaningful step should feel like entering a living place,
  not operating software.
- Own-world metaphor: a living cartography field folio, with map marks and
  route lines suggesting continuity without pretending to be a real map.
- First viewport: a Chinese promise, one primary entry action, and a world
  card that gives the player a place to go.

## Visual system

- Ink navy `#14263b` anchors type and navigation.
- Cool paper `#f5f1e8` is the page ground; pale blue and jade carry place and
  world-state surfaces.
- Coral is reserved for the forward action; cobalt and ochre are secondary
  wayfinding accents.
- Body copy uses a Chinese system fallback stack; no external font or remote
  asset is required.
- Spacing follows a compact 8px rhythm with generous hero breathing room.
- Cards use restrained borders and shallow shadows; the map geometry is a
  decorative orientation cue, not a second source of world truth.

## Interaction and responsive behavior

- Player routes are the only data source for the Player UI. The browser holds
  selection and routing state, never canonical world state.
- World detail precedes entry and exposes scenario, location, time, present
  moment, character choice, and the recommended opening in player language.
- Play state exposes scene, actual committed changes, chronicle, character
  state, memories, and relations from server projections.
- Leave and continue return to the same instance/branch rather than creating a
  fresh story.
- At 760px and below, the hero, details, play panels, and forms collapse to a
  single readable column; focus rings and reduced-motion preferences remain
  explicit.
- Player copy comes from a shared immutable catalog: `zh-CN` is the explicit
  default, while `en-US` is an opt-in surface selected by query or header;
  browser locale never silently changes the Player language.

## Validation record

- Automated UI review: `tests/integration/test_m95_player_experience_browser.py`.
- Target screenshots: `.impeccable/review/desktop.png` and
  `.impeccable/review/mobile.png` (local review files, ignored by Git).
- Detector run over the Player asset/style/script/routes and projection route:
  zero findings.
- Human comprehension, immersion, and acceptance are not inferred from these
  checks; M95 remains `USER_INPUT_REQUIRED` until a real player completes the
  supplied Chinese packet.

## Continuity and consequence pass (local agent, `feature/source-to-visual-world`)

- The home now leads with the world you were already in: continue strip first, plaza
  second, brand hero demoted, and cards carry visual identity, latest place, world time,
  latest event and continue state instead of engineering status.
- The World Stage is banded rather than overlapped: caption, HUD, narrative and context
  each own a band and the action dock sits in the shell flow. Geometry is measured, not
  eyeballed (`CURRENT_PRODUCT_VISUAL_AUDIT/audit.json`).
- Consequence is written in world language: a committed change renders as a concrete
  before → after line plus a secondary category chip, and the chronicle carries time, who,
  place and a sentence derived only from the committed event, with the record description
  available behind a disclosure.
- Observing is an explicit state: no role moves, nothing changes, the action controls are
  replaced by a single "choose a character to enter" step.
- Embodiment discloses possessions, goals, memories and relations progressively.
- Mobile is a first-class target down to 320px: 44px targets, bottom safe-area padding on
  the dock, and no horizontal overflow.
- Player payloads expose an opaque derived `asset_revision`, never a canonical digest.
- Human comprehension, immersion and acceptance remain `WAITING_HUMAN`; the automated audit
  records measurements, it does not rate the experience.
