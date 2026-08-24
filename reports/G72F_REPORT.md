# G72F Report — Studio product flow

**PASS (2026-08-25)** — Studio one-click performs Create → Auto Author →
Review Inbox → Preview → explicit Publish. The inbox remains a review surface;
publish validates the package and writes only the authoring job checkpoint.
Entering the world remains a separate runtime operation.

Evidence: `test_studio_one_click_and_cli_reference_use_the_same_flow` and the
M68 review-inbox regression.
