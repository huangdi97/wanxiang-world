# Seven-day Autonomous Worldness Qualification (G15C)

## Run profile
- World: Synthetic Full Reference World (G15B) — places, people, guild, objects, beliefs.
- Horizon: 7 simulated days (7 x 100 ticks) with the deterministic AutonomousScheduler; NO user session.
- Periodic captures: semantic hash + checkpoint at each day boundary.

## Results
| Worldness criterion | Result |
|---|---|
| World advances without a user session | PASS (events every day) |
| State evolves (>=3 distinct daily hashes) | PASS |
| Event stream valid (contiguous seq) | PASS |
| Replay reproduces final semantic hash | PASS |
| Emergent/conditional events from policies (EntityUpdate ops) | PASS |
| No actor starvation (all 4 people present with valid body condition) | PASS |
| No knowledge leak (private belief hidden after 7 days) | PASS |
| Periodic checkpoints created each day | PASS |

## Evidence
- `uv run pytest tests/integration/test_g15c_seven_day.py -q` -> 1 passed (3.2s).
- Deterministic run (seeded); no LLM used for the mandatory run.
- Any future LLM-enhanced optional run must be separately labeled non-deterministic.
