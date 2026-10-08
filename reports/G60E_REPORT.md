# G60E Report — Isolated Preview Scope

## Status

**PASS** — Preview installs are namespaced by `preview://`, idempotent per
  package, and kept in an in-memory registry separate from the published
  package registry.

## Evidence

- Each install records preview id, package id, draft id, and manifest hash.
- A repeated install returns the existing install; uninstall removes only that
  preview scope.
- Package hash matching is enforced by preview instantiation.

