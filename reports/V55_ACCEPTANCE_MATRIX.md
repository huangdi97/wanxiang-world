# v5.5 M85-M94 Acceptance Matrix

Status at G88A: **IN_PROGRESS / NOT_ACCEPTED**. This ledger is frozen for the
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
| 12 | From Source regression | PENDING | — |
| 13 | From Prompt E5 Candidate/WorldDraft | PENDING | — |
| 14 | Hybrid E0-E5 provenance | PENDING | — |
| 15 | Publish visibility/rights gates | PENDING | — |
| 16 | PressureProfile outside Kernel | PENDING | — |
| 17 | CANON/DIRECTED/LIVING/EXPERIMENT modes | PENDING | — |
| 18 | Director has no Commit authority | PENDING | — |
| 19 | Opportunity can be ignored | PENDING | — |
| 20 | Intervention branch/artifact isolation | PENDING | — |
| 21 | 24-hour smoke | PENDING | — |
| 22 | 7-day runtime | PENDING | — |
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
| 53 | v5.4 critical regression | ACCEPTED | G88A baseline: 1219 passed, 1 skipped |
| 54 | Full Python/TypeScript quality | ACCEPTED | G88A baseline: local Python and prior stable TS evidence |
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
