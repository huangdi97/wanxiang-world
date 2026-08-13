# ADR-0040: Opportunity / Challenge / Event Compiler Design (G07C)
- Status: accepted
- Date: 2026-08-13

## Context
G07C needs deterministic opportunities compiled into executable challenges with
prerequisites and verifiable outcomes, without LLM-generated unvalidated tasks.

## Decision
1. OpportunityDetector is a domain-neutral port with a deterministic default.
2. ChallengeSpec carries prerequisites, safety/rights/evidence requirements and
   end conditions; compiler validates every spec.

## Consequences
- Challenges are executable and reviewable; no unvalidated tasks enter the
  world.