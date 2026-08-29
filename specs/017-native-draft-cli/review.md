# Exact-Head Manual Review — Specification 017

## Review target

- Product PR: #21
- Canonical shaped base: `5c7783dde897c975b3519b37bfd45b547244b273`
- Reviewed repaired implementation head: `0a01d0c10039f277458b6f30652ed9443f80e645`

This review covers the implementation diff from the canonical shaped base through the repaired implementation head. Evidence-only documentation added after this review must be rechecked before merge but does not expand product authority.

## Findings

### Store write boundary

`create_draft_spec` loads the existing repository-local store, rejects invalid refinement structure, allocates the lowest unused positive canonical ID, constructs a `SpecNode` fixed to `DRAFT`, and writes it through create-if-absent file creation.

The persistence path uses `os.open` with `O_CREAT | O_EXCL`; an existing target produces `StoreExistsError` and is not replaced. Write failure cleanup is bounded to the newly created target and suppresses only cleanup `OSError` before re-raising the original failure.

No edit, replace, rename-over-existing, or lifecycle transition path is introduced.

### Lifecycle and readiness authority

The created node is explicitly fixed to `SpecState.DRAFT.value`. The implementation does not populate parent, children, dependencies, acceptance conditions, change surface, or readiness declaration fields. The CLI reports `CREATED`, not `PASS`, `VERIFIED`, `READY`, or equivalent.

No transition authority, Grain readiness mutation, WorkPacket generation, execution, verification, or evidence mutation is added.

### Validation layering

The authoring primitive reuses store parsing, `SpecNode` validation, and refinement validation. It does not broaden the lower-level store module into dependency scheduling or execution orchestration.

A new root DRAFT has no dependencies and cannot alter existing dependency edges. Dependency-graph validation remains owned by the higher project/check layer. Expanding that layering was therefore not required for this bounded write and would be silent scope growth.

### CLI safety

Known store/model validation failures return non-zero. Unexpected exceptions are redacted as `internal error`. JSON output is deterministic and contains only the created spec ID, DRAFT state, relative store path, and semantic revision.

No repository command execution, shell invocation, network call, telemetry, secret access, or provider-specific behavior is added.

### Package and dependency surface

No runtime dependency, workflow, release configuration, benchmark implementation, provider adapter, hosted surface, or package version change is present.

README and architecture changes distinguish current `main` behavior from published `v0.1.0`; CHANGELOG records the feature under `Unreleased` and does not claim another release.

### Test and CI defects found during review cycle

Two material gate defects were found before merge and repaired forward:

1. Ruff `SIM105` in cleanup logic at head `f8cf61d864dba23a8754f7c981c57462fd8e7447`.
2. An isolated CLI test fixture missing the new store symbol at head `695088d6fbeb0a07f712aded3527cf7f10a3027b`.

The repaired implementation head `0a01d0c10039f277458b6f30652ed9443f80e645` subsequently completed exact-head CI run `33235745053` successfully across all five permanent matrix jobs.

## Review-service state

GitHub reports no submitted review and no inline review thread. Qodo is billing/trial blocked. CodeRabbit skipped automatic review because the repository has fewer than 10 stars. Cubic supplied only an automated summary. These conditions are not external-review approvals.

## Residual risks

- ID allocation is deterministic for a loaded store but concurrent independent writers can select the same next ID; create-if-absent semantics make the loser fail closed and retry against refreshed truth rather than overwrite.
- Local filesystem actors outside SpecGrain remain outside the process-level trust boundary and can mutate files between operations; the command does not claim transactional multi-process locking.
- Recursive refinement and editing remain unavailable through the CLI by design and require a future evidence-shaped specification if selected.
- Public adoption evidence remains sparse because the project/release are new.

## Manual review disposition

No unresolved material implementation defect was found on `0a01d0c10039f277458b6f30652ed9443f80e645` after the two forward repairs above. This disposition does not authorize merge of a later head until that exact final head is rechecked for diff, CI, and review-thread state.
