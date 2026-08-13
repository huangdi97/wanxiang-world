/**
 * Wanxiang projection contracts + server-composed view models.
 *
 * Projections are DTOs composed server-side; clients never treat local state
 * as canonical truth. Rendering layers (React Studio / Phaser canvas) consume
 * these view models, which stay deterministic and browser-free.
 */

export type ProjectionMode = "text" | "map" | "debug";

export interface ProjectionRequest {
  readonly sessionId: string;
  readonly actorId: string;
  readonly branchId: string;
  readonly mode: ProjectionMode;
}

export interface ProjectionItem {
  readonly entityId: string;
  readonly entityType: string;
  readonly label: string;
  readonly redacted: boolean;
  readonly redactionReason: string;
  readonly fields: ReadonlyArray<readonly [string, string]>;
}

export interface ProjectionSnapshot {
  readonly sessionId: string;
  readonly actorId: string;
  readonly branchId: string;
  readonly mode: ProjectionMode;
  readonly revision: number;
  readonly items: ReadonlyArray<ProjectionItem>;
}

/** Validate a server snapshot; malformed snapshots fail loudly. */
export function assertProjectionSnapshot(value: unknown): ProjectionSnapshot {
  if (typeof value !== "object" || value === null) {
    throw new Error("projection snapshot must be an object");
  }
  const snapshot = value as Record<string, unknown>;
  if (
    typeof snapshot.sessionId !== "string" ||
    typeof snapshot.actorId !== "string" ||
    typeof snapshot.branchId !== "string" ||
    typeof snapshot.revision !== "number" ||
    !Array.isArray(snapshot.items)
  ) {
    throw new Error("projection snapshot is missing required fields");
  }
  return snapshot as unknown as ProjectionSnapshot;
}

/** True if the client should render a redacted placeholder. */
export function isRedacted(item: ProjectionItem): boolean {
  return item.redacted;
}

/** Field lookup helper (server-filtered fields only). */
export function field(item: ProjectionItem, key: string): string | undefined {
  for (const [fieldKey, value] of item.fields) {
    if (fieldKey === key) {
      return value;
    }
  }
  return undefined;
}

export function findEntity(snapshot: ProjectionSnapshot, entityId: string): ProjectionItem | undefined {
  return snapshot.items.find((item) => item.entityId === entityId);
}

export interface StudioView {
  readonly revision: number;
  readonly entities: ReadonlyArray<ProjectionItem>;
  readonly redactedCount: number;
}

/** Studio entity-inspector / timeline view model (pure). */
export function composeStudioView(snapshot: ProjectionSnapshot): StudioView {
  const entities = [...snapshot.items].sort((a, b) => a.entityId.localeCompare(b.entityId));
  return {
    revision: snapshot.revision,
    entities,
    redactedCount: entities.filter((item) => item.redacted).length,
  };
}

export interface MapLayout {
  readonly originX: number;
  readonly originY: number;
  readonly tile: number;
}

export interface MapPlace {
  readonly entityId: string;
  readonly x: number;
  readonly y: number;
}

export interface ActorToken {
  readonly entityId: string;
  readonly placeId: string;
  readonly x: number;
  readonly y: number;
}

export interface MapView {
  readonly revision: number;
  readonly places: ReadonlyArray<MapPlace>;
  readonly tokens: ReadonlyArray<ActorToken>;
}

/**
 * Map projection: map semantic places/portals to display coordinates via
 * projection metadata only. Rendered coordinates never become canonical
 * topology (server projection is authoritative).
 */
export function composeMapView(snapshot: ProjectionSnapshot, layout: MapLayout): MapView {
  const places: MapPlace[] = [];
  const placeIds = new Set<string>();
  for (const item of snapshot.items) {
    if (item.entityType === "spatial.place" && !item.redacted) {
      const index = places.length;
      const x = layout.originX + index * layout.tile;
      const y = layout.originY + (index % 2) * layout.tile;
      places.push({ entityId: item.entityId, x, y });
      placeIds.add(item.entityId);
    }
  }
  const tokens: ActorToken[] = [];
  for (const item of snapshot.items) {
    if (item.entityType === "person" && !item.redacted) {
      const placeId = field(item, "spatial.position.place_id") ?? field(item, "place_id");
      const place = placeIds.has(placeId ?? "") ? places.find((p) => p.entityId === placeId) : undefined;
      if (place) {
        tokens.push({ entityId: item.entityId, placeId: place.entityId, x: place.x, y: place.y });
      }
    }
  }
  return { revision: snapshot.revision, places, tokens };
}