import { CONTRACT_IDS, getContract } from "./contracts";

/**
 * RuntimeLock reference pinned by a worldline.
 *
 * The authoritative lock is produced by the Python package `wanxiang_reality`
 * (`RuntimeLock.lock_digest`). The composition host consumes it as data so there
 * is exactly one lock model in the repository, and checks that the seams it is
 * about to compose match what the lock pinned. A worldline that runs without a
 * pinned lock is rejected: "reality is versioned, explicit and auditable".
 */
export interface ProfileRef {
  readonly id: string;
  readonly version: string;
  readonly digest: string;
}

export interface RuntimeLockRef {
  readonly lockId: string;
  readonly lockVersion: string;
  readonly lockDigest: string;
  readonly realityProfile: ProfileRef;
  readonly worldProfile: ProfileRef;
  readonly compositionRuntime: { readonly name: string; readonly version: string };
  /** contractId (`namespace@apiVersion`) -> the API version the lock pinned. */
  readonly serviceContractVersions: Readonly<Record<string, string>>;
  readonly providerVersions: Readonly<Record<string, string>>;
  readonly schemaVersions: Readonly<Record<string, string>>;
}

export class RuntimeLockError extends Error {
  override readonly name: string = "RuntimeLockError";
}

const DIGEST = /^[0-9a-f]{64}$/;
const VERSION = /^\d+(\.\d+){0,2}$/;
/** The composition runtime may be pinned at a prerelease, e.g. cordis 4.0.0-rc.10. */
const RUNTIME_VERSION = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/;

function requireText(value: string, field: string): void {
  if (!value) throw new RuntimeLockError(`runtime lock ${field} is required`);
}

function requireVersion(value: string, field: string): void {
  if (!VERSION.test(value)) {
    throw new RuntimeLockError(`runtime lock ${field} is not a version: ${value}`);
  }
}

function requireDigest(value: string, field: string): void {
  if (!DIGEST.test(value)) {
    throw new RuntimeLockError(`runtime lock ${field} is not a sha256 hex digest`);
  }
}

/** Validate a lock reference before a worldline is allowed to open. */
export function validateRuntimeLockRef(ref: RuntimeLockRef): void {
  requireText(ref.lockId, "lockId");
  requireVersion(ref.lockVersion, "lockVersion");
  requireDigest(ref.lockDigest, "lockDigest");
  for (const [name, profile] of [
    ["realityProfile", ref.realityProfile],
    ["worldProfile", ref.worldProfile],
  ] as const) {
    requireText(profile.id, `${name}.id`);
    requireVersion(profile.version, `${name}.version`);
    requireDigest(profile.digest, `${name}.digest`);
  }
  requireText(ref.compositionRuntime.name, "compositionRuntime.name");
  if (!RUNTIME_VERSION.test(ref.compositionRuntime.version)) {
    throw new RuntimeLockError(
      `runtime lock compositionRuntime.version is not a version: ${ref.compositionRuntime.version}`,
    );
  }
  const declared = Object.keys(ref.serviceContractVersions);
  if (declared.length === 0) {
    throw new RuntimeLockError("runtime lock must pin at least one service contract version");
  }
  if (Object.keys(ref.providerVersions).length === 0) {
    throw new RuntimeLockError("runtime lock must pin at least one provider version");
  }
  for (const id of CONTRACT_IDS) {
    if (!(id in ref.serviceContractVersions)) {
      throw new RuntimeLockError(`runtime lock does not pin required seam ${id}`);
    }
  }
  for (const [id, version] of Object.entries(ref.serviceContractVersions)) {
    requireVersion(version, `serviceContractVersions[${id}]`);
    if (getContract(id).apiVersion !== version) {
      throw new RuntimeLockError(
        `runtime lock pins ${id} at ${version} but this host provides ${getContract(id).apiVersion}`,
      );
    }
  }
}

/** Check that the composed seams match exactly what the lock pinned. */
export function assertSeamsMatchLock(
  ref: RuntimeLockRef,
  actualCompositionRuntimeVersion: string,
): void {
  if (ref.compositionRuntime.name !== "cordis") {
    throw new RuntimeLockError(
      `runtime lock expects composition runtime ${ref.compositionRuntime.name}, host provides cordis`,
    );
  }
  if (ref.compositionRuntime.version !== actualCompositionRuntimeVersion) {
    throw new RuntimeLockError(
      `runtime lock pins cordis ${ref.compositionRuntime.version}, host runs ${actualCompositionRuntimeVersion}`,
    );
  }
  for (const id of CONTRACT_IDS) {
    const pinned = ref.serviceContractVersions[id];
    const provided = getContract(id).apiVersion;
    if (pinned !== provided) {
      throw new RuntimeLockError(`seam ${id} drifted: lock ${pinned}, host ${provided}`);
    }
  }
}

export interface RuntimeLockInput {
  readonly lockId: string;
  readonly lockVersion: string;
  readonly lockDigest: string;
  readonly realityProfile: ProfileRef;
  readonly worldProfile: ProfileRef;
  readonly compositionRuntimeVersion: string;
  readonly providerVersions: Readonly<Record<string, string>>;
  readonly schemaVersions?: Readonly<Record<string, string>>;
  readonly serviceContractVersions?: Readonly<Record<string, string>>;
}

/**
 * Build a lock reference for the seams this host composes.
 *
 * The digest still comes from the authority that produced the lock: this helper
 * only fills the seam map for a lock the caller already holds.
 */
export function createRuntimeLockRef(input: RuntimeLockInput): RuntimeLockRef {
  const seams: Record<string, string> = {};
  for (const id of CONTRACT_IDS) {
    seams[id] = input.serviceContractVersions?.[id] ?? getContract(id).apiVersion;
  }
  const ref: RuntimeLockRef = {
    lockId: input.lockId,
    lockVersion: input.lockVersion,
    lockDigest: input.lockDigest,
    realityProfile: input.realityProfile,
    worldProfile: input.worldProfile,
    compositionRuntime: { name: "cordis", version: input.compositionRuntimeVersion },
    serviceContractVersions: seams,
    providerVersions: input.providerVersions,
    schemaVersions: input.schemaVersions ?? {},
  };
  validateRuntimeLockRef(ref);
  return ref;
}
