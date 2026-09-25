import { Context } from "cordis";

import { CommitAuthority } from "./authority";
import { commitThroughAuthority, type CommitOutcome, type CommitRequest } from "./commit";
import { buildResolvedGraph, type GraphConsumer, type ResolvedGraph } from "./graph";
import { MemoryHistoryProvider, type HistoryProvider } from "./history";
import { CrossWorldlineGuard, PolicyRegistry, UnversionedWriteGuard } from "./policy";
import { WorldScopeManager, type WorldlineRuntime } from "./scopes";

export const AUTHORITY_PROVIDER_VERSION = "1.0.0";

export interface HostOptions {
  readonly providerFactory?: (worldlineId: string) => HistoryProvider;
  readonly authorityProviderVersion?: string;
}

export interface WanxiangHost {
  readonly root: Context;
  readonly authority: CommitAuthority;
  readonly policy: PolicyRegistry;
  readonly scopes: WorldScopeManager;
  readonly authorityProviderVersion: string;
  openWorld(worldId: string, worldlineId: string): WorldlineRuntime;
  commit(request: CommitRequest): CommitOutcome;
  resolvedGraph(): ResolvedGraph;
  dispose(): Promise<void>;
}

/**
 * Build the composition host.
 *
 * The Cordis context carries services, scopes and lifecycle only: no canonical
 * world state is stored in it, and every canonical write goes through the single
 * `commit` path below.
 */
export function createHost(options: HostOptions = {}): WanxiangHost {
  const root = new Context();
  const authority = new CommitAuthority(root);
  const policy = new PolicyRegistry();
  policy.register(new CrossWorldlineGuard());
  policy.register(new UnversionedWriteGuard());
  const factory: (worldlineId: string) => HistoryProvider =
    options.providerFactory ?? (() => new MemoryHistoryProvider());
  const authorityProviderVersion = options.authorityProviderVersion ?? AUTHORITY_PROVIDER_VERSION;
  const scopes = new WorldScopeManager(root, authority, factory);

  return {
    root,
    authority,
    policy,
    scopes,
    authorityProviderVersion,
    openWorld(worldId: string, worldlineId: string): WorldlineRuntime {
      return scopes.openWorldline(worldId, worldlineId);
    },
    commit(request: CommitRequest): CommitOutcome {
      const runtime = scopes.runtime(request.worldlineId);
      return commitThroughAuthority(
        { authority, history: runtime.history, policy },
        request,
      );
    },
    resolvedGraph(): ResolvedGraph {
      const consumers: readonly GraphConsumer[] = [];
      return buildResolvedGraph({
        worldlines: scopes.openWorldlines().map((worldlineId) => {
          const runtime = scopes.runtime(worldlineId);
          return {
            worldId: runtime.worldId,
            worldlineId,
            historyProviderId: runtime.history.providerId,
            historyProviderVersion: runtime.history.providerVersion,
            authorityProviderVersion,
            consumers: [
              ...consumers,
              ...runtime.consumers.map((consumer) => ({ ...consumer, worldlineId })),
            ],
            ctx: runtime.ctx,
          };
        }),
      });
    },
    async dispose(): Promise<void> {
      for (const worldlineId of scopes.openWorldlines()) {
        await scopes.closeWorldline(worldlineId);
      }
      await root.fiber.dispose();
    },
  };
}
