# Actor & Organization Runtime (G03C)

Ownership: `wanxiang_substrate.agency` (actors, organizations, policies,
orders; not giant chat agents).

## Model

- `IntentCandidate`: a policy's propose-only output (actor, action, payload,
  policy ref) ? never a mutation.
- `Order`: issued -> received -> accepted/rejected -> executed -> reported
  lifecycle with deviation/outcome; invalid transitions are structured
  conflicts.
- `ExecutionReport` (model seam) for outcome + deviation.

## Policies

- `Policy` protocol: `propose(context) -> IntentCandidate | None` (typed
  propose-only).
- `DeterministicPolicy` (fixed), `RulePolicy` (requires observation),
  `HumanPolicy` (queued human input seam) ? all no-LLM, no state mutation.
- Policy context is knowledge-bounded: only authorized observations/beliefs.

## Authority

- `agency.issue_order / receive / accept / reject / execute / report`,
  `set_actor_state`, `instantiate` are resolvers through the M1 Commit
  Authority; orders are versioned components (payload encoded as JSON string).

## Organization views

- `AgencyQuery`: orders by actor/state, actor active state, organization
  members via institution memberships.

## Compatibility

- Agency state rides on versioned components (`agency` schema v1); no new
  migration; replay deterministic.
