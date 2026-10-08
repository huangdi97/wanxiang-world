# Wanxiang · Source-to-Visual-World Product V1 (2026-10-08)

Status: **DESIGN + first source-driven budget planner**, NOT a completed visual world generator. This is a product correction grounded in R5–R7 canonical masters and the existing `02_SOURCE_TO_LIVING_WORLD_PIPELINE.md`, `09_STUDIO_ONE_CLICK_SPEC.md`, `apps/api/src/wanxiang_api/one_click_routes.py`, `WorldDraft`, `AssetFoundry`, and `PlayableService`.

## Product requirement: one book, one world — no per-book code

A user supplies an authorized book (TXT, EPUB, DOCX, PDF with extraction/OCR when necessary), selects desired experience/style/cost budget, reviews rights and high-impact ambiguities, and receives a scene-rich, persistent world without a developer authoring buildings, cameras, NPCs or routes for that specific book.

**The book is input/data. The world generator and player are generic software.**

Wrong approach: create `JiangnanWorldRenderer` or handcrafted CSS/Babylon geometry whenever a book is uploaded. Historical PR #2 is superseded and must not merge as the primary solution.

## The correct existing-to-new chain

```text
Book + rights + source checksum
  -> Existing Source Registry / parse / stable locators
  -> Multi-pass source distillation / Evidence / Candidate E0–E5
  -> Existing WorldDraft + WorldPackageDraft (characters, places, events, rules, worldline)
  -> NEW SourceScenePlanner / VisualSceneBlueprint
       - evidence-derived scenes, locality and story sequence
       - source-aware character/object references, with unknowns left unknown
       - story visual bible / reusable style profile
       - priority + cost budget + content-addressed cache keys
  -> Existing AssetFoundry adapter
       - cheap generic art library / deterministic SVG/Tiled fallback
       - image model provider (local or paid; optional, on demand)
       - 3D spatial generation provider (optional/high quality tier)
       - each result is an AssetCandidate with provenance/rights/quality checks
  -> Shared VisualExperience Manifest + Player
       - environment picture/panorama + layered actors/objects/hotspots
       - map/scene navigation, optional 2.5D/3D projection
       - server-side player perception/rights filtering
  -> Existing Player Action -> Commit Authority -> World History
  -> redraw changed overlays / resume same worldline
```

**Do not generate one costly 3D level per novel or every chapter.** Produce a small number of reusable key-place assets first; load/generate additional locations only when visited and approved. Same place + source/style/version uses one cached picture for many sessions; time/weather/movement/status overlays are dynamic without regenerating the background.

## V1 visual product (low-cost, credible minimum)

- A cover/portal picture and a **visual world atlas** of verified named places. Unknown topology is displayed as an abstract narrative graph, never fabricated geography.
- Enter a location and see **a scene background illustration** (generated through provider if permitted; otherwise fallback is labeled illustrative).
- Characters/objects/events as anchored **separate overlays/hotspots** tied to source identifiers and filtered by player perspective. Never infer that a global character list means all of them are inside the current location.
- Click to inspect, converse/act using existing PlayableService/Authority, show committed state changes on overlays, and keep worldline identity across leave/continue.
- Scene image styles may differ per book; renderer code and mapping contracts remain shared.
- 3D camera/mesh/VR are upgrade providers, not minimum requirements; a strong image + interactive layers can be immersive at much lower cost.

## Current data gap and honest fallback

The present WorldDraft records global `places`, `entities`, `objects`, `events`, etc., but does not guarantee a trustworthy **place ↔ person/object ↔ time/scene** graph or actual geometry. Scene planning can prioritize source-attested place names now. Production scene placement requires improved evidence-linked Scene/Location candidates in the source pipeline. A book with no extracted places must return `PLACES_NOT_EXTRACTED`; it cannot silently produce a fake bespoke city and claim it came from the book. Long free-form Chinese novels require separate live quality evaluation; existing CI synthetic fixtures are not proof of arbitrary-book semantics.

## First engineering slice already in this branch

`packages/substrate/src/wanxiang_substrate/assets/book_scene_plan.py` generates a generic `SourceVisualPlan` directly from WorldPackageDraft for the book profile. It uses pinned source/package digest, deduplicates attested places, caps default preview to 3 scene asset requests, content-addresses cache keys, blocks unknown/unapproved source rights and returns **zero billable provider calls**. It reuses existing `SemanticSceneSpec` instead of creating a competing asset registry. The planner is connected to `OneClickAuthoring.run` and Studio's `/studio/one-click` result exposes summary status. Tests cover two unrelated books and rights/budget/dedup. This slice **does not generate pixels**.

## Next execution goals (priority order)

1. **S2 Semantic Scene Extraction**: evidence-linked scene/place/temporal candidates and reusable style bible from long narrative texts; negative/unknown/out-of-domain tests. No place leakage.
2. **S3 Pluggable Image Asset Producer**: local/on-demand and optional remote; explicit rights consent, bounded retries, concurrency, exact cost accounting, deterministic cache key incl. model/style/prompt version; store image bytes/digest/metadata and candidate review status, with at least one *actual generated* visual asset.
3. **S4 Generic Visual Player**: no hardcoded book/character/place names; server-sanitized scene atlas, actual background images, avatars and clickable hotspot overlays; interaction writes ONLY through existing Player authority.
4. **S5 Change and Persistence**: update only changes on commit, diff/branch/leave/continue/replay parity, per-character knowledge and rights, no fabricated visual consequences.
5. **S6 Cross-book acceptance**: at least two distinct rights-safe textual books/novellas, first-time and long-source test, automatic generated scenes (not hand-authored screenshot), screenshots and browser E2E, source-to-image trace, asset licensing, cache reuse, budget metrics. Human independently judges spatial/visual sense; cannot be replaced by a model self-rating.

## Economics and quality controls

Total incremental cost per new book = source parsing / LLM distillation + **unique uncached scene images** + optional character assets + user-triggered extra locations + ongoing world simulation. Player render/replay and cached scenes incur no repeated image-generation fee. Put default cost governor at 1–3 preview scenes, require explicit opt-in above budget; report actual metered provider costs when provider exists rather than inventing per-book prices.

Do not compress full novels into arbitrary prompts and pretend consistent world simulation. Extraction must preserve chapter-scoped source evidence, relationship uncertainty, scene changes and identity, while generative *depiction* remains a candidate interpretation.

## Scope and release boundaries

- Keep R7 Composition/Authority/History and v5.5 Stable acceptance untouched.
- Do not add a separate 3D-only world runtime or special-case Jiangnan city.
- Do not claim novel-to-3D, image model output, human immersion or published product from this first budget-planner step.
- Do not transmit copyrighted/private text or prompts to external providers without rights and provider authorization.
- Existing M95 human Gates 62–66 remain WAITING_HUMAN; new cross-book visual gates are additional, not a shortcut.
