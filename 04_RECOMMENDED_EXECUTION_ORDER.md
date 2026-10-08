# Recommended execution order and dependency handling

## Critical path
G98A → G98B → G98C → G98D/G98E → G99A–E → G100A–E → G101A–G → G103A–I

## Parallel/blocked behavior
- If G98D awaits a human: continue G99A–E, G100A–C, G101A–G and G102A–D. G100D human-derived fields remain missing; G103/Stable release remains locked.
- M99 is never on the required critical path unless Stable scope is formally changed before Gate 61 freeze.
- If live PostgreSQL is unavailable: keep it EXTERNAL_BLOCKED; do not turn it into a SQLite success claim.
- If a real external provider/API is unavailable: reference-provider runs may support bounded engineering evidence, but must stay labeled as such.

## What should not happen
- no new Reality Root design;
- no second event store/canonical state;
- no M85–M94 rewrite;
- no arbitrary “quality score” that merges Worldness and UX;
- no 10k/100k claim by extrapolating the 1000-actor tier;
- no fake Godot through screenshots/mocks;
- no release tag before all required Stable gates are evidence-backed.
