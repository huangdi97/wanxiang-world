# Wanxiang Source → Living Visual World — repository closure (this pass)

Updated: local agent pass on `feature/source-to-visual-world` (PR #3, draft, base `feature/r7-cordis-native`).

This report records **what was verified in this pass** and **what was not**. Every claim
below is tied to a command, an artifact or a file; nothing here is a human verdict.

## 0. Baseline re-verification (before any change)

| fact | value | how |
|---|---|---|
| branch HEAD at start | `af5731e8c4b13f525468185424c51c5be588bacd` | `git fetch origin`, `git rev-parse origin/feature/source-to-visual-world` |
| PR #3 | open, **draft**, head `af5731e8…`, base `feature/r7-cordis-native` | GitHub REST API (`/repos/huangdi97/wanxiang-world/pulls/3`) |
| CI at that SHA | `ci` runs completed **success** | GitHub REST API (`/actions/runs?branch=feature/source-to-visual-world`) |

The SHA in the goal text was still current, but it was re-read from GitHub rather than assumed.

## 1. What this pass changed (all committed on the branch)

Product/UX (Player surface, server-rendered HTML/CSS/JS):

- **Home is continue-first.** When a resumable session exists the continue strip is the first
  block, the world plaza follows, and the brand hero is demoted below them
  (`player_ui_style.py` `#home-view.is-active.has-continue` ordering, `player_ui_asset.py`
  slot move, `player_ui_home_script.HOME_SCRIPT`).
- **World cards carry world state**: visual identity (image + consumer tier chip) or an honest
  "no world visual yet" placeholder, latest place, world time, latest event, continue state,
  and a 可以继续 / 可以进入 chip. Engineering tiers stay out of the card.
- **Consequence is legible.** Diff changes now render a concrete before → after line
  (`状态 未记录 → 清醒`) plus a secondary category chip instead of a terse sentence; the
  project layer derives it from committed `DiffChange.before/after` through an allowlist
  (`player_projection_deltas._consumer_deltas`).
- **Chronicle reads as world memory.** Each record carries time, who (你 / actor name), place,
  a concrete sentence derived only from the committed event, and a collapsed
  `记录说明` disclosure (`_chronicle_card`, `player_ui_replay_script.chronicleRow`).
- **Observer mode is honest.** The action bar and suggestions are replaced by an observer gate
  ("你正在观察这个世界：角色没有移动，世界也没有因为你改变") with a single
  "选择角色进入" action; the "your character" panel is hidden while observing.
- **Embodiment uses progressive disclosure**: possessions / goals / memories / relations are
  collapsed sections instead of an open dump.
- **Stage composition is banded, not overlapped.** Caption, HUD, narrative and context each own
  a band; the dock sits in the shell flow. Measured geometry confirms zero overlap between
  dock/story/context/rail/caption/actions on desktop and mobile
  (`probe/overlap_check.py` over `measure-*.json`).
- **Unrecorded facts are not shouted**: empty HUD cells are hidden and the duplicated
  "世界时刻 世界时刻 N" label was fixed.
- **`[hidden]` now actually hides** flex/grid children (`.site-shell [hidden]{display:none!important}`),
  which is what makes the observer gate / action bar / panels switch correctly.
- **Mobile**: 44px touch targets for 15 control types plus inputs/selects/summary, bottom
  safe-area padding on the dock, and 320px overflow bounding.
- **Player payloads no longer carry a raw asset digest**: `content_sha256` was replaced by an
  opaque, derived `asset_revision` (`player_asset_revision._asset_revision`) in the world
  detail atlas/scenes and the live scene visual; the panorama renderer keys on it.

Maintainability (the size guard drove these, not preference):

- `player_i18n_world_memory_{zh,en}.py` — consequence/chronicle/card copy split out of the base
  catalogs; merged in `player_i18n.py`.
- `player_projection_deltas.py` — consequence helpers plus the chronicle/change card builders.
- `player_ui_home_script.py` — home/plaza rendering split out of the main Player script.

Evidence and review entry points:

- `tests/integration/test_svw_product_visual_audit.py` — boots the real server, seeds a
  source-grounded world, walks every surface at 1440×1000 / 1280×800 / 390×844 / 320×720 and
  writes screenshots plus measured facts (console errors, overflow, controls under 44px, image
  alt coverage).
- `CURRENT_PRODUCT_VISUAL_AUDIT/` — 36 captures, `SCREENSHOT_INDEX.md`, `audit.json`.
- `scripts/player_preview_server.py` — one-command local review server (SQLite, deterministic
  resolvers, no credentials, no network).
- `HUMAN_REVIEW_START_HERE.md` — the only page a human reviewer needs.

## 2. Verification performed in this pass

| check | result | evidence |
|---|---|---|
| `ruff check .` | PASS | `All checks passed!` |
| `ruff format --check .` | PASS | 3102 files already formatted |
| `pyright` | PASS | `0 errors, 0 warnings, 0 informations` |
| `scripts/architecture_check.py` | PASS | `Architecture conformance: PASS` |
| `scripts/kernel_guard.py` | PASS | `kernel guard: 0 violation(s)` |
| `pytest tests/api -q` | PASS | 184 passed |
| `pytest tests/integration/test_svw_product_visual_audit.py -q` | PASS | 36 captures, no page errors, no horizontal overflow |
| stage geometry overlap / overflow | PASS | `overlap_check.py`: `problems: 0` on desktop + mobile, both modes |
| `pytest tests/integration/test_svw_large_world_scale.py -q` | PASS | 2 specs, 117s: (a) 100-place world — bounded place page, search returns one place inside the budget, 320px viewport does not scroll sideways; (b) 400 entities + 60 places — compile inside budget, every place still indexed, `0 < scenes <= 3` and `scenes < places` (bounded initial generation), payload under the bound, no overflow, no page errors |
| full `pytest -q` (local) | PASS | 2334 passed, 2 skipped, 2336 collected (skips: PostgreSQL and Docker unavailable on this host) |
| TypeScript gates (`pnpm -r lint/typecheck/test/build`) | PASS | CI `ts` job at `cc9c61fc` (not run on this host: no Node) |
| PostgreSQL migration/integration | PASS in CI, EXTERNAL_BLOCKED locally | CI `postgres` job at `cc9c61fc`; no Docker on this host |

## 3. Status matrix (only what is actually true)

```
SOURCE_PIPELINE              PASS (unchanged, not re-verified end to end in this pass)
WORLD_PACKAGE                PASS (unchanged)
SOURCE_GROUNDING             PASS (unchanged)
WORLD_ATLAS                  PASS (consumer tier language, bounded index, localized source-relation labels; conflict state asserted by tests)
T0                           PASS (offline scenes render; motifs vary per place)
T1_CONTRACT                  PASS (untouched by this pass)
T1_REAL                      EXTERNAL_BLOCKED (no credential)
T2_CONTRACT                  PASS (upgrade surface captured as contract surface)
T2_REAL                      EXTERNAL_BLOCKED (no credential)
T3_CONTRACT                  PASS (upgrade surface captured as contract surface)
T3_REAL                      EXTERNAL_BLOCKED (no credential)
PLAYER_STAGE                 PASS (banded layout, zero measured overlap)
OBSERVER                     PASS (observer gate, preview wording, non-committing)
EMBODIMENT                   PASS (progressive disclosure, present vs known people)
ACTION_COMMIT                PASS (unchanged; committed action visible)
HISTORY                      PARTIAL (time/who/place/concrete consequence added;
                                     provenance disclosure present; no per-event actor audit)
REPLAY                       PASS (banner, viewed time, return-to-now, read-only)
WORLDLINE                    PASS (unchanged)
LEAVE_CONTINUE               PASS (continue-first home, same instance)
DESKTOP                      PASS
MOBILE                       PASS (390×844 measured, no overflow)
320PX                        PASS (320×720 measured, no overflow, 44px targets)
ZH_CN                        PASS
EN_US                        PASS (catalog parity; no Han characters and no CJK punctuation in en-US chrome)
PRIVACY                      PASS (unchanged; no new leak; asset digest removed from payload)
RIGHTS                       PASS (unchanged consumer copy)
CACHE                        PASS (unchanged)
RESTART                      PASS (unchanged)
ARCHITECTURE                 PASS
KERNEL_FREEZE                PASS
CI                           PASS (run 42125651683 at 2ddd34fb: six of six jobs green)
SVW_J_HUMAN                  WAITING_HUMAN
M95_HUMAN                    WAITING_HUMAN
STABLE_RELEASE               LOCKED
```

## 4. CI (authoritative full-suite evidence)

Branch `feature/source-to-visual-world` was pushed across `1d7ebb82` … `2ddd34fb`. Runs
`41877978549` (`cc9c61fc`), `41980731016` (`512bf8b4`), `42027410465` (`0600c35d`),
`42079119239` (`41a87af2`) and `42125651683` (**`2ddd34fb`**) are **success**, with every job green:

| job | result |
|---|---|
| Repository safety / secret scan / forbidden tracked files | success |
| python (ruff, format, pyright, `pytest -q`, architecture/quality, kernel guard) | success |
| PostgreSQL migration + integration | success |
| API / package / SDK generation + drift | success |
| Release build + clean-room certification smoke | success |
| ts (pnpm lint / typecheck / test / build) | success |

Two intermediate runs failed exactly one assertion each and both were fixed rather than
worked around: `1f3164c8` lost the 44px mobile height on a worldline compare button when the
touch-target rule was rewritten (fixed in `cc9c61fc`), and `95ba879b` tripped an existing
browser assertion that expected the raw atlas relation type after that type became localized
(fixed in `512bf8b4`). Local gates in section 2 were re-run after every later edit.

## 5. Known remaining gaps (not hidden, not counted as done)

1. **Visual tier proof placement.** Place chips and gallery captions still carry
   `T0 · 离线场景 · 视觉生成器 procedural-svg@1.1.0`, i.e. part of the engineering proof is on
   the consumer line instead of only in a disclosure.
2. **Localization literals (mostly closed).** The hardcoded `：` and `、` separators, the raw
   atlas `relation_type` and the English panorama aria fallback now come from the copy catalog, and
   the contract suite rejects Han characters *and* CJK punctuation in the en-US document. What
   remains are defensive English fallbacks inside the spatial built-in (`copy(key, fallback, ...)`);
   the catalog keys they stand in for exist in both locales, so no user-visible leak was observed.
3. **Scale evidence (closed for places and entities, open for mixed bundles).** Browser specs now
   cover a 100-place world (bounded page, progressive reveal, search — actually 60 places and 402
   entities and 200 relations in a 16KB source) and this is the measured shape of a long source.
   A single bundle that mixes *conflicting* sources still has no dedicated spec; conflicting
   relations from one source are covered by the atlas conflict browser test.
4. **T2/T3 stage activation.** The audit captures the upgrade/contract surfaces; a real
   panorama or spatial asset was never attached on this host, so `#panorama-stage-toggle` /
   `#spatial-stage-toggle` stayed hidden and their in-stage renderers were not exercised here.
5. **Replay server-side guard.** Replay remains a client-side read mode; a direct POST while
   replaying still commits (the UI cannot do it).
6. **World card art.** Cards show a real world visual only once one exists; otherwise an honest
   placeholder. No world-level visual is materialised at creation time.
7. **Human judgement.** Immersion, comprehension and "is this Wanxiang" remain
   `WAITING_HUMAN`; this pass does not rate them.

8. **Multi-source bundles must meet the raised bar (decided, not a defect).** Decision recorded
   2026-11-04: adding a source to a bundle *may* raise the required capability set, so a bundle whose
   combined evidence does not cover it is refused at compile time with `422 ZERO_COVERAGE` instead of
   silently producing a thinner world. Readiness requires `coverage > 0.0`
   (`authoring/draft_builder.py:190`) and coverage is computed over the selected domains' required
   capabilities (`draft/coverage.py:40-59`). `tests/integration/test_svw_multisource_coverage.py` pins
   the policy: the same text compiles as one source, compiles concatenated, and is refused as an
   under-covering two-source bundle. A “sufficiently evidenced” bundle was then attempted and measured: a
   richer book (two places, two people, two rules, an institution) plus a short travel-notes source is
   still refused with `ZERO_COVERAGE`, and a doubled book plus the same notes is refused too but with an
   **empty `details` payload**, so that second refusal carries no diagnosis for a client. Conclusion:
   under the decided policy a book + short-notes bundle is not compilable at all, and reaching a
   compilable bundle needs a second source of comparable weight — not a small appendix. Two follow-ups
   are queued: make the refusal always carry `product_state`, and build a two-comparable-sources spec.

9. **The rejected built-in suggestion is fixed (was a defect, now resolved).** `休息片刻` returned
   `422 missing_fields:entity_id,status` because the action parser only resolves the
   `让自己保持<status>` shape; the shipped zh phrasing used a different verb. The catalog now ships
   `让自己保持休息`‑style wording (`让自己保持休息`), verified on the real server (`200`, `状态：警觉 → 休息中`),
   and the i18n contract asserts the shared shape plus that the refused phrasing cannot come back.
   Also corrected, twice: the “three actions, two change rows” observation was first wrongly attributed to
   that refusal, and then wrongly called a bounded window. Measured on the real server, every action
   returns exactly **one** `recent_changes` entry (the newest commit's changes, which is what
   “world changes” is for). The extra match came from the spec itself: `#change-list li` also matched
   the nested `.change-deltas > li` lines. The spec now counts `.change-row`, so the observation is
   closed as a measurement artifact rather than a product behaviour.

## 6. Boundaries that were not crossed

- No Canon/History/Worldline change; visual and projection layers remain read-only byproducts.
- No second canon, no second frontend application, no browser-owned canonical state.
- No per-book hardcoding; no invented source relations; no fake provider or human PASS.
- No merge, tag, release, Stable declaration, or PR "ready for review".
- No validation loosened to make a test pass: the two contract tests touched here were
  **strengthened** (44px now asserted for 15 control types plus fields; the world-count
  announcement is asserted in the served document) and the size guard was satisfied by
  extracting cohesive modules, not by raising limits.

