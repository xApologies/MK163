#!/usr/bin/env python3
"""Verify every methodology payload file against MANIFEST.json, including path safety and extra-file checks."""
from pathlib import Path
import argparse,hashlib,json,sys

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=p.parse_args();root=args.root.resolve();errors=[]
    try:
        manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
        expected=set()
        for row in manifest['files']:
            relative=row['path'];path=(root/relative).resolve()
            if not path.is_relative_to(root) or relative in expected:
                errors.append('Unsafe or duplicate path: '+relative);continue
            expected.add(relative)
            if not path.is_file():errors.append('Missing: '+relative);continue
            raw=path.read_bytes()
            if len(raw)!=row['bytes']:errors.append('Size mismatch: '+relative)
            if hashlib.sha256(raw).hexdigest()!=row['sha256']:errors.append('Hash mismatch: '+relative)
        actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        for relative in sorted(actual-expected-{'MANIFEST.json'}):errors.append('Unlisted: '+relative)
        print(json.dumps({'status':'FAIL' if errors else 'PASS','payload_files':len(expected),'errors':errors},indent=2))
        return bool(errors)
    except (OSError,KeyError,ValueError) as e:
        print(str(e),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
