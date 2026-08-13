import { describe, expect, it } from "vitest";

import { API_VERSION_POLICY, parseOpenApi, type OpenApiDocument } from "./openapi.js";

const doc: OpenApiDocument = {
  openapi: "3.0.0",
  info: { title: "Wanxiang API", version: "v1" },
  paths: {
    "/worlds/{id}/projection": {
      get: { operationId: "getProjection", parameters: [{ name: "id" }] },
    },
    "/worlds/{id}/commands": {
      post: { operationId: "submitCommand", parameters: [] },
    },
  },
};

describe("G12C openapi sdk", () => {
  it("parses operations deterministically", () => {
    const ops = parseOpenApi(doc);
    expect(ops.map((o) => o.operationId)).toEqual(["submitCommand", "getProjection"]);
    const first = ops[0];
    expect(first).toBeDefined();
    expect(first?.method).toBe("post");
    expect(first?.parameters).toEqual([]);
    const again = parseOpenApi(doc);
    expect(JSON.stringify(ops)).toBe(JSON.stringify(again));
  });

  it("documents the version policy", () => {
    expect(API_VERSION_POLICY.current).toBe("v1");
    expect(API_VERSION_POLICY.generated).toContain("deterministic");
  });
});