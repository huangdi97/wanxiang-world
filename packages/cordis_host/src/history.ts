import { createHash } from "node:crypto";
import { Context, Service } from "cordis";

import type { IssuedCapability } from "./internal/capability-core";
import { isIssuedCapability } from "./internal/capability-core";

/** A committed world event, as seen through the history seam. */
export interface WorldEvent {
  readonly eventId: string;
  readonly kind: string;
  readonly payloadDigest: string;
}

/** A worldline revision with the state hash that revision produces. */
export interface Revision {
  readonly revision: number;
  readonly stateHash: string;
}

export interface AppendRequest {
  readonly worldlineId: string;
  readonly expectedRevision: number;
  readonly events: readonly WorldEvent[];
}

export interface AppendResult extends Revision {
  readonly eventIds: readonly string[];
}

export class HistoryError extends Error {
  override readonly name: string = "HistoryError";
}

/**
 * Typed conflict raised when a writer's `expectedRevision` is stale.
 *
 * Thrown instead of silently overwriting: last-write-wins is never accepted for
 * canonical history.
 */
export class RevisionConflictError extends HistoryError {
  override readonly name: string = "RevisionConflictError";

  constructor(
    readonly worldlineId: string,
    readonly expectedRevision: number,
    readonly actualRevision: number,
  ) {
    super(
      `worldline ${worldlineId} is at revision ${actualRevision}, writer expected ${expectedRevision}`,
    );
  }
}

export class CommitDeniedError extends HistoryError {
  override readonly name: string = "CommitDeniedError";
}

/** Replaceable history backend; the python authority implements the same port. */
export interface HistoryProvider {
  readonly providerId: string;
  readonly providerVersion: string;
  head(worldlineId: string): Revision;
  read(worldlineId: string, fromRevision: number): readonly WorldEvent[];
  append(request: AppendRequest): AppendResult;
  checkpoint(worldlineId: string): Revision;
  worldlines(): readonly string[];
}

interface WorldlineState {
  revision: number;
  stateHash: string;
  events: WorldEvent[];
}

/**
 * Fold the state hash one event at a time.
 *
 * INVARIANT: appending events one by one and rebuilding the whole history from
 * the event list must produce the same digest, so replay never depends on how
 * the writes were batched.
 */
function foldStateHash(previous: string, events: readonly WorldEvent[]): string {
  let state = previous;
  for (const event of events) {
    state = createHash("sha256")
      .update(state)
      .update("|")
      .update(event.eventId)
      .update(":")
      .update(event.payloadDigest)
      .digest("hex");
  }
  return state;
}

/**
 * In-process reference provider.
 *
 * It is a real provider (and the one the composition spike certifies), not a
 * stand-in for the python authority: the bridge provider implements the same
 * port over JSON-RPC and both are covered by the same contract tests.
 */
export class MemoryHistoryProvider implements HistoryProvider {
  readonly providerId = "history-memory";
  readonly providerVersion = "1.0.0";

  private readonly worlds = new Map<string, WorldlineState>();

  head(worldlineId: string): Revision {
    const state = this.stateOf(worldlineId);
    return { revision: state.revision, stateHash: state.stateHash };
  }

  read(worldlineId: string, fromRevision: number): readonly WorldEvent[] {
    const state = this.stateOf(worldlineId);
    return state.events.slice(fromRevision);
  }

  append(request: AppendRequest): AppendResult {
    const state = this.stateOf(request.worldlineId);
    if (state.revision !== request.expectedRevision) {
      throw new RevisionConflictError(
        request.worldlineId,
        request.expectedRevision,
        state.revision,
      );
    }
    if (request.events.length === 0) {
      throw new HistoryError("append requires at least one event");
    }
    state.stateHash = foldStateHash(state.stateHash, request.events);
    state.events = [...state.events, ...request.events];
    state.revision += request.events.length;
    return {
      revision: state.revision,
      stateHash: state.stateHash,
      eventIds: request.events.map((event) => event.eventId),
    };
  }

  checkpoint(worldlineId: string): Revision {
    return this.head(worldlineId);
  }

  worldlines(): readonly string[] {
    return [...this.worlds.keys()].sort();
  }

  /** Rebuild the state hash from the recorded events only (snapshot-free replay). */
  rebuildFromHistory(worldlineId: string): string {
    return foldStateHash("", this.stateOf(worldlineId).events);
  }

  private stateOf(worldlineId: string): WorldlineState {
    const existing = this.worlds.get(worldlineId);
    if (existing) return existing;
    const created: WorldlineState = { revision: 0, stateHash: "", events: [] };
    this.worlds.set(worldlineId, created);
    return created;
  }
}

/**
 * The history seam as a Cordis service.
 *
 * `append` is the only mutating method and it demands a commit capability that
 * the authority minted. A plugin that holds no capability can observe, read and
 * checkpoint, but never write canonical history.
 */
export class HistoryService extends Service {
  readonly providerId: string;
  readonly providerVersion: string;

  constructor(
    ctx: Context,
    private readonly provider: HistoryProvider,
  ) {
    super(ctx, "history");
    this.providerId = provider.providerId;
    this.providerVersion = provider.providerVersion;
  }

  head(worldlineId: string): Revision {
    return this.provider.head(worldlineId);
  }

  read(worldlineId: string, fromRevision: number): readonly WorldEvent[] {
    return this.provider.read(worldlineId, fromRevision);
  }

  checkpoint(worldlineId: string): Revision {
    return this.provider.checkpoint(worldlineId);
  }

  worldlines(): readonly string[] {
    return this.provider.worldlines();
  }

  append(capability: IssuedCapability, request: AppendRequest): AppendResult {
    if (!isIssuedCapability(capability)) {
      // SAFETY: the capability check happens before any provider call, so an
      // unauthenticated writer can never reach the canonical append path.
      throw new CommitDeniedError(
        "canonical append requires a commit capability issued by the authority",
      );
    }
    return this.provider.append(request);
  }
}
