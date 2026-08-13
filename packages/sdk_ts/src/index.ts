/**
 * Wanxiang TypeScript SDK baseline.
 *
 * This module intentionally carries no world behavior; it establishes the
 * strict typed-client foundation that later projection/API code will build on.
 */

export const SDK_VERSION = "0.1.0";

/** Stable reference to a world instance and branch (identity only). */
export interface WorldRef {
  readonly instanceId: string;
  readonly branchId: string;
}

/** Build a validated {@link WorldRef}. */
export function makeWorldRef(instanceId: string, branchId: string): WorldRef {
  if (instanceId.length === 0 || branchId.length === 0) {
    throw new Error("instanceId and branchId must be non-empty");
  }
  return { instanceId, branchId };
}

export * from "./projection.js";
export * from "./studio.js";
export * from "./phaser.js";