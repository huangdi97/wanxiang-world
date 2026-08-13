# Source Registry & Source Gate (G04B)

Ownership: `wanxiang_substrate.sources` (intake gate before canonical
compilation).

## Model

- `SourceRecord`: immutable source identity (id + sha256 content hash), kind
  (text/yaml/json/markdown), content ref, review stage and rights envelope.
- `RightsEnvelope`: owner, usage, approval flag, policy version and reviewer.
- `ClaimCandidate` + `EvidenceLink`: conflicting claims are never overwritten;
  each candidate keeps its own evidence links with roles (supports /
  contradicts) and weights.
- Review stages E0..E5 (received -> rights verified -> reviewed -> approved ->
  rejected -> superseded); only approved stages are canonical-eligible.

## Registry

`SourceRegistry` registers sources immutably (duplicate content rejected),
transitions review stages with validation, and keeps an append-only audit
history (reviewer, policy version, provenance) per source.

## Gate

`SourceGate` is a pure decision engine:
- rights must be approved (policy versioned);
- stage must be canonical-eligible;
- malicious injection markers are detected and the payload is never surfaced
  as data once flagged.

## Data vs instructions

`SourceGate.read_as_data` returns source content strictly as data. Source
payload is never treated as system/prompt instructions; injection attempts are
rejected rather than executed or passed to any model/compiler channel.