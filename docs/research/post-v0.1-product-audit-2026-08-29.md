# Post-v0.1 Product Audit — 2026-08-29

**Audit source revision:** `7c343841424ca48207f9c42eae725a53213d19e5`  
**Release inspected:** `v0.1.0` at `5eb46db0479cb8707afe070027dab4f3c558849a`

## Purpose

This audit identifies the smallest defensible product frontier after the closed v0.1 program. It does not authorize deferred roadmap ideas by itself and does not treat early popularity metrics as product-quality evidence.

## Live public-state snapshot

At audit time GitHub reports:

- no open pull requests or issues;
- zero stars and forks;
- zero downloads for both published `v0.1.0` release assets;
- successful canonical `main` CI at `7c343841424ca48207f9c42eae725a53213d19e5`;
- successful post-closeout release workflow;
- a public, non-draft, non-prerelease `v0.1.0` release.

The repository and release are less than a day old. These zero adoption signals are therefore an absence of evidence, not evidence of product failure or market rejection.

## Product-surface audit

### README and onboarding

The README explains the thesis, supported commands, trust boundary, brownfield behavior, Spec Kit import, benchmarks, and a tested Python zero-to-VERIFIED example. The one-minute CLI path can install, scan, initialize an empty local store, and check it.

The key onboarding gap is that a new user cannot create the first native SpecNode through a supported CLI command. After `specgrain init`, the user must construct canonical JSON manually or switch to Python APIs before the recursive specification workflow becomes tangible.

### Package and install experience

The release publishes wheel and source-distribution assets and documents installation from the tagged GitHub source archive. The current repository release contract does not include PyPI publication. PyPI distribution could reduce installation friction later, but it introduces publishing identity/credential governance and does not fix the more fundamental empty-project authoring gap.

### CLI and API

The deterministic API already exposes the core model, readiness, graph, context, WorkPacket, verification, metrics, Spec Kit import, and adapters. The CLI exposes `init`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`.

There is no supported native authoring command. Store v1 can load SpecNodes but exposes no public creation primitive beyond project initialization.

### Architecture and methodology

The architecture explicitly includes an Intent/Import -> Spec Compiler -> Store path and lists future authoring/refinement commands as progressive additions. Adding a deterministic local DRAFT authoring boundary fits the existing architecture without a new runtime dependency or provider coupling.

The methodology and constitution favor small batches, deterministic transitions, progressive refinement, and no false readiness. A first authoring increment should therefore create only a safe `DRAFT`, not synthesize fields that might accidentally satisfy Grain readiness.

### Spec Kit interoperability

The v0.1 importer is intentionally read-only and source-bound. Automatically turning imported artifacts into executable native SpecNodes would be a larger migration-policy decision and should not be bundled into first-party authoring.

### Brownfield workflow

`scan` is useful before planning and remains bounded and non-executing. The missing bridge is from repository understanding or user intent into the first native specification artifact.

### WorkPacket and executor workflow

WorkPacket/result contracts exist and are agent-neutral, but CLI orchestration does not expose the full path. Exposing packet/executor commands before users can author native specs would optimize a later stage before the first stage is usable.

### Agent adapters

Generic adapter contracts exist. Provider-specific execution has no adoption evidence and remains intentionally deferred.

### Verification and proof UX

`prove` exposes independent evidence already recorded for a specification. This is valuable after execution but does not address first-use authoring friction.

### SpecGrainBench

The benchmark ledger and comparability preflight exist. No controlled public multi-arm empirical dataset is published, so there is no basis for comparative winner claims. Running a superiority program is not the next adoption-critical Grain.

### Observability, reporting, and visualization

Delivery metrics exist as deterministic APIs. A dashboard or richer visualization could improve comprehension later, but it would add surface area before the core local authoring loop is complete.

### Security and trust

The current trust model is local, deterministic, fail-closed around store parsing, symlinks, imported data, evidence binding, and executor authority. A native authoring command must preserve strict validation, refuse overwrite/races, avoid executing repository content, and avoid silently promoting state beyond `DRAFT`.

### Technical debt and documentation drift

The architecture still describes several commands as future/planned even though some (`scan`, `next`, `prove`) have shipped. This is minor documentation drift worth correcting only when a nearby specification already touches the CLI architecture section; it is not by itself a product frontier.

### Community and ecosystem opportunities

There are no open community issues or PRs to prioritize. The adjacent specification-driven-development ecosystem is active, but SpecGrain should improve its own concrete local loop before adding hosted, model-specific, or broad integration surfaces.

## Candidate frontier comparison

| Candidate | User value now | Scope/risk | Evidence dependency | Decision |
| --- | --- | --- | --- | --- |
| Native root DRAFT CLI | High: makes first native spec possible | Small, deterministic | Existing store/model contracts | **Select** |
| PyPI publication | Medium: easier install | External publishing governance | Trusted publishing setup | Defer |
| Native recursive refine CLI | High after first DRAFT exists | Larger multi-file tree mutation | Needs authoring boundary first | Reassess after 017 |
| WorkPacket/executor CLI | Medium later-stage value | Medium | Needs usable authoring loop | Defer |
| Empirical benchmark program | Potential proof value | High/expensive | Controlled dataset and execution resources | Defer |
| Hosted dashboard/SaaS | Premature | High | Adoption evidence | Defer |
| Provider-specific orchestration | Premature | Medium/high lock-in risk | Adoption evidence | Defer |

## Selected frontier

Shape Specification 017 as **Native DRAFT CLI**.

Its single outcome is that, after `specgrain init`, a user can create one validated root SpecNode in state `DRAFT` through a deterministic supported command without hand-authoring internal JSON.

The specification deliberately excludes child refinement, automatic Grain shaping, lifecycle promotion, WorkPacket generation, execution, verification, provider integration, networking, and package-distribution changes. Those remain future evidence-shaped decisions.
