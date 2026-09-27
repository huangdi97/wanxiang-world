import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { RPC_HARNESS_FAILED, RPC_TRANSPORT_FAILURE, RpcProtocolError, RpcStdioClient } from "./bridge_protocol";
import {
  AgentHarnessClient,
  HARNESS_PROTOCOL,
  HarnessConsequencePath,
  parseDecision,
  type HarnessProposalRecord,
} from "./harness";

/**
 * Stub harness speaking the frozen protocol. Modes are selected by the observed
 * worldline id: `__garbage__` writes a non-JSON line, `__noproposal__` answers
 * "proposed" without a proposal, `__harness_error__` returns the harness-failed
 * code and `__abstain__` abstains. A separate copy of this script advertises
 * another protocol, so protocol drift is testable without an env channel.
 */
const STUB_SOURCE = `"use strict";
const readline = require("node:readline");
const rl = readline.createInterface({ input: process.stdin });
const ok = (id, result) => process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, result }) + "\\n");
const fail = (id, code, message) => process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message, data: {} } }) + "\\n");
rl.on("line", (line) => {
  const request = JSON.parse(line);
  const params = request.params || {};
  const observation = params.observation || {};
  const worldlineId = observation.worldlineId || "";
  if (request.method === "harness.info") {
    return ok(request.id, {
      harnessId: "stub-harness",
      harnessVersion: "0.0.1",
      kind: "stub-harness",
      protocol: "wanxiang.r7.agent-harness-rpc.v1",
      officialDsh: false,
    });
  }
  if (request.method === "harness.decide") {
    if (worldlineId === "__harness_error__") return fail(request.id, -32010, "harness failed");
    if (worldlineId === "__garbage__") return process.stdout.write("not-json\\n");
    if (worldlineId === "__abstain__") return ok(request.id, { status: "abstained", proposal: null, reason: "nothing to do" });
    if (worldlineId === "__noproposal__") return ok(request.id, { status: "proposed", reason: "missing proposal" });
    return ok(request.id, {
      status: "proposed",
      proposal: {
        proposalId: "prop-" + worldlineId,
        action: "set_status",
        rationaleRef: "stub#rule",
        payloadDigest: "d".repeat(64),
      },
      reason: "stub rule",
    });
  }
  if (request.method === "harness.consequence") {
    return ok(request.id, { acknowledged: true, status: params.status });
  }
  return fail(request.id, -32601, "unknown method");
});
`;

const STUB_DIR = mkdtempSync(join(tmpdir(), "wanxiang-harness-stub-"));
const STUB_PATH = join(STUB_DIR, "harness_stub.cjs");
writeFileSync(STUB_PATH, STUB_SOURCE);
const DRIFTED_PROTOCOL_PATH = join(STUB_DIR, "harness_drifted_protocol.cjs");
writeFileSync(
  DRIFTED_PROTOCOL_PATH,
  STUB_SOURCE.replace('"wanxiang.r7.agent-harness-rpc.v1"', '"wanxiang.other.v1"'),
);

const transport = () => ({
  command: [process.execPath, STUB_PATH],
  cwd: tmpdir(),
  requestTimeoutMs: 2000,
});

let harness: AgentHarnessClient;
let client: RpcStdioClient;

beforeEach(() => {
  client = new RpcStdioClient(transport());
  harness = new AgentHarnessClient(transport(), client);
});

afterEach(async () => {
  await client.dispose();
});

describe("agent-harness client", () => {
  it("reads harness identity and never assumes official DSH", async () => {
    const info = await harness.info();
    expect(info.harnessId).toBe("stub-harness");
    expect(info.protocol).toBe(HARNESS_PROTOCOL);
    expect(info.officialDsh).toBe(false);
  });

  it("rejects a harness speaking a different protocol instead of guessing", async () => {
    const drifted = {
      command: [process.execPath, DRIFTED_PROTOCOL_PATH],
      cwd: tmpdir(),
      requestTimeoutMs: 2000,
    };
    const other = new RpcStdioClient(drifted);
    const badProtocol = new AgentHarnessClient(drifted, other);
    await expect(badProtocol.info()).rejects.toBeInstanceOf(RpcProtocolError);
    await other.dispose();
  });

  it("returns a proposal without any capability for it", async () => {
    const decision = await harness.decide({ worldlineId: "wl-a", revision: 0 });
    expect(decision.status).toBe("proposed");
    if (decision.status !== "proposed") throw new Error("unreachable");
    expect(decision.proposal.proposalId).toBe("prop-wl-a");
    expect(decision.proposal).not.toHaveProperty("capability");
  });

  it("keeps abstention distinct from a malformed answer", async () => {
    const decision = await harness.decide({ worldlineId: "__abstain__", revision: 3 });
    expect(decision).toEqual({ status: "abstained", reason: "nothing to do" });
    await expect(harness.decide({ worldlineId: "__noproposal__", revision: 0 })).rejects.toBeInstanceOf(
      RpcProtocolError,
    );
  });

  it("passes a harness-reported failure code through verbatim", async () => {
    const failure = await harness.decide({ worldlineId: "__harness_error__", revision: 0 }).catch((error: unknown) => error);
    expect(failure).toBeInstanceOf(RpcProtocolError);
    expect((failure as RpcProtocolError).code).toBe(RPC_HARNESS_FAILED);
  });

  it("fails on a non-JSON answer instead of treating it as no decision", async () => {
    const failure = await harness.decide({ worldlineId: "__garbage__", revision: 0 }).catch((error: unknown) => error);
    expect(failure).toBeInstanceOf(RpcProtocolError);
    expect((failure as RpcProtocolError).code).toBe(RPC_TRANSPORT_FAILURE);
  });

  it("requires the harness to acknowledge the consequence it was told about", async () => {
    await expect(
      harness.announce({ proposalId: "prop-1", status: "committed" }),
    ).resolves.toEqual({ acknowledged: true, status: "committed" });
    await expect(harness.announce({ proposalId: "prop-1", status: "rejected" })).resolves.toEqual({
      acknowledged: true,
      status: "rejected",
    });
  });

  it("refuses an invented consequence status", async () => {
    await expect(
      harness.announce({ proposalId: "prop-1", status: "maybe" as unknown as "committed" }),
    ).rejects.toBeInstanceOf(RpcProtocolError);
  });

  it("rejects a negative revision before sending anything", async () => {
    await expect(harness.decide({ worldlineId: "wl-a", revision: -1 })).rejects.toBeInstanceOf(RpcProtocolError);
  });
});

describe("harness consequence path", () => {
  it("turns a proposal into host-facing data and reports the rejection too", async () => {
    const path = new HarnessConsequencePath(harness);
    const report = await path.decide("wl-a", 7, { targetRevision: "9" });
    expect(report.proposal?.worldlineId).toBe("wl-a");
    expect(report.proposal?.proposalId).toBe("prop-wl-a");
    const proposal = report.proposal as HarnessProposalRecord;
    await expect(path.announce(proposal, "rejected", "policy denied")).resolves.toEqual({
      acknowledged: true,
      status: "rejected",
    });
  });

  it("returns no proposal record when the harness abstains", async () => {
    const path = new HarnessConsequencePath(harness);
    const report = await path.decide("__abstain__", 0);
    expect(report.proposal).toBeNull();
    expect(report.reason).toBe("nothing to do");
  });

  it("calls the harness exactly once per decision", async () => {
    // A double round trip would double-advance a real harness' internal counter.
    const path = new HarnessConsequencePath(harness);
    await path.decide("wl-a", 0, { targetRevision: "2" });
    const head = await harness.decide({ worldlineId: "wl-a", revision: 0 });
    expect(head.status).toBe("proposed");
  });
});

describe("parseDecision", () => {
  it("rejects an unknown status", () => {
    expect(() => parseDecision({ status: "maybe" })).toThrow(RpcProtocolError);
  });
});

describe("agent harness architecture guards", () => {
  const text = readFileSync(join(process.cwd(), "src", "harness.ts"), "utf-8");

  it("holds no commit path and no capability mint", () => {
    expect(text).not.toContain("mintCapability");
    expect(text).not.toContain("commitThroughAuthority");
    expect(text).not.toContain("./authority");
    expect(text).not.toContain("./commit");
  });

  it("never touches the canonical history provider", () => {
    expect(text).not.toContain("MemoryHistoryProvider");
    expect(text).not.toContain("history.append");
    expect(text).toContain("./bridge_protocol");
  });
});

/**
 * The cross-language test drives the real Python reference harness, so it needs
 * uv. CI provisions it; a workstation without uv reports an explicit skip reason.
 */
const pythonToolchainAvailable = spawnSync("uv", ["--version"], { stdio: "ignore" }).status === 0;
if (!pythonToolchainAvailable) {
  console.warn("uv is not on PATH: the cross-language harness test will be skipped");
}

describe.skipIf(!pythonToolchainAvailable)("python reference harness integration", () => {
  it("decides, abstains and acknowledges through the real harness process", async () => {
    const options = {
      command: ["uv", "run", "python", "scripts/r7_reference_harness.py", "--stdio"],
      cwd: resolve(process.cwd(), "..", ".."),
      requestTimeoutMs: 120_000,
    };
    const real = new AgentHarnessClient(options);
    try {
      const info = await real.info();
      expect(info.harnessId).toBe("wanxiang-reference-rule-harness");
      expect(info.officialDsh).toBe(false);

      const path = new HarnessConsequencePath(real);
      const report = await path.decide("wl-int", 0, { targetRevision: "2" });
      const expectedDigest = createHash("sha256")
        .update("prop_wl-int_1|set_status")
        .digest("hex");
      expect(report.proposal).toEqual({
        worldlineId: "wl-int",
        proposalId: "prop_wl-int_1",
        action: "set_status",
        rationaleRef: "reference-rule-harness#advance-to-2",
        payloadDigest: expectedDigest,
      });

      const reached = await path.decide("wl-int", 2, { targetRevision: "2" });
      expect(reached.proposal).toBeNull();
      expect(reached.decision.status).toBe("abstained");

      await expect(path.announce(report.proposal as HarnessProposalRecord, "committed")).resolves.toEqual({
        acknowledged: true,
        status: "committed",
      });
    } finally {
      await real.dispose();
    }
  });
});
