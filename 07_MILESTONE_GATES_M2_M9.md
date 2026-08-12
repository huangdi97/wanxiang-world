# Milestone Gates M2–M9

> System-level acceptance gates for the continuation program.

## M2 — Deterministic Living World Exists

**Integrated scenario:** Run a source-neutral synthetic house/micro-town for at least 72 in-world hours with multiple actors, rooms/portals, schedules, material objects, a sealed information payload, body constraints, duties/permissions and background population scheduling.

**Must prove:**
- World time is monotonic and can pause/advance without wall-clock dependence.
- Spatial reachability, access, capacity and occupancy invariants hold.
- Material custody/ownership/container state is conserved; acquiring a sealed message does not imply reading it.
- Body/condition state can block or alter an otherwise valid action/schedule.
- Institution roles/duties/permissions affect allowed actions.
- With no user input, scheduler advances the world deterministically under resource budgets.
- Snapshot/replay/branch/idempotency/stale-revision invariants from M1 remain green.
- Same initial snapshot + seed + versions yields identical final semantic hash and ordered committed events.

Detailed executable gate: `milestones/M2_QUALIFICATION.md`

## M3 — Bounded Agents Can Live Inside the World

**Integrated scenario:** Use a deterministic synthetic scenario with at least two actors and one organization. One actor observes a private/partial event, forms a belief, later receives a correction, executes a multi-step skill, and changes a bounded capability. Another actor must not receive knowledge they never observed or were not told.

**Must prove:**
- Observation, belief, memory and canonical truth are separate data concepts.
- Temporal epistemic graph preserves contradiction/correction lineage.
- Actors and organizations propose through policies; no policy owns Commit Authority.
- Affordances and ActionValidator reject unreachable, unauthorized or epistemically impossible actions.
- Resolver outputs auditable adjudication/proposed deltas with version/seed provenance.
- Skill execution is resumable and every step still passes normal validation.
- Capability change requires declared practice/assessment evidence and remains bounded.
- Knowledge-leakage and deterministic policy tests pass.

Detailed executable gate: `milestones/M3_QUALIFICATION.md`

## M4 — Worlds Can Be Authored, Reviewed, Installed and Instantiated

**Integrated scenario:** Author a synthetic Domain Pack + World Pack + Scenario using supported JSON/YAML/Markdown inputs, run them through Source/Review/Compiler/Registry, install them, instantiate a pinned world, export/re-import, then publish a v2 package without silently mutating the v1 instance.

**Must prove:**
- Package hierarchy and dependency/version resolution are deterministic.
- Untrusted executable extensions are denied by default.
- Source Gate blocks unapproved/rights-denied/malicious content from canonical compilation.
- Conflicting claims survive as separate evidence-backed candidates.
- Compiler MVP supports only declared formats; unsupported PDF/OCR/video is explicit, not faked.
- Canon/completion/model/reconstruction/user-fiction labels are preserved.
- Install/export round-trip works and package hashes/version pins are checked.
- Package/schema migration compatibility is tested.

Detailed executable gate: `milestones/M4_QUALIFICATION.md`

## M5 — Human Can Enter a Persistent World Without Becoming the Authority

**Integrated scenario:** Run a hosted synthetic world with Studio and Phaser clients. Acquire an embodiment lease, take over one actor, commit actions, release control, allow the AI/deterministic policy to resume, disconnect all clients while the world continues, restart the process, reconnect, and verify authoritative continuity.

**Must prove:**
- WorldHost is an orchestration boundary, not a second Commit Authority.
- Exactly one primary embodiment controller exists per actor.
- ShadowPolicy cannot compete for authoritative body control.
- Projection filters enforce knowledge/rights server-side.
- Studio edits and Phaser movement use command APIs and cannot mutate client-local truth into canonical truth.
- Lifecycle modes persist independently of sessions.
- Multi-client retries/conflicts remain idempotent and revision-safe.
- Crash recovery, lease recovery and scheduler restoration preserve canonical semantic hash.

Detailed executable gate: `milestones/M5_QUALIFICATION.md`

## M6 — Reality-Coupled Context and Controlled Experiments Work Safely

**Integrated scenario:** Feed deterministic fake physical observations with duplicates/conflicts into Reality Bridge, fuse them, generate at least one opportunity/challenge, let a Director propose an external event under constraints, and run a multi-seed experiment from a fixed baseline.

**Must prove:**
- PhysicalObservation remains observation, never direct truth.
- Fusion preserves conflicting inputs/provenance and emits only claims/proposals.
- ChallengeSpec includes executable prerequisites, safety/rights/evidence and verifiable outcome requirements.
- Director layers cannot directly commit or rewrite actor beliefs/personality.
- Experiment branches never mutate baseline.
- Results include run/seed/version metrics, assumptions and ValidityEnvelope.
- Same deterministic experiment spec reproduces the same result set.
- All proposals still traverse normal validation/adjudication/commit.

Detailed executable gate: `milestones/M6_QUALIFICATION.md`

## M7 — Multiple Unrelated Domains Prove Core Generality

**Integrated scenario:** Pass system qualification using at least three unrelated domain families: synthetic mansion/literature, family genealogy/archive, and heritage/museum. Real Red Chamber data is used only if Source Gate allows it.

**Must prove:**
- Synthetic mansion passes seven-day persistence/control/knowledge/material/branch checks without Core hacks.
- Family supports GEDCOM round-trip profile, source retention, conflicting claims and living-person privacy.
- Family persona modes clearly distinguish evidence/reconstructed/creative outputs and enforce revocation.
- Heritage supports IIIF references plus selected Linked Art/CIDOC mapping profile.
- Physical object, digital surrogate, semantic twin and reconstruction remain distinct.
- Object biography/conservation history is replayable and rights/cultural protocols are enforced.
- Domain-specific rules remain plugins/packages above Core.
- Real-source slices may be EXTERNAL_BLOCKED, but Source Gate negative/positive fixture behavior must PASS.

Detailed executable gate: `milestones/M7_QUALIFICATION.md`

## M8 — Mechanistic External Models Can Participate Without Owning Canonical State

**Integrated scenario:** Run a synthetic campaign with at least two deterministic fake simulators operating at different rates, organization orders, logistics/resource flow, movement constraints and fog-of-war; then execute batch experiments across multiple seeds/variants.

**Must prove:**
- SimulationAdapter implements the complete declared contract including checkpoint/restore/assumptions/validity.
- Adapters receive slices/snapshots and only emit events/proposed deltas.
- Multi-rate/event-driven ordering is deterministic and restartable.
- Conflicting simulator proposals are adjudicated explicitly.
- Campaign logistics/position/resource invariants hold.
- Faction observations/beliefs respect fog-of-war.
- Batch results are distributions with verification/validation/ValidityEnvelope metadata.
- Liaoshen real pack never fabricates missing history and may be EXTERNAL_BLOCKED without blocking generic M8.

Detailed executable gate: `milestones/M8_QUALIFICATION.md`

## M9 — Release-qualified Wanxiang Platform Foundation

**Integrated scenario:** Run complete release qualification: long-duration synthetic world, full regression from M1-M8, backup/restore/migrations, SDK generation/examples, research/projection/foundry/digital-human adapter contracts, and supported local/private deployment security checks.

**Must prove:**
- At least 30 in-world days and 1000+ commit/scheduler cycles complete with no invariant failure and bounded resource growth.
- Backup restored into a clean environment reproduces canonical hashes and old fixture databases migrate/replay.
- OpenAPI/TypeScript SDK generation is reproducible; public API vocabulary/version policy is documented.
- Gymnasium/PettingZoo adapters preserve authority and epistemic filtering when optional dependencies are installed.
- Godot/Babylon projection contracts, Asset Foundry and Digital Human/XR gateways remain non-authoritative.
- Rights prevent unauthorized asset/voice/face generation calls.
- Security tests cover secrets, uploads/source injection, admin/debug/private/export access and audit protection.
- Fresh-clone local startup/runbook works; external-only environment checks are explicitly labeled rather than falsely passed.
- Complete architecture, migration, replay, source-gate, rights, projection-leakage and long-run regression matrix is green.

Detailed executable gate: `milestones/M9_QUALIFICATION.md`
