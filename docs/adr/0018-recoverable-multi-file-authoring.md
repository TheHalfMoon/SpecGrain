# ADR-0018 — Recoverable Multi-File Authoring Transactions

**Status:** Accepted

## Context

Specification 017 can safely create one new root SpecNode with `O_CREAT|O_EXCL` because only one canonical file is added. Native child authoring is different: the child must declare `parent_id`, while the parent must reciprocally add the child ID. Specification 003 intentionally rejects a forest where only one side exists.

Portable standard-library filesystem operations do not provide one atomic commit across two independent existing/new JSON files. Calling the operation "atomic" would therefore create a false crash-safety guarantee. At the same time, publishing one side and hoping the second write succeeds would expose an invalid canonical forest after interruption.

The store already reserves `.specgrain/tmp/` as ignored runtime state and retains a zero-runtime-dependency design under ADR-0005.

## Decision

1. Multi-file child authoring is **recoverable and fail-closed**, not advertised as operating-system atomic.
2. Exactly one supported multi-file authoring transaction may be pending per local project, represented by a create-if-absent versioned journal at `.specgrain/tmp/authoring-transaction.json`.
3. The journal records exact parent preimage, intended parent postimage, intended child content, canonical IDs, transaction version, and operation kind. Recovery decisions are made from exact journal/file agreement, never inference from partial semantic similarity.
4. Ordinary store loads and authoring writes refuse a pending journal. Read-oriented operations do not silently mutate state to repair it.
5. A child-authoring writer validates the existing forest and complete proposed forest before journal creation, then writes in this order: journal, child create-if-absent, exact-preimage parent replacement, exact post-state confirmation, journal removal.
6. Parent replacement uses a same-directory temporary file and `os.replace` for atomic replacement of that **single** file. This does not make the two-file transaction atomic.
7. Explicit recovery recognizes only:
   - parent preimage + absent child: clear journal;
   - parent preimage + exact intended child: remove that transaction-created child, then clear journal;
   - parent postimage + exact intended child: preserve canonical files and clear stale journal.
8. Any different parent/child state is ambiguous. Recovery leaves the journal and canonical files unchanged and fails closed for manual investigation.
9. A handled implementation failure may attempt the same deterministic rollback classification. If rollback cannot prove a safe state, it leaves the journal for explicit recovery instead of escalating to destructive cleanup.
10. Child authoring in Specification 019 may mutate only a parent currently in state `DRAFT`. `children` participates in the parent's semantic revision, so modifying non-DRAFT parents requires separately shaped editing/lifecycle authority.
11. Supported writer serialization is journal-based. This ADR does not claim cross-process locking against arbitrary non-cooperating manual edits; exact preimage re-checks detect drift where observable before replacement.
12. The transaction/recovery implementation remains standard-library only and must preserve store-v1 canonical SpecNode JSON.

## Consequences

- Interrupted supported child writes are either explicitly rolled back, explicitly finalized, or blocked as ambiguous rather than silently leaving trusted half-state.
- `specgrain recover` is a bounded mutation surface with deterministic semantics, not a general repair tool.
- Existing root-DRAFT creation remains single-file create-if-absent but must refuse to proceed while a multi-file authoring journal is pending.
- Repository checks can report recovery-required state without acquiring mutation authority.
- A future need for stronger multi-writer concurrency, generation-based storage, database transactions, or schema migration requires separate evidence and authority.
- The implementation must test interruption/recovery semantics on the permanent Linux/macOS/Windows CI matrix rather than assuming POSIX-only rename behavior.
