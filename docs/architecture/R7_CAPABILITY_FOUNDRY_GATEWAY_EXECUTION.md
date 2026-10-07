# R7 Capability Foundry, Execution Fabric and World Gateway

## Artifact2Capability

```text
Artifact
 -> CapabilityCandidate
 -> interface + environment declaration
 -> isolated GOLDEN / NEGATIVE / BOUNDARY / SECURITY execution
 -> VerificationReport
 -> provenance-bound CapabilityPackage
 -> VerifiedCapabilityRegistry
 -> invocation
 -> Observation / Proposal
```

Artifact kinds cover paper, repo, API, manual, standard, notebook, workflow,
dataset and simulation. Unknown evidence is never interpreted as PASS.

## Qualification / provenance

Automated qualification reaches K3/C3; C4/C5 remain human/organisation
governance. A package binds source URI/digest/rights basis, declared interface,
exact verification cases, validity/limitations, execution environment and four
provenance layers: source method, generated wrapper, validation fixture and
runtime adapter.

A provenance digest establishes traceability, not scientific truth.

## Execution

Foundry invocation uses Execution Fabric. Current reference isolation is a real
child process with a scrubbed environment and deny-by-default policy; it is not
claimed as a hostile-code container/microVM sandbox. Execution output is
proposal-side and has no canonical writer.

Irreversible effects use durable intent -> outbox -> idempotent external handler
-> result -> Observation -> reconciliation. R7 drives a real local HTTP
subprocess for the reference I/O path, including duplicate, crash, timeout,
restart, retry and manual reconciliation cases.

## World Capability Gateway

AgentSessionIdentity binds principal/role/world/branch, optional actor lease,
capability/rights/secret scopes, expiry and audit id. The gateway exposes bounded
observation/history/branch-diff queries, proposal-only actions, governed
fork/experiment requests and WorldSkill.

Raw canonical state requires explicit `world.canonical.read`. The gateway
deliberately has no commit/force-commit/raw database/rewrite-history operation.

MCP/OpenAPI/CLI/gRPC may adapt this gateway; none is the canonical internal world
protocol.

## DeepSeek Harness

Wanxiang keeps DSH outside the core. A deterministic subprocess harness qualifies
the protocol in CI. An optional `deepseek-harness-sdk` adapter exists for the
official runtime and returns committed/rejected consequences to the same durable
session. Live model-backed evidence is not claimed without actual runtime and
credentials.
