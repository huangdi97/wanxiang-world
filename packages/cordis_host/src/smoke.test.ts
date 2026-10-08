import { Context } from "cordis";
import { describe, expect, it } from "vitest";

import { CommitAuthority } from "./authority";
import { HistoryService, MemoryHistoryProvider } from "./history";

/**
 * Wiring smoke test for the Cordis API surface the host depends on.
 *
 * It pins the assumptions the rest of the package builds on: a Service subclass
 * becomes reachable as `ctx[name]`, `ctx.effect` registrations are undone when a
 * plugin is disposed, and `ctx.isolate` keeps world-scoped services apart.
 */
describe("cordis wiring", () => {
  it("exposes services on the context by their registered name", () => {
    const ctx = new Context();
    const history = new HistoryService(ctx, new MemoryHistoryProvider());
    const authority = new CommitAuthority(ctx);

    expect(ctx.get("history")).toBeDefined();
    expect(ctx.get("authority")).toBeDefined();
    expect(history.providerId).toBe("history-memory");
    expect(authority.grantAudit()).toHaveLength(0);
  });

  it("runs an effect and undoes it when the plugin fiber is disposed", async () => {
    const ctx = new Context();
    new HistoryService(ctx, new MemoryHistoryProvider());
    let active = 0;
    let cleaned = 0;
    const plugin = (scope: Context): void => {
      scope.effect(() => {
        active += 1;
        return () => {
          active -= 1;
          cleaned += 1;
        };
      }, "smoke.effect");
    };

    const fiber = await ctx.plugin(plugin);
    expect(active).toBe(1);

    await fiber.dispose();
    expect(cleaned).toBe(1);
    expect(active).toBe(0);
  });

  it("isolates a named service per label", () => {
    const root = new Context();
    const worldA = root.isolate("history", Symbol("world-a"));
    const worldB = root.isolate("history", Symbol("world-b"));
    const historyA = new HistoryService(worldA, new MemoryHistoryProvider());
    const historyB = new HistoryService(worldB, new MemoryHistoryProvider());

    expect(historyA).not.toBe(historyB);
    expect(worldA.get("history")).toBeDefined();
    expect(worldB.get("history")).toBeDefined();
  });
});
