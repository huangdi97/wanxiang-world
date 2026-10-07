# Third-party source notice

This directory contains a pinned copy of `optimality_search.py` from:

- Repository: https://github.com/TimoKellerMath/PointCountsAbelianVarieties
- Commit: `f9fcaf80b059378c6130532ca9a4ce7b1b18f47b`
- Upstream Git blob: `5c502b85161c3aeeda1efd352be3b83ce4b5d6df`
- License: MIT (copied as `LICENSE.upstream`)

It is included only as a bounded R7 Artifact2Capability qualification fixture.
The associated paper is arXiv:2606.28989v2. Only citation metadata is vendored;
the paper PDF/text is not redistributed here.

The Wanxiang wrapper imports the pinned upstream module and calls its real
`study(q, N=2)` implementation. It does not reimplement the scientific method.
