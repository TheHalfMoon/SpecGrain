# Verification — Specification 024 Native WorkPacket Export

**Status:** `CLOSEOUT_CANDIDATE`  
**Canonical shaping merge:** `440a8b14459ade2fe8235cc873229dd87ba926b5`  
**Final implementation head:** `7e1db87f69108fc8693b987e77d20f92e4f46866`  
**Implementation PR:** #50 — merged/closed  
**Canonical product merge:** `1666ba8c135ee8575f1546019ab592db32947dd2`  
**Canonical post-product CI:** `33422235433` — `completed/success`  
**Published release preserved:** `v0.3.0` / Release `378962445`

Specification 024 is not `CLOSED_CANONICAL` yet. This document records product evidence already proven from live GitHub truth. Documentation closeout, post-closeout CI, and final evidence reconciliation remain required before canonical closure.

## Selection evidence

Specification 024 was selected by the deterministic post-023 interoperability reproduction in `docs/research/post-023-workpacket-handoff-reproduction-2026-08-31.md`.

Exact selection proof:

```text
canonical_base = f2e8378dcba0cfea2beedc6da61324b0c3fea95e
observation_head = 95e5358ed420cd2e6fbd0bc7c56690763cea1283
fixture_blob = 58cb3e355468f6bcd7de63b676dba52361ff0dd7
ci_run = 33416110142
ci_result = completed/success across all five permanent cells
```

The fixture proved that native authoring reached a dependency-eligible `GRAIN`, native CLI lacked WorkPacket export, and the existing WorkPacket could be built only after switching to custom Python API glue.

## Shaping proof

Documentation-only shaping head `043abdf8f15f688cdbae746c0abd83dda74d0dae` passed push CI `33416602621` and PR CI `33416635970`, both `completed/success` across the permanent five-cell matrix.

PR #49 merged with expected-head protection as canonical shaping merge `440a8b14459ade2fe8235cc873229dd87ba926b5`. Canonical post-shaping CI `33416908615` completed `success` across all five cells before product implementation began.

## Product implementation proof

The final implementation head is:

`7e1db87f69108fc8693b987e77d20f92e4f46866`

The exact shaped-base-to-final-head diff changed only:

- `README.md`;
- `src/specgrain/cli.py`;
- `tests/test_workpacket_cli.py`;
- `tests/test_launch.py`;
- `tests/test_repository_cli.py`.

The last two are test-only compatibility exceptions required by full-regression evidence: the launch contract needed to recognize `packet` as a current-source command, and the isolated mocked CLI fixture needed the newly imported `load_project` symbol. Neither widens runtime authority.

Exact push CI `33421885016` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11. Ubuntu/Python 3.11 recorded `592 passed` and then passed tracked-tree cleanliness, compile, source CLI smoke, package build, built-wheel reinstall with `--no-deps`, and installed CLI smoke. Both source and installed CLI help exposed `packet`.

Exact PR CI `33422062846` also completed `success` across all five permanent cells on the same final head.

Superseded failed runs were retained as engineering evidence, not hidden:

- `e0ec4b400d9a5df815382c6f3e8070b6358d0afc` / run `33417702813` — failed regression because new CLI imports and stale test assumptions exposed fixture defects;
- `482606f0a8632d1a391aa2a059354b320419d477` / run `33421661140` — failed only the remaining help-format smoke assertion;
- both were repaired without weakening product invariants before the final successful head.

## Acceptance proof

The implemented command is:

```text
specgrain packet <spec_id> [path] --context-sources <json-file> [--json]
```

Focused and full-regression evidence proves:

1. an exact dependency-eligible stored `GRAIN` exports the existing WorkPacket contract;
2. JSON output round-trips through `WorkPacket.from_dict` with its declared digest;
3. CLI and existing public API construction produce identical canonical packet JSON for identical node/context inputs;
4. repeated export and representative failures leave `.specgrain/` byte-identical;
5. context array ordering is canonicalized through existing context-budget semantics;
6. wrong state, missing/noncanonical target, dependency-ineligible target, and invalid dependency graph fail closed;
7. malformed JSON, duplicate keys, non-finite numeric tokens, missing/unknown fields, invalid ContextSource values, and duplicate source IDs fail closed;
8. required context beyond the Grain token budget fails closed while existing optional-source selection semantics are preserved;
9. symlink, non-file, oversized, and invalid-UTF-8 context input fail closed;
10. no lifecycle advancement, executor/provider call, verification execution, evidence mutation, automatic context discovery, network access, or LLM selection was added.

## Review proof

At the product merge gate, PR #50 had no submitted reviews and no inline review threads.

Review-system availability was recorded without false PASS claims:

- Qodo was billing-blocked;
- automatic CodeRabbit review was skipped by repository-star policy;
- Cubic supplied descriptive summary text only.

## Product merge proof

PR #50 merged with expected-head protection against exact head `7e1db87f69108fc8693b987e77d20f92e4f46866`, producing canonical product merge `1666ba8c135ee8575f1546019ab592db32947dd2`.

Canonical post-product CI `33422235433` completed `success` across all five permanent cells.

## Historical release preservation

After the product merge:

- tag `v0.3.0` -> `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID `378962445`, target `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- wheel asset ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

The historical release notes and historical v0.3.0 command surface remain unchanged.

## Remaining closure gates

Before Specification 024 can become `CLOSED_CANONICAL`:

1. this documentation-only closeout candidate must pass exact-head push and PR five-cell CI;
2. its exact diff, reviews, threads, mergeability, and review-system availability must be checked;
3. the closeout PR must merge with expected-head protection;
4. canonical post-closeout five-cell CI must succeed;
5. historical `v0.3.0` preservation must be reverified;
6. a final documentation-only evidence reconciliation must publish those exact facts to canonical `main`.
