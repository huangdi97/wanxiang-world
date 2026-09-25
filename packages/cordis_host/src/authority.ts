import { Context, Service } from "cordis";

import type { ActorRule } from "./commit";
import { isIssuedCapability, mintCapability } from "./internal/capability-core";
import type { IssuedCapability } from "./internal/capability-core";

export class AuthorityError extends Error {
  override readonly name = "AuthorityError";
}

export interface AuthorityHolderRecord {

  readonly holderId: string;
  readonly grantedAtMs: number;
  readonly auditRef: string;
}

export interface AuthorityGrant {
  readonly holderId: string;
  readonly capability: IssuedCapability;
  readonly auditRef: string;
}

/**
 * Explicit authority bootstrap.
 *
 * Only holders registered through `registerAuthorityHolder` can be granted a
 * commit capability. Plugins get the authority service so they can ask for a
 * decision, but the grant call rejects every unregistered holder, and no other
 * module can mint a capability (enforced by `src/architecture.test.ts`).
 */
export class CommitAuthority extends Service {
  private readonly holders = new Map<string, AuthorityHolderRecord>();
  private readonly grants: AuthorityGrant[] = [];
  private sequence = 0;

  private readonly worldlineOwners = new Map<string, string>();
  private readonly rules = new Map<string, Map<string, ActorRule>>();

  constructor(ctx: Context) {
    super(ctx, "authority");
  }

  registerAuthorityHolder(holderId: string, auditRef: string): AuthorityHolderRecord {
    if (!holderId) throw new AuthorityError("authority holder requires an id");
    const record: AuthorityHolderRecord = {
      holderId,
      grantedAtMs: Date.now(),
      auditRef,
    };
    this.holders.set(holderId, record);
    return record;
  }

  grant(holderId: string): IssuedCapability {
    const holder = this.holders.get(holderId);
    if (!holder) {
      throw new AuthorityError(`holder ${holderId} is not a registered authority holder`);
    }
    this.sequence += 1;
    const auditRef = `${holder.auditRef}#grant-${this.sequence}`;
    const capability = mintCapability({
      holderId,
      issuedAtMs: Date.now(),
      auditRef,
    });
    this.grants.push({ holderId, capability, auditRef });
    return capability;
  }

  isAuthorityHolder(holderId: string): boolean {
    return this.holders.has(holderId);
  }

  /** Audit trail of every capability ever minted, including revoked holders. */
  grantAudit(): readonly AuthorityGrant[] {
    return [...this.grants];
  }

  /** Report whether a value can actually write canonical history. */
  accepts(value: unknown): value is IssuedCapability {
    return isIssuedCapability(value);

  }
  /** Record which world owns a worldline; used by the cross-worldline guard. */
  bindWorldline(worldlineId: string, worldId: string): void {
    this.worldlineOwners.set(worldlineId, worldId);
  }

  worldlineOwner(worldlineId: string): string | undefined {
    return this.worldlineOwners.get(worldlineId);
  }

  /**
   * Register an actor rule for a worldline.
   *
   * The returned function removes the rule; plugins wrap it in a Cordis effect so
   * unloading the plugin removes its rules with it.
   */
  registerRule(worldlineId: string, rule: ActorRule): () => void {
    const existing = this.rules.get(worldlineId) ?? new Map<string, ActorRule>();
    if (existing.has(rule.ruleId)) {
      throw new AuthorityError(`rule ${rule.ruleId} is already registered for ${worldlineId}`);
    }
    existing.set(rule.ruleId, rule);
    this.rules.set(worldlineId, existing);
    return () => {
      const rules = this.rules.get(worldlineId);
      if (!rules) return;
      rules.delete(rule.ruleId);
      if (rules.size === 0) this.rules.delete(worldlineId);
    };
  }

  rule(worldlineId: string, ruleId: string): ActorRule | undefined {
    return this.rules.get(worldlineId)?.get(ruleId);
  }

  rulesFor(worldlineId: string): readonly string[] {
    return [...(this.rules.get(worldlineId)?.keys() ?? [])].sort();
  }

  registeredRuleCount(): number {
    let total = 0;
    for (const rules of this.rules.values()) total += rules.size;
    return total;
  }
}
