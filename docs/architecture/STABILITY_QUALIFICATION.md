# 30-Day / 1000+ Tick Stability Qualification (G12A)

`tests/integration/test_g12a_stability.py` runs a synthetic world 30 in-world
days (3000 ticks) plus 1000+ committed cycles with no invariant failure; events
== committed commands (bounded resource growth) and the semantic hash is
deterministic.