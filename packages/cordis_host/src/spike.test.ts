import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

import { seamDigest } from "./contracts";
import type { ResolvedGraph } from "./graph";
import { runCompositionSpike } from "./spike";

const ARTIFACT = resolve(
  process.cwd(),
  "..",
  "..",
  "artifacts",
  "r7",
  "composition",
  "resolved_graph.json",
);

describe("R7 composition spike", () => {
  it("passes S1-S5 and writes the resolved capability graph", async () => {
    const report = await runCompositionSpike({ artifactPath: ARTIFACT });

    const failed = report.scenarios.filter((item) => item.status !== "PASS");
    expect(failed, `failing scenarios: ${JSON.stringify(failed)}`).toHaveLength(0);
    expect(report.conclusion).toBe("PASS");

    const stored = JSON.parse(readFileSync(ARTIFACT, "utf-8")) as ResolvedGraph;
    expect(stored.compositionRuntime.name).toBe("cordis");
    expect(stored.compositionRuntime.exact).toBe(true);
    expect(stored.compositionRuntime.version).toBe(report.cordis.version);
    expect(stored.seamDigest).toBe(seamDigest());
    expect(stored.contracts.length).toBeGreaterThanOrEqual(16);
    expect(stored.scopes.length).toBeGreaterThanOrEqual(1);
  });

  it("keeps revision monotonic and rebuildable across the 100-commit run", async () => {
    const report = await runCompositionSpike({ lifecycleCycles: 5 });
    const s1 = report.scenarios.find((item) => item.scenario === "S1");
    expect(s1?.status).toBe("PASS");
    expect(s1?.detail.headRevision).toBe(100);
    expect(s1?.detail.rebuildMatches).toBe(true);
    expect(s1?.detail.staleConflict).toBe("RevisionConflictError");
  });

  it("leaves no timer, listener, service or rule behind after unload", async () => {
    const report = await runCompositionSpike({ lifecycleCycles: 50 });
    const s2 = report.scenarios.find((item) => item.scenario === "S2");
    const s4 = report.scenarios.find((item) => item.scenario === "S4");
    expect(s2?.status).toBe("PASS");
    expect(s4?.status).toBe("PASS");
    expect(s4?.detail.leakedTimers).toBe(0);
    expect(s4?.detail.leakedListeners).toBe(0);
    expect(s4?.detail.leakedRules).toBe(0);
    expect(s4?.detail.leakedServices).toBe(0);
  });

  it("continues the same worldline when the actor rule is replaced", async () => {
    const report = await runCompositionSpike({ lifecycleCycles: 2 });
    const s3 = report.scenarios.find((item) => item.scenario === "S3");
    expect(s3?.status).toBe("PASS");
    expect(s3?.detail.sameProviderInstance).toBe(true);
    expect(s3?.detail.continuedFromCurrentRevision).toBe(true);
    expect(s3?.detail.activeRules).toEqual(["actor-rule/actor_alpha/v2"]);
  });
});
