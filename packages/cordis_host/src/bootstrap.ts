import type { ResolvedGraph } from "./graph";
import { createHost, type HostOptions, type WorldlineOpenIdentity } from "./host";
import type { Revision } from "./history";
import type { RuntimeLockRef } from "./lock";

export class BootstrapError extends Error {
  override readonly name = "BootstrapError";
}

export interface BootstrapHistoryExpectation {
  readonly revision: number;
  readonly stateHash: string;
}

export interface WorldBootstrapRequest extends HostOptions {
  readonly worldId: string;
  readonly worldlineId: string;
  readonly identity?: WorldlineOpenIdentity;
  readonly expectedHistoryHead?: BootstrapHistoryExpectation;
}

export interface BootstrappedWorld {
  readonly worldId: string;
  readonly worldlineId: string;
  readonly lockRef: RuntimeLockRef;
  readonly head: Revision;
  resolvedGraph(): ResolvedGraph;
  close(): Promise<void>;
}

/**
 * Fail-closed startup envelope for one canonical worldline.
 *
 * The returned object intentionally exposes no Cordis root Context, raw history
 * provider, Authority, commit capability or commit method. Trusted composition
 * code can still use createHost directly; product/agent entry points should use
 * the bounded WorldHandle / Gateway surfaces.
 */
export async function bootstrapWorld(request: WorldBootstrapRequest): Promise<BootstrappedWorld> {
  const {
    worldId,
    worldlineId,
    identity,
    expectedHistoryHead,
    ...hostOptions
  } = request;
  const host = createHost(hostOptions);
  try {
    const runtime = host.openWorld(worldId, worldlineId, identity);
    const lockRef = host.lockFor(worldlineId);
    if (lockRef === null) {
      throw new BootstrapError("worldline opened without a RuntimeLock");
    }
    if (runtime.ctx.get("history") === undefined) {
      throw new BootstrapError("required history seam is not ready");
    }
    if (host.root.get("authority") === undefined) {
      throw new BootstrapError("required authority seam is not ready");
    }

    const graph = host.resolvedGraph();
    const graphLock = graph.runtimeLocks.find((item) => item.worldlineId === worldlineId);
    if (graphLock === undefined || graphLock.lockDigest !== lockRef.lockDigest) {
      throw new BootstrapError("resolved graph does not bind the opened RuntimeLock");
    }
    const graphContracts = new Set(graph.contracts.map((item) => item.id));
    const missing = Object.keys(lockRef.serviceContractVersions).filter(
      (contractId) => !graphContracts.has(contractId),
    );
    if (missing.length > 0) {
      throw new BootstrapError("required seams missing from resolved graph: " + missing.join(", "));
    }

    const currentHead = runtime.history.head(worldlineId);
    if (currentHead.revision < 0 || typeof currentHead.stateHash !== "string") {
      throw new BootstrapError("history head is invalid");
    }
    if (
      expectedHistoryHead !== undefined &&
      (currentHead.revision !== expectedHistoryHead.revision ||
        currentHead.stateHash !== expectedHistoryHead.stateHash)
    ) {
      throw new BootstrapError(
        "history head mismatch: expected " +
          expectedHistoryHead.revision +
          "/" +
          expectedHistoryHead.stateHash +
          ", got " +
          currentHead.revision +
          "/" +
          currentHead.stateHash,
      );
    }

    return Object.freeze({
      worldId,
      worldlineId,
      lockRef,
      head: currentHead,
      resolvedGraph: (): ResolvedGraph => host.resolvedGraph(),
      close: (): Promise<void> => host.dispose(),
    });
  } catch (error) {
    await host.dispose();
    if (error instanceof BootstrapError) throw error;
    const message = error instanceof Error ? error.message : String(error);
    throw new BootstrapError("world bootstrap failed closed: " + message);
  }
}
