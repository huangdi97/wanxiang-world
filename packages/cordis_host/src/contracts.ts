import { createHash } from "node:crypto";

import { GENERATED_SERVICE_CONTRACTS } from "./contracts.generated";

/**
 * R7 versioned service contracts as consumed by the composition host.
 *
 * The full contract bodies live once in Python `wanxiang_reality.contracts`.
 * This host consumes a generated namespace/API-version/scope projection, so
 * composition scope cannot drift from the authoritative contract table.
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

const CONTRACTS: readonly ServiceContractRef[] = GENERATED_SERVICE_CONTRACTS;


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
 * Host-local digest of the frozen cross-language seam identity map.
 *
 * The JSON-RPC wire contract intentionally hashes only identity + API version.
 * Scope is generated from the same Python source and used by composition, but
 * it is not part of the frozen history-authority wire digest. This preserves
 * protocol compatibility while still letting CI detect scope drift through the
 * generated projection's clean-tree check and scope-specific tests.
 */
export function seamDigest(): string {
  const payload = CONTRACTS.map((ref) => ({
    id: contractId(ref),
    apiVersion: ref.apiVersion,
  })).sort((left, right) => (left.id < right.id ? -1 : 1));
  return createHash("sha256").update(JSON.stringify(payload)).digest("hex");
}
