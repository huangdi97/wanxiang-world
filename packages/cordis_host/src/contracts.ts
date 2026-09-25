import { createHash } from "node:crypto";

/**
 * R7 versioned service contracts as consumed by the composition host.
 *
 * Only the identity-bearing part of each contract is duplicated here (namespace,
 * API version, scope). The full contract bodies live once, in the Python package
 * `wanxiang_reality.contracts`; the host verifies that its seam versions match
 * the RuntimeLock a worldline pinned, so the two sides cannot drift silently.
 */
export type ContractScope = "root" | "tenant" | "world" | "worldline";

export interface ServiceContractRef {
  readonly namespace: string;
  readonly apiVersion: string;
  readonly scope: ContractScope;
}

export class ContractError extends Error {
  override readonly name = "ContractError";
}

const CONTRACTS: readonly ServiceContractRef[] = [
  { namespace: "wanxiang.identity", apiVersion: "1", scope: "tenant" },
  { namespace: "wanxiang.reality.observe", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.reality.proposal", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.reality.policy", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.authority", apiVersion: "1", scope: "root" },
  { namespace: "wanxiang.history", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.branch", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.lineage", apiVersion: "1", scope: "world" },
  { namespace: "wanxiang.replay", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.evidence", apiVersion: "1", scope: "world" },
  { namespace: "wanxiang.rights", apiVersion: "1", scope: "world" },
  { namespace: "wanxiang.execution", apiVersion: "1", scope: "root" },
  { namespace: "wanxiang.actor", apiVersion: "1", scope: "worldline" },
  { namespace: "wanxiang.model", apiVersion: "1", scope: "root" },
  { namespace: "wanxiang.capability", apiVersion: "1", scope: "world" },
  { namespace: "wanxiang.reality.profile", apiVersion: "1", scope: "world" },
];

export const SERVICE_CONTRACTS: readonly ServiceContractRef[] = CONTRACTS;

/** Canonical `namespace@apiVersion` identifier for a contract. */
export function contractId(ref: ServiceContractRef): string {
  return `${ref.namespace}@${ref.apiVersion}`;
}

export const CONTRACT_IDS: readonly string[] = CONTRACTS.map(contractId);

export function getContract(id: string): ServiceContractRef {
  const found = CONTRACTS.find((ref) => contractId(ref) === id);
  if (!found) throw new ContractError(`unknown service contract: ${id}`);
  return found;
}

/**
 * Digest of the seam identity map (id -> apiVersion).
 *
 * The Python side computes the same digest over its contract table, so a
 * divergence between the two language runtimes is detectable instead of being
 * assumed away.
 */
export function seamDigest(): string {
  const payload = CONTRACTS.map((ref) => ({
    id: contractId(ref),
    apiVersion: ref.apiVersion,
  })).sort((left, right) => (left.id < right.id ? -1 : 1));
  return createHash("sha256").update(JSON.stringify(payload)).digest("hex");
}
