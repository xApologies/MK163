"""Validate the additive 020 historical-ledger repair against its Git baseline.

Read-only. Run with --archive-dir _inbox to also verify the two local ZIPs.
Earlier transaction receipts remain historical and are not rewritten.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shutil
import stat
import subprocess
import urllib.parse
import zipfile

BASELINE = '9062336207f55413f1c753f1214653b4fac8ac2b'
W = 'PROVENANCE/WORKSHOP/CUMULATIVE_020_2026_11_11/'
C = 'CHECKPOINTS/CUMULATIVE_020_HISTORICAL_REPAIR/'
MODIFIED = {'AGENTS.md', 'PROVENANCE/OPEN_QUESTIONS_CURRENT.md',
            'PROVENANCE/SOURCES.md', 'PROVENANCE/SOURCE_REGISTRY.json'}
ORIGINALS = {
    W + '018/CALENDAR/DAILY_LEDGER_DAY_000_116.md':
        '85b169f49a2fc5149f09786656ef0d74a69b1f4e36e4fd903f77cb0645dc9cc4',
    W + '018/CALENDAR/DAILY_LEDGER_DAY_000_116.csv':
        '687fcf95130f63d5718ec433789edc64f2ca957a1dcd7db2e31154ba5c6e5d94',
}
ADDED = set(ORIGINALS) | {
    W + '020/HISTORICAL_LEDGER_REPAIR_NOTE.md',
    W + 'HISTORICAL_LEDGER_REPAIR_MAP.json',
    C + 'INTEGRATION_REPORT.md', C + 'VALIDATION.json',
    'CHECKPOINTS/TOOLS/validate_checkpoint_020_repair.py',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_zip(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        need(len(names) == len({n.casefold() for n in names}), 'Duplicate ZIP paths')
        need(archive.testzip() is None, 'ZIP CRC failure')
        for entry in archive.infolist():
            p = PurePosixPath(entry.filename)
            need(not p.is_absolute() and not PureWindowsPath(str(p)).drive
                 and '\\' not in str(p) and ':' not in str(p), 'Unsafe archive path')
            need(all(part not in ('..', '.git', '_inbox')
                     and not PureWindowsPath(part).is_reserved() for part in p.parts),
                 'Unsafe archive component')
            need(not stat.S_ISLNK(entry.external_attr >> 16)
                 and not entry.flag_bits & 1 and entry.file_size < 50_000_000,
                 'Unsupported archive entry')
        return {name: archive.read(name) for name in names}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--archive-dir', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    git_path = os.environ.get('MK163_GIT') or shutil.which('git')
    need(git_path, 'Git is required')

    def git(*argv):
        return subprocess.check_output([git_path, '-C', str(root), *argv])

    repair = json.loads((root / W / 'HISTORICAL_LEDGER_REPAIR_MAP.json').read_bytes())
    old_map = json.loads((root / W / 'SOURCE_MAP.json').read_bytes())
    members = repair['members']
    need(len(members) == 44 and len(old_map['members']) == 41, 'Source counts')
    need(repair['baseline'] == BASELINE, 'Repair baseline mismatch')
    need(set(old_map['members']) <= set(members), 'Prior source lost')
    payload = {}
    for name, entry in members.items():
        target = (root / entry['installed']).resolve()
        need(target.is_relative_to(root), 'Source target escapes repository')
        data = target.read_bytes()
        need(sha(data) == entry['sha256'] and len(data) == entry['bytes'], name)
        if name in old_map['members']:
            need(entry['installed'] == old_map['members'][name]['installed'],
                 'Duplicated prior source: ' + name)
            need(entry['disposition'] == 'unchanged prior entry', 'Prior source state')
        else:
            need(entry['disposition'] == 'new repair entry', 'New source state')
        payload[name] = data
    need(len({e['installed'] for e in members.values()}) == 44, 'Duplicate source targets')
    for path, digest in ORIGINALS.items():
        need(sha((root / path).read_bytes()) == digest, 'Restored original hash: ' + path)

    manifests = {}
    for name, data in payload.items():
        if 'MANIFEST' not in name or not name.endswith('.json'):
            continue
        document = json.loads(data)
        entries = document.get('files', document)
        parent = str(PurePosixPath(name).parent)
        for path, digest in entries.items():
            candidates = [path, parent + '/' + path]
            if path.startswith('MK163_') and '/' in path:
                candidates.append(parent + '/' + path.split('/', 1)[1])
            found = [p for p in dict.fromkeys(candidates) if p in payload]
            need(len(found) == 1 and sha(payload[found[0]]) == digest,
                 'Manifest mismatch: ' + name + ': ' + path)
        manifests[name] = len(entries)
    need(sorted(manifests.values()) == [19, 26, 30, 40], 'Manifest coverage')

    csv_path = next(p for p in ORIGINALS if p.endswith('.csv'))
    md_path = next(p for p in ORIGINALS if p.endswith('.md'))
    rows = list(csv.DictReader(io.StringIO((root / csv_path).read_text(encoding='utf-8-sig'))))
    need(len(rows) == 117 and [int(next(iter(r.values()))) for r in rows] == list(range(117)),
         'Historical day sequence')
    md_rows = [[x.strip() for x in line.strip('|').split('|')]
               for line in (root / md_path).read_text(encoding='utf-8').splitlines()
               if line.startswith('| ') and line.split('|')[1].strip().isdigit()]
    need(md_rows == [list(row.values()) for row in rows], 'Historical MD/CSV mismatch')

    baseline = {}
    for row in git('ls-tree', '-r', '-z', BASELINE).split(b'\0')[:-1]:
        metadata, name = row.split(b'\t', 1)
        mode, kind, oid = metadata.split()
        need(kind == b'blob', 'Unexpected baseline object')
        baseline[name.decode()] = oid.decode()
    need(len(baseline) == 746, 'Unexpected baseline inventory')
    old_metadata = {}
    proc = subprocess.Popen([git_path, '-C', str(root), 'cat-file', '--batch'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for path, oid in baseline.items():
            proc.stdin.write((oid + '\n').encode())
            proc.stdin.flush()
            header = proc.stdout.readline().split()
            need(len(header) == 3 and header[0].decode() == oid and header[1] == b'blob',
                 'Git object header')
            data = proc.stdout.read(int(header[2]))
            need(proc.stdout.read(1) == b'\n', 'Git object framing')
            current = (root / path).read_bytes()
            if path in MODIFIED:
                need(current != data, 'Missing metadata update: ' + path)
                old_metadata[path] = data
                if path.endswith('.md'):
                    need(current.endswith(data), 'Prior text changed: ' + path)
                    prefix = current[:-len(data)].decode('utf-8')
                    for link in re.findall(r'\]\(([^)]+)\)', prefix):
                        need(((root / path).parent / urllib.parse.unquote(link)).is_file(),
                             'Broken repair link: ' + link)
            else:
                need(current == data, 'Unrelated baseline file changed: ' + path)
    finally:
        proc.stdin.close()
        proc.stdout.close()
        need(proc.wait() == 0, 'Git object reader failed')
    previous_registry = json.loads(old_metadata['PROVENANCE/SOURCE_REGISTRY.json'])
    current_registry = json.loads((root / 'PROVENANCE/SOURCE_REGISTRY.json').read_bytes())
    delivery = current_registry['subsequent_deliveries'].pop()
    need(current_registry == previous_registry, 'Prior registry content changed')
    need(delivery['id'] == 'MK163_CUMULATIVE_CHECKPOINT_020_HISTORICAL_LEDGER_REPAIR'
         and delivery['historical_gap'] == 'resolved', 'Repair registry entry')
    paths = set(git('ls-files', '--cached', '--others', '--exclude-standard', '-z')
                .decode().split('\0')[:-1])
    need(paths == set(baseline) | ADDED, 'Unexpected repository file inventory')
    need(not any(p.startswith('_inbox/') for p in paths), 'Inbox tracked')
    git('diff', '--check')
    git('diff', '--cached', '--check')

    archive_status = 'not requested; installed source bytes verified'
    if args.archive_dir:
        folder = args.archive_dir.resolve()
        old_path = folder / 'MK163_CUMULATIVE_CHECKPOINT_020_ACCUMULATED_2026-11-11.zip'
        new_path = folder / repair['archive']
        need(sha(old_path.read_bytes()) == repair['prior_archive_sha256'], 'Prior ZIP hash')
        need(sha(new_path.read_bytes()) == repair['archive_sha256'], 'Repaired ZIP hash')
        old_zip, new_zip = safe_zip(old_path), safe_zip(new_path)
        need(len(old_zip) == 41 and new_zip == payload, 'ZIP versus installed sources')
        need(set(old_zip) <= set(new_zip)
             and all(new_zip[k] == v for k, v in old_zip.items()), 'Prior ZIP entry changed')
        archive_status = 'PASS: CRC, paths, SHA-256, 41 unchanged members, 3 additions'
    print(json.dumps({
        'status': 'PASS', 'scope': 'accumulated historical provenance repair only',
        'baseline': BASELINE, 'source_members_verified': len(payload),
        'prior_source_members_reused': 41, 'new_source_members': 3,
        'manifest_hashes_passed': sum(manifests.values()), 'manifest_counts': manifests,
        'historical_rows_md_csv_agree': len(rows), 'historical_018_ledger_gap': 'RESOLVED',
        'added': len(ADDED), 'modified': len(MODIFIED), 'deleted': 0,
        'prior_files_byte_identical': len(baseline) - len(MODIFIED),
        'canonical_owners_and_current_ledger_unchanged': True,
        'prior_text_preserved': True, 'prior_registry_entries_preserved': True,
        'archive_validation': archive_status, 'unrelated_paths': [],
        'calendar_and_other_open_items_unchanged': True,
        'literal_transcript_completeness_claimed': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
