import { describe, expect, it } from "vitest";

import {
  actorTokenPlace,
  composeScene,
  diffScenes,
  validateCommandInput,
} from "./projection3d.js";
import type { ProjectionItem, ProjectionSnapshot } from "./projection.js";

const item = (id: string, type: string, label = "canon", redacted = false): ProjectionItem => ({
  entityId: id,
  entityType: type,
  label,
  redacted,
  redactionReason: redacted ? "sealed" : "",
  fields: [],
});

const snap = (items: ReadonlyArray<ProjectionItem>): ProjectionSnapshot => ({
  sessionId: "s",
  actorId: "alice",
  branchId: "b1",
  mode: "map",
  revision: 3,
  items,
});

describe("G12E projection3d contracts", () => {
  it("composes a deterministic scene projection", () => {
    const scene = composeScene(snap([item("hall", "spatial.place"), item("alice", "person")]), {
      originX: 0,
      originY: 0,
      tile: 32,
    });
    const hall = scene.entities[0];
    const alice = scene.entities[1];
    expect(hall).toBeDefined();
    expect(alice).toBeDefined();
    expect(hall?.position).toEqual([0, 0, 0]);
    expect(alice?.position).toEqual([32, 0, 32]);
    expect(alice?.stateCue).toBe("canon");
  });

  it("omits redacted items from the scene", () => {
    const scene = composeScene(snap([item("vault", "spatial.place", "canon", true)]), {
      originX: 0,
      originY: 0,
      tile: 32,
    });
    expect(scene.entities).toHaveLength(0);
  });

  it("diffs scene revisions for the update protocol", () => {
    const before = composeScene(snap([item("a", "spatial.place")]), { originX: 0, originY: 0, tile: 32 });
    const after = composeScene(
      snap([item("a", "spatial.place"), item("b", "spatial.place")]),
      { originX: 0, originY: 0, tile: 32 },
    );
    const diff = diffScenes(before, after);
    expect(diff.added).toEqual(["b"]);
    expect(diff.fromRevision).toBe(3);
  });

  it("validates command input shape", () => {
    expect(
      validateCommandInput({ sessionId: "s", branchId: "b", actionType: "spatial.move", payload: {} }),
    ).toBe(true);
    expect(validateCommandInput({ sessionId: "", branchId: "b", actionType: "x", payload: {} })).toBe(false);
  });

  it("finds an actor token by id", () => {
    expect(actorTokenPlace(snap([item("alice", "person")]), "alice")).toBe("alice");
  });
});