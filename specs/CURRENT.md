# Current Execution State

**Repository:** `TheHalfMoon/SpecGrain`  
**Canonical branch:** `main`  
**Canonical base before current shaping:** `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`  
**Program status:** `SHAPING_023`  
**Last closed specification:** `specs/022-native-grain-preparation/` — `CLOSED_CANONICAL`  
**Active shaping candidate:** `specs/023-spec-kit-preset-compatible-import/` — `SHAPED` candidate; implementation blocked pending canonical shaping merge  
**Published release:** `v0.3.0`  
**Published release source:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Published release ID:** `378962445`

## Last canonical closed state

Specification 022 is `CLOSED_CANONICAL` and closes exactly the native pre-execution preparation gap:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN
```

Its final implementation candidate `8af20015bd59424c7882b8c8fa7ea4c78e0af2e5` passed exact push CI `33261979828` and PR CI `33261982603`, PR #38 merged as product merge `653cfb64c8885174ea3ea729d1bbb6418613b10d`, and canonical post-product CI `33262123902` succeeded.

Documentation closeout head `7b3b5beed297d024ad897e3b7e4d5376c8c5f24a` passed push CI `33262421052` and PR CI `33262442496`; PR #39 merged as canonical closeout merge `9cd52eb6d1ba6839910ceb973fedf5b3a727cc0a`; post-closeout CI `33262519733` succeeded.

Evidence reconciliation PR #40 then merged as `ff9f640bf0e4de5bdd5bf2af0e11b98d86f6587b`; post-reconciliation CI `33262914956` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11.

The historical `v0.3.0` tag and GitHub Release remain unchanged at `70dd66aba0e68ae710e6ef12605ed153d107bab4` / Release `378962445`. `shape`, `refine`, and `grain` are current-source additions and are not historical v0.3.0 commands.

A bounded concurrent-writer race around exact-preimage validation and atomic replacement remains an explicit post-022 residual; 023 does not select or alter that boundary.

## Post-022 evidence that selected Specification 023

The exact comparison is recorded in:

`docs/research/post-022-spec-kit-1.0-compatibility-audit-2026-08-29.md`

Reviewed upstream GitHub Spec Kit truth:

- exact `main`: `51e52be6c3b26fed3ff5424c671f4a559519a759`;
- latest observed release: `v1.0.1` / Release `374643230`;
- canonical standard spec template blob: `ceb28776215a098e977650ac090c785dcbf53651`;
- bundled Lean preset README blob: `ab17257f96091590d2289699aaf2b114cc05bbbe`;
- bundled Lean specify command blob: `c15353557aa941b18e811c15aef605c41ff64133`.

Current SpecGrain `src/specgrain/speckit.py` requires the exact full-template `# Feature Specification:` heading to obtain feature identity. Current upstream Lean is a bundled official preset that intentionally produces focused Markdown without requiring full-template boilerplate.

The bounded reproduced gap is therefore: a valid official template-light Spec Kit artifact may be rejected before SpecGrain can produce its existing deterministic read-only migration report solely because the canonical full-template heading is absent.

## Specification 023 bounded outcome

Specification 023 proposes only preset-compatible import identity:

- preserve existing canonical full-template parsing exactly;
- when the canonical feature heading is absent, derive feature identity only from the concrete final parent component of the normalized repository-relative `spec.md` path;
- emit `FEATURE_NAME_DERIVED_FROM_PATH` for that fallback;
- keep unrecognized structured semantics unmapped rather than guessed;
- preserve all source safety, digest binding, read-only behavior, legacy-task non-promotion, and constitution non-adoption;
- keep `SPECKIT_IMPORT_VERSION == 1` and preserve existing full-template report/digest output;
- add no runtime dependency and execute no Spec Kit preset/hook/extension/workflow code.

ADR-0020 governs this candidate boundary.

## Current execution gate

Specification 023 implementation is **not yet authorized**.

The only eligible work on this branch is documentation-only shaping. T007 must first prove from live GitHub truth that:

1. the exact shaping head changes only expected research/governance/specification paths;
2. permanent five-cell CI passes on that exact head;
3. reviews/threads/mergeability and review-system availability are rechecked without treating unavailable systems as PASS;
4. the shaping PR merges with expected-head protection;
5. resulting canonical `main` passes permanent five-cell CI;
6. historical `v0.3.0` remains unchanged.

Only after T007 closes may implementation branch `feat/023-spec-kit-preset-compatible-import` begin.

## Explicitly unselected

Specification 023 does not authorize READY mutation, WorkPacket/executor work, verification execution, evidence mutation, stronger locking, release publication, arbitrary Markdown semantic inference, automatic SpecNode creation, Spec Kit preset installation, hooks/extensions/bundles/workflows, or provider/agent orchestration.

An external architectural review, including a Fable review, may contribute additional findings. It remains evidence only and cannot widen 023 without canonical reshaping.
