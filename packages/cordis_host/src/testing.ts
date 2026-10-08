import cordisPackage from "cordis/package.json";

import { CONTRACT_IDS, getContract } from "./contracts";
import type { ProfileRef } from "./lock";

/**
 * Test-support fixtures for the composition host.
 *
 * These build a lock reference for the seams this host composes so tests (and a
 * local developer boot) have a realistic, valid lock. The authoritative lock and
 * its digest are still produced by the Python `wanxiang_reality` package.
 */
const FIXTURE_DIGEST = "0".repeat(64);

export interface FixtureOverrides {
  readonly lockId?: string;
  readonly lockVersion?: string;
  readonly lockDigest?: string;
  readonly realityProfile?: ProfileRef;
  readonly worldProfile?: ProfileRef;
  readonly compositionRuntimeVersion?: string;
  readonly providerVersions?: Readonly<Record<string, string>>;
  readonly serviceContractVersions?: Readonly<Record<string, string>>;
}

export interface SampleLockRef {
  readonly lockId: string;
  readonly lockVersion: string;
  readonly lockDigest: string;
  readonly realityProfile: ProfileRef;
  readonly worldProfile: ProfileRef;
  readonly compositionRuntime: { readonly name: string; readonly version: string };
  readonly serviceContractVersions: Readonly<Record<string, string>>;
  readonly providerVersions: Readonly<Record<string, string>>;
  readonly schemaVersions: Readonly<Record<string, string>>;
}

export function sampleProfileRef(id: string, version = "1"): ProfileRef {
  return { id, version, digest: FIXTURE_DIGEST };
}

export function sampleRuntimeLockRef(overrides: FixtureOverrides = {}): SampleLockRef {
  const seams: Record<string, string> = {};
  for (const id of CONTRACT_IDS) {
    seams[id] = overrides.serviceContractVersions?.[id] ?? getContract(id).apiVersion;
  }
  return {
    lockId: overrides.lockId ?? "lock_r7_fixture",
    lockVersion: overrides.lockVersion ?? "1",
    lockDigest: overrides.lockDigest ?? FIXTURE_DIGEST,
    realityProfile: overrides.realityProfile ?? sampleProfileRef("reality:persistent-v1"),
    worldProfile: overrides.worldProfile ?? sampleProfileRef("world:fixture"),
    compositionRuntime: {
      name: "cordis",
      version: overrides.compositionRuntimeVersion ?? cordisPackage.version,
    },
    serviceContractVersions: seams,
    providerVersions: overrides.providerVersions ?? {
      "history-memory": "1.0.0",
      "commit-authority": "1.0.0",
    },
    schemaVersions: { storage: "1" },
  };
}
