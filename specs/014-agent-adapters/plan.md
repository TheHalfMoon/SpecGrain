# Plan 014 — Agent Adapters

## Design

Add one dependency-free `adapter.py` public module that translates canonical WorkPackets into deterministic request envelopes and normalizes bounded external result payloads back into canonical ExecutionResults.

No vendor-specific adapter is added because the roadmap requires demonstrated adoption demand before taking on that maintenance surface, and current canonical repository evidence contains no such demand signal.

The implementation deliberately does not modify package-root exports. `specgrain.adapter` is the bounded public adapter surface and declares its own `__all__`.

## Change surface

- `src/specgrain/adapter.py`
- `tests/test_adapter.py`
- Specification/ADR/continuation records only.

No root export, CLI, store, lifecycle, verification, dependency, repository-scan, context, packet, or runtime-dependency change is authorized.

## Verification

- focused adapter determinism/strictness tests;
- full 001–014 pytest regression on the exact product/test bytes;
- compileall;
- editable install with available build dependencies;
- console/module entry-point parity;
- Ruff on the 014 surface and full repository diagnostic;
- changed-line length inspection;
- exact uploaded-blob and exact-diff review.

Because the transient local workspace was unavailable, exact regression was run on an isolated verification-only branch. That branch differs from the product commit only by a workflow file and is not part of the product PR.
