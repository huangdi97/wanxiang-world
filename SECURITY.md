# Security Policy

## Supported versions

Only the current certified production baseline is supported:

| Version | Supported |
|---|---|
| v5.2 / M42 (`m42-v5.2-production`) | ✅ |

Earlier experimental milestones (M0–M41) are historical records and receive no
security fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Report privately via **GitHub Private Security Advisories**:

1. Open the repository on GitHub.
2. Go to **Security → Security advisories → New draft advisory**.
3. Include: affected component, minimum reproduction, impact, and suggested
   fix if you have one.

You should receive acknowledgement within a few business days. We do not
currently publish an external email address; the GitHub advisory workflow is
the supported channel.

## Security posture

- **No secrets in the repository.** `.env.example` contains placeholders only;
  real credentials must stay out of Git. The CI safety job scans for common
  secret patterns and forbidden tracked files on every push.
- **Canonical world state is append-only.** Commit Authority is the only
  mutator; all other participants only propose. Integrity is verified by
  replay (`scripts/kernel_guard.py`, `scripts/clean_room_certify.py`).
- **No LLM API key required for core tests.** External model providers are
  behind adapters and never own canonical state.
- **Restricted corpora are excluded.** This repository intentionally does not
  contain 《红楼梦》 edition text or other restricted source material; see
  `DATA_AND_ASSET_RIGHTS.md`.
