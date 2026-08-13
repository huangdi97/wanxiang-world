# ADR-0046: Heritage & Museum Design (G10A-G10D)
- Status: accepted
- Date: 2026-08-13

## Context
G10 needs IIIF ingest, Linked Art/CIDOC mapping, distinct object/twin/
reconstruction identities and replayable object biographies.

## Decision
1. IIIF and Linked Art are adapters over synthetic fixtures (real endpoints
   EXTERNAL_BLOCKED).
2. Physical object, digital surrogate, semantic twin and reconstruction are
   distinct; conservation history is versioned/replayable.
3. Museum biography entries carry truth labels; curator mode gates private
   entries.

## Consequences
- Heritage domains run on the same core with provenance and rights enforced.