# ADR-0026: Source Registry & Source Gate Design (G04B)

- Status: accepted
- Date: 2026-08-13

## Context

G04B needs a source/evidence/rights intake gate so unapproved, rights-denied or
malicious content cannot enter canonical compilation, and conflicting claims
survive as separate evidence-backed candidates.

## Decision

1. Source records are immutable (id + content hash); review stage transitions
   (E0..E5) are validated and every decision is appended to an audit history.
2. Canonical eligibility requires rights approval + an approved review stage,
   checked by a pure SourceGate with a versioned SourcePolicy.
3. Malicious injection markers are detected at the gate; flagged payloads are
   never surfaced as data or instructions.
4. Conflicting claims coexist as separate ClaimCandidates with their own
   EvidenceLinks; no losing claim is overwritten.

## Consequences

- Only rights-approved, reviewed sources reach compilation; audit history is
  immutable; source payloads stay data, never instructions.