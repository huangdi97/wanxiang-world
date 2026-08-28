# M96 G99D — Bounded Seven-Day Run

**Conclusion:** `PASS` for the bounded G99D contract.

The run enters the published world through PlayableService, makes a committed
action with StateDiff evidence, leaves and continues the same instance, then
executes seven accelerated days with seven checkpoints. Every checkpoint has a
matching replay hash. A child branch receives a separate scoped command and is
verified not to alter the parent. The actor-continuity record reports seven
completed days with replay and leave/re-enter equality plus goal, memory,
belief, and relationship revision counts.

Machine evidence: `artifacts/v55_stable/m96/original_prompt_world.json` under
`play` and `bounded_7d`; reproducible command is the one in
`reports/M96_G99B_PROMPT_GENESIS.md`. This remains a bounded reference run,
not a population, emergence, or universal long-horizon claim.
