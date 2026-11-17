"""Validate the scoped Violet 008 correction against its published baseline."""
from pathlib import Path
from urllib.parse import unquote
from zipfile import ZipFile
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--git', default=shutil.which('git'))
parser.add_argument('--structural-report', required=True)
args = parser.parse_args()
assert args.git, 'Provide the Git executable using --git'
ROOT = Path(__file__).resolve().parents[2]
BASE = '5260cefdf22f59c297f4ab66ade132f6ec8584a6'
SOURCE = 'PROVENANCE/WORKSHOP/VIOLET_CALENDAR_RESTORATION_008'
CHECKPOINT = 'CHECKPOINTS/VIOLET_CALENDAR_RESTORATION_008'
ARC = 'BOOKS/RED/ARCS/ARC_006'
CALENDAR = 'WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md'
GAMES = 'WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md'
LEDGER = 'CONTINUITY/RED_RUNNING_DAY_LEDGER.md'

def git(*cmd):
    return subprocess.check_output([args.git, *cmd], cwd=ROOT)

def read(path):
    return (ROOT/path).read_text(encoding='utf-8-sig')

def previous(path):
    return git('show', BASE+':'+path).decode('utf-8-sig')

def md_rows(text):
    return [[v.strip() for v in line.split('|')[1:-1]]
            for line in text.splitlines() if re.match(r'^\| \d+ \|', line)]

week = ['Ailar', 'Aiden', 'Aiveth', 'Ailor', 'Aithen', 'Aiven']
months = list(zip(['Aelor','Aerith','Aelora','Aevrin','Aelis','Aevor',
                   'Aelith','Aerion','Aeveth','Aesith','Aeleth'],
                  [33,32,31,33,31,32,33,32,31,33,32]))

def coordinates(day):
    remaining = (33+32+4+day) % 353
    for month, count in months:
        if remaining < count:
            return month, remaining+1, week[(day+4)%6], (day+4)%6+1
        remaining -= count

mapping = json.loads(read(SOURCE+'/SOURCE_MAP.json'))
assert mapping['baseline'] == BASE and len(mapping['files']) == 5
for entry in mapping['files']:
    content = (ROOT/entry['original_destination']).read_bytes()
    assert len(content) == entry['bytes']
    assert hashlib.sha256(content).hexdigest() == entry['sha256'], entry['path']
archive = ROOT/'_inbox'/mapping['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest() == mapping['archive_sha256']
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == {e['path'] for e in mapping['files']}
    for entry in mapping['files']:
        assert z.read(entry['path']) == (ROOT/entry['original_destination']).read_bytes()

source_rows = list(csv.DictReader(io.StringIO(read(SOURCE+'/VIOLET_CORRECTED_DAILY_LEDGER.csv'), newline='')))
active_rows = list(csv.DictReader(io.StringIO(read(ARC+'/VIOLET_DAILY_LEDGER_008.csv'), newline='')))
assert len(source_rows) == len(active_rows) == 80
assert [int(r['story_day']) for r in active_rows] == list(range(1080,1160))
active_md = md_rows(read(ARC+'/VIOLET_DAILY_LEDGER_008.md'))
source_md = md_rows(read(SOURCE+'/VIOLET_CORRECTED_DAILY_LEDGER.md'))
assert len(active_md) == len(source_md) == 80
for r, original, m, sm in zip(active_rows, source_rows, active_md, source_md):
    expected = dict(original, event=original['event'].replace('Illi','illi'))
    assert r == expected, r['story_day']
    day = int(r['story_day'])
    assert (r['month'],int(r['day_of_month']),r['weekday_name'],int(r['weekday_number'])) == coordinates(day)
    assert m == [r['story_day'],r['month']+' '+r['day_of_month'],r['weekday_number']+' · '+r['weekday_name'],r['event']]
    assert sm == [original['story_day'],original['month']+' '+original['day_of_month'],original['weekday_number']+' · '+original['weekday_name'],original['event']]
assert read(ARC+'/VIOLET_DAILY_LEDGER_008.md').startswith(read(SOURCE+'/VIOLET_CORRECTED_DAILY_LEDGER.md').replace('Illi','illi'))

old = [r for r in md_rows(previous(LEDGER)) if len(r) == 6]
new = [r for r in md_rows(read(LEDGER)) if len(r) == 6]
assert len(new) == len(old) == 1160
assert [int(r[0]) for r in new] == list(range(1160))
assert new[:1081] == old[:1081], 'Historical rows changed'
for day, row in enumerate(new):
    assert (row[1],int(row[2]),row[4]) == coordinates(day)[:3], (day,row[:5])
    assert row[:5] == old[day][:5], day
    if day > 1080:
        assert row[5].split(' [Violet plan]',1)[0] == active_rows[day-1080]['event'], day
assert 'does not participate' in new[1021][5]
assert 'accepts invitation as seventh member' in new[1080][5]
events={int(r['story_day']):r['event'] for r in active_rows}
assert [d for d,e in events.items() if e.startswith("King's weekly raeon")] == [1098,1140]
for day in [1098,1140]:
    assert coordinates(day)[2:] == ('Aithen',5)
for day in range(1081,1087):
    assert events[day] == 'Recovery, personal time and ordinary slice-of-life. No royal game or royal-capital trip.'
assert 'no royal game' in events[1139]
for day in [1099,1100,1141]:
    assert 'Princess illi' in events[day]
for day in [1101,1142]:
    assert 'returns to Blue capital' in events[day]
assert 'no scheduled local tournament' in events[1120]

expeditions=[]
for route, start, end, phases in [('VTR-09',1087,1097,[4,3,4]),
                                ('VTR-01',1103,1117,[8,7]),
                                ('VTR-02',1123,1135,[7,6]),
                                ('VTR-10',1143,1159,[7,3,7])]:
    assert [d for d,e in events.items() if e.startswith(route)] == list(range(start,end+1))
    assert end-start+1 == sum(phases)
    path=ARC+'/TRAINING_ROUTES_005/'+route+'.md'
    assert read(path) == previous(path)
    expeditions.append(dict(route=route,start=start,end=end,days=end-start+1,phases=phases))
calendar=read(CALENDAR)
for i,name in enumerate(week,1):
    assert f'| {i} | {name} |' in calendar
assert '`((d + 4) % 6) + 1`' in calendar
assert calendar.split('# Academic cycle',1)[1] == previous(CALENDAR).split('# Academic cycle',1)[1]
games=read(GAMES)
assert 'each **Aithen**, the fifth weekday' in games
assert 'on **Aiven**, the sixth weekday' in games
assert 'on **Aiven**, sixth weekday' in games
assert games.split('| Story days |',1)[1].split('\n---',1)[0] == previous(GAMES).split('| Story days |',1)[1].split('\n---',1)[0]

old_report='CHECKPOINTS/VIOLET_CUMULATIVE_007/INTEGRATION_REPORT.md'
changed_report=read(old_report).split('\n\n',1)[1]
old_link='../../'+ARC+'/VIOLET_DAILY_LEDGER_007.md'
pinned='https://github.com/xApologies/MK163/blob/'+BASE+'/'+ARC+'/VIOLET_DAILY_LEDGER_007.md'
assert changed_report.replace(pinned,old_link) == previous(old_report)
reg=json.loads(read('PROVENANCE/SOURCE_REGISTRY.json'))
old_reg=json.loads(previous('PROVENANCE/SOURCE_REGISTRY.json'))
assert reg['subsequent_deliveries'][:-1] == old_reg['subsequent_deliveries']
assert reg['subsequent_deliveries'][-1]['archive_sha256'] == mapping['archive_sha256']

modified=git('diff','--name-only','--diff-filter=M',BASE).decode().splitlines()
deleted=git('diff','--name-only','--diff-filter=D',BASE).decode().splitlines()
added=sorted(set(git('diff','--name-only','--diff-filter=A',BASE).decode().splitlines()) |
             set(git('ls-files','--others','--exclude-standard').decode().splitlines()))
allowed={'.gitattributes','AGENTS.md',ARC+'/ARC.md',ARC+'/DUNGEON_ATLAS_002_BRIDGE.md',
         ARC+'/FIRST_VAELUM_TRIAL_R001_B041.md',ARC+'/TRAINING_ROUTES_005/README.md',
         'BOOKS/RED/BOOK_OVERVIEW.md',old_report,LEDGER,'CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md',
         'PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md',CALENDAR,GAMES,
         'WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/VIOLET_VAELUM_TRAVERSAL_LOGISTICS.md'}
assert set(modified)==allowed, set(modified)^allowed
assert set(deleted)=={ARC+'/VIOLET_DAILY_LEDGER_007.md',ARC+'/VIOLET_DAILY_LEDGER_007.csv'}
assert all(p.startswith((SOURCE+'/',CHECKPOINT+'/')) or p in {ARC+'/VIOLET_DAILY_LEDGER_008.md',ARC+'/VIOLET_DAILY_LEDGER_008.csv'} for p in added)
tracked=set(git('ls-files').decode().splitlines())
paths=(tracked-set(deleted))|set(added)
assert len(paths)==len({p.casefold() for p in paths})
assert not any(p.startswith(('_inbox/','AERA/','MK727/')) for p in paths)
for p in added+modified:
    assert (ROOT/p).stat().st_size < 100*1024*1024
assert sorted(p.name for p in (ROOT/ARC).glob('VIOLET*LEDGER*')) == ['VIOLET_DAILY_LEDGER_008.csv','VIOLET_DAILY_LEDGER_008.md']

links=0
for p in added+modified:
    if not p.endswith('.md') or p.startswith(SOURCE+'/'): continue
    for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',read(p)):
        target=unquote(target.strip('<>')).split('#',1)[0]
        if not target or re.match(r'^[a-z]+:',target,re.I): continue
        destination=(ROOT/p).parent/target
        assert destination.resolve().is_relative_to(ROOT) and destination.exists(), (p,target)
        links+=1
    if p.startswith(('BOOKS/','WORLD_CLOCK/','CONTINUITY/')) or p=='AGENTS.md':
        s=read(p)
        assert 'VIOLET_DAILY_LEDGER_007.md' not in s
        assert not re.search(r'Ailor\*{0,2}, (?:the )?(?:fifth weekday|weekday 5)|Aiven\*{0,2}, (?:the )?(?:first weekday|weekday 1)',s)
assert not re.search(r'\bIlli\b',read(ARC+'/VIOLET_DAILY_LEDGER_008.md').split('**Reading boundary:**',1)[0])
structural=json.loads(Path(args.structural_report).read_text(encoding='utf-8-sig'))
assert structural['status']=='PASS'
structural.pop('validated_root',None)
result=dict(status='PASS',baseline_commit=BASE,archive=mapping['archive'],archive_sha256=mapping['archive_sha256'],
            supplied_files_preserved=5,crc='PASS',source_hashes_verified=5,supplied_hash_manifest=False,
            calendar=dict(weekday_order=week,consecutive_running_rows=1160,range=[0,1159],
                          calendar_mismatches=0,unchanged_historical_rows=1081,source_schedule_rows=80,
                          replaced_event_rows=79,royal_games=[1098,1140],recovery_days=list(range(1081,1087)),
                          illi_visits=[1099,1100,1141],returns=[1101,1142],day1120='No scheduled local tournament'),
            expeditions=expeditions,internal_path_links_checked=links,structural_validation=structural,
            historical_sources_preserved=True,unrelated_owners_and_atlas_unchanged=True,
            old_007_report='Historical banner and pinned link only; original body and prior receipt preserved',
            obsolete_active_ledger_pairs_removed=1,active_daily_ledger_pairs=1,
            conflicts=[],omissions_in_supplied_correction=[],
            added=added,modified=modified,deleted=deleted,
            file_counts=dict(added=len(added),modified=len(modified),deleted=len(deleted)))
(ROOT/CHECKPOINT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',running_rows=1160,source_rows=80,unchanged_historical_rows=1081,
                     calendar_mismatches=0,expeditions=4,links=links,file_counts=result['file_counts']),indent=2))
