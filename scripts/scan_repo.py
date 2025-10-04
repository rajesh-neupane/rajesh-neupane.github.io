#!/usr/bin/env python3
"""
Repository folder-structure scanner for the Jekyll site.
Creates a report highlighting potential issues: missing important directories, files with spaces, large files, markdown files missing YAML front matter, duplicate post slugs, and uncommitted changes summary.
"""
import os
import sys
import stat
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'scan-report.txt'

IGNORED_DIRS = {'.git', '.github', '_site', 'node_modules', '.sass-cache'}
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open('rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def find_markdown_missing_frontmatter(root: Path):
    missing = []
    for p in root.rglob('*.md'):
        if any(part in IGNORED_DIRS for part in p.parts):
            continue
        try:
            with p.open('r', encoding='utf-8') as f:
                first = f.read(400)
                if not first.lstrip().startswith('---'):
                    missing.append(str(p.relative_to(root)))
        except Exception:
            missing.append(str(p.relative_to(root)) + ' (readerror)')
    return missing


def find_files_with_spaces(root: Path):
    return [str(p.relative_to(root)) for p in root.rglob('*') if ' ' in p.name and not p.is_dir() and not any(part in IGNORED_DIRS for part in p.parts)]


def find_large_files(root: Path, limit=MAX_FILE_BYTES):
    out = []
    for p in root.rglob('*'):
        if p.is_file() and not any(part in IGNORED_DIRS for part in p.parts):
            try:
                if p.stat().st_size > limit:
                    out.append((str(p.relative_to(root)), p.stat().st_size))
            except Exception:
                continue
    return out


def find_missing_important_dirs(root: Path):
    must = ['_posts', '_pages', '_sass', '_includes']
    missing = [d for d in must if not (root / d).exists()]
    return missing


def find_duplicate_post_slugs(root: Path):
    slugs = {}
    for p in root.glob('_posts/*.md'):
        name = p.name
        # typical Jekyll post: YEAR-MONTH-DAY-title.md
        parts = name.split('-', 3)
        slug = parts[-1] if len(parts) >= 4 else name
        slug = slug.lower()
        slugs.setdefault(slug, []).append(str(p.relative_to(root)))
    return {k: v for k, v in slugs.items() if len(v) > 1}


def git_uncommitted(root: Path):
    try:
        out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=str(root), text=True)
        return out.strip().splitlines()
    except Exception:
        return ['(git not available)']


def small_report():
    root = ROOT
    lines = []
    lines.append(f'Repository scan for: {root}\n')

    missing = find_markdown_missing_frontmatter(root)
    if missing:
        lines.append('Markdown files missing YAML front matter:')
        lines.extend('  - ' + m for m in missing[:50])
    else:
        lines.append('All markdown files have front matter (or none were found).')

    spaces = find_files_with_spaces(root)
    if spaces:
        lines.append('\nFiles with spaces in their names:')
        lines.extend('  - ' + s for s in spaces[:50])

    large = find_large_files(root)
    if large:
        lines.append('\nLarge files (>5MB):')
        lines.extend(f'  - {n} ({size/1024/1024:.1f} MB)' for n, size in large[:50])

    dup = find_duplicate_post_slugs(root)
    if dup:
        lines.append('\nDuplicate post slugs (possibly conflicting post filenames):')
        for slug, files in dup.items():
            lines.append('  - ' + slug)
            for f in files:
                lines.append('      * ' + f)

    lines.append('\nUncommitted git changes:')
    for l in git_uncommitted(root):
        lines.append('  ' + l)

    return '\n'.join(lines)


def main():
    txt = small_report()
    print(txt)
    try:
        REPORT.write_text(txt, encoding='utf-8')
        print('\nSaved report to', REPORT)
    except Exception as e:
        print('Could not write report:', e, file=sys.stderr)


if __name__ == '__main__':
    main()
