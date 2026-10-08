# G95E — Multi-provider / Mixed-population

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

`ProviderAssignmentPolicy` is a schema-versioned immutable policy with
homogeneous, deterministic round-robin, and explicit member assignment modes.
`ProviderRunInput` binds one world package/scenario, source references,
population, seed, and parameter set to every invocation and exposes one input
hash for replay comparison. The original payload is execution-only and is
redacted from exported evidence.

`MultiProviderWorldlineRunner` reuses the existing `Provider` and
`ProviderProposal` boundary. It checks provider identity, availability,
determinism, private-source safety, and source-reference scope before accepting
output. Every result is an exact `ProviderProposal`; a provider cannot return a
commit-capable value, write canonical state, or bypass Commit Authority.
Provider activation is recorded through the existing append-only
`RuntimeControlLedger`, which is runtime control evidence and never a World
Commit.

## Evidence

- Unit: `tests/unit/substrate/test_g95e_multi_provider.py` — 3 passed,
  proving deterministic assignment, identical input delivery, policy
  round-trip/completeness, runtime-control isolation, sanitized export, and
  rejection of a commit-capable provider output.
- Integration: `tests/integration/test_g95e_multi_provider_product_chain.py`
  — 1 passed. The same private rights-approved source ran a four-member mixed
  population with two private-safe reference providers through
  WorldPackage → PlayableService → SQLite WorldRuntime. The provider run left
  the event stream unchanged; a later explicit Playable action used the normal
  Commit Authority and produced snapshot, replay, and WorldRunArtifact
  evidence.
- Full quality: 1405 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  architecture, SDK compatibility, duplicate-abstraction, and minimality
  checks pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED
  profile.

## Boundary

Gate 42 (multi-provider/policy or mixed population) is accepted. Gate 41
remains pending because the G95D real SQLite qualification was intentionally
serial; the bounded-parallelism unit evidence is retained without overstating
it as parallel qualification. G95F-G97J and the remaining M92-M94 gates remain
pending, so v5.5 remains NOT_ACCEPTED.
