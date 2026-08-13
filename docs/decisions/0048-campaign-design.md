# ADR-0048: Synthetic Campaign Domain Design (G11C, G11D)
- Status: accepted
- Date: 2026-08-13

## Context
G11 needs a synthetic campaign with orders, logistics, movement and fog-of-war.

## Decision
1. CampaignDomain models factions/units/regions/routes/resources/objectives.
2. Orders have delay/lifecycle; supply respects capacity; movement needs a
   route; fog-of-war limits faction knowledge to observed regions.

## Consequences
- Campaign invariants are deterministic and testable; beliefs respect
  fog-of-war.