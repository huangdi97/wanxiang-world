/**
 * Phaser 2D player vertical slice (G05F): map projection + movement commands.
 *
 * The Phaser scene is fed by the server projection API. Semantic places are
 * mapped to display coordinates via projection metadata only; rendered
 * coordinates never become canonical topology. Reconnect reconstructs the view
 * from a fresh server projection.
 */

import type { ProjectionSnapshot } from "./projection.js";
import { composeMapView, findEntity, type MapLayout, type MapView } from "./projection.js";

export interface MovementCommand {
  readonly entityId: string;
  readonly targetPlaceId: string;
}

export interface PlayerCommandResult {
  readonly accepted: boolean;
  readonly revision: number;
  readonly error?: string;
}

export interface PhaserSceneState {
  readonly revision: number;
  readonly map: MapView;
  readonly tokensByEntity: Readonly<Record<string, { x: number; y: number }>>;
}

export interface PhaserClient {
  /** Render a server projection into scene state (reconnect path). */
  render(snapshot: ProjectionSnapshot, layout: MapLayout): PhaserSceneState;
  /** Submit a movement command through the generated client. */
  move(command: MovementCommand): PlayerCommandResult;
  /** Surface server-rejected actions with branch/session context. */
  describeRejection(result: PlayerCommandResult): string;
}

export function createPhaserClient(
  submit: (command: MovementCommand) => PlayerCommandResult,
): PhaserClient {
  return {
    render(snapshot, layout) {
      const map = composeMapView(snapshot, layout);
      const tokensByEntity: Record<string, { x: number; y: number }> = {};
      for (const token of map.tokens) {
        tokensByEntity[token.entityId] = { x: token.x, y: token.y };
      }
      return { revision: snapshot.revision, map, tokensByEntity };
    },
    move,
    describeRejection(result) {
      if (result.accepted) {
        return `committed at revision ${result.revision}`;
      }
      return `rejected: ${result.error ?? "unknown"} (revision ${result.revision})`;
    },
  };

  function move(command: MovementCommand): PlayerCommandResult {
    if (command.entityId.length === 0 || command.targetPlaceId.length === 0) {
      return { accepted: false, revision: 0, error: "movement requires entity and target" };
    }
    return submit(command);
  }
}

export function tokenAtPlace(snapshot: ProjectionSnapshot, actorId: string): string | undefined {
  const item = findEntity(snapshot, actorId);
  if (!item || item.redacted) {
    return undefined;
  }
  for (const [key, value] of item.fields) {
    if (key.endsWith(".place_id")) {
      return value;
    }
  }
  return undefined;
}