# Plan 011 — Method Profiles

## Design

Add a dependency-free `specgrain.method` module. Keep profile evaluation separate from the existing 004 readiness engine, then compose both reports through `evaluate_method_readiness`.

This preserves backward compatibility: ordinary `quick` nodes behave exactly as before, while callers that require method-aware readiness receive the stricter composite gate.

## Planned implementation surface

- `src/specgrain/method.py` — profile definitions, issues, profile report, composite readiness;
- `src/specgrain/__init__.py` — bounded exports;
- `tests/test_method.py` — profile and composition tests.

No changes are planned to lifecycle, store, verification, WorkPacket, CLI, repository scan, context budget, or dependencies.

## Evidence reuse

Method profiles do not create a second evidence vocabulary. Required method evidence identifiers are declared in `SpecNode.evidence.required`, then automatically flow into WorkPacket 009 and independent verification 010.
