# R7 03 — Versioned Service Seams

Status: `PARTIAL` — the versioned seam identity and the contract catalog exist on
both sides; the JSON-RPC bridge that lets the Python authority serve the history
seam is **not** implemented in this slice.

## Contract catalog

The full contract bodies live once, in the Python package
`wanxiang_reality.contracts`; the TypeScript host duplicates only the
identity-bearing part (namespace, API version, scope) and recomputes a digest
over it, so a divergence between the two runtimes is detectable rather than
assumed away.

16 contracts are declared, each with namespace, API version, schema version,
scope, capabilities, error semantics and a compatibility rule:

```text
wanxiang.identity@1          wanxiang.history@1        wanxiang.actor@1
wanxiang.reality.observe@1   wanxiang.branch@1         wanxiang.model@1
wanxiang.reality.proposal@1  wanxiang.lineage@1        wanxiang.capability@1
wanxiang.reality.policy@1    wanxiang.replay@1         wanxiang.reality.profile@1
wanxiang.authority@1         wanxiang.evidence@1       wanxiang.execution@1
wanxiang.rights@1
```

Seam digest at this tree:
`b1864b952a2abd157718b92b99980acb93f2e85b6ed66d67b8bdf019b5a37fc9`
(sha256 over the sorted `id -> apiVersion` map, recorded in
`artifacts/r7/composition/resolved_graph.json`).

## Provider / consumer rule

Consumers depend on a seam, never on a provider implementation or on
provider-internal modules. Two guards enforce it:

* `packages/cordis_host/src/architecture.test.ts` — only `authority.ts` may reach
  the capability mint; `bundle.ts` (the reference plugin) must not mention the
  concrete history provider or the mint, and must import the authority seam.
* The Python side keeps the existing repository guards green
  (`uv run python scripts/architecture_check.py` → PASS).

## Consumer-side seam types

`packages/cordis_host/src/history.ts` defines the history seam as an interface
(`head`, `read`, `append`, `checkpoint`, `worldlines`) plus a provider port. Two
implementations are planned against that port: the in-process reference provider
(implemented and certified by the spike) and the JSON-RPC provider bridging to the
Python authority (not implemented).

## Boundaries

* IMPLEMENTED: 16 versioned contracts (Python + TS identity map), seam digest,
  history seam with a provider port, architecture guards on both sides.
* VALIDATED: Python contract tests (30 in `tests/unit/reality`), TS architecture
  guard tests, `tsc` + ESLint clean, repository quality gate PASS.
* NOT_PROVEN: cross-language seam digest equality at runtime (the TS digest is
  recorded; the Python side computes its own over a richer table, so an automated
  equality check is still missing), and the JSON-RPC provider.
