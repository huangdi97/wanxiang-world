# External Author Guide (G17C)

## Quickstart
1. Install the workspace: `uv sync --all-groups --all-packages`.
2. Scaffold a package: `python scripts/wxpack.py scaffold ./packs my-domain --kind domain`.
3. Build/validate: `python scripts/wxpack.py validate ./packs my-domain` and
   `python scripts/wxpack.py build ./packs my-domain` (returns a lock hash).

## Conceptual hierarchy
`Domain Pack -> World Pack -> Scenario -> World Instance -> Branch -> Session -> Projection`.
Definition (packs/manifests) is immutable and versioned; a World Instance owns mutable runtime state.
Documentation examples always distinguish definition content from runtime instance state.

## State / action boundaries
- Canonical World State is writable ONLY through Commit Authority.
- A package defines resolvers/actions that PROPOSE deltas; it never mutates state directly.
- Projections are server-composed read models; they own no exclusive state.

## Source / evidence / rights
- Canonical claims require approved, versioned sources (Source Gate: E3 + rights approval).
- Claim provenance (source_refs) is retained through the completion ledger.
- Model-inference and reconstruction are labeled, never presented as canon.

## Testing
- Every scaffolded package ships a minimal test (register + resolve).
- Run `uv run pytest <package_dir>/test_package.py`.

## Versioning
- Semantic versioning; breaking changes require a major bump (see docs/SDK_COMPATIBILITY_POLICY.md).

## Debugging
- Use the observability runbook (docs/OBSERVABILITY_RUNBOOK.md) to trace commands; structured errors
  carry codes (e.g., `validation_rejected`, `stale_revision`).

## Anti-patterns (avoid)
- Importing ORM sessions or Commit Authority internals into a package.
- Rendering Unknown/inference as facts.
- Relying on frontend hiding for authorization.
