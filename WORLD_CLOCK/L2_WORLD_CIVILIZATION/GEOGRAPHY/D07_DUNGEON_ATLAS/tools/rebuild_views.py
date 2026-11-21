#!/usr/bin/env python3
"""Validate and redraw the saved atlas without generating or changing geography."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
a=p.parse_args(); base=a.atlas_dir.resolve()
before={f.name:hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted((base/'data').iterdir()) if f.is_file()}
for tool in ['validate_graph.py','render_atlas.py','build_viewer.py','build_atlas_pdf.py']:
    subprocess.run([sys.executable,str(base/'tools'/tool),'--atlas-dir',str(base)],check=True)
after={f.name:hashlib.sha256(f.read_bytes()).hexdigest()
       for f in sorted((base/'data').iterdir()) if f.is_file()}
result={'status':'PASS' if before==after else 'FAIL',
        'all_graph_exports_unchanged':before==after,
        'graph_sha256':after['dungeon_graph.json'],
        'operation':'Redrew views from existing graph; initial generator was not invoked.'}
(base/'validation').mkdir(exist_ok=True)
(base/'validation/VIEW_REBUILD.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if before==after else 1)
