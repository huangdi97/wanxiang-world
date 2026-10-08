import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

import { Context } from "cordis";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { RpcAuthorityBootstrap, RpcHistoryProvider } from "./bridge";
import {
  RPC_UNKNOWN_METHOD,
  RpcProtocolError,
  RpcStdioClient,
  type RpcMethod,
  type RpcTransportOptions,
} from "./bridge_protocol";
import { seamDigest } from "./contracts";
import {
  CommitDeniedError,
  HistoryService,
  RevisionConflictError,
  type AppendRequest,
  type HistoryProvider,
  type WorldEvent,
} from "./history";
import { mintCapability } from "./internal/capability-core";

/**
 * Stub authority speaking the frozen protocol: `__slow__` delays an answer,
 * `__garbage__` writes a non-JSON line and `__badid__` answers with an id no
 * request is waiting for. The fold rule is the frozen one.
 */
const STUB_SOURCE = `"use strict";
const crypto = require("node:crypto");
const readline = require("node:readline");
const events = new Map(), hashes = new Map(), holders = new Map(), tokens = new Set();
function fold(state, event) { return crypto.createHash("sha256").update(state + "|" + event.eventId + ":" + event.payloadDigest, "utf8").digest("hex"); }
function list(id) { return events.get(id) || []; }
function head(id) { return { revision: list(id).length, stateHash: hashes.get(id) || "" }; }
function reply(id, result) { process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result }) + "\\n"); }
function fail(id, code, message, data) { process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message, data: data || {} } }) + "\\n"); }
function rpcError(code, message, data) { const error = new Error(message); error.rpc = { code, message, data: data || {} }; return error; }
const handlers = {
  "runtime.info": () => ({ server: "wanxiang-reality-rpc-stub", version: "0.0.1", schema: "wanxiang.r7.history-rpc.v1" }),
  "seam.digest": () => ({ digest: "stub-digest", contracts: [] }),
  "authority.register_holder": (p) => { holders.set(p.holderId, p.auditRef); return { holderId: p.holderId, registered: true }; },
  "authority.grant": (p) => {
    if (!holders.has(p.holderId)) throw rpcError(-32002, "unknown holder", { reason: "unknown-holder" });
    const token = "stub-token-" + (tokens.size + 1);
    tokens.add(token);
    return { holderId: p.holderId, capabilityToken: token };
  },
  "history.head": (p) => head(p.worldlineId),
  "history.read": (p) => ({ events: list(p.worldlineId).slice(p.fromRevision) }),
  "history.checkpoint": (p) => head(p.worldlineId),
  "history.worldlines": () => ({ worldlines: Array.from(events.keys()).sort() }),
  "history.append": (p) => {
    if (!tokens.has(p.capabilityToken)) throw rpcError(-32002, "capability token is not valid", { reason: "unknown-capability-token" });
    if (p.expectedRevision !== list(p.worldlineId).length) {
      throw rpcError(-32001, "stale expected revision", { expectedRevision: p.expectedRevision, actualRevision: list(p.worldlineId).length });
    }
    let state = hashes.get(p.worldlineId) || "";
    for (const event of p.events) state = fold(state, event);
    events.set(p.worldlineId, list(p.worldlineId).concat(p.events));
    hashes.set(p.worldlineId, state);
    return { revision: list(p.worldlineId).length, stateHash: state, eventIds: p.events.map((event) => event.eventId) };
  },
};
readline.createInterface({ input: process.stdin, crlfDelay: Infinity }).on("line", (line) => {
  if (line.trim() === "") return;
  const request = JSON.parse(line);
  const worldlineId = request.params && request.params.worldlineId;
  const respond = () => {
    try {
      const handler = handlers[request.method];
      if (!handler) throw rpcError(-32601, "unknown method: " + request.method);
      reply(request.id, handler(request.params || {}));
    } catch (error) {
      const payload = error.rpc || { code: -32603, message: "internal error", data: {} };
      fail(request.id, payload.code, payload.message, payload.data);
    }
  };
  if (worldlineId === "__garbage__") process.stdout.write("this is not json\\n");
  else if (worldlineId === "__badid__") reply(999999, {});
  else if (worldlineId === "__slow__") setTimeout(respond, 10000);
  else respond();
});
`;

const STUB_PATH = join(mkdtempSync(join(tmpdir(), "wanxiang-rpc-stub-")), "authority_stub.cjs");
writeFileSync(STUB_PATH, STUB_SOURCE);

const HOLDER = "holder-r7";

/** The harness is inferred from `startStub` so the fixture has one definition. */
type StubHarness = ReturnType<typeof startStub>;

function startStub(requestTimeoutMs = 2000) {
  const options: RpcTransportOptions = { command: [process.execPath, STUB_PATH], cwd: tmpdir(), requestTimeoutMs };
  const client = new RpcStdioClient(options);
  const tokens = new Map<string, string>();
  return {
    client,
    tokens,
    provider: new RpcHistoryProvider(options, (holderId) => tokens.get(holderId), undefined, client),
    bootstrap: new RpcAuthorityBootstrap(options, undefined, client),
    dispose: () => client.dispose(),
  };
}

async function grant(stub: StubHarness, holderId: string): Promise<string> {
  await stub.bootstrap.registerHolder(holderId, `audit:${holderId}`);
  const token = await stub.bootstrap.grant(holderId);
  stub.tokens.set(holderId, token);
  return token;
}

function event(index: number): WorldEvent {
  const payloadDigest = createHash("sha256").update(`payload-${index}`).digest("hex");
  return { eventId: `evt-${index}`, kind: "test.event", payloadDigest };
}

/** Independent implementation of the frozen fold rule, used as the oracle. */
function foldEvents(events: readonly WorldEvent[]): string {
  let state = "";
  for (const one of events) {
    state = createHash("sha256").update(`${state}|${one.eventId}:${one.payloadDigest}`, "utf8").digest("hex");
  }
  return state;
}

async function rejection(promise: Promise<unknown>): Promise<unknown> {
  return promise.then(
    () => null,
    (error: unknown) => error,
  );
}

describe("RpcHistoryProvider over the frozen stdio protocol", () => {
  let stub: StubHarness;

  beforeEach(() => {
    stub = startStub();
  });

  afterEach(async () => {
    await stub.dispose();
  });

  it("reads an empty worldline head, events and checkpoint", async () => {
    expect(await stub.provider.head("wl-empty")).toEqual({ revision: 0, stateHash: "" });
    expect(await stub.provider.read("wl-empty", 0)).toEqual([]);
    expect(await stub.provider.checkpoint("wl-empty")).toEqual({ revision: 0, stateHash: "" });
    expect(await stub.provider.worldlines()).toEqual([]);
  });

  it("appends events and reports revision, state hash and event ids", async () => {
    await grant(stub, HOLDER);
    const events = [event(1), event(2)];
    const appended = { worldlineId: "wl-a", expectedRevision: 0, authorityHolderId: HOLDER, events };
    const result = await stub.provider.append(appended);
    expect(result).toEqual({ revision: 2, stateHash: foldEvents(events), eventIds: ["evt-1", "evt-2"] });
    expect(await stub.provider.head("wl-a")).toEqual({ revision: 2, stateHash: foldEvents(events) });
    expect(await stub.provider.read("wl-a", 1)).toEqual(events.slice(1));
    expect(await stub.provider.worldlines()).toEqual(["wl-a"]);
  });

  it("folds incremental and batched appends to the same state hash", async () => {
    await grant(stub, HOLDER);
    const events = [event(1), event(2), event(3)];
    let revision = 0;
    for (const one of events) {
      await stub.provider.append({ worldlineId: "wl-incremental", expectedRevision: revision, authorityHolderId: HOLDER, events: [one] });
      revision += 1;
    }
    const batched = await stub.provider.append({ worldlineId: "wl-batched", expectedRevision: 0, authorityHolderId: HOLDER, events });
    expect(batched.stateHash).toBe(foldEvents(events));
    expect(await stub.provider.head("wl-incremental")).toEqual({ revision: 3, stateHash: batched.stateHash });
  });

  it("maps a stale expected revision to RevisionConflictError", async () => {
    await grant(stub, HOLDER);
    await stub.provider.append({ worldlineId: "wl-a", expectedRevision: 0, authorityHolderId: HOLDER, events: [event(1)] });
    const failure = await rejection(stub.provider.append({ worldlineId: "wl-a", expectedRevision: 0, authorityHolderId: HOLDER, events: [event(2)] }));
    expect(failure).toBeInstanceOf(RevisionConflictError);
    if (failure instanceof RevisionConflictError) {
      expect(failure.worldlineId).toBe("wl-a");
      expect(failure.expectedRevision).toBe(0);
      expect(failure.actualRevision).toBe(1);
    }
  });

  it("maps a rejected capability token to CommitDeniedError", async () => {
    stub.tokens.set("holder-ghost", "not-a-real-token");
    const failure = await rejection(stub.provider.append({ worldlineId: "wl-a", expectedRevision: 0, authorityHolderId: "holder-ghost", events: [event(1)] }));
    expect(failure).toBeInstanceOf(CommitDeniedError);
  });

  it("maps an unknown method to RpcProtocolError with the frozen code", async () => {
    // The typed client only names frozen methods; this case bypasses that union
    // on purpose to prove the unknown-method mapping.
    const unknownMethod: string = "history.unknown";
    const failure = await rejection(stub.client.call(unknownMethod as RpcMethod, {}));
    expect(failure).toBeInstanceOf(RpcProtocolError);
    if (failure instanceof RpcProtocolError) expect(failure.code).toBe(RPC_UNKNOWN_METHOD);
  });

  it("refuses an append without a capability token before spawning the authority", async () => {
    const missing = new RpcHistoryProvider({ command: [join(tmpdir(), "wanxiang-missing-authority")], cwd: tmpdir() }, () => undefined);
    const noToken = await rejection(missing.append({ worldlineId: "wl-a", expectedRevision: 0, authorityHolderId: HOLDER, events: [event(1)] }));
    expect(noToken).toBeInstanceOf(RpcProtocolError);
    if (noToken instanceof RpcProtocolError) expect(noToken.message).toContain(HOLDER);
    const noHolder = await rejection(stub.provider.append({ worldlineId: "wl-a", expectedRevision: 0, events: [event(1)] }));
    expect(noHolder).toBeInstanceOf(RpcProtocolError);
    await missing.dispose();
  });

  it("rejects a request that exceeds the timeout with RpcProtocolError", async () => {
    await stub.dispose();
    stub = startStub(200);
    const started = Date.now();
    const failure = await rejection(stub.provider.head("__slow__"));
    expect(failure).toBeInstanceOf(RpcProtocolError);
    if (failure instanceof RpcProtocolError) expect(failure.message).toContain("timed out");
    expect(Date.now() - started).toBeLessThan(5000);
  });

  it("raises RpcProtocolError when the authority writes a line that is not JSON", async () => {
    const failure = await rejection(stub.provider.head("__garbage__"));
    expect(failure).toBeInstanceOf(RpcProtocolError);
    if (failure instanceof RpcProtocolError) expect(failure.message).toContain("not valid JSON");
  });

  it("raises RpcProtocolError when a response id has no pending request", async () => {
    const failure = await rejection(stub.provider.head("__badid__"));
    expect(failure).toBeInstanceOf(RpcProtocolError);
    if (failure instanceof RpcProtocolError) expect(failure.message).toContain("no pending request");
  });

  it("bootstraps a holder and grants a capability token", async () => {
    const info = await stub.bootstrap.info();
    expect(info.server).toBe("wanxiang-reality-rpc-stub");
    expect(info.schema).toBe("wanxiang.r7.history-rpc.v1");
    expect(await stub.bootstrap.seamDigest()).toBe("stub-digest");
    expect(await stub.bootstrap.registerHolder("holder-bootstrap", "audit:bootstrap")).toEqual({ holderId: "holder-bootstrap", registered: true });
    expect((await stub.bootstrap.grant("holder-bootstrap")).length).toBeGreaterThan(0);
    expect(await rejection(stub.bootstrap.grant("holder-unregistered"))).toBeInstanceOf(CommitDeniedError);
  });
});

describe("history seam capability stamping", () => {
  it("stamps the capability holder onto the append request for the provider", () => {
    const captured: AppendRequest[] = [];
    const provider: HistoryProvider = {
      providerId: "capture",
      providerVersion: "1.0.0",
      head: () => ({ revision: 0, stateHash: "" }),
      read: () => [],
      append: (request) => { captured.push(request); return { revision: 0, stateHash: "", eventIds: [] }; },
      checkpoint: () => ({ revision: 0, stateHash: "" }),
      worldlines: () => [],
    };
    const capability = mintCapability({ holderId: "holder-seam", issuedAtMs: 0, auditRef: "audit:seam" });
    new HistoryService(new Context(), provider).append(capability, { worldlineId: "wl-a", expectedRevision: 0, events: [event(1)] });
    expect(captured[0]?.authorityHolderId).toBe("holder-seam");
  });
});

/**
 * The cross-language test drives the real Python authority process, so it needs
 * the Python toolchain. CI's `ts` job provisions uv and syncs the workspace,
 * which means the test runs for real there; a workstation without uv reports a
 * skip with an explicit reason instead of a misleading failure.
 */
const PYTHON_SEAM_SKIP_REASON =
  "uv is not on PATH: install uv (this repository's CI provisions it) to run the cross-language seam test";
const pythonToolchainAvailable =
  spawnSync("uv", ["--version"], { stdio: "ignore" }).status === 0;
if (!pythonToolchainAvailable) {
  console.warn(PYTHON_SEAM_SKIP_REASON);
}

describe.skipIf(!pythonToolchainAvailable)("python authority integration", () => {
  it("matches the python seam digest and commits through a real grant", async () => {
    const transport: RpcTransportOptions = {
      command: ["uv", "run", "python", "-m", "wanxiang_reality.rpc", "--stdio"],
      cwd: resolve(process.cwd(), "..", ".."),
      // Generous on purpose: a cold `uv run` resolves and syncs before it answers.
      requestTimeoutMs: 120_000,
    };
    const client = new RpcStdioClient(transport);
    const bootstrap = new RpcAuthorityBootstrap(transport, undefined, client);
    try {
      const info = await bootstrap.info().catch((error: unknown) => {
        const message = error instanceof Error ? error.message : String(error);
        throw new Error(`python authority process failed to start: ${message}`);
      });
      expect(info.server).toBe("wanxiang-reality-rpc");
      expect(await bootstrap.seamDigest()).toBe(seamDigest());
      await bootstrap.registerHolder("r7-bridge-test", "audit:r7-bridge-test");
      const tokens = new Map([["r7-bridge-test", await bootstrap.grant("r7-bridge-test")]]);
      const provider = new RpcHistoryProvider(transport, (holderId) => tokens.get(holderId), undefined, client);
      const first = await provider.append({ worldlineId: "wl-integration", expectedRevision: 0, authorityHolderId: "r7-bridge-test", events: [event(1)] });
      expect(first).toEqual({ revision: 1, stateHash: foldEvents([event(1)]), eventIds: ["evt-1"] });
      const failure = await rejection(provider.append({ worldlineId: "wl-integration", expectedRevision: 0, authorityHolderId: "r7-bridge-test", events: [event(2)] }));
      expect(failure).toBeInstanceOf(RevisionConflictError);
    } finally {
      await client.dispose();
    }
  });
});
