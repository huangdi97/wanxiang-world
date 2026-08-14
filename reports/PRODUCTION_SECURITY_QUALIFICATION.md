# Production Security Qualification (G16F)

## Hardening delivered
- **Rate limiting**: fixed-window token bucket on the sensitive write endpoint (`submit_action`) -> 429 on
  abusive profiles (server-side, not UI hiding).
- **Payload size guard**: writes > 64KB rejected with 413 (`payload_too_large`).
- **Server-side authorization**: debug projection requires admin; media generation requires explicit rights.
- **Supply chain**: `scripts/generate_sbom.py` produces `artifacts/sbom.json` + `artifacts/SBOM_INFO.md`
  (42 Python + 113 JS packages); secrets never baked into artifacts; secret scan clean.

## Results
| Check | Result |
|---|---|
| Abusive request profile bounded (429) | PASS |
| Oversized payload rejected (413) | PASS |
| Unauthorized actions denied server-side (admin gate + gateway rights) | PASS |
| SBOM inventory generated; no secrets in artifacts; secret scan clean | PASS |
| API regression | 7 passed |

## Security exceptions
- Vulnerability scanning tooling unavailable offline -> EXTERNAL_BLOCKED (documented; inventory supports
  manual advisory review). No known critical unmitigated issue in the shipped profile is claimed beyond
  what the inventory can confirm.

## Evidence
- `uv run pytest tests/integration/test_g16f_security_hardening.py -q` -> 4 passed.
- `uv run python scripts/generate_sbom.py` -> python=42 js=113.
