# Verification — Specification 023 Spec Kit Preset-Compatible Import

**Status:** `SHAPING_CANDIDATE`  
**Shaping base:** `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`  
**Implementation authority:** not yet canonical

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

Exact SpecGrain evidence reviewed:

- canonical base: `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`;
- importer blob: `fe68ca91d9bca3b649a80bf7fc4d2942db6a18a0`;
- importer-test blob: `f0664f8d42b86d48a2938f15b64e91418772e90b`;
- Specification 013 and ADR-0013 migration authority.

The reproduced finding is structural: current `_feature()` requires the canonical full-template feature heading, while the official bundled Lean preset explicitly does not require full-template boilerplate. A template-light official artifact can therefore fail before the existing read-only migration report is produced.

## Shaping verification requirements

Before implementation begins, live GitHub evidence must prove:

1. this shaping change is documentation/governance/research only;
2. its exact head is based on canonical `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b` with no unrelated commits;
3. permanent five-cell CI succeeds on the exact shaping head;
4. exact diff, review comments/threads, mergeability, and review-system availability are rechecked;
5. the shaping PR merges with expected-head protection;
6. resulting canonical `main` passes permanent five-cell CI;
7. historical `v0.3.0` tag/release/assets remain unchanged.

Only then may T007 close and implementation begin.

## Planned product verification

The implementation candidate must prove:

- existing canonical full-template fixture produces an unchanged report dictionary and digest;
- `SPECKIT_IMPORT_VERSION` remains `1`;
- template-light source under a concrete feature directory receives exact path-derived identity plus `FEATURE_NAME_DERIVED_FROM_PATH`;
- a bare top-level template-light `spec.md` fails closed;
- no arbitrary prose becomes invented structured semantics;
- all current source/path/role/size/UTF-8/symlink/duplicate safety tests remain green;
- import remains read-only and tasks/constitution remain non-authoritative;
- no runtime dependency or upstream command execution is introduced;
- full permanent verification succeeds on the exact product head.

## Current conclusion

`SHAPED` is a candidate state only. Specification 023 is not yet authorized for implementation because the shaping merge and canonical post-shaping CI do not yet exist.
