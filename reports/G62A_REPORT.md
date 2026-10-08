# G62A Report — Book E2E

**PASS** — TXT and EPUB sources use the existing `BookAdapter`, stable
locators, distillation pipeline, compiler boundary, package manifest, and
isolated preview. EPUB bytes are resolved through an injected blob resolver;
they are not copied into the repository or into Core.

Evidence: `test_epub_blob_reaches_draft_package_and_preview_without_api` and
the existing book-adapter/locator regression tests.
