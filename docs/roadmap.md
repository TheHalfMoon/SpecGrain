# Roadmap

The roadmap is progressive and evidence-shaped. Only selected work receives implementation detail.

## Current frontier

Specifications 000–026 are `CLOSED_CANONICAL`.

Specification 027 — Execution Attempt Identity Contract has completed product implementation and canonical post-product qualification. A documentation-only closeout package is now the active unit.

```text
product_merge = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
post_product_ci = 34164674946 = completed/success across all five permanent cells
closeout_state = CLOSEOUT_CANDIDATE
```

After exact closeout merge + five-cell canonical post-closeout CI + release preservation + authority reread, Specification 027 is `CLOSED_CANONICAL` and the roadmap returns to `POST_027_OBSERVATION` with no preselected Specification 028.

## Completed/active program

- 000–026: `CLOSED_CANONICAL`.
- 027 — Execution Attempt Identity Contract: product complete; closeout candidate active.

## Specification 027 delivered outcome

A separate deterministic portable occurrence-identity contract now lets different execution attempts bind identical packet/request/result content identities without altering existing v1 schemas or granting lifecycle/verification authority.

Exact product surface:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

## Deferred by evidence boundary

No current authority exists for attempt persistence, automatic attempt-ID generation, execution/provider invocation, agent orchestration, lifecycle mutation, retry scheduling, verification/evidence mutation, hidden reasoning/evaluation access, fixed donor stage graphs, networking/hosted scope, runtime dependencies, or release publication.

These are not backlog promises. They may become candidates only if future fresh reproducible evidence selects a concrete bounded gap.

## Historical release

`v0.3.0` remains unchanged at source `70dd66aba0e68ae710e6ef12605ed153d107bab4`, Release `378962445`, with recorded wheel/source asset digests unchanged.

## Continuation rule

Do not create work merely to continue activity. After Specification 027 closure, perform bounded observation against live canonical truth and shape no successor without fresh selection evidence.