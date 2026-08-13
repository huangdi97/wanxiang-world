/**
 * G12C: reproducible OpenAPI/TypeScript SDK generation contract.
 *
 * The public API vocabulary and version policy are documented; a stable
 * OpenAPI document is parsed into typed client helpers. Generation is
 * deterministic: the same document always produces the same client surface.
 */

export interface OpenApiOperation {
  readonly operationId: string;
  readonly method: string;
  readonly path: string;
  readonly parameters: ReadonlyArray<string>;
}

export interface OpenApiDocument {
  readonly openapi: string;
  readonly info: { readonly title: string; readonly version: string };
  readonly paths: Readonly<Record<string, Readonly<Record<string, unknown>>>>;
}

/** Parse a stable OpenAPI document into typed operations (deterministic). */
export function parseOpenApi(doc: OpenApiDocument): ReadonlyArray<OpenApiOperation> {
  const operations: OpenApiOperation[] = [];
  for (const path of Object.keys(doc.paths).sort()) {
    const item = doc.paths[path] as Readonly<Record<string, unknown>>;
    for (const method of ["get", "post", "put", "delete"] as const) {
      const op = item[method] as Readonly<Record<string, unknown>> | undefined;
      if (!op) {
        continue;
      }
      operations.push({
        operationId: String(op.operationId ?? `${method}_${path.replace(/[^a-zA-Z0-9]/g, "_")}`),
        method,
        path,
        parameters: ((op.parameters as ReadonlyArray<unknown> | undefined) ?? [])
          .map((p) => String((p as Readonly<Record<string, unknown>>).name ?? ""))
          .filter((name) => name.length > 0),
      });
    }
  }
  return operations;
}

/** Documented public API version policy. */
export const API_VERSION_POLICY = {
  current: "v1",
  compatibility: "additive changes within v1; breaking changes require a new major",
  generated: "openapi.json -> TypeScript client types (deterministic)",
} as const;