# Status ? Wanxiang Engineering Program

Updated: 2026-08-11 (batch start)

## Milestones

| Milestone | Meaning | Status |
|---|---|---|
| M0 | Reproducible Engineering Base | PASS (2026-08-12) |
| M1 | Authoritative World Exists | PASS (2026-08-12) |

## Goal status

| Goal | Status |
|---|---|
| GOAL_00A Repository & Toolchain Foundation | PASS (2026-08-11) |
| GOAL_00B Architecture Guards & Engineering Constitution | PASS (2026-08-12) |
| GOAL_01A Core Semantic Contracts | PASS (2026-08-12) |
| GOAL_01B Commit Authority & Core Invariants | PASS (2026-08-12) |
| GOAL_01C Event Store / Ordering / Idempotency / Concurrency | PASS (2026-08-12) |
| GOAL_01D Snapshot / Replay / Branch / Determinism | PASS (2026-08-12) |
| GOAL_01E Persistence / Migration / Recovery Foundation | PASS (2026-08-12) |
| GOAL_01F Minimal World Vertical Slice + M1 Qualification | PASS (2026-08-12) |

## Current HEAD

- Branch: main
- Batch complete: M0 PASS + M1 PASS; tag `m1-authoritative-world`.
- Stop condition met: do NOT start G02A until M1 evidence is reviewed.

## M2?M9 continuation (2026-08-13)

M1 re-verified on this tree: `uv run python scripts/quality.py` -> PASS (130 tests),
A1?A10 PASS at commit c45b64e. M0/M1 are NOT being re-implemented.

### Milestones

| Milestone | Meaning | Status |
|---|---|---|
| M2 | Deterministic Living World Exists | PASS (2026-08-13, tag m2-deterministic-living-world) |
| M3 | Bounded Agents Can Live Inside the World | PASS (2026-08-13, tag m3-bounded-agents) |
| M4 | Worlds Can Be Authored, Reviewed, Installed, Instantiated | PASS (2026-08-13, tag m4-worlds-authored-installed) |
| M5 | Human Can Enter a Persistent World Without Becoming Authority | PASS (2026-08-13, tag m5-human-in-world-without-authority) |
| M6 | World Can Be Safely Coupled to External Context and Controlled Experiments | PASS (2026-08-13, tag m6-reality-experiments) |
| M7 | Multiple Unrelated Domains Prove Core Generality | NOT_STARTED |
| M8 | Mechanistic External Models Participate Without Owning Canonical State | NOT_STARTED |
| M9 | Release-qualified Wanxiang Platform Foundation | NOT_STARTED |

### Goals (55)

| Goal | Status |
|---|---|
| G02A Spatial Topology & Access | PASS (2026-08-13, commit goal g02a) |
| G02B Temporal System & Schedules | PASS (2026-08-13, commit goal g02b) |
| G02C Material/Container/Custody/Information Payload | PASS (2026-08-13, commit goal g02c) |
| G02D Body & Condition Constraints | PASS (2026-08-13, commit goal g02d) |
| G02E Institution/Authority/Duty/Norm | PASS (2026-08-13, commit goal g02e) |
| G02F Population Resolution & Autonomous Scheduler | PASS (2026-08-13, commit goal g02f) |
| G03A Observation & Perspective Isolation | PASS (2026-08-13, commit goal g03a) |
| G03B Belief/Memory/Temporal Epistemic Graph | PASS (2026-08-13, commit goal g03b) |
| G03C Actor & Organization Runtime | PASS (2026-08-13, commit goal g03c) |
| G03D Action/Affordance/Validator | PASS (2026-08-13, commit goal g03d) |
| G03E Resolver/Adjudication/Deterministic Policies | PASS (2026-08-13, commit goal g03e) |
| G03F Skill Runtime | PASS (2026-08-13, commit goal g03f) |
| G03G Capability & Learning | PASS (2026-08-13, commit goal g03g) |
| G04A Package, Schema & Dependency Registry | PASS (2026-08-13, commit goal g04a) |
| G04B Source Registry & Source Gate | PASS (2026-08-13, commit goal g04b) |
| G04C Structured Compiler MVP | PASS (2026-08-13, commit goal g04c) |
| G04D Completion Ledger & Review Workflow | PASS (2026-08-13, commit goal g04d) |
| G04E Package Install/Export/Migration Compatibility | PASS (2026-08-13, commit goal g04e) |
| G05A Minimal World Host & Authority Boundary | PASS (2026-08-13, commit goal g05a) |
| G05B Session/Embodiment/Lease | PASS (2026-08-13, commit goal g05b) |
| G05C Shadow/Human Policy Control Handoff | PASS (2026-08-13, commit goal g05c) |
| G05D Projection API/Perspective/Rights Filters | PASS (2026-08-13, commit goal g05d) |
| G05E Studio Debug Vertical Slice | PASS (2026-08-13, commit goal g05e) |
| G05F Phaser 2D Player Vertical Slice | PASS (2026-08-13, commit goal g05f) |
| G06A Persistent Lifecycle/Pause/Advance/Background | PASS (2026-08-13, commit goal g06a) |
| G06B Command Queue & Idempotent Multi-client Semantics | PASS (2026-08-13, commit goal g06b) |
| G06C Crash Recovery, Checkpoint & Resource Budget | PASS (2026-08-13, commit goal g06c) |
| G07A PhysicalObservation & Reality Bridge | PASS (2026-08-13, commit goal g07a) |
| G07B Observation Fusion & Validation | PASS (2026-08-13, commit goal g07b) |
| G07C Opportunity/Challenge/Event Compiler | PASS (2026-08-13, commit goal g07c) |
| G07D Director Runtime | PASS (2026-08-13, commit goal g07d) |
| G07E Experiment Runtime/Multi-run/ValidityEnvelope | PASS (2026-08-13, commit goal g07e) |
| G08A..G10D Domain Generality | NEXT |
| G05A Minimal World Host & Authority Boundary | PASS (2026-08-13, commit goal g05a) |
| G05B Session/Embodiment/Lease | PASS (2026-08-13, commit goal g05b) |
| G05C Shadow/Human Policy Control Handoff | PASS (2026-08-13, commit goal g05c) |
| G05D Projection API/Perspective/Rights Filters | PASS (2026-08-13, commit goal g05d) |
| G05E Studio Debug Vertical Slice | PASS (2026-08-13, commit goal g05e) |
| G05F Phaser 2D Player Vertical Slice | PASS (2026-08-13, commit goal g05f) |
| G06A Persistent Lifecycle/Pause/Advance/Background | PASS (2026-08-13, commit goal g06a) |
| G06B Command Queue & Idempotent Multi-client Semantics | PASS (2026-08-13, commit goal g06b) |
| G06C Crash Recovery, Checkpoint & Resource Budget | PASS (2026-08-13, commit goal g06c) |
| G07A PhysicalObservation & Reality Bridge | PASS (2026-08-13, commit goal g07a) |
| G07B Observation Fusion & Validation | PASS (2026-08-13, commit goal g07b) |
| G07C Opportunity/Challenge/Event Compiler | PASS (2026-08-13, commit goal g07c) |
| G07D Director Runtime | PASS (2026-08-13, commit goal g07d) |
| G07E Experiment Runtime/Multi-run/ValidityEnvelope | PASS (2026-08-13, commit goal g07e) |
| G08A..G10D Domain Generality | NEXT |
| G06A Persistent Lifecycle/Pause/Advance/Background | PASS (2026-08-13, commit goal g06a) |
| G06B Command Queue & Idempotent Multi-client Semantics | PASS (2026-08-13, commit goal g06b) |
| G06C Crash Recovery, Checkpoint & Resource Budget | PASS (2026-08-13, commit goal g06c) |
| G07A PhysicalObservation & Reality Bridge | PASS (2026-08-13, commit goal g07a) |
| G07B Observation Fusion & Validation | PASS (2026-08-13, commit goal g07b) |
| G07C Opportunity/Challenge/Event Compiler | PASS (2026-08-13, commit goal g07c) |
| G07D Director Runtime | PASS (2026-08-13, commit goal g07d) |
| G07E Experiment Runtime/Multi-run/ValidityEnvelope | PASS (2026-08-13, commit goal g07e) |
| G08A..G10D Domain Generality | NEXT |
| G07A PhysicalObservation & Reality Bridge | PASS (2026-08-13, commit goal g07a) |
| G07B Observation Fusion & Validation | PASS (2026-08-13, commit goal g07b) |
| G07C Opportunity/Challenge/Event Compiler | PASS (2026-08-13, commit goal g07c) |
| G07D Director Runtime | PASS (2026-08-13, commit goal g07d) |
| G07E Experiment Runtime/Multi-run/ValidityEnvelope | PASS (2026-08-13, commit goal g07e) |
| G08A..G10D Domain Generality | NEXT |
| G08A..G10D Domain Generality | NEXT |
| G11A..G11F Co-Simulation | NOT_STARTED |
| G12A..G12H Release | NOT_STARTED |
