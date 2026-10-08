# G72G Report — CLI/API product flow

**PASS (2026-08-25)** — The API exposes one-click, status, review-inbox, and
publish over the shared `AuthoringService`; the reference CLI exposes the same
no-API path with explicit `--publish`. Package preview/entry uses the existing
runtime handoff rather than a parallel CLI authority.

Evidence: `tests/integration/test_m69_one_click.py` Studio/API/CLI assertions.
