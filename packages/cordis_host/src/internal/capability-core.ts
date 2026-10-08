/**
 * Capability minting core.
 *
 * This module is deliberately the only place that can turn an object into a
 * usable `CommitCapability`. `src/authority.ts` is its sole non-test importer,
 * and `src/architecture.test.ts` fails the build if any other module imports it,
 * which is the JS-level equivalent of an unforgeable capability handed out by a
 * single trusted bootstrap.
 */
const ISSUED = new WeakSet<object>();

export interface CapabilityRecord {
  readonly holderId: string;
  readonly issuedAtMs: number;
  readonly auditRef: string;
}

export class CapabilityError extends Error {
  override readonly name = "CapabilityError";
}

export class IssuedCapability {
  readonly holderId: string;
  readonly issuedAtMs: number;
  readonly auditRef: string;

  constructor(record: CapabilityRecord) {
    if (!record.holderId) throw new CapabilityError("capability requires a holder");
    this.holderId = record.holderId;
    this.issuedAtMs = record.issuedAtMs;
    this.auditRef = record.auditRef;
    ISSUED.add(this);
  }
}

/** Mint a capability. Only the authority bootstrap may call this. */
export function mintCapability(record: CapabilityRecord): IssuedCapability {
  return new IssuedCapability(record);
}

/**
 * Report whether a value is a capability minted by this module.
 *
 * A structurally identical object created anywhere else is rejected, so a plugin
 * cannot fabricate write access by copying the shape.
 */
export function isIssuedCapability(value: unknown): value is IssuedCapability {
  return typeof value === "object" && value !== null && ISSUED.has(value);
}
