# Co-Simulation (G11A-G11E)

Ownership: `wanxiang_substrate.cosim`.

## SimulationAdapter (G11A)
`SimulationAdapter` protocol: initialize(world_slice), ingest_state(snapshot),
advance(t0,t1), emit_events(), emit_proposed_deltas(), checkpoint(), restore(),
describe_assumptions(), describe_validity_envelope(). `FakeSimulator` is a
deterministic implementation; adapters only emit events/proposed deltas and
never own commit authority.

## Orchestrator (G11B)
`CoSimOrchestrator` registers simulators at rates, steps to synchronization
barriers deterministically (sorted by name; each simulator advances only on its
own rate boundaries), supports checkpoint/restore, and adjudicates conflicting
proposals explicitly (`ArbitrationResult` with deterministic winner).

## Campaign (G11C-D)
`CampaignDomain` models factions, units, terrain/regions/routes, resources,
objectives and orders with delay/lifecycle, route capacity, movement time and
fog-of-war (a faction only knows observed regions).

## Batch evaluation (G11E)
Reuses the experiment runtime (G07E): batch variants x seeds -> metrics ->
distributions -> Finding with assumptions + ValidityEnvelope.