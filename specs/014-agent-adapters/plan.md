# Plan 014 — Agent Adapters

## Design

Add one dependency-free `adapter.py` module that translates canonical WorkPackets into deterministic request envelopes and normalizes bounded external result payloads back into canonical ExecutionResults.

No vendor-specific adapter is added because the roadmap requires demonstrated adoption demand before taking on that maintenance surface, and current canonical repository evidence contains no such demand signal.

## Change surface

- `src/specgrain/adapter.py`
- `src/specgrain/__init__.py`
- `tests/test_adapter.py`
- Specification/ADR/continuation records only.

No CLI, store, lifecycle, verification, dependency, repository-scan, context, packet, or runtime-dependency change is authorized.

## Verification

- focused adapter determinism/strictness tests;
- full 001–014 pytest regression on the exact product/test bytes;
- compileall;
- editable install with available build dependencies;
- console/module entry-point parity;
- changed-line length inspection;
- available static checks;
- exact uploaded-blob and exact-diff review.

If the local transient workspace is unavailable, an isolated verification branch may add a temporary GitHub Actions workflow while preserving identical product/test blob identities; that verification branch is not part of the product PR.
