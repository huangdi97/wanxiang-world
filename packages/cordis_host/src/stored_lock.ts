import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";

import { RuntimeLockError, type RuntimeLockRef } from "./lock";

/**
 * Persisted runtime-lock record.
 *
 * The authoritative lock is written by the Python package `wanxiang_reality`
 * (`FileLockStore`, schema `wanxiang.r7.runtime-lock.v1`). This module is the
 * read side: it decodes that exact file, recomputes the digest over the same
 * canonical JSON the writer used, and refuses anything else. A worldline whose
 * lock is missing, tampered, or bound to another identity must not open.
 */
export const LOCK_STORE_SCHEMA = "wanxiang.r7.runtime-lock.v1";

export interface RuntimeLockProjection {
  readonly world_id: string;
  readonly world_definition_version: string;
  readonly world_instance_id: string;
  readonly worldline_id: string;
  readonly reality_profile_ref: string;
  readonly reality_profile_hash: string;
  readonly world_profile_ref: string;
  readonly world_profile_hash: string;
  readonly composition_runtime: string;
  readonly composition_runtime_version: string;
  readonly service_contract_versions: Readonly<Record<string, string>>;
  readonly provider_versions: Readonly<Record<string, string>>;
  readonly artifact_hashes: Readonly<Record<string, string>>;
  readonly schema_versions: Readonly<Record<string, string>>;
  readonly migration_lineage: readonly string[];
  readonly runtime_config_hash: string;
}

const PROJECTION_KEYS: readonly (keyof RuntimeLockProjection)[] = [
  "world_id",
  "world_definition_version",
  "world_instance_id",
  "worldline_id",
  "reality_profile_ref",
  "reality_profile_hash",
  "world_profile_ref",
  "world_profile_hash",
  "composition_runtime",
  "composition_runtime_version",
  "service_contract_versions",
  "provider_versions",
  "artifact_hashes",
  "schema_versions",
  "migration_lineage",
  "runtime_config_hash",
];

export interface StoredRuntimeLock {
  readonly worldlineId: string;
  readonly revision: number;
  readonly writtenAt: string;
  readonly lockDigest: string;
  readonly lock: RuntimeLockProjection;
}

export class RuntimeLockMissingError extends RuntimeLockError {
  override readonly name: string = "RuntimeLockMissingError";
}

export class RuntimeLockTamperedError extends RuntimeLockError {
  override readonly name: string = "RuntimeLockTamperedError";
}

/**
 * Canonical JSON: sorted object keys, compact separators, UTF-8.
 *
 * COMPATIBILITY:
 * This must stay byte-identical to `wanxiang_reality.hashing.canonical_digest`
 * (`json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`),
 * because the digest is the value that pins a worldline. All keys and values in a
 * lock are ASCII, so Python's code-point ordering and this comparison agree.
 */
export function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) {
    return `[${value.map((item) => canonicalJson(item)).join(",")}]`;
  }
  if (value !== null && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>).sort((left, right) =>
      left[0] < right[0] ? -1 : left[0] > right[0] ? 1 : 0,
    );
    const body = entries
      .map(([key, item]) => `${JSON.stringify(key)}:${canonicalJson(item)}`)
      .join(",");
    return `{${body}}`;
  }
  return JSON.stringify(value);
}

/** The canonical digest of a lock projection (same value `RuntimeLock.lock_digest()` returns). */
export function lockProjectionDigest(projection: RuntimeLockProjection): string {
  return createHash("sha256").update(canonicalJson(projection), "utf-8").digest("hex");
}

const DIGEST = /^[0-9a-f]{64}$/;

function asObject(value: unknown, what: string): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new RuntimeLockTamperedError(`${what} must be a JSON object`);
  }
  return value as Record<string, unknown>;
}

function requireText(fields: Record<string, unknown>, key: string, what: string): string {
  const value = fields[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new RuntimeLockTamperedError(`${what}.${key} must be a non-empty string`);
  }
  return value;
}

function requireVersionMap(fields: Record<string, unknown>, key: string, what: string): Record<string, string> {
  const raw = asObject(fields[key], `${what}.${key}`);
  const result: Record<string, string> = {};
  for (const [name, version] of Object.entries(raw)) {
    if (typeof version !== "string" || version.length === 0) {
      throw new RuntimeLockTamperedError(`${what}.${key}[${name}] must be a non-empty string`);
    }
    result[name] = version;
  }
  return result;
}

function requireStringList(fields: Record<string, unknown>, key: string, what: string): string[] {
  const raw = fields[key];
  if (!Array.isArray(raw)) {
    throw new RuntimeLockTamperedError(`${what}.${key} must be an array`);
  }
  return raw.map((item) => {
    if (typeof item !== "string") {
      throw new RuntimeLockTamperedError(`${what}.${key} must contain only strings`);
    }
    return item;
  });
}

function decodeProjection(raw: unknown): RuntimeLockProjection {
  const fields = asObject(raw, "stored lock .lock");
  const unknown = Object.keys(fields).filter((key) => !PROJECTION_KEYS.includes(key as keyof RuntimeLockProjection));
  if (unknown.length > 0) {
    throw new RuntimeLockTamperedError(`stored lock .lock has unknown fields: ${unknown.join(", ")}`);
  }
  for (const key of PROJECTION_KEYS) {
    if (!(key in fields)) {
      throw new RuntimeLockTamperedError(`stored lock .lock is missing field ${key}`);
    }
  }
  return {
    world_id: requireText(fields, "world_id", "stored lock .lock"),
    world_definition_version: requireText(fields, "world_definition_version", "stored lock .lock"),
    world_instance_id: requireText(fields, "world_instance_id", "stored lock .lock"),
    worldline_id: requireText(fields, "worldline_id", "stored lock .lock"),
    reality_profile_ref: requireText(fields, "reality_profile_ref", "stored lock .lock"),
    reality_profile_hash: requireText(fields, "reality_profile_hash", "stored lock .lock"),
    world_profile_ref: requireText(fields, "world_profile_ref", "stored lock .lock"),
    world_profile_hash: requireText(fields, "world_profile_hash", "stored lock .lock"),
    composition_runtime: requireText(fields, "composition_runtime", "stored lock .lock"),
    composition_runtime_version: requireText(fields, "composition_runtime_version", "stored lock .lock"),
    service_contract_versions: requireVersionMap(fields, "service_contract_versions", "stored lock .lock"),
    provider_versions: requireVersionMap(fields, "provider_versions", "stored lock .lock"),
    artifact_hashes: requireVersionMap(fields, "artifact_hashes", "stored lock .lock"),
    schema_versions: requireVersionMap(fields, "schema_versions", "stored lock .lock"),
    migration_lineage: requireStringList(fields, "migration_lineage", "stored lock .lock"),
    runtime_config_hash: requireText(fields, "runtime_config_hash", "stored lock .lock"),
  };
}

/**
 * Decode one persisted lock file.
 *
 * INVARIANT:
 * A record is accepted only when its declared `lockDigest` equals the digest
 * recomputed from its own body and the body names the worldline the file is for.
 * A field edited by hand therefore fails here instead of silently pinning a
 * different reality.
 */
export function decodeStoredLock(payload: unknown, expectedWorldlineId: string): StoredRuntimeLock {
  const fields = asObject(payload, "stored lock");
  const schema = fields["schema"];
  if (schema !== LOCK_STORE_SCHEMA) {
    throw new RuntimeLockTamperedError(
      `stored lock schema must be ${LOCK_STORE_SCHEMA}, got ${JSON.stringify(schema)}`,
    );
  }
  const revision = fields["revision"];
  if (typeof revision !== "number" || !Number.isInteger(revision) || revision < 1) {
    throw new RuntimeLockTamperedError("stored lock revision must be an integer >= 1");
  }
  const declaredDigest = requireText(fields, "lockDigest", "stored lock");
  if (!DIGEST.test(declaredDigest)) {
    throw new RuntimeLockTamperedError("stored lock lockDigest must be a sha256 hex digest");
  }
  const lock = decodeProjection(fields["lock"]);
  const recomputed = lockProjectionDigest(lock);
  if (recomputed !== declaredDigest) {
    throw new RuntimeLockTamperedError(
      `stored lock digest ${declaredDigest} does not match its body (${recomputed})`,
    );
  }
  if (lock.worldline_id !== expectedWorldlineId) {
    throw new RuntimeLockTamperedError(
      `stored lock belongs to worldline ${lock.worldline_id}, not ${expectedWorldlineId}`,
    );
  }
  return {
    worldlineId: expectedWorldlineId,
    revision,
    writtenAt: requireText(fields, "writtenAt", "stored lock"),
    lockDigest: declaredDigest,
    lock,
  };
}

/** The identity a caller claims before a worldline is allowed to open. */
export interface WorldlineLockIdentity {
  readonly worldId: string;
  readonly worldDefinitionVersion: string;
  readonly worldInstanceId: string;
  readonly worldlineId: string;
}

/** Assert the persisted lock belongs to the worldline the caller is opening. */
export function assertStoredLockMatchesWorldline(
  stored: StoredRuntimeLock,
  identity: WorldlineLockIdentity,
): void {
  const pairs: readonly (readonly [string, string, string])[] = [
    ["world_id", stored.lock.world_id, identity.worldId],
    ["world_definition_version", stored.lock.world_definition_version, identity.worldDefinitionVersion],
    ["world_instance_id", stored.lock.world_instance_id, identity.worldInstanceId],
    ["worldline_id", stored.lock.worldline_id, identity.worldlineId],
  ];
  for (const [field, pinned, actual] of pairs) {
    if (pinned !== actual) {
      throw new RuntimeLockError(`runtime lock ${field} is ${pinned}, this worldline is ${actual}`);
    }
  }
}

/**
 * Assert the providers and schemas this host runs are exactly the pinned ones.
 *
 * A provider or schema that was upgraded (or added, or removed) is a refusal, not
 * a silent rewrite of the lock: the pinned set is the contract.
 */
export function assertProvidersMatchLock(
  stored: StoredRuntimeLock,
  local: {
    readonly providerVersions: Readonly<Record<string, string>>;
    readonly schemaVersions: Readonly<Record<string, string>>;
  },
): void {
  for (const [dimension, pinned, running] of [
    ["provider", stored.lock.provider_versions, local.providerVersions],
    ["schema", stored.lock.schema_versions, local.schemaVersions],
  ] as const) {
    for (const [name, version] of Object.entries(pinned)) {
      const actual = running[name];
      if (actual === undefined) {
        throw new RuntimeLockError(`runtime lock pins ${dimension} ${name}@${version} but this host does not run it`);
      }
      if (actual !== version) {
        throw new RuntimeLockError(
          `runtime lock pins ${dimension} ${name}@${version}, this host runs ${actual} (refusing a silent upgrade)`,
        );
      }
    }
    for (const name of Object.keys(running)) {
      if (!(name in pinned)) {
        throw new RuntimeLockError(`this host runs ${dimension} ${name}, which the runtime lock does not pin`);
      }
    }
  }
}

/** Project a persisted lock into the reference the composition host consumes. */
export function toRuntimeLockRef(stored: StoredRuntimeLock): RuntimeLockRef {
  const split = (ref: string): { id: string; version: string } => {
    const at = ref.lastIndexOf("@");
    if (at <= 0 || at === ref.length - 1) {
      throw new RuntimeLockError(`runtime lock profile ref is not id@version: ${ref}`);
    }
    return { id: ref.slice(0, at), version: ref.slice(at + 1) };
  };
  const reality = split(stored.lock.reality_profile_ref);
  const world = split(stored.lock.world_profile_ref);
  return {
    lockId: stored.lock.worldline_id,
    lockVersion: String(stored.revision),
    lockDigest: stored.lockDigest,
    realityProfile: { id: reality.id, version: reality.version, digest: stored.lock.reality_profile_hash },
    worldProfile: { id: world.id, version: world.version, digest: stored.lock.world_profile_hash },
    compositionRuntime: {
      name: stored.lock.composition_runtime,
      version: stored.lock.composition_runtime_version,
    },
    serviceContractVersions: { ...stored.lock.service_contract_versions },
    providerVersions: { ...stored.lock.provider_versions },
    schemaVersions: { ...stored.lock.schema_versions },
  };
}

/** Where a worldline's pinned lock comes from. */
export interface LockSource {
  /** Return the stored lock, or `null` when the worldline has no persisted lock. */
  read(worldlineId: string): StoredRuntimeLock | null;
}

/** Reads the lock files the Python `FileLockStore` writes: `<root>/<worldlineId>.json`. */
export class FileLockSource implements LockSource {
  constructor(private readonly root: string) {}

  read(worldlineId: string): StoredRuntimeLock | null {
    const path = join(this.root, `${worldlineId}.json`);
    let text: string;
    try {
      text = readFileSync(path, "utf-8");
    } catch (error: unknown) {
      const code = (error as { code?: string }).code;
      if (code === "ENOENT") return null;
      throw new RuntimeLockError(`cannot read runtime lock ${path}: ${String(error)}`);
    }
    let parsed: unknown;
    try {
      parsed = JSON.parse(text);
    } catch {
      throw new RuntimeLockTamperedError(`runtime lock ${path} is not valid JSON`);
    }
    return decodeStoredLock(parsed, worldlineId);
  }
}
