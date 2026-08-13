# SDK, Plugin & World Pack Ecosystem Standard

The ecosystem claim is proven only when an external project can build a package without importing repository-private code or changing Core.

Required: stable public SDK boundary, semver/deprecation policy, authoring CLI/scaffold, schema validation, package conformance certification, plugin trust/capability policy, registry lifecycle, version pinning, dependency resolution, external black-box sample and tested documentation.

Executable plugins are a security boundary. If strong sandboxing is not implemented, say so and use a trusted/signed executable extension policy. Data-only packages must not gain code execution.

Publishing a new package version must never silently alter an existing World Instance pinned to an older version.
