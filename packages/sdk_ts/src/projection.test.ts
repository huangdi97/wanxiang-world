import { describe, expect, it } from "vitest";

import {
  assertProjectionSnapshot,
  composeMapView,
  composeStudioView,
  findEntity,
  isRedacted,
  type ProjectionItem,
  type ProjectionSnapshot,
} from "./projection.js";

const item = (id: string, type: string, redacted = false, fields: ReadonlyArray<readonly [string, string]> = []): ProjectionItem => ({
  entityId: id,
  entityType: type,
  label: "canon",
  redacted,
  redactionReason: redacted ? "sealed_payload" : "",
  fields,
});

const snapshot = (items: ReadonlyArray<ProjectionItem>): ProjectionSnapshot => ({
  sessionId: "s1",
  actorId: "alice",
  branchId: "b1",
  mode: "text",
  revision: 7,
  items,
});

describe("projection view models", () => {
  it("validates server snapshots", () => {
    expect(assertProjectionSnapshot(snapshot([])).revision).toBe(7);
    expect(() => assertProjectionSnapshot({ items: [] })).toThrow("missing required fields");
  });

  it("flags redacted items", () => {
    expect(isRedacted(item("p", "material.info_payload", true))).toBe(true);
    expect(isRedacted(item("p", "material.info_payload", false))).toBe(false);
  });

  it("composes a studio view", () => {
    const view = composeStudioView(snapshot([item("a", "spatial.place"), item("b", "material.info_payload", true)]));
    expect(view.entities).toHaveLength(2);
    expect(view.redactedCount).toBe(1);
    expect(findEntity(snapshot([item("a", "spatial.place")]), "a")?.entityId).toBe("a");
  });

  it("maps semantic places to display coordinates deterministically", () => {
    const snap = snapshot([
      item("hall", "spatial.place"),
      item("kitchen", "spatial.place"),
      item("alice", "person", false, [["spatial.position.place_id", "hall"]]),
    ]);
    const map = composeMapView(snap, { originX: 0, originY: 0, tile: 32 });
    expect(map.places.map((p) => p.entityId)).toEqual(["hall", "kitchen"]);
    expect(map.tokens[0]).toMatchObject({ entityId: "alice", placeId: "hall", x: 0, y: 0 });
  });

  it("omits redacted places from the map", () => {
    const snap = snapshot([item("vault", "spatial.place", true)]);
    const map = composeMapView(snap, { originX: 0, originY: 0, tile: 32 });
    expect(map.places).toHaveLength(0);
  });
});