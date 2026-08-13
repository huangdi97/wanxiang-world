# Heritage / Museum Substrate (G10A-G10D)

## IIIF (G10A)
`IiifIngester` parses manifests (canvas/annotation bodies, image/audio/video
service refs, rights/attribution) into a local metadata cache; real IIIF
endpoints are EXTERNAL_BLOCKED.

## Linked Art / CIDOC (G10B)
`LinkedArtMapper` maps production/acquisition/custody/conservation events with
Actor/Place/TimeSpan provenance and JSON-LD/external IDs (documented subset).

## Semantic twin (G10C)
`HeritageTwin` keeps PhysicalHeritageObject, DigitalSurrogate,
SemanticHeritageTwin and ReconstructionModel distinct; ConservationHistory is
versioned and replayable with rights/provenance.

## Museum biography (G10D)
`MuseumBiography` labels entries (evidence/reconstructed/creative) and enforces
curator review for private entries; `MuseumScenario` separates current /
historical / biography / conservation-lab instances.