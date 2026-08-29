# ADR-0016 — Public Release Contract

**Status:** Accepted

## Context

Specification 016 is the first public release boundary. Earlier repository documents described launch aspirations that included commands, benchmark results, and public assets that did not yet exist. The release must represent only capabilities that are present and independently verifiable on the exact release revision.

## Decision

SpecGrain v0.1.0 will be a dependency-light Python release with these launch invariants:

1. Public documentation demonstrates only commands and APIs that exist on the release revision.
2. Permanent CI verifies Linux, macOS, and Windows before release.
3. Package metadata is versioned `0.1.0`; the Git tag and GitHub Release use `v0.1.0`.
4. The zero-to-verified walkthrough is executable and tested, rather than prose-only.
5. Spec Kit migration is documented as an explicit inspection/conversion boundary with no claim of silent in-place conversion.
6. Brownfield examples use pinned public repository revisions or the SpecGrain repository itself; fabricated scan output is forbidden.
7. The benchmark report distinguishes harness capability from empirical comparative results. No arm may be declared superior without a reproducible completed dataset.
8. Security, contribution, conduct, issue-reporting, architecture, methodology, provenance, and trust entry points are discoverable from the launch README.
9. Runtime dependency count remains zero unless a release requirement proves a dependency necessary.
10. Release closure requires exact product-PR merge evidence plus live tag/release evidence. Repository closeout may follow as a documentation-only commit after the release is published.

## Consequences

The first release is intentionally conservative. It proves the deterministic kernel and public workflow surface without pretending that deferred orchestration commands or comparative benchmark wins already exist. Later releases may expand the CLI and publish empirical benchmark conclusions when their evidence exists.
