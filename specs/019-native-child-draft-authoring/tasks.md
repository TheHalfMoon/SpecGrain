# Tasks 019 — Native Child-DRAFT Authoring

## Shaping

- [x] T001 Re-read exact canonical `main`, repository instructions, constitution, execution master plan, roadmap, post-v0.2 audit, relevant store/refinement/lifecycle contracts, live release truth, Actions, PRs, and issues.
- [x] T002 Reconcile Specification 018 as `CLOSED_CANONICAL` from closeout merge `c5282caa29fbfeb8c118755766b6a7b8a49d2781`, post-closeout CI `33246162550`, and no-mutation release verification `33246212598`.
- [x] T003 Select DRAFT-parent child authoring as the smallest recursive product gap and split it from broad lifecycle-aware refinement.
- [x] T004 Define the recoverable multi-file transaction contract, explicit recovery boundary, exclusions, acceptance gates, risks, and expected change surface.
- [x] T005 Merge the exact documentation-only shaping chain with expected-head protection, re-read canonical `main`, and prove canonical shaping CI `33246611384` on merge `e10cce6b11cbe4724881936858d7721baa938667`.

## Recoverable transaction foundation

- [x] T006 Add versioned pending-journal detection and explicit recovery primitives without read-time mutation.
- [x] T007 Add exact parent preimage replacement, child create-if-absent sequencing, handled rollback, and fail-closed ambiguous recovery.

## Child-DRAFT API and CLI

- [x] T008 Add the public DRAFT-parent child-authoring API with deterministic ID allocation, reciprocal parent/child construction, and full proposed-forest validation.
- [x] T009 Extend `specgrain draft` with `--parent` while preserving root behavior; add deterministic `specgrain recover` text/JSON surfaces.
- [x] T010 Update README, architecture, and Unreleased changelog truthfully without lifecycle/release overclaim.

## Verification

- [x] T011 Add API coverage for normal/nested child creation, non-DRAFT rejection, invalid parent/forest, journal blocking, recovery phases, and ambiguous-state refusal.
- [x] T012 Add CLI coverage for root compatibility, child text/JSON, recovery text/JSON, errors, and internal-error redaction.
- [x] T013 Run exact regression, Ruff, compileall, CLI help parity, package build/install, and permanent cross-platform CI on product head `994f40f84ad3696b4037ea05eaec746c19bb473f`; run `33247361906` succeeded across all five cells and Ubuntu/Python 3.11 recorded `554 passed`.
- [x] T014 Review exact product head `994f40f84ad3696b4037ea05eaec746c19bb473f` for lifecycle authority, semantic overwrite, journal/recovery safety, unsupported atomicity claims, dependency creep, and unrelated scope; record findings/repairs in `review.md`.

## Product PR and canonical closeout

- [x] T015 Open bounded implementation PR #27 from exact canonical shaping merge `e10cce6b11cbe4724881936858d7721baa938667` and resolve every material product/verification finding forward through reviewed product head `994f40f84ad3696b4037ea05eaec746c19bb473f`.
- [x] T016 Merge PR #27 with expected-head protection at exact final head `53cd8482b727d4f61bfafbea6ed363e4e8783d52`; verify canonical product merge `d6727b6c5cdafcf6265b6d999418c0fe853249a7`, post-merge CI `33248014390`, and no-mutation Release run `33248070688`.
- [x] T017 Record exact implementation/review/merge/release-preservation evidence and run fresh `docs/research/post-019-product-audit-2026-08-29.md` from exact product source `d6727b6...`.
- [ ] T018 Close 019 through this documentation-only exact-head PR, expected-head merge, post-closeout canonical CI, and any triggered historical-release no-mutation verification before claiming `CLOSED_CANONICAL`.
