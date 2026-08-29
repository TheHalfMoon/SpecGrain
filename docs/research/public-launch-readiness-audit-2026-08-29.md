# Public Launch Readiness Audit — 2026-08-29

**Audit source revision:** `1ea1ee8554ce84f96f67d12eb86188324c81534a`  
**Published release:** `v0.3.0`, GitHub Release `378962445`

## Purpose

Re-evaluate the public repository surface after the v0.3.0 program entered `POST_V0.3_OBSERVATION`, prompted by an explicit maintainer request to make the repository launch-ready and professional across discoverability, licensing, security, documentation, community entry points, CI, and release presentation.

This audit is evidence for bounded shaping. It does not authorize product behavior, lifecycle, execution, hosted, PyPI, benchmark, or provider scope.

## Live findings

| Surface | Live evidence | Assessment |
| --- | --- | --- |
| Repository description | GitHub repository metadata reports `description: null` | **Gap — platform discoverability** |
| Repository topics | GitHub repository metadata reports `topics: []` | **Gap — platform discoverability** |
| Homepage | GitHub repository metadata reports no homepage | Optional; no standalone documentation site exists, so no value should be invented |
| License | GitHub recognizes `MIT`; root `LICENSE` contains the MIT text and `pyproject.toml` declares `license = "MIT"` plus `license-files = ["LICENSE"]` | **Pass** |
| Package keywords | `pyproject.toml` declares `specification`, `software-delivery`, `ai-agents`, `verification`, and `devtools` | **Pass for package metadata**; GitHub topics remain absent |
| README | Current v0.3.0 installation and supported CLI are truthful; contribution/security/license links exist | **Pass with presentation polish opportunity** |
| Security policy | `SECURITY.md` still lists `0.1.x` as the supported line after v0.3.0 publication | **Defect — stale public support policy** |
| Launch strategy | `docs/launch-strategy.md` still presents a `v0.1.0 launch demo` | **Defect — stale public launch guidance** |
| Community files | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, bug/feature templates, and PR template are present | **Pass** |
| Changelog/release notes | `CHANGELOG.md` is current through v0.3.0 and versioned v0.1/v0.2/v0.3 release notes exist | **Pass** |
| CI | Permanent Ubuntu 3.11/3.12/3.13, macOS 3.11, Windows 3.11 matrix exists with read-only repository permissions | **Pass** |
| Release automation | Publication is metadata-derived, bound to successful canonical `main` CI, and historical releases are immutable-by-contract | **Pass** |
| Branch protection | `main` reports `protected: false`; repository rulesets list is empty | **Residual platform-governance risk** |

## Repository-side corrections selected

The smallest evidence-supported repository change is documentation/test hardening only:

1. correct the public supported-version table to the current `0.3.x` line while making the older-line policy explicit;
2. refresh `docs/launch-strategy.md` to the current v0.3.0 release and public installation path;
3. sharpen the README first-screen presentation with current-release, Python, and MIT signals while preserving exact capability/trust boundaries;
4. add regression checks so the license file remains part of the public launch surface and stale security/launch-version text cannot silently return.

No package version bump is needed because no packaged product metadata or runtime behavior changes. The existing `v0.3.0` release remains a historical identity and later `main` CI may only verify it without mutation.

## Canonical GitHub metadata target

Repository settings should use the following concise public metadata when applied through GitHub settings:

**Description**

> Deterministic, agent-neutral delivery control plane for turning software work into small, bounded, independently verifiable changes.

**Topics**

- `spec-driven-development`
- `ai-agents`
- `coding-agents`
- `developer-tools`
- `software-delivery`
- `software-engineering`
- `verification`
- `cli`
- `python`
- `spec-kit`

These settings are platform metadata, not file-backed repository state. They must not be claimed as applied until live GitHub metadata proves them.

## Recommended `main` governance target

The repository currently has no branch protection/ruleset. A future GitHub-settings operation should prefer a minimal solo-maintainer-safe rule set:

- require changes to enter `main` through pull requests;
- require the configured CI checks before merge;
- require conversation resolution;
- block force pushes and branch deletion;
- keep expected-head merge checks in the repository workflow;
- avoid mandatory external reviewer approval while the project has a single maintainer unless governance changes.

This is a platform-governance recommendation, not implementation authority for hidden settings mutation.

## Decision

The maintainer request plus the two reproducible stale public documents are sufficient fresh evidence to shape **Specification 021 — Public Launch Readiness Hardening**.

Specification 021 is intentionally narrow. It corrects public truth and launch presentation without changing `src/specgrain/`, package version, runtime dependencies, release workflow, historical releases, lifecycle/readiness/execution authority, PyPI scope, hosted surfaces, or benchmark claims.
