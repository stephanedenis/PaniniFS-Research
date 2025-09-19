#!/usr/bin/env python3
"""Generate SHA256 hashes for cached reference files and produce a JSON manifest.

Usage:
    python3 scripts/generate_cache_hashes.py --input cache_sources.txt --out cache_manifest.json \
        [--root path/to/downloads] [--update-section]

The input file lists entries: ID <whitespace> URL <whitespace> TYPE(optional)
Downloaded resources should exist locally under --root using filename derived from ID or URL.
The script:
 1. Parses the list
 2. Computes SHA256 for each existing local file
 3. Emits manifest JSON: {
       "version": "0.1",
       "generated": ISO8601,
       "items": [ {"id":..., "url":..., "type":..., "filename":..., "sha256":..., "size":... } ]
     }
Exit code non-zero if any listed file missing.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, datetime, pathlib, re

def derive_filename(entry_id: str, url: str) -> str:
    # Prefer ID with extension inferred from URL
    suffix = ''.join(pathlib.Path(url).suffixes) or ''
    # basic sanitization
    safe_id = re.sub(r'[^A-Za-z0-9_.-]', '_', entry_id)
    return f"{safe_id}{suffix}" if suffix else safe_id

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_input(lines):
    for ln in lines:
        ln = ln.strip()
        if not ln or ln.startswith('#'):
            continue
        parts = ln.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid line (need at least ID URL): {ln}")
        entry_id, url = parts[0], parts[1]
        ftype = parts[2] if len(parts) > 2 else None
        yield {"id": entry_id, "url": url, "type": ftype}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--root', default='cache_downloads')
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"Root directory {root} does not exist", file=sys.stderr)
        sys.exit(2)

    with open(args.input, 'r', encoding='utf-8') as f:
        entries = list(parse_input(f.readlines()))

    manifest_items = []
    missing = False
    for e in entries:
        filename = derive_filename(e['id'], e['url'])
        fpath = root / filename
        if not fpath.exists():
            print(f"MISSING: {fpath}", file=sys.stderr)
            missing = True
            continue
        digest = sha256_file(fpath)
        manifest_items.append({
            'id': e['id'],
            'url': e['url'],
            'type': e['type'],
            'filename': filename,
            'sha256': digest,
            'size': fpath.stat().st_size
        })

    manifest = {
        'version': '0.1',
        'generated': datetime.datetime.utcnow().isoformat() + 'Z',
        'items': manifest_items
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    if missing:
        print("One or more files missing", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
