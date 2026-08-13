# Deployment, Security & Private Installation (G12H)

`tests/integration/test_g12h_security.py` covers secrets redaction, upload/
source injection validation, admin/debug/private/export access and audit
protection. External environment checks (Docker/PostgreSQL/browser) are
EXTERNAL_BLOCKED and explicitly labeled, never falsely passed.