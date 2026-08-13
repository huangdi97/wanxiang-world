# Wanxiang Post-M9 Engineering Program Architecture — M10 → M17

> Date: 2026-08-13
> Continuation after the v5.0-R1 M0–M9 implementation program.
> This program does **not** redefine the product. `docs/spec/WANXIANG_v5_MASTER_SPEC.md` remains the product/architecture source of truth for v5.0-R1.

## 1. Why a Post-M9 Program exists

M0–M9 can establish a broad implementation, but breadth itself is not proof. The next engineering risk is false completion: interfaces with no real vertical path, mock-only product surfaces, replay compatibility that only works for current fixtures, or a platform that passes its own tests but fails under independent audit, hostile inputs, long-horizon operation or clean-room deployment.

The Post-M9 program therefore changes the execution mode from **feature construction** to **proof, closure, adversarial qualification, black-box generality, production operation and controlled research expansion**.

## 2. Milestones

- **M10 — Independent Verification & Gap Closure:** do not trust prior PASS claims; trace every normative requirement to code, test and runtime evidence; close P0 and required P1 gaps.
- **M11 — Adversarial / Failure Qualification:** concurrency, crash, corruption, hostile package/source, auth/privacy, external simulator failures and resource exhaustion.
- **M12 — Reference World & Worldness Certification:** comprehensive synthetic world, seven-day and extended runs, human leave/rejoin, material/information continuity, branching and source-gated real reference slices.
- **M13 — Productionization & Operations:** PostgreSQL profile, queues/workers only as justified, assets, observability, security, backup/DR, CI/CD, capacity and private/staging deployment.
- **M14 — SDK / Plugin / World Pack Ecosystem:** stable public extension surface, authoring CLI, third-party certification, trust model, registry lifecycle and clean-room external pack.
- **M15 — Product Surface Completion:** Studio, Experience, Strategy, Family, Heritage, Learn and operator/admin surfaces all connected to the same authoritative world.
- **M16 — v5.1/v6 Research Expansion:** experimental AI compiler, long-horizon cognition, cognitive LOD, world-model planner, generative assets, digital human/XR, multi-simulator, reality streams and distribution experiments. Stable Core remains default.
- **M17 — Final Independent Certification:** final traceability, clean-room build/restore/replay, security/chaos rerun, black-box external author/end-user test and release readiness freeze.

## 3. Non-negotiable invariants carried forward

1. `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains the formal hierarchy.
2. Only Commit Authority may mutate Canonical World State.
3. LLMs, UIs, Directors, sensors, simulators, plugins and research models only propose/observe; they never own truth.
4. Event history, replay, snapshot, branch isolation and version compatibility remain release invariants.
5. Projection state is discardable/rebuildable; it cannot become an alternate save format.
6. Real literary/history/family/heritage data must pass Source/Evidence/Rights gates. Model memory is not a source.
7. Deterministic core tests remain network/API-key independent.
8. Security, rights, observability, migration and compatibility are continuous requirements.
9. Domain-specific reference worlds may expose generic Core gaps; fixes must generalize rather than hard-code the reference world.
10. Research code is experimental until evidence promotes it; feature flags OFF must preserve stable behavior.

## 4. Execution graph

```text
M9 PASS
  ↓
M10 Independent audit + gap closure
  ↓
M11 adversarial/failure qualification
  ↓
M12 reference-world/worldness qualification
  ↓
M13 productionization/operations
  ↓
M14 SDK/ecosystem black-box extensibility
  ↓
M15 product-surface completion
  ↓
M16 isolated research expansion
  ↓
M17 final independent certification
```

Milestones are gates. A failing stable-path gate blocks advancement. A narrowly external real-data/hardware/provider dependency may be `EXTERNAL_BLOCKED` only for that slice if generic capability and deterministic substitutes are fully implemented and tested.

## 5. Definition of Done for every Goal

Every Goal file is an executable engineering contract and must contain/obey:

- Objective
- Scope
- Non-goals
- Required reading
- Architecture constraints
- Deliverables
- Implementation tasks
- Tests
- Acceptance criteria
- Failure / blocker handling
- Documentation updates
- Git / checkpoint requirements

A Goal is not complete when code exists. It is complete when the requested behavior is integrated, negative paths are tested, architecture rules still pass, docs/ledgers are updated and evidence can be reproduced.

## 6. Quality model

Maintainability is a release property. Continue enforcing the existing Engineering Standards. In particular:

- domain code remains framework/storage/model-SDK independent;
- business logic stays out of routes/UI;
- public contracts are typed/versioned;
- default production file size target remains about 300 lines unless a coherent exception is documented;
- no giant manager/service/utils/helper dumping grounds;
- no mutable global authority;
- no hidden I/O constructors;
- no swallowed exceptions;
- no broad `Any` escape hatch;
- no TODO/FIXME/placeholder/static fake that is required for acceptance;
- architecture conformance and import-cycle checks remain continuous;
- generated clients/schemas are generated, not manually forked;
- event/package/API/database migrations are explicit and tested.

## 7. Audit evidence statuses

Use only:

- `PASS` / `VERIFIED`
- `FAIL` / `GAP`
- `PARTIAL`
- `EXTERNAL_BLOCKED`
- `NOT_APPLICABLE`
- `EXPERIMENTAL` for M16 research scope

`EXTERNAL_BLOCKED` means a real external dependency is missing: legal source, credentials, unavailable hardware/provider/environment. It never means “too much work”, “ran out of context”, “difficult”, or an internal bug.

## 8. Stable vs research completion

M10–M15 and M17 certify stable platform behavior. M16 is different: a research Goal may end in `PROMOTE`, `KEEP_EXPERIMENTAL` or `REJECT`. A well-run experiment that demonstrates a bad tradeoff is still a successful research Goal. Rejected experiments must not contaminate stable defaults.
