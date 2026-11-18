"""Validate the additive 010 robe overlay and scoped ownership correction."""
from pathlib import Path,PurePosixPath
from urllib.parse import unquote
from zipfile import ZipFile
import argparse,csv,hashlib,io,json,re,shutil,stat,subprocess

ap=argparse.ArgumentParser();ap.add_argument('--git',default=shutil.which('git'));ap.add_argument('--structural-report',required=True)
args=ap.parse_args();assert args.git
ROOT=Path(__file__).resolve().parents[2];BASE='93b5fa3236fe0f45df8ca7e297f5782acb69c5dc'
ARC='BOOKS/RED/ARCS/ARC_006';SRC='PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_010';CK='CHECKPOINTS/VIOLET_CUMULATIVE_010'
OWNER='WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/GENESIS_ROBE.md';LEDGER='CONTINUITY/RED_RUNNING_DAY_LEDGER.md'
def git(*a):return subprocess.check_output([args.git,*a],cwd=ROOT)
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def prev(p):return git('show',BASE+':'+p).decode('utf-8-sig')
def csvrows(s):return list(csv.DictReader(io.StringIO(s,newline='')))
def mdrows(s,n):return [[v.strip() for v in l.split('|')[1:-1]] for l in s.splitlines() if re.match(r'^\| \d+ \|',l) and l.count('|')==n+1]
def lines(s,n):return [l for l in s.splitlines() if re.match(r'^\| \d+ \|',l) and l.count('|')==n+1]
week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
months=list(zip(['Aelor','Aerith','Aelora','Aevrin','Aelis','Aevor','Aelith','Aerion','Aeveth','Aesith','Aeleth'],[33,32,31,33,31,32,33,32,31,33,32]))
def coordinates(d):
 rem=(d+69)%353
 for name,count in months:
  if rem<count:return name,rem+1,week[(d+4)%6],(d+4)%6+1
  rem-=count

mapping=json.loads(read(SRC+'/SOURCE_MAP.json'));assert mapping['baseline']==BASE and len(mapping['files'])==5
archive=ROOT/'_inbox'/mapping['archive'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==mapping['archive_sha256']
with ZipFile(archive) as z:
 assert z.testzip() is None and len(z.infolist())==5 and len({n.casefold() for n in z.namelist()})==5
 for e in mapping['files']:
  name=e['path'];p=PurePosixPath(name);info=z.getinfo(name)
  assert not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name and not stat.S_ISLNK(info.external_attr>>16)
  b=(ROOT/e['original_destination']).read_bytes();assert b==z.read(name)
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
for e in mapping['preserved_baseline']:
 b=(ROOT/e['preserved_path']).read_bytes()
 assert b==git('show',BASE+':'+e['baseline_path']) and len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']

source=csvrows(read(SRC+'/GENESIS_ROBE_DAY_OVERLAY.csv'))
work=[int(r['story_day']) for r in source if r['overlay_type']=='GENESIS_ROBE_WORK']
milestones=[int(r['story_day']) for r in source if r['overlay_type']=='GENESIS_ROBE_MILESTONE']
windows=[(1120,1122),(1137,1139),(1161,1167),(1186,1187),(1211,1213),(1226,1229),(1253,1257),(1278,1280),(1299,1303)]
assert work==[d for start,end in windows for d in range(start,end+1)] and len(set(work))==35
assert milestones==[1303,1304,1320,1326,1327] and len(source)==40
assert len({(r['story_day'],r['overlay_type']) for r in source})==40
claim=json.loads(read(SRC+'/VALIDATION.json'))
assert claim['work_windows']==[list(w) for w in windows] and claim['milestone_days']==milestones and claim['overlay_rows']==40
applied=json.loads(read(CK+'/APPLIED_OVERLAY.json'));assert applied['baseline']==BASE and len(applied['rows'])==40
source_map={(int(r['story_day']),r['overlay_type']):r['addition'] for r in source}
clauses={}
for r in applied['rows']:
 d=r['story_day'];original=source_map[(d,r['overlay_type'])];assert r['source_addition']==original
 expected=original.replace('Princess Illi','Princess illi').replace(' Existing daily activity retained.','')
 if 1299<=d<=1302 and r['overlay_type']=='GENESIS_ROBE_WORK':
  expected=expected.replace('final repetitive ring-by-ring weaving/assembly and completion of the first Genesis Robe.','final repetitive ring-by-ring weaving/assembly toward completion of the first Genesis Robe on Day 1303.')
 assert r['active_addition']==expected and 1080<=d<=1346
 clauses.setdefault(d,[]).append(expected)
clauses={d:' '.join(parts) for d,parts in clauses.items()};assert len(clauses)==39

new=csvrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.csv'));old=csvrows(prev(ARC+'/VIOLET_DAILY_LEDGER_009.csv'))
assert len(new)==len(old)==267 and [int(r['story_day']) for r in new]==list(range(1080,1347))
md=mdrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.md'),4);assert len(md)==267
oldmd=lines(prev(ARC+'/VIOLET_DAILY_LEDGER_009.md'),4);newmd=lines(read(ARC+'/VIOLET_DAILY_LEDGER_009.md'),4)
for r,b,m,ol,nl in zip(new,old,md,oldmd,newmd):
 d=int(r['story_day']);expected=dict(b,event=b['event']+(' — '+clauses[d] if d in clauses else ''))
 assert r==expected,d
 assert (r['month'],int(r['day_of_month']),r['weekday_name'],int(r['weekday_number']))==coordinates(d)
 assert m==[r['story_day'],r['month']+' '+r['day_of_month'],r['weekday_number']+' · '+r['weekday_name'],r['event']]
 assert nl==(ol[:-2]+' — '+clauses[d]+' |' if d in clauses else ol),d
oldrunning=lines(prev(LEDGER),6);newrunning=lines(read(LEDGER),6)
running=mdrows(read(LEDGER),6);assert len(running)==len(oldrunning)==1347
assert [int(r[0]) for r in running]==list(range(1347))
for d,(r,ol,nl) in enumerate(zip(running,oldrunning,newrunning)):
 assert (r[1],int(r[2]),r[4])==coordinates(d)[:3]
 expected=ol[:-2]+' — '+clauses[d]+f' [Genesis Robe](../{OWNER}) |' if d in clauses else ol
 assert nl==expected,d
assert len([d for d in range(1347) if oldrunning[d]!=newrunning[d]])==39
events={int(r['story_day']):r['event'] for r in new}
assert 'places Blue' in events[1165] and 'Genesis Robe' in events[1165]
assert 'completes her FIRST and ONLY finished Genesis Robe' in events[1303]
for d in range(1299,1303):assert 'toward completion' in events[d] and 'completes her' not in events[d]
for d,prefix in [(1304,'VTR-07 descent'),(1320,'VTR-07 ascent'),(1326,"King's regular raeon"),(1327,'Kaira returns'),(1328,'VTR-08 descent'),(1346,'VTR-08 ascent')]:assert events[d].startswith(prefix),(d,events[d])
assert coordinates(1326)==('Aeleth',16,'Aithen',5)
assert 'Terms, acceptance and completion OPEN' in events[1326]
assert 'Princess illi' in events[1326] and 'Illi' not in events[1326]
for d in [1328,1346]:assert events[d]==old[d-1080]['event']

owner=read(OWNER);before=prev(OWNER)
assert owner.split('## Origin and structural realization',1)[1].split('## Development chronology',1)[0]==before.split('## Origin and structural realization',1)[1].split('## Three women and King',1)[0]
assert owner.split('## Crown research and Age of Knowledge',1)[1]==before.split('## Crown research and Age of Knowledge',1)[1]
assert 'each have one' not in owner and 'wearing their new robes' not in owner
assert 'sole owner' in owner and 'No second Genesis Robe is completed' in owner
assert 'physical Chainmail Robes' in owner and 'knitting a scarf' in owner and 'relatively quick' in owner
assert 'The Alchemist and Princess obtain robes' not in read(ARC+'/ARC.md')
assert 'COMPLETE AS AN OUTLINED ARC through Day 1346' in read(ARC+'/ARC.md')
assert 'VTR-11 remains unused and unscheduled' in read(ARC+'/ARC.md')
assert 'future, unscheduled Tournament' in read(ARC+'/ARC.md')

modified=git('diff','--no-renames','--name-only','--diff-filter=M',BASE).decode().splitlines()
deleted=git('diff','--no-renames','--name-only','--diff-filter=D',BASE).decode().splitlines()
added=sorted(set(git('diff','--no-renames','--name-only','--diff-filter=A',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines()))
allowed={'.gitattributes','AGENTS.md',ARC+'/ARC.md',ARC+'/VIOLET_DAILY_LEDGER_008.md',ARC+'/VIOLET_DAILY_LEDGER_009.md',ARC+'/VIOLET_DAILY_LEDGER_009.csv','BOOKS/RED/BOOK_OVERVIEW.md',LEDGER,'CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/KAIRA.md',OWNER}
assert set(modified)==allowed,set(modified)^allowed
assert not deleted
assert all(p.startswith((SRC+'/',CK+'/')) for p in added)
tracked=set(git('ls-files').decode().splitlines());paths=tracked|set(added)
assert len(paths)==len({p.casefold() for p in paths}) and not any(p.startswith(('_inbox/','AERA/','MK727/')) for p in paths)
links=0
for p in added+modified:
 assert (ROOT/p).stat().st_size<100*1024*1024
 if not p.endswith('.md') or p.startswith(SRC+'/'):continue
 for t in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',read(p)):
  t=unquote(t.strip('<>')).split('#',1)[0]
  if not t or re.match(r'^[a-z]+:',t,re.I):continue
  dest=(ROOT/p).parent/t;assert dest.resolve().is_relative_to(ROOT) and dest.exists(),(p,t)
  links+=1
activepairs=[p for p in (ROOT/ARC).glob('VIOLET_DAILY_LEDGER_*.csv')];assert [p.name for p in activepairs]==['VIOLET_DAILY_LEDGER_009.csv']
reg=json.loads(read('PROVENANCE/SOURCE_REGISTRY.json'));oldreg=json.loads(prev('PROVENANCE/SOURCE_REGISTRY.json'))
assert reg['subsequent_deliveries'][:-1]==oldreg['subsequent_deliveries']
assert reg['subsequent_deliveries'][-1]['archive_sha256']==mapping['archive_sha256']
structural=json.loads(Path(args.structural_report).read_text(encoding='utf-8-sig'));assert structural['status']=='PASS';structural.pop('validated_root',None)
result=dict(status='PASS',baseline_commit=BASE,archive=mapping['archive'],archive_sha256=mapping['archive_sha256'],source_files_verified=5,pre_correction_snapshots_verified=2,crc='PASS',package_paths_safe=True,supplied_hash_manifest=False,
 work=dict(windows=windows,distinct_days=35,milestone_days=milestones,overlay_rows=40,affected_dates=39),
 continuity=dict(violet_rows=267,violet_range=[1080,1346],running_rows=1347,running_range=[0,1346],calendar_mismatches=0,all_preexisting_events_retained=True,unchanged_running_rows=1308,unchanged_violet_rows=228,day1165_Blue_placement_preserved=True,day1303_completion=True,day1326_single_existing_game='Aeleth 16, Aithen/5',closure=1346,tournament_date='OPEN',VTR11='unused'),
 preservation=dict(technical_origin_and_seams='verbatim',crown_research='verbatim',prior_workshop_and_checkpoint_files='unchanged',routes_atlas_calendar_blackstone_other_arcs='unchanged',deleted_files=0),
 normalizations=applied['normalizations'],internal_links_checked=links,structural_validation=structural,conflicts=[],omitted_supplied_topics=[],
 open=['Exact daily breakthroughs','Field tests, outcomes and protection limits','Royal bargain terms, acceptance and outcome','Any later additional Genesis Robe','Tournament date/qualification and VTR-11 scheduling','Unrelated prior OPEN items and chapter prose'],
 added=added,modified=modified,deleted=deleted,file_counts=dict(added=len(added),modified=len(modified),deleted=0))
(ROOT/CK/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:result[k] for k in ['status','work','continuity','file_counts','internal_links_checked']},indent=2))
