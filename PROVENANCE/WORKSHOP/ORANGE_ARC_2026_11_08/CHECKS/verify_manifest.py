#!/usr/bin/env python3
"""Verify the extracted MK163_ORANGE_2026_11_08 payload against its exact manifest.

Usage: python CHECKS/verify_manifest.py /path/to/MK163_ORANGE_2026_11_08
This does not modify files or access GitHub.
"""
import hashlib, json, sys, zipfile
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]).resolve()
    manifest=json.loads((root/'MANIFEST.json').read_text('utf8'))
    failures=[]
    declared=set()
    for item in manifest['files']:
        path=item['path']
        folded=path.lower()
        if folded in declared: failures.append('duplicate case-fold path: '+path)
        declared.add(folded)
        p=(root/path).resolve()
        if not p.is_relative_to(root):failures.append('outside root: '+path);continue
        if not p.is_file():failures.append('missing: '+path);continue
        if p.stat().st_size!=item['bytes']:failures.append('size mismatch '+path)
        if sha(p)!=item['sha256']:failures.append('sha mismatch '+path)
        if p.suffix.lower()=='.zip':
            try:
                with zipfile.ZipFile(p) as z:
                    bad=z.testzip()
                    if bad:failures.append('ZIP bad member '+path+'::'+bad)
            except Exception as e: failures.append(f'ZIP invalid {path}: {e}')
    actual={str(p.relative_to(root)).lower() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    missing_from_manifest=actual-declared
    for p in sorted(missing_from_manifest):failures.append('undeclared file: '+p)
    checks=[
        ('DECISIONS/09_SIGIL_CHAINMAIL_INGOT_SPOOL_RING_PARALLEL_TRANSDUCTION.md','300,000'),
        ('DECISIONS/05_SMITHY_MODULES_SOUTHWEST_CRAFTSMEN_PLAZA.md','NO OVERHANG'),
        ('DECISIONS/08_FIRST_NATURE_DETOUR_GENESIS_FROG_MOSS_MINERAL_VAEN.md','NOT vaen'),
        ('DECISIONS/07_VAEL_RAEON_CARD_SHOP_CHARACTER_ARC.md','**both Cards'),
        ('DECISIONS/02_ECONOMIC_PREMIUM_RESOURCES_PRICES_AND_HOUSING.md','1.3–1.7'),
    ]
    for path,needle in checks:
        if needle.lower() not in (root/path).read_text('utf8').lower():failures.append('semantic missing: '+path+'::'+needle)
    print(f'MK163 Orange package: {len(manifest["files"])} declared files; {len(failures)} failures')
    if failures:
        print('\n'.join('FAIL '+f for f in failures))
        return 1
    print('PASS: sizes, SHA256, nested ZIP CRC, member paths, semantic spot checks')
    return 0

if __name__=='__main__':sys.exit(main())
