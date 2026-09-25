import { Context } from "cordis";
import { describe, expect, it } from "vitest";

import { AuthorityError, CommitAuthority } from "./authority";
import { actorRulePlugin, type ActorRuleConfig } from "./bundle";
import { CommitDeniedError, HistoryService, MemoryHistoryProvider } from "./history";
import { createHost } from "./host";
import { PolicyRegistry, resolveDecisions, type PolicyDecision } from "./policy";

const RULE: ActorRuleConfig = {
  worldlineId: "wl_authority",
  actorId: "actor_beta",
  salt: "authority-salt",
};

function hostWithWorldline(): ReturnType<typeof createHost> {
  const host = createHost();
  host.openWorld("world_authority", RULE.worldlineId);
  host.authority.registerAuthorityHolder("world-host", "audit:test");
  return host;
}

describe("R7 authority hardening", () => {
  it("refuses to grant a capability to an unregistered holder", () => {
    const ctx = new Context();
    const authority = new CommitAuthority(ctx);
    expect(() => authority.grant("stranger")).toThrowError(AuthorityError);
  });

  it("rejects a plugin that appends without a commit capability", () => {
    const ctx = new Context();
    const history = new HistoryService(ctx, new MemoryHistoryProvider());
    const forged = { holderId: "world-host", issuedAtMs: 0, auditRef: "forged" };
    expect(() =>
      history.append(forged as never, {
        worldlineId: "wl_authority",
        expectedRevision: 0,
        events: [{ eventId: "e1", kind: "k", payloadDigest: "d" }],
      }),
    ).toThrowError(CommitDeniedError);
  });

  it("denies a commit from a holder that was never granted a capability", async () => {
    const host = hostWithWorldline();
    await host.scopes.load(RULE.worldlineId, {
      pluginId: "actor-rule/actor_beta/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin(RULE),
    });
    expect(() =>
      host.commit({
        worldlineId: RULE.worldlineId,
        requestingWorldlineId: RULE.worldlineId,
        requestedBy: "world-host",
        ruleId: "actor-rule/actor_beta/v1",
        capability: { holderId: "world-host" },
      }),
    ).toThrowError(CommitDeniedError);
    expect(host.scopes.runtime(RULE.worldlineId).history.head(RULE.worldlineId).revision).toBe(0);
    await host.dispose();
  });

  it("denies a cross-worldline write without touching either history", async () => {
    const host = createHost();
    host.openWorld("world_a", "wl_a");
    host.openWorld("world_b", "wl_b");
    host.authority.registerAuthorityHolder("world-host", "audit:test");
    const capability = host.authority.grant("world-host");
    await host.scopes.load("wl_a", {
      pluginId: "actor-rule/actor_beta/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin({ ...RULE, worldlineId: "wl_a" }),
    });
    await host.scopes.load("wl_b", {
      pluginId: "actor-rule/actor_beta/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin({ ...RULE, worldlineId: "wl_b" }),
    });

    const outcome = host.commit({
      worldlineId: "wl_b",
      requestingWorldlineId: "wl_a",
      requestedBy: "world-host",
      ruleId: "actor-rule/actor_beta/v1",
      capability,
    });

    expect(outcome.status).toBe("DENIED");
    expect(outcome.resolution.hardDeniedBy).toBe("policy.cross-worldline-guard");
    expect(host.scopes.runtime("wl_b").history.head("wl_b").revision).toBe(0);
    expect(host.scopes.runtime("wl_a").history.head("wl_a").revision).toBe(0);
    await host.dispose();
  });

  it("keeps a hard deny monotonic against a later allow", () => {
    const decisions: PolicyDecision[] = [
      { providerId: "policy.rights", kind: "HARD_DENY", reason: "rights blocked" },
      { providerId: "plugin.optimistic", kind: "ALLOW", reason: "plugin says fine" },
    ];
    const resolved = resolveDecisions(decisions);
    expect(resolved.resolution).toBe("DENY");
    expect(resolved.hardDeniedBy).toBe("policy.rights");
    expect(resolved.ignoreAllowAfterHardDeny).toEqual(["plugin.optimistic"]);
  });

  it("denies an unversioned overwrite of canonical history", async () => {
    const host = hostWithWorldline();
    const capability = host.authority.grant("world-host");
    await host.scopes.load(RULE.worldlineId, {
      pluginId: "actor-rule/actor_beta/v1",
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin(RULE),
    });
    const outcome = host.commit({
      worldlineId: RULE.worldlineId,
      requestingWorldlineId: RULE.worldlineId,
      requestedBy: "world-host",
      ruleId: "actor-rule/actor_beta/v1",
      capability,
      kind: "unversioned-overwrite",
    });
    expect(outcome.status).toBe("DENIED");
    await host.dispose();
  });

  it("audits every capability it mints and keeps policy providers removable", () => {
    const ctx = new Context();
    const authority = new CommitAuthority(ctx);
    authority.registerAuthorityHolder("world-host", "audit:test");
    const first = authority.grant("world-host");
    const second = authority.grant("world-host");
    expect(authority.grantAudit()).toHaveLength(2);
    expect(authority.accepts(first)).toBe(true);
    expect(authority.accepts({ holderId: "world-host" })).toBe(false);
    expect(second.auditRef).not.toBe(first.auditRef);

    const policy = new PolicyRegistry();
    const remove = policy.register({
      providerId: "policy.temp",
      evaluate: () => ({ providerId: "policy.temp", kind: "ALLOW", reason: "temp" }),
    });
    expect(policy.providerIds()).toContain("policy.temp");
    remove();
    expect(policy.providerIds()).not.toContain("policy.temp");
  });
});
