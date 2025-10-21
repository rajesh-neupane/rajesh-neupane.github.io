#!/usr/bin/env python3
"""Normalize markdown files in _publications to ensure valid YAML front matter and common keys.
This script:
- Creates a .bak for each file if not present
- Ensures front matter starts/ends with ---
- Parses YAML front matter and ensures keys: title, collection, date, permalink, venue, citation (if present)
- Writes updated file preserving body
"""
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB_DIR = ROOT / '_publications'

DEFAULTS = {
    'collection': 'publications'
}

for p in sorted(PUB_DIR.glob('*.md')):
    txt = p.read_text(encoding='utf-8')
    # backup
    bak = p.with_suffix(p.suffix + '.bak')
    if not bak.exists():
        bak.write_text(txt, encoding='utf-8')
    # strip any leading/trailing code fences
    lines = txt.splitlines()
    if lines and lines[0].startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].startswith('```'):
        lines = lines[:-1]
    # find front matter
    if len(lines) >= 1 and lines[0].strip() == '---':
        # find end
        try:
            end = lines[1:].index('---') + 1
            fm_lines = lines[1:end]
            body_lines = lines[end+1:]
        except ValueError:
            # no end marker, treat as missing
            fm_lines = []
            body_lines = lines
    else:
        fm_lines = []
        body_lines = lines
    fm_text = '\n'.join(fm_lines)
    try:
        fm = yaml.safe_load(fm_text) if fm_text.strip() else {}
        if fm is None:
            fm = {}
    except Exception as e:
        print('YAML parse error in', p, e)
        fm = {}
    # ensure required keys
    for k, v in DEFAULTS.items():
        fm.setdefault(k, v)
    # ensure permalink
    if 'permalink' not in fm:
        slug = p.stem
        fm['permalink'] = f"/publication/{slug}"
    # ensure title
    if 'title' not in fm:
        fm['title'] = p.stem.replace('-', ' ').title()
    # ensure date
    if 'date' not in fm:
        fm['date'] = '1970-01-01'
    # write back
    new_fm = yaml.safe_dump(fm, sort_keys=False)
    new_text = '---\n' + new_fm + '---\n' + '\n'.join(body_lines).lstrip() + '\n'
    p.write_text(new_text, encoding='utf-8')
    print('Normalized', p)

print('Done')
