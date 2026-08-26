# G89B — Goal Reprioritization

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

`GoalReprioritizationPolicy` is a read-only protocol. The deterministic
reference implementation combines actor-authorized evidence impact with a
bounded deadline urgency delta, clamps the result to `[0, 100]`, sorts all
inputs and outputs, and includes the seed, reason, and evidence references in
the resulting `GoalReprioritizationProposal`. Re-running the same context and
seed produces byte-for-byte equivalent proposals.

`ProviderGoalReprioritizationPolicy` treats provider output as untrusted. It
checks actor/goal identity, base stack revision, source priority, duplicate
proposal references, and then returns a namespaced proposal. It never calls a
provider commit method and contains no Commit Authority or canonical-state
write path. `apply_goal_reprioritization` applies a checked proposal only to
the immutable ActorGoalStack projection and emits its existing goal revision
record.

## Gates

| Gate | Result |
|---|---|
| Policy interface and deterministic reference policy | PASS |
| Same-seed deterministic proposal | PASS |
| Reason / evidence reference lineage | PASS |
| Provider cannot commit or mutate the goal stack | PASS |
| Stale provider revision / source priority rejection | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| v5.4 agency + epistemic regression | PASS; 20 passed, 1 expected Hypothesis warning |

No database schema or canonical world event path was changed in G89B, so no
migration was required. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**; G89C is
next.
