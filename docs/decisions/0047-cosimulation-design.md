# ADR-0047: SimulationAdapter & Co-Sim Orchestrator Design (G11A, G11B)
- Status: accepted
- Date: 2026-08-13

## Context
G11 needs deterministic fake simulators that participate without owning
canonical state, stepped multi-rate with explicit arbitration.

## Decision
1. SimulationAdapter is the full contract; FakeSimulator implements it
   deterministically and only emits events/proposed deltas.
2. CoSimOrchestrator steps to barriers deterministically and adjudicates
   conflicts explicitly (deterministic winner, rejected list).
3. Checkpoint/restore is part of the contract.

## Consequences
- Adapters never own commit authority; multi-rate ordering is deterministic and
  restartable.