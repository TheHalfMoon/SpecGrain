# Verification — Specification 020 v0.3.0 Recursive Authoring Release

**Verified implementation head:** `d207d54317457a744cb8887a260fcb78dc0710be`  
**Canonical shaping base:** `05219b4ea7ce1be201c8fb2ff31e707ae02cba17`  
**CI run:** `33249652226` — `completed/success`

## Permanent matrix

The exact implementation head passed the permanent five-cell CI matrix:

- Ubuntu / Python 3.11 — job `99093025588` — success;
- Ubuntu / Python 3.12 — job `99093025617` — success;
- Ubuntu / Python 3.13 — job `99093025610` — success;
- macOS / Python 3.11 — job `99093025452` — success;
- Windows / Python 3.11 — job `99093025594` — success.

## Exact-head evidence

Ubuntu/Python 3.11 job `99093025588` checked out exact head `d207d54317457a744cb8887a260fcb78dc0710be` and recorded:

- Ruff source: success;
- Ruff tests: success;
- Ruff examples: success;
- editable install of `specgrain-0.3.0`: success;
- full regression: `555 passed in 1.46s`;
- tracked-tree unchanged check: success;
- `python -m compileall -q src tests examples`: success;
- module and installed CLI help parity: success, listing `init`, `draft`, `recover`, `check`, `next`, `scan`, `prove`, and `import-spec-kit`;
- package build: `specgrain-0.3.0.tar.gz` and `specgrain-0.3.0-py3-none-any.whl` built successfully;
- built-wheel reinstall with `--no-deps`: success;
- installed CLI smoke: success.

The runtime dependency list remains empty in `pyproject.toml`.

## Publication boundary

This verification proves the release candidate on the exact implementation head. It does not prove publication. No `RELEASED` claim is authorized until an expected-head product merge, successful canonical post-merge CI, and live `v0.3.0` tag/GitHub Release/asset evidence satisfy T012–T013.
