# Player / Studio Identity Boundary — Release Blocker

Status: **TRUSTED AUTH INTEGRATION NOT PROVEN / RELEASE LOCKED**.

## Why this exists

The local demonstration API accepts `x-wanxiang-user` as a simulated
identity; the demo web Player currently sends `studio`. This header is
**not authentication**. It can be forged by any HTTP client. In particular,
do **not** expose the local-demo API to the Internet and do not treat
`visual_asset_rights_v1` or actor-scoped filtering as production authorization
while callers can impersonate a user. These source-rights controls are
only meaningful when viewer identity itself is verified.

## Fail-closed deployment seam

With `WANXIANG_IDENTITY_MODE=trusted`, the app requires a trusted **outer
ASGI authentication middleware** to populate:

- `scope["wanxiang_authenticated_user"]`: a verified, nonempty user ID;
- `scope["wanxiang_authenticated_roles"]`: includes `creator` for Studio access.

Without a principal, every HTTP request is rejected with 401; Studio without
the creator role returns 403. Any inbound HTTP `x-wanxiang-user` is removed
and replaced from the trusted scope value before existing Player/Experience
route handlers run. The browser cannot select its own identity in this mode.
Unknown identity modes fail at application creation.

An HTTP reverse-proxy header alone MUST NOT be copied into the trusted scope
without independently verifying the upstream authentication. An external
authenticator and deployment configuration have **not** been shipped or
validated by this change. This is a protective integration seam, not a
claim of finished production login, tenant isolation, authoring permission
policy, anti-CSRF, or a completed security audit.

The default `local-demo` mode retains the existing synthetic browser/CI
workflow and must be restricted to trusted development machines.

## Remaining production gates

Before any public deployment: integrate a trusted authenticator, complete
Studio/authoring authorization and per-user source visibility, test public vs
private reads on every API including metadata/Atlas/clues, validate anonymous
and adversarial clients, and record real deployment evidence. The general
Source → WorldDraft → WorldPackage → Projection → Commit Authority chain is
unchanged by identity handling.
