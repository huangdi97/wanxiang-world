# G65D Report — Subtitle Transcript Adapter

**PASS** — deterministic SRT cue parsing emits stable source-linked time
ranges, rejects invalid ranges, and does not classify subtitle text as a
semantic claim.

Evidence: `SubtitleAdapter` cue and malformed-input tests.
