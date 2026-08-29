# Security Policy

## Supported versions

| Version | Security fixes |
| --- | --- |
| 0.1.x | Supported |
| < 0.1 | Not released/supported |

## Reporting a vulnerability

Do not post exploit details, secrets, or sensitive reproduction data in a public issue.

If the repository Security tab offers private vulnerability reporting, use **Report a vulnerability** there. If private reporting is not available, open a minimal public issue that asks maintainers to establish a private reporting channel; do not include exploit details in that issue.

A useful private report includes the affected version/revision, impacted component, reproduction steps, expected vs observed behavior, realistic impact, and any proposed mitigation.

## Security boundaries worth testing

SpecGrain is a local deterministic control plane. High-value security reports include bypasses involving:

- symlink or path traversal protections;
- bounded repository/source/evidence reads;
- malformed or duplicate JSON handling;
- digest/revision binding;
- unauthorized change-surface acceptance;
- forged evidence chains;
- unsafe Spec Kit import paths;
- agent-result fields that could manufacture verification authority;
- unintended command, network, or provider execution from deterministic core paths.

## Non-claims

SpecGrain does not make an executor, repository, or agent trustworthy by itself. Verification quality depends on independent checks and the correctness of the implementation revision being bound. See [`docs/trust-model.md`](docs/trust-model.md).
