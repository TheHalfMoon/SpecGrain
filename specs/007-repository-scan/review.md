# Review 007 — Repository Scan

**Review date:** 2026-08-28  
**Reviewed implementation head:** `20d36002720fe5c7183e8e7defd02451c134516f`

## Objective

Verify that Specification 007 adds deterministic bounded brownfield repository facts and standalone scan output without becoming a semantic indexer, executing repository content, following untrusted indirection, mutating project/lifecycle state, or changing dependency scheduling/evidence semantics.

## Exact-diff result

No material implementation defect remains in the reviewed uploaded product head.

The net implementation diff from the 007 planning head is limited to the planned five-file surface:

- `src/specgrain/repository.py`;
- `src/specgrain/cli.py`;
- `src/specgrain/__init__.py`;
- `tests/test_repository.py`;
- `tests/test_repository_cli.py`.

An exact-diff review defect was found and repaired before this review record: selected manifest and Git metadata reads now enforce their byte ceilings during the read itself rather than relying only on a pre-read stat size.

## Structural review

The scanner:

- requires an ordinary existing directory root and rejects root symlinks;
- never follows filesystem symlinks;
- skips the specified VCS/control/vendor/generated directories;
- fails closed when a regular file exceeds the depth/file-count budget;
- reports deterministic repository-relative facts only;
- parses semantic dependency names only from bounded `pyproject.toml`, `package.json`, `Cargo.toml`, and `go.mod` inputs;
- treats recognized manifests, dependencies, components, tests, configs, and languages as conservative signals rather than semantic truth;
- reads ordinary in-repository Git metadata without invoking `git` and never follows `.git` file/symlink indirection;
- computes `content_digest` from normalized map content excluding the digest field itself;
- exposes no absolute root path, timestamp, username, hostname, inode, or mtime in normalized output.

## Trust boundary

The exact net diff contains no:

- AST or semantic repository indexing;
- arbitrary file-content indexing;
- embeddings or LLM/provider calls;
- package/vulnerability resolution;
- subprocess execution;
- symlink or external `gitdir:` following;
- lifecycle/store mutation;
- context selection or token-budget policy;
- evidence-ledger/verification semantics;
- dependency-scheduler behavior change;
- third-party runtime dependency.

## Verification evidence

The exact product/test blobs match the locally verified bytes. Verification is 304 pytest tests PASS, compileall PASS, editable install PASS, console/module help parity PASS, and 0 changed source/test lines over 100 characters. Ruff is NOT RUN because it is unavailable in the execution environment.

## History note

During connector-side upload, temporary probe/staging files were created and then removed by normal forward commits. No force-push, rebase, or destructive history rewriting was used. The final tree and net implementation diff contain none of those temporary files.

## Conclusion

Specification 007 implementation is ready for a bounded pull request after the documentation record commits. Those documentation commits move the branch head beyond the reviewed product commit, so exact-head PR checks/reviews and the final merge guard must bind to the resulting PR head before merge.
