# ADR-0041: Director Runtime Design (G07D)
- Status: accepted
- Date: 2026-08-13

## Context
G07D needs directors that influence worlds without owning commit authority or
rewriting actor beliefs/persona.

## Decision
1. Directors emit proposals; world-changing proposals traverse normal
   validation/commit.
2. Narrative signals and performance directives are projection-only.
3. Character/persona delta candidates require actor-logic review.

## Consequences
- Directors can shape but never commit or silently rewrite actors.