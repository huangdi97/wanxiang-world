import cordisPackage from "cordis/package.json";

import { CONTRACT_IDS, SERVICE_CONTRACTS, contractId, seamDigest } from "./contracts";
import type { Context } from "cordis";
import type { ProfileRef, RuntimeLockRef } from "./lock";

/**
 * Resolved capability graph export.
 *
 * The graph is the composition runtime's own output: which providers are mounted
 * for which seam, which consumers asked for them, which scope owns them, and the
 * exact runtime versions in play. It deliberately contains no world state.
 */
export interface GraphProvider {
  readonly serviceId: string;
  readonly providerId: string;
  readonly providerVersion: string;
  readonly scope: "root" | "worldline";
  readonly worldlineId: string | null;
}

export interface GraphConsumer {
  readonly consumerId: string;
  readonly worldlineId: string;
  readonly requires: readonly string[];
}

export interface GraphScope {
  readonly scopeId: string;
  readonly worldlineId: string;
  readonly services: readonly string[];
}

export interface ResolvedGraph {
  readonly schema: "wanxiang.r7.composition.resolved-graph.v1";
  readonly compositionRuntime: {
    readonly name: "cordis";
    readonly version: string;
    readonly exact: true;
  };
  readonly runtime: {
    readonly node: string;
  };
  readonly seamDigest: string;
  readonly contracts: readonly {
    readonly id: string;
    readonly apiVersion: string;
    readonly scope: string;
  }[];
  readonly providers: readonly GraphProvider[];
  readonly consumers: readonly GraphConsumer[];
  readonly scopes: readonly GraphScope[];
  /** The lock each worldline pinned; absence is never possible at runtime. */
  readonly runtimeLocks: readonly GraphRuntimeLock[];
}

export interface GraphRuntimeLock {
  readonly worldlineId: string;
  readonly lockId: string;
  readonly lockVersion: string;
  readonly lockDigest: string;
  readonly realityProfile: ProfileRef;
  readonly worldProfile: ProfileRef;
  readonly compositionRuntime: { readonly name: string; readonly version: string };
  readonly serviceContractVersions: Readonly<Record<string, string>>;
  readonly providerVersions: Readonly<Record<string, string>>;
}

export interface GraphInput {
  readonly worldlines: readonly {
    readonly worldId: string;
    readonly worldlineId: string;
    readonly historyProviderId: string;
    readonly historyProviderVersion: string;
    readonly authorityProviderVersion: string;
    readonly lockRef: RuntimeLockRef;
    readonly consumers: readonly GraphConsumer[];
    readonly ctx: Context;
  }[];
}

export function buildResolvedGraph(input: GraphInput): ResolvedGraph {
  const providers: GraphProvider[] = [];
  const consumers: GraphConsumer[] = [];
  const scopes: GraphScope[] = [];
  const runtimeLocks: GraphRuntimeLock[] = [];
  for (const worldline of input.worldlines) {
    providers.push(
      {
        serviceId: "wanxiang.history@1",
        providerId: worldline.historyProviderId,
        providerVersion: worldline.historyProviderVersion,
        scope: "worldline",
        worldlineId: worldline.worldlineId,
      },
      {
        serviceId: "wanxiang.authority@1",
        providerId: "commit-authority",
        providerVersion: worldline.authorityProviderVersion,
        scope: "root",
        worldlineId: null,
      },
    );
    consumers.push(...worldline.consumers);
    scopes.push({
      scopeId: `world:${worldline.worldId}/worldline:${worldline.worldlineId}`,
      worldlineId: worldline.worldlineId,
      services: ["history", "actor"],
    });
    runtimeLocks.push({
      worldlineId: worldline.worldlineId,
      lockId: worldline.lockRef.lockId,
      lockVersion: worldline.lockRef.lockVersion,
      lockDigest: worldline.lockRef.lockDigest,
      realityProfile: worldline.lockRef.realityProfile,
      worldProfile: worldline.lockRef.worldProfile,
      compositionRuntime: worldline.lockRef.compositionRuntime,
      serviceContractVersions: worldline.lockRef.serviceContractVersions,
      providerVersions: worldline.lockRef.providerVersions,
    });
  }
  return {
    schema: "wanxiang.r7.composition.resolved-graph.v1",
    compositionRuntime: {
      name: "cordis",
      version: cordisPackage.version,
      exact: true,
    },
    runtime: { node: process.version },
    seamDigest: seamDigest(),
    contracts: SERVICE_CONTRACTS.map((ref) => ({
      id: contractId(ref),
      apiVersion: ref.apiVersion,
      scope: ref.scope,
    })),
    providers,
    consumers,
    scopes,
    runtimeLocks,
  };
}

export function contractIdList(): readonly string[] {
  return CONTRACT_IDS;
}
