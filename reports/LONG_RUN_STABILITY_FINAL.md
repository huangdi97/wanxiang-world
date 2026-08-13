# Long-run Stability ? Final

## Evidence
- G12A: 30 in-world days (3000 ticks) + 1000+ committed cycles, no invariant
  failure, events == committed commands (bounded growth), deterministic hash.
- M2: 72h integrated living-world test stays green in every full suite run.
- Restart/recovery: kill/restart reproduces canonical hash (G06C); M5 vertical
  restarts the process and reconnects with hash continuity.
- Resource budgets bound autonomous loops (G06C/G07E).