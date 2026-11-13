"""Validate final Break 02 fidelity, bounded timeline, owner reconciliation and preservation."""
from pathlib import Path
import argparse,csv,hashlib,io,json,os,re,shutil,subprocess
a=argparse.ArgumentParser();a.add_argument('--root',default='.');args=a.parse_args()
R=Path(args.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
BASE='1a5f3e9a539907521fdabe3b4f354d9e33423b77'
W='PROVENANCE/WORKSHOP/GREEN_SEMESTER_II_BREAK_02';C='CHECKPOINTS/GREEN_SEMESTER_II_BREAK_02'
A='BOOKS/RED/ARCS/ARC_004/ARC.md';D='CONTINUITY/RED_RUNNING_DAY_LEDGER.md'
H='WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md'
N='WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/NYX.md'
Q='WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/CHAINMAIL_ROBE_AND_AGE_OF_KNOWLEDGE.md'
E='WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md'
F='WORLD_CLOCK/L2_WORLD_CIVILIZATION/PROFESSIONS/BLACKSMITH_ROW_AND_ARTISANS.md'
I='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS'
Y=I+'/BLACKSTONE_ACADEMIC_CALENDAR.md';L=I+'/BLACKSTONE_EDUCATION/SEMESTER_I_LIVE_MODEL'
checks=[]
def git(*args):return subprocess.check_output([G,'-c','core.autocrlf=false','-C',str(R),*args])
def read(n):return (R/n).read_bytes()
def txt(n):return read(n).decode('utf8')
def current(n):return txt(n).split('## Earlier record · preserved verbatim',1)[0]
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members']
check('all eleven supplied members exactly recoverable',len(members)==11 and all(sha(read(x['repository_path']))==x['sha256'] and len(read(x['repository_path']))==x['bytes'] for x in members.values()))
manifest={}
for line in txt(W+'/MANIFEST_SHA256.txt').splitlines():
 m=re.fullmatch(r'([0-9a-f]{64})\s+(.+)',line)
 if m:manifest[m[2]]=m[1]
check('all ten manifest hashes and exact member accounting',len(manifest)==10 and set(manifest)==set(members)-{'MANIFEST_SHA256.txt'} and all(members[n]['sha256']==h for n,h in manifest.items()))
maprow=members['SOURCES/AUTHOR_DOMAIN_MAP.jpeg']
check('one exact existing map reused; no new image copy',maprow['repository_path']=='PROVENANCE/WORKSHOP/BOOK_RED_2026_11_07/SOURCES/LM_011/REFERENCES/USER_SUPPLIED_KINGDOM_MAP.jpeg' and maprow['sha256']=='3b97ee32e3fb39068923ca92c7ad52374487377a34c60f975049e430d4ed643a' and maprow['bytes']==527825 and not (R/W/'SOURCES/AUTHOR_DOMAIN_MAP.jpeg').exists())
archive=R/'_inbox'/source['physical_filename']
if archive.exists():check('local archive hash unchanged',sha(archive.read_bytes())==source['archive_sha256'])
priorreport=json.loads(read('CHECKPOINTS/BLACKSTONE_SEMESTER_I_ANNUAL/VALIDATION.json'))
check('Semester I dependency already integrated and validated',priorreport['status']=='PASS_WITH_DOCUMENTED_OPEN_ITEMS' and priorreport['days']==96 and len(list((R/L).glob('WEEK_*/DAY_[0-9][0-9][0-9].md')))==96)
rawcsv=list(csv.DictReader(io.StringIO(txt(W+'/CONTINUITY/BREAK_LEDGER.csv'))))
check('six supplied macro anchors only',len(rawcsv)==6 and [x['story_day'] for x in rawcsv]==['319','320-330','331','332','333-340','341'] and all(set(x)=={'story_day','period','status','anchor'} for x in rawcsv))
breakdays=list(range(320,331))+[331,332]+list(range(333,341))
check('21 break days exactly once, not 21 authored timetables',breakdays==list(range(320,341)) and len(breakdays)==21 and 'not finished scenes or 21 daily 31-hour timetables' in current(A))
check('Day 319 additive feast preserves name and social-statistics limits',all(x in current(A) for x in ['Aiselle, the Alchemist','Day 319','existing symposium/feast attendance and timetable remain intact','not quantified enrollment','Blue District residence in the Blue Domain capital']))
check('complete visit/commission context',all(x in current(A) for x in ['approximately eleven days','Nyx and the young Black Sprite','completes it during this visit','Exact completion day','early chainmail training','unnamed smith','personally made by Kaira','not identified as her established master mailwright supplier']))
check('331 gift and request; 332 separate two-robe procurement; no delivery inference',all(x in current(A) for x in ['Day 331','surprises **Elaira (E)**','conveys aina','Day 332','rickshaw','two separate personally crafted originals','payment terms','single production batch','no new ring delivery or construction start is established']))
check('aina exact name, relationship, office, White palace and no illi relocation',all(x in current(H) for x in ['Princess aina','exact lowercase','older sister','ruling princess','White District of the Blue Domain capital','she does not relocate','five-layer','Day 331','Aiselle remains the Alchemist']))
check('governor identity resolved without conflating illi',all(x in current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/CIVILIZATION/NOBILITY_AND_CIVIC_AUTHORITY.md') for x in ['Princess aina','older sister of illi','illi retains her separate non-governing role','governing residence','not the Violet Domain']))
check('three Yellow artisan plazas scoped to capital; original city/supplier and staging preserved',all(x in current(F) for x in ['three prestigious artisan plazas','Yellow District of the Blue Domain capital','does not relocate','originating Green Domain','Violet Dungeon staging','not identified','quantity, cost, arrival']))
check('wall all six colors, precise intervals, Sprite identity and no transport/new mechanics',all(x in current(N) for x in ['behind Kaira','Weeks 1–5, Days 224–253','Red, Orange, Yellow, Green, Blue and Violet','Weeks 6–16','Day 319','young Black Sprite','not the mature Sprite Professor','not direct stabilization of the Genesis Field','remains at Blackstone','no wall transport']))
check('gift complete during visit, presented 331, two separate new commissions in current ledger',all(x in current(Q) for x in ['incomplete on 319','Days 320–330','exact completion day/work hours OPEN','**331**','Princess aina','Unnamed Yellow District smith','**Two** new robes','Elaira','ring arrival and new construction start are not selected']))
check('Registry capacity distinct from demand and new commissions unpriced',all(x in current(E) for x in ['four smiths / twelve originals per month capacity','not guaranteed production','sales','No personal commission price','not Registry inventory']))
cov=json.loads(read(C+'/COVERAGE.json'));modified=cov['modified'];added=cov['added']
prior={}
for line in git('ls-tree','-r','-z',BASE).split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t',1);prior[path.decode()]=meta.split()[2].decode()
drift=[]
for n in sorted(set(prior)-set(modified)):
 b=read(n)
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=prior[n]:drift.append(n)
check('1061 untargeted baseline files byte-identical '+json.dumps(drift),len(prior)==1078 and not drift)
allrows=re.findall(r'(?m)^\| \d+ \|.*$',txt(D))
check('342 unique primary days 0–341 plus 24 historical summary rows',len(allrows)==366 and [int(re.match(r'\| (\d+) \|',s)[1]) for s in allrows[:342]]==list(range(342)))
months=[('Aelor',33),('Aerith',32),('Aelora',31),('Aevrin',33),('Aelis',31),('Aevor',32),('Aelith',33),('Aerion',32),('Aeveth',31),('Aesith',33),('Aeleth',32)]
wd=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
for d in range(320,342):
 offset=(69+d)%353
 for month,length in months:
  if offset<length:dom=offset+1;break
  offset-=length
 assert allrows[d].startswith(f'| {d} | {month} | {dom} | — | {wd[(d-224)%6]} |'),d
check('interval rows label unassigned detail, calendar anchor distinct',all('INTERVAL OUTLINE' in allrows[d] for d in list(range(320,331))+list(range(333,341))) and 'CALENDAR ANCHOR' in allrows[341] and '| Ailor |' in allrows[341])
for n in modified:
 old=git('show',BASE+':'+n);now=read(n)
 if n==D:
  s=now.decode()
  for line in allrows[320:342]:s=s.replace('\n'+line,'',1)
  check('entire previous ledger preserved after removing exactly 22 inserted rows',s.encode().endswith(old))
 elif n.endswith('.md'):check(n+' complete previous body retained',now.endswith(old))
 elif n=='.gitattributes':check('all previous Git attributes retained',now.startswith(old))
 else:
  x=json.loads(old);y=json.loads(now);v=y['subsequent_deliveries'].pop()
  check('one append-only source registry record',x==y and v['id']=='MK163_GREEN_SEMESTER_II_BREAK_02')
check('annual calendar unchanged and correct break/II ranges',read(Y)==git('show',BASE+':'+Y) and '| Break I | 320 | 340 | 21 |' in txt(Y) and '| Semester II | 341 | 436 | 96 |' in txt(Y))
protected=[n for n in prior if n.startswith((L+'/',I+'/BLACKSTONE_EDUCATION/TEACHING/','BOOKS/RED/ARCS/ARC_002/','BOOKS/RED/ARCS/ARC_003/','CHECKPOINTS/','CONSTITUTIONS/','WORLD_CLOCK/L0_')) or n.endswith(('_PRIMARY.md','.jpeg','.jpg','.png','.pdf','.zip'))]
check('Semester I source model, schedules, teaching, history, Orange/Yellow and images unchanged',not set(modified)&set(protected))
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('only intended paths: 16 added, 17 modified, zero deleted; inbox untracked',len(added)==16 and len(modified)==17 and actual==set(added+modified) and not git('diff','--name-only','--diff-filter=D',BASE).strip() and not git('ls-files','_inbox').strip())
check('no new semester daily timetable, duplicate image or inherited corpus',all(n.startswith((W+'/',C+'/')) for n in added) and not any(n.lower().endswith(('.jpeg','.jpg','.png','.zip')) for n in added))
broken=[]
for n in sorted(set(added+modified)):
 if not n.endswith('.md') or n.startswith(W+'/'):continue
 for dest in re.findall(r'\]\(([^)]+)\)',current(n)):
  dest=dest.split('#',1)[0].strip('<>')
  if not dest or '://' in dest:continue
  target=(R/n).parent.joinpath(dest).resolve()
  if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([n,dest])
check('generated local links resolve '+json.dumps(broken),not broken)
check('whitespace check',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf8')
check('repository structural validator',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_OPEN_ITEMS','baseline':BASE,'supplied_members':11,'manifest_hashes_verified':10,'new_originals':10,'reused_assets':1,'macro_source_records':6,'break_days':21,'ledger_rows_added':22,'running_primary_days':342,'Semester_I_daily_files_unchanged':96,'counts':{'added':16,'modified':17,'deleted':0,'prior_unchanged':1061},'added':added,'modified':modified,'deleted':[],'blocking_conflicts':[],'source_dispositions':['Retain confirmed Aiselle name; source OPEN is stale','Retain professor they/them and ended standing instruction; source his is not gender selection','Capital Yellow Rows added without relocating original-city Rows or supplier','Completed E gift is distinct from two pending commissions','Image reused by exact hash'], 'open_items':['Full 21-day timetables and dialogue','Exact interval dates/hours, E completion day and break whereabouts','Palace name/aina traits, smith identity','Prices, ring quantities, supplier, payment, batch, deadlines, ring arrival and construction start','No quantitative enrollment/sales or new biological mechanism'], 'checks':checks,'repository_validation':json.loads(run.stdout)}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','manifest_hashes_verified','reused_assets','break_days','Semester_I_daily_files_unchanged','counts','blocking_conflicts']},indent=2))
