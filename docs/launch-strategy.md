# Launch Strategy

## Goal

Make SpecGrain understandable in under one minute and credible after one hour of inspection.

GitHub popularity is an outcome of usefulness, clarity, proof, and community execution; it cannot be guaranteed. The launch strategy should maximize those inputs rather than optimize for empty star acquisition.

## Core message

> Big ideas. Small specs. Proven software.

Expanded:

> SpecGrain recursively refines software work until every executable change is small enough to understand, contextually isolate, verify, recover, and prove.

## 30-second demo

The launch demo should show a real brownfield repository:

```text
$ specgrain ask "Add organization invitations"

Outcome SG-001
  SG-002 invitation persistence       GRAIN
  SG-003 invitation creation          waiting on SG-002
  SG-004 invitation acceptance        waiting on SG-002
  SG-005 expiration                   GRAIN

2 READY / 4 total
```

Then:

```text
$ specgrain packet SG-002
$ <agent executes packet>
$ specgrain verify SG-002 --result <revision>
VERIFIED
$ specgrain prove SG-002
```

The audience should see decomposition, bounded context, exact scope, and proof without reading a methodology essay first.

## README structure for launch

1. One-sentence problem and promise.
2. Animated terminal demo.
3. Why large specs fail.
4. Recursive spec / Grain model diagram.
5. Five-minute quickstart.
6. Evidence and trust model.
7. Spec Kit migration example.
8. Reproducible benchmark results.
9. Architecture and local-first guarantees.
10. Roadmap and contribution entry points.

## Proof before claims

Do not publish fabricated comparison tables. Every numeric comparison must link to a reproducible SpecGrainBench run, repository snapshot, scoring logic, and configuration.

## Community design

The project should have contributor-sized Grains available publicly. Good first contributions should include:

- adapter additions;
- repository scanners for specific ecosystems;
- validation rules;
- benchmark cases;
- documentation examples;
- visualization layers over stable core JSON.

## Launch assets

Before a major public push, require:

- installable release;
- Linux/macOS/Windows verification;
- three real example repositories;
- a short demo video/GIF;
- benchmark report;
- architecture diagram;
- migration guide from Spec Kit;
- contribution guide;
- security policy;
- code of conduct;
- issue templates;
- release notes.

## Adoption wedge

The first adoption wedge is not "replace every project-management tool." It is:

> Take one risky or over-large AI coding change and turn it into small, independently provable units.

Spec Kit migration is the second wedge because it gives an established SDD community a low-friction path to test the model without discarding existing work.
