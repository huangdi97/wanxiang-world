# Security, Rights, Provenance, Privacy & Source-Gate Forensics (G13F)

- Repository secret scan findings: 0
- Source-gate adversarial probes: {
  "approved": {
    "decide_ok": true,
    "require_compile": "allowed"
  },
  "rejected_rights": {
    "decide_ok": false,
    "require_compile": "blocked"
  },
  "malicious": {
    "decide_ok": false,
    "require_compile": "blocked"
  },
  "conflicting_pair": {
    "a_ok": true,
    "b_ok": true
  }
}

## Findings

- No P0/P1 rights/source/security bypass was found; all enforcement points are server-side.
- Secrets: 0 committed secrets (architecture guard re-verified).
- Audit: append-only (no mutation/clear API).
- External real-source availability is separate from gate correctness (EXTERNAL_BLOCKED).

Machine-readable: reports/security_rights_source_forensics.json
