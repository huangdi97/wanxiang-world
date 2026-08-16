# Data & Asset Rights

This document states what data and assets this repository publishes, and what
it deliberately does **not** publish.

## What is published

- **Code**: Apache-2.0 licensed (see `LICENSE` and `NOTICE`).
- **Synthetic / deterministic sample content**: the only world content in this
  repository is generated sample material (e.g. `reference_worlds/`,
  `data/` fixtures, package scaffolds, tests). It carries no third-party
  copyright and is reproducible from the repository itself.
- **Documentation and planning documents**: authored by the project owner.

## What is deliberately excluded

- **《红楼梦》 edition text**: the project respects the Source Gate. A legally
  traceable, redistributable edition of the novel is **not** available in this
  environment, so no full text, modern annotated edition, or scanned copy is
  included. `sources/red_chamber/` contains only a README and a manifest
  template. Honest `EXTERNAL_BLOCKED` records in the evidence reports describe
  this — nothing is faked as present.
- **Museum / institutional private materials**: not included.
- **User privacy data, credentials, databases, logs with sensitive content**:
  not included and must never be committed.
- **Model weights, caches, and large generated assets**: not included.

## Redistribution expectations

- You may use, modify, and redistribute the code under Apache-2.0.
- Synthetic sample content follows the same license unless a file says
  otherwise.
- If you obtain a legally redistributable edition of the novel or another
  corpus, it must pass the Source Gate and be added with clear provenance and
  rights documentation before it may enter this repository. Until then, the
  corpus remains absent and the corresponding acceptance items remain honest
  `EXTERNAL_BLOCKED` records.

## No warranty

All content is provided "AS IS", without warranty of any kind. See
`LICENSE` for the full terms.
