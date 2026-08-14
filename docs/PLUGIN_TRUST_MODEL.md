# Plugin Trust Model (G17E)

## Trust classes
- **Data-only** (`executable_trust=untrusted`): never execute code; declare no capabilities.
- **Trusted** (`executable_trust=trusted`): may execute declared known extensions ONLY when signed
  (deterministic HMAC signature seam) and within declared capabilities.

## Signing / verification
- `sign_manifest(plugin_id, version, secret)` -> HMAC-SHA256 digest; `verify_signature` compares
  constant-time. Deterministic test keys are used; production secret injection is config-driven.

## Capabilities
- Declared capabilities: `filesystem`, `network`, `database` (and `commit`, which is NEVER granted:
  only Commit Authority may mutate canonical state).
- `CapabilityGate.authorize` enforces declared capabilities at the adapter boundary; escalation fails.

## Isolation honesty
- OS-level sandboxing (subprocess/seccomp/container) is NOT claimed. This is an application-boundary
  policy (trusted/signed or none). Documented as future work.

## Audit
- Every plugin action is recorded with plugin id, version, action and allowed flag.

## Evidence
- `uv run pytest tests/integration/test_g17e_plugin_trust.py -q` -> 4 passed.
