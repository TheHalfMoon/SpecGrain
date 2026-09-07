# Post-026 Tencent Donor Qualification — 2026-09-08

## Purpose

Record a bounded design-reference review of two Tencent open-source projects against live canonical SpecGrain after Specification 026 closure conditions were realized.

This is **source qualification and observation evidence only**. It does not select a successor specification, authorize product implementation, adopt a runtime dependency, add agent/provider orchestration, or copy donor source code.

Canonical SpecGrain baseline reviewed:

```text
repository = TheHalfMoon/SpecGrain
main = faddebccb4f4b1dd71bf06b1ce7e3d7b367178ed
program_mode = post-026 bounded observation
active_product_specification = none
```

## Sources reviewed

### Tencent/LoopForge

- Repository: <https://github.com/Tencent/LoopForge>
- Reviewed revision: `09c765286f549624dd95434e1e6ef2249657cbeb`
- License: MIT, with third-party attribution requirements recorded in the donor repository license file
- Key reviewed paths:
  - `README.md`
  - `LICENSE`
  - `.claude/assets/workflow-state-template.json`
  - `.claude/runtime/workflow-state-spec.md`
  - `.claude/commands/start-devflow.md`
  - `.claude/assets/devflow.defaults.yaml`
  - `.claude/agents/devflow-code-reviewer.md`

### Tencent/SkillHone

- Repository: <https://github.com/Tencent/SkillHone>
- Reviewed revision: `7d565839fb4dc74f9c77f09ace660e1c0484e048`
- License: MIT
- Key reviewed paths:
  - `README.md`
  - `LICENSE`
  - `skills/skillhone-optimization/SKILL.md`
  - `skills/skillhone-evaluation/SKILL.md`
  - `skills/skillhone-optimization/scripts/write_observation.py`

No donor code is copied by this research change. Any future copied or closely adapted material still requires a separate `docs/provenance/` record under `docs/donor-policy.md`.

## Executive fit assessment

| Source | Fit for SpecGrain | Strongest contribution | Keep out of the deterministic core |
| --- | --- | --- | --- |
| LoopForge | **High** | resumable delivery state, explicit stage artifacts, role-separated review/test, compact handoff, bounded routing | host-specific orchestration, mandatory user-confirmation ceremony, provider/runtime coupling |
| SkillHone | **Medium-High** | persistent decision/observation history, diagnostic-layer separation, redacted evidence, eval isolation, one-change attribution | self-optimizing skill loop, model gateway, Forgejo dependency, private-eval-specific workflow |

LoopForge is the stronger product-design reference for the next execution-boundary problem. SkillHone is the stronger evidence-learning and evaluation-isolation reference.

## Existing SpecGrain capabilities that already cover adjacent ground

The donor review must not be mistaken for evidence that SpecGrain lacks all of these concepts. Current source already provides:

- recursively refined `SpecNode` planning and deterministic Grain readiness;
- immutable, revision-bound `WorkPacket` export;
- an `ExecutionResult` contract that remains executor self-report rather than verification authority;
- independent `VerificationReport` evaluation;
- append-oriented hash-chained `EvidenceRecord` storage;
- explicit authorized change-surface checking;
- context-budget accounting and digest binding;
- agent-neutral adapters that normalize request/result boundaries without invoking providers;
- fail-closed pre-Grain persistence and supported cross-writer coordination.

Therefore, copying either donor workflow wholesale would duplicate existing trust boundaries and weaken SpecGrain's independent architecture.

## LoopForge lessons worth retaining

### 1. Durable workflow state should be explicit, inspectable, and resumable

LoopForge persists one workflow-state document containing immutable task identity, current stage, last event, next target, per-stage status, artifacts, retry state, errors, decisions, and summary metadata. Resume reads this state and continues from the most recent incomplete stage rather than reconstructing workflow truth from conversation memory.

**SpecGrain implication:** if SpecGrain later owns execution-attempt continuity, continuity should be represented as deterministic repository data rather than agent conversation state.

This aligns with the constitution's evidence, recoverability, bounded-context, and deterministic-control-plane principles.

### 2. Stage artifacts are better handoff boundaries than replaying conversation history

LoopForge persists requirement, design, implementation, review, testing, and knowledge artifacts. Downstream stages read those artifacts rather than receiving an ever-growing conversational transcript. Its workflow explicitly compresses the orchestration context after requirement clarification and preserves a small handoff card that points to durable files.

**SpecGrain implication:** WorkPacket/context digests already support bounded execution input. Any later multi-stage attempt model should preserve compact references to canonical artifacts instead of embedding complete reasoning or logs.

SpecGrain should continue rejecting private reasoning transcripts as product authority.

### 3. Role separation has value only when authority remains explicit

LoopForge separates architect, developer, code reviewer, test engineer, and knowledge roles. Its code-review stage checks actual changed paths against a design whitelist and checks acceptance completion before allowing the workflow to continue.

**SpecGrain implication:** the useful idea is not the named personas. The useful invariant is that implementation self-report, independent review, and independent testing remain distinguishable evidence producers with different authority.

SpecGrain already enforces this principle structurally through `ExecutionResult` versus independent verification. Future orchestration must preserve that separation instead of treating an agent role label as proof.

### 4. Small work should not pay full orchestration ceremony

LoopForge routes small changes through a lightweight single-agent path and reserves its full workflow for medium/large work.

**SpecGrain implication:** this reinforces adaptive-method and minimal-ceremony principles. If future execution orchestration exists, method selection should remain proportional to Grain risk and evidence needs rather than requiring a fixed stage graph for every Grain.

### 5. Recovery semantics require bounded deterministic rules

LoopForge records retry counts, last errors, stage status, and resume rules. Its implementation is workflow-specific, but the general lesson is useful: recovery behavior should be derived from explicit persisted state, not inferred from a stale conversation.

**SpecGrain implication:** any future attempt-resume feature must distinguish legal recovery from blind resume. This is especially important because existing SpecGrain lifecycle ADRs intentionally reject direct downstream resume from exceptional states without later explicit history-aware semantics.

## SkillHone lessons worth retaining

### 1. Persistent decision history should record outcomes, not hidden reasoning

SkillHone describes a persistent decision history built from bounded records such as diagnosis, candidate revision, redacted evidence, and outcome. This is compatible with SpecGrain's rule that decision-relevant information may be structured while private reasoning transcripts are not authority.

**SpecGrain implication:** a future delivery-attempt history can record what was tried, why it was selected at a public decision level, what exact revision resulted, what evidence was observed, and whether the attempt verified—without storing chain-of-thought.

### 2. Diagnose the failing layer before changing the product

SkillHone separates skill failure, infrastructure failure, solver/tool failure, compiler/validator failure, and verifier failure. It warns against turning a low aggregate score directly into a product change.

**SpecGrain implication:** this strongly matches evidence-over-assertion. Future observation records should preserve failure provenance and layer classification so a failed execution does not automatically imply that the specification or implementation method is wrong.

### 3. Redacted observation surfaces are preferable to leaking evaluation secrets

SkillHone deliberately turns private/raw evaluation evidence into redacted diagnostic summaries before passing them to the improver. It also separates probe, PR-validation, and final test surfaces.

**SpecGrain implication:** this reinforces the existing benchmark contamination boundary. In particular, it supports the standing rule that invalidated `SGB-EXP-001` hidden scorer material remains outside inspection/search/materialization/reproduction/use authority.

A future evidence API should be capable of referencing redacted diagnostic artifacts without requiring hidden benchmark material to enter execution context.

### 4. One change per improvement cycle improves attribution

SkillHone uses one focused issue/PR per optimization cycle so observed score movement can be attributed to one bounded change.

**SpecGrain implication:** this is directly compatible with Grain minimality, authorized change surfaces, exact-head verification, and small-batch metrics.

### 5. Score and evidence provenance must remain explicit

SkillHone requires a score to name which split, output, workdir, or phase produced it rather than collapsing several runs into one unlabeled number.

**SpecGrain implication:** this reinforces exact-revision and evidence-origin binding. Any future process-quality metric should preserve source identity and must not merge incomparable evidence into a single success claim.

## Combined design insight

The two donors converge on one pattern that is not equivalent to full agent orchestration:

```text
WorkPacket
  -> execution attempt starts
  -> bounded stage/attempt events are persisted
  -> result is bound to the exact packet/revision
  -> independent verification evaluates the result
  -> durable observation/evidence history records the outcome
  -> interruption or failure can be inspected and recovered without conversation replay
```

SpecGrain already owns the left boundary (`WorkPacket`) and the verification/evidence boundary. The potentially interesting future gap is the **durable execution-attempt continuity between them**.

That gap is only a **candidate observation**, not selected implementation authority.

A narrowly shaped future primitive, if fresh reproducible evidence selects it, could resemble an append-oriented `ExecutionAttemptRecord` or equivalent deterministic ledger that binds a bounded attempt identity to:

- `spec_id` and `spec_revision`;
- `packet_digest`;
- attempt state/event;
- adapter/executor identity as descriptive metadata, not trust authority;
- implementation revision when one exists;
- `result_digest` when reported;
- verification/evidence record digest when independently produced;
- concise public decision/diagnostic references;
- failure/retry/recovery metadata;
- no provider invocation and no hidden reasoning transcript.

This would be materially smaller than importing LoopForge's host workflow or SkillHone's optimization harness.

## Rejected adoptions

This review does **not** justify:

- copying LoopForge's complete stage taxonomy into SpecGrain;
- making Claude Code, Cursor, Codex, CodeBuddy, or any host bundle part of the core;
- adding Node.js, LiteLLM, Forgejo, model SDKs, or other runtime dependencies;
- making a user-confirmation ceremony mandatory for every medium/large Grain;
- allowing role labels to grant verification authority;
- adding automatic agent/provider invocation;
- adding self-optimizing skills to the core;
- storing hidden reasoning traces as canonical decision history;
- exposing private or hidden benchmark/eval data to an executor or improver;
- using donor score thresholds as SpecGrain benchmark truth;
- opening Specification 027 solely because these donors have adjacent features.

## Source-use ranking for SpecGrain

### Priority 1 — LoopForge

Best used as a reference for:

1. resumable deterministic delivery-state modeling;
2. explicit artifact pointers and compact cross-stage handoff;
3. retry/error/resume semantics;
4. separation of implementation, review, and test roles;
5. proportional small-versus-complex workflow routing.

### Priority 2 — SkillHone

Best used as a reference for:

1. persistent public decision/observation history;
2. diagnostic-layer classification;
3. redacted evidence surfaces;
4. evaluation/optimization isolation;
5. one-change-per-cycle attribution and score provenance.

## Continuation rule

No product change is authorized by this donor review alone.

The next valid step is bounded observation against live canonical SpecGrain. A successor specification should be shaped only if fresh reproducible evidence demonstrates a concrete user-visible or correctness-relevant failure that the current `WorkPacket -> ExecutionResult -> VerificationReport -> EvidenceRecord` surface cannot safely represent.

If such evidence is not found, remain in post-026 observation and keep these donors as qualified design references only.
