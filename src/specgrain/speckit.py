"""Explicit read-only migration from bounded GitHub Spec Kit artifacts."""
from __future__ import annotations
import hashlib, json, os, re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
SPECKIT_IMPORT_VERSION = 1
DEFAULT_ARTIFACT_LIMIT_BYTES = 1048576
ROLES = {
    'spec.md': 'spec',
    'plan.md': 'plan',
    'tasks.md': 'tasks',
    'constitution.md': 'constitution',
}
HEADING = re.compile('^(#{1,6})\\s+(.+?)\\s*$')
STORY = re.compile('^User Story\\s+\\d+\\s+-\\s+(.+?)\\s+\\(Priority:\\s*([^)]+)\\)\\s*$')
ITEM = re.compile('^-\\s+\\*\\*([A-Z]+-\\d+)\\*\\*:\\s*(.+?)\\s*$')
TASK = re.compile(
    r'^-\s+\[(?P<mark>[ xX])\]\s+(?P<id>T\d+)\s+'
    r'(?:(?P<p>\[P\])\s+)?(?:(?P<s>\[US\d+\])\s+)?(?P<d>.+?)\s*$'
)
FIELD = re.compile('^\\*\\*([^*]+)\\*\\*:\\s*(.+?)\\s*$')
COMMENT = re.compile('<!--.*?-->', re.DOTALL)

class SpecKitImportError(ValueError):
    pass

@dataclass(frozen=True, slots=True, order=True)
class SourceArtifact:
    role: str
    path: str
    size_bytes: int
    content_digest: str

    def to_dict(self):
        return {
            'content_digest': self.content_digest,
            'path': self.path,
            'role': self.role,
            'size_bytes': self.size_bytes,
        }

@dataclass(frozen=True, slots=True, order=True)
class ImportedStory:
    title: str
    priority: str
    independent_test: str

    def to_dict(self):
        return {
            'independent_test': self.independent_test,
            'priority': self.priority,
            'title': self.title,
        }

@dataclass(frozen=True, slots=True, order=True)
class ImportedItem:
    item_id: str
    text: str

    def to_dict(self):
        return {'id': self.item_id, 'text': self.text}

@dataclass(frozen=True, slots=True, order=True)
class TechnicalContextField:
    name: str
    value: str

    def to_dict(self):
        return {'name': self.name, 'value': self.value}

@dataclass(frozen=True, slots=True, order=True)
class LegacyTask:
    task_id: str
    description: str
    completed: bool
    parallel: bool
    story_id: str | None = None

    def to_dict(self):
        d = {
            'completed': self.completed,
            'description': self.description,
            'parallel': self.parallel,
            'task_id': self.task_id,
        }
        if self.story_id is not None:
            d['story_id'] = self.story_id
        return d

@dataclass(frozen=True, slots=True, order=True)
class ImportNotice:
    code: str
    message: str
    source_path: str

    def to_dict(self):
        return {'code': self.code, 'message': self.message, 'source_path': self.source_path}

@dataclass(frozen=True, slots=True)
class SpecKitImportReport:
    source_revision: str
    feature_name: str
    feature_branch: str | None
    status: str | None
    source_artifacts: tuple[SourceArtifact, ...]
    stories: tuple[ImportedStory, ...]
    functional_requirements: tuple[ImportedItem, ...]
    success_criteria: tuple[ImportedItem, ...]
    assumptions: tuple[str, ...]
    technical_context: tuple[TechnicalContextField, ...]
    constitution_checks: tuple[str, ...]
    legacy_tasks: tuple[LegacyTask, ...]
    notices: tuple[ImportNotice, ...]

    @property
    def tasks_promoted_to_core(self):
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            'assumptions': list(self.assumptions),
            'constitution_checks': list(self.constitution_checks),
            'feature_branch': self.feature_branch,
            'feature_name': self.feature_name,
            'functional_requirements': [
                x.to_dict() for x in self.functional_requirements
            ],
            'legacy_tasks': [x.to_dict() for x in self.legacy_tasks],
            'notices': [x.to_dict() for x in self.notices],
            'source_artifacts': [x.to_dict() for x in self.source_artifacts],
            'source_revision': self.source_revision,
            'status': self.status,
            'stories': [x.to_dict() for x in self.stories],
            'success_criteria': [x.to_dict() for x in self.success_criteria],
            'tasks_promoted_to_core': False,
            'technical_context': [x.to_dict() for x in self.technical_context],
            'version': SPECKIT_IMPORT_VERSION,
        }

    @property
    def digest(self):
        b = json.dumps(
            self.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            separators=(',', ':'),
            allow_nan=False,
        ).encode()
        return f'sha256:{hashlib.sha256(b).hexdigest()}'

@dataclass(frozen=True, slots=True)
class _Section:
    level: int
    title: str
    body: tuple[str, ...]

def _text(v, field):
    if not isinstance(v, str) or not v.strip():
        raise SpecKitImportError(f'{field} must be non-empty text')
    return v.strip()

def _path(v):
    s = _text(v, 'artifact path')
    if '\\' in s:
        raise SpecKitImportError('artifact paths must use POSIX separators')
    p = PurePosixPath(s)
    if p.is_absolute() or '..' in p.parts or s.startswith('./'):
        raise SpecKitImportError('artifact path must be normalized and repository-relative')
    return p.as_posix()

def _role(p):
    try:
        return ROLES[PurePosixPath(p).name]
    except KeyError as e:
        raise SpecKitImportError(f'unsupported Spec Kit artifact: {p}') from e

def _artifact(p, c):
    b = c.encode()
    return SourceArtifact(_role(p), p, len(b), f'sha256:{hashlib.sha256(b).hexdigest()}')

def _sections(text):
    out = []
    level = 0
    title = '__preamble__'
    body = []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            out.append(_Section(level, title, tuple(body)))
            level = len(m.group(1))
            title = m.group(2).strip()
            body = []
        else:
            body.append(line)
    out.append(_Section(level, title, tuple(body)))
    return tuple(out)

def _section(ss, title):
    return next((x for x in ss if x.title == title), None)

def _lines(body):
    return tuple((x.strip() for x in COMMENT.sub('', '\n'.join(body)).splitlines() if x.strip()))

def _meta(text, label):
    m = re.search(f'^\\*\\*{re.escape(label)}\\*\\*:\\s*(.+?)\\s*$', COMMENT.sub('', text), re.M)
    return None if not m else m.group(1).strip().strip('`') or None

def _feature(text):
    for line in COMMENT.sub('', text).splitlines():
        m = re.match('^#\\s+Feature Specification:\\s*(.+?)\\s*$', line.strip())
        if m:
            name = m.group(1).strip()
            if not name or name.startswith('['):
                raise SpecKitImportError('spec.md contains an unresolved feature-name placeholder')
            return name
    raise SpecKitImportError("spec.md is missing '# Feature Specification:' heading")

def _stories(ss):
    out = []
    for sec in ss:
        m = STORY.match(sec.title)
        if not m:
            continue
        val = next(
            (
                x[len('**Independent Test**:'):].strip()
                for x in _lines(sec.body)
                if x.startswith('**Independent Test**:')
            ),
            None,
        )
        if not val or val.startswith('['):
            raise SpecKitImportError(f'user story {m.group(1)!r} lacks a concrete Independent Test')
        out.append(ImportedStory(m.group(1).strip(), m.group(2).strip(), val))
    return tuple(out)

def _items(sec, prefix):
    if sec is None:
        return ()
    out = []
    seen = set()
    for line in _lines(sec.body):
        m = ITEM.match(line)
        if not m or not m.group(1).startswith(prefix):
            continue
        i, t = (m.group(1), m.group(2).strip())
        if i in seen:
            raise SpecKitImportError(f'duplicate {i} in source artifact')
        if '[' in t and ']' in t:
            raise SpecKitImportError(f'{i} contains an unresolved placeholder')
        seen.add(i)
        out.append(ImportedItem(i, t))
    return tuple(out)

def _assumptions(sec):
    if sec is None:
        return ()
    return tuple(
        x[2:].strip()
        for x in _lines(sec.body)
        if x.startswith('- ') and not x[2:].strip().startswith('[')
    )

def _context(sec):
    if sec is None:
        return ()
    out = []
    for line in _lines(sec.body):
        m = FIELD.match(line)
        if (
            m
            and not m.group(2).strip().startswith('[')
            and 'NEEDS CLARIFICATION' not in m.group(2)
        ):
            out.append(TechnicalContextField(m.group(1).strip(), m.group(2).strip()))
    return tuple(sorted(out))

def _checks(sec):
    if sec is None:
        return ()
    return tuple(x for x in _lines(sec.body) if not x.startswith(('*', '[')))

def _tasks(text):
    out = []
    seen = set()
    for line in COMMENT.sub('', text).splitlines():
        m = TASK.match(line.strip())
        if not m:
            continue
        i = m.group('id')
        if i in seen:
            raise SpecKitImportError(f'duplicate legacy task {i}')
        seen.add(i)
        s = m.group('s')
        out.append(
            LegacyTask(
                i,
                m.group('d').strip(),
                m.group('mark').lower() == 'x',
                bool(m.group('p')),
                None if s is None else s.strip('[]'),
            )
        )
    return tuple(out)

def import_spec_kit_artifacts(
    artifacts: Mapping[str, str],
    *,
    source_revision: str,
    max_artifact_bytes: int = DEFAULT_ARTIFACT_LIMIT_BYTES,
) -> SpecKitImportReport:
    rev = _text(source_revision, 'source_revision')
    if (
        isinstance(max_artifact_bytes, bool)
        or not isinstance(max_artifact_bytes, int)
        or max_artifact_bytes <= 0
    ):
        raise SpecKitImportError('max_artifact_bytes must be a positive integer')
    if not isinstance(artifacts, Mapping) or not artifacts:
        raise SpecKitImportError('artifacts must be a non-empty mapping')
    norm = {}
    roles = {}
    for raw, c in artifacts.items():
        p = _path(raw)
        if not isinstance(c, str):
            raise SpecKitImportError(f'artifact {p} must be UTF-8 text')
        r = _role(p)
        if len(c.encode()) > max_artifact_bytes:
            raise SpecKitImportError(f'{p} exceeds {max_artifact_bytes} bytes')
        if r in roles:
            raise SpecKitImportError(f'multiple artifacts claim role {r!r}: {roles[r]} and {p}')
        roles[r] = p
        norm[p] = c
    if 'spec' not in roles:
        raise SpecKitImportError('spec.md is required for Spec Kit migration')
    sp = roles['spec']
    st = norm[sp]
    ss = _sections(st)
    pt = norm.get(roles.get('plan', ''), '')
    ps = _sections(pt) if pt else ()
    tt = norm.get(roles.get('tasks', ''), '')
    stories = _stories(ss)
    tasks = _tasks(tt) if tt else ()
    notices = []
    if tasks:
        notices.append(
            ImportNotice(
                'LEGACY_TASKS_PRESERVED_NOT_CORE',
                'Spec Kit tasks are preserved in the conversion report and are not '
                'promoted to the SpecGrain core ontology.',
                roles['tasks'],
            )
        )
    if 'constitution' in roles:
        notices.append(
            ImportNotice(
                'CONSTITUTION_SOURCE_BOUND',
                'The constitution artifact is preserved by exact source digest; policy '
                'adoption requires explicit repository governance review.',
                roles['constitution'],
            )
        )
    if not stories:
        notices.append(
            ImportNotice(
                'NO_USER_STORIES_EXTRACTED',
                'No canonical Spec Kit user-story headings were extracted; inspect the '
                'source artifact before mapping delivery slices.',
                sp,
            )
        )
    notices.append(
        ImportNotice(
            'SPEC_SOURCE_PARTIALLY_MAPPED',
            'Selected independently testable stories, requirements, outcomes, and '
            'assumptions are mapped; other spec content remains bound to the source '
            'artifact digest for explicit manual migration review.',
            sp,
        )
    )
    if 'plan' in roles:
        notices.append(
            ImportNotice(
                'PLAN_SOURCE_PARTIALLY_MAPPED',
                'Technical Context and Constitution Check are mapped; other plan content '
                'remains bound to the source artifact digest for explicit manual migration review.',
                roles['plan'],
            )
        )
    return SpecKitImportReport(
        rev,
        _feature(st),
        _meta(st, 'Feature Branch'),
        _meta(st, 'Status'),
        tuple(sorted(_artifact(p, c) for p, c in norm.items())),
        stories,
        _items(_section(ss, 'Functional Requirements'), 'FR-'),
        _items(_section(ss, 'Measurable Outcomes'), 'SC-'),
        _assumptions(_section(ss, 'Assumptions')),
        _context(_section(ps, 'Technical Context')),
        _checks(_section(ps, 'Constitution Check')),
        tasks,
        tuple(sorted(notices)),
    )

def _read(path: Path, limit: int) -> str:
    try:
        if path.is_symlink() or not path.is_file():
            raise SpecKitImportError(f'{path.name} must be an ordinary file')
        with path.open('rb') as f:
            data = f.read(limit + 1)
    except OSError as e:
        raise SpecKitImportError(f'cannot read {path.name}') from e
    if len(data) > limit:
        raise SpecKitImportError(f'{path.name} exceeds {limit} bytes')
    try:
        return data.decode()
    except UnicodeDecodeError as e:
        raise SpecKitImportError(f'{path.name} must be UTF-8 text') from e

def load_spec_kit_feature(
    feature_dir: str | os.PathLike[str],
    *,
    source_revision: str,
    constitution_path: str | os.PathLike[str] | None = None,
    max_artifact_bytes: int = DEFAULT_ARTIFACT_LIMIT_BYTES,
) -> SpecKitImportReport:
    if (
        isinstance(max_artifact_bytes, bool)
        or not isinstance(max_artifact_bytes, int)
        or max_artifact_bytes <= 0
    ):
        raise SpecKitImportError('max_artifact_bytes must be a positive integer')
    root = Path(feature_dir)
    try:
        if root.is_symlink() or not root.is_dir():
            raise SpecKitImportError('feature_dir must be an ordinary directory')
    except OSError as e:
        raise SpecKitImportError('feature_dir must be an ordinary directory') from e
    a = {}
    for name in ('spec.md', 'plan.md', 'tasks.md'):
        p = root / name
        if name == 'spec.md' or p.exists():
            a[name] = _read(p, max_artifact_bytes)
    if constitution_path is not None:
        a['constitution.md'] = _read(Path(constitution_path), max_artifact_bytes)
    return import_spec_kit_artifacts(
        a,
        source_revision=source_revision,
        max_artifact_bytes=max_artifact_bytes,
    )
