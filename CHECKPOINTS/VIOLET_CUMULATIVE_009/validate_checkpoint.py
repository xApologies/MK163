"""Validate the scoped 009 continuation against published 008 and original routes."""
from pathlib import Path
from urllib.parse import unquote
from zipfile import ZipFile
from decimal import Decimal
import argparse,csv,hashlib,io,json,re,shutil,stat,subprocess
from pathlib import PurePosixPath

ap=argparse.ArgumentParser()
ap.add_argument('--git',default=shutil.which('git'))
ap.add_argument('--structural-report',required=True)
args=ap.parse_args();assert args.git
ROOT=Path(__file__).resolve().parents[2]
BASE='0ee036e7e2d015ab9d181fdc665fcce7757198f7'
ARC='BOOKS/RED/ARCS/ARC_006';ROUTES=ARC+'/TRAINING_ROUTES_005'
SRC='PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009';CK='CHECKPOINTS/VIOLET_CUMULATIVE_009'
ATLAS='WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON_ATLAS'
CALENDAR='WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md'
LEDGER='CONTINUITY/RED_RUNNING_DAY_LEDGER.md'
def git(*a):return subprocess.check_output([args.git,*a],cwd=ROOT)
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def prev(p):return git('show',BASE+':'+p).decode('utf-8-sig')
def csvrows(s):return list(csv.DictReader(io.StringIO(s,newline='')))
def mdrows(s):return [[v.strip() for v in l.split('|')[1:-1]] for l in s.splitlines() if re.match(r'^\| \d+ \|',l)]
def day_bytes(blob):return [l for l in blob.splitlines(keepends=True) if re.match(rb'^\| \d+ \|',l) and l.count(b'|')==7]
week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
months=list(zip(['Aelor','Aerith','Aelora','Aevrin','Aelis','Aevor','Aelith','Aerion','Aeveth','Aesith','Aeleth'],[33,32,31,33,31,32,33,32,31,33,32]))
def coordinates(d):
 rem=(d+69)%353
 for name,n in months:
  if rem<n:return name,rem+1,week[(d+4)%6],(d+4)%6+1
  rem-=n

mapping=json.loads(read(SRC+'/SOURCE_MAP.json'))
assert mapping['baseline']==BASE and len(mapping['files'])==6
archive=ROOT/'_inbox'/mapping['archive'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==mapping['archive_sha256']
with ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.infolist())==6 and len({n.casefold() for n in z.namelist()})==6
 for e in mapping['files']:
  n=e['path'];p=PurePosixPath(n);info=z.getinfo(n)
  assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n and not stat.S_ISLNK(info.external_attr>>16)
  b=(ROOT/e['original_destination']).read_bytes();assert z.read(n)==b
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
for e in mapping['preserved_baseline']:
 b=(ROOT/e['preserved_path']).read_bytes()
 assert b==git('show',BASE+':'+e['baseline_path'])
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
old_source_map=json.loads(read('PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_007/SOURCE_MAP.json'))
relocated={e['baseline_path']:e['preserved_path'] for e in mapping['preserved_baseline']}
originals_verified=0
for e in old_source_map:
 if e['original_destination']:
  p=relocated.get(e['original_destination'],e['original_destination'])
  assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==e['sha256'],p
  originals_verified+=1

baseline=csvrows(prev(ARC+'/VIOLET_DAILY_LEDGER_008.csv'))
extension=csvrows(read(SRC+'/VIOLET_EXTENSION_1160_1346.csv'))
cumulative=csvrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.csv'))
assert len(baseline)==80 and len(extension)==187 and len(cumulative)==267
assert cumulative[:80]==baseline
expected=[dict(r,event=r['event'].replace('Illi','illi')) for r in extension]
assert cumulative[80:]==expected
assert [int(r['story_day']) for r in cumulative]==list(range(1080,1347))
assert mdrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.md'))[:80]==mdrows(prev(ARC+'/VIOLET_DAILY_LEDGER_008.md'))
for r,m in zip(cumulative,mdrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.md'))):
 assert (r['month'],int(r['day_of_month']),r['weekday_name'],int(r['weekday_number']))==coordinates(int(r['story_day']))
 assert m==[r['story_day'],r['month']+' '+r['day_of_month'],r['weekday_number']+' · '+r['weekday_name'],r['event']]
assert len(mdrows(read(ARC+'/VIOLET_DAILY_LEDGER_009.md')))==267
assert not mdrows(read(ARC+'/VIOLET_DAILY_LEDGER_008.md'))
running=[r for r in mdrows(read(LEDGER)) if len(r)==6]
assert [int(r[0]) for r in running]==list(range(1347))
assert day_bytes((ROOT/LEDGER).read_bytes())[:1160]==day_bytes(git('show',BASE+':'+LEDGER))
for d,r in enumerate(running):
 assert (r[1],int(r[2]),r[4])==coordinates(d)[:3],d
 if d>=1160:assert r[5].split(' [Violet plan]',1)[0]==expected[d-1160]['event']
assert read(CALENDAR).replace('VIOLET_DAILY_LEDGER_009.md','VIOLET_DAILY_LEDGER_008.md')==prev(CALENDAR)
anchors={1165:('Aevor',16,'Aiven',6),1188:('Aelith',7,'Aithen',5),1209:('Aelith',28,'Aiden',2),1225:('Aerion',11,'Aiven',6),1250:('Aeveth',4,'Ailar',1),1277:('Aeveth',31,'Ailor',4),1298:('Aesith',21,'Ailar',1),1320:('Aeleth',10,'Aithen',5),1326:('Aeleth',16,'Aithen',5),1346:('Aelor',4,'Ailar',1)}
for d,c in anchors.items():assert coordinates(d)==c
events={int(r['story_day']):r['event'] for r in cumulative}
assert 'places Blue' in events[1165] and 'result OPEN' in events[1225]
assert [d for d,e in events.items() if d>=1160 and e.startswith("King's regular")]==[1188,1326]
assert 'Princess illi' in events[1189] and 'Princess illi' in events[1190]
assert 'returns to Blue capital' in events[1191] and 'returns to Blue capital' in events[1327]
for start,end,count in [(1251,1258,8),(1278,1281,4),(1299,1303,5)]:
 assert end-start+1==count and all(not events[d].startswith('VTR-') for d in range(start,end+1))

edges={r['edge_id']:r for r in csvrows(read(ATLAS+'/data/edges.csv'))}
index={r['route_id']:r for r in csvrows(read(ROUTES+'/ROUTE_INDEX.csv'))}
old_index={r['route_id']:r for r in csvrows(prev(ROUTES+'/ROUTE_INDEX.csv'))}
passages=csvrows(read(ROUTES+'/ROUTE_PASSAGES.csv'))
assert len(index)==11 and len(list((ROOT/ROUTES).glob('VTR-*.md')))==11
for rid,r in index.items():
 for key in r:
  if key!='status':assert r[key]==old_index[rid][key],(rid,key)
 if rid in [f'VTR-{n:02}' for n in range(3,9)]:assert r['status']=='AUTHOR_SELECTED_SCHEDULE_009'
 else:assert r['status']==old_index[rid]['status']
receipt=json.loads(read(CK+'/ROUTE_VALIDATION.json'));assert len(receipt['occurrences'])==8
manifest=read(SRC+'/EXPEDITION_NODE_ROUTE_MANIFEST.md')
occupied=[];edge_uses=0
for o in receipt['occurrences']:
 rid=o['route_id'];r=index[rid];s=read(ROUTES+'/'+rid+'.md');nodes=o['outbound_nodes'];returns=o['return_nodes']
 block=next(b for name,b in re.findall(r'^## (VTR-\d+)(.*?)(?=^## |\Z)',manifest,re.M|re.S) if name==rid)
 assert nodes==re.search(r'Outbound nodes \(\d+\): `([^`]+)`',block)[1].split(' → ')
 assert returns==re.search(r'Return: `([^`]+)`',block)[1].split(' → ')==nodes[::-1]
 assert nodes==r['node_sequence'].split(' → ')==re.search(r'\*\*Outbound:\*\* `([^`]+)`',s)[1].split(' → ')
 assert returns==r['return_sequence'].split(' → ')==re.search(r'\*\*Return:\*\* `([^`]+)`',s)[1].split(' → ')
 pp=sorted([p for p in passages if p['route_id']==rid],key=lambda p:int(p['step']))
 assert len(pp)==len(nodes)-1 and [p['edge_id'] for p in pp]==o['edge_ids']
 distance=Decimal(0)
 for i,p in enumerate(pp):
  e=edges[p['edge_id']];assert [p['source'],p['target']]==nodes[i:i+2]
  assert set(nodes[i:i+2])=={e['source'],e['target']} and e['direction']=='UNDIRECTED_TOPOLOGY'
  assert Decimal(p['distance_mi'])==Decimal(e['modeled_centerline_mi'])
  distance+=Decimal(p['distance_mi'])
 assert abs(distance-Decimal(r['one_way_mi']))<=Decimal('.0005')
 assert abs(distance*2-Decimal(r['round_trip_mi']))<=Decimal('.0005')
 assert str(distance)==o['modeled_distance_sum']
 assert [d for d in range(1160,1347) if events[d].startswith(rid)]==list(range(o['start'],o['end']+1))
 assert o['end']-o['start']+1==o['days']==sum(p['days'] for p in o['phases'])
 for phase in o['phases']:
  for i,d in enumerate(range(phase['start'],phase['end']+1),1):
   assert phase['kind'] in events[d] and f"day {i} of {phase['days']}" in events[d]
 assert 'surface return' in events[o['end']]
 assert s.split('## Node-by-node expectations',1)[1].split('## Operational interpretation',1)[0]==prev(ROUTES+'/'+rid+'.md').split('## Node-by-node expectations',1)[1].split('## Operational interpretation',1)[0]
 occupied+=list(range(o['start'],o['end']+1));edge_uses+=len(pp)
assert len(occupied)==len(set(occupied))==134 and edge_uses==107
assert not set(occupied)&{1165,1188,1189,1190,1191,1225,1326,1327}
assert not any('VTR-11' in e for e in events.values())
assert read(ROUTES+'/VTR-11.md')==prev(ROUTES+'/VTR-11.md')

modified=git('diff','--no-renames','--name-only','--diff-filter=M',BASE).decode().splitlines()
deleted=git('diff','--no-renames','--name-only','--diff-filter=D',BASE).decode().splitlines()
added=sorted(set(git('diff','--no-renames','--name-only','--diff-filter=A',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines()))
allowed={'.gitattributes','AGENTS.md',ARC+'/ARC.md',ARC+'/DUNGEON_ATLAS_002_BRIDGE.md',ARC+'/FIRST_VAELUM_TRIAL_R001_B041.md',ROUTES+'/README.md',ROUTES+'/ROUTE_INDEX.csv',ARC+'/VIOLET_DAILY_LEDGER_008.md','BOOKS/RED/BOOK_OVERVIEW.md','CHECKPOINTS/VIOLET_CALENDAR_RESTORATION_008/INTEGRATION_REPORT.md',LEDGER,'CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md',CALENDAR,'WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/VIOLET_VAELUM_TRAVERSAL_LOGISTICS.md'}|{ROUTES+f'/VTR-{n:02}.md' for n in range(3,11)}
assert set(modified)==allowed,set(modified)^allowed
assert deleted==[ARC+'/VIOLET_DAILY_LEDGER_008.csv']
assert all(p.startswith((SRC+'/',CK+'/')) or p in {ARC+'/VIOLET_DAILY_LEDGER_009.md',ARC+'/VIOLET_DAILY_LEDGER_009.csv'} for p in added)
paths=(set(git('ls-files').decode().splitlines())-set(deleted))|set(added)
assert len(paths)==len({p.casefold() for p in paths})
assert not any(p.startswith(('_inbox/','AERA/','MK727/')) for p in paths)
links=0
for p in added+modified:
 assert (ROOT/p).stat().st_size<100*1024*1024
 if not p.endswith('.md') or p.startswith(SRC+'/'):continue
 for t in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',read(p)):
  t=unquote(t.strip('<>')).split('#',1)[0]
  if not t or re.match(r'^[a-z]+:',t,re.I):continue
  dest=(ROOT/p).parent/t
  assert dest.resolve().is_relative_to(ROOT) and dest.exists(),(p,t)
  links+=1
old_report='CHECKPOINTS/VIOLET_CALENDAR_RESTORATION_008/INTEGRATION_REPORT.md'
assert read(old_report).split('\n\n',1)[1].replace('../../'+SRC+'/BASELINE_008/VIOLET_DAILY_LEDGER_008.csv','../../'+ARC+'/VIOLET_DAILY_LEDGER_008.csv')==prev(old_report)
oldreg=json.loads(prev('PROVENANCE/SOURCE_REGISTRY.json'));reg=json.loads(read('PROVENANCE/SOURCE_REGISTRY.json'))
assert reg['subsequent_deliveries'][:-1]==oldreg['subsequent_deliveries']
assert reg['subsequent_deliveries'][-1]['archive_sha256']==mapping['archive_sha256']
structural=json.loads(Path(args.structural_report).read_text(encoding='utf-8-sig'));assert structural['status']=='PASS';structural.pop('validated_root',None)
result=dict(status='PASS',baseline_commit=BASE,archive=mapping['archive'],archive_sha256=mapping['archive_sha256'],crc='PASS',package_paths_safe=True,supplied_source_files=6,source_hashes_verified=6,supplied_hash_manifest=False,
 calendar=dict(running_rows=1347,range=[0,1346],violet_rows=267,violet_range=[1080,1346],extension_rows=187,baseline_fields_unchanged=80,previous_running_rows_byte_identical=1160,mismatches=0,weekday_order=week,anchors={str(k):list(v) for k,v in anchors.items()}),
 routes=dict(new_occurrences=8,newly_scheduled_routes=6,repeats=2,cumulative_occurrences=12,cumulative_distinct_routes=10,original_route_records=11,unused='VTR-11',extension_expedition_days=134,outbound_edge_uses_verified=107,reverse_edge_uses_verified=107,atlas_and_passage_data_unchanged=True),
 preservation=dict(prior_007_originals_hash_verified=originals_verified,relocated_original_route_files=6,exact_archived_008_files=2,all_previous_workshop_files_unchanged=True,blackstone_and_other_arcs_unchanged=True),
 active_violet_schedule_pairs=1,historical_008_navigation_stub=True,internal_links_checked=links,structural_validation=structural,conflicts=[],omitted_supplied_topics=[],
 open=['Day 1225 tournament result','Royal-game results','King tournament date, qualification and scenes','VTR-11 schedule','Exact node/day assignments, individual encounters and outcomes','Previously unassigned CSR manufacture and character details','Chapter prose'],
 added=added,modified=modified,deleted=deleted,file_counts=dict(added=len(added),modified=len(modified),deleted=len(deleted)))
(ROOT/CK/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:result[k] for k in ['status','calendar','routes','file_counts','internal_links_checked']},indent=2))
