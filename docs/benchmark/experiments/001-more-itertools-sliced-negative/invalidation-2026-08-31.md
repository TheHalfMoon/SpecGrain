# SGB-EXP-001 Experiment Invalidation — 2026-08-31

**Case:** `SGB-EXP-001`  
**Experiment status:** `INVALIDATED_ORACLE_REVEALED_PRE_FREEZE`  
**Purpose of this record:** preserve experiment-validity evidence only.  
**Product implication:** none.  
**Specification 024 authority:** not created or implied.

## 1. Summary

SGB-EXP-001 cannot produce a valid comparative benchmark result under its existing pre-registration.

Two independent validity failures occurred before a valid nine-cell dataset existed:

1. Attempt 002 was contaminated before Cell 2 because its first fresh cell observed a workspace baseline that did not match the pinned source identity.
2. During subsequent operator-side recovery work, hidden scorer source content was unexpectedly surfaced to the operator context before all nine raw run records were frozen.

The second event is terminal for this pre-registration because the hidden acceptance scorer was committed to remain unrevealed until all nine raw run records were frozen.

No scorer source bytes are reproduced in this repository record.

## 2. Attempt 002 preserved status

```text
attempt_id = SGB-EXP-001-ATTEMPT-002
status = INVALID_CONTAMINATED
invalidated_before_cell = 2
cell_1_status = blocked
cell_1_failure_code = WORKSPACE_BASELINE_MISMATCH
```

Attempt 002 MUST NOT be resumed or counted as a valid benchmark attempt.

## 3. Canonical baseline identities

The experiment's locked brownfield identity remains unchanged:

```text
repository_revision = ed86a1528aa015f219f8d3385ea2ebd3f63a5212
baseline_archive_digest = sha256:6bdf91b309f86e4ac755f7ba33504aa7314567b69978ba71e5f0b62e33bbfbc1
more_itertools/more.py blob = 5607346368e6eb903eac3d50aad9ef65eacd0b01
tests/test_more.py blob = 1d2894b4c0dd7ff28f2ff041873f5198dc915699
```

At the pinned source revision, the relevant baseline function does not contain the requested explicit negative-size guard. This identity fact remains useful historical evidence for understanding the Attempt 002 contamination event.

## 4. Harness qualification finding

After Attempt 002 was invalidated, work shifted to execution-harness qualification before any Attempt 003 creation.

The frozen runner package was internally rechecked without modifying it. Its recorded identities include:

```text
runner = Claude Code
runner_version = 2.1.251
provider = anthropic
model = claude-fable-5
runner_image_digest = sha256:d410f9a22b896edb5edeaa20ccc920f879c00a78b67f089abb647adf91e68bf8
network_mode = none
benchmark_plan_digest = sha256:24927fb6957ce6f53311fe8ae3eb3b00772ce009f2e738ea75daedef11a3f820
```

The package records that agent shell commands are routed into the Docker workspace, but the package does not contain the executable launcher or an exact launcher command that implements that routing. The currently connected executor also does not have access to the original Windows/Docker/Claude execution host.

Therefore execution-harness qualification could not be completed from direct evidence and Attempt 003 was never created.

This harness reproducibility problem is preserved as a methodological finding, but it is no longer the active gate for SGB-EXP-001 because the later oracle-reveal event independently invalidated the experiment.

## 5. Hidden-oracle reveal incident

During operator-side recovery work for the missing frozen harness launcher, a broad search over private working-library artifacts unexpectedly returned content from the committed hidden scorer source.

The scorer source was not intentionally opened, requested, copied into the repository, supplied to a benchmark agent, or used to execute or solve a benchmark cell. Nevertheless, scorer source content became visible to the operator context before all nine raw run records were frozen.

The pre-registration states that the scorer may be revealed only after all nine raw run records are frozen. That condition is no longer satisfiable for SGB-EXP-001.

Current truth is therefore:

```text
hidden_scorer_revealed = true
all_nine_raw_run_records_frozen_before_reveal = false
```

No scorer implementation details, acceptance cases, source excerpts, or derived solution information are recorded here.

## 6. Canonical consequence

```text
case_id = SGB-EXP-001
experiment_status = INVALIDATED_ORACLE_REVEALED_PRE_FREEZE
attempt_002_status = INVALID_CONTAMINATED
attempt_003_status = NOT_CREATED
benchmark_cells_authorized = false
comparative_report_authorized = false
superiority_claim_authorized = false
```

No additional SGB-EXP-001 benchmark cell may be executed under this pre-registration.

The frozen task commitment, scorer commitment, BenchmarkPlan, runner lock, method configurations, and preregistration MUST remain unchanged as historical artifacts. They MUST NOT be retroactively rewritten to rescue the experiment.

## 7. Evidence boundary

This invalidation record does not:

- reveal the hidden scorer source;
- describe hidden acceptance implementation details;
- solve the benchmark task;
- alter the pinned brownfield baseline;
- alter the frozen runner lock or BenchmarkPlan;
- alter the pre-registration;
- create Attempt 003 IDs or workspaces;
- authorize a successor product specification;
- support any prompt-only, Spec Kit, or SpecGrain superiority claim.

## 8. Future benchmark requirement

Any future comparative execution must be a **newly pre-registered experiment**, not Attempt 003 of SGB-EXP-001.

Before its first benchmark cell, the new experiment must establish at minimum:

1. a new hidden oracle commitment whose source has not been exposed to the operator or benchmark agents;
2. a reproducible execution-harness launcher captured as an exact immutable artifact, not only a prose routing description;
3. file-level baseline attestation for host, container, Python import, and coding-agent file tools;
4. explicit fresh-context isolation evidence for file tools and shell tools;
5. unique run/workspace/context IDs generated only after all preflight gates pass;
6. fail-closed handling for any baseline, routing, context, scorer-visibility, or environment mismatch.

A new experiment remains evidence gathering only. It does not authorize Specification 024 unless a completed reproducible dataset later demonstrates a bounded SpecGrain product gap against live canonical truth.

## 9. Closeout

SGB-EXP-001 is preserved as an invalid empirical attempt and a methodology lesson.

The correct closeout is:

```text
SGB-EXP-001 = INVALIDATED_ORACLE_REVEALED_PRE_FREEZE
NO VALID COMPARATIVE RESULT
NO ATTEMPT 003
NO SUPERIORITY CLAIM
RETURN TO POST_023_OBSERVATION
```
