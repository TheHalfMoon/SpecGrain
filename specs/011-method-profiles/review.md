# Review 011 — Method Profiles

## Exact implementation review

Reviewed product commit:

`48626e69c155f08710337c2c7605d05c2eb9ff3a`

Implementation surface is limited to:

- `src/specgrain/method.py`
- bounded exports in `src/specgrain/__init__.py`
- `tests/test_method.py`

## Findings

No material repository-local defect found in the exact uploaded diff.

The design preserves these boundaries:

- `quick` remains backward-compatible and adds zero method-specific ceremony.
- Existing 004 readiness behavior is not modified.
- Stronger profiles are deterministic metadata/evidence gates, not document factories.
- Profile evidence is expressed through the existing `evidence.required` contract instead of a parallel evidence system.
- No lifecycle transition is granted by the method module.
- No CLI/store/scheduler/provider/executor behavior is added.
- No third-party runtime dependency is added.

## Residual boundary

Method profiles validate declarations. They do not independently prove that a baseline, cause analysis, rollback plan, experiment result, or independent review is truthful. Those identifiers become verification obligations through the existing 010 evidence boundary.
