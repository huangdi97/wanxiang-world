# Final Security / Rights Report

## Status
PASS (mechanism) — security, rights and supply-chain controls verified.

## Evidence
- Prompt injection: SourceGate `_is_malicious` rejects instruction-injection
  payloads; source payloads are data, never instructions (G04B).
- Malicious/unapproved sources: `MaliciousSource` / `RightsDenied` /
  `SourceNotApproved`; E0-E5 stage semantics; completion never masquerades as E0.
- RBAC/access: institution roles/memberships/permissions + spatial access +
  narrative visit access (G02E/G35F).
- Commit capability never granted to plugins (CapabilityGate.commit denied);
  only Commit Authority mutates canonical state.
- Supply chain: package trust enforcement, executable extension policy, HMAC
  signatures, SBOM/secret scans (G17E/G16F/G45F); kernel_guard 0 violations.
