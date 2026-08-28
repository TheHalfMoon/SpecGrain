# Review 008 — Context Budget

**Review date:** 2026-08-28  
**Reviewed implementation head:** `5d7822218888302d95ccfc580ea37a0853759d34`

## Objective

Verify that Specification 008 makes context a deterministic finite accounting resource without introducing source-content retrieval, semantic selection, hidden tokenization, lifecycle/store mutation, or WorkPacket/evidence behavior.

## Exact-diff result

No material implementation defect remains in the reviewed uploaded head.

The exact one-commit implementation diff changes only:

- new `src/specgrain/context.py`;
- bounded public exports in `src/specgrain/__init__.py`;
- new `tests/test_context.py`.

## Structural review

- context source records are immutable/slotted and revision/provenance/reason bound;
- bool and invalid integer costs/ceilings fail closed;
- source collections reject non-record members and duplicate IDs;
- evaluation canonicalizes source identity so collection order cannot change results;
- all required sources remain selected even when their aggregate budget fails;
- required token/byte/source-count overflows have stable blocker codes;
- optional sources are considered only by `(priority, source_id)` and never convert required overflow into a pass;
- a large omitted optional source does not prevent a later smaller source from fitting;
- normalized plan digest binds policy, all records, selected/omitted IDs, totals, and issues;
- `require_context_budget` preserves the exact failed report;
- repository-map integration serializes only the already-normalized `RepositoryMap`, binds its digest, and does not rescan or open repository source content.

## Trust boundary

The exact diff contains no:

- arbitrary file-content retrieval;
- tokenizer invocation or hidden token estimate;
- LLM/embedding/semantic relevance selection;
- WorkPacket or execution-result contract;
- evidence or verification semantics;
- lifecycle/store mutation;
- scheduler/dependency-wave changes;
- subprocess execution;
- third-party runtime dependency.

## Verification evidence

Exact uploaded blobs match locally verified bytes. Verification is 354 pytest tests PASS, compileall PASS, editable install PASS, entry-point help parity PASS, and 0 changed source/test lines over 100 characters. Ruff is NOT RUN because unavailable.

## Residual risk

The deterministic core cannot establish that a caller-supplied `token_cost` came from the intended tokenizer. The source record binds the cost to explicit provenance/revision data; stronger measurement provenance belongs at a later adapter or packet/evidence boundary rather than inside this model-neutral kernel.

## Conclusion

Specification 008 implementation is ready for a bounded pull request after the review/verification record commits. Exact PR-head checks/reviews and the expected-head merge guard must bind to the final documentation head, not only to the product commit above.
