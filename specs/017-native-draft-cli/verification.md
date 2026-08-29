# Verification Evidence — Specification 017

## Scope

This document records pre-merge verification for Specification 017 — Native DRAFT CLI. It does not claim canonical completion or product merge.

## Authority chain

- Pre-017 canonical closeout: `7c343841424ca48207f9c42eae725a53213d19e5`.
- Shaping PR: #20.
- Exact shaping head: `c700f5dcda9b82619bbae5fd920ab1b01b3d76de`.
- Shaping PR CI: run `33235373688`, successful on that exact head.
- Canonical shaping merge: `5c7783dde897c975b3519b37bfd45b547244b273`.
- Implementation branch: `feat/017-native-draft-cli-implementation`, created from that exact shaping merge.
- Product PR: #21.

## Verification chronology

### Initial implementation head

Head `f8cf61d864dba23a8754f7c981c57462fd8e7447` did not satisfy the repository gate. CI run `33235632792` stopped in Ruff source checks because `src/specgrain/store.py` violated `SIM105` in write-error cleanup.

No success claim is attached to that head.

### First repair head

Head `695088d6fbeb0a07f712aded3527cf7f10a3027b` replaced the cleanup `try/except/pass` with `contextlib.suppress(OSError)` without changing create-if-absent behavior.

CI run `33235713907` progressed past Ruff but failed full regression. The exact failure was isolated to the `tests/test_repository_cli.py` module fixture, whose synthetic `specgrain.store` stub did not expose the newly added `create_draft_spec` symbol. The regression log reported 525 passing tests before four import/setup errors from that fixture.

No success claim is attached to that head.

### Repaired implementation head

Head `0a01d0c10039f277458b6f30652ed9443f80e645` updated only the isolated CLI fixture to expose the new store API.

Exact-head CI run `33235745053` completed with conclusion `success` and was associated with PR #21. All five permanent matrix jobs completed successfully:

- Ubuntu / Python 3.11;
- Ubuntu / Python 3.12;
- Ubuntu / Python 3.13;
- macOS / Python 3.11;
- Windows / Python 3.11.

Across those jobs the repository gates completed successfully, including Ruff source/tests/examples, editable install, full regression, tracked-tree unchanged check, compile, CLI smoke, package build, built-wheel installation, and installed-CLI smoke.

## Behavioral evidence covered by tests

The implementation test surface covers:

- root DRAFT creation through the public API;
- deterministic lowest-unused positive `SG-######` allocation;
- root-only state and absence of implicit readiness metadata;
- canonical store-v1 persistence;
- create-if-absent collision refusal without overwrite;
- invalid input without artifact creation;
- CLI text output using `CREATED` rather than a verification claim;
- deterministic machine-readable JSON output;
- missing-store and invalid-input failures;
- unexpected internal-error redaction;
- `init -> draft -> check` compatibility;
- compatibility of the isolated repository-scan CLI fixture.

## Review-service boundary

No external substantive review is recorded for PR #21:

- Qodo posted that reviews are paused because the trial ended / billing is blocked.
- CodeRabbit explicitly skipped automatic review because the repository has fewer than 10 stars.
- GitHub reports no submitted PR reviews and no inline review threads at the time this evidence was recorded.
- Cubic added an automated PR summary, not a review submission or review thread.

None of these service states is converted into an external-review success claim.

## Evidence-head rule

The successful implementation head above predates this evidence document. Committing verification/review documentation moves the PR head, so the final product PR head must complete the required CI matrix again and be rechecked for review/thread state before expected-head merge.
