# Trust Model

SpecGrain separates proposal/execution from authority. Humans and agents may propose specifications, context, changes, results, or review conclusions; deterministic contracts decide whether repository state and evidence satisfy declared gates.

## Deterministic authority

The core owns deterministic validation for:

- SpecNode schema and semantic revision digests;
- lifecycle legality and transition preconditions;
- refinement-tree integrity;
- Grain readiness;
- dependency graph blockers and eligible sets;
- bounded repository-map facts;
- context-budget accounting;
- WorkPacket/result serialization and digest binding;
- independent verification and evidence-chain integrity;
- method-profile requirements;
- change-scope/drift/metrics calculations;
- Spec Kit import boundaries;
- generic agent-adapter normalization;
- SpecGrainBench comparability preflight.

## Executor self-report is not proof

An `ExecutionResult` records what an executor reports. `verify_execution` independently checks the current spec revision, packet/result binding, observed changed paths, authorized change surface, acceptance checks, required evidence checks, and implementation revision. A successful executor status alone cannot produce `VERIFIED`.

## Brownfield safety boundary

`specgrain scan` inspects bounded repository facts. It does not execute package scripts, builds, tests, Git commands, arbitrary repository code, LLMs, embeddings, or network requests. Symlink and bounded-read rules are fail-closed where the scanner consumes repository files.

## Local-first data

The local store is repository-local `.specgrain/` state. v0.1.0 has no hosted account service, telemetry requirement, model provider, or runtime third-party package dependency.

## Evidence storage

Verification reports can be wrapped in immutable, hash-chained evidence records. Evidence loading validates record filenames, digests, chain shape, record limits, bounded reads, and exact SpecNode ownership. Evidence is still only as trustworthy as the independent checks and implementation revision supplied by the caller; SpecGrain does not claim a cryptographic digest proves semantic correctness by itself.

## Integration boundary

Agent adapters render exact WorkPackets and normalize external executor results. Adapters do not invoke providers in v0.1.0 and cannot accept external fields that manufacture packet/result digests or verification authority.

## Security reporting

See [`../SECURITY.md`](../SECURITY.md) for vulnerability reporting and supported-version policy.
