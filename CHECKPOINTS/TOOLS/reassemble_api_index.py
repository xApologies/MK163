#!/usr/bin/env python3
"""Recombine an exact split API member outside the repository; never stage the result."""
import argparse, hashlib, json
from pathlib import Path

def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',required=True,type=Path);a.add_argument('--output',required=True,type=Path);v=a.parse_args()
    root=v.repo.resolve();out=v.output.resolve()
    if out==root or root in out.parents: raise SystemExit('Output must be outside the tracked repository.')
    if out.exists(): raise SystemExit('Output exists; refusing overwrite.')
    manifest=json.loads((root/'WORLD_CLOCK/L0_MATHEMATICS/SOURCE_API_4_3/EXTRACTION_MANIFEST.json').read_text(encoding='utf-8'))
    entries=[x for x in manifest if 'exact_byte_parts' in x]
    if len(entries)!=1: raise SystemExit('Expected exactly one split member.')
    entry=entries[0];out.parent.mkdir(parents=True,exist_ok=True);total=hashlib.sha256()
    with out.open('xb') as target:
        for part in entry['exact_byte_parts']:
            src=root/part['path'];b=src.read_bytes()
            if len(b)!=part['bytes'] or hashlib.sha256(b).hexdigest()!=part['sha256']: raise SystemExit('Part failed hash check: '+part['path'])
            target.write(b);total.update(b)
    if total.hexdigest()!=entry['sha256'] or out.stat().st_size!=entry['original_bytes']: raise SystemExit('Combined hash failed.')
    print(str(out),total.hexdigest())
if __name__=='__main__':main()
