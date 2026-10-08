# G93E — Organization Lifecycle

Date: 2026-08-27
Status: PASS

## Implemented contract

G93E adds a typed organization lifecycle projection over the existing
`InstitutionQuery`. It does not add a Canonical State, Event Store, Branch,
Package Registry, Source Registry, or persistence schema. Existing institution
role, membership, and delegated-permission components remain the source of
truth when `organization_state_from_canonical` builds a read-only view.

The projection covers `create`, `join`, `leave`, `role_change`,
`grant_permission`, `revoke_permission`, `dissolve`, and `split`. Roles,
memberships, delegated grants, organization resources, parent/child lineage,
and lifecycle event refs are explicit typed fields. Proposals carry the G93A
`OrganizationDelta` and source/event provenance. They require explicit
review, reject Commit Authority as a provider, enforce stale before-state
checks, and never submit or commit a world delta.

Authority is checked from active organization roles. Self join/leave is
allowed; invitations, role changes, permission changes, dissolution, and
split require the corresponding organization authority permission. Leaving
removes the member's memberships and grants. Effective permission queries
also require an active recipient and active member granter (or the
organization itself), so orphan permissions cannot remain effective. Split
partitions members and resources, drops cross-partition grants, and conserves
the explicit resource quantities. Dissolution clears memberships and grants
while retaining resources for an explicit settlement projection.

## Reproducible evidence

- `tests/unit/substrate/test_g93e_organization_lifecycle.py`: 5 passed,
  covering formation, self-join, role change, review gating, authority
  rejection, provider boundary, revoke, orphan-permission cleanup, split
  partitioning/resource conservation, and dissolution.
- `tests/integration/test_g93e_organization_lifecycle_product_chain.py`: 1
  passed. A private rights-approved source traversed OneClickAuthoring,
  PlayableService, Preview, and SQLite-backed WorldRuntime. A committed
  product event supplied provenance to the lifecycle proposals. The
  projection changes left canonical hash, revision, event count, and replay
  equality unchanged.
- `scripts/sdk_baseline.py`: `routes=62 ts=5 py=1865` after the additive
  public evolution surface.

## Quality and boundary gates

- G93A-E and institution focused regression: 34 passed, with the existing
  Hypothesis collection warning.
- Full repository pytest run: `1350 passed, 1 skipped, 2 warnings` in
  `339.97s`; the single skip is the documented PostgreSQL
  `EXTERNAL_BLOCKED` profile.
- Ruff: PASS.
- Pyright: 0 errors, 0 warnings, 0 informations.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.
- No private source was uploaded, no source text was modified, no model was
  trained, and no v5.6 work was started.

G93E is PASS and is ready for the required commit
`g93e: Organization Lifecycle`. Gate 30 remains pending until G93H completes
the integrated 30-day Actor/Relationship/Organization qualification. Gate 24,
G93F-G97J, and the remaining v5.5 release gates remain pending; v5.5 stays
`IN_PROGRESS / NOT_ACCEPTED`.
