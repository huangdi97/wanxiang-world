# Rights Enforcement Matrix (G13F)

| Right | Decision point | Enforcement | Test | Status |
|---|---|---|---|---|
| Source rights approval | SourceGate.decide/require_compile (rights.approved) | packages/substrate sources/gate.py | test_source_gate::test_rights_denied_source_blocked; test_g13f_security | ENFORCED |
| Canonical compilation eligibility (stage) | SourceRecord.canonical_eligible (E3) | packages/substrate sources/model.py | test_source_gate::test_unapproved_stage_blocked | ENFORCED |
| Projection visibility (beliefs/memories/sealed/places) | ProjectionService._project_entity (actor + admin) | packages/substrate projection/service.py | test_projection_filters; test_g13f_security | ENFORCED |
| Media generation (tts/lipsync/expression/face) | DigitalHumanGateway.require_permission | packages/substrate gateway/gateway.py | test_g12h_security; test_g13f_security | ENFORCED |
| Debug projection (privileged) | ProjectionService.compose mode=debug requires admin | packages/substrate projection/service.py | test_g12h_security::test_admin_debug_private_export_access | ENFORCED |
| Audit append-only | no mutation/clear API on audit/history | SourceRegistry.audit_history; AuditTraceRepository | test_g12h_security::test_audit_protection_append_only | ENFORCED |

Every rights decision is server-enforced; no UI-only rights check exists.
