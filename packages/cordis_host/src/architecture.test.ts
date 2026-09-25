import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

import { describe, expect, it } from "vitest";

/**
 * Architecture guard for the composition host.
 *
 * It is the JS-level counterpart of the repository's Python architecture check:
 * consumers must depend on seams, and only the authority bootstrap may mint a
 * commit capability.
 */
const SRC = join(process.cwd(), "src");

interface SourceFile {
  readonly name: string;
  readonly text: string;
}

function sources(): SourceFile[] {
  const files: SourceFile[] = [];
  const walk = (dir: string, prefix: string): void => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        walk(join(dir, entry.name), `${prefix}${entry.name}/`);
        continue;
      }
      if (!entry.name.endsWith(".ts")) continue;
      files.push({
        name: `${prefix}${entry.name}`,
        text: readFileSync(join(dir, entry.name), "utf-8"),
      });
    }
  };
  walk(SRC, "");
  return files;
}

function modulesMentioning(token: string): string[] {
  return sources()
    .filter((file) => !file.name.endsWith(".test.ts") && file.text.includes(token))
    .map((file) => file.name)
    .sort();
}

describe("R7 composition host architecture guards", () => {
  it("lets only the authority bootstrap mint a commit capability", () => {
    expect(modulesMentioning("mintCapability")).toEqual([
      "authority.ts",
      "internal/capability-core.ts",
    ]);
  });

  it("keeps plugin consumers away from the concrete history provider", () => {
    const mentioning = modulesMentioning("MemoryHistoryProvider");
    // Infrastructure may name the provider; consumers must not.
    expect(mentioning).not.toContain("bundle.ts");
    expect(mentioning).not.toContain("commit.ts");
    expect(mentioning).toEqual(["history.ts", "host.ts", "index.ts", "scopes.ts"]);
  });

  it("loads plugins through the seam only", () => {
    // The reference plugin depends on the authority and history *seams*, never on
    // a provider implementation or on the authority's private mint.
    const bundle = sources().find((file) => file.name === "bundle.ts");
    expect(bundle).toBeDefined();
    expect(bundle?.text).not.toContain("MemoryHistoryProvider");
    expect(bundle?.text).not.toContain("mintCapability");
    expect(bundle?.text).toContain("./authority");
  });

  it("never imports composition-runtime internals", () => {
    const offenders = sources()
      .filter((file) => /from\s+"cordis\/(lib|src)\//.test(file.text))
      .map((file) => file.name);
    expect(offenders).toEqual([]);
  });

  it("requires every import path to stay inside the package", () => {
    const offenders = sources()
      .filter((file) => /from\s+"\.\.\//.test(file.text))
      .map((file) => file.name);
    expect(offenders).toEqual([]);
  });
});
