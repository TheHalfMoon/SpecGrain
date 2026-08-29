# Specification 019 Exact-Head Review

## Reviewed product head

`994f40f84ad3696b4037ea05eaec746c19bb473f`

The subsequent evidence commit changes specification evidence/task material only. It must receive its own exact-head CI before product merge.

## Scope review

The implementation remains bounded to native DRAFT authoring, transaction/recovery store logic, CLI/export surfaces, focused tests, truthful unreleased documentation, and active-spec status. Package metadata remains `0.2.0` and runtime dependencies remain empty.

No SpecNode schema, lifecycle graph, readiness rule, dependency scheduler, WorkPacket/executor/provider, verification authority, release workflow, PyPI path, hosted service, telemetry, or empirical benchmark behavior changed.

## Authoring authority review

- `create_child_draft_spec` rejects malformed or missing parent IDs and requires the selected parent state to be exactly `DRAFT`.
- The new child is fixed to `DRAFT` and receives only the bounded authoring inputs plus `parent_id`; no lifecycle promotion or execution/readiness authority is synthesized.
- The parent postimage is constructed from the complete parent dictionary with only `children` changed by one appended child ID.
- The complete proposed forest is passed through the existing refinement validator before journal creation.
- Existing root `create_draft_spec` behavior remains available and refuses a pending authoring journal through ordinary `load_project` semantics.

## Persistence and recovery review

- The two-file operation is described as recoverable/fail-closed, never as multi-file OS-atomic.
- `.specgrain/tmp/authoring-transaction.json` is created with `O_CREAT|O_EXCL` semantics and records exact parent preimage text, parent postimage, child content, IDs, operation kind, and transaction version.
- Child publication remains create-if-absent.
- Parent replacement checks the exact preimage before and immediately before a same-directory `os.replace`; that atomicity claim applies only to the single parent file.
- Ordinary reads do not recover automatically; a pending journal causes an explicit recovery-required failure.
- Explicit recovery recognizes only exact no-write, child-only, and completed states. Any divergent parent/child state fails closed without canonical overwrite or ambiguous deletion.

## Findings and forward repairs

1. Manual review found that the handled child-collision path could have delegated to general child-only recovery and thereby deleted an externally created matching child. Commit `8b0a89252f3b43bcfd0a1d6c72756b7754876cc2` repaired the path so a create-if-absent collision with an unchanged parent clears only this transaction's journal and preserves the colliding child. A regression test binds that behavior.
2. CI run `33247281069` found four isolated repository-CLI fixture import errors after `550 passed`. The fixture stub predated the new public store imports. Commit `994f40f84ad3696b4037ea05eaec746c19bb473f` updated only that isolation surface; exact-head run `33247361906` then passed all five permanent cells with `554 passed` on Ubuntu/Python 3.11.

No unresolved material finding is known at this review point.

## Residual risk

Portable standard-library filesystems still do not provide one atomic commit across the child and parent files. Process interruption is handled through exact journal classification, but power-loss durability depends on filesystem/OS guarantees beyond the repository contract.

The journal serializes supported child-authoring writers. The contract does not claim global locking against arbitrary manual edits or that an explicit recovery command invoked concurrently with an actively running writer is safe; recovery is an operator mutation for an interrupted/pending transaction. Parent drift observable before replacement is detected by exact-preimage checks; a final non-cooperating race window remains documented rather than hidden.

## Review boundary

Qodo billing status and CodeRabbit's automatic-review skip are not review approvals. No submitted external review or inline thread existed at the reviewed product head. Manual exact-diff review plus exact-head automated evidence is the current review basis; external agents are not treated as verification authority.
