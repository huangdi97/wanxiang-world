/**
 * Studio vertical slice (G05E): world/entity/timeline views + command form.
 *
 * The Studio client consumes server-composed projections and submits bounded
 * commands through the command API. It never treats local state as world
 * truth; validation/conflict errors come from the server and are surfaced.
 * React rendering is a thin consumer of these deterministic view models.
 */

import type { ProjectionItem, ProjectionSnapshot } from "./projection.js";
import { composeStudioView, field } from "./projection.js";

export interface CommandDraft {
  readonly actionType: string;
  readonly payload: Readonly<Record<string, string | number | boolean | null>>;
}

/** Bounded synthetic action set the Studio command form supports. */
export const STUDIO_ACTIONS: ReadonlyArray<string> = [
  "create_entity",
  "transfer_resource",
  "set_status",
  "spatial.move",
];

export interface CommandResult {
  readonly accepted: boolean;
  readonly revision: number;
  readonly error?: string;
}

export interface BranchCompare {
  readonly added: ReadonlyArray<string>;
  readonly removed: ReadonlyArray<string>;
  readonly changed: ReadonlyArray<readonly [string, string, string]>;
}

export interface StudioClient {
  /** Submit a bounded command; server acceptance is authoritative. */
  submitCommand(draft: CommandDraft): CommandResult;
  /** Diff two branch projections (entity presence/label changes). */
  compareBranches(before: ProjectionSnapshot, after: ProjectionSnapshot): BranchCompare;
  /** Renderable entity rows for the inspector. */
  inspectEntities(snapshot: ProjectionSnapshot): ReadonlyArray<ProjectionItem>;
}

export function createStudioClient(submit: (draft: CommandDraft) => CommandResult): StudioClient {
  return {
    submitCommand,
    compareBranches,
    inspectEntities: (snapshot) => composeStudioView(snapshot).entities,
  };

  function submitCommand(draft: CommandDraft): CommandResult {
    if (!STUDIO_ACTIONS.includes(draft.actionType)) {
      return { accepted: false, revision: 0, error: `unsupported action ${draft.actionType}` };
    }
    return submit(draft);
  }
}

export function compareBranches(
  before: ProjectionSnapshot,
  after: ProjectionSnapshot,
): BranchCompare {
  const beforeIds = new Set(before.items.map((item) => item.entityId));
  const afterIds = new Set(after.items.map((item) => item.entityId));
  const added: string[] = [];
  for (const id of afterIds) {
    if (!beforeIds.has(id)) {
      added.push(id);
    }
  }
  const removed: string[] = [];
  for (const id of beforeIds) {
    if (!afterIds.has(id)) {
      removed.push(id);
    }
  }
  const changed: Array<readonly [string, string, string]> = [];
  for (const id of afterIds) {
    if (beforeIds.has(id)) {
      const beforeItem = before.items.find((item) => item.entityId === id);
      const afterItem = after.items.find((item) => item.entityId === id);
      if (beforeItem && afterItem && beforeItem.label !== afterItem.label) {
        changed.push([id, beforeItem.label, afterItem.label]);
      }
    }
  }
  return { added: added.sort(), removed: removed.sort(), changed };
}

export function entitySummary(item: ProjectionItem): string {
  const name = field(item, "name") ?? item.entityId;
  return `${name} (${item.entityType}, ${item.label})`;
}