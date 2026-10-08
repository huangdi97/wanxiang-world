# M95 Real Player Experience — Human Test Packet

This file is to be generated/filled against a real running build. It is not acceptance evidence until a genuine human completes it.

## Session metadata
- build SHA:
- world_package_id:
- scenario_id:
- world_instance_id:
- branch/worldline_id:
- actor/character_id:
- session_id:
- start/end time:
- tester pseudonymous ID:

## Required route
1. World Plaza
2. Select World / Scenario
3. Select or Create Character
4. Enter
5. Observe current world state
6. Perform >= 3 free-form actions
7. See NPC/world response
8. Inspect consequence / StateDiff
9. Leave
10. Continue

## Human questions (1–5)
- I understood where I was and what I could do:
- My choices felt meaningfully different:
- I could tell what changed because of my action:
- NPC/world responses were coherent with prior state:
- After Continue, the world felt like the same ongoing world:
- Overall experience quality:

## Open questions
- What was confusing?
- Which action felt ignored or overly constrained?
- Did any response claim a consequence you could not see in state/history?
- Did any character forget something important from this session?
- Would you continue this world voluntarily? Why/why not?

## Hard-failure checklist
- [ ] authority bypass
- [ ] private information leak
- [ ] narrative claims state change without committed StateDiff
- [ ] leave/continue restores wrong branch/character/world state
- [ ] crash/data loss
- [ ] P0/P1 usability blocker

## Evidence links
- sanitized session artifact:
- event refs:
- state diff refs:
- replay hash:
- screenshots/video (optional, sanitized):
