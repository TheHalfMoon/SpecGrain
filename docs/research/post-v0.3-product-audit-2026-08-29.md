# Post-v0.3 Product Audit — 2026-08-29

**Audit source revision:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Latest published release:** `v0.3.0`, GitHub Release `378962445`

## Purpose

This audit re-evaluates the smallest defensible product frontier after Specification 020 product delivery and first publication of v0.3.0. It is evidence for later shaping only. It does not authorize a successor specification or any deferred product, lifecycle, execution, distribution, hosted, or benchmark scope.

## Live repository and adoption snapshot

At audit time:

- canonical product `main` is `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- canonical post-merge CI run `33249920673` succeeded across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11;
- Release workflow `33249956337`, job `99093825183`, published new `v0.3.0` from that exact canonical product revision;
- live `v0.3.0` tag targets exact product revision `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- GitHub Release `378962445` is public, non-draft, and non-prerelease;
- the v0.3.0 wheel and source distribution are the exact two expected release assets;
- historical v0.1.0 and v0.2.0 tags/releases/assets remain unchanged;
- GitHub reports zero open issues, zero stars, and zero forks;
- both v0.3.0 release assets report zero downloads immediately after publication;
- the repository is still less than two days old.

The popularity and download counts are an absence of adoption evidence, not evidence of product failure.

## Distribution discontinuity closed

The product gap that shaped Specification 020 no longer exists.

Published v0.3.0 now exposes the already-canonical native path:

```text
init -> draft root -> draft child -> check
                       |
                       +-> recover only for an exact supported pending authoring transaction
```

The latest public versioned release and canonical `main` are aligned for:

- root DRAFT authoring;
- child DRAFT authoring under an existing DRAFT parent;
- reciprocal refinement validation;
- explicit supported authoring-transaction recovery;
- fail-closed ambiguous transaction handling.

No new product behavior was introduced by Specification 020 itself.

## Candidate frontier comparison

| Candidate | Evidence now | Scope/risk | Decision |
| --- | --- | --- | --- |
| Broad lifecycle-aware recursive `refine` / automatic progression | No user request, bug report, adoption signal, or governance requirement demonstrates need | High: expands mutation and transition authority across protected lifecycle states | **Defer** |
| Generic DRAFT editing / protected lifecycle mutation | No observed demand; current authoring path is bounded and functional | Medium/high: needs a separate mutation, authorization, and recovery contract | **Defer** |
| Stronger multi-writer authoring/recovery concurrency | Existing contract documents its scoped concurrency boundary; no collision report or concurrent-writer evidence exists | Medium: locking/serialization semantics and cross-platform recovery risk | **Defer** |
| WorkPacket/executor orchestration CLI | Internal contracts exist, but no evidence that native execution orchestration is the next adoption blocker | High: materially expands execution authority and agent/provider boundary | **Defer** |
| PyPI or broader registry distribution | GitHub tag/archive/release installation works; no adoption signal identifies registry absence as a blocker | Medium/external: publishing identity, credentials/trusted publishing, recovery and governance | **Defer** |
| Empirical benchmark superiority claim | No controlled public multi-arm dataset exists | High evidence risk | **Defer** |
| Hosted service, provider integration, enterprise/account surfaces | No adoption or operational evidence justifies them | Very high and category-expanding | **Premature** |

## Decision

**No evidence-supported successor specification is selected at this time.**

The smallest defensible next action is observation, not another product mutation. SpecGrain has completed its initial v0.1 program and the evidence-shaped 017–020 sequence, with current recursive DRAFT authoring/recovery behavior now available in the latest versioned GitHub Release.

A later Specification 021 may be shaped only from fresh evidence such as:

- concrete user/adoption friction;
- a reproducible defect or security finding;
- a demonstrated authoring/recovery limitation;
- controlled benchmark data;
- a clearly bounded interoperability/distribution blocker;
- a new governance requirement that cannot be satisfied within the current contract.

The absence of a selected successor is intentional progressive refinement, not abandonment. Creating lifecycle, execution, hosting, registry, or benchmark scope merely to keep a roadmap moving would violate the repository's evidence-shaped post-v0.1 rules.

## Residual risks and observations

- Repository adoption evidence is currently too sparse to distinguish onboarding, distribution, workflow, or category-fit friction.
- GitHub branch protection remains disabled; expected-head merges continue to provide repository-level race protection for canonical merges but are not a substitute for native branch rules.
- GitHub Release API reports `immutable:false`; release immutability remains a repository contract enforced by workflow/governance rather than the platform immutable-release feature.
- Native child-authoring recovery is deliberately scoped and does not claim global serialization across arbitrary concurrent writers.
- No empirical comparative benchmark winner can be claimed without a reproducible controlled dataset.

These residuals are recorded for future evidence collection. None currently supplies enough evidence to authorize a new specification.
