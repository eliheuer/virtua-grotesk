"""Project-local TTF/OTF references shared with Runebender's native proof.

This module reads font metadata only. It never downloads fonts or changes sources.
"""
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import time
from fontTools.ttLib import TTFont

MAX_BYTES = 32 * 1024 * 1024
CACHE_GRACE_SECONDS = 300


def prune_reference_cache(target, stale_since, now):
    """Remove only obsolete, intact generated copies after a five-minute grace.

    Both manifests pin their files: a new tab may still load the startup data
    before its first reference poll. Never follow symlinks or prune an archive.
    The caller opts in only for the generated live directory.
    """
    try:
        live = json.loads((target / 'live-fonts.json').read_text())
        raw = (target / 'review-data.js').read_text()
        startup = json.loads(raw[raw.index('=') + 1:].strip().removesuffix(';'))['fonts']
        keep = {face['url'] for manifest in (live, startup)
                for record in manifest.values() for face in record.get('faces', [record])}
        folder = target / 'fonts'
        if target.is_symlink() or folder.is_symlink():
            return []
        candidates = list(folder.iterdir())
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        # An incomplete or externally prepared manifest is not permission to delete.
        return []
    removed, obsolete = [], set()
    for path in candidates:
        match = re.fullmatch(r'reference-([0-9a-f]{64})\.(ttf|otf)', path.name)
        if not match or path.is_symlink() or not path.is_file():
            continue
        if f'fonts/{path.name}' in keep:
            stale_since.pop(path.name, None)
            continue
        obsolete.add(path.name)
        since = stale_since.setdefault(path.name, now)
        if now - since < CACHE_GRACE_SECONDS:
            continue
        try:
            if hashlib.sha256(path.read_bytes()).hexdigest() != match[1]:
                continue
            path.unlink()
            removed.append(path.name)
        except OSError:
            continue
    for name in list(stale_since):
        if name not in obsolete or name in removed:
            stale_since.pop(name, None)
    return removed


def reference_directory(document):
    document = Path(document).resolve()
    parent = document.parent if document.suffix.lower() in ('.ufo', '.designspace', '.glyphs', '.ttf', '.otf') or document.is_file() else document
    root = next((p for p in [parent, *parent.parents] if (p / '.git').exists()), parent)
    return root / 'reference-fonts'


def font_paths(folder):
    if not folder.exists():
        return []
    paths = []
    def visit(directory):
        for path in sorted(directory.iterdir()):
            if path.name.startswith('.') or path.is_symlink():
                continue
            if path.is_dir():
                visit(path)
            elif path.suffix.lower() in ('.ttf', '.otf'):
                paths.append(path)
    visit(folder)
    return sorted(paths)


def collect(folder, target):
    """Return deterministic families, per-face coverage and errors; copy verified bytes for serving."""
    families, errors, seen = {}, [], set()
    try:
        paths = font_paths(folder)
    except OSError as error:
        return {'fonts': {}, 'errors': [str(error)]}
    for path in paths:
        try:
            if path.stat().st_size > MAX_BYTES:
                raise ValueError('font exceeds 32 MiB')
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen:
                continue
            with TTFont(io.BytesIO(raw)) as font:
                names = font['name']
                family = names.getDebugName(16) or names.getDebugName(1)
                if not family:
                    raise ValueError('missing family name')
                os2 = font['OS/2']
                italic = bool(os2.fsSelection & (1 | 512))
                width = os2.usWidthClass
                label = family + (f' · Width {width}' if width != 5 else '') + (' Italic' if italic else '')
                key = (family.lower(), width, italic)
                axes = {a.axisTag: [a.minValue, a.defaultValue, a.maxValue] for a in font['fvar'].axes} if 'fvar' in font else {}
                weights = axes.get('wght', [os2.usWeightClass] * 3)
                if not all(math.isfinite(value) for value in weights) or weights[0] > weights[2]:
                    raise ValueError('invalid weight range')
                face = dict(sha256=digest, url=f'fonts/reference-{digest}{path.suffix.lower()}',
                            path=path.relative_to(folder).as_posix(), axes=axes,
                            minWeight=weights[0], maxWeight=weights[2],
                            weight=str(os2.usWeightClass), codepoints=sorted(cp for cp, glyph in (font.getBestCmap() or {}).items() if font.getGlyphID(glyph) != 0))
            destination = target / face['url']
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists() or hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
                # Write the bytes we hashed, not a second read of a potentially changing source.
                destination.write_bytes(raw)
            record = families.setdefault(key, dict(family=label, sourceFamily=family, label=label, reference=True, faces=[]))
            record['faces'].append(face)
            seen.add(digest)
        except Exception as error:
            errors.append(f'{path.relative_to(folder)}: {error}')
    fonts = {f'reference-{index}': families[key] for index, key in enumerate(sorted(families))}
    return dict(fonts=fonts, errors=errors)


class ReferenceCache:
    """Stat on each poll, parse/copy only when the directory contents have changed."""
    def __init__(self, folder, target, base_fonts=None, *, prune=False):
        self.folder, self.target = folder, target
        self.base_fonts = base_fonts
        self.signature, self.value = None, None
        self.prune, self.stale_since = prune, {}

    def get(self):
        try:
            signature = [(str(p), p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ctime_ns) for p in font_paths(self.folder)]
        except OSError as error:
            signature = str(error)
        if signature != self.signature:
            self.value = collect(self.folder, self.target)
            self.value['revision'] = hashlib.sha256(json.dumps(self.value, sort_keys=True).encode()).hexdigest()
            if self.base_fonts is not None:
                base_fonts = self.base_fonts
                if self.signature is not None:
                    # Another prepare run may have advanced the verified snapshots.
                    # Refreshing references must not restore this server's old revisions.
                    current = json.loads((self.target / 'live-fonts.json').read_text())
                    base_fonts = {key: value for key, value in current.items() if key in ('before', 'after')}
                manifest = {**base_fonts, **self.value['fonts']}
                temporary = self.target / '.live-fonts.json.partial'
                temporary.write_text(json.dumps(manifest, indent=2) + '\n')
                temporary.replace(self.target / 'live-fonts.json')
            self.signature = signature
        if self.prune:
            prune_reference_cache(self.target, self.stale_since, time.monotonic())
        return self.value


def prepare_live(snapshot, target, project):
    """Use frozen Before/Working with today's UI and local references; leave the archive untouched."""
    raw = (snapshot / 'review-data.js').read_text()
    data = json.loads(raw[raw.index('=') + 1:].strip().removesuffix(';'))
    state_path = project / 'design/reviews/current.json'
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if snapshot.resolve() == (project / state['proof_snapshot']).resolve():
            data['fonts']['after']['label'] = state['proof_label']
            data.setdefault('study', {})['status'] = state['proof_label']
            data['study']['note'] = state['summary']
            data['reviewState'] = dict(verdict=state['proof_verdict'], summary=state['summary'])
    target.mkdir(parents=True, exist_ok=True)
    data['fonts'] = {key: value for key, value in data['fonts'].items() if key in ('before', 'after')}
    for record in data['fonts'].values():
        for face in record.get('faces', [record]):
            source = (snapshot / face['url']).resolve()
            if not source.is_relative_to(snapshot.resolve()):
                raise ValueError('Snapshot font is outside its archive')
            raw = source.read_bytes()
            if hashlib.sha256(raw).hexdigest() != face['sha256']:
                raise ValueError('Snapshot font hash differs from the archive')
            destination = target / face['url']
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
    shutil.copy2(snapshot / 'fonts/labels.ttf', target / 'fonts/labels.ttf')
    cache = ReferenceCache(reference_directory(project), target, dict(data['fonts']))
    references = cache.get()
    data['fonts'].update(references['fonts'])
    data['referenceErrors'] = references['errors']
    data['referenceRevision'] = references['revision']
    data['referenceEndpoint'] = 'references.json'
    (target / 'review-data.js').write_text('window.REVIEW_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n')
    (target / 'live-fonts.json').write_text(json.dumps(data['fonts'], indent=2) + '\n')
    for name in ['index.html', 'review.css', 'review.js', 'reference-selection.js']:
        shutil.copy2(Path(__file__).parent / name, target / name)
    # Enable only after both startup manifests have been replaced successfully.
    cache.prune = True
    return cache
