/**
 * G34E: typed client helper for the constitution API surface.
 *
 * Constitution manifests are immutable, versioned records (domain value
 * objects); the client only reads them through the read-only endpoint.
 */

export interface ConstitutionManifest {
  readonly constitution_id: string;
  readonly version: number;
  readonly name: string;
  readonly schema_version: number;
  readonly root_constraints: ReadonlyArray<string>;
  readonly mutable_law_layers: ReadonlyArray<string>;
  readonly rights_ref: string;
  readonly evolution_policy: string;
  readonly content_hash: string;
}

/** Build a validated constitution-id string (read-only helper). */
export function constitutionId(value: string): string {
  if (value.length === 0) {
    throw new Error("constitution_id must be non-empty");
  }
  return value;
}

/** Validate a fetched manifest shape (server truth; client never mutates). */
export function assertConstitutionManifest(
  value: unknown,
): asserts value is ConstitutionManifest {
  const v = value as ConstitutionManifest;
  if (
    typeof v !== "object" ||
    v === null ||
    typeof v.constitution_id !== "string" ||
    typeof v.version !== "number" ||
    !Array.isArray(v.root_constraints)
  ) {
    throw new Error("invalid constitution manifest");
  }
}
