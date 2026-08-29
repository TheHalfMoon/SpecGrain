# Verification — Specification 023 Spec Kit Preset-Compatible Import

**Status:** `IMPLEMENTATION_CHECKPOINT_VERIFIED`  
**Pre-shaping canonical base:** `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`  
**Canonical shaped base:** `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`  
**Implementation checkpoint:** `0d18c523f57da007d946c3ad6ed99bcccaabe784`  
**Checkpoint CI:** `33264209823` — `completed/success`

## Evidence selection

Specification 023 is selected from the post-022 compatibility audit, not from roadmap assumption.

Exact upstream evidence reviewed:

- GitHub Spec Kit `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed release: `v1.0.1` / release `374643230`;
- standard spec template blob: `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean README blob: `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean specify blob: `c15353557aa941b18e811c15aef605c41ff64133`;
- bundled Lean plan blob: `9fbbe4c3713203a363169b9ca4d7f0dedbd0d1e0`;
- bundled Lean tasks blob: `724a7b840074b8e34cf107f2ca37d211745d15be`.

Exact pre-023 SpecGrain evidence reviewed:

- importer blob: `fe68ca91d9bca3b649a80bf7fc4d2942db6a18a0`;
- importer-test blob: `f0664f8d42b86d48a2938f15b64e91418772e90b`;
- Specification 013 and ADR-0013 migration authority.

The reproduced finding is structural: pre-023 `_feature()` required the canonical full-template feature heading, while the official bundled Lean preset explicitly does not require full-template boilerplate. A template-light official artifact could therefore fail before the existing read-only migration report was produced.

## Canonical shaping proof

Documentation-only shaping head:

`e19484f292c7601036e1993e58203554d1267594`

passed exact push CI `33263751909` and exact PR CI `33263768939` across the permanent five-cell matrix. Review state contained no submitted reviews or inline threads; Qodo was billing-blocked and automatic CodeRabbit review was skipped by repository-star policy, and neither was treated as PASS.

PR #41 merged with expected-head protection and produced signature-verified canonical shaping merge:

`99d8ee5bc7ce49c00ae542f3c06f564d05641a70`

with exact parents:

1. `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b` — post-022 canonical base;
2. `e19484f292c7601036e1993e58203554d1267594` — exact shaping head.

Canonical post-shaping CI `33263898618` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. The historical `v0.3.0` tag remained `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

T007 is therefore closed and implementation authority is canonical.

## Implementation behavior

Checkpoint `0d18c523f57da007d946c3ad6ed99bcccaabe784` changes only:

- `src/specgrain/speckit.py`;
- `tests/test_speckit.py`;
- `docs/migration-from-spec-kit.md`.

It is one commit ahead of canonical shaped base `99d8ee5bc7ce49c00ae542f3c06f564d05641a70`, zero behind, with that base as merge base.

The bounded implementation does exactly:

1. preserve canonical `# Feature Specification: <name>` extraction first;
2. when absent, derive identity only from a concrete feature-path parent;
3. emit `FEATURE_NAME_DERIVED_FROM_PATH` for that fallback;
4. keep arbitrary unrecognized prose out of structured story/FR/SC fields;
5. fail closed for a bare top-level template-light `spec.md` and placeholder-like parent identity;
6. preserve legacy task non-promotion, constitution non-adoption, source artifact digest binding, byte/path/UTF-8/symlink safety, and read-only behavior;
7. preserve `SPECKIT_IMPORT_VERSION == 1`.

For direct artifact mappings, the identity source is the already-normalized `spec.md` parent path. For `load_spec_kit_feature`, the explicitly selected feature directory's final component is used solely as the fallback identity path. Existing source-artifact report paths stay unchanged, which preserves existing loader/report compatibility rather than rewriting source identities for already-supported canonical full-template imports.

No Spec Kit preset, hook, extension, bundle, workflow, or command is installed or executed. No upstream runtime dependency, SpecNode creation, lifecycle authority, executor/provider orchestration, verification execution, evidence mutation, concurrency expansion, package-version change, tag, or release mutation is introduced.

## Compatibility lock

The pre-023 canonical full-template fixture remains locked at:

`sha256:678fcc87985902002a9d2bc852196fbffdc59b332740660f1deeaf0d4f58746a`

The checkpoint test asserts the exact same report digest after 023 and also asserts `SPECKIT_IMPORT_VERSION == 1`. Standard full-template imports do not receive the new fallback notice.

Template-light tests prove:

- `specs/search-workspace/spec.md` -> feature identity `search-workspace`;
- `FEATURE_NAME_DERIVED_FROM_PATH` is emitted;
- ordinary Lean-style prose is not promoted into stories, FR items, or SC items;
- top-level `spec.md` without canonical heading fails for lack of concrete path identity;
- placeholder-like parent identity fails closed;
- filesystem loader fallback uses the explicitly selected feature directory identity.

## Checkpoint verification

Push CI `33264209823` ran on exact checkpoint `0d18c523f57da007d946c3ad6ed99bcccaabe784` and completed `success` across the permanent five-cell matrix.

Ubuntu/Python 3.11 recorded:

- Ruff `src` — PASS;
- Ruff `tests` — PASS;
- Ruff `examples` — PASS;
- editable install with `--no-deps` — PASS;
- full regression — `578 passed`;
- tracked-tree cleanliness — PASS;
- compileall — PASS;
- source CLI smoke — PASS;
- package build — PASS;
- built-wheel reinstall with `--no-deps` — PASS;
- installed CLI smoke — PASS.

The same workflow gates completed successfully across Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11.

## Remaining product gates

The implementation checkpoint is verified, but Specification 023 is not product-merged or closed.

Remaining gates:

1. reconcile tasks/current/master-plan/roadmap against this exact evidence;
2. verify the exact shaped-base-to-final-head diff contains only authorized 023 scope;
3. open the implementation PR from canonical shaped base;
4. prove push and PR permanent five-cell CI on the exact final PR head;
5. recheck comments, reviews, threads, mergeability, and review-system availability without treating unavailable systems as PASS;
6. merge only with expected-head protection;
7. prove canonical product merge parentage, post-product five-cell CI, and historical `v0.3.0` preservation;
8. perform documentation-only closeout and final canonical verification.
