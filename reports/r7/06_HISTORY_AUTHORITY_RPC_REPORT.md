# R7 06 — History Authority JSON-RPC Seam (Python server + TS bridge)

Status: `IMPLEMENTED` / `VALIDATED` — cross-language, exercised against the real
Python process.

## 1. Wire contract (frozen)

Newline-delimited JSON-RPC 2.0 over stdio. Server entry:

```text
uv run python -m wanxiang_reality.rpc --stdio
```

| Method | Result |
|---|---|
| `runtime.info` | `{server, version, schema}` |
| `seam.digest` | `{digest, contracts[]}` |
| `authority.register_holder` | `{holderId, registered}` |
| `authority.grant` | `{holderId, token, auditRef}` |
| `history.head` / `history.read` / `history.checkpoint` / `history.worldlines` | read-only projections |
| `history.append` | `{revision, stateHash, eventIds}` |

Errors: `-32700` parse, `-32600` invalid request, `-32601` unknown method,
`-32602` invalid params, `-32603` internal, `-32001` revision conflict (with
`expectedRevision`/`actualRevision`), `-32002` commit denied.

State hash fold (frozen, batch-invariant): `state = ""`, then for every event
`state = sha256_hex((state + "|" + eventId + ":" + payloadDigest).encode("utf-8"))`.

`seam.digest` hashes the compact JSON of `{id, apiVersion}` pairs sorted by id, so
Python and TypeScript produce identical bytes.

## 2. Implementation

| Artefact | Responsibility |
|---|---|
| `packages/reality/src/wanxiang_reality/rpc.py` | `HistoryAuthority` + dispatcher + `serve_stdio` |
| `packages/reality/src/wanxiang_reality/rpc_support.py` | error codes, `HistoryEvent`, param decoders, envelopes, `seam_digest`, UTF-8 stdio on Windows |
| `tests/unit/reality/test_rpc.py` | 15 behaviour tests, including a real subprocess end-to-end run |
| `packages/cordis_host/src/bridge_protocol.ts` | serialized stdio client: one in-flight request, per-request id, timeout, fatal transport failures |
| `packages/cordis_host/src/bridge.ts` | `RpcHistoryProvider` (`AsyncHistoryProvider`), `RpcAuthorityBootstrap`, `-32001`/`-32002` -> typed domain errors |
| `packages/cordis_host/src/bridge.test.ts` | stub-authority tests plus one real cross-language test |

## 3. Authority invariants

- `history.append` requires a capability token obtained from `authority.grant`;
  a holder without a token, or an unknown holder, is denied with `-32002` and the
  stored state is unchanged.
- A stale `expectedRevision` is rejected with `-32001`; nothing is written.
- The client rejects a request without `authorityHolderId` locally and sends
  nothing (no accidental unauthenticated append).
- The TS provider returns promises, so the synchronous `HistoryProvider` seam is
  unchanged; the async seam is a separate, additive interface.

## 4. Evidence

```text
uv run pytest tests/unit/reality/test_rpc.py -q        -> 15 passed (real subprocess run included)
pnpm -C packages/cordis_host exec vitest run           -> 7 files / 41 tests passed
  - "python authority integration > matches the python seam digest and commits through a real grant"
    asserts info().server == "wanxiang-reality-rpc", seamDigest() == Python digest,
    a real grant, one committed append and a -32001 conflict.
seam digest (both sides) = b1864b952a2abd157718b92b99980acb93f2e85b6ed66d67b8bdf019b5a37fc9
```

The CI `ts` job now provisions uv and syncs the Python workspace, so this
cross-language test runs for real in CI; a workstation without uv reports an
explicit skip reason instead of a misleading failure.

## 5. Not claimed

- This is a loopback authority for one worldline store; no remote/multi-tenant
  transport, TLS or rate limiting is implemented.
- Token issuance is in-process and ephemeral (`uuid4`-based); tokens are not
  persisted across server restarts, which is stated in the test suite.
