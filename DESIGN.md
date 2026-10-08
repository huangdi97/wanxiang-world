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
