import { Context, type Fiber } from "cordis";

import { CommitAuthority } from "./authority";
import { HistoryService, MemoryHistoryProvider, type HistoryProvider } from "./history";

/** A plugin mounted into a worldline scope, as reported in the resolved graph. */
export interface PluginLoad {
  readonly pluginId: string;
  readonly requires: readonly string[];
  readonly apply: (ctx: Context) => void;
}

export interface GraphConsumerRecord {
  readonly consumerId: string;
  readonly requires: readonly string[];
}

/**
 * World / worldline scopes over one Cordis root context.
 *
 * A worldline owns isolated instances of the worldline-scoped seams (`history`,
 * `actor`), so unloading one worldline cannot touch another. The authority stays
 * at the root: there is exactly one commit bootstrap, and a worldline writes only
 * through a capability it was granted.
 */
export interface WorldlineRuntime {
  readonly worldId: string;
  readonly worldlineId: string;
  readonly ctx: Context;
  readonly history: HistoryService;
  readonly provider: HistoryProvider;
  readonly fibers: Fiber[];
  readonly consumers: GraphConsumerRecord[];
}

export class ScopeError extends Error {
  override readonly name = "ScopeError";
}

export class WorldScopeManager {
  private readonly worldlines = new Map<string, WorldlineRuntime>();
  /** Providers of unloaded worldlines: committed history outlives its runtime. */
  private readonly retained = new Map<string, HistoryProvider>();

  constructor(
    private readonly root: Context,
    private readonly authority: CommitAuthority,
    private readonly providerFactory: (worldlineId: string) => HistoryProvider = () =>
      new MemoryHistoryProvider(),
  ) {}

  openWorldline(worldId: string, worldlineId: string): WorldlineRuntime {
    const existing = this.worldlines.get(worldlineId);
    if (existing) return existing;
    const ctx = this.root
      .isolate("history", Symbol(worldlineId))
      .isolate("actor", Symbol(worldlineId));
    const provider = this.retained.get(worldlineId) ?? this.providerFactory(worldlineId);
    const history = new HistoryService(ctx, provider);
    const runtime: WorldlineRuntime = {
      worldId,
      worldlineId,
      ctx,
      history,
      provider,
      fibers: [],
      consumers: [],
    };
    this.authority.bindWorldline(worldlineId, worldId);
    this.worldlines.set(worldlineId, runtime);
    return runtime;
  }

  runtime(worldlineId: string): WorldlineRuntime {
    const found = this.worldlines.get(worldlineId);
    if (!found) throw new ScopeError(`worldline ${worldlineId} is not open`);
    return found;
  }

  isOpen(worldlineId: string): boolean {
    return this.worldlines.has(worldlineId);
  }

  /** Load a plugin into a worldline scope and record its fiber for cleanup. */
  async load(worldlineId: string, load: PluginLoad): Promise<Fiber> {
    const runtime = this.runtime(worldlineId);
    const fiber = await runtime.ctx.plugin(load.apply);
    runtime.fibers.push(fiber);
    runtime.consumers.push({
      consumerId: load.pluginId,
      requires: [...load.requires],
    });
    return fiber;
  }

  /** Unload a single plugin; its effects are undone, committed history is not. */
  async unload(fiber: Fiber): Promise<void> {
    await fiber.dispose();
  }

  /**
   * Unload a worldline runtime.
   *
   * Only the worldline's own plugin fibers are disposed. Cordis `isolate()`
   * derives a child context that shares the parent fiber, so disposing
   * `runtime.ctx.fiber` would tear down the whole runtime — including every
   * other world — which the world-isolation test caught. Committed history is
   * retained in the provider, so it stays readable and replayable afterwards.
   */
  async closeWorldline(worldlineId: string): Promise<void> {
    const runtime = this.worldlines.get(worldlineId);
    if (!runtime) return;
    for (const fiber of [...runtime.fibers]) {
      await fiber.dispose();
    }
    this.retained.set(worldlineId, runtime.provider);
    this.worldlines.delete(worldlineId);
  }

  openWorldlines(): readonly string[] {
    return [...this.worldlines.keys()].sort();
  }

  /** History provider of a closed worldline, retained after its runtime unloads. */
  retainedProvider(worldlineId: string): HistoryProvider | undefined {
    return this.worldlines.get(worldlineId)?.provider ?? this.retained.get(worldlineId);
  }
}
