import { describe, expect, it } from "vitest";

import {
  compareBranches,
  createStudioClient,
  entitySummary,
} from "./studio.js";
import type { ProjectionItem, ProjectionSnapshot } from "./projection.js";

const item = (id: string, type: string, label: string): ProjectionItem => ({
  entityId: id,
  entityType: type,
  label,
  redacted: false,
  redactionReason: "",
  fields: [["name", id]],
});

const snap = (items: ReadonlyArray<ProjectionItem>): ProjectionSnapshot => ({
  sessionId: "studio",
  actorId: "alice",
  branchId: "b1",
  mode: "debug",
  revision: 3,
  items,
});

describe("studio client slice", () => {
  it("submits bounded commands through the command API", () => {
    const client = createStudioClient((draft) => ({ accepted: draft.actionType === "spatial.move", revision: 4 }));
    expect(client.submitCommand({ actionType: "spatial.move", payload: {} }).accepted).toBe(true);
    expect(client.submitCommand({ actionType: "evil.inject", payload: {} }).accepted).toBe(false);
  });

  it("diffs branches by presence and label", () => {
    const diff = compareBranches(
      snap([item("a", "spatial.place", "canon"), item("b", "spatial.place", "canon")]),
      snap([item("a", "spatial.place", "source_backed"), item("c", "spatial.place", "canon")]),
    );
    expect(diff.added).toEqual(["c"]);
    expect(diff.removed).toEqual(["b"]);
    expect(diff.changed).toEqual([["a", "canon", "source_backed"]]);
  });

  it("summarizes entities for the inspector", () => {
    expect(entitySummary(item("hall", "spatial.place", "canon"))).toContain("spatial.place");
  });
});