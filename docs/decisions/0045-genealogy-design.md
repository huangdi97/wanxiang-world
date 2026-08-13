# ADR-0045: Genealogy & Family Design (G09A-G09C)
- Status: accepted
- Date: 2026-08-13

## Context
G09 needs GEDCOM interoperability, a family semantic world with conflicting
claims, and privacy/persona modes.

## Decision
1. GEDCOM subset parser/writer with source/media preservation and round-trip.
2. Imported facts are Claims/Evidence, never unconditional truth.
3. Living-archive privacy gates by consent/revocation/posthumous policy; persona
   modes are strictly labeled.

## Consequences
- Genealogy imports stay evidence-bound; living-person privacy is enforced.