# Config & Secret Qualification (G16A)

## Typed configuration
- `WanxiangSettings` (env, log_level, database_url, log_json) with a `production` flag.
- `load_settings` validates profiles: `development`/`test` use deterministic offline defaults (no secrets);
  `production` requires an explicit `WANXIANG_DATABASE_URL` (dev sqlite default rejected) and
  `WANXIANG_SECRET_KEY`, failing fast with `ConfigError`.

## Secrets
- Secrets are injected via environment; never committed (architecture secret scan clean).
- The public settings surface and logs redact secret values.

## Production safety
- Startup fails clearly on missing required production config (no silent dev/test fallback).
- The runtime always wires the durable SQLAlchemy event store; in-memory test Fakes are never selected by a
  production/default profile.

## Evidence
| Check | Result |
|---|---|
| Secret scanner clean | PASS |
| Dev/test offline deterministic defaults | PASS |
| Production missing config fails fast | PASS |
| Production valid + public surface redacts secrets | PASS |
| Production uses durable persistence (no test Fakes) | PASS |
| Config regression (test_config_redaction, test_api) | 11 passed |
