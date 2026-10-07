# R7 Operator Runbook

## Worldline open

Writable worldlines require a persisted valid RuntimeLock. Refuse operation on
missing lock, digest/tamper failure, identity mismatch, provider/schema/contract
drift or unresolved major RealityProfile change. Never repair a drifted lock
silently.

## Migration

1. quiesce the worldline;
2. capture checkpoint and baseline lock;
3. build candidate profile/lock;
4. shadow replay;
5. inspect drift/invariants;
6. approve migrate/fork or reject;
7. retain migration artifact and lineage.

## External effects

Check the durable outbox before retry. Ambiguous results are not automatically
resent. Reconcile only after checking the external system. A timeout is not
success.

## Capability incidents

Revoke the exact version, retain historical registry evidence, stop new
invocations, qualify a new version, and never rewrite past world outcomes.

## DSH incidents

An unavailable/malformed DSH provider is a provider failure, not a world-history
failure. Preserve the worldline and resume only after the provider route is
healthy.

## Readiness

R7 operational/readiness views are observability only and never a hidden source
of canonical truth.

## Release boundary

Do not create `v5.5.0` Stable or a `v5.6` release from this runbook. Stable
release remains gated by the authoritative acceptance matrix, including genuine
human Gates 62–66.
