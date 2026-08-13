import { describe, expect, it } from "vitest";

import { createPhaserClient, tokenAtPlace, type MovementCommand } from "./phaser.js";
import type { ProjectionItem, ProjectionSnapshot } from "./projection.js";

const item = (id: string, type: string, fields: ReadonlyArray<readonly [string, string]> = []): ProjectionItem => ({
  entityId: id,
  entityType: type,
  label: "canon",
  redacted: false,
  redactionReason: "",
  fields,
});

const snap = (items: ReadonlyArray<ProjectionItem>): ProjectionSnapshot => ({
  sessionId: "phaser",
  actorId: "alice",
  branchId: "b1",
  mode: "map",
  revision: 5,
  items,
});

describe("phaser client slice", () => {
  it("renders a scene from a server projection (reconnect path)", () => {
    const client = createPhaserClient(() => ({ accepted: true, revision: 5 }));
    const scene = client.render(
      snap([
        item("hall", "spatial.place"),
        item("kitchen", "spatial.place"),
        item("alice", "person", [["spatial.position.place_id", "hall"]]),
      ]),
      { originX: 0, originY: 0, tile: 32 },
    );
    expect(scene.revision).toBe(5);
    expect(scene.tokensByEntity["alice"]).toEqual({ x: 0, y: 0 });
  });

  it("submits movement commands and surfaces rejections", () => {
    const client = createPhaserClient((command: MovementCommand) =>
      command.targetPlaceId === "kitchen"
        ? { accepted: true, revision: 6 }
        : { accepted: false, revision: 5, error: "not_reachable" },
    );
    expect(client.move({ entityId: "alice", targetPlaceId: "kitchen" }).accepted).toBe(true);
    const rejected = client.move({ entityId: "alice", targetPlaceId: "vault" });
    expect(rejected.accepted).toBe(false);
    expect(client.describeRejection(rejected)).toContain("not_reachable");
    expect(client.describeRejection({ accepted: true, revision: 6 })).toContain("revision 6");
  });

  it("finds an actor's token place from projection metadata", () => {
    const snapshot = snap([item("alice", "person", [["spatial.position.place_id", "hall"]])]);
    expect(tokenAtPlace(snapshot, "alice")).toBe("hall");
  });
});