# Plan 010 — Verification and Evidence

## Design

Implement a dependency-free `specgrain.verification` module and a read-only `prove` CLI surface.

### Verification flow

1. validate current `SpecNode`, `WorkPacket`, `ExecutionResult`, implementation revision, observed paths, and independent checks;
2. bind packet to current spec revision;
3. bind result to packet digest;
4. require executor success without treating it as sufficient;
5. compare executor-reported paths to independent observations;
6. enforce literal repository-relative authorized path/prefix surface;
7. evaluate packet acceptance and required-evidence check IDs;
8. require at least one independent check;
9. emit a normalized immutable `VerificationReport`.

### Evidence flow

- `.specgrain` must already be an ordinary initialized store;
- `.specgrain/evidence` is optional until the first append;
- records are canonical JSON with a bounded 1 MiB read limit and a 10,000-entry chain limit;
- each record links the previous digest and is named by its own digest;
- loading validates the full single-head chain without mutation;
- append uses exclusive creation, reloads the chain, and rolls back only its own just-created file on post-write failure.

### CLI

`specgrain prove SPEC_ID [PATH] [--json]` only reads the evidence chain. It performs no verification command execution and no lifecycle mutation.

## Planned implementation surface

- `src/specgrain/verification.py` — new verification/evidence kernel;
- `src/specgrain/cli.py` — add read-only `prove` command;
- `src/specgrain/__init__.py` — bounded public exports;
- `tests/test_verification.py` — kernel/storage adversarial coverage;
- `tests/test_verification_cli.py` — deterministic CLI proof coverage.

No modifications are planned to model, lifecycle, readiness, dependency scheduling, store parsing, repository scan, context budgeting, WorkPacket semantics, or runtime dependencies.
