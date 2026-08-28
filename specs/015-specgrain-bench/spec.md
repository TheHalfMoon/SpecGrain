# Specification 015 — SpecGrainBench

**Status:** SHAPED

## Outcome

Implement a deterministic benchmark experiment ledger that can validate whether prompt-only, GitHub Spec Kit, and SpecGrain runs are comparable before producing reproducible arm summaries.

## Required initial arms

- `prompt-only`;
- `spec-kit`;
- `specgrain`.

## Core contracts

### Benchmark case

A case binds:

- case ID;
- immutable repository revision;
- task-intent digest;
- acceptance-oracle digest;
- environment digest;
- scorer revision;
- whether scorer fixtures must remain hidden;
- repetition count;
- exact arm method configuration digests;
- exact model/provider configuration digest when model-based comparisons are used.

### Run observation

Each `(case, arm, repetition)` observation records:

- unique run, workspace, and context/session identifiers;
- observed repository/scorer/method/model configuration revisions;
- run status (`completed`, `failed`, `blocked`);
- acceptance, regression, scope, and optional safety outcomes;
- token counts when available;
- duration when comparable;
- retries and human interventions;
- changed file/line counts;
- first-pass verification and rework units;
- whether hidden scorer fixtures were visible;
- failure code when the run did not complete.

### Contamination preflight

The harness MUST fail comparison validity when it detects:

- duplicate or missing benchmark cells;
- shared workspace IDs or context/session IDs across cells;
- baseline repository mismatch;
- scorer revision mismatch;
- arm method configuration mismatch;
- model configuration mismatch where controlled;
- hidden scorer visibility;
- invalid repetition identifiers.

### Reporting

The report MUST retain failed and blocked runs. Summaries use deterministic integer counts/totals and never filter unfavorable outcomes.

The core report MUST NOT automatically declare a winner or superiority claim.

## Out of scope

- launching coding agents, models, containers, or subprocesses;
- provisioning benchmark repositories or credentials;
- hidden-test implementation;
- collecting private prompts or reasoning traces;
- fabricating prompt-only/Spec Kit/SpecGrain outcome data;
- adding post-hoc exclusions to improve results.

## Acceptance

1. Identical plans and observations produce identical canonical JSON and report digests.
2. Initial plans require exactly the three canonical v1 arms.
3. Every expected arm/repetition cell must be present exactly once for a valid comparison.
4. Workspace/context reuse, baseline/config mismatch, and hidden-scorer leakage invalidate the report.
5. Failed/blocked runs remain counted.
6. Summaries expose reproducible outcome/efficiency/process totals without ranking methods.
7. No runtime dependency or execution/network behavior is introduced.
