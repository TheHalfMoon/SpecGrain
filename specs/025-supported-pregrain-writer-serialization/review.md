# Review — Specification 025 Supported Pre-Grain Writer Serialization

**Status:** `CLOSEOUT_CANDIDATE`

## Review conclusion

The canonical Specification 025 product implementation is consistent with the shaped boundary and ADR-0020.

The delivered change is intentionally narrow: it serializes only the existing supported pre-Grain persistence critical section and retains all prior deterministic drift, lifecycle, readiness, dependency, and postimage defenses.

## Authority review

Canonical shaping authority was established by PR #54 and post-shaping CI `33432447491`.

Final product diff from shaping merge `e394ab0c7efabbfade91b64bcdf9a11c8146f469` to final implementation head `bb1fa1406ef9dab6a65c1721378025943ba3f6de` changed exactly:

- `src/specgrain/pregrain.py`;
- `tests/test_pregrain_serialization.py`.

This is within the expected Specification 025 surface. The focused additional test module is explicitly permitted by the plan for subprocess/platform lock proof.

No CLI, public schema, lifecycle module, child-authoring journal, workflow, dependency, package metadata, release, benchmark, provider, hosted, or unrelated product contract path changed.

## Implementation review

The implementation satisfies the architectural decision because:

- all existing supported shape/refine/grain writes converge on `_persist`;
- `_persist` acquires one project-scoped advisory lock for the complete validation/read/replace/postimage transaction;
- contention is non-blocking and fails closed immediately;
- Unix-family and Windows locking use only standard-library platform primitives;
- anchor existence is not interpreted as ownership, stale state, or recovery state;
- ownership is descriptor/process scoped and released in `finally`;
- unsafe symlink/non-regular anchors are rejected;
- read-only loading remains outside the lock;
- the previous exact-preimage and postimage protections remain additive rather than replaced.

## Acceptance review

The focused suite directly covers the reproduced defect and required recovery/lifetime boundaries:

- the competing supported writer no longer also succeeds;
- the intended lock owner commits the expected semantic revision;
- stale callers still fail the existing preimage check;
- shape/refine/grain share one contention boundary;
- sequential use remains valid;
- success/failure/process-exit ownership release is proven;
- persistent anchor reuse is proven;
- read-only behavior remains unlocked;
- unsafe anchors fail closed.

Final exact-head push CI `33434286534` and PR CI `33434757539` both completed `success` across all five permanent cells. The canonical post-product CI `33434910548` also completed `success` across all five permanent cells.

## Review-system disposition

At the PR #55 merge gate:

- no submitted reviews were present;
- no inline review threads were present;
- Qodo was billing-blocked;
- automatic CodeRabbit review was skipped by repository-star policy;
- Cubic provided descriptive summary text only.

No unavailable, skipped, or descriptive review system was treated as independent approval or PASS.

## Residual risk review

Residual boundaries are explicit and acceptable for this specification:

- arbitrary external/manual writers are not coordinated;
- the implementation is not a universal filesystem compare-and-swap primitive;
- advisory-lock semantics are intentionally cooperative among supported SpecGrain pre-Grain writers;
- child-authoring journal/recovery remains separately governed by ADR-0018;
- no blocking/retry/lease/stale-owner policy exists;
- distributed/network filesystem guarantees are not claimed.

These are preserved residuals, not hidden completion claims.

## Historical release review

After canonical product merge `5e3966fb0db3d8971b5abe19106949001ed55ba9`, historical `v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with the existing wheel/source asset IDs and digests unchanged.

## Closeout recommendation

Specification 025 product work is ready for documentation-only closeout. `CLOSED_CANONICAL` must not be published until closeout merge, permanent post-closeout CI, and final evidence reconciliation are proven.