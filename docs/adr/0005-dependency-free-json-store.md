# ADR-0005: Dependency-Free JSON Local Store for M2

**Status:** Accepted  
**Date:** 2026-08-28

## Context

The foundation architecture proposed YAML for authored repository state and listed Typer, Rich, Pydantic, and PyYAML as possible implementation dependencies. Specifications 001–004 reached a deterministic kernel with no runtime dependencies.

Specification 005 needs only a repository-local store plus `init` and `check`. Adding multiple dependencies at this boundary would increase installation, supply-chain, compatibility, and maintenance surface before evidence shows they are necessary.

JSON is already supported by Python's standard library, is machine-readable and diff-friendly, preserves Unicode, and maps directly onto the existing public `SpecNode.to_dict()` contract. A strict parser can reject duplicate object keys and non-finite numbers instead of silently normalizing them.

## Decision

Specification 005 uses a versioned JSON local-store format and the Python standard library only.

Canonical M2 layout:

```text
.specgrain/
  project.json
  specs/
    SG-000001.json
  policies/
    default.json
```

The 005 CLI uses `argparse` and is exposed through both `python -m specgrain` and the `specgrain` console entry point.

No Typer, Rich, Pydantic, PyYAML, or graph dependency is added in 005.

YAML may later be supported as an import/export or authored-format adapter if user evidence justifies it. Such support must preserve deterministic normalized semantics and cannot silently replace the versioned store contract.

## Consequences

- Fresh installs remain dependency-free at runtime.
- Store parsing and serialization can share explicit deterministic JSON rules with the existing kernel.
- Users can inspect and edit state with ordinary text tooling, but JSON comments/anchors are intentionally unavailable in v1.
- File extension, semantic format version, and migrations become explicit rather than relying on YAML parser behavior.
- Richer terminal presentation remains possible later without making presentation libraries part of the trust kernel.
- Evidence storage remains deferred to Specification 010 rather than creating empty canonical directories before their contract exists.
