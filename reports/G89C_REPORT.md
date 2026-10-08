# G89C — EpistemicMemory v1

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

G89C extends the existing `wanxiang_substrate.epistemic.MemoryRecord` rather
than creating a second memory store. A record now carries source perception
references, a bounded decay rate, reinforcement count, and the last
reinforcement tick. `effective_salience` and `decayed` are read-only decay
hooks; `reinforce` returns a new record with explicit lineage and never writes
canonical state. The existing `BeliefAssertion` remains a separate type with
its own confidence/status lineage.

`PerceptionEnvelope` now records its envelope reference in the memory's
perception refs while retaining the existing source-event compatibility field.
Component fields are optional additions under the existing v1 component shape;
`memory_from_component` defaults missing fields so old persisted events remain
readable. The compatibility test uses the old field shape. No private source
content or secret value is copied into the new refs; they remain opaque refs.

## Gates

| Gate | Result |
|---|---|
| Memory record + source perception refs | PASS |
| Read-only decay and explicit reinforcement hooks | PASS |
| Memory is distinct from belief and canonical truth | PASS |
| Legacy component field compatibility | PASS |
| Secret/ref-only isolation | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| Epistemic unit, propagation, and replay regression | PASS; 14 passed, 1 expected Hypothesis warning |

Gate 8 (`Memory / Belief / Truth separation`) is **ACCEPTED** in
`reports/V55_ACCEPTANCE_MATRIX.md`. No database migration was required because
the component extension is backward-compatible and no relational schema was
changed. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**; G89D is next.
