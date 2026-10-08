# G95A — WorldRunArtifact v1

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

WorldRunArtifact is an immutable schema-versioned evidence record over the
existing WorldPackage/Preview/PlayableService/SQLite runtime chain. It pins
world package, scenario, constitution, runtime profile, provider versions,
seed, control/event/snapshot/branch references, actor trajectory references,
intervention references, metrics, and V0-V7 result statuses. Its canonical
payload is hashed with the repository semantic hash function.

The export boundary is strict: raw source text/bytes/payload, secrets, tokens,
and API keys are rejected; short opaque metadata can be retained while
redacted fields are explicitly listed. Deserialization verifies the content
hash, so payload tampering is observable.

## Evidence

- Unit: tests/unit/substrate/test_g95a_world_run_artifact.py — 3 passed.
- Integration: tests/integration/test_g95a_world_run_artifact_product_chain.py
  — 1 passed using a private rights-approved source through
  OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime.
- The integration artifact round-trips, includes real commit/snapshot/branch
  refs and replay hash evidence, excludes source bytes, and preserves runtime
  replay equality.
- Full quality: 1389 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  pytest, architecture conformance, SDK compatibility, and minimality checks
  pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED profile.

## Boundary

The artifact is evidence only. It does not own canonical state, event history,
branch creation, source registry, or Commit Authority. G95B-G97J remain pending;
v5.5 remains IN_PROGRESS / NOT_ACCEPTED.
