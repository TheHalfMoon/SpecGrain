# Closeout 027 — Execution Attempt Identity Contract

## Closeout state

`CLOSEOUT_CANDIDATE`

The selected product gap has been implemented and canonically post-product-qualified. This documentation-only package records final evidence and reconciles program authority.

Specification 027 becomes `CLOSED_CANONICAL` without a recursive follow-up documentation PR when all of these live conditions are true:

1. this exact closeout package is merged with expected-head protection;
2. the merge commit contains only the qualified documentation/governance/evidence closeout scope;
3. canonical post-closeout CI succeeds across all five permanent cells;
4. historical `v0.3.0` remains unchanged;
5. canonical authority is reread after the merge.

Once those conditions hold, return directly to `POST_027_OBSERVATION`. Do not create another docs-only PR merely to write the merge SHA, CI run ID, or flip a textual task checkbox.

## Product delivered

Specification 027 adds a portable deterministic occurrence-identity contract:

```text
ExecutionAttemptRecord
```

It lets two separate attempts bind the same exact packet/request/result content identities while remaining distinguishable through caller-supplied canonical `attempt_id` and derived `attempt_digest`.

The implementation preserves existing v1 WorkPacket, AgentRequest, and ExecutionResult content identities rather than contaminating those hashes with occurrence data.

## Exact canonical product

```text
product_merge = 08f3ca9e6bb46386e23a196339d7157362b2a9b6
product_tree = 020fb6b348495893693bf169a155ddb585360727
post_product_ci = 34164674946 = completed/success across all five permanent cells
```

Exact product surface:

```text
src/specgrain/attempt.py
src/specgrain/__init__.py
tests/test_attempt.py
```

## Review and trust statement

No unavailable, skipped, neutral, billing-blocked, or descriptive review system was treated as approval. The product merge gate had no submitted reviews and no inline review threads. Exact-head push/PR/post-merge CI and bounded diff evidence provide the machine-verifiable qualification recorded in `verification.md`; they do not create external reviewer approval that did not exist.

## Deferred ownership

The following remain intentionally unimplemented and require fresh reproducible evidence before any successor specification may select them:

- durable `.specgrain` attempt persistence or append ledgers;
- attempt writer concurrency/recovery;
- automatic attempt ID generation;
- executor/subprocess/provider/model invocation;
- orchestration and automatic retry scheduling;
- lifecycle mutation;
- verification/evidence mutation;
- hidden reasoning or hidden evaluation material;
- fixed donor workflow stages;
- networking/hosted scope;
- runtime dependencies;
- release publication.

## Release preservation

`v0.3.0` remains the latest published historical release at source `70dd66aba0e68ae710e6ef12605ed153d107bab4` with its previously recorded wheel/source asset digests unchanged.

## Final continuation rule

After closeout conditions are realized:

```text
SPECIFICATION_027 = CLOSED_CANONICAL
ACTIVE_PRODUCT_SPECIFICATION = none
PROGRAM_STATE = POST_027_OBSERVATION
```

No Specification 028 exists or is authorized by this closeout. A successor may be shaped only from fresh reproducible live evidence against the then-canonical repository.