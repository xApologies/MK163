#!/usr/bin/env python3
"""Verify the complete payload manifest in an extracted atlas or its ZIP."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, zipfile

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
p.add_argument('--zip',type=Path,dest='zip_path')
a=p.parse_args();errors=[]
if a.zip_path:
    with zipfile.ZipFile(a.zip_path) as z:
        bad=z.testzip()
        if bad:errors.append('CRC failure: '+bad)
        names=[n for n in z.namelist() if not n.endswith('/')]
        roots={PurePosixPath(n).parts[0] for n in names}
        if len(roots)!=1:raise SystemExit('Expected one atlas root in ZIP.')
        prefix=next(iter(roots))+'/'
        manifest=json.loads(z.read(prefix+'MANIFEST.json'))
        actual={n[len(prefix):] for n in names if n!=prefix+'MANIFEST.json'}
        expected={f['path'] for f in manifest['files']}
        if actual!=expected:errors.append('ZIP manifest coverage mismatch.')
        for f in manifest['files']:
            q=PurePosixPath(f['path'])
            if q.is_absolute() or '..' in q.parts:errors.append('Unsafe path '+f['path']);continue
            try:payload=z.read(prefix+f['path'])
            except KeyError:errors.append('Missing '+f['path']);continue
            if len(payload)!=f['size_bytes']:errors.append('Size mismatch '+f['path'])
            if hashlib.sha256(payload).hexdigest()!=f['sha256']:errors.append('Hash mismatch '+f['path'])
else:
    base=a.atlas_dir.resolve();manifest=json.loads((base/'MANIFEST.json').read_text())
    actual={f.relative_to(base).as_posix() for f in base.rglob('*')
            if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'
            and f!=base/'MANIFEST.json'}
    expected={f['path'] for f in manifest['files']}
    if actual!=expected:errors.append('Directory manifest coverage mismatch.')
    for f in manifest['files']:
        q=PurePosixPath(f['path'])
        if q.is_absolute() or '..' in q.parts:errors.append('Unsafe path '+f['path']);continue
        path=base/f['path']
        if not path.is_file():errors.append('Missing '+f['path']);continue
        payload=path.read_bytes()
        if len(payload)!=f['size_bytes']:errors.append('Size mismatch '+f['path'])
        if hashlib.sha256(payload).hexdigest()!=f['sha256']:errors.append('Hash mismatch '+f['path'])
result={'status':'FAIL' if errors else 'PASS','payload_files':len(manifest['files']),
        'full_manifest_coverage':actual==expected,'errors':errors}
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
