# Review — Specification 026 Supported Mutation Cross-Writer Coordination

**Status:** `CLOSEOUT_CANDIDATE`

## Review conclusion

The canonical Specification 026 shaping authority and product implementation remain consistent with the bounded selection evidence and ADR-0021.

The delivered change coordinates only existing supported pre-Grain persistence and native child authoring through one project-scoped non-blocking advisory lock while preserving the existing child-authoring journal as the separate crash/recovery mechanism.

## Authority review

Fresh post-025 observation on exact canonical baseline `1931d5a90ded5f7b2d4f5ea0f0ccffa03e2affc1` reproduced `SUPPORTED_CHILD_PRE_GRAIN_CROSS_WRITER_PARTIAL_MUTATION` on qualifying observation head `3b557f91ec80c147b30f797198d736c2b6b42518` with CI `33441481985` successful across all five permanent cells.

Shaping PR #59 used final head `51079a25cdd0f90a9af1cc34ae7577c72ecdf2d6`, passed push CI `33441902147` and PR CI `33442057984`, merged as `d27e000728823e93d2fce9ecd669629a839bfdb3`, and canonical post-shaping CI `33442261877` completed `success` across all five permanent cells. Product implementation was therefore genuinely authorized before work began.

## Implementation review

Final product diff from canonical shaping merge `d27e000728823e93d2fce9ecd669629a839bfdb3` to exact implementation head `24728cd52b2daef2c83c5b83f084421b8096a11f` changed exactly:

- `src/specgrain/store.py`;
- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

The lower-level store module now owns the private shared advisory-lock helper so both writer families use the identical callable without a circular import. `pregrain.py::_persist` retains its complete critical section through exact postimage/project validation. `create_child_draft_spec` acquires the same lock before journal creation and holds it through normal completion or handled recovery.

The implementation preserves the existing lock anchor `.specgrain/tmp/pregrain-mutation.lock`, standard-library Unix/Windows primitives, unsafe-anchor rejection, descriptor/process ownership semantics, non-blocking contention behavior, zero runtime dependencies, `AUTHORING_TRANSACTION_VERSION`, journal schema, recovery classifications, child-ID behavior, lifecycle rules, and explicit recovery semantics.

## Acceptance review

Corrected-invariant tests prove both contention directions:

- pre-Grain ownership makes a competing supported child writer fail before journal/child/parent side effects while the pre-Grain writer completes and the project remains valid;
- child-authoring ownership makes a competing supported pre-Grain writer fail before target mutation while child authoring completes and the project remains valid.

Existing Specification 025 serialization/lifetime/unsafe-anchor/read-only regression coverage and existing child-authoring recovery coverage remain part of the full regression suite.

Final exact-head push CI `33443061640`, PR #60 CI `33443161567`, and canonical post-product CI `33485603844` all completed `success` across Ubuntu/Python 3.11, Ubuntu/Python 3.12, Ubuntu/Python 3.13, macOS/Python 3.11, and Windows/Python 3.11.

## Review-system disposition

At the PR #60 merge gate:

- no submitted reviews were present;
- no inline review threads were present;
- Qodo was billing-blocked;
- automatic CodeRabbit review was skipped because repository star policy was not met;
- Cubic was neutral/descriptive because the monthly AI review line limit was reached.

None of these unavailable, skipped, neutral, or descriptive systems was treated as independent approval or PASS.

## Merge review

PR #60 exact head was `24728cd52b2daef2c83c5b83f084421b8096a11f` on exact base `d27e000728823e93d2fce9ecd669629a839bfdb3`. The PR merged as signed canonical merge `69c6cc8a2cbc3b666dbda0150f65a9440acd0c0b` with parents `d27e000728823e93d2fce9ecd669629a839bfdb3` and `24728cd52b2daef2c83c5b83f084421b8096a11f`.

Canonical post-product CI `33485603844` completed `success` across all five permanent cells.

## Residual risk review

Residual boundaries remain explicit and acceptable. Non-cooperating external writers are not coordinated; the advisory lock is cooperative rather than a universal filesystem transaction primitive; the child-authoring journal remains a separate recovery mechanism; no blocking/retry/lease/distributed guarantee is claimed; no release, hosted, lifecycle, execution/provider, verification/evidence, or benchmark authority was added.

## Historical release review

Historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with wheel digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817` and source digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835` unchanged.

## Recommendation

Proceed with the documentation/governance/evidence-only closeout PR. Do not mark Specification 026 `CLOSED_CANONICAL` until that exact closeout head is qualified, merged with expected-head protection, and canonical post-closeout CI succeeds across all five permanent cells.
