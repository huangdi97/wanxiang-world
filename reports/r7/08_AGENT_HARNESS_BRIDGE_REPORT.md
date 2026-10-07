# R7 08 — Agent Harness / DeepSeek Harness Integration

Status:
- reference bridge/protocol: `IMPLEMENTED / VALIDATED`;
- official DeepSeek Harness SDK adapter: `IMPLEMENTED`;
- live model-backed official DSH E2E: `EXTERNAL_BLOCKED`.

## Reference bridge

`wanxiang.r7.agent-harness-rpc.v1` supplies read-only WorldObservation,
proposal/abstention decisions and committed/rejected consequences. The
deterministic reference harness runs as a real subprocess and declares
`officialDsh=false`. The Cordis consequence path covers accepted and rejected
flows.

## Official adapter

`wanxiang_runtime.deepseek_harness_provider` lazily imports the official
`deepseek-harness-sdk` when available. It sends only bounded observation,
requests exact structured JSON, treats returned actions as proposals, lets
Wanxiang derive/verify payload digests, and reports committed/rejected
consequences to the same durable session. It imports no Commit Authority or
persistence writer.

Unit tests inject an SDK test double to qualify adapter behavior without
misreporting a live DSH run.

## Evidence boundary

Adapter code plus reference protocol tests do not prove a real model-backed DSH
session. That row stays `EXTERNAL_BLOCKED` until the official runtime route and
credentials are actually available and exercised.
