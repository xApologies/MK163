"""Validate Day 224 source fidelity, scoped supersession and preservation."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess
q=argparse.ArgumentParser();q.add_argument('--root',default='.');a=q.parse_args()
R=Path(a.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Git required: set MK163_GIT or PATH')
BASE='bffeb8354bd040912dedbeab1b218a434835a018'
W='PROVENANCE/WORKSHOP/GREEN_DAY224';C='CHECKPOINTS/GREEN_DAY224'
A='BOOKS/RED/ARCS/ARC_004/ARC.md';D='CONTINUITY/RED_RUNNING_DAY_LEDGER.md'
P='WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/BLACKSTONE_SPRITE_PROFESSOR.md'
E='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION'
modified=['.gitattributes','AGENTS.md',A,D,'CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md','WORLD_CLOCK/L1_FANTASY/PROPHECIES/FRAMEWORK_AND_CORRESPONDENCE.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/MAEGE_GLASS_AND_CONSTRUCTS.md',P,'WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/KAIRA.md']
added=[W+'/'+n for n in ['DAY_224_GREEN_ARC_AUTHOR_BEATS.md','README.md','SHA256_MANIFEST.json','executable.md','SOURCE_MAP.json']]+[C+'/'+n for n in ['INTEGRATION_REPORT.md','REVERSE_DIFF.md','UPSTREAM_VERIFICATION.json','UPSTREAM_VERIFICATION.md','validate_checkpoint.py','VALIDATION.json']]
checks=[]
def git(*args):return subprocess.check_output([G,'-c','core.autocrlf=false','-C',str(R),*args])
def read(n):return (R/n).read_bytes()
def txt(n):return read(n).decode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def current(n):return txt(n).split('## Earlier record · preserved verbatim',1)[0]
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members'];manifest=json.loads(read(W+'/SHA256_MANIFEST.json'))
check('all four original package members exactly preserved',len(members)==4 and all(sha(read(x['repository_path']))==x['sha256'] and len(read(x['repository_path']))==x['bytes'] for x in members.values()))
check('all three declared hashes and exact manifest accounting',len(manifest)==3 and set(manifest)==set(members)-{'SHA256_MANIFEST.json'} and all(members[n]['sha256']==h for n,h in manifest.items()))
archive=R/'_inbox'/source['physical_filename']
if archive.exists():check('local source ZIP hash unchanged',sha(archive.read_bytes())==source['archive_sha256'])
for n in modified:
 old=git('show',BASE+':'+n);now=read(n)
 if n.endswith('.md'):check(n+' entire earlier record preserved',now.endswith(old))
 elif n=='.gitattributes':check('all prior attributes preserved',now.startswith(old))
 else:
  x=json.loads(old);y=json.loads(now);entry=y['subsequent_deliveries'].pop()
  check('single append-only source registry record',x==y and entry['id']=='MK163_GREEN_DAY224')
prior={}
for line in git('ls-tree','-r','-z',BASE).split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t',1);prior[path.decode()]=meta.split()[2].decode()
drift=[]
for n in sorted(set(prior)-set(modified)):
 b=read(n)
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=prior[n]:drift.append(n)
check('all 870 untargeted baseline files byte-identical '+json.dumps(drift),len(prior)==884 and not drift)
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('exact scoped inventory: 11 added, 14 modified, zero deleted',len(added)==11 and len(modified)==14 and actual==set(added+modified) and not git('diff','--name-only','--diff-filter=D',BASE).strip())
check('no inbox tracking',not git('ls-files','_inbox').strip())
oldrows=re.findall(r'(?m)^\| (\d+) \|.*$',git('show',BASE+':'+D).decode())
newrows=re.findall(r'(?m)^\| (\d+) \|.*$',txt(D))
oldlines=re.findall(r'(?m)^\| \d+ \|.*$',git('show',BASE+':'+D).decode())
newlines=re.findall(r'(?m)^\| \d+ \|.*$',txt(D))
check('225 unique primary day rows 0 through 224 and 24 older summary rows unchanged',oldrows==newrows and oldlines==newlines and list(map(int,newrows[:225]))==list(range(225)) and len(newrows)==249)
src=txt(W+'/DAY_224_GREEN_ARC_AUTHOR_BEATS.md')
seq=src.split('## Author-selected day sequence\n',1)[1].split('## Natural Philosophy',1)[0].strip()
meet=src.split('## Natural Philosophy · professor meeting · 16:00–20:00\n',1)[1].split('## Mathematical',1)[0].strip().replace('Eldris','ELDRIS')
guards=src.split('## Mathematical and narrative guardrails\n',1)[1].strip()
check('complete eight source rows verbatim in existing scene owner',seq in current(A))
check('complete seven meeting points in existing character owner with protected ELDRIS normalization',meet in current(P) and len(re.findall(r'(?m)^\d\. ',meet))==7)
check('all five mathematical/narrative source guards preserved',guards in current(A) and len(re.findall(r'(?m)^- ',guards))==5)
times=[tuple(map(int,m)) for m in re.findall(r'(?m)^\| (\d\d):00–(\d\d):00 \|',seq)]
check('eight contiguous selected intervals 09 through 31, required class unchanged',times==[(9,11),(11,13),(13,15),(15,16),(16,20),(20,21),(21,22),(22,31)])
check('outline frontier, earlier morning detail and unassigned interval explicit',all(s in current(A) for s in ['not completed drafted prose','Days 218–223 remain unassigned','nothing after Day 224','first-day exception','illi teases her','illi — Kaira — Elaira','one first lecture','E means Elaira']))
check('professor identity, consent, availability, prophecy and growth limits explicit',all(s in current(P) for s in ['they/them','Natural Philosophy','16:00–20:00','not mandatory daily attendance','not a human infant','Singularity within the prophecy','scholarly excitement','identity and consent','aspirational target','collective-morphology','Aiven rest','senses the Black Sprite remain OPEN']))
tech=current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/MAEGE_GLASS_AND_CONSTRUCTS.md')
check('Maege stationery, six ink choices and absence of abacus scoped',all(s in tech for s in ['Maege Paper spiral notebooks and loose leaf','Maege Glass styluses','Red, Orange, Yellow, Green, Blue, Violet','no black ink selector','no abacus','lowercase maege/maegi','second glass substrate']))
for student in ['KAIRA','ILLI','ELAIRA']:
 n=E+'/'+student+'_PRIMARY.md';s=txt(n)
 body=re.search(r'<!-- BEGIN ORIGINAL [^\n]+SEMESTER_01\.md -->\n(.*?)\n<!-- END ORIGINAL',s,re.S)[1]
 day=re.split(r'(?m)^#{2,3} Day 1\b',body,1)[1];day=re.split(r'(?m)^#{2,3} Day 2\b',day,1)[0]
 check(student+' Semester I Day 1 required GFT I 11-13 remains',bool(re.search(r'\| 11:00[–—-]13:00 \|[^\n]*Genesis Field Theory I',day)))
 check(student+' recurring schedule and all five semesters unchanged',read(n)==git('show',BASE+':'+n))
v51=json.loads(read('CHECKPOINTS/BLACKSTONE_CURRICULUM_V5_1/VALIDATION.json'))
teaching=[n for n in prior if n.startswith(E+'/TEACHING/')]
check('v5.1 validated teaching corpus untouched: 1440 days, 736 classes, 512 master rows',v51['student_days']==1440 and v51['class_entries']==736 and v51['master_weekly_lessons']==512 and not set(teaching)&set(modified))
protected=[n for n in prior if n.startswith(('CONSTITUTIONS/','BOOKS/RED/ARCS/ARC_002/','BOOKS/RED/ARCS/ARC_003/','WORLD_CLOCK/L0_','WORLD_CLOCK/L1_FANTASY/PROPHECIES/MANUSCRIPTS/')) or Path(n).suffix.lower() in ['.jpg','.jpeg','.png','.webp','.pdf']]
check('constitutions, Orange/Yellow, mathematics, eight manuscripts and original images untouched',not set(protected)&set(modified))
up=json.loads(read(C+'/UPSTREAM_VERIFICATION.json'));local=up['local_black_manuscript']
check('four pinned AERA source records and exact local Black manuscript match',len(up['AERA']['files'])==4 and up['AERA']['commit']=='42437950ad2aa72ad885ff1a9129226da23d9286' and sha(read(local['path']))==local['sha256'] and local['exact_upstream_match'])
broken=[]
for n in sorted(set(added+modified)):
 if not n.endswith('.md') or n.startswith(W+'/'):continue
 for dest in re.findall(r'\]\(([^)]+)\)',current(n)):
  dest=dest.split('#',1)[0].strip('<>')
  if not dest or '://' in dest:continue
  target=(R/n).parent.joinpath(dest).resolve()
  if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([n,dest])
check('new local links resolve '+json.dumps(broken),not broken)
check('whitespace check',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf8')
check('repository structural validator',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_OPEN_ITEMS','baseline':BASE,'package_members':4,'manifest_hashes_verified':3,'selected_intervals':times,'historical_day_rows_preserved':225,'source_meeting_points_preserved':7,'source_guardrails_preserved':5,'current_curriculum_days_preserved':1440,'current_curriculum_classes_preserved':736,'counts':{'added':11,'modified':14,'deleted':0,'prior_unchanged':870},'added':sorted(added),'modified':sorted(modified),'deleted':[],'material_conflicts':[],'frontier':'Day 224 author-selected outline; drafting resumes 09:00; no completed prose claim','checks':checks,'repository_validation':json.loads(run.stdout),'open_items':['Convocation time','Professor name/gender/exact age/office address and sensing mechanism','Dialogue, exact prophecy wording used in scene and lesson exercises','Sprite age/name, individual/collective development mechanism and actual target date','Earlier teaching/prerequisite and source-volume limits']}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','manifest_hashes_verified','historical_day_rows_preserved','counts','material_conflicts']},indent=2))
