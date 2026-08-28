# Verification 009 — Work Packet

**Verification date:** 2026-08-28  
**Exact reviewed product commit:** `b7529a9290ac547aa7baa3084e947e5b70aad39c`

## Exact uploaded product/test blobs

```text
src/specgrain/packet.py          7ff0f351ae2fb2572c8b3f4c403e725892f47879
src/specgrain/__init__.py        e678bee437db684ab97380c082ff7aa7f6421d2d
tests/test_packet.py             7b148f5d5f46247c1693f0629d07aab8f31233f8
```

GitHub returned these same blob SHAs at the uploaded implementation head. The implementation comparison from planning head `01b8d996113b7c9d77515442aa149252301af6a8` contains exactly these three paths.

## Pytest

```text
python -m pytest -q
```

Result: **403 passed**.

This is the 354-test Specifications 001–008 baseline plus 49 new Specification 009 tests.

Focused coverage includes:

- portable context-source snapshots and immutability;
- exact SpecNode and context-plan revision binding;
- selected-context identity validation;
- passing-context-plan requirement;
- canonical ordering/permutation invariance;
- packet digest stability and semantic sensitivity;
- canonical compact JSON;
- detached serialization;
- strict packet unknown/missing-field and digest-tamper rejection;
- finite JSON float compatibility with SpecNode risk data;
- canonical SpecGrain dependency-ID validation;
- ExecutionResult succeeded/failed/blocked and error-code semantics;
- result digest sensitivity;
- canonical result JSON;
- strict result round-trip/tamper rejection;
- explicit absence of verification authority and provider/model/prompt fields.

## Compile / packaging / entry points

```text
python -m compileall -q src tests
python -m pip install -e . --no-build-isolation -q
cmp <(specgrain --help) <(python -m specgrain --help)
```

Result: **PASS** for all three checks.

Specification 009 intentionally adds no CLI command; entry-point parity verifies the existing CLI surface remains unchanged.

## Style preflight

Changed source/test lines over 100 characters: **0**.

Ruff remains unavailable in the execution environment and is therefore **NOT RUN**, not PASS.

## Scope verification

No executor is invoked. No provider/model/IDE/agent or procedural prompt becomes canonical packet state. No lifecycle/store/scheduler/CLI behavior is mutated. No evidence is independently verified. No subprocess or third-party runtime dependency is introduced.

## Result

The exact uploaded Specification 009 product bytes satisfy the planned WorkPacket / ExecutionResult contract and preserve the authority boundary required for Specification 010.