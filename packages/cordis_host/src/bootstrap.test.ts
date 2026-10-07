import { describe, expect, it } from "vitest";

import { bootstrapWorld, BootstrapError } from "./bootstrap";
import { MemoryHistoryProvider } from "./history";
import { sampleRuntimeLockRef } from "./testing";

describe("R7 World Bootstrap", () => {
  it("opens only after lock/seam/history checks and exposes no commit authority", async () => {
    const lockRef = sampleRuntimeLockRef({ lockId: "lock_bootstrap" });
    const boot = await bootstrapWorld({
      worldId: "world_bootstrap",
      worldlineId: "wl_bootstrap",
      lockRef,
      expectedHistoryHead: { revision: 0, stateHash: "" },
    });

    expect(boot.lockRef.lockDigest).toBe(lockRef.lockDigest);
    expect(boot.head).toEqual({ revision: 0, stateHash: "" });
    expect(boot.resolvedGraph().runtimeLocks[0]?.worldlineId).toBe("wl_bootstrap");
    expect("commit" in boot).toBe(false);
    expect("authority" in boot).toBe(false);
    expect("root" in boot).toBe(false);

    await boot.close();
  });

  it("fails closed when the authoritative history head disagrees", async () => {
    const provider = new MemoryHistoryProvider();
    provider.append({
      worldlineId: "wl_head_mismatch",
      expectedRevision: 0,
      events: [{ eventId: "evt-1", kind: "test", payloadDigest: "a".repeat(64) }],
    });

    await expect(
      bootstrapWorld({
        worldId: "world_head_mismatch",
        worldlineId: "wl_head_mismatch",
        lockRef: sampleRuntimeLockRef({ lockId: "lock_head_mismatch" }),
        providerFactory: () => provider,
        expectedHistoryHead: { revision: 0, stateHash: "" },
      }),
    ).rejects.toThrowError(BootstrapError);
  });

  it("fails closed on an invalid runtime lock rather than best-effort booting", async () => {
    const broken = sampleRuntimeLockRef({ compositionRuntimeVersion: "0.0.1" });
    await expect(
      bootstrapWorld({
        worldId: "world_invalid_lock",
        worldlineId: "wl_invalid_lock",
        lockRef: broken,
      }),
    ).rejects.toThrowError(/runtime lock pins cordis 0\.0\.1/);
  });
});
