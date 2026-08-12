# Institution, Authority, Duty & Norm Substrate (G02E)

Ownership: `wanxiang_substrate.institution` (social/institutional constraints).

## Model

- `Role`: name + granted permissions.
- `Membership`: time-scoped role membership (start/end ticks); expired roles
  cannot grant current authority.
- `DelegatedPermission`: explicit grant with granter provenance and time scope.
- `Duty`: actor duty with due ticks and state (pending/done/overdue).
- `PermissionDecision`: allow/deny with rule references and provenance.

## Authority

- `institution.define_role` / `grant_role` / `grant_permission` /
  `assign_duty` / `complete_duty` / `apply_sanction` / `instantiate` are
  resolvers through the M1 Commit Authority; changes are auditable events.

## Permission integration

The spatial move resolver requires permission (`enter.<place>`) to enter a
`restricted` place; an unauthorized actor is rejected with
`PermissionDeniedByInstitution` (rule references available via the decision).
Duties reference schedule/clock time by id (no cyclic package dependency).

## Compatibility

- Institution state rides on versioned components (`institution` schema v1); no
  new migration; M1 replay untouched. Role/permission history replays exactly.
