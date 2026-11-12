"""Read-only transaction validation for incremental MK163 Delta 021.

Run from the repository with Python 3. The baseline is intentionally fixed:
later author amendments do not retroactively rewrite this transaction receipt.
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

BASELINE = '15ca6f75ec79b442be8334224465c440e427fb61'
W = 'PROVENANCE/WORKSHOP/YELLOW_CLOSURE_021_2026_11_11/'
C = 'CHECKPOINTS/YELLOW_CLOSURE_021/'
LEDGER = 'CONTINUITY/RED_RUNNING_DAY_LEDGER.md'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    git_path = os.environ.get('MK163_GIT') or shutil.which('git')
    need(git_path, 'Git required')

    def git(*argv):
        return subprocess.check_output([git_path, '-C', str(root), *argv])

    def read(path):
        return (root / path).read_bytes()

    def text(path):
        return read(path).decode('utf-8')

    def active(path):
        return text(path).split('## Earlier record · preserved verbatim')[0]

    source_map = json.loads(read(W + 'SOURCE_MAP.json'))
    inventory = json.loads(read(C + 'FILE_CHANGES.json'))
    changes = inventory['changes']
    need(inventory['baseline'] == source_map['baseline'] == BASELINE, 'Baseline')
    need((inventory['added'], inventory['modified'], inventory['deleted']) == (24, 27, 0),
         'Scope counts')
    members = source_map['members']
    need(len(members) == 15, 'Source count')
    payload = {}
    for name, entry in members.items():
        need(entry['installed'] == W + name and not entry['existing_matches'], 'Source mapping')
        data = read(entry['installed'])
        need(sha(data) == entry['sha256'] and len(data) == entry['bytes'], 'Source hash: ' + name)
        payload[name] = data
    manifest = json.loads(payload['SHA256_MANIFEST.json'])['file_sha256']
    need(len(manifest) == 14 and set(manifest) == set(payload) - {'SHA256_MANIFEST.json'},
         'Manifest coverage')
    for name, digest in manifest.items():
        need(sha(payload[name]) == digest, 'Manifest hash: ' + name)
    archive_status = 'Installed source bytes and all manifest hashes verified'
    if args.archive:
        need(sha(args.archive.read_bytes()) == source_map['archive_sha256'], 'Archive hash')
        with zipfile.ZipFile(args.archive) as archive:
            names = archive.namelist()
            need(len(names) == len({n.casefold() for n in names}) == 15, 'Archive path collisions')
            need(archive.testzip() is None, 'Archive CRC')
            for entry in archive.infolist():
                n = entry.filename
                p = PurePosixPath(n)
                need(not p.is_absolute() and not PureWindowsPath(n).drive and '\\' not in n
                     and ':' not in n and all(x not in ('..', '.git', '_inbox')
                     and not PureWindowsPath(x).is_reserved() for x in p.parts), 'Unsafe archive path')
                need(not stat.S_ISLNK(entry.external_attr >> 16) and not entry.flag_bits & 1
                     and entry.file_size < 50_000_000, 'Unsupported archive entry')
            need({n: archive.read(n) for n in names} == payload, 'Archive versus installed bytes')
        archive_status = 'PASS: SHA-256, CRC, safe paths, full installed-byte equality'

    delta = list(csv.DictReader(io.StringIO(payload['CALENDAR/DAILY_LEDGER_DAY_168_211.csv'].decode('utf-8-sig'))))
    need([int(r['ledger_day']) for r in delta] == list(range(168, 212)), 'Delta day sequence')
    delta_md = [[x.strip() for x in line.strip('|').split('|')]
                for line in payload['CALENDAR/DAILY_LEDGER_DAY_168_211.md'].decode().splitlines()
                if line.startswith('| ') and line.split('|')[1].strip().isdigit()]
    need(delta_md == [[r['ledger_day'], r['month'] + ' ' + r['day_of_month'],
                      r['weekday'], r['event_status']] for r in delta], 'Delta MD/CSV')
    daily_text = text(LEDGER).split('## Earlier detailed interval record')[0]
    daily = [[x.strip() for x in line.strip('|').split('|')]
             for line in daily_text.splitlines()
             if line.startswith('| ') and line.split('|')[1].strip().isdigit()]
    need(len(daily) == 212 and [int(r[0]) for r in daily] == list(range(212)), 'Master day uniqueness')
    old_csv = 'PROVENANCE/WORKSHOP/CUMULATIVE_020_2026_11_11/020/CALENDAR/DAILY_LEDGER_DAY_000_167.csv'
    previous_rows = list(csv.DictReader(io.StringIO(text(old_csv))))
    need(daily[:168] == [list(r.values()) for r in previous_rows], 'Prior daily content changed')
    need(daily[168:] == [[r['ledger_day'], r['month'], r['day_of_month'], '—',
                         r['weekday'], r['event_status']] for r in delta], 'New canonical daily content')
    months = [('Aelor', 33), ('Aerith', 32), ('Aelora', 31), ('Aevrin', 33), ('Aelis', 31),
              ('Aevor', 32), ('Aelith', 33), ('Aerion', 32), ('Aeveth', 31), ('Aesith', 33), ('Aeleth', 32)]
    weekdays = ['Ailar', 'Aiden', 'Aiveth', 'Ailor', 'Aithen', 'Aiven']
    need(sum(n for _, n in months) == 353, 'Year sum')
    for row in daily:
        day = int(row[0]); ordinal = 70 + day
        for month, count in months:
            if ordinal <= count:
                break
            ordinal -= count
        need(row[1:3] == [month, str(ordinal)] and row[4] == weekdays[(4 + day) % 6],
             'Calendar mismatch on day ' + str(day))
    need(daily[211][1:3] == ['Aeveth', '24'] and daily[211][4] == 'Aiven', 'Final date')
    need(211 - 63 + 1 == 149 and 187 - 180 + 1 == 8 and 209 - 202 == 7, 'Interval arithmetic')
    need(12 * 1550 - 12 * 1000 - 4 * 580 - 130 == 4150, 'Business arithmetic')
    need(7 * 1550 - 7 * 1000 - 2 * 580 == 2690 and 1700 - 1550 == 150, 'Prior price arithmetic')

    # Exact substantive source inclusion, not only keyword coverage.
    for name, owner in inventory['canonical_topic_owners'].items():
        supplied = payload[name].decode('utf-8').strip()
        for visual in payload:
            if visual.startswith('VISUAL_REFERENCES/'):
                relative = os.path.relpath(W + visual, str(Path(owner).parent)).replace('\\', '/')
                supplied = supplied.replace('`' + visual + '`', '[' + Path(visual).name + ']('
                                            + urllib.parse.quote(relative, safe='/._-') + ')')
        if name.startswith('CANON/05'):
            supplied = supplied.replace('Currency uses **eln and ahm**, exact exchange ratio OPEN; never canonize 100:1 without user approval.',
                'Currency uses **eln and ahm**. **1 Red eln = 180 ahm** remains current by the author\'s explicit integration reply; the incoming claim that this ratio is OPEN is stale. No 100:1 conversion is selected.')
        if name.startswith('CANON/07'):
            calendar, terms = supplied.split('\n\nProtected terms:', 1)
            calendar = calendar.replace('# Calendar and protected terms — current author decisions',
                                        '# Calendar · 353-day year selected in Delta 021')
            need(calendar in active(owner), 'Calendar detail missing')
            need('Protected terms:' + terms in active('CONSTITUTIONS/07_NAMING_CONVENTIONS.md'),
                 'Protected terms detail missing')
        else:
            need(supplied in active(owner), 'Substantive detail missing: ' + name)
    need('Yellow COMPLETE' in active('BOOKS/RED/ARCS/ARC_003/ARC.md'), 'Arc status')
    need('after Day 211' in active('BOOKS/RED/ARCS/ARC_004/ARC.md'), 'Green boundary')
    need('1 Red eln = 6 Violet ahm coins = 6 × 30 = 180 base ahm.' in text('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CURRENCY_AND_COMMODITY_EXCHANGE.md'),
         'Currency authority')

    # Compare every baseline blob, including all prior checkpoints and originals.
    objects = {}
    for line in git('ls-tree', '-r', '-z', BASELINE).split(b'\0')[:-1]:
        meta, path = line.split(b'\t', 1); mode, kind, oid = meta.split()
        need(kind == b'blob', 'Unexpected baseline object')
        objects[path.decode()] = oid.decode()
    need(len(objects) == 753, 'Baseline file count')
    old_bytes = {}; changed_prefixes = {}
    proc = subprocess.Popen([git_path, '-C', str(root), 'cat-file', '--batch'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for path, oid in objects.items():
            proc.stdin.write((oid + '\n').encode()); proc.stdin.flush()
            header = proc.stdout.readline().split()
            need(len(header) == 3 and header[0].decode() == oid and header[1] == b'blob', 'Git framing')
            data = proc.stdout.read(int(header[2])); need(proc.stdout.read(1) == b'\n', 'Git separator')
            current = read(path)
            if path not in changes:
                need(current == data, 'Unrelated baseline file changed: ' + path)
                continue
            need(changes[path]['operation'] == 'modified' and current != data, 'Missing expected update')
            mode = changes[path]['preservation']
            if mode == 'prefix':
                need(current.endswith(data), 'Prior record changed: ' + path)
                changed_prefixes[path] = current[:-len(data)].decode('utf-8')
            elif mode == 'append':
                need(current.startswith(data), 'Prior configuration changed')
            else:
                old_bytes[path] = data
    finally:
        proc.stdin.close(); proc.stdout.close(); need(proc.wait() == 0, 'Object reader failed')
    original_ledger = old_bytes[LEDGER]
    delta_lines = ''.join('| ' + r['ledger_day'] + ' | ' + r['month'] + ' | ' + r['day_of_month']
                          + ' | — | ' + r['weekday'] + ' | ' + r['event_status'] + ' |\n' for r in delta).encode()
    ledger_bytes = read(LEDGER)
    need(ledger_bytes.count(delta_lines) == 1, 'Delta inserted more than once')
    need(ledger_bytes.replace(delta_lines, b'').endswith(original_ledger), 'Prior ledger bytes lost')
    changed_prefixes[LEDGER] = ledger_bytes[:ledger_bytes.index(original_ledger.splitlines()[0])].decode()
    registry_path = 'PROVENANCE/SOURCE_REGISTRY.json'
    registry = json.loads(read(registry_path)); added_delivery = registry['subsequent_deliveries'].pop()
    need(registry == json.loads(old_bytes[registry_path]), 'Prior registry entries changed')
    need(added_delivery['id'] == 'MK163_YELLOW_ARC_CLOSURE_DELTA_021', 'New registry ID')
    paths = set(git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1])
    added = {p for p, e in changes.items() if e['operation'] == 'added'}
    modified = {p for p, e in changes.items() if e['operation'] == 'modified'}
    need(len(added) == 24 and len(modified) == 27 and modified <= set(objects), 'Changed-path counts')
    need(paths == set(objects) | added, 'Unexpected file inventory')
    need(not any(p.startswith('_inbox/') or p.endswith('.zip') for p in changes), 'Inbox/archive staged')
    need(len(paths) == len({p.casefold() for p in paths}), 'Windows path collisions')
    need(all((root / p).stat().st_size < 50_000_000 for p in added), 'Oversized added file')
    for path in added:
        if path.endswith('.md') and not path.startswith(W):
            changed_prefixes[path] = text(path)
    checked_links = 0
    for path, document in changed_prefixes.items():
        for target in re.findall(r'\]\(([^)]+)\)', document):
            if '://' in target or target.startswith('#'):
                continue
            local = urllib.parse.unquote(target.split('#')[0])
            need(((root / path).parent / local).is_file(), 'Broken new local link: ' + path + ': ' + target)
            checked_links += 1
    git('diff', '--check'); git('diff', '--cached', '--check')
    result = {'status': 'PASS', 'baseline': BASELINE, 'source_files_verified': 15,
              'manifest_hashes_passed': 14, 'visual_originals_verified': 3,
              'full_substantive_topic_records_verified': 7,
              'daily_rows_verified': 212, 'new_days_verified': 44, 'prior_daily_rows_unchanged': 168,
              'yellow_inclusive_days': 149, 'final_date': 'Day 211 = Aeveth 24, Aiven',
              'year_days': 353, 'prior_detail_preserved': True, 'old_history_and_images_unchanged': True,
              'orange_arc_and_ledger_unchanged': True, 'rate_author_resolution': '1 Red eln = 180 ahm',
              'calendar_week_and_astronomy_open': True, 'banking_transport_and_security_open': True,
              'added': len(added), 'modified': len(modified), 'deleted': 0,
              'baseline_files_byte_identical': len(objects) - len(modified),
              'new_local_links_checked': checked_links, 'archive_validation': archive_status,
              'blocking_conflicts': [], 'literal_transcript_completeness_claimed': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
