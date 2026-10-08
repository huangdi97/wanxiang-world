import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

import { actorRulePlugin, actorRuleV2Plugin, leakCounters, type ActorRuleConfig } from "./bundle";
import type { CommitOutcome } from "./commit";
import { RevisionConflictError } from "./history";
import { createHost, type WanxiangHost } from "./host";
import { sampleRuntimeLockRef } from "./testing";
import type { ResolvedGraph } from "./graph";

/**
 * Composition spike S1-S5.
 *
 * These scenarios are the acceptance evidence for the Cordis-native composition
 * runtime: commit continuity, plugin-unload continuity, actor-rule replacement,
 * lifecycle leak freedom, and the resolved capability graph.
 */
export interface ScenarioResult {
  readonly scenario: "S1" | "S2" | "S3" | "S4" | "S5";
  readonly status: "PASS" | "FAIL";
  readonly detail: Record<string, unknown>;
}

export interface SpikeReport {
  readonly schema: "wanxiang.r7.composition.spike.v1";
  readonly cordis: { readonly version: string };
  readonly scenarios: readonly ScenarioResult[];
  readonly conclusion: "PASS" | "FAIL";
  readonly graph: ResolvedGraph;
}

export interface SpikeOptions {
  readonly artifactPath?: string;
  readonly lifecycleCycles?: number;
}

const WORLDLINE = "wl_spike_main";
const HOLDER = "world-host";
const RULE_V1 = "actor-rule/actor_alpha/v1";
const RULE_V2 = "actor-rule/actor_alpha/v2";
const RULE_CONFIG: ActorRuleConfig = {
  worldlineId: WORLDLINE,
  actorId: "actor_alpha",
  salt: "spike-salt",
};

interface ProviderWithRebuild {
  rebuildFromHistory?: (worldlineId: string) => string;
}

function commitOnce(host: WanxiangHost, capability: unknown, ruleId: string): CommitOutcome {
  return host.commit({
    worldlineId: WORLDLINE,
    requestingWorldlineId: WORLDLINE,
    requestedBy: HOLDER,
    ruleId,
    capability,
  });
}

async function s1CommitContinuity(host: WanxiangHost, capability: unknown): Promise<ScenarioResult> {
  const runtime = host.openWorld("world_spike", WORLDLINE);
  await host.scopes.load(WORLDLINE, {
    pluginId: RULE_V1,
    requires: ["wanxiang.authority@1", "wanxiang.history@1"],
    apply: actorRulePlugin(RULE_CONFIG),
  });
  let committed = 0;
  for (let index = 0; index < 100; index += 1) {
    if (commitOnce(host, capability, RULE_V1).status === "COMMITTED") committed += 1;
  }
  const head = runtime.history.head(WORLDLINE);
  const provider = runtime.provider as ProviderWithRebuild;
  const rebuildHash = provider.rebuildFromHistory
    ? provider.rebuildFromHistory.call(runtime.provider, WORLDLINE)
    : null;

  let staleConflict = "no-conflict";
  try {
    runtime.history.append(capability as never, {
      worldlineId: WORLDLINE,
      expectedRevision: 1,
      events: [{ eventId: "stale", kind: "stale", payloadDigest: "0" }],
    });
  } catch (error) {
    staleConflict = error instanceof RevisionConflictError ? error.name : `unexpected:${String(error)}`;
  }

  const detail = {
    commits: committed,
    headRevision: head.revision,
    stateHash: head.stateHash,
    rebuildHash,
    rebuildMatches: rebuildHash === head.stateHash,
    staleConflict,
    recordedFibers: runtime.fibers.length,
  };
  const status =
    committed === 100 &&
    head.revision === 100 &&
    detail.rebuildMatches &&
    staleConflict === "RevisionConflictError"
      ? "PASS"
      : "FAIL";
  return { scenario: "S1", status, detail };
}

async function s2UnloadContinuity(host: WanxiangHost): Promise<ScenarioResult> {
  const runtime = host.scopes.runtime(WORLDLINE);
  const fiber = runtime.fibers[0];
  const before = runtime.history.head(WORLDLINE);
  if (fiber) await host.scopes.unload(fiber);
  const after = runtime.history.head(WORLDLINE);
  const rulesAfterUnload = host.authority.rulesFor(WORLDLINE);
  const detail = {
    fiberRecorded: Boolean(fiber),
    headBefore: before,
    headAfter: after,
    headUnchanged: before.revision === after.revision && before.stateHash === after.stateHash,
    rulesAfterUnload,
    leakTimers: leakCounters.timers,
    leakListeners: leakCounters.listeners,
    leakRules: leakCounters.rules,
  };
  const status =
    detail.fiberRecorded &&
    detail.headUnchanged &&
    rulesAfterUnload.length === 0 &&
    leakCounters.timers === 0 &&
    leakCounters.listeners === 0 &&
    leakCounters.rules === 0
      ? "PASS"
      : "FAIL";
  return { scenario: "S2", status, detail };
}

async function s3RuleReplacement(host: WanxiangHost, capability: unknown): Promise<ScenarioResult> {
  const runtime = host.scopes.runtime(WORLDLINE);
  const provider = runtime.provider;
  const before = runtime.history.head(WORLDLINE);
  await host.scopes.load(WORLDLINE, {
    pluginId: RULE_V2,
    requires: ["wanxiang.authority@1", "wanxiang.history@1"],
    apply: actorRuleV2Plugin(RULE_CONFIG),
  });
  const outcome = commitOnce(host, capability, RULE_V2);
  const after = runtime.history.head(WORLDLINE);
  const later = host.scopes.runtime(WORLDLINE);
  const detail = {
    sameProviderInstance: later.provider === provider,
    headBeforeRevision: before.revision,
    headAfterRevision: after.revision,
    continuedFromCurrentRevision: after.revision === before.revision + 1,
    outcome: outcome.status,
    activeRules: host.authority.rulesFor(WORLDLINE),
  };
  const status =
    detail.sameProviderInstance &&
    detail.continuedFromCurrentRevision &&
    detail.outcome === "COMMITTED" &&
    detail.activeRules.length === 1 &&
    detail.activeRules[0] === RULE_V2
      ? "PASS"
      : "FAIL";
  return { scenario: "S3", status, detail };
}

async function s4LifecycleLeak(host: WanxiangHost, cycles: number): Promise<ScenarioResult> {
  // The v2 rule loaded by S3 stays mounted, so the leak check compares against
  // the live baseline instead of assuming an empty runtime.
  const baseline = {
    timers: leakCounters.timers,
    listeners: leakCounters.listeners,
    rules: leakCounters.rules,
    registry: host.root.registry.size,
    registeredRules: host.authority.registeredRuleCount(),
  };
  for (let index = 0; index < cycles; index += 1) {
    const fiber = await host.scopes.load(WORLDLINE, {
      pluginId: `actor-rule/cycle-${index}`,
      requires: ["wanxiang.authority@1"],
      apply: actorRulePlugin({ ...RULE_CONFIG, actorId: `cycle_${index}` }),
    });
    await host.scopes.unload(fiber);
  }
  const after = {
    timers: leakCounters.timers,
    listeners: leakCounters.listeners,
    rules: leakCounters.rules,
    registry: host.root.registry.size,
    registeredRules: host.authority.registeredRuleCount(),
  };
  const detail = {
    cycles,
    baseline,
    after,
    leakedTimers: after.timers - baseline.timers,
    leakedListeners: after.listeners - baseline.listeners,
    leakedRules: after.rules - baseline.rules,
    leakedServices: after.registry - baseline.registry,
    worldlineRules: host.authority.rulesFor(WORLDLINE),
  };
  const status =
    detail.leakedTimers === 0 &&
    detail.leakedListeners === 0 &&
    detail.leakedRules === 0 &&
    detail.leakedServices === 0 &&
    after.registeredRules === baseline.registeredRules
      ? "PASS"
      : "FAIL";
  return { scenario: "S4", status, detail };
}

function s5ResolvedGraph(graph: ResolvedGraph, artifactPath?: string): ScenarioResult {
  let written: string | null = null;
  if (artifactPath) {
    mkdirSync(dirname(artifactPath), { recursive: true });
    writeFileSync(artifactPath, `${JSON.stringify(graph, null, 2)}\n`, "utf-8");
    written = artifactPath;
  }
  const detail = {
    cordisVersion: graph.compositionRuntime.version,
    exact: graph.compositionRuntime.exact,
    contractCount: graph.contracts.length,
    seamDigest: graph.seamDigest,
    providers: graph.providers.length,
    consumers: graph.consumers.length,
    scopes: graph.scopes.length,
    artifactPath: written,
  };
  const status =
    graph.compositionRuntime.name === "cordis" &&
    graph.contracts.length >= 16 &&
    graph.providers.length >= 2 &&
    graph.scopes.length >= 1
      ? "PASS"
      : "FAIL";
  return { scenario: "S5", status, detail };
}

export async function runCompositionSpike(options: SpikeOptions = {}): Promise<SpikeReport> {
  const host = createHost({ lockRef: sampleRuntimeLockRef() });
  const cycles = options.lifecycleCycles ?? 1000;
  const scenarios: ScenarioResult[] = [];
  try {
    host.authority.registerAuthorityHolder(HOLDER, "audit:r7-composition-spike");
    const capability = host.authority.grant(HOLDER);
    scenarios.push(await s1CommitContinuity(host, capability));
    scenarios.push(await s2UnloadContinuity(host));
    scenarios.push(await s3RuleReplacement(host, capability));
    scenarios.push(await s4LifecycleLeak(host, cycles));
    const graph = host.resolvedGraph();
    scenarios.push(s5ResolvedGraph(graph, options.artifactPath));
    return {
      schema: "wanxiang.r7.composition.spike.v1",
      cordis: { version: graph.compositionRuntime.version },
      scenarios,
      conclusion: scenarios.every((item) => item.status === "PASS") ? "PASS" : "FAIL",
      graph,
    };
  } finally {
    await host.dispose();
  }
}
