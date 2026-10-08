# G72C Report — One-click structured world

**PASS (2026-08-25)** — JSON and CSV structured inputs use the existing
`StructuredAdapter` and deterministic reference distillation. Both produce
identity/event/place candidates and enter an isolated preview; JSON also
passes the publish gate, while CSV entry is verified as a living preview.

Evidence: `tests/integration/test_m69_one_click.py` structured JSON and CSV
flows; no API key or external provider is used.
