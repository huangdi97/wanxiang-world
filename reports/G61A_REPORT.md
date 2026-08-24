# G61A Report — Creation API

**PASS** — `AuthoringService` and `/studio/jobs` implement create/add-source,
start, cancel, resume, and status over the existing JobStore checkpoint
contract. Repeated start/preview requests are idempotent.

Evidence: `test_authoring_service_reference_e2e_and_idempotent_preview`,
`test_cancel_then_resume_keeps_checkpoint_contract`, and API surface tests.

