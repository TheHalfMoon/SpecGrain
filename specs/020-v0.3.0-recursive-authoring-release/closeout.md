# Closeout — Specification 020 v0.3.0 Recursive Authoring Release

**Status:** `CLOSED_CANONICAL`  
**Canonical shaping merge:** `05219b4ea7ce1be201c8fb2ff31e707ae02cba17`  
**Final implementation/evidence PR head:** `bf59a2ceba3e28cabc2294a0bd95e4e973b1e2bf`  
**Canonical product merge:** `70dd66aba0e68ae710e6ef12605ed153d107bab4`  
**Canonical closeout head:** `a9cb5c65598b12e005034b3fec3b356239bbaf29`  
**Canonical closeout merge:** `123e1ded9d6bdc1aa15767ec7185bfffab5f8eba`  
**GitHub Release:** `378962445` / `v0.3.0`

## Scope delivered

Specification 020 publishes the already-canonical recursive DRAFT authoring and explicit recovery surface as v0.3.0. It changes package/release truth only and adds no new `src/specgrain/` product behavior.

The release preserves these boundaries:

- a native child is fixed to `DRAFT` and requires an existing `DRAFT` parent;
- the selected parent remains `DRAFT`;
- `specgrain recover` is explicit and bounded to exact recognized authoring-transaction states;
- ambiguous transaction state fails closed;
- no generic editing, lifecycle promotion, readiness synthesis, executor/provider invocation, hosted service, PyPI publication, runtime dependency, or empirical benchmark-winner claim is introduced.

## Exact implementation evidence

Product candidate `d207d54317457a744cb8887a260fcb78dc0710be` passed exact-head permanent-matrix CI run `33249652226`. Ubuntu/Python 3.11 job `99093025588` recorded `555 passed in 1.46s`, successful Ruff/compile/CLI checks, successful `specgrain-0.3.0` wheel/source build, built-wheel reinstall, and installed CLI smoke.

Manual review found one unnecessary wording change inside the historical v0.1.0 changelog entry on prior head `e00d3186cef4ff033fd7f15916b1849752c1059c`. It was repaired forward at `d207d54317457a744cb8887a260fcb78dc0710be` before final evidence.

Evidence commit `bf59a2ceba3e28cabc2294a0bd95e4e973b1e2bf` added only `review.md`, `verification.md`, and T009–T011 task evidence after the reviewed product candidate. Final PR CI run `33249768557` completed successfully across all five permanent matrix cells on that exact final head. Final recheck found no submitted reviews or inline review threads; PR #30 remained mergeable and canonical `main` remained at the shaping merge.

## Canonical product merge

PR #30 merged with expected-head protection as `70dd66aba0e68ae710e6ef12605ed153d107bab4`.

The merge is GitHub-signature verified and has:

- first parent: exact canonical shaping merge `05219b4ea7ce1be201c8fb2ff31e707ae02cba17`;
- second parent: exact final implementation/evidence head `bf59a2ceba3e28cabc2294a0bd95e4e973b1e2bf`.

Canonical post-merge CI run `33249920673` completed successfully across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11 on exact product merge `70dd66a...`.

## v0.3.0 first publication evidence

Release workflow run `33249956337`, job `99093825183`, completed successfully. Its log proves that the workflow:

1. checked out exact canonical product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
2. resolved package version `0.3.0`, tag `v0.3.0`, title `SpecGrain v0.3.0`, and the expected wheel/source filenames from metadata;
3. built exactly `specgrain-0.3.0-py3-none-any.whl` and `specgrain-0.3.0.tar.gz`;
4. created new tag `v0.3.0`;
5. created the GitHub Release for that tag.

Live GitHub truth after publication:

- `refs/tags/v0.3.0` is a lightweight tag targeting exact product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- GitHub Release ID: `378962445`;
- tag: `v0.3.0`;
- target: `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- title: `SpecGrain v0.3.0`;
- draft: `false`;
- prerelease: `false`;
- GitHub API `immutable`: `false`; repository governance treats the release as immutable-by-contract rather than claiming the GitHub immutable-release feature;
- publication timestamp: `2026-08-29T11:22:04Z`.

Published assets:

1. `specgrain-0.3.0-py3-none-any.whl`
   - asset ID: `535129008`
   - size: `70463`
   - digest: `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`
   - download count at closeout audit: `0`
2. `specgrain-0.3.0.tar.gz`
   - asset ID: `535129009`
   - size: `104057`
   - digest: `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`
   - download count at closeout audit: `0`

## Historical release preservation

Live re-verification after v0.3.0 publication confirms:

- `v0.1.0` still targets `5eb46db0479cb8707afe070027dab4f3c558849a`, Release `378876694`, with original asset IDs `534763956`/`534763957`, sizes `65542`/`93125`, and original digests unchanged;
- `v0.2.0` still targets `baf00995a7ae9cf01b6196d68c62f4eca2c1ec85`, Release `378936896`, with original asset IDs `535032845`/`535032844`, sizes `66709`/`96850`, and original digests unchanged.

No historical tag or release was retargeted or mutated to achieve v0.3.0 progression.

## Fresh frontier audit

`docs/research/post-v0.3-product-audit-2026-08-29.md` records that v0.3.0 now closes the distribution discontinuity that motivated Specification 020. Current canonical product behavior and the latest public versioned release are aligned for native root/child DRAFT authoring and explicit recovery.

The audit finds no evidence-supported successor specification at this time. Deferred lifecycle mutation, generic editing, broader distribution, executor orchestration, multi-writer locking, hosted/provider surfaces, and benchmark claims remain materially larger or externally dependent than the observed evidence justifies.

This is an observation-state decision, not a claim that the product can never evolve. Fresh user/adoption evidence, bug reports, reproducible benchmark data, or a separately shaped governance need may justify later work.

## Canonical closeout evidence

Documentation-only closeout PR #31 used exact head `a9cb5c65598b12e005034b3fec3b356239bbaf29`.

- exact-head PR CI `33250227572` completed `success` across the permanent five-cell matrix;
- final recheck found no submitted reviews or inline review threads;
- PR #31 merged with expected-head protection as `123e1ded9d6bdc1aa15767ec7185bfffab5f8eba`;
- the closeout merge is GitHub-signature verified;
- first parent is exact product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- second parent is exact closeout head `a9cb5c65598b12e005034b3fec3b356239bbaf29`;
- canonical post-closeout CI `33250422380` completed `success` across Ubuntu/Python 3.11, 3.12, 3.13, macOS/Python 3.11, and Windows/Python 3.11;
- Release verification `33250468134`, job `99095156240`, checked out exact closeout merge `123e1de...` and completed `success`;
- the Release log states that `SpecGrain v0.3.0 is already published at historical tag target 70dd66aba0e68ae710e6ef12605ed153d107bab4; no release mutation is required.`

Live post-verification release truth remains unchanged:

- tag `v0.3.0` still targets exact product merge `70dd66aba0e68ae710e6ef12605ed153d107bab4`;
- Release ID remains `378962445`;
- wheel asset remains ID `535129008`, size `70463`, digest `sha256:b4f724e5ae187db28053c264cf9b9612f864fe5052459c7341a7f470602fb817`;
- source asset remains ID `535129009`, size `104057`, digest `sha256:e7dc5484b8439cf8a6c594c65b454e141fef7c94a7edb0c7cb4edfc839007835`.

All canonical closure conditions are therefore satisfied. Specification 020 is `CLOSED_CANONICAL`.

## Program state

The program is now `POST_V0.3_OBSERVATION` with no active successor specification. Any later specification must be shaped from fresh evidence under the repository's post-v0.1 rules; deferred roadmap items are not implicit authority.
