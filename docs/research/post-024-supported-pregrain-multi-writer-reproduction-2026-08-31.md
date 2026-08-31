# Post-024 Supported Pre-Grain Multi-Writer Reproduction — 2026-08-31

## Purpose

Determine whether the explicit concurrent-writer residual retained after Specification 022 and left outside Specification 024 can be reproduced using only supported public SpecGrain mutation APIs.

This observation does not use the invalidated SGB-EXP-001 benchmark and does not authorize product implementation by itself.

## Canonical baseline

```text
repository = TheHalfMoon/SpecGrain
canonical_main = 101f018095868fc011c4ebea15dcac64f64d1061
program_state = POST_024_OBSERVATION
active_product_specification = none
published_release = v0.3.0
```

Canonical governance permits successor shaping only when fresh reproducible evidence against live repository truth independently selects a bounded product gap.

## Existing residual

Canonical `src/specgrain/pregrain.py` persists every supported pre-Grain mutation through `_persist` -> `_replace_spec_exact`.

`_replace_spec_exact` performs:

1. an exact preimage read/check;
2. temporary-file creation and fsync;
3. a second exact preimage read/check;
4. unconditional `os.replace(temp_path, path)`.

The second preimage check and the replacement are separate filesystem operations. Therefore a competing supported writer that commits after step 3 but before step 4 can be overwritten unless supported writers are serialized or the replacement primitive provides an atomic compare-and-swap contract.

## Observation fixture

A test-only observation branch was created directly from the canonical baseline:

```text
branch = obs/025-multi-writer-parent-replace-fixture
final_observation_head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
fixture = tests/test_post_024_multi_writer_observation.py
fixture_blob = b0852096a6f8916955a6a31b3a785ca8bb0d708d
```

The final fixture injects exactly one competing supported writer at writer A's final `os.replace` boundary:

```text
writer A: shape_draft_spec(... writer_a ...)
  -> loads DRAFT
  -> validates proposed SHAPED value
  -> reaches _replace_spec_exact
  -> passes final preimage check
  -> pauses immediately before os.replace

writer B: shape_draft_spec(... writer_b ...)
  -> loads the same still-DRAFT canonical file
  -> validates a distinct SHAPED value
  -> commits it through the same supported public API
  -> confirms the stored postimage
  -> returns success

writer A resumes
  -> os.replace overwrites writer B's successful SHAPED value
  -> confirms writer A's postimage
  -> returns success
```

The fixture proves all of the following simultaneously:

- both calls use the supported public `shape_draft_spec` API;
- both calls return success;
- writer A and writer B produce distinct semantic revision digests;
- writer B's successful postimage is present before writer A resumes;
- the final canonical file contains writer A's revision only;
- writer B's successful revision is silently lost.

This is a supported-writer lost update, not an arbitrary manual-file-edit scenario.

## Machine-run evidence

Final GitHub Actions evidence:

```text
run_id = 33431133156
head = 58174dbc87e9c02ebbb3a19d38727e1f42149226
workflow = CI
status = completed
conclusion = success
```

All permanent cells completed successfully:

```text
ubuntu-latest / Python 3.11 = success
ubuntu-latest / Python 3.12 = success
ubuntu-latest / Python 3.13 = success
macos-latest / Python 3.11 = success
windows-latest / Python 3.11 = success
```

The workflow also passed Ruff over source/tests/examples, the full regression suite, tracked-tree cleanliness, compileall, source CLI smoke, package build, built-wheel installation, and installed CLI smoke.

## Superseded observation heads

Two earlier heads are preserved as methodology history but are not selection evidence:

```text
32d524cfcd92d354b56558f7b9c72c09e8f03356
```

This head successfully demonstrated that an arbitrary direct file edit can land between the final preimage check and `os.replace`, but ADR-0018 explicitly does not promise coordination with arbitrary non-cooperating edits. It therefore did not establish the supported-writer gap required for successor selection.

```text
c0b2f77fa98099b5e571ed75e5c9b78a6128aaf5
```

This head attempted the supported-writer reproduction but its fixture recursively reinjected writer B and failed CI run `33430982287` with a fixture `RecursionError`. The product hypothesis was neither accepted nor rejected by that failed harness. The final head added a one-injection guard and is the only supported-writer selection evidence.

## Reproduced gap

The reproduced product gap is:

```text
SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
```

A supported pre-Grain mutation can return success and later be silently overwritten by another supported mutation that had already passed its final preimage check.

This violates the intended fail-closed mutation boundary more narrowly than general filesystem concurrency. No evidence here shows that SpecGrain should coordinate with arbitrary external editors, non-SpecGrain writers, remote filesystems, distributed stores, or all repository mutations.

## Smallest justified product boundary

Fresh evidence justifies shaping only cooperative serialization for supported pre-Grain persistence operations that flow through `src/specgrain/pregrain.py::_persist`.

A candidate implementation may use one project-scoped, non-blocking advisory lock anchor under `.specgrain/tmp/` held only around `_persist`'s validate/read/replace/postimage-confirmation transaction.

The lock must:

- use standard-library platform primitives only;
- fail closed immediately when another supported pre-Grain persistence transaction holds the lock;
- release automatically when its file descriptor/process terminates rather than infer ownership from lock-file presence;
- treat a persistent lock-anchor file as inert runtime metadata rather than transaction state;
- preserve exact-preimage checks and atomic replacement as defense in depth;
- add no retry loop, timeout heuristic, daemon, network service, or runtime dependency.

Candidate standard-library primitives are `fcntl.flock(... LOCK_EX | LOCK_NB)` on supported Unix-family runners and `msvcrt.locking(... LK_NBLCK ...)` on Windows. Product implementation must prove the chosen abstraction on the permanent CI matrix rather than rely on documentation alone.

## Explicit non-authority

This evidence does not justify:

- coordination with arbitrary manual/non-SpecGrain file edits;
- project-wide serialization of unrelated read-only commands;
- changing child-authoring journal semantics;
- distributed or network locking;
- blocking waits, retries, leases, heartbeats, or timeout ownership inference;
- filesystem/database replacement;
- new runtime dependencies;
- lifecycle expansion beyond the existing DRAFT -> SHAPED -> REFINING -> GRAIN path;
- executor/provider/result/verification/evidence orchestration;
- release publication;
- benchmark claims.

## Selection conclusion

The post-024 evidence criterion is satisfied by an exact cross-platform machine-run reproduction using two supported public mutation calls.

```text
BOUNDED_PRODUCT_GAP = SUPPORTED_PRE_GRAIN_MULTI_WRITER_LOST_UPDATE
SUCCESSOR_SHAPING_JUSTIFIED = true
IMPLEMENTATION_AUTHORIZED = false
```

A Specification 025 shaping candidate may therefore be created. Product implementation remains blocked until the documentation-only shaping package is merged canonically and the resulting `main` passes the permanent CI matrix.
