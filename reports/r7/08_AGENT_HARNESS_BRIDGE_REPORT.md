# R7 08 — Agent-Harness Bridge (DSH seam) and Reference Harness

Status: `IMPLEMENTED` / `VALIDATED` for the bridge and the reference harness.
Official DeepSeek Harness (DSH) integration: `NOT_IMPLEMENTED` — the official
harness binary was never provided in this environment, so nothing about it is
claimed.

## 1. What was built

| Artefact | Responsibility |
|---|---|
| `packages/runtime/src/wanxiang_runtime/r7_agent_harness_contract.py` | `WorldObservation`, `AgentProposal`, `AgentDecision`, `HarnessConsequence`, `HarnessInfo`, `AgentHarnessProvider` port, `parse_decision`, typed errors |
| `packages/runtime/src/wanxiang_runtime/r7_agent_harness.py` | `JsonRpcAgentHarnessProvider`: newline-delimited JSON-RPC stdio transport with a threaded reader that enforces the request timeout |
| `scripts/r7_reference_harness.py` | a real harness process implementing the protocol with a deterministic rule; reports `officialDsh: false` |
| `tests/unit/runtime/test_r7_agent_harness.py` | 14 tests, including a real subprocess run of the reference harness |
| `packages/cordis_host/src/harness.ts` | `AgentHarnessClient` + `HarnessConsequencePath`: the host-side consequence path (decide, then announce committed/rejected) |
| `packages/cordis_host/src/harness.test.ts` | 16 tests: stub harness (protocol drift, malformed answer, harness-failed code, abstention) plus a real cross-language run of the reference harness |

Protocol: `wanxiang.r7.agent-harness-rpc.v1`; methods `harness.info`,
`harness.decide`, `harness.consequence`; errors `-32601` unknown method,
`-32602` invalid params, `-32010` harness failed.

## 2. Invariants

- The harness is an **independent provider**: it observes a read-only world view,
  proposes, and receives the committed/rejected consequence. The bridge contains
  no commit path and no authority, and a guard test asserts that.
- An answer that does not match the protocol is a typed protocol error, never a
  silent default: a missing/ill-typed field cannot become an empty proposal.
- A harness that dies or exceeds the timeout surfaces as `HarnessUnavailable`.
- The reference harness is explicitly labelled a reference rule harness; nothing
  in the repository presents it as the official DSH.
- A harness advertising a different protocol is refused instead of guessed, and
  the host-side path makes exactly one harness call per decision (a double round
  trip would double-advance a real harness' internal state).
- The consequence path is binding in both directions: a rejection is announced as
  a rejection, so a harness can never read success out of silence.


## 3. Evidence

```text
uv run pytest tests/unit/runtime/test_r7_agent_harness.py -q  -> 14 passed
uv run ruff check / pyright on the three files                -> clean
uv run python scripts/r7_reference_harness.py --stdio         -> answers harness.info with officialDsh=false
pnpm -C packages/cordis_host exec vitest run                  -> 8 files / 57 tests passed (16 in harness.test.ts, incl. the real cross-language run)
uv run python scripts/quality.py                              -> 1605 passed, architecture PASS
```

## 4. Not claimed / remaining

- No official DSH binary, model credentials or hosted agent runtime was used;
  the DSH integration is design-complete (port + protocol) but not integration-tested
  against the official harness.
- The consequence announcement path is exercised against the reference harness,
  not against a production agent loop.
- No official DSH binary, model credentials or hosted agent runtime was used, so
  the official DSH integration stays `EXTERNAL_BLOCKED`.
- The host-side consequence path exists and is tested, but no production agent
  loop drives it yet: the harness is asked to decide and is told the outcome,
  while the actual commit still happens only through the host's single commit
  path with a real capability.
