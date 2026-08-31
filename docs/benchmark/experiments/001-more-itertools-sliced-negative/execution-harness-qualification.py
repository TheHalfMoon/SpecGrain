#!/usr/bin/env python3
"""Fail-closed operator qualification for SGB-EXP-001 before Attempt 003."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import uuid
import zipfile
from pathlib import Path

REV = "ed86a1528aa015f219f8d3385ea2ebd3f63a5212"
ARCHIVE_SHA = "sha256:6bdf91b309f86e4ac755f7ba33504aa7314567b69978ba71e5f0b62e33bbfbc1"
MORE_BLOB = "5607346368e6eb903eac3d50aad9ef65eacd0b01"
TEST_BLOB = "1d2894b4c0dd7ff28f2ff041873f5198dc915699"
IMAGE_DIGEST = "sha256:d410f9a22b896edb5edeaa20ccc920f879c00a78b67f089abb647adf91e68bf8"
IMAGE = "sgbench-runner:exp001@" + IMAGE_DIGEST
MODEL = "claude-fable-5"
CLAUDE_VERSION = "2.1.251"
MORE = Path("more_itertools/more.py")
TEST = Path("tests/test_more.py")


class Blocked(RuntimeError):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code, self.detail = code, detail


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def run(argv: list[str], cwd: Path | None = None, env=None, check=True):
    p = subprocess.run(
        argv, cwd=cwd, env=env, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and p.returncode:
        raise RuntimeError(f"{argv!r} -> {p.returncode}\n{p.stdout}\n{p.stderr}")
    return p


def git_blob(path: Path) -> str:
    return run(["git", "hash-object", str(path)]).stdout.strip()


def extract(archive: Path, dest: Path) -> Path:
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as z:
            root = dest.resolve()
            for member in z.infolist():
                try:
                    (dest / member.filename).resolve().relative_to(root)
                except ValueError as e:
                    raise Blocked("EXTRACTED_BASELINE_FILE_MISMATCH", member.filename) from e
            z.extractall(dest)
    elif tarfile.is_tarfile(archive):
        with tarfile.open(archive) as t:
            root = dest.resolve()
            for m in t.getmembers():
                try:
                    (dest / m.name).resolve().relative_to(root)
                except ValueError as e:
                    raise Blocked("EXTRACTED_BASELINE_FILE_MISMATCH", m.name) from e
            t.extractall(dest)
    else:
        raise Blocked("BASELINE_ARCHIVE_DIGEST_MISMATCH", "unsupported archive format")
    if (dest / MORE).is_file() and (dest / TEST).is_file():
        return dest
    roots = [p for p in dest.iterdir() if p.is_dir() and (p / MORE).is_file() and (p / TEST).is_file()]
    if len(roots) != 1:
        raise Blocked("EXTRACTED_BASELINE_FILE_MISMATCH", "repository root not unique")
    return roots[0]


def has_negative_guard(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "sliced"), None)
    if fn is None:
        raise Blocked("EXTRACTED_BASELINE_FILE_MISMATCH", "sliced() absent")
    source = ast.get_source_segment(text, fn) or ""
    return bool(re.search(r"\bn\s*<\s*0\b|\b0\s*>\s*n\b|\bn\s*<=\s*-1\b", source))


def contamination(root: Path) -> list[str]:
    exact = {".git", ".claude", ".specify", ".specgrain", ".mcp.json", "CLAUDE.md"}
    bad = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        low = p.name.lower()
        if p.name in exact or (len(rel.parts) == 1 and p.name == "specs"):
            bad.append(rel.as_posix())
        elif any(x in low for x in ("sgbench", "attempt-001", "attempt-002", "runner-lock", "cell-plan")):
            bad.append(rel.as_posix())
    return sorted(set(bad))


def context_clean(home: Path, root: Path) -> tuple[bool, dict]:
    evidence = {"ancestor_artifacts": [], "user_config_hits": [], "prior_project_hits": []}
    cur = root.parent
    while True:
        for name in ("CLAUDE.md", ".mcp.json", ".claude"):
            p = cur / name
            if p.exists() and not (cur == home and name == ".claude"):
                evidence["ancestor_artifacts"].append(str(p))
        if cur == home or cur.parent == cur:
            break
        cur = cur.parent
    ch = home / ".claude"
    sensitive = re.compile(r"specgrain|speckit|spec-kit|sgbench|more-itertools|sliced-negative", re.I)
    if ch.exists():
        for p in ch.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".json", ".md", ".toml", ".yaml", ".yml"}:
                continue
            if "projects" in {x.lower() for x in p.parts} or "history" in p.name.lower():
                continue
            try:
                if p.stat().st_size <= 2_000_000 and sensitive.search(p.read_text(encoding="utf-8", errors="replace")):
                    evidence["user_config_hits"].append(str(p))
            except OSError:
                pass
        projects = ch / "projects"
        if projects.exists():
            for p in projects.rglob("*"):
                if root.name.lower() in str(p).lower():
                    evidence["prior_project_hits"].append(str(p))
    for k in evidence:
        evidence[k] = sorted(set(evidence[k]))
    return not any(evidence.values()), evidence


def make_hooks(state: Path) -> tuple[Path, Path, Path]:
    state.mkdir()
    log = state / "events.jsonl"
    hook = state / "hook.py"
    settings = state / "settings.json"
    empty_mcp = state / "mcp.json"
    hook.write_text(
        "import json,os,sys\nfrom pathlib import Path\n"
        "e=json.load(sys.stdin); p=Path(os.environ['SGBENCH_QUAL_LOG'])\n"
        "with p.open('a',encoding='utf-8') as f:f.write(json.dumps({'phase':sys.argv[1],'event':e},sort_keys=True)+'\\n')\n"
        "if sys.argv[1]=='pre' and e.get('tool_name') in {'Edit','Write','MultiEdit'}:\n"
        " print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':'non-mutating qualification probe'}}))\n"
        "else: print('{}')\n",
        encoding="utf-8",
    )
    cmd = lambda phase: f'"{sys.executable}" "{hook}" {phase}'
    settings.write_text(json.dumps({"hooks": {
        "PreToolUse": [{"matcher": "Read|Grep|Glob|Edit|Write|MultiEdit|Bash", "hooks": [{"type": "command", "command": cmd("pre")}]}],
        "PostToolUse": [{"matcher": "Read|Grep|Glob|Bash", "hooks": [{"type": "command", "command": cmd("post")}]}],
    }}, indent=2) + "\n", encoding="utf-8")
    empty_mcp.write_text('{"mcpServers":{}}\n', encoding="utf-8")
    return settings, empty_mcp, log


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def tool_input(rec: dict):
    e = rec.get("event", {})
    return e.get("tool_name"), e.get("tool_input", {}) if isinstance(e.get("tool_input"), dict) else {}


def validate_events(events: list[dict], nonce: str) -> dict[str, bool]:
    pre = [tool_input(x) for x in events if x.get("phase") == "pre"]
    post = {tool_input(x)[0] for x in events if x.get("phase") == "post"}
    read = any(t == "Read" and (i.get("file_path") or i.get("path", "")).replace("\\", "/").endswith(MORE.as_posix()) for t, i in pre)
    grep = any(t == "Grep" and i.get("pattern") == nonce for t, i in pre)
    glob = any(t == "Glob" and nonce in str(i.get("pattern", "")) for t, i in pre)
    edit = any(t in {"Edit", "Write", "MultiEdit"} and nonce in str(i.get("file_path") or i.get("path", "")) for t, i in pre)
    bash = any(t == "Bash" and "git hash-object more_itertools/more.py" in str(i.get("command", "")) for t, i in pre)
    return {
        "claude_read_observes_canonical_workspace": read and "Read" in post,
        "claude_search_observes_canonical_workspace": grep and glob and "Grep" in post and "Glob" in post,
        "claude_edit_targets_canonical_workspace": edit,
        "claude_shell_targets_canonical_workspace": bash and "Bash" in post,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-archive", type=Path, required=True)
    ap.add_argument("--runner-lock-dir", type=Path, required=True)
    ap.add_argument("--qualification-parent", type=Path, default=Path.home())
    ap.add_argument("--runner-image", default=IMAGE)
    ap.add_argument("--harness-launcher", nargs="+")
    a = ap.parse_args()

    qid = str(uuid.uuid4())
    qdir = a.qualification_parent.resolve() / f"sgbench-harness-qualification-{qid}"
    out = qdir / "sgbench-exp001-execution-harness-qualification.json"
    ev = {
        "schema": "sgbench-execution-harness-qualification-v1",
        "repository_revision": REV,
        "baseline_archive_digest": ARCHIVE_SHA,
        "canonical_more_py_git_blob": MORE_BLOB,
        "canonical_test_more_py_git_blob": TEST_BLOB,
        "attempt_002_status": "INVALID_CONTAMINATED",
        "attempt_002_hidden_scorer_revealed": False,
        "attempt_003_status": "NOT_CREATED",
        "hidden_scorer_inspected": False,
        "blockers": [],
    }
    container = None

    def block(code, detail):
        ev["blockers"].append({"code": code, "detail": detail})
        raise Blocked(code, detail)

    try:
        qdir.mkdir(parents=True, exist_ok=False)
        archive = a.baseline_archive.resolve()
        observed = sha256(archive)
        ev["observed_baseline_archive_digest"] = observed
        ev["baseline_archive_digest_match"] = observed == ARCHIVE_SHA
        if not ev["baseline_archive_digest_match"]:
            block("BASELINE_ARCHIVE_DIGEST_MISMATCH", f"observed {observed}")

        root = extract(archive, qdir)
        ev["qualification_host_root"] = str(root.resolve())
        bad = contamination(root)
        ev["forbidden_extracted_artifacts"] = bad
        if bad:
            block("EXTRACTED_BASELINE_FILE_MISMATCH", ", ".join(bad))

        hm, ht = git_blob(root / MORE), git_blob(root / TEST)
        ev["host_more_py_git_blob"], ev["host_test_more_py_git_blob"] = hm, ht
        if (hm, ht) != (MORE_BLOB, TEST_BLOB):
            block("EXTRACTED_BASELINE_FILE_MISMATCH", f"{hm} {ht}")
        ev["baseline_negative_guard_present"] = has_negative_guard(root / MORE)
        if ev["baseline_negative_guard_present"]:
            block("BASELINE_ALREADY_MODIFIED", "negative-size guard present")

        lock_dir = a.runner_lock_dir.resolve()
        runner = json.loads((lock_dir / "runner-lock.json").read_text(encoding="utf-8"))
        envlock = json.loads((lock_dir / "environment-lock.json").read_text(encoding="utf-8"))
        if runner.get("runner", {}).get("version") != CLAUDE_VERSION or runner.get("model_config", {}).get("model") != MODEL:
            block("LOCKED_RUNTIME_MISMATCH", "runner/model lock mismatch")
        if runner.get("runner", {}).get("runner_image_digest") != IMAGE_DIGEST or envlock.get("workspace", {}).get("network_mode") != "none":
            block("LOCKED_RUNTIME_MISMATCH", "image/network lock mismatch")

        docker, claude = shutil.which("docker"), shutil.which("claude")
        ev["docker_executable"], ev["claude_executable"] = docker, claude
        if not docker or not claude:
            block("LOCKED_RUNTIME_MISMATCH", "docker and claude must exist on locked host")
        cv = run([claude, "--version"]).stdout.strip()
        ev["observed_claude_version"] = cv
        if CLAUDE_VERSION not in cv:
            block("LOCKED_RUNTIME_MISMATCH", cv)
        image_json = run([docker, "image", "inspect", a.runner_image]).stdout
        if IMAGE_DIGEST not in image_json:
            block("LOCKED_RUNTIME_MISMATCH", "runner image digest not locally attested")

        container = f"sgbench-harness-qualification-{qid}"
        run([docker, "run", "-d", "--rm", "--name", container, "--network", "none", "-v", f"{root.resolve()}:/workspace", "-w", "/workspace", a.runner_image, "sh", "-lc", "trap : TERM INT; sleep infinity & wait"])
        net = run([docker, "inspect", "--format", "{{.HostConfig.NetworkMode}}", container]).stdout.strip()
        ev["network_mode"] = net
        if net != "none":
            block("LOCKED_RUNTIME_MISMATCH", f"network={net}")
        cm = run([docker, "exec", container, "git", "hash-object", MORE.as_posix()]).stdout.strip()
        ct = run([docker, "exec", container, "git", "hash-object", TEST.as_posix()]).stdout.strip()
        ev["container_more_py_git_blob"], ev["container_test_more_py_git_blob"] = cm, ct
        ev["host_container_workspace_identity"] = (hm, ht, cm, ct) == (MORE_BLOB, TEST_BLOB, MORE_BLOB, TEST_BLOB)
        if not ev["host_container_workspace_identity"]:
            block("HOST_CONTAINER_WORKSPACE_DIVERGENCE", f"{hm} {ht} {cm} {ct}")

        ip = run([docker, "exec", container, "python", "-c", "import json,pathlib,more_itertools,more_itertools.more;print(json.dumps([str(pathlib.Path(more_itertools.__file__).resolve()),str(pathlib.Path(more_itertools.more.__file__).resolve())]))"]).stdout.strip()
        paths = json.loads(ip)
        ev["python_import_paths"] = paths
        ev["python_imports_workspace_copy"] = all(x.startswith("/workspace/") for x in paths)
        if not ev["python_imports_workspace_copy"]:
            block("PYTHON_IMPORT_PATH_CONTAMINATION", repr(paths))

        clean, ctx = context_clean(Path.home().resolve(), root.resolve())
        ev["fresh_context_evidence"] = ctx
        if not clean:
            block("CLAUDE_CONTEXT_ISOLATION_UNPROVEN", "Claude-visible prior/project state found")
        if not a.harness_launcher:
            block("CLAUDE_HARNESS_LAUNCHER_UNAVAILABLE", "exact frozen launcher not supplied; raw Claude substitution forbidden")

        nonce = uuid.uuid4().hex
        sentinel = root / f".sgbench-routing-sentinel-{nonce}.txt"
        sentinel.write_text(f"{nonce}\nROUTING_PROBE_A\n", encoding="utf-8")
        sentinel_sha = sha256(sentinel)
        before = (git_blob(root / MORE), git_blob(root / TEST))
        state = qdir.parent / f"sgbench-qualification-state-{qid}"
        settings, mcp, log = make_hooks(state)
        session = str(uuid.uuid4())
        prompt = (
            "Filesystem routing qualification only. Do not solve or analyze any benchmark task. "
            f"Use Read on more_itertools/more.py; Grep for {nonce}; Glob for .sgbench-routing-sentinel-{nonce}.txt; "
            f"attempt Edit on .sgbench-routing-sentinel-{nonce}.txt replacing ROUTING_PROBE_A with ROUTING_PROBE_B (the hook will deny it; do not retry); "
            "then Bash exactly: pwd && git hash-object more_itertools/more.py && git hash-object tests/test_more.py. Stop."
        )
        env = dict(os.environ); env["SGBENCH_QUAL_LOG"] = str(log.resolve())
        argv = a.harness_launcher + ["--model", MODEL, "--session-id", session, "--settings", str(settings.resolve()), "--strict-mcp-config", "--mcp-config", str(mcp.resolve()), "--tools", "Read,Grep,Glob,Edit,Write,Bash", "--allowedTools", "Read,Grep,Glob,Bash,Edit,Write", "--disallowedTools", "WebSearch,WebFetch", "--print", "--output-format", "json", "--max-turns", "12", prompt]
        cp = run(argv, cwd=root, env=env, check=False)
        ev["claude_probe_exit_code"] = cp.returncode
        ev["claude_probe_stdout"], ev["claude_probe_stderr"] = cp.stdout, cp.stderr
        if cp.returncode:
            block("CLAUDE_FILE_TOOL_ROUTING_CONTAMINATION", f"probe exit {cp.returncode}")
        events = read_events(log)
        flags = validate_events(events, nonce)
        after = (git_blob(root / MORE), git_blob(root / TEST))
        stable = before == after == (MORE_BLOB, TEST_BLOB) and sha256(sentinel) == sentinel_sha
        text = cp.stdout + cp.stderr + "\n" + "\n".join(json.dumps(x) for x in events)
        flags["claude_read_observes_canonical_workspace"] &= stable
        flags["claude_search_observes_canonical_workspace"] &= stable
        flags["claude_shell_targets_canonical_workspace"] &= all(x in text for x in ("/workspace", MORE_BLOB, TEST_BLOB))
        ev.update(flags)
        if not all(flags.values()):
            block("CLAUDE_FILE_TOOL_ROUTING_CONTAMINATION", repr(flags))
        ev["fresh_context_isolation"] = True
        ev["qualification_status"] = "PASS"
        ev["attempt_003_status"] = "READY_TO_CREATE_NOT_CREATED"
        out.write_text(json.dumps(ev, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(out)
        return 0
    except Blocked as e:
        ev["qualification_status"] = "FAIL"
        for k in ("baseline_archive_digest_match", "python_imports_workspace_copy", "host_container_workspace_identity", "claude_read_observes_canonical_workspace", "claude_search_observes_canonical_workspace", "claude_edit_targets_canonical_workspace", "claude_shell_targets_canonical_workspace", "fresh_context_isolation"):
            ev.setdefault(k, False)
        if qdir.exists():
            out.write_text(json.dumps(ev, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(out)
        print(f"BLOCKED: {e.code}: {e.detail}", file=sys.stderr)
        return 2
    except Exception as e:
        ev["qualification_status"] = "FAIL"
        ev["blockers"].append({"code": "QUALIFICATION_HARNESS_ERROR", "detail": repr(e)})
        if qdir.exists():
            out.write_text(json.dumps(ev, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(out)
        print(f"BLOCKED: QUALIFICATION_HARNESS_ERROR: {e!r}", file=sys.stderr)
        return 3
    finally:
        if container and shutil.which("docker"):
            subprocess.run([shutil.which("docker") or "docker", "rm", "-f", container], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


if __name__ == "__main__":
    raise SystemExit(main())
