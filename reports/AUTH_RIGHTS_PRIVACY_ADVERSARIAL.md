# Authorization, Rights, Privacy & Data-leak Adversarial Qualification (G14G)

## Scenarios
| Attack | Behavior | Result |
|---|---|---|
| Guessed/cross-branch access | projecting one branch never exposes another branch's content | PASS |
| Perspective bypass (private belief) | another actor's belief/memory excluded server-side (not UI hiding) | PASS |
| Debug/privileged projection | denied without explicit admin privilege | PASS |
| Revocation of media permission | future generation denied (GatewayRightsDenied) | PASS |
| Revocation of source rights | future canonical compilation denied (RightsDenied) | PASS |
| Audit alteration | no clear/delete/mutate/rewrite API; history append-only and monotonic | PASS |

## Semantics
- Authorization is server-enforced at the projection/runtime layer; UI hiding is never accepted as authorization.
- Revocation semantics: rights changes invalidate FUTURE projection/export/compilation access.
- Audit/history retention is append-only (documented exception to revocation: historical events are immutable).
- Tests use synthetic identities/data only; no production personal data.

## Evidence
- `uv run pytest tests/integration/test_g14g_auth_privacy.py -q` -> 5 passed.
