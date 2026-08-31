# SGB-EXP-001 Execution Harness Qualification

**Purpose:** operator-only qualification before Attempt 003.  
**Benchmark cells executed by this procedure:** none.  
**Hidden scorer access:** prohibited.  
**Frozen runner lock / preregistration mutation:** prohibited.

## Why this qualification exists

Attempt 002 is `INVALID_CONTAMINATED` before Cell 2 because its first fresh cell observed a negative-size guard that is not present in the pinned baseline. The benchmark must not resume until the execution harness proves that host filesystem tools, container shell execution, Python imports, and Claude Code project/session context all refer to one fresh canonical workspace.

This procedure is an experiment-validity control. It is not a SpecGrain product change and does not alter any benchmark arm, task, oracle, method configuration, scorer, model, or frozen runner identity.

## Canonical identities

```text
repository_revision = ed86a1528aa015f219f8d3385ea2ebd3f63a5212
baseline_archive_digest = sha256:6bdf91b309f86e4ac755f7ba33504aa7314567b69978ba71e5f0b62e33bbfbc1
more_itertools/more.py blob = 5607346368e6eb903eac3d50aad9ef65eacd0b01
tests/test_more.py blob = 1d2894b4c0dd7ff28f2ff041873f5198dc915699
runner_image_digest = sha256:d410f9a22b896edb5edeaa20ccc920f879c00a78b67f089abb647adf91e68bf8
Claude Code = 2.1.251
model = claude-fable-5
network_mode = none
```

## Qualification program

`execution-harness-qualification.py` is fail-closed and creates a never-before-used directory named:

```text
sgbench-harness-qualification-<UUID>
```

It performs these checks without starting a benchmark cell:

1. SHA-256 of the baseline archive before extraction.
2. Fresh extraction and absence of `.git`, Claude project artifacts, Spec Kit/SpecGrain artifacts, prior benchmark evidence, and run outputs.
3. Host Git blob identities for the two canonical files.
4. Operator-side inspection limited to the `sliced()` function to confirm no pre-existing explicit negative-size guard.
5. Exact frozen runner-lock identities without rewriting lock files.
6. Exact local Docker image identity and `--network none`.
7. Host/container Git blob equality.
8. Python import resolution inside `/workspace`.
9. Claude-visible project/user-state contamination preflight.
10. Qualification-only Claude tool routing instrumentation for `Read`, `Grep`, `Glob`, `Edit`/`Write`, and `Bash`.

The Edit/Write probe is non-mutating: a temporary qualification hook records the requested target and denies the tool call before execution. The baseline files are hashed immediately before and after the Claude probe. The temporary hook state is outside the extracted repository and is not part of any benchmark cell.

## Exact frozen harness launcher is required

The runner-lock package records the required behavior but does not contain the executable launcher that routes Claude Code Bash calls through Docker. Therefore the qualification program refuses to substitute raw `claude` for the frozen launcher.

The actual locked host must invoke the program with the exact launcher argv prefix used for the benchmark harness:

```text
python execution-harness-qualification.py \
  --baseline-archive <locked-baseline-archive> \
  --runner-lock-dir <final-runner-lock-directory> \
  --qualification-parent C:\Users\Shehr \
  --harness-launcher <exact-frozen-harness-launcher-and-fixed-prefix-args>
```

If the exact launcher cannot be recovered and supplied, qualification stops with:

```text
BLOCKED: CLAUDE_HARNESS_LAUNCHER_UNAVAILABLE
```

Do not reconstruct or improvise a new benchmark launcher and call it equivalent. If the original launcher is unrecoverable, the frozen execution harness is not reproducible and Attempt 003 must remain uncreated until that methodological blocker is resolved explicitly.

## Context-isolation boundary

The program does not delete global Claude data. It inspects only configuration/skill/plugin metadata for benchmark-sensitive contamination and checks that the new random project path has no prior project state. It does not read old conversation bodies.

A qualification session uses a brand-new explicit UUID and never passes `--continue` or `--resume`. Temporary strict-empty MCP and tool-observation settings are qualification instrumentation only and MUST NOT be carried into a benchmark cell unless those controls are already part of the frozen harness.

## PASS rule

`qualification_status` is derived, never hard-coded. PASS requires all of these evidence-derived booleans:

```text
baseline_archive_digest_match = true
baseline_negative_guard_present = false
python_imports_workspace_copy = true
host_container_workspace_identity = true
claude_read_observes_canonical_workspace = true
claude_search_observes_canonical_workspace = true
claude_edit_targets_canonical_workspace = true
claude_shell_targets_canonical_workspace = true
fresh_context_isolation = true
network_mode = none
```

The output file is:

```text
sgbench-exp001-execution-harness-qualification.json
```

## Attempt 003 hard stop

The qualification program deliberately does **not** create Attempt 003. After a genuine PASS, a separate operator step may create Attempt 003 with nine brand-new run/workspace/context ID triplets while preserving the frozen BenchmarkPlan and runner lock. Even then, **Cell 1 must not be executed until the new Attempt 003 cell plan is frozen and the required per-cell file-level baseline attestation is installed.**

Until PASS:

```text
ATTEMPT_002_STATUS = INVALID_CONTAMINATED
ATTEMPT_002_HIDDEN_SCORER_REVEALED = false
HARNESS_QUALIFICATION = FAIL
ATTEMPT_003_STATUS = NOT_CREATED
```
