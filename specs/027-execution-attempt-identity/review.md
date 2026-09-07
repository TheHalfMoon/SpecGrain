# Review 027 — Execution Attempt Identity Contract

## Shaping review checklist

- Does the selection come from fresh local reproducible evidence rather than donor feature presence?
- Does exact observation CI `34163498855` prove the fixture across all five permanent cells?
- Is the reproduced gap occurrence identity rather than a false claim that content digests are defective?
- Does the specification keep `WorkPacket`, `AgentRequest`, and `ExecutionResult` v1 schemas unchanged?
- Is `attempt_id` explicitly separate from content digest identity?
- Is the attempt status vocabulary separate from `SpecState` lifecycle authority?
- Does the shaped product avoid persistence because persistence failure was not independently reproduced?
- Are provider invocation, orchestration, retry scheduling, lifecycle mutation, verification/evidence mutation, hidden reasoning, hidden evaluator access, dependencies, hosted scope, and release work explicitly excluded?
- Does the proposal remain agent/vendor neutral and standard-library only?
- Are LoopForge and SkillHone treated as attributed design references only, with no donor code copied?

## Product review checklist

- Is implementation surface limited to the isolated attempt contract, exports, and focused tests unless expansion is explicitly justified?
- Are attempt IDs validated in exact canonical grammar?
- Are all SHA-256 bindings strict lowercase `sha256:<64 hex>` values?
- Are status/result/error invariants deterministic and complete?
- Does strict deserialization reject unknown/missing fields and digest tampering?
- Can two different attempt IDs bind identical packet/request/result digests while remaining distinct?
- Does identical attempt content round-trip with stable `attempt_digest`?
- Are existing packet/request/result v1 digests unchanged?
- Is there no `verified` or lifecycle-authority field in the attempt contract?
- Is runtime dependency count still zero?
- Did the exact product head pass all five permanent CI cells?
- Were unavailable/skipped/neutral review systems recorded accurately rather than treated as PASS?
- Is historical `v0.3.0` unchanged?

## Residual-risk boundary

Even after Specification 027, SpecGrain will not yet own durable attempt persistence, process recovery, automatic retries, or executor invocation. A caller can represent separate attempt occurrences portably, but storage and orchestration remain external. That is intentional unless future reproducible evidence selects a narrower next gap.