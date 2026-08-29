# Launch Strategy

## Goal

Make SpecGrain understandable in under one minute and credible after one hour of inspection. Popularity is an outcome of usefulness, clarity, proof, and community execution; it is not a guarantee the project can truthfully make.

## Core message

> Big ideas. Small specs. Proven software.

SpecGrain recursively refines work until executable leaves are small enough to understand, contextually isolate, verify, recover, and prove.

## v0.1.0 launch demo

The public demo uses only release surfaces that exist:

```bash
python -m pip install .
specgrain scan .
python examples/zero_to_verified.py
```

The first command installs the dependency-light package. `scan` shows bounded brownfield repository facts. The example then demonstrates Grain readiness, context budgeting, a digest-bound WorkPacket, independent verification, append-oriented evidence, and proof.

Earlier planning examples referenced future orchestration commands. Those commands are not part of the v0.1.0 CLI and must not be advertised as shipped behavior.

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
