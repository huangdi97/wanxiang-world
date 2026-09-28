import cordisPackage from "cordis/package.json";
import { Context } from "cordis";

import { CommitAuthority } from "./authority";
import { commitThroughAuthority, type CommitOutcome, type CommitRequest } from "./commit";
import { buildResolvedGraph, type GraphConsumer, type ResolvedGraph } from "./graph";
import { MemoryHistoryProvider, type HistoryProvider } from "./history";
import {
  assertSeamsMatchLock,
  validateRuntimeLockRef,
  RuntimeLockError,
  type RuntimeLockRef,
} from "./lock";
import { CrossWorldlineGuard, PolicyRegistry, UnversionedWriteGuard } from "./policy";
import { WorldScopeManager, type WorldlineRuntime } from "./scopes";
import {
  assertProvidersMatchLock,
  assertStoredLockMatchesWorldline,
  RuntimeLockMissingError,
  toRuntimeLockRef,
  type LockSource,
} from "./stored_lock";

export const AUTHORITY_PROVIDER_VERSION = "1.0.0";

/** The world-definition identity a caller claims when it opens a worldline. */
export interface WorldlineOpenIdentity {
  readonly worldDefinitionVersion: string;
  readonly worldInstanceId: string;
}

export interface HostOptions {
  /**
   * The lock every worldline of this host is pinned to, for a host that holds one
   * already. Exactly one of `lockRef` / `lockSource` is required: a host that
   * cannot state which reality semantics, seams and provider versions it runs is
   * not allowed to open a worldline.
   */
  readonly lockRef?: RuntimeLockRef;
  /**
   * A source of persisted per-worldline locks (the files the Python
   * `FileLockStore` writes). Preferred over `lockRef`: every worldline is checked
   * against its own pinned lock, and a missing/tampered/drifted lock refuses to
   * open that worldline.
   */
  readonly lockSource?: LockSource;
  /** Providers this host actually runs, compared with the pinned set. */
  readonly providerVersions?: Readonly<Record<string, string>>;
  /** Schema versions this host actually runs, compared with the pinned set. */
  readonly schemaVersions?: Readonly<Record<string, string>>;
  readonly providerFactory?: (worldlineId: string) => HistoryProvider;
  readonly authorityProviderVersion?: string;
}

export interface WanxiangHost {
  readonly root: Context;
  readonly authority: CommitAuthority;
  readonly policy: PolicyRegistry;
  readonly scopes: WorldScopeManager;
  /** Present only for a host pinned through a single lock reference. */
  readonly lockRef: RuntimeLockRef | null;
  readonly authorityProviderVersion: string;
  openWorld(worldId: string, worldlineId: string, identity?: WorldlineOpenIdentity): WorldlineRuntime;
  /** The lock an *open* worldline is pinned to, or null when it is not open. */
  lockFor(worldlineId: string): RuntimeLockRef | null;
  commit(request: CommitRequest): CommitOutcome;
  resolvedGraph(): ResolvedGraph;
  dispose(): Promise<void>;
}

function defaultProviderVersions(): Readonly<Record<string, string>> {
  // A throwaway instance is deliberate: the pinned provider version must be read
  // from the provider itself so a bump cannot drift from the lock silently.
  return {
    [new MemoryHistoryProvider().providerId]: new MemoryHistoryProvider().providerVersion,
    "commit-authority": AUTHORITY_PROVIDER_VERSION,
  };
}

/**
 * Build the composition host.
 *
 * The Cordis context carries services, scopes and lifecycle only: no canonical
 * world state is stored in it, and every canonical write goes through the single
 * `commit` path below. Opening a worldline is fail-closed: the lock is resolved,
 * its digest re-verified, its identity compared with the worldline being opened,
 * and its provider/schema/contract versions compared with what this host runs
 * before any worldline state exists.
 */
export function createHost(options: HostOptions): WanxiangHost {
  const singleLock = options.lockRef;
  const lockSource = options.lockSource;
  if ((singleLock === undefined) === (lockSource === undefined)) {
    throw new RuntimeLockError("createHost requires exactly one of lockRef or lockSource");
  }
  if (singleLock !== undefined) {
    validateRuntimeLockRef(singleLock);
    assertSeamsMatchLock(singleLock, cordisPackage.version);
  }

  const providerVersions = options.providerVersions ?? defaultProviderVersions();
  const schemaVersions = options.schemaVersions ?? {};
  const root = new Context();
  const authority = new CommitAuthority(root);
  const policy = new PolicyRegistry();
  policy.register(new CrossWorldlineGuard());
  policy.register(new UnversionedWriteGuard());
  const factory: (worldlineId: string) => HistoryProvider =
    options.providerFactory ?? (() => new MemoryHistoryProvider());
  const authorityProviderVersion = options.authorityProviderVersion ?? AUTHORITY_PROVIDER_VERSION;
  const scopes = new WorldScopeManager(root, authority, factory);

  const resolveLock = (
    worldId: string,
    worldlineId: string,
    identity: WorldlineOpenIdentity | undefined,
  ): RuntimeLockRef => {
    if (lockSource === undefined) {
      return singleLock as RuntimeLockRef;
    }
    if (identity === undefined) {
      throw new RuntimeLockError(
        `opening ${worldlineId} from a lock source requires its world definition version and instance id`,
      );
    }
    const stored = lockSource.read(worldlineId);
    if (stored === null) {
      throw new RuntimeLockMissingError(`worldline ${worldlineId} has no persisted runtime lock`);
    }
    assertStoredLockMatchesWorldline(stored, {
      worldId,
      worldlineId,
      worldDefinitionVersion: identity.worldDefinitionVersion,
      worldInstanceId: identity.worldInstanceId,
    });
    assertProvidersMatchLock(stored, { providerVersions, schemaVersions });
    const ref = toRuntimeLockRef(stored);
    validateRuntimeLockRef(ref);
    assertSeamsMatchLock(ref, cordisPackage.version);
    return ref;
  };

  return {
    root,
    authority,
    policy,
    scopes,
    lockRef: singleLock ?? null,
    authorityProviderVersion,
    openWorld(worldId: string, worldlineId: string, identity?: WorldlineOpenIdentity): WorldlineRuntime {
      return scopes.openWorldline(worldId, worldlineId, resolveLock(worldId, worldlineId, identity));
    },
    lockFor(worldlineId: string): RuntimeLockRef | null {
      if (!scopes.openWorldlines().includes(worldlineId)) return null;
      return scopes.runtime(worldlineId).lockRef;
    },
    commit(request: CommitRequest): CommitOutcome {
      const runtime = scopes.runtime(request.worldlineId);
      return commitThroughAuthority({ authority, history: runtime.history, policy }, request);
    },
    resolvedGraph(): ResolvedGraph {
      const sharedConsumers: readonly GraphConsumer[] = [];
      return buildResolvedGraph({
        worldlines: scopes.openWorldlines().map((worldlineId) => {
          const runtime = scopes.runtime(worldlineId);
          return {
            worldId: runtime.worldId,
            worldlineId,
            lockRef: runtime.lockRef,
            historyProviderId: runtime.history.providerId,
            historyProviderVersion: runtime.history.providerVersion,
            authorityProviderVersion,
            consumers: [
              ...sharedConsumers,
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
