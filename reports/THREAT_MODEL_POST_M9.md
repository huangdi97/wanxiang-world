# Threat Model (Post-M9, G13F)

| ID | Threat | Mitigation | Evidence | Status |
|---|---|---|---|---|
| T1 | Prompt/source injection into canonical facts | SourceGate flags instruction markers; payloads are read as data only; compiler emits candidates, never executes source text. | test_source_gate (malicious), test_g13f_security::test_prompt_injection_source_remains_data | MITIGATED |
| T2 | Unapproved/rights-denied source reaches canonical state | SourceGate.decide/require_compile blocks non-E3/rights-denied sources before compilation. | test_source_gate, test_g13f_security::test_unapproved_sources_cannot_enter_canonical_compiled_facts | MITIGATED |
| T3 | Private knowledge/projection leakage | Server-composed projections filter beliefs/memories/sealed payloads/restricted places by actor; debug requires admin. | test_projection_filters, test_g13f_security::test_denied_rights_block_projection_and_export | MITIGATED |
| T4 | Unauthorized media/voice/face generation (digital human) | DigitalHumanGateway.require_permission rejects missing permission with GatewayRightsDenied; outputs are proposals. | test_g12h_security::test_unauthorized_voice_face_generation_rejected, test_g13f_security | MITIGATED |
| T5 | Secrets/privacy leaked into logs, config or backups | Settings public dict redacts secret-named values; log pipeline redacts known secrets; architecture secret scan is clean. | test_config_redaction, test_g12h_security, test_g13f_security::test_secret_scan_and_privacy_logs | MITIGATED |
| T6 | Audit/history tampering or deletion | Audit records append-only (no mutation/clear API); event history append-only; corrections via new events/branches. | test_g12h_security::test_audit_protection_append_only, G13E forensics | MITIGATED |
| T7 | Conflicting claims silently resolved without provenance | Ledger keeps claims with source_refs; promotions require review; no silent overwrite. | test_completion_ledger, test_g13f_security::test_conflicting_claims_coexist_with_provenance | MITIGATED |
| T8 | Authn/authz bypass through transport | Thin FastAPI routes call application use-cases; debug/private access is server-enforced; rights checks never UI-only. | test_api, test_g12h_security | MITIGATED |

Real external providers/hardware remain EXTERNAL_BLOCKED; generic capability and deterministic
substitutes are complete (never falsely passed).
