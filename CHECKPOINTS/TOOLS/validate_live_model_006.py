#!/usr/bin/env python3
"""Read-only validation of the complete 006 checkpoint and installed receipt."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile

STALE_INNER = {
    'ECONOMIC_FOUNDATION_INDEX.md': (
        'a5008f4a9fba283989b7509d9c0cb0e282efd34c8d2f580a6edc73d2d1ae8d38',
        '6cc0052254cb12bdb80bb4ee0b283142eebcf1e4b395da3cdd22d3f637225df3'),
    'VISUALS/ATLAS_INDEX.md': (
        '2b64e0b19390a0808249d7f6d6ded16821b7799c6fb79acc47d4530f058522c4',
        '6b2ef97775df2d1ae5d1f17b3d3669ad9d034dccd5e4a8ffbc02461b3335911d'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{v}{n}' for v in ('COM', 'LPT') for n in range(1, 10)}
    return (bool(name) and not p.is_absolute() and not PureWindowsPath(name).drive
            and '\\' not in name and ':' not in name and str(p) == name
            and all(c not in ('.', '..') and c.casefold() not in ('.git', '_inbox')
                    and c.rstrip(' .') == c and c.split('.')[0].upper() not in reserved
                    for c in p.parts))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate_archive(path):
    result = {'archive_sha256': sha(path.read_bytes()), 'documented_corrections': []}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(z.testzip() is None, 'Archive CRC failure')
        require(len(names) == len({n.casefold() for n in names}), 'Archive path collision')
        for i in z.infolist():
            require(safe(i.filename) and not i.is_dir(), 'Unsafe archive path: ' + i.filename)
            require(not stat.S_ISLNK(i.external_attr >> 16), 'Archive symlink: ' + i.filename)
        m = json.loads(z.read('CHECKPOINT_MANIFEST.json'))
        require(len(m['files']) == len({e['path'] for e in m['files']}), 'Duplicate manifest record')
        require(set(names) == {'CHECKPOINT_MANIFEST.json'} | {e['path'] for e in m['files']}, 'Incomplete outer manifest')
        for e in m['files']:
            data = z.read(e['path'])
            require(len(data) == e['size'] and sha(data) == e['sha256'], 'Outer hash/size: ' + e['path'])
        legacy = json.loads(z.read('LIVE_MODEL_006/MANIFEST.json'))
        for e in legacy['records']:
            data = z.read('LIVE_MODEL_006/' + e['path'])
            require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'Legacy hash/size: ' + e['path'])
        sm = json.loads(z.read('LIVE_MODEL_006/SESSION_006/SESSION_006_HASHES.json'))
        found = {}
        for name, expected in sm['files'].items():
            actual = sha(z.read('LIVE_MODEL_006/SESSION_006/' + name))
            if actual != expected:
                found[name] = (expected, actual)
        require(found == STALE_INNER, 'Unexpected inner-hash discrepancy: ' + repr(found))
        result['documented_corrections'] = [{'path': n, 'stale_inner_sha256': v[0], 'outer_verified_sha256': v[1]} for n, v in found.items()]
        side = z.read('LIVE_MODEL_006/SESSION_006/MELEE_WEAPON_BASE_PRICES.sha256').decode().split()
        require(side == [sha(z.read('LIVE_MODEL_006/SESSION_006/MELEE_WEAPON_BASE_PRICES.md')), 'MELEE_WEAPON_BASE_PRICES.md'], 'Weapon sidecar mismatch')
        nested = z.read('DELTA_005_ORIGINAL/MK163_LIVE_MODEL_EXPORT_005_CODEX.zip')
        require(sha(nested) == '6402e6077db9a5fc413b1d7463d332268560d140eea29cc4408a7f0c5e729b53', 'Prior recovery archive changed')
        with zipfile.ZipFile(io.BytesIO(nested)) as old:
            require(old.testzip() is None, 'Recovery archive CRC failure')
            for n in names:
                if n.startswith('LIVE_MODEL_006/') and '/SESSION_006/' not in n:
                    require(z.read(n) == old.read(n.removeprefix('LIVE_MODEL_006/')), 'Legacy recovery mismatch: ' + n)
        for n in names:
            if n.endswith('.svg'):
                root = ET.fromstring(z.read(n))
                require(root.tag == '{http://www.w3.org/2000/svg}svg', 'Invalid SVG: ' + n)
                require(not any(x.tag.split('}')[-1] in ('script', 'foreignObject') or any(k.lower().startswith('on') or k.split('}')[-1] == 'href' for k in x.attrib) for x in root.iter()), 'Unexpected active SVG content')
        result.update(archive_entries=len(names), outer_manifest_records=len(m['files']), legacy_manifest_records=len(legacy['records']), session_files=sum('/SESSION_006/' in n for n in names), session_hash_records=len(sm['files']), crc='PASS', paths='PASS', outer_hashes='PASS', legacy_hashes='PASS', inner_hashes='PASS after the two documented outer-verified corrections; original retained')
    return result


def validate_model(root, archive):
    root = root.resolve()
    receipt = root / 'CHECKPOINTS/LIVE_MODEL_006_MANIFEST.json'
    manifest = json.loads(receipt.read_text(encoding='utf-8'))
    records = manifest['files']
    require(manifest['archive_sha256'] == sha(archive.read_bytes()), 'Archive differs from integration receipt')
    require(len(records) == len({e['path'].casefold() for e in records}), 'Installed case collision')
    original_count = 0
    history_count = 0
    for e in records:
        p = root / e['path']
        require(safe(e['path']) and p.is_file() and p.resolve().is_relative_to(root), 'Unsafe/absent installed file: ' + e['path'])
        require(not any(q.is_symlink() or getattr(q, 'is_junction', lambda: False)() for q in [p, *p.parents] if q.is_relative_to(root)), 'Installed reparse path: ' + e['path'])
        data = p.read_bytes()
        require(len(data) < 100 * 1024 * 1024, 'Oversize file: ' + e['path'])
        if e['after_sha256'] is None:
            require(e['path'] == 'CHECKPOINTS/LIVE_MODEL_006_MANIFEST.json', 'Unexpected unhashed record')
        else:
            require(len(data) == e['after_bytes'] and sha(data) == e['after_sha256'], 'Installed hash/size: ' + e['path'])
        if e['before_sha256']:
            original_count += 1
            before = subprocess.check_output(['git', '-C', str(root), 'show', manifest['baseline_commit'] + ':' + e['path']])
            require(sha(before) == e['before_sha256'], 'Baseline mismatch: ' + e['path'])
            if e['path'] == 'PROVENANCE/SOURCE_REGISTRY.json':
                a, b = json.loads(before), json.loads(data)
                for k, v in a.items():
                    require(b[k][:len(v)] == v if isinstance(v, list) else b[k] == v, 'Prior registry value lost: ' + k)
            else:
                require(before in data, 'Prior content shortened/removed: ' + e['path'])
            if e['path'].startswith(('PROVENANCE/WORKSHOP/', 'CHECKPOINTS/')):
                require(before == data, 'History changed: ' + e['path'])
                history_count += 1
    with zipfile.ZipFile(archive) as z:
        require({e['archive_path'] for e in manifest['source_mapping']} == set(z.namelist()), 'Unaccounted archive entry')
        for e in manifest['source_mapping']:
            data = z.read(e['archive_path'])
            require(sha(data) == e['sha256'], 'Source-map hash: ' + e['archive_path'])
            if e['repository_path']:
                stored = (root / e['repository_path']).read_bytes()
                off = e['source_offset']
                require(stored[off:off + len(data)] == data, 'Source lost: ' + e['archive_path'])
    broken = []
    for e in records:
        if e['operation'] == 'unchanged' or not e['path'].endswith('.md'):
            continue
        p = root / e['path']
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            target = urllib.parse.unquote(target.split('#')[0].strip('<>'))
            if not (p.parent / target).exists():
                broken.append([e['path'], target])
    require(not broken, 'Broken links: ' + repr(broken))
    return {'installed_files': len(records), 'prior_files_preserved': original_count, 'prior_workshop_and_checkpoint_history_byte_identical': history_count, 'source_entries_accounted_for': len(manifest['source_mapping']), 'local_links': 'PASS', 'file_size_and_case': 'PASS'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', type=Path)
    ap.add_argument('--root', type=Path, help='Validate installed files against the new integration manifest')
    ap.add_argument('--report', type=Path, help='Optional new external JSON result; existing files are never overwritten')
    a = ap.parse_args()
    result = {'delivery': 'MK163_LIVE_MODEL_006_CODEX_CHECKPOINT'}
    try:
        result['package'] = validate_archive(a.archive)
        if a.root:
            result['installed'] = validate_model(a.root, a.archive)
        result['status'] = 'PASS'
        result['scope'] = 'Integrity and preservation of the supplied checkpoint; not proof of full raw-workshop completeness or field physics.'
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, ET.ParseError, subprocess.CalledProcessError) as exc:
        result.update(status='FAIL', error=str(exc))
    if a.report:
        with a.report.open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write('\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
