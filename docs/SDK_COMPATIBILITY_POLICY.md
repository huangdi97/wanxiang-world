# SDK Compatibility Policy (G17A)

## Stable vs experimental namespaces
- **Stable**: `wanxiang_domain`, `wanxiang_application`, `wanxiang_runtime`, `wanxiang_substrate`
  (public names only, no underscore-prefixed internals), `wanxiang_api` routes, and the TypeScript SDK.
  Breaking changes require a major version bump per semantic versioning.
- **Experimental**: research/feature-flagged surfaces (M16) live in explicitly named experimental
  namespaces and are OFF by default; they are labeled experimental and may change without a major bump.

## Compatibility guarantees
- Within major v1: additive changes are allowed; breaking changes (renames, signature changes, removed
  endpoints) require a new major version and a documented deprecation path.
- Event/package/database schema compatibility is protected by versioned contracts and migration tests.
- Support ranges are documented per release (current: v1; deprecation at least one minor before removal).

## Extension points (documented)
- Domain/World/Scenario packages via the public package SDK (`wanxiang_substrate.packages`).
- Runtime use-cases via `wanxiang_application` (WorldRuntime + resolvers) — never ORM sessions or Commit
  internals.
- Projections via the server-composed projection API.

## Forbidden dependencies for third-party packages
- No ORM sessions, no Commit Authority internals, no `wanxiang_persistence` internals, no private
  (`_`-prefixed) runtime objects. SDK does not grant canonical mutation authority.

## Enforcement
- `reports/sdk_api_baseline.json` snapshots the public API surface; compatibility tests detect any drift
  (a breaking change changes the snapshot and fails the gate).
