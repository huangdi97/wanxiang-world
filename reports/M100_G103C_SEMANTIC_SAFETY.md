# M100 G103C Semantic Safety Requalification

Conclusion: PASS. 9/9 commands completed on
candidate SHA `a9be096ba0cda3b9c05d039e61e27cd529ca6b45`. Each command stores stdout/stderr hashes and a
bounded output tail in the machine-readable artifact; no result is inferred from prose.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
| security_reliability | PASS | 0 | 70939.569 ms |
| security_forensics | PASS | 0 | 810.386 ms |
| architecture_guard | PASS | 0 | 2744.932 ms |
| kernel_guard | PASS | 0 | 413.45 ms |
| source_canon_immutability | PASS | 0 | 2495.896 ms |
| provider_integration_boundaries | PASS | 0 | 4846.457 ms |
| provider_unit_boundaries | PASS | 0 | 2267.672 ms |
| replay_branch_recovery | PASS | 0 | 4827.751 ms |
| rights_privacy_resources | PASS | 0 | 33204.539 ms |

The matrix explicitly exercises source/canon immutability, provider proposal-only boundaries,
replay/branch/recovery, rights/privacy/resource controls, secret scanning, and kernel/architecture
guards. A missing executable is EXTERNAL_BLOCKED; every other non-zero command remains FAIL.
No private source, copyrighted source text, model cache, secret, or token is exported by this
qualification.

Boundaries: IMPLEMENTED = enforcement paths and guards; VALIDATED = PASS commands above;
EXPERIMENTAL/BOUNDED = provider/reference and research-adjacent behavior; NOT_PROVEN = live
customer data, production hosting, and external provider/hardware behavior; EXTERNAL_BLOCKED =
only commands whose required host executable is absent.

Machine-readable evidence: artifacts/v55_stable/m100/semantic_safety.json
Reproduce with: uv run python scripts/m100_semantic_safety.py
