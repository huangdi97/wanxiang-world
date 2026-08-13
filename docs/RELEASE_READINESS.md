# Release Readiness ? Wanxiang Platform Foundation

## Status
Local release-qualified foundation (M1-M9 PASS; 385 Python + 21 TS tests).

## What is ready
- Authoritative event-sourced world kernel (M1) with full substrate planes
  through M8 and release adapters through M9.
- Deterministic, replayable, branch-safe canonical state; no LLM required for
  core tests; modular monolith with strict architecture guards.

## Local startup
- `uv sync --all-groups --all-packages`, `uv run python scripts/quality.py`,
  API via `apps/api` (FastAPI). Fresh-clone runbook is documented in
  `docs/runbook/DEVELOPMENT.md`; CI workflow exists.

## External prerequisites (EXTERNAL_BLOCKED in this environment)
- Real source packs (Red Chamber, Liaoshen), real IIIF endpoints,
  Gymnasium/PettingZoo, React/Phaser/Godot/Babylon renderers,
  Docker/PostgreSQL/browser checks. Interfaces, fakes, negative gates and all
  local behavior are complete; nothing is falsely marked done.

## Versioning
- Public API version policy documented (additive within v1; breaking changes
  require a new major); SDK generation deterministic from OpenAPI.