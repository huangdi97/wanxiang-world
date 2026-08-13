# Adversarial & Chaos Qualification Protocol

## Principle
The purpose is not maximum random failure. It is controlled fault injection around semantic authority, persistence boundaries, concurrency, rights and external adapters.

## Required fault families
1. concurrent/stale/duplicate commands;
2. crash before/during/after commit;
3. DB/network/storage timeout and unavailable states;
4. corrupt events/snapshots/branch ancestry/version;
5. reconnect, reordering, slow consumer, queue pressure;
6. hostile package/source/prompt injection;
7. authorization/privacy/rights bypass attempts;
8. Byzantine simulator/sensor proposals;
9. resource exhaustion, fuzz and long-run memory growth.

## Invariant monitor
Chaos tests must continuously watch event ordering, branch isolation, canonical semantic hash validity, custody/container constraints, permissions, time monotonicity and information isolation as applicable.

## Safety
Fault hooks must be test-only or protected by explicit non-production configuration. Never ship a debug endpoint that can corrupt authoritative state.

## Reporting
Record seed, profile, environment, injected fault, expected behavior, actual behavior, invariant results, recovery path and residual risk.
