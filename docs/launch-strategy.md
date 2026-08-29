# Launch Strategy

## Goal

Make SpecGrain understandable in under one minute and credible after one hour of inspection. Popularity is an outcome of usefulness, clarity, proof, and community execution; it is not a guarantee the project can truthfully make.

## Core message

> Big ideas. Small specs. Proven software.

SpecGrain recursively refines work until executable leaves are small enough to understand, contextually isolate, verify, recover, and prove.

## Current v0.3.0 launch demo

The public demo uses only surfaces shipped in the current versioned release:

```bash
python -m pip install "https://github.com/TheHalfMoon/SpecGrain/archive/refs/tags/v0.3.0.zip"
mkdir specgrain-demo
specgrain init specgrain-demo --project-id demo
specgrain draft specgrain-demo \
  --title "Add a bounded health check" \
  --outcome "The service exposes one deterministic health endpoint"
specgrain check specgrain-demo
```

The release installs with zero runtime third-party dependencies. `init` creates repository-local state, `draft` creates a validated root `DRAFT`, and `check` validates that state without promoting lifecycle status or granting execution authority.

The same release also ships bounded brownfield scanning, child-DRAFT authoring through `draft --parent`, explicit supported transaction recovery through `recover`, dependency eligibility through `next`, evidence loading through `prove`, and read-only Spec Kit migration reports through `import-spec-kit`.

For a source checkout, `python examples/zero_to_verified.py` demonstrates Grain readiness, context budgeting, a digest-bound WorkPacket, independent verification, append-oriented evidence, and proof. It is exercised by the repository test suite rather than advertised as precomputed benchmark output.

Future orchestration commands, hosted surfaces, generic lifecycle editing, and provider execution are not part of v0.3.0 and must not be advertised as shipped behavior.

## Public proof order

1. real supported command or API surface;
2. exact automated verification;
3. exact source/release revision;
4. public claim no stronger than the evidence.

Do not publish fabricated comparison tables. Every future numerical competitive comparison must link to a reproducible SpecGrainBench dataset, repository snapshot, scoring logic, configuration, contamination preflight, and raw run status.

## Adoption wedge

The first adoption wedge remains narrow:

> Take one risky or over-large software change and make its execution boundary small, explicit, and independently provable.

Brownfield scanning and Spec Kit migration make that idea testable without asking users to discard existing repositories or planning artifacts.

## Community entry points

Contributor-sized work should remain available in scanner signals, deterministic validators, benchmark cases, adapters, documentation examples, and visualization layers over stable JSON contracts. Hosted SaaS, large persona catalogs, and vendor-specific orchestration remain deferred until evidence justifies them.
