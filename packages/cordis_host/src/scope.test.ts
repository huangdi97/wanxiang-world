import { describe, expect, it } from "vitest";

import { sampleRuntimeLockRef } from "./testing";

import { actorRulePlugin, type ActorRuleConfig } from "./bundle";
import { createHost } from "./host";

const RULE_A: ActorRuleConfig = { worldlineId: "wl_a", actorId: "actor_a", salt: "salt-a" };
const RULE_B: ActorRuleConfig = { worldlineId: "wl_b", actorId: "actor_b", salt: "salt-b" };

/**
 * World scope isolation.
 *
 * Two worlds must be able to run at once, and unloading one must leave the other
 * untouched — including its committed history, which survives the unload.
 */
describe("R7 world scope isolation", () => {
  it("keeps world B intact when world A unloads", async () => {
    const host = createHost({ lockRef: sampleRuntimeLockRef() });
    host.authority.registerAuthorityHolder("world-host", "audit:scope");
    const capability = host.authority.grant("world-host");
    host.openWorld("world_a", "wl_a");
    host.openWorld("world_b", "wl_b");
    await host.scopes.load("wl_a", {
      pluginId: "actor-rule/actor_a/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin(RULE_A),
    });
    await host.scopes.load("wl_b", {
      pluginId: "actor-rule/actor_b/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin(RULE_B),
    });

    for (const worldlineId of ["wl_a", "wl_b"]) {
      const suffix = worldlineId === "wl_a" ? "a" : "b";
      for (let index = 0; index < 3; index += 1) {
        const outcome = host.commit({
          worldlineId,
          requestingWorldlineId: worldlineId,
          requestedBy: "world-host",
          ruleId: `actor-rule/actor_${suffix}/v1`,
          capability,
        });
        expect(outcome.status).toBe("COMMITTED");
      }
    }

    const headB = host.scopes.runtime("wl_b").history.head("wl_b");
    const historyA = host.scopes.runtime("wl_a").history;
    await host.scopes.closeWorldline("wl_a");

    // World A's runtime is unloaded, but its committed history is retained and
    // still readable from the retained provider.
    expect(host.scopes.isOpen("wl_a")).toBe(false);
    expect(host.scopes.isOpen("wl_b")).toBe(true);
    expect(historyA.head("wl_a").revision).toBe(3);
    const retained = host.scopes.retainedProvider("wl_a");
    expect(retained?.head("wl_a").revision).toBe(3);

    // World B is untouched by that unload.
    expect(host.scopes.runtime("wl_b").history.head("wl_b")).toEqual(headB);
    expect(host.scopes.runtime("wl_b").history.head("wl_b").revision).toBe(3);
    expect(host.authority.rulesFor("wl_b")).toEqual(["actor-rule/actor_b/v1"]);
    expect(host.authority.rulesFor("wl_a")).toEqual([]);

    await host.dispose();
  });

  it("keeps a single authority bootstrap across worlds", async () => {
    const host = createHost({ lockRef: sampleRuntimeLockRef() });
    const registryBefore = host.root.registry.size;
    host.authority.registerAuthorityHolder("world-host", "audit:scope");
    host.openWorld("world_a", "wl_a");
    host.openWorld("world_b", "wl_b");

    // Opening more worlds registers no new root-level service: there is one
    // authority bootstrap, while each worldline owns its own history instance.
    expect(host.root.registry.size).toBe(registryBefore);
    expect(host.authority.grantAudit()).toHaveLength(0);
    host.authority.grant("world-host");
    expect(host.authority.grantAudit()).toHaveLength(1);
    await host.dispose();
  });
});
