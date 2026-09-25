import { createHash } from "node:crypto";

import { CommitAuthority, AuthorityError } from "./authority";
import type { IssuedCapability } from "./internal/capability-core";
import { CommitDeniedError, HistoryService, type AppendResult, type Revision } from "./history";
import { PolicyRegistry, type ResolutionResult, type PolicyProposal } from "./policy";

/**
 * An actor rule proposes the next event for a worldline.
 *
 * Rules are proposals only: they cannot append, and the commit path refuses to
 * call one unless the caller already holds a commit capability.
 */
export interface ActorRule {
  readonly ruleId: string;
  readonly ruleVersion: string;
  propose(head: Revision): { readonly kind: string; readonly payloadDigest: string };
}

export interface CommitRequest {
  readonly worldlineId: string;
  readonly requestingWorldlineId: string;
  readonly requestedBy: string;
  readonly ruleId: string;
  readonly capability: unknown;
  readonly kind?: string;
}

export interface CommitOutcome {
  readonly status: "COMMITTED" | "DENIED";
  readonly result: AppendResult | null;
  readonly resolution: ResolutionResult;
  readonly reason: string;
}

export interface CommitDeps {
  readonly authority: CommitAuthority;
  readonly history: HistoryService;
  readonly policy: PolicyRegistry;
}

/** Deterministic payload digest for a proposed event. */
export function proposalDigest(ruleId: string, revision: number, kind: string): string {
  return createHash("sha256")
    .update(`${ruleId}|${revision}|${kind}`)
    .digest("hex");
}

/**
 * The single commit path.
 *
 * Order is fixed: capability check, policy resolution, expected revision from the
 * live head, then append. A denied proposal never reaches the history seam, and a
 * provider ALLOW arriving after a HARD_DENY cannot reopen the decision.
 */
export function commitThroughAuthority(
  deps: CommitDeps,
  request: CommitRequest,
): CommitOutcome {
  if (!deps.authority.accepts(request.capability)) {
    throw new CommitDeniedError(
      `holder ${request.requestedBy} holds no commit capability for ${request.worldlineId}`,
    );
  }
  const rule = deps.authority.rule(request.worldlineId, request.ruleId);
  if (!rule) {
    throw new AuthorityError(`unknown actor rule ${request.ruleId}`);
  }
  const head = deps.history.head(request.worldlineId);
  const proposal: PolicyProposal = {
    worldlineId: request.worldlineId,
    requestingWorldlineId: request.requestingWorldlineId,
    requestedBy: request.requestedBy,
    kind: request.kind ?? "actor-rule",
  };
  const resolution = deps.policy.evaluate(proposal);
  if (resolution.resolution === "DENY") {
    return {
      status: "DENIED",
      result: null,
      resolution,
      reason: resolution.hardDeniedBy
        ? `hard deny from ${resolution.hardDeniedBy}`
        : "policy deny",
    };
  }
  const proposed = rule.propose(head);
  const capability: IssuedCapability = request.capability;
  const result = deps.history.append(capability, {
    worldlineId: request.worldlineId,
    expectedRevision: head.revision,
    events: [
      {
        eventId: `${request.worldlineId}:evt:${head.revision + 1}`,
        kind: proposed.kind,
        payloadDigest: proposed.payloadDigest,
      },
    ],
  });
  return { status: "COMMITTED", result, resolution, reason: "committed" };
}
