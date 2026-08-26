# v5.5 M85-M94 Acceptance Matrix

Status at G92G: **IN_PROGRESS / NOT_ACCEPTED**. This ledger is frozen for the
v5.5 run; thresholds may not be lowered to obtain a release.

| Gate | Area | Status | Evidence |
|---:|---|---|---|
| 1 | PlayableWorldProfile from v5.4 world | PENDING | — |
| 2 | Plaza / Continue / My Worlds / My Characters E2E | ACCEPTED | G88H API/CLI/Studio shared backend E2E |
| 3 | Character / Observer / Embodiment permissions | ACCEPTED | G88E contracts + G88H embodied API path |
| 4 | Free Action proposal-to-commit loop | ACCEPTED | G88H IntentCompiler → CommitAuthority |
| 5 | Committed StateDiff | ACCEPTED | G88H committed event diff and replay hash |
| 6 | Leave / Continue continuity | ACCEPTED | G88H same instance/branch after leave |
| 7 | ActorGoalStack persistence/replay | ACCEPTED | G89A serialization + replay verification |
| 8 | Memory / Belief / Truth separation | ACCEPTED | G89C EpistemicMemory + G03B replay/authority tests |
| 9 | Secret / rumor / future-knowledge isolation | ACCEPTED | G89D future guard + G03B/G35G privacy regressions |
| 10 | RelationshipState time/event provenance | ACCEPTED | G89E time-scoped graph + visibility/replay tests |
| 11 | 7-day actor continuity | ACCEPTED | G89H source-created two-actor 7-day replay/Continue qualification |
| 12 | From Source regression | ACCEPTED | G90H/M87 qualification: reports/G90H_REPORT.md |
| 13 | From Prompt E5 Candidate/WorldDraft | ACCEPTED | G90H E5 contract, measured WorldDraft coverage, Preview and review gate |
| 14 | Hybrid E0-E5 provenance | ACCEPTED | G90H source/prompt traces with preserved dissent |
| 15 | Publish visibility/rights gates | ACCEPTED | G90H private/public/rights/API qualification |
| 16 | PressureProfile outside Kernel | ACCEPTED | G91H real playable qualification; substrate-only profile and kernel guard |
| 17 | CANON/DIRECTED/LIVING/EXPERIMENT modes | ACCEPTED | G91H mode evaluation and audited switch |
| 18 | Director has no Commit authority | ACCEPTED | G91H proposal-only policy and architecture review |
| 19 | Opportunity can be ignored | ACCEPTED | G91H actor ignore and projection status |
| 20 | Intervention branch/artifact isolation | ACCEPTED | G91H real runtime child branch, parent event/hash/replay proof |
| 21 | 24-hour smoke | ACCEPTED | G92G real SQLite accelerated 24h reference with checkpoint/replay/recovery |
| 22 | 7-day runtime | ACCEPTED | G92G real SQLite accelerated 7d multi-actor run with daily checkpoint/replay/storage evidence |
| 23 | 30-day literary run | PENDING | — |
| 24 | 90-day selected-world run | PENDING | — |
| 25 | Checkpoint/resume/crash recovery | PENDING | — |
| 26 | Compaction replay equality | PENDING | — |
| 27 | LOD transition continuity | PENDING | — |
| 28 | Cost/storage/memory quantification | PENDING | — |
| 29 | Evolution delta taxonomy separation | PENDING | — |
| 30 | 30-day Actor/Relationship/Organization evolution | PENDING | — |
| 31 | Evolution explainability/replay | PENDING | — |
| 32 | Source/canon immutability | PENDING | — |
| 33 | Positive/negative pattern benchmark | PENDING | — |
| 34 | Evidence-backed emergence candidate | PENDING | — |
| 35 | High-level promotion review | PENDING | — |
| 36 | False-positive controls | PENDING | — |
| 37 | No universal-emergence claim | PENDING | — |
| 38 | WorldRunArtifact re-verification | PENDING | — |
| 39 | Recoverable Experiment Registry | PENDING | — |
| 40 | Fork/intervention parent isolation | PENDING | — |
| 41 | Four or more parallel worldlines | PENDING | — |
| 42 | Multi-provider/policy or mixed population | PENDING | — |
| 43 | Worldline trajectory/cost comparator | PENDING | — |
| 44 | ValidationProfile V0-V7, unknown != pass | PENDING | — |
| 45 | Physical Provider ABI | PENDING | — |
| 46 | Visual Provider ABI | PENDING | — |
| 47 | Reference physical provider E2E | PENDING | — |
| 48 | Reference visual projection E2E | PENDING | — |
| 49 | Multi-perspective privacy isolation | PENDING | — |
| 50 | Provider output cannot write reality | PENDING | — |
| 51 | Browser Experience/Studio E2E | PENDING | — |
| 52 | Security/private-source/UGC scan | PENDING | — |
| 53 | v5.4 critical regression | ACCEPTED | M88 final regression: 1296 passed, 1 skipped, 2 warnings; PostgreSQL skip is documented external profile |
| 54 | Full Python/TypeScript quality | ACCEPTED | M88 Ruff/Pyright/Kernel/architecture gates pass; SDK and TypeScript baselines remain stable |
| 55 | Clean clone | ACCEPTED-INHERITED | v5.4 post-release evidence; v5.5 clean clone pending |
| 56 | Remote SHA equals local HEAD | PENDING | v5.5 branch not pushed yet |
| 57 | Required GitHub Actions | PENDING | v5.5 branch not pushed yet |
| 58 | Working tree clean | PENDING | G88A commit pending |
| 59 | Evidence boundary separation | PENDING | Final evidence goal |
| 60 | Release gate / rc1 only if all ACCEPTED | LOCKED | G97H/G97J |

Required release condition: Gates 1-59 must be ACCEPTED with real evidence;
then and only then may G97H create annotated `v5.5.0-rc1` and a GitHub
prerelease. Otherwise the final status remains `NOT_ACCEPTED`.

## Latest checkpoint — G88B (2026-08-26)

Gate 1 **ACCEPTED**. Evidence: `reports/G88B_REPORT.md`; four focused contract
tests pass, including v0-to-v1 compatibility and invalid reference rejection.
Gates 2-52 remain pending. Release status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G88C (2026-08-26)

G88C PASS. ExperiencePackage round-trip, embodiment-policy, and private/family
visibility negative tests pass; no new final gate is promoted independently of
the M85 qualification. Release status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G88D (2026-08-26)

G88D PASS. Plaza cards, owner filtering, recent-session ordering, continue
selection, and private-profile negative access all pass. Gate 2 remains pending
until the shared API/Studio playable E2E is complete.

## Latest checkpoint — G88E (2026-08-26)

G88E PASS. Character ownership/compatibility, observer presence, single-lease
embodiment, leave/resume, and observer-no-lease tests pass. Gate 3 remains
pending until these rules are exercised through the full product route.

## Latest checkpoint — G88F (2026-08-26)

G88F PASS. Text/structured intent compilation, typed clarification/unsupported
outcomes, hostile-input rejection, and proposal-only authority boundaries pass.
Gate 4 remains pending until the compiler is connected to the real runtime
commit/replay path in G88H.

## Latest checkpoint — G88H (2026-08-26)

G88H PASS. Gates 2-6 are now **ACCEPTED** by the source-created-world E2E;
Gates 7-52 remain pending. Release status remains **IN_PROGRESS /
NOT_ACCEPTED**.

## Latest checkpoint — G88G (2026-08-26)

G88G PASS. Committed-state categories, epistemic permission filtering,
no-change semantics, replay determinism, and narrative read-only separation
pass. Gate 5 remains pending until the full playable E2E emits this diff from a
real committed event.

## Latest checkpoint — G89A (2026-08-26)

G89A PASS. ActorGoalStack v1 provides five goal tiers, dependency/priority/
deadline contracts, explicit provenance, immutable revision events, and
schema-versioned serialization whose snapshot is verified against replay.
Gate 7 is **ACCEPTED**. Gates 8-11 and the remaining gates remain pending;
release status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G89B (2026-08-26)

G89B PASS. Goal reprioritization now has a deterministic reference policy with
bounded deadline/evidence deltas, reason/evidence lineage, stale-source checks,
and a provider adapter that can only return proposals. Gate 7 remains
**ACCEPTED**; Gates 8-11 and the remaining gates remain pending. Release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G89C (2026-08-26)

G89C PASS. The existing Epistemic substrate now carries perception refs,
read-only decay, reinforcement lineage, and legacy-field compatibility without
creating a second memory store. Gate 8 is **ACCEPTED**. Gates 9-11 and the
remaining gates remain pending; release status remains **IN_PROGRESS /
NOT_ACCEPTED**.

## Latest checkpoint — G89D (2026-08-26)

G89D PASS. Belief revisions support, contradict, refine, and explicitly mark
unknown while retaining before/after lineage; future-scoped evidence is
rejected. Gate 9 is **ACCEPTED**. Gates 10-11 and the remaining gates remain
pending; release status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G89E (2026-08-26)

G89E PASS. RelationshipState v1 carries eight bounded dimensions, temporal
validity, event refs, replayable revisions, and actor-scoped visibility. Gate 10
is **ACCEPTED**. Gate 11 and the remaining gates remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G89F (2026-08-26)

G89F PASS. Character Passport is a ref-only, privacy-aware projection over the
existing CharacterRecord. Per-entry portability flags, origin refs, target
compatibility checks, and explicit impossible-entry rejection pass. Gate 11 and
the remaining gates remain pending; release status remains **IN_PROGRESS /
NOT_ACCEPTED**.

## Latest checkpoint — G89G (2026-08-26)

G89G PASS. ActorContinuityProjection provides frontend timeline DTOs and
why-action refs with actor/admin cognition access, observer redaction, and
relationship visibility filtering. Gate 11 remains pending until G89H's
multi-day continuity qualification; release status remains **IN_PROGRESS /
NOT_ACCEPTED**.

## Latest checkpoint — G89H / M86 (2026-08-26)

G89H PASS. The source-created literary world, two real PlayableService actor
instances, leave/Continue boundary, seven-day accelerated Goal/Memory/Belief/
Relationship run, replay digest, and checkpoint resume all pass. Gate 11 is
**ACCEPTED** and M86 is complete. Gates 12-52 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G90A (2026-08-26)

G90A PASS. The World Workshop now has a shared Source/Prompt/Hybrid home and
an optimistic immutable `WorkshopDraftStore` used by all editor panels.
Canonical state, event history, candidates, package registry, and Commit
Authority remain in their existing v5.4 boundaries. Gates 12-15 remain pending
until G90H exercises the three real creation paths and publishing checks.

## Latest engineering checkpoint — G90G (2026-08-26)

G90G PASS. World Registry search/open/install now delegates to the existing
package registry, dependency resolver, installer, and trust policy while
retaining label/category/tag/version/compatibility/provenance metadata.
Untrusted executables remain blocked and rights-blocked worlds are not
registered. Gates 12-15 remain pending until G90H qualification.

## Latest engineering checkpoint — G90H / M87 (2026-08-26)

G90H PASS. Source, Prompt, and Hybrid all produce measured, non-zero-coverage
WorldPackage/Preview artifacts through the shared Workshop service. Prompt
claims remain E5 and cannot publish until the three review actions are
accepted. API/Studio wiring and PlayableService observer entry pass over the
reference runtime. Gates 12-15 are **ACCEPTED**; Gates 16-52 and final release
gates remain pending. M87 is complete and v5.5 remains **IN_PROGRESS /
NOT_ACCEPTED**. Evidence: `reports/G90H_REPORT.md` and
`reports/M87_QUALIFICATION.md`.

## Latest engineering checkpoint — G91A (2026-08-26)

G91A PASS. `PressureProfile` v1 now carries all eleven bounded pressure
dimensions, Scenario/Domain refs, schema/version, provenance, deterministic
serialization, and a matched zero-pressure baseline. The type lives only in
the substrate reality plane; kernel/domain packages remain unchanged. Gate 16
stays pending until the M88 qualification exercises it in a real playable
world. G91B is next; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91B (2026-08-26)

G91B PASS. Existing Opportunity records now have explicit lifecycle,
eligibility, expiry, reward/risk, completion-evidence, and world-state refs.
Actor ignore is an immutable terminal proposal decision and cannot overwrite a
goal or canonical state. Gate 19 stays pending until the M88 real playable
qualification. G91C is next; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91C (2026-08-26)

G91C PASS. CANON, DIRECTED, LIVING, and EXPERIMENT now have explicit allowed
proposal contracts, immutable mode transitions, and audit records. Policy
evaluation never exposes Commit Authority. Gates 17-18 stay pending until the
M88 real playable qualification. G91D is next; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91D (2026-08-26)

G91D PASS. `CanonAttractorPolicy` measures normalized soft/hard constraint
distance and recommends a new branch on major divergence while preserving the
observed actor choice. It never forces an action or mutates goals, state, or
history. Gates 17-19 stay pending until M88 qualification. G91E is next; v5.5
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91E (2026-08-26)

G91E PASS. Explicit time/event triggers, reversible artifact-linked
interventions, immutable experiment setup, and a real child branch created by
the existing runtime are covered. Parent events and state hash remain equal;
Gate 20 stays pending until M88 full qualification. G91F is next; v5.5
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91F (2026-08-26)

G91F PASS. Quest is a projection over Opportunity evidence, with required and
optional objectives and progress derived only from committed state/event refs.
Narrative text cannot fake progress and no Quest object can commit. Gates
19-20 stay pending until M88 qualification. G91G is next; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91G (2026-08-26)

G91G PASS. Matched pressure/no-pressure traces use the same seed, profile
fingerprint, and horizon, and emit deterministic metrics, deltas, hashes, and
validity envelope. The result is explicitly an engineering reference
benchmark with `scientific_claim=false`. G91H is next; Gates 16-20 remain
pending and v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest engineering checkpoint — G91H / M88 (2026-08-26)

G91H PASS. A rights-approved source-created WorldPackage entered the real
PlayableService world; an embodied actor committed an action, switched
CANON→LIVING, ignored an eligible Opportunity, and created an artifact-linked
experiment child branch through the existing runtime. Parent events and
semantic hash remained unchanged and child replay matched. Gates 16-20 are
**ACCEPTED**; M88 is complete. M89-G94 and final release gates remain pending;
v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G91H_REPORT.md` and `reports/M88_QUALIFICATION.md`.

## Latest engineering checkpoint — G92A (2026-08-26)

G92A PASS. The long-horizon substrate now emits deterministic recurring
occurrences from a priority queue, records actor availability and catch-up,
and advances only monotonically. A real SQLite WorldRuntime qualification
adapted those occurrences into the existing temporal Commit path; no scheduler
authority or second event store was introduced. Gate 21 remains pending until
G92G; G92B-G97J remain pending and v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G92A_REPORT.md`.

## Latest engineering checkpoint — G92B (2026-08-26)

G92B PASS. Existing Playable RuntimeProfile values now drive paused, realtime,
accelerated, background, and full-autonomy offline policy. A leave cursor can
be consumed without a live user session and re-entered after scheduler
occurrences are adapted through the existing temporal Commit path. Gate 21
remains pending until G92G; G92C-G97J remain pending and v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G92B_REPORT.md`.

## Latest engineering checkpoint — G92C (2026-08-26)

G92C PASS. Cursor-only RunCheckpoint records are atomically published with
sequence/event-head monotonicity, deterministic crash injection, and exact
scheduler restore. A real Runtime retry after simulated restart returned the
existing committed event and produced no duplicate world effect. Gate 25
remains pending until M89 long-run qualification; G92D-G97J remain pending and
v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G92C_REPORT.md`.

## Latest engineering checkpoint — G92D (2026-08-26)

G92D PASS. Snapshot cadence and reference-only event/memory compaction now
produce deterministic archive refs while preserving the existing append-only
EventStore. Real Runtime golden replay hashes match before and after the
manifest, and event count/sequence are unchanged. Gate 26 remains pending
until M89 qualification; G92E-G97J remain pending and v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G92D_REPORT.md`.

## Latest engineering checkpoint — G92E (2026-08-26)

G92E PASS. L0-L4 activity scoring, deterministic transitions, L3/L4 cohort
aggregation, and promotion back to L0 preserve World-owned state/memory refs.
Real Runtime canonical hash and event count remain unchanged because LOD is a
projection/worker boundary. Gate 27 remains pending until M89 qualification;
G92F-G97J remain pending and v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.
Evidence: `reports/G92E_REPORT.md`.

## Latest engineering checkpoint — G92F (2026-08-26)

G92F PASS. World/actor/provider cost admission covers calls, tokens, time,
storage, alerts, soft/hard backpressure, and graceful LOD degradation with no
partial charge. Real Runtime truth remains unchanged while budget decisions
are projected. Gate 28 remains pending until M89 quantification; G92G-G97J
remain pending and v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G92F_REPORT.md`.

## Latest engineering checkpoint — G92G (2026-08-26)

G92G PASS. A real SQLite town WorldRuntime ran deterministic accelerated 24h
and 7d world-time horizons with multiple actors, daily checkpoints, replay /
restart recovery, bounded storage metrics, and reference compaction equality.
Gates 21-22 are **ACCEPTED**; Gate 23/24 and later M89+ gates remain pending,
so v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G92G_REPORT.md`.

## Latest engineering checkpoint — G90F (2026-08-26)

G90F PASS. Publishing profiles now separate visibility, rights summary,
package metadata, and safety extension refs; blocked rights stop publication,
and private/family-private profiles never list in Plaza. Gates 12-15 remain
pending until the full M87 qualification.

## Latest engineering checkpoint — G90E (2026-08-26)

G90E PASS. Scenario/Experience edits share the versioned workshop draft,
validate package references and product contracts, and produce a hashed
read-only preview without publish/runtime mutation. Gates 12-15 remain pending
until the full M87 qualification.

## Latest engineering checkpoint — G90D (2026-08-26)

G90D PASS. Hybrid Genesis now preserves source/prompt alternatives across E0-E5
with configurable precedence, explicit conflict review, and origin traces.
Generated claims cannot silently overwrite explicit source claims. Gates 12-15
remain pending until the full M87 qualification.

## Latest engineering checkpoint — G90C (2026-08-26)

G90C PASS. Prompt Genesis reuses the ProviderRouter with a typed missing-
provider result, private-safe deterministic local provider, bounded checkpoint,
and strict E5/candidate-only output validation. Gates 12-15 remain pending
until the full M87 qualification.

## Latest engineering checkpoint — G90B (2026-08-26)

G90B PASS. `CreatorIntent` now produces explicit, provenance-bound E5
constraints/domain suggestions/claims behind a three-action review gate;
directive-like prompt text is not executed or promoted to world facts. Gates
12-15 remain pending until the full M87 qualification.
