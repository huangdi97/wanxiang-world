"""Private data table for the R7 versioned service-contract catalog.

The declarative rows are split into bounded modules so the architecture file-size
gate remains meaningful while the public catalog stays a single deterministic tuple.
"""

from __future__ import annotations

from typing import Final

from wanxiang_reality._contract_specs_core import CORE_CONTRACT_SPECS
from wanxiang_reality._contract_specs_extended import EXTENDED_CONTRACT_SPECS

_ContractSpec = tuple[str, str, tuple[str, ...], tuple[str, ...], str]

CONTRACT_SPECS: Final[tuple[_ContractSpec, ...]] = CORE_CONTRACT_SPECS + EXTENDED_CONTRACT_SPECS
