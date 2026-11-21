#!/usr/bin/env python3
"""Reproduce the preserved Blue Capital graph in a new directory; never edit a live atlas."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path, help='A directory that does not yet exist')
    p.add_argument('--render', action='store_true', help='Also regenerate eight PDF/PNG/SVG map views')
    p.add_argument('--viewer', action='store_true', help='Also regenerate the offline HTML viewer')
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    reference = root / 'reference/blue_capital'
    output = a.output.resolve()
    if output.exists():
        p.error('Output already exists. Select a new directory; no overwrite is permitted.')
    output.parent.mkdir(parents=True, exist_ok=True)
    logs: dict[str, str] = {}
    def run(name: str, script: str, *args: str) -> None:
        result = subprocess.run([sys.executable, str(reference / 'tools' / script), *args], text=True, capture_output=True)
        logs[name] = result.stdout + result.stderr
        if result.returncode:
            raise RuntimeError(f'{name} failed ({result.returncode}):\n{logs[name]}')
    try:
        run('generate', 'generate_proposal_002.py', '--output', str(output))
        run('validate', 'validate_graph.py', '--atlas-dir', str(output))
        checks = []
        for source in sorted((reference / 'data').iterdir()):
            # Environment 003 is a saved overlay, not output of the 002 generator.
            if source.name.startswith('environment_') or not source.is_file():
                continue
            actual = output / 'data' / source.name
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            actual_hash = hashlib.sha256(actual.read_bytes()).hexdigest() if actual.exists() else None
            checks.append({'file': source.name, 'matches': source_hash == actual_hash,
                           'reference_sha256': source_hash, 'regenerated_sha256': actual_hash})
        if a.render:
            run('render', 'render_atlas.py', '--atlas-dir', str(output))
        if a.viewer:
            run('viewer', 'build_viewer.py', '--atlas-dir', str(output))
        report = {'status': 'PASS' if all(c['matches'] for c in checks) else 'FAIL',
                  'scope': 'Byte equality of the eight graph-generation outputs; map PDF byte equality is not asserted.',
                  'environment_overlay_regenerated': False, 'checks': checks, 'logs': logs}
        (output / 'REPRODUCTION_REPORT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'status': report['status'], 'graph_files_compared': len(checks),
                          'rendered': a.render, 'viewer_built': a.viewer,
                          'report': str(output / 'REPRODUCTION_REPORT.json')}, indent=2))
        return 0 if report['status'] == 'PASS' else 1
    except (OSError, RuntimeError, ValueError) as exc:
        print(f'Reproduction failed: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
