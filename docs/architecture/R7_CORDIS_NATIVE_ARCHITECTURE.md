# R7 Cordis-Native Architecture

Status: canonical engineering architecture for branch `feature/r7-cordis-native`.

## Architecture decision

Wanxiang does not implement a second Cordis-like composition kernel. The
first-generation composition runtime is the exact-pinned Cordis dependency in
`packages/cordis_host/package.json`. Wanxiang-specific semantics live above that
runtime as versioned service contracts, profiles, authority rules and persistent
world history.

```text
Applications / Experiences / Distribution
                  |
Domain / Forge / Simulation / Capability
                  |
       Versioned RealityProfile
                  |
          Wanxiang Base Bundle
                  |
               Cordis
        /                    \
trusted in-process       external execution
plugins                  process/remote/etc.
```

Cordis owns service composition, scope, dependency activation and reversible
runtime effects. Wanxiang owns world identity, proposal, authority, commit,
history, branch/lineage and profile migration.

## Non-negotiable boundaries

```text
Cordis Effect     != World Event
Plugin Unload     != Undo Committed History
Cordis Context    != Canonical World State
Execution Success != Canonical World Truth
ExecutionTrace    != World History
Sandbox Snapshot  != World Branch
Agent/LLM Output  != Commit
World             != Experience != Projection != Distribution
```

Canonical reality remains reconstructible from committed history interpreted
under the worldline's pinned profile/migration chain. Cordis contexts carry
services/capabilities, never a second mutable copy of world truth.

## Versioned seams

`packages/reality/src/wanxiang_reality/contracts.py` is the contract catalog.
Each seam records namespace, service id, API/schema version, scope, capabilities,
typed error semantics and compatibility policy. Consumers depend on contracts;
providers are replaceable implementations.

## Scope and state

Wanxiang uses world/worldline-scoped composition so one worldline can be disposed
without tearing down another. The scope tree is a capability graph, not a state
tree. Canonical state stays behind history/snapshot/projection services and
Commit Authority.

## RuntimeLock

A writable worldline is tied to a persisted, tamper-evident RuntimeLock binding
world identity, RealityProfile/WorldProfile refs+hashes, exact composition
runtime/version, service/provider/schema versions, artifact hashes, migration
lineage and runtime configuration hash. Missing/tampered/drifted locks fail
closed in Python and the TypeScript Cordis host.

## Authority

```text
Proposal
 -> policy / rights / invariants
 -> monotonic hard-deny guards
 -> expected-revision check
 -> Commit Authority
 -> committed history
 -> projection / consequence
```

Ordinary plugins, external agents, Foundry capabilities and projections never
receive the canonical write credential.

## Execution / agents / experiences

Untrusted/generated code is routed through Execution Fabric. DSH is an external
agent provider, not the World OS. WorldCapabilityGateway exposes query/proposal
operations and deliberately has no direct commit. ExperienceBlueprint,
InteractionProfile, ProjectionProfile and DistributionAdapter own references and
product policy only, never canonical reality.

The final R7 closure report is authoritative for PASS/BLOCKED/HUMAN_INPUT_REQUIRED
status at an exact SHA; design existence alone is never implementation evidence.
