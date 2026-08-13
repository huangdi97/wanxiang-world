# Audit & Traceability Protocol

## Purpose
Independent verification must be requirement-driven, not file-count-driven.

## Requirement extraction
Create stable requirement IDs from the mother specification and engineering contracts. Prioritize normative language and architecture invariants. Preserve original meaning; do not silently “fix” the specification during audit.

## Required trace fields
- requirement_id
- source_document + section/line or heading reference
- requirement summary
- kernel/cross-cutting owner
- implementation path/symbol
- public contract/API/schema
- test path/name
- runtime/build evidence
- status
- severity if gap
- notes/blocker

## Evidence hierarchy
Strongest evidence is an executable black-box/integration/property test over a real vertical path. Unit tests support but do not replace integration proof. Class/interface existence is weak evidence. Comments, TODOs and prior reports are not sufficient.

## Gap severity
P0: world truth/data-loss/security-critical/authority/replay/branch/mandatory-path false completion.
P1: required integration, maintainability, compatibility, rights, observability or release defect.
P2: non-blocking optimization/polish/research.

## False-completion indicators
- production path selects a Fake/static fixture;
- UI shows canned JSON rather than server projection;
- adapter interface exists but no contract/integration test;
- API route returns success without authoritative commit;
- migration claims without old-version fixture;
- replay test starts from already-derived current state;
- branch test shares mutable references;
- rights checked only in UI;
- source provenance lost after compile;
- generated SDK manually diverges from OpenAPI.

## Closure
Every P0/P1 fix should link root cause, code diff, regression test and affected requirement IDs. Never delete baseline audit evidence.
