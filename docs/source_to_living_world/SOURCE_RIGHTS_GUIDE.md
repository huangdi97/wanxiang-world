# Source, Rights, and Publication Guide

Source bytes, claims, candidates, Completion, and Canonical World State are
different layers. A source record is an immutable identity and provenance
record; its `content_hash` must match the bytes consumed by the adapter.

## Source record requirements

For authoring, provide a stable `source_id`, kind, SHA-256 `content_hash`,
version, access classification, provenance, and a `RightsEnvelope`. Use
`access="private"` or `"restricted"` for non-public material and keep the
actual bytes in an approved external store. Never commit the bytes or a family
archive to this repository.

`E0` through `E5` are review stages. E3 is the approved source stage used by
the compiler, but approval and usage scope still have to pass the rights gate.
Candidates and Completion E1-E5 are never silently promoted to E0 Canon.

## Scope-aware rights check

The existing `RightsGate` checks `model`, `display`, `export`, and `package`
scopes independently:

```python
from wanxiang_substrate.rights.gate import RightsGate

gate = RightsGate()
decision = gate.decide(source_record, "package")
if not decision.ok:
    print(decision.reason)
else:
    gate.require(source_record, "package")
```

An approved source whose usage does not include `package` is still rejected for
package publication. A denied or missing rights envelope is an explicit
failure, not an empty candidate set. Review decisions and provenance remain
append-only and auditable.

## Special cases

- A scanned PDF without an OCR provider returns `OCR_REQUIRED`; do not claim
  text extraction, infer facts from pixels, or silently fall back to a model.
- A private family source may be used only under the granted scope and privacy
  policy; do not send it to a provider that is not marked `private_safe`.
- A source hash mismatch is a hard failure. Do not replace the registered hash
  or reuse a job fingerprint for changed bytes.
- Publishability is a package-validation result. Preview can exist while
  unresolved completion, conflict, or rights gaps block publication.

## Repository publication checklist

Before a commit or release, check tracked files for secrets, env/key/database
artifacts, source caches, provider outputs, and private/copyrighted material.
The CI safety job and `scripts/security_forensics.py` are the authoritative
repository checks. External legal access and rights grants must be recorded in
the deployment/source system, never fabricated in Git.
