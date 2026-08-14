# Goal G17E Acceptance Report — Plugin Trust, Signing, Capability Permissions & Isolation Policy

## Status
PASS

## Objective
Resolve the executable-extension trust model and enforce permissions so plugin convenience cannot become unrestricted filesystem/network/database/commit access.

## Delivered
- `packages/substrate/src/wanxiang_substrate/packages/trust_model.py` — signing seam, permissions, CapabilityGate, audit.
- `tests/integration/test_g17e_plugin_trust.py` — 4 tests.
- `docs/PLUGIN_TRUST_MODEL.md`, `reports/PLUGIN_TRUST_QUALIFICATION.md`, `reports/G17E_REPORT.md`.

## Findings
- Data-only packages never execute code; trusted plugins require a valid signature + declared capabilities.
- Capability escalation and commit access are denied at the adapter boundary; every action is audited.
- OS-level sandboxing is honestly stated as not implemented (application-boundary policy).

## Evidence
- 4 tests passed; ruff/pyright clean; architecture PASS.

## Remaining limitations
- Real code-signing PKI and OS sandboxing are EXTERNAL_BLOCKED/future work; the trust seam is deterministic and tested.

## Final checkpoint
- commit: `g17e: plugin trust, signing, capability permissions & isolation policy`
