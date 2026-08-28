# ADR-0014 — Generic Agent Adapter Boundary

## Status

Accepted for Specification 014.

## Decision

SpecGrain will keep `WorkPacket` and `ExecutionResult` as the canonical execution protocol. Agent adapters are deterministic translation helpers around those contracts; they are not executors and never gain verification authority.

Specification 014 will implement only generic JSON and Markdown request envelopes plus strict result normalization. It will not add a vendor SDK, subprocess invocation, network client, credential handling, agent discovery, or provider-specific state.

Vendor-specific coding-agent adapters remain deferred until repository evidence demonstrates real adoption demand and a stable integration contract worth maintaining.

## Consequences

- the same WorkPacket digest survives every adapter representation;
- external agents cannot choose or spoof the packet digest when results are normalized;
- adapter output is deterministic and portable;
- executor self-report remains subject to Specification 010 independent verification;
- future provider adapters can wrap the generic boundary without changing the kernel.
