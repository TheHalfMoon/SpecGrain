# SpecGrainBench Experiment 001 — Pre-registration

**Case ID:** `SGB-EXP-001`  
**Status:** `PRE_REGISTERED_AWAITING_RUNNER_AND_MODEL_LOCK`  
**Purpose:** Evidence gathering only. This experiment does not select or authorize Specification 024.

## Research question

Does the current SpecGrain method reduce unauthorized or unnecessary product changes on a small real brownfield bug fix without reducing correctness, compared with a prompt-only baseline and current GitHub Spec Kit?

Secondary observation: does the current SpecGrain `GRAIN -> external implementation` boundary create measurable handoff friction or evidence loss?

No superiority claim is authorized by this pre-registration.

## Immutable brownfield baseline

- Repository: `more-itertools/more-itertools`
- Baseline revision: `ed86a1528aa015f219f8d3385ea2ebd3f63a5212`
- License: MIT
- Language/runtime: Python, project requires Python `>=3.10`
- Experiment runtime target before final runner lock: Python 3.11 on Ubuntu 24.04

At the pinned baseline, `more_itertools.sliced` constructs slices from `count(0, n)` without a negative-size guard. A negative `n` therefore produces an incorrect truncated slice instead of the required domain error. This behavior is reproduced from the pinned source, not inferred from an external review.

## Common agent-visible task

The exact agent-visible task is stored in `task.md`.

Task commitment:

`sha256:59ee44939820af0c29da7fa9b271bd798f2d2fc8a1e5e460612727f84a39fe23`

The same task bytes MUST be supplied to every benchmark cell.

## Hidden acceptance oracle commitment

The acceptance scorer is intentionally not stored in this public repository before execution.

Oracle commitment:

`sha256:139e6344de40568d6a94b0f3da11c56a0d4268c1c5a7c33ea3413eafc4c0f4fa`

Scorer revision:

`sgbench-exp001-scorer-v1`

The committed scorer checks the requested negative-size behavior plus preservation of zero-size, positive-size, and strict-mode behavior. The scorer MUST remain outside the agent workspace and unreadable during every cell. It may be revealed only after all nine raw run records are frozen.

A scorer whose bytes do not match the commitment above invalidates the experiment.

## Regression and style gates

The evaluator will run, outside the agent context:

```text
python -m unittest
ruff format --check .
ruff check more_itertools tests
```

These commands are derived from the pinned repository's existing Makefile/test configuration.

## Product change surface

Allowed product paths:

- `more_itertools/more.py`
- `tests/test_more.py`

Any other changed product path fails the scope oracle unless the run is explicitly retained as a failed/blocked cell.

Method-owned generated artifacts are not counted as product-scope violations. They MUST be recorded separately as method artifact footprint and MUST NOT be silently discarded from raw evidence.

## Arms

### `prompt-only`

- Receive only the common task and brownfield repository.
- No Spec Kit or SpecGrain initialization or method artifacts.
- Normal repository inspection, editing, and tests are allowed.

Pre-runner method commitment:

`sha256:ea940f324bd6b934362110cb32babfb044dbccf94a2d6be668bae231f32f75a0`

### `spec-kit`

Pinned upstream:

`github/spec-kit@51e52be6c3b26fed3ff5424c671f4a559519a759`

Use the official brownfield initialization model and the official workflow:

```text
constitution
-> specify
-> clarify
-> plan
-> tasks
-> analyze
-> implement
-> converge
```

The exact integration key is runner-dependent and MUST be frozen in the final runner lock before the first cell starts. No optional extension is enabled by this pre-registration.

Pre-runner method commitment:

`sha256:e77fdbd9c1687690cfa10216399ae61b393a10755672b3be02dadd015aa10ef1`

### `specgrain`

Pinned method:

`TheHalfMoon/SpecGrain@3b07063fbc466ee051687c488ea93b95814dc7fb`

Use current native preparation through `GRAIN`:

```text
scan
-> init
-> draft
-> shape
-> refine
-> grain
-> check
-> next
-> external implementation
-> repository verification
```

The run MUST NOT claim or mutate `READY`, `RUNNING`, `VERIFYING`, `VERIFIED`, or `CONTROLLED` through SpecGrain because that authority is not part of the current native CLI frontier.

The transition from GRAIN to ordinary runner editing is intentionally preserved as an observed handoff rather than hidden by benchmark glue.

Pre-runner method commitment:

`sha256:0ecf30c2f2d5157f4e5643734b3401e56695153891dce12d5db5ed2f2d449258`

## Repetitions and cells

Three repetitions per arm:

- 3 `prompt-only`
- 3 `spec-kit`
- 3 `specgrain`

Total expected cells: **9**.

Every cell requires unique:

- run ID;
- workspace ID;
- context/session ID.

Missing cells, duplicate cells, workspace/context reuse, repository mismatch, method mismatch, model mismatch, scorer mismatch, or scorer visibility invalidate the comparative report under SpecGrainBench v1.

Failed and blocked cells remain in the dataset.

## Isolation controls

Before an agent context starts:

1. construct a fresh source archive from the exact baseline revision;
2. remove `.git` and all future repository history from the agent workspace;
3. install project and method dependencies outside the timed/agent context;
4. disable network access for the agent run;
5. ensure the hidden scorer is not mounted or readable;
6. ensure no previous cell's generated files, caches, conversations, workspaces, or IDs are reused;
7. sanitize global agent configuration so only the selected arm's method integration is exposed.

A prompt-only cell that can see a Spec Kit/SpecGrain skill, or a method cell that can see another arm's state, is contaminated.

## Metrics

Required SpecGrainBench v1 fields:

- acceptance pass;
- regression pass;
- scope pass;
- first-pass verification;
- run status;
- changed files;
- changed lines;
- retries;
- human interventions;
- rework units;
- input/output tokens when available;
- duration when comparable.

Experiment-specific raw evidence should additionally retain:

- product diff;
- method artifact diff;
- number of method commands/steps;
- handoff count;
- whether implementation required manual glue after method preparation;
- test commands actually run by the agent;
- final evaluator output.

Repository outcome metrics are primary. Generated prose volume is not a correctness proxy.

## Anti-leak rule

Agents MUST NOT receive:

- the hidden scorer source;
- a post-baseline Git history;
- network access;
- a gold patch or gold commit;
- another arm's artifacts or conversation;
- this pre-registration document as extra context beyond the common task and the selected method configuration.

If a runner cannot enforce these controls, the corresponding cells are `BLOCKED`, not improvised.

## Final lock still required

No benchmark cell may start until a separate final runner lock records:

- exact model/provider identity and configuration digest;
- exact coding-agent/runner identity and version;
- exact Spec Kit integration key/dialect;
- exact runner/container image digest;
- exact installed Spec Kit artifact digest;
- exact installed SpecGrain artifact digest;
- final three method configuration digests;
- final environment digest;
- final `BenchmarkPlan.plan_digest`.

Until that lock exists, status remains:

`PRE_REGISTERED_AWAITING_RUNNER_AND_MODEL_LOCK`

This is a methodological blocker only. It is not a SpecGrain product failure and does not justify Specification 024 by itself.

## Decision rule after execution

After all cells are frozen and the hidden scorer is revealed:

- run deterministic SpecGrainBench preflight;
- publish every completed, failed, blocked, tied, and invalidated cell;
- do not auto-declare a winner;
- compare correctness before efficiency or scope claims;
- reproduce any claimed handoff defect from raw evidence;
- shape a successor only if the dataset demonstrates a bounded product problem against live canonical SpecGrain truth.

Possible result:

- `NO NEW SPECIFICATION JUSTIFIED`
- `OBSERVATION SHOULD CONTINUE`
- `BOUNDED SUCCESSOR JUSTIFIED`

No one of these outcomes is preselected.
