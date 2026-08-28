# Review 006 — Dependency Graph

**Review date:** 2026-08-28  
**Reviewed implementation head:** `72409ba2881b04a7db41a3b30b9dc05c9eb69603`

## Objective

Verify that Specification 006 adds deterministic dependency structure/eligibility analysis and read-only `next` orchestration without crossing into lifecycle mutation, repository intelligence, conflict analysis, execution, or evidence semantics.

## Exact-diff result

No material implementation defect remains in the reviewed uploaded head.

The exact product source changes are limited to:

- a dependency-free `dependency.py` kernel;
- a small `project.py` orchestration layer composing the unchanged 005 local store with refinement/dependency checks;
- `next` CLI rendering/exit behavior;
- bounded public exports.

Specification 005 `store.py` is unchanged. This is intentionally narrower than the initial 006 plan, which considered extending store orchestration directly.

## Structural review

The dependency layer fails closed on duplicate IDs, missing dependencies, self-dependencies, and directed cycles. Diagnostics are deterministic. Grain eligibility requires current `GRAIN` state and all direct dependencies currently `VERIFIED`/`CONTROLLED`.

Hard blockers propagate through unresolved dependency chains but traversal stops at satisfied nodes. Wave projection is deterministic and dependency-only; it does not claim file/conflict-safe parallel execution.

A dense strongly connected sample was also manually exercised after the full test run and produced deterministic `CYCLE` blockers, confirming cycle invalidation remains fail-closed beyond the focused two/three-node fixtures.

## Trust boundary

The diff contains no:

- lifecycle mutation or `GRAIN -> READY` writer;
- repository scan or semantic dependency inference;
- file/change-surface conflict analysis;
- evidence ledger or verification execution;
- subprocess/provider/agent execution;
- third-party graph/runtime dependency.

`next_project` and `specgrain next` are read-only current-state projections. A projected wave is advisory dependency ordering only.

## Verification evidence

The exact product/test blobs uploaded to GitHub match the locally verified blob SHAs. Local verification for this candidate is 275 pytest tests PASS, compileall PASS, editable install PASS, console/module help equivalence PASS, and 0 changed source/test lines over 100 characters. Ruff remains NOT RUN because unavailable/offline.

## Conclusion

Specification 006 is ready for a bounded pull request after this review-record commit. The review record itself moves the branch head, so external checks and the final manual head confirmation must be repeated on that new exact SHA before merge.
