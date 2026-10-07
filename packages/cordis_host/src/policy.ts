/**
 * Policy decision resolution with a monotonic hard-deny guard.
 *
 * Providers may ALLOW, DENY, CONSTRAIN or TRANSFORM a proposal. A HARD_DENY is
 * final: once any provider has established it, a later provider cannot turn the
 * proposal back into an ALLOW, and the resolver reports the conflict instead of
 * letting a plugin quietly re-open a security decision.
 */
export type DecisionKind = "ALLOW" | "DENY" | "CONSTRAIN" | "TRANSFORM" | "HARD_DENY";

export interface PolicyDecision {
  readonly providerId: string;
  readonly kind: DecisionKind;
  readonly reason: string;
}

export type Resolution = "ALLOW" | "DENY";

export class PolicyError extends Error {
  override readonly name = "PolicyError";
}

export interface ResolutionResult {
  readonly resolution: Resolution;
  readonly hardDeniedBy: string | null;
  readonly ignoreAllowAfterHardDeny: readonly string[];
  readonly decisions: readonly PolicyDecision[];
}

export function resolveDecisions(decisions: readonly PolicyDecision[]): ResolutionResult {
  let hardDeniedBy: string | null = null;
  const ignored: string[] = [];
  for (const decision of decisions) {
    if (hardDeniedBy !== null && decision.kind === "ALLOW") {
      // SAFETY: a hard deny is monotonic; an ALLOW that arrives afterwards is
      // recorded for audit but can never flip the resolution back.
      ignored.push(decision.providerId);
    }
    if (decision.kind === "HARD_DENY" && hardDeniedBy === null) {
      hardDeniedBy = decision.providerId;
    }
  }
  const denied = hardDeniedBy !== null || decisions.some((item) => item.kind === "DENY");
  return {
    resolution: denied ? "DENY" : "ALLOW",
    hardDeniedBy,
    ignoreAllowAfterHardDeny: ignored,
    decisions: [...decisions],
  };
}

/** A registered policy provider: it inspects a proposal and returns one decision. */
export interface PolicyProvider {
  readonly providerId: string;
  evaluate(proposal: PolicyProposal): PolicyDecision;
}

export interface PolicyProposal {
  readonly worldlineId: string;
  readonly requestingWorldlineId: string;
  readonly requestedBy: string;
  readonly kind: string;
  readonly rightsApproved?: boolean;
  readonly evidenceRequired?: boolean;
  readonly evidencePresent?: boolean;
  readonly externalEffect?: boolean;
  readonly externalEffectViaOutbox?: boolean;
}

export class PolicyRegistry {
  private readonly providers: PolicyProvider[] = [];

  register(provider: PolicyProvider): () => void {
    this.providers.push(provider);
    return () => {
      const index = this.providers.indexOf(provider);
      if (index >= 0) this.providers.splice(index, 1);
    };
  }

  evaluate(proposal: PolicyProposal): ResolutionResult {
    return resolveDecisions(this.providers.map((provider) => provider.evaluate(proposal)));
  }

  providerIds(): readonly string[] {
    return this.providers.map((provider) => provider.providerId);
  }
}

/** Refuses a write that targets a worldline other than the requester's own. */
export class CrossWorldlineGuard implements PolicyProvider {
  readonly providerId = "policy.cross-worldline-guard";

  evaluate(proposal: PolicyProposal): PolicyDecision {
    const same = proposal.worldlineId === proposal.requestingWorldlineId;
    return {
      providerId: this.providerId,
      kind: same ? "ALLOW" : "HARD_DENY",
      reason: same
        ? "write targets the requesting worldline"
        : `write targets ${proposal.worldlineId} but the requester owns ${proposal.requestingWorldlineId}`,
    };
  }
}

/** Refuses a write that carries no expected revision (unbounded overwrite). */
export class UnversionedWriteGuard implements PolicyProvider {
  readonly providerId = "policy.unversioned-write-guard";

  evaluate(proposal: PolicyProposal): PolicyDecision {
    const versioned = proposal.kind !== "unversioned-overwrite";
    return {
      providerId: this.providerId,
      kind: versioned ? "ALLOW" : "HARD_DENY",
      reason: versioned
        ? "proposal carries an expected revision"
        : "unversioned overwrite of canonical history is never allowed",
    };
  }
}

/** Refuses a write that has an explicit rights/privacy denial. */
export class RightsGuard implements PolicyProvider {
  readonly providerId = "policy.rights-guard";

  evaluate(proposal: PolicyProposal): PolicyDecision {
    const approved = proposal.rightsApproved !== false;
    return {
      providerId: this.providerId,
      kind: approved ? "ALLOW" : "HARD_DENY",
      reason: approved
        ? "no explicit rights/privacy denial"
        : "rights/privacy policy denied the proposal",
    };
  }
}

/** Refuses a write when the caller declares evidence mandatory but supplies none. */
export class EvidenceGuard implements PolicyProvider {
  readonly providerId = "policy.evidence-guard";

  evaluate(proposal: PolicyProposal): PolicyDecision {
    const missing = proposal.evidenceRequired === true && proposal.evidencePresent !== true;
    return {
      providerId: this.providerId,
      kind: missing ? "HARD_DENY" : "ALLOW",
      reason: missing ? "mandatory evidence is missing" : "evidence requirement satisfied",
    };
  }
}

/** Refuses irreversible effects that bypass the durable outbox boundary. */
export class ExternalEffectGuard implements PolicyProvider {
  readonly providerId = "policy.external-effect-guard";

  evaluate(proposal: PolicyProposal): PolicyDecision {
    const bypass = proposal.externalEffect === true && proposal.externalEffectViaOutbox !== true;
    return {
      providerId: this.providerId,
      kind: bypass ? "HARD_DENY" : "ALLOW",
      reason: bypass
        ? "irreversible external effect must be committed through the outbox boundary"
        : "no external-effect boundary violation",
    };
  }
}
