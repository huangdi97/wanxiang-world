# Genealogy / Family Substrate (G09A-G09C)

## GEDCOM (G09A)
`parse_gedcom`/`serialize_gedcom` implement a documented GEDCOM 5.5 subset
(INDI/FAM/SOUR) with source/media refs, extension preservation and round-trip
checks. Imported facts map to Claims/Evidence, not truth. A privacy hook flags
living persons.

## Family world (G09B)
`FamilyWorld` validates time-scoped kinship (no self-loops/cycles), lineage
queries, life events, residences/media links and conflicting Claim sets.

## Privacy & persona modes (G09C)
`LivingArchive` gates private memories/media by consent, revocation and
posthumous policy; Evidence / Reconstructed Persona / Creative Legacy modes are
strictly labeled and never conflated.