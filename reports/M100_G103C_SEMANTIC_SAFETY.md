# M100 G103C Semantic Safety Requalification

Conclusion: PASS. 9/9 commands completed on
candidate SHA `57ca7916a63e4332b996f60fe820c84b18c006c5`. Each command stores stdout/stderr hashes and a
bounded output tail in the machine-readable artifact; no result is inferred from prose.

| Command | Status | Exit | Duration |
|---|---|---:|---:|
| security_reliability | PASS | 0 | 75804.331 ms |
| security_forensics | PASS | 0 | 992.901 ms |
| architecture_guard | PASS | 0 | 3318.276 ms |
| kernel_guard | PASS | 0 | 460.081 ms |
| source_canon_immutability | PASS | 0 | 3105.058 ms |
| provider_integration_boundaries | PASS | 0 | 5614.141 ms |
| provider_unit_boundaries | PASS | 0 | 3115.51 ms |
| replay_branch_recovery | PASS | 0 | 5570.69 ms |
| rights_privacy_resources | PASS | 0 | 34960.763 ms |

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
