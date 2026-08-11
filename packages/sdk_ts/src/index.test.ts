import { describe, expect, it } from "vitest";

import { makeWorldRef, SDK_VERSION } from "./index.js";

describe("sdk baseline", () => {
  it("exports a version", () => {
    expect(SDK_VERSION).toBe("0.1.0");
  });

  it("builds a validated world ref", () => {
    expect(makeWorldRef("w1", "b1")).toEqual({ instanceId: "w1", branchId: "b1" });
  });

  it("rejects empty identities", () => {
    expect(() => makeWorldRef("", "b1")).toThrow("non-empty");
    expect(() => makeWorldRef("w1", "")).toThrow("non-empty");
  });
});
