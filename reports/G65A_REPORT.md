# G65A Report — OCR Provider Port

**PASS** — OCR is represented by the existing ProviderRouter/Provider port;
without a registered capability the source path raises explicit
`OCR_REQUIRED`, including scanned PDF behavior. No OCR output is fabricated.

Evidence: M62 provider negative test and existing scanned-PDF test.
