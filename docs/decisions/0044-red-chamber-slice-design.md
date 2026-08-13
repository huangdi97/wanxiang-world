# ADR-0044: Red Chamber Source-gated Reference Slice Design (G08B)
- Status: accepted
- Date: 2026-08-13

## Context
G08B needs a bounded Red Chamber slice; real literary data is not available
with rights.

## Decision
1. Real data is EXTERNAL_BLOCKED; only manifests/templates/tests are created.
2. Source Gate positive/negative behavior must PASS; unapproved text never
   becomes canon; no fabricated facts.

## Consequences
- The platform gate is proven without inventing literary content.