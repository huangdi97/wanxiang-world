/**
 * G12E: Godot / Babylon projection contracts (non-authoritative).
 *
 * Scene/entity transforms, asset refs, animation/state cues, command input and
 * an update protocol are view-model contracts over server projections.
 * Rendered scenes are never canonical truth.
 */

import type { ProjectionSnapshot } from "./projection.js";
import { findEntity, type MapLayout } from "./projection.js";

export interface EntityTransform {
  readonly entityId: string;
  readonly position: readonly [number, number, number];
  readonly rotation: readonly [number, number, number, number];
  readonly assetRef: string;
  readonly animationCue: string;
  readonly stateCue: string;
}

export interface SceneProjection {
  readonly revision: number;
  readonly entities: ReadonlyArray<EntityTransform>;
}

export interface CommandInput {
  readonly sessionId: string;
  readonly branchId: string;
  readonly actionType: string;
  readonly payload: Readonly<Record<string, string | number | boolean | null>>;
}

export interface UpdateProtocol {
  readonly fromRevision: number;
  readonly toRevision: number;
  readonly added: ReadonlyArray<string>;
  readonly removed: ReadonlyArray<string>;
  readonly changed: ReadonlyArray<string>;
}

/** Compose a deterministic scene projection from a server snapshot. */
export function composeScene(
  snapshot: ProjectionSnapshot,
  layout: MapLayout,
): SceneProjection {
  const entities: EntityTransform[] = [];
  let index = 0;
  for (const item of snapshot.items) {
    if (item.redacted) {
      continue;
    }
    const x = layout.originX + index * layout.tile;
    const z = layout.originY + index * layout.tile;
    entities.push({
      entityId: item.entityId,
      position: [x, 0, z],
      rotation: [0, 0, 0, 1],
      assetRef: `asset://${item.entityType}/${item.entityId}`,
      animationCue: "idle",
      stateCue: item.label,
    });
    index += 1;
  }
  return { revision: snapshot.revision, entities };
}

/** Compute an update protocol diff between two scene revisions. */
export function diffScenes(before: SceneProjection, after: SceneProjection): UpdateProtocol {
  const beforeIds = new Set(before.entities.map((e) => e.entityId));
  const afterIds = new Set(after.entities.map((e) => e.entityId));
  const added = [...afterIds].filter((id) => !beforeIds.has(id)).sort();
  const removed = [...beforeIds].filter((id) => !afterIds.has(id)).sort();
  const changed = [...afterIds]
    .filter((id) => beforeIds.has(id))
    .filter((id) => {
      const b = before.entities.find((e) => e.entityId === id);
      const a = after.entities.find((e) => e.entityId === id);
      return b && a && JSON.stringify(b.position) !== JSON.stringify(a.position);
    })
    .sort();
  return { fromRevision: before.revision, toRevision: after.revision, added, removed, changed };
}

/** Validate a command input before submission (client-side shape only). */
export function validateCommandInput(input: CommandInput): boolean {
  return (
    input.sessionId.length > 0 &&
    input.branchId.length > 0 &&
    input.actionType.length > 0
  );
}

export function actorTokenPlace(snapshot: ProjectionSnapshot, actorId: string): string | undefined {
  return findEntity(snapshot, actorId)?.entityId;
}