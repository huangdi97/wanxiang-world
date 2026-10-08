import { describe, expect, it } from "vitest";
import cordisPackage from "cordis/package.json";

import { CONTRACT_IDS } from "./contracts";
import { createHost } from "./host";
import {
  createRuntimeLockRef,
  RuntimeLockError,
  validateRuntimeLockRef,
  type RuntimeLockRef,
} from "./lock";
import { sampleProfileRef, sampleRuntimeLockRef } from "./testing";

describe("R7 worldline runtime lock pinning", () => {
  it("accepts a lock that pins every required seam", () => {
    const ref = sampleRuntimeLockRef();
    expect(() => validateRuntimeLockRef(ref)).not.toThrow();
    expect(Object.keys(ref.serviceContractVersions).sort()).toEqual([...CONTRACT_IDS].sort());
  });

  it("rejects a lock that omits a required seam", () => {
    const ref = sampleRuntimeLockRef();
    const seams: Record<string, string> = { ...ref.serviceContractVersions };
    delete seams["wanxiang.history@1"];
    const broken: RuntimeLockRef = { ...ref, serviceContractVersions: seams };

    expect(() => validateRuntimeLockRef(broken)).toThrowError(RuntimeLockError);
  });

  it("rejects a seam version that drifted from what this host provides", () => {
    const broken = sampleRuntimeLockRef({
      serviceContractVersions: { "wanxiang.history@1": "2" },
    });

    expect(() => validateRuntimeLockRef(broken)).toThrowError(/wanxiang\.history@1/);
  });

  it("rejects a malformed lock digest or profile version", () => {
    expect(() => validateRuntimeLockRef(sampleRuntimeLockRef({ lockDigest: "nope" }))).toThrowError(
      RuntimeLockError,
    );
    const badProfile = { ...sampleProfileRef("reality:persistent-v1"), version: "v1" };
    expect(() =>
      validateRuntimeLockRef(sampleRuntimeLockRef({ realityProfile: badProfile })),
    ).toThrowError(RuntimeLockError);
  });

  it("refuses to open a worldline whose lock pins another composition runtime", () => {
    const otherRuntime = sampleRuntimeLockRef({ compositionRuntimeVersion: "0.0.1" });
    expect(() => createHost({ lockRef: otherRuntime })).toThrowError(RuntimeLockError);
  });

  it("builds a lock reference for the seams the host composes", () => {
    const ref = createRuntimeLockRef({
      lockId: "lock_built",
      lockVersion: "2",
      lockDigest: "a".repeat(64),
      realityProfile: sampleProfileRef("reality:persistent-v2", "2"),
      worldProfile: sampleProfileRef("world:built"),
      compositionRuntimeVersion: cordisPackage.version,
      providerVersions: { "history-memory": "1.0.0" },
    });

    expect(ref.compositionRuntime).toEqual({ name: "cordis", version: cordisPackage.version });
    expect(ref.lockVersion).toBe("2");
    expect(Object.keys(ref.serviceContractVersions)).toHaveLength(CONTRACT_IDS.length);
  });

  it("carries the pinned lock into the resolved capability graph", async () => {
    const lockRef = sampleRuntimeLockRef({ lockId: "lock_graph" });
    const host = createHost({ lockRef });
    host.openWorld("world_lock", "wl_lock");

    const graph = host.resolvedGraph();
    expect(graph.runtimeLocks).toHaveLength(1);
    expect(graph.runtimeLocks[0]?.worldlineId).toBe("wl_lock");
    expect(graph.runtimeLocks[0]?.lockId).toBe("lock_graph");
    expect(graph.runtimeLocks[0]?.lockDigest).toBe(lockRef.lockDigest);
    expect(graph.runtimeLocks[0]?.compositionRuntime.version).toBe(cordisPackage.version);
    await host.dispose();
  });
});
