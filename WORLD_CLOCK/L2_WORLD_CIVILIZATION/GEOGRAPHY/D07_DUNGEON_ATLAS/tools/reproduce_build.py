#!/usr/bin/env python3
"""Reproduce the frozen initial graph in a fresh directory and compare all exports.

Never use initial generation as an edit or redraw operation for a live atlas.
The existing data/dungeon_graph.json remains authoritative after handoff.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

FILES = ['dungeon_graph.json','nodes.csv','edges.csv','adjacency.csv',
         'view_index.csv','stratum_connections.csv','dungeon_graph.graphml','VALIDATION.json']
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas-dir',type=Path,default=Path(__file__).resolve().parents[1])
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(); base=a.atlas_dir.resolve(); dest=a.output.resolve()
if dest.exists():
    raise SystemExit('Refusing an existing reproduction directory; choose a fresh --output.')
command=[sys.executable,str(base/'tools/generate_dungeon.py'),'--spec',
         str(base/'config/dungeon_spec.json'),'--output',str(dest)]
run=subprocess.run(command,capture_output=True,text=True)
if run.returncode:
    sys.stderr.write(run.stdout+run.stderr)
    raise SystemExit(run.returncode)
comparisons=[]
for name in FILES:
    expected=(base/'data'/name).read_bytes(); actual=(dest/'data'/name).read_bytes()
    comparisons.append({'file':name,'byte_identical':expected==actual,
                        'expected_sha256':hashlib.sha256(expected).hexdigest(),
                        'actual_sha256':hashlib.sha256(actual).hexdigest()})
result={'status':'PASS' if all(x['byte_identical'] for x in comparisons) else 'FAIL',
        'scope':'Frozen initial build reproduction, not a live atlas update.',
        'graph_files_compared':len(comparisons),'comparisons':comparisons}
(dest/'REPRODUCTION_REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
