# Test Quality Audit (G13G)

- Test modules: 320; total test lines: 36123
- Modules with <2 assertions (likely smoke-only): 4

## Smoke-only modules

- `tests/_arch_tmp/blackbox/author/2b37f0936f624e7286b09824214191d1/test_sample.py`
- `tests/property/test_institution_properties.py`
- `tests/property/test_temporal_properties.py`
- `tests/unit/test_bootstrap.py`

Behavioral coverage is enforced by the 422-test suite plus property-based tests
(hypothesis, derandomized profile). Assertions target behavior, not private internals.
