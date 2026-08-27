# v5.5 M85-M94 Acceptance Matrix

Status at G96B: **IN_PROGRESS / NOT_ACCEPTED**. This ledger is frozen for the
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
| 23 | 30-day literary run | ACCEPTED | G92H real SQLite source-created literary world, 30d / 3,000 ticks, two actors, replay/recovery equality |
| 24 | 90-day selected-world run | PENDING | — |
| 25 | Checkpoint/resume/crash recovery | ACCEPTED | G92H 30 successful run checkpoints, exact cursor resume, restart hash equality, and atomic crash probe |
| 26 | Compaction replay equality | ACCEPTED | G92H reference-only compaction with 155-event source count, 12 memory-summary refs, and equal golden hash |
| 27 | LOD transition continuity | ACCEPTED | G92H source actors retain state/memory refs across observed L0/L3/L4 transitions |
| 28 | Cost/storage/memory quantification | ACCEPTED | G92H 1,832→31,968 serialized bytes, 60 actor memories, 150 world calls, 30,136 charged storage bytes |
| 29 | Evolution delta taxonomy separation | ACCEPTED | G93A typed six-kind records, provenance policy, no-generic-blob and real product-chain evidence |
| 30 | 30-day Actor/Relationship/Organization evolution | ACCEPTED | G93H M90 30d qualification: 3,000 ticks, nonzero Actor/Relationship/Organization changes, source/package unchanged, append-only history and replay equality |
| 31 | Evolution explainability/replay | ACCEPTED | G93G typed delta reason/source/event/trajectory explanation projection and real product-chain replay evidence |
| 32 | Source/canon immutability | PENDING | — |
| 33 | Positive/negative pattern benchmark | ACCEPTED | G94H real positive/negative playable worlds with cross-window and same-window controls |
| 34 | Evidence-backed emergence candidate | ACCEPTED | G94H three-window Norm→Institution→Ontology candidate and provenance |
| 35 | High-level promotion review | ACCEPTED | G94H authorized review plus Constitution-gated ontology validation |
| 36 | False-positive controls | ACCEPTED | G94H same-window burst remains unqualified and cannot form NormCandidate |
| 37 | No universal-emergence claim | ACCEPTED | G94H report explicitly limits result to the qualified test scope |
| 38 | WorldRunArtifact re-verification | ACCEPTED | G95A artifact unit + real private-source product-chain round-trip/tamper evidence |
| 39 | Recoverable Experiment Registry | ACCEPTED | G95B versioned definition/run records, atomic claim, revision guard, recovery and snapshot round-trip |
| 40 | Fork/intervention parent isolation | ACCEPTED | G95C explicit snapshot/event fork, append-only intervention ledger, child replay resume, and real private-source parent-isolation evidence |
| 41 | Four or more parallel worldlines | PENDING | — |
| 42 | Multi-provider/policy or mixed population | ACCEPTED | G95E deterministic assignment + same-input mixed-population product-chain evidence |
| 43 | Worldline trajectory/cost comparator | ACCEPTED | G95F complete five-plane alignment, all-key diffs, and sanitized API/visual real-chain evidence |
| 44 | ValidationProfile V0-V7, unknown != pass | ACCEPTED | G95G independent profile/report/stack, real private-source chain, and V7 UNKNOWN non-acceptance evidence |
| 45 | Physical Provider ABI | ACCEPTED | G96A contract + SQLite product-chain boundary evidence |
| 46 | Visual Provider ABI | ACCEPTED | G96B contract + SQLite projection boundary evidence |
| 47 | Reference physical provider E2E | PENDING | — |
| 48 | Reference visual projection E2E | PENDING | — |
| 49 | Multi-perspective privacy isolation | PENDING | — |
| 50 | Provider output cannot write reality | ACCEPTED | G96A/G96B proposal/projection-only contracts + unchanged SQLite reality |
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

## Latest checkpoint — G96B / M93 (2026-08-27)

G96B PASS. Evidence: `reports/G96B_REPORT.md`; immutable scene state and actor
perspective records produce sanitized projection frames with explicit
snapshot/event refs, asset refs, state hash, and projection hash. Audience and
rights policy is not copied into frame objects. A fresh SQLite WorldRuntime
projection probe kept canonical hash and event history unchanged. Gates 46 and
50 are ACCEPTED; G96C-G97J and Gates 47-49, 51-52, 56-60 remain pending; release
status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G96A / M93 (2026-08-27)

G96A PASS. Evidence: `reports/G96A_REPORT.md`; immutable physical snapshot
and simulation request records cross a versioned `PhysicalWorldProvider`
protocol, and resolution output is the existing proposal-only
`ProposedWorldDelta` with replay/evidence refs. A fresh SQLite WorldRuntime
product-chain probe kept the canonical hash and event history unchanged. Gate
45 is ACCEPTED; G96B-G97J and Gates 46-52, 56-60 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95H / M92 (2026-08-27)

G95H PASS. Evidence: `reports/G95H_REPORT.md` and
`reports/M92_QUALIFICATION.md`; one real private literary source produced a
four-worldline registry batch, typed intervention fork/resume, complete
five-plane comparison, and sanitized hash-verifiable RunArtifacts through the
existing WorldPackage → PlayableService → SQLite chain. M92 is PASS for this
laboratory scope. Gate 41 remains pending because the real SQLite run was
serial and does not prove four parallel worldlines; G96A-G97J and Gates 45-52,
56-60 remain pending; release status remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95G (2026-08-27)

G95G PASS. Evidence: `reports/G95G_REPORT.md`; the independent versioned
ValidationProfile/Report/Stack covers V0-V7 and fills missing evidence with
`unknown`. A real private-source WorldPackage → Preview/Living Instance →
SQLite chain produced complete checks, but V7 external calibration remains
UNKNOWN, so `ValidationReport.accepted` is false. Gate 44 is accepted for the
implementation and evidence-semantics boundary; this is not a scientific
validity claim. Gate 41 remains pending because the G95D SQLite qualification
was serial; G95H-G97J and Gates 45-52, 56-60 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95F (2026-08-27)

G95F PASS. Evidence: `reports/G95F_REPORT.md`; sanitized baseline/candidate
WorldRunArtifact measurements aligned on one private-source input across Actor,
Relation, Institution, Macro, and Cost planes. All aligned keys are retained,
missing/extra metrics block qualification, and the API/visual report contains
refs plus numeric series only. Real SQLite branches preserved separate event
streams, normal Commit Authority evidence, and replay equality. Gate 43 is
accepted; Gate 41 remains pending because G95D's real SQLite qualification was
serial; G95G-G97J and Gates 44-52, 56-60 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95E (2026-08-27)

G95E PASS. Evidence: `reports/G95E_REPORT.md`; versioned deterministic
provider assignment and four-member mixed-population execution used the same
private source/package/scenario input across two private-safe reference
providers. Provider outputs remained `ProviderProposal` values, activation
was recorded only in `RuntimeControlLedger`, and the real SQLite event stream
was unchanged until the later normal Playable Commit Authority action. Gate 42
is accepted; Gate 41 remains pending because G95D's real SQLite qualification
was serial; G95G-G97J and Gates 44-52, 56-60 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95D (2026-08-27)

G95D PASS. Evidence: `reports/G95D_REPORT.md`; one registry definition
produced four seed/parameter worldlines with bounded worker execution,
versioned checkpoints, recovery, and all-row aggregation. The real private
source chain retained per-run WorldPackage/SQLite snapshot/RunArtifact/replay
evidence. Gate 41 remains pending because the real SQLite qualification was
serial; G95F-G97J and Gates 43-52, 56-60 remain pending; release status
remains **IN_PROGRESS / NOT_ACCEPTED**.

## Latest checkpoint — G95C (2026-08-27)

Gate 40 **ACCEPTED**. Evidence: `reports/G95C_REPORT.md`; the real private
rights-approved source chain produced both an event-selected and an explicit
snapshot-revision child branch. Parent event history/hash stayed unchanged,
and child resume required replay-hash equality. G95D-G97J and Gates 41-52,
56-60 remain pending; release status remains **IN_PROGRESS / NOT_ACCEPTED**.

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

## Latest engineering checkpoint — G92H / M89 long-run evidence (2026-08-26)

G92H PASS. The same private, rights-approved source-created literary
WorldPackage entered PlayableService and ran on the real SQLite WorldRuntime
for accelerated 30d / 3,000 world ticks. Two source actors produced 30
actor-local memories each; 30 runtime checkpoints, exact scheduler-cursor
resume, atomic crash rejection, restart replay equality, reference-only
compaction, LOD continuity, and measured cost/storage growth all passed. Gates
23 and 25-28 are **ACCEPTED**. Gate 24 and all M90-M94/final release gates
remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G92H_REPORT.md`.

## Latest engineering checkpoint — G93A (2026-08-27)

G93A PASS. Six explicit immutable evolution Delta records now separate State,
Belief, Relationship, Capability, Persona, and Organization payloads. All carry
schema/version and evidence/event provenance; generic evolution blobs are
rejected. `EvolutionCommitPolicy` validates proposal provenance and creates only
an explicit receipt for an already committed canonical event, so it cannot
mutate World Truth or create a second event store. A real private source-created
WorldPackage traversed PlayableService, Preview, and SQLite WorldRuntime before
the six proposals were validated; canonical hash/event count stayed unchanged.
Gate 29 is **ACCEPTED**. G93B-G97J, Gate 24, and the remaining M90-M94 gates
remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G93A_REPORT.md`.

## Latest engineering checkpoint — G93B (2026-08-27)

G93B PASS. `CapabilityCandidate` now requires domain support, validates
prerequisites and composition, aggregates practice evidence, distinguishes
successful and failed assessments, and creates a proposal-only promotion to
the existing actor-skill resolver. Impossible capabilities and
failure-dominant evidence are rejected. A private source-created package ran
through PlayableService/Preview/SQLite before a validated promotion was
committed and replayed; the actor skill retained the candidate evidence refs.
Gate 30 remains pending until G93H's 30-day Actor/Relationship/Organization
run. G93C-G97J and Gate 24 remain pending; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G93B_REPORT.md`.

## Latest engineering checkpoint — G93C (2026-08-27)

G93C PASS. Six bounded persona trait dimensions now use slow-variable,
multi-event windows and deterministic weighted changes. A single event or
short window cannot rewrite a persona; proposals are one-trait, review-gated,
and carry the existing `PersonaDelta` evidence lineage. A real private source
product chain supplied committed event refs, while the approved projection
change left canonical hash/event count and replay unchanged. Gate 30 remains
pending until G93H's 30-day Actor/Relationship/Organization run. G93D-G97J
and Gate 24 remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.
Evidence: `reports/G93C_REPORT.md`.

## Latest engineering checkpoint — G93D (2026-08-27)

G93D PASS. Relationship events now map through exactly-one typed delta rule,
bounded/clamped dimensions, actor/relation invariants, and proposal-only
provider output. Reviewed proposals reuse the existing RelationshipGraph
projection history and replay equal; behavior feedback is read-only. A real
private source-created product chain supplied committed event evidence and
the approved relationship projection left canonical hash/event count unchanged.
Gate 30 remains pending until G93H's 30-day Actor/Relationship/Organization
run. G93E-G97J and Gate 24 remain pending; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G93D_REPORT.md`.

## Latest engineering checkpoint — G93E (2026-08-27)

G93E PASS. Organization lifecycle is a typed, proposal-only projection over
the existing institution query: create/join/leave/role/permission/dissolve/
split, role authority, resource partitioning, and explicit review are covered.
Leaving removes memberships and delegated grants; effective permission
queries reject orphan recipient/granter references. Split drops cross-partition
grants and conserves resources. A real private source → WorldPackage →
PlayableService → Preview → SQLite Runtime chain supplied event provenance,
while canonical hash/revision/event count and replay stayed unchanged. Gate 30
remains pending until G93H's integrated 30-day run; G93F-G97J and Gate 24
remain pending. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G93E_REPORT.md`.

## Latest engineering checkpoint — G93F (2026-08-27)

G93F PASS. Reputation now has typed local/global immutable projections, with
observer-specific views where applicable, weighted bounded changes, source and
committed-event provenance, explicit review, and stale-state rejection. Belief
and rumor are rejected as reputation evidence. Social roles are independent
review-gated projections and cannot mutate institution roles, permissions, or
canonical state. A private source → WorldPackage → PlayableService → Preview →
SQLite Runtime chain supplied a real committed event; canonical hash,
revision, event count, and replay remained unchanged. Gate 30 remains pending
until G93H's integrated 30-day run; G93G-G97J, Gate 24, and the remaining
release gates remain pending. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.
Evidence: `reports/G93F_REPORT.md`.

## Latest engineering checkpoint — G93G (2026-08-27)

G93G PASS. The typed evolution deltas now expose queryable reasons, subjects,
projection refs, deterministic fingerprints, source/event lineage, and
explicit links to existing ActorEvolution trajectories. Relationship and
organization subjects remain typed; provider-only provenance is rejected. A
private source → WorldPackage → PlayableService → Preview → SQLite Runtime
chain supplied the real committed event, while canonical hash, revision, event
count, and replay stayed unchanged. Gate 31 is **ACCEPTED**. Gate 30 remains
pending until G93H's integrated 30-day run; G93H-G97J, Gate 24, and the
remaining release gates remain pending. v5.5 remains **IN_PROGRESS /
NOT_ACCEPTED**. Evidence: `reports/G93G_REPORT.md`.

## Latest engineering checkpoint — G94H / M91 (2026-08-27)

G94H PASS and M91 is complete within scope. A real private rights-approved
source traversed OneClickAuthoring → WorldPackage → Preview → PlayableService
→ SQLite WorldRuntime. The positive world produced three disjoint repeated
cross-window detections, NormCandidates, a reviewed InstitutionCandidate, and a
reviewed OntologyCandidate; canonical history, Constitution hash, and replay
remained unchanged. The negative world produced a same-window burst that stayed
unqualified and could not form a NormCandidate. Gates 33-37 are **ACCEPTED**;
Gate 24 and Gates 32, 38-52, and 55-60 remain pending. This is bounded evidence
of one qualified pattern, not a universal-emergence claim. G95A-G97J remain
pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G94H_REPORT.md`.

## Latest engineering checkpoint — G94G / M91 (2026-08-27)

G94G PASS. The existing L0-L8 promotion ladder now carries policy-version,
world-count, benchmark, sandbox, rollback-readiness, and high-level-review
evidence. M91 L0-L5 requirements increase evidence/world thresholds; L4
requires a passing benchmark and sandbox, and L5 additionally requires
rollback readiness and explicit review. Existing PlatformFeedbackLab and
PromotionControlLedger remain the sandbox/release/withdrawal mechanisms;
promotion validation itself never writes Canon. A real SQLite runtime retained
the same canonical hash, event history, and replay after sandbox, versioned
release, rollback, and withdrawal qualification. G94H-G97J and Gates 24,
32-52, and 55-60 remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.
Evidence: `reports/G94G_REPORT.md`.

## Latest engineering checkpoint — G94F / M91 (2026-08-27)

G94F PASS. The existing `OntologyCandidate` now records strict long-window
evidence, norm/institution provenance, measured complexity/interpretability,
and an explicit reviewer decision. Creation requires three independent norm
records spanning three distinct windows, multi-window support, high support and
confidence, bounded exceptions, and low derived complexity; unreviewed
evidence-backed candidates are rejected by the existing ontology validator.
The real private rights-approved source chain produced three detections,
norms, and a reviewed institution before deriving the ontology candidate;
Constitution hash, canonical revision/hash, event history, and replay stayed
unchanged. G94G-G97J and Gates 24, 32-52, and 55-60 remain pending; v5.5
remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G94F_REPORT.md`.

## Latest engineering checkpoint — G94E / M91 (2026-08-27)

G94E PASS. The existing `InstitutionCandidate` now carries structured
rule/role/resource/process references and provenance, while a pure helper
derives the candidate from a `NormCandidate`. Explicit reviewer approval is
recorded separately and never invokes Commit Authority; incomplete structure
and unauthorized reviewers are rejected, and existing law promotion remains
an explicit controlled operation. A private rights-approved source traversed
OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
WorldRuntime; the resulting scoped norm produced a structured reviewed
institution candidate without changing canonical hash, revision, or replay.
G94F-G97J and Gates 24, 32-52, and 55-60 remain pending; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G94E_REPORT.md`.

## Latest engineering checkpoint — G94D / M91 (2026-08-27)

G94D PASS. `NormCandidate` requires a minimum population, explicit local or
global scope, repeated-window evidence, exception-rate bounds, and committed
event-linked reward/sanction correlation. Small samples and exception-heavy
patterns remain ineligible; candidate construction/evaluation is immutable and
does not activate a norm or write Canon. A private rights-approved source
traversed OneClickAuthoring → WorldPackage → Preview → PlayableService →
SQLite WorldRuntime; repeated committed status events over two subjects yielded
a scoped norm candidate with outcome evidence while canonical hash and replay
stayed unchanged. G94E-G97J and Gates 24, 32-52, and 55-60 remain pending;
v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G94D_REPORT.md`.

## Latest engineering checkpoint — G94C / M91 (2026-08-27)

G94C PASS. Qualified repeated detections can produce actor-local Habit/Skill
Candidate records with explicit evidence windows, event refs, stability,
confidence, decay, and an evaluation policy. Unqualified detections, missing
actors, insufficient windows, and stale/decayed evidence remain ineligible;
candidate creation and decay are immutable proposal operations with no
canonical commit path. A private rights-approved source traversed the real
OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
WorldRuntime chain; a repeated actor action yielded a skill candidate and
evaluation while canonical hash and replay stayed unchanged. G94D-G97J and
Gates 24, 32-52, and 55-60 remain pending; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G94C_REPORT.md`.

## Latest engineering checkpoint — G94B / M91 (2026-08-27)

G94B PASS. `RepeatedPatternDetector` applies deterministic occurrence,
window-support, confidence, and counterexample thresholds to the G94A derived
cache. Same-window duplicates do not satisfy multi-window stability, sparse or
one-off fixtures are returned as unqualified detections with concrete missing
windows, and no result becomes truth or a Candidate automatically. A private,
rights-approved source traversed the real OneClickAuthoring → WorldPackage →
Preview → PlayableService → SQLite WorldRuntime chain; repeated committed
actions produced a qualified behavior detection while canonical hash, replay,
and event history stayed unchanged. G94C-G97J and Gates 24, 32-52, and 55-60
remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G94B_REPORT.md`.

## Latest engineering checkpoint — G94A / M91 (2026-08-27)

G94A PASS. `PatternObservationStore` derives typed behavior, relationship,
exchange, and organization observations, windowed statistics, feature means,
and committed event references from the existing immutable event stream. The
cache is deterministic under reordered input and remains rebuildable; it owns
no EventStore, Branch, Candidate, or Commit Authority. A private,
rights-approved source traversed OneClickAuthoring → WorldPackage → Preview →
PlayableService → SQLite WorldRuntime, and the observation cache was rebuilt
from the resulting committed events without changing canonical hash, revision,
event refs, source bytes, or replay. G94B-G97J and Gates 24, 32-52, and 55-60
remain pending; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**. Evidence:
`reports/G94A_REPORT.md`.

## Latest engineering checkpoint — G93H / M90 (2026-08-27)

G93H PASS. A deterministic private, rights-approved source traversed the real
OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
WorldRuntime chain and ran for 30 days / 3,000 world ticks. The baseline and
evolved snapshots show nonzero Actor, Relationship, and Organization changes
with 7 validated reviewed deltas, while the source payload/hash and package
identity remained unchanged. The canonical event history grew only through
the existing Commit Authority path, retained its baseline prefix, and replayed
to the same hash. Gate 30 is **ACCEPTED** and M90 is complete. G93I-G97J,
Gate 24, and the remaining release gates remain pending; v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**. Evidence: `reports/G93H_REPORT.md`.

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
