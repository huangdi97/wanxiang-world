import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

import { afterEach, describe, expect, it } from "vitest";

import { createHost } from "./host";
import { RuntimeLockError } from "./lock";
import {
  FileLockSource,
  LOCK_STORE_SCHEMA,
  RuntimeLockMissingError,
  RuntimeLockTamperedError,
  canonicalJson,
  decodeStoredLock,
  lockProjectionDigest,
  type RuntimeLockProjection,
  type StoredRuntimeLock,
} from "./stored_lock";

const repoRoot = resolve(process.cwd(), "..", "..");

function fixtureProjection(overrides: Partial<RuntimeLockProjection> = {}): RuntimeLockProjection {
  return {
    world_id: "world-a",
    world_definition_version: "1",
    world_instance_id: "instance-a",
    worldline_id: "wl-a",
    reality_profile_ref: "reality:reference-v1@1",
    reality_profile_hash: "1".repeat(64),
    world_profile_ref: "world:reference-v1@1",
    world_profile_hash: "2".repeat(64),
    composition_runtime: "cordis",
    composition_runtime_version: "4.0.0-rc.10",
    service_contract_versions: { "wanxiang.history@1": "1" },
    provider_versions: { "history-memory": "1.0.0" },
    artifact_hashes: {},
    schema_versions: {},
    migration_lineage: [],
    runtime_config_hash: "3".repeat(64),
    ...overrides,
  };
}

function fixtureRecord(overrides: Partial<RuntimeLockProjection> = {}, worldlineId = "wl-a"): Record<string, unknown> {
  const lock = fixtureProjection({ worldline_id: worldlineId, ...overrides });
  return {
    schema: LOCK_STORE_SCHEMA,
    revision: 1,
    writtenAt: "2026-09-26T00:00:00Z",
    lockDigest: lockProjectionDigest(lock),
    lock,
  };
}

/** Write a record to `<dir>/<worldlineId>.json`, re-signing it like the Python writer would. */
function writeLockFile(dir: string, record: Record<string, unknown>): void {
  const lock = record["lock"] as RuntimeLockProjection;
  writeFileSync(join(dir, `${lock.worldline_id}.json`), JSON.stringify(record, null, 2));
}

function resign(record: Record<string, unknown>): Record<string, unknown> {
  const lock = record["lock"] as RuntimeLockProjection;
  return { ...record, lockDigest: lockProjectionDigest(lock) };
}

describe("canonical lock digest", () => {
  it("matches the Python canonical encoding (sorted keys, compact separators)", () => {
    expect(canonicalJson({ b: 1, a: ["x", { d: "y", c: null }] })).toBe('{"a":["x",{"c":null,"d":"y"}],"b":1}');
    expect(canonicalJson("plain")).toBe('"plain"');
  });
});

describe("stored runtime lock decoding", () => {
  it("accepts a well-formed record and reports its digest", () => {
    const stored = decodeStoredLock(fixtureRecord(), "wl-a");
    expect(stored.lockDigest).toBe(lockProjectionDigest(stored.lock));
    expect(stored.revision).toBe(1);
  });

  it("refuses a record whose body was edited without re-signing", () => {
    const record = fixtureRecord();
    (record["lock"] as Record<string, unknown>)["provider_versions"] = { "history-memory": "9.9.9" };
    expect(() => decodeStoredLock(record, "wl-a")).toThrowError(RuntimeLockTamperedError);
  });

  it("refuses a wrong schema, a bad revision, a bad digest shape, missing and unknown fields", () => {
    expect(() => decodeStoredLock({ ...fixtureRecord(), schema: "other" }, "wl-a")).toThrowError(RuntimeLockTamperedError);
    expect(() => decodeStoredLock({ ...fixtureRecord(), revision: 0 }, "wl-a")).toThrowError(RuntimeLockTamperedError);
    expect(() => decodeStoredLock({ ...fixtureRecord(), lockDigest: "nope" }, "wl-a")).toThrowError(RuntimeLockTamperedError);
    const missing = { ...fixtureRecord() } as Record<string, unknown>;
    delete (missing["lock"] as Record<string, unknown>)["runtime_config_hash"];
    expect(() => decodeStoredLock(missing, "wl-a")).toThrowError(RuntimeLockTamperedError);
    const extra = fixtureRecord();
    (extra["lock"] as Record<string, unknown>)["unknown_field"] = "x";
    expect(() => decodeStoredLock(resign(extra), "wl-a")).toThrowError(RuntimeLockTamperedError);
  });

  it("refuses a lock that belongs to another worldline", () => {
    expect(() => decodeStoredLock(fixtureRecord(), "wl-b")).toThrowError(RuntimeLockTamperedError);
  });

  it("returns null for a missing file and fails on an unreadable one", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    const source = new FileLockSource(dir);
    expect(source.read("wl-missing")).toBeNull();
    writeFileSync(join(dir, "wl-bad.json"), "{not json");
    expect(() => source.read("wl-bad")).toThrowError(RuntimeLockTamperedError);
  });
});

describe("host lock enforcement without a Python toolchain", () => {
  it("requires exactly one lock source", () => {
    expect(() => createHost({})).toThrowError(RuntimeLockError);
  });

  it("refuses to open a worldline that has no persisted lock", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    const host = createHost({ lockSource: new FileLockSource(dir) });
    expect(() =>
      host.openWorld("world-a", "wl-a", { worldDefinitionVersion: "1", worldInstanceId: "instance-a" }),
    ).toThrowError(RuntimeLockMissingError);
    expect(host.scopes.openWorldlines()).toEqual([]);
  });

  it("demands the worldline identity when a lock source is configured", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    writeLockFile(dir, fixtureRecord());
    const host = createHost({ lockSource: new FileLockSource(dir) });
    expect(() => host.openWorld("world-a", "wl-a")).toThrowError(RuntimeLockError);
  });

  it("refuses an identity that the lock does not pin", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    writeLockFile(dir, fixtureRecord());
    const host = createHost({ lockSource: new FileLockSource(dir) });
    expect(() =>
      host.openWorld("world-a", "wl-a", { worldDefinitionVersion: "2", worldInstanceId: "instance-a" }),
    ).toThrowError(/world_definition_version/);
  });

  it("refuses a provider that drifted from the pinned version instead of rewriting the lock", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    const record = fixtureRecord();
    (record["lock"] as Record<string, unknown>)["provider_versions"] = { "history-memory": "2.0.0" };
    writeLockFile(dir, resign(record));
    const before = readFileSync(join(dir, "wl-a.json"), "utf-8");
    const host = createHost({
      lockSource: new FileLockSource(dir),
      providerVersions: { "history-memory": "1.0.0", "commit-authority": "1.0.0" },
    });
    expect(() =>
      host.openWorld("world-a", "wl-a", { worldDefinitionVersion: "1", worldInstanceId: "instance-a" }),
    ).toThrowError(/refusing a silent upgrade/);
    expect(readFileSync(join(dir, "wl-a.json"), "utf-8")).toBe(before);
  });

  it("refuses a schema the lock pins but this host does not run", () => {
    const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-"));
    const record = fixtureRecord({ schema_versions: { "event-schema": "3" } });
    writeLockFile(dir, record);
    const host = createHost({
      lockSource: new FileLockSource(dir),
      providerVersions: { "history-memory": "1.0.0" },
      schemaVersions: {},
    });
    expect(() =>
      host.openWorld("world-a", "wl-a", { worldDefinitionVersion: "1", worldInstanceId: "instance-a" }),
    ).toThrowError(/schema event-schema/);
  });
});

const pythonToolchainAvailable = spawnSync("uv", ["--version"], { stdio: "ignore" }).status === 0;
if (!pythonToolchainAvailable) {
  console.warn("uv is not on PATH: the cross-language runtime-lock tests will be skipped");
}

interface CreatedLock {
  readonly dir: string;
  readonly worldlineId: string;
  readonly stored: StoredRuntimeLock;
}

/** Create a real lock with the Python CLI and read it back through the TS reader. */
function createLockWithPython(): CreatedLock {
  const dir = mkdtempSync(join(tmpdir(), "wanxiang-lock-py-"));
  const worldlineId = "wl-py-locked";
  const result = spawnSync(
    "uv",
    [
      "run",
      "python",
      "-m",
      "wanxiang_reality.lock_cli",
      "create-worldline",
      "--root",
      dir,
      "--world-id",
      "world-py",
      "--world-instance-id",
      "instance-py",
      "--worldline-id",
      worldlineId,
      "--world-definition-version",
      "1",
      "--composition-runtime-version",
      "4.0.0-rc.10",
    ],
    { cwd: repoRoot, encoding: "utf-8" },
  );
  if (result.status !== 0) {
    throw new Error(`lock_cli failed: ${result.stdout} ${result.stderr}`);
  }
  const stored = new FileLockSource(dir).read(worldlineId);
  if (stored === null) throw new Error("lock_cli reported success but no lock file exists");
  return { dir, worldlineId, stored };
}

describe.skipIf(!pythonToolchainAvailable)("cross-language runtime lock", () => {
  const created = pythonToolchainAvailable ? createLockWithPython() : null;

  it("reads a lock written by Python with an identical digest", () => {
    const stored = created!.stored;
    expect(stored.lockDigest).toBe(lockProjectionDigest(stored.lock));
    expect(stored.lock.worldline_id).toBe(created!.worldlineId);
    expect(Object.keys(stored.lock.service_contract_versions).length).toBeGreaterThan(0);
    // The file on disk is the one we decoded: re-decoding the raw JSON is stable.
    const raw: unknown = JSON.parse(readFileSync(join(created!.dir, `${created!.worldlineId}.json`), "utf-8"));
    expect(decodeStoredLock(raw, created!.worldlineId).lockDigest).toBe(stored.lockDigest);
  });

  it("opens the worldline, pins it to the lock, and commits through the authority", () => {
    const stored = created!.stored;
    const host = createHost({
      lockSource: new FileLockSource(created!.dir),
      providerVersions: { ...stored.lock.provider_versions },
      schemaVersions: { ...stored.lock.schema_versions },
    });
    host.authority.registerAuthorityHolder("world-host", "audit:lock");
    const capability = host.authority.grant("world-host");
    const worldlineId = created!.worldlineId;
    host.openWorld(stored.lock.world_id, worldlineId, {
      worldDefinitionVersion: stored.lock.world_definition_version,
      worldInstanceId: stored.lock.world_instance_id,
    });
    expect(host.lockFor(worldlineId)?.lockDigest).toBe(stored.lockDigest);
    host.authority.registerRule(worldlineId, {
      ruleId: "rule-lock/v1",
      ruleVersion: "1",
      propose: () => ({ kind: "set_status", payloadDigest: "a".repeat(64) }),
    });
    const outcome = host.commit({
      worldlineId,
      requestingWorldlineId: worldlineId,
      requestedBy: "world-host",
      ruleId: "rule-lock/v1",
      capability,
    });
    expect(outcome.status).toBe("COMMITTED");
    expect(host.scopes.runtime(worldlineId).history.head(worldlineId).revision).toBe(1);
  });

  it("refuses a worldline whose lock file was edited by hand", () => {
    const stored = created!.stored;
    const path = join(created!.dir, `${created!.worldlineId}.json`);
    const record: unknown = JSON.parse(readFileSync(path, "utf-8"));
    const mutated = JSON.parse(JSON.stringify(record)) as Record<string, unknown>;
    (mutated["lock"] as Record<string, unknown>)["provider_versions"] = { "history-memory": "9.9.9" };
    writeFileSync(path, JSON.stringify(mutated));
    const host = createHost({
      lockSource: new FileLockSource(created!.dir),
      providerVersions: { ...stored.lock.provider_versions },
      schemaVersions: { ...stored.lock.schema_versions },
    });
    expect(() =>
      host.openWorld(stored.lock.world_id, created!.worldlineId, {
        worldDefinitionVersion: stored.lock.world_definition_version,
        worldInstanceId: stored.lock.world_instance_id,
      }),
    ).toThrowError(RuntimeLockTamperedError);
  });
});

afterEach(() => {
  // Nothing global to reset: every test owns its temporary lock directory.
});
