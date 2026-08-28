# Core Domain Model

## 1. Design rule

Use one recursive specification primitive and keep execution evidence separate from planning state.

## 2. SpecNode

`SpecNode` represents intent at any level of refinement.

Required conceptual fields:

- `id`: stable repository-local identifier.
- `revision`: monotonic or content-addressed spec revision.
- `parent_id`: optional parent spec.
- `title`: concise outcome-oriented name.
- `outcome`: the result this node is responsible for.
- `rationale`: why the outcome matters.
- `scope.in`: explicitly authorized behavior or surfaces.
- `scope.out`: explicitly excluded behavior or surfaces.
- `acceptance`: verifiable acceptance conditions.
- `dependencies`: other SpecNode IDs that must be satisfied first.
- `risk`: risk class plus required mitigations or recovery.
- `context`: context policy, sources, and budget.
- `change_surface`: allowed repository paths or semantic boundaries when known.
- `evidence`: evidence requirements.
- `method`: selected delivery method profile.
- `state`: lifecycle state.
- `children`: child SpecNode IDs.

A parent and child use the same schema. The core does not require different entity types for initiatives, epics, stories, or tasks.

## 3. Grain

A Grain is a derived property of a SpecNode, not a second planning schema.

A node is a Grain when all of the following are true:

1. It has no unresolved child refinement requirement.
2. It represents one independently understandable outcome.
3. Scope is bounded and internally coherent.
4. Acceptance conditions are independently verifiable.
5. Dependencies are explicit and acyclic.
6. Risk and recovery requirements are sufficient for its risk class.
7. Required context fits the active context policy.
8. The permitted change surface is explicit or a justified discovery exception exists.
9. Evidence requirements can prove the outcome for the exact revision.
10. No unresolved decision blocks implementation.

A node that fails a Grain gate remains a spec and should normally be refined.

## 4. State machine

Canonical lifecycle:

```text
DRAFT -> SHAPED -> REFINING -> GRAIN -> READY -> RUNNING -> VERIFYING -> VERIFIED
                                                        \-> FAILED
                       \-> BLOCKED
```

Optional terminal/control states:

- `CONTROLLED`: required post-verification control checks completed.
- `SUPERSEDED`: replaced by another spec revision or node.
- `CANCELLED`: intentionally abandoned.
- `STALE`: assumptions or dependencies changed enough to require review.

State transitions must be validated by deterministic rules. An agent response cannot directly assign `VERIFIED`.

## 5. Decomposition edge

A parent-child edge means "this child refines part of the parent's responsibility." Children collectively must preserve parent intent. Decomposition validation should detect:

- uncovered parent acceptance conditions;
- duplicated responsibility;
- conflicting child outcomes;
- children that introduce unauthorized scope;
- children that depend circularly on one another.

## 6. Dependency edge

A dependency edge means "this node requires the verified or otherwise policy-satisfied result of another node before it can become READY."

Decomposition edges form a tree or forest view. Dependency edges form a DAG across executable leaves. They are distinct relationships.

## 7. WorkPacket

A `WorkPacket` is an immutable execution projection for one Grain revision.

It contains only what an executor needs:

- Grain ID and revision digest;
- outcome and acceptance conditions;
- constraints and constitution excerpts relevant to the Grain;
- selected repository context with provenance;
- dependency evidence summaries;
- allowed change surface;
- required checks and evidence;
- risk and recovery instructions;
- execution adapter metadata.

A WorkPacket should be reproducible from repository state.

## 8. ExecutionRun

An `ExecutionRun` records an attempt to implement one WorkPacket.

Conceptual fields:

- run ID;
- Grain ID and revision;
- baseline repository revision;
- executor type, provider, model/tool version when known;
- start and end timestamps;
- result repository revision;
- changed paths;
- execution outcome;
- resource metrics when available;
- reported blockers.

Runs are historical facts and are never rewritten to make a later run look cleaner.

## 9. EvidenceRecord

An `EvidenceRecord` binds verification facts to exact inputs.

It should include:

- Grain revision digest;
- implementation revision;
- verifier identity/tool version;
- acceptance results;
- test/static-check results;
- scope-compliance result;
- provenance checks;
- residual risks;
- evidence artifact digests;
- final verification decision.

## 10. MethodProfile

A `MethodProfile` selects additional gates and evidence based on work class and risk. Initial profiles:

- `quick`;
- `dmadv-lite`;
- `dmaic-lite`;
- `experiment`;
- `controlled`.

Method profiles extend the core Grain contract; they do not replace it.

## 11. DecisionRecord

Durable architectural or product decisions belong in ADRs, not hidden inside individual agent transcripts. Specs may reference ADRs, and WorkPackets should include only relevant ADR excerpts or summaries.
