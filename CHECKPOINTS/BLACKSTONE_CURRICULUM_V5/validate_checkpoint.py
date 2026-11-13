"""Reproduce the v5 curriculum checks without executing historical handoffs."""
from pathlib import Path
import argparse,collections,hashlib,json,os,re,shutil,subprocess
parser=argparse.ArgumentParser();parser.add_argument('--root',default='.');args=parser.parse_args()
R=Path(args.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Set MK163_GIT or put git on PATH.')
BASE='238ba655afccfb3fd9e8c1e3065f7c1917c19934'
E='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION';T=E+'/TEACHING/V5'
W='PROVENANCE/WORKSHOP/BLACKSTONE_CURRICULUM_V5';C='CHECKPOINTS/BLACKSTONE_CURRICULUM_V5'
checks=[]
def git(*a):return subprocess.check_output([G,'-C',str(R),*a])
def read(n):return (R/n).read_bytes()
def txt(n):return read(n).decode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,ok):
 checks.append({'check':n,'pass':bool(ok)})
 if not ok:raise AssertionError(n)
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members']
check('12 supplied members exact by size and SHA-256',len(members)==12 and all(len(read(x['repository_path']))==x['bytes'] and sha(read(x['repository_path']))==x['sha256'] for x in members.values()))
manifest=json.loads(read(W+'/SHA256_MANIFEST.json'))
check('all 11 declared hashes pass with complete manifest accounting',set(manifest)==set(members)-{'SHA256_MANIFEST.json'} and all(h==members[n]['sha256'] for n,h in manifest.items()))
check('one exact v8 reuse; 11 new originals',sum(x['operation']=='reuse existing exact bytes' for x in members.values())==1 and members['PRIOR_V4/SOURCE/V8_SYLLABUS.md']['repository_path']=='PROVENANCE/WORKSHOP/GREEN_DAY217_V8/CURRICULUM/BLACKSTONE_GENESIS_TRANSDUCTION_FIVE_SEMESTERS_v1.md')
required={};patterns=0
for student in ['KAIRA','ILLI','ELAIRA']:
 owner=txt(E+'/'+student+'_PRIMARY.md');semester_count=0
 for name,body in re.findall(r'<!-- BEGIN ORIGINAL (.+?SEMESTER_0[1-5]\.md) -->\n(.*?)\n<!-- END ORIGINAL',owner,re.S):
  sem=int(re.search(r'_0([1-5])',name)[1]);semester_count+=1;day=None;ds={};rs=[]
  for l in body.splitlines():
   m=re.match(r'^#{2,3} Day ([1-6])\b',l)
   if m:day=int(m[1]);ds[day]=[]
   if day is None or not l.startswith('|'):continue
   cells=[v.strip().replace('**','') for v in l.strip('|').split('|')]
   m=re.fullmatch(r'(\d\d?):00[–—-](\d\d?):00',cells[0])
   if not m:continue
   a,b=map(int,m.groups());ds[day].append((a,b));act=cells[1];detail=' '.join(cells[2:])
   if re.search(r'REQUIRED|COMPULSORY',act) or (re.search('^Required',detail,re.I) and not re.search('optional',act,re.I)):
    rs.append((day,a,b,re.sub(r'REQUIRED|COMPULSORY','',act).strip(' —–:-')))
  check(student+name+' continuous 31-hour patterns',set(ds)==set(range(1,7)) and all(v[0][0]==0 and v[-1][1]==31 and all(a[1]==b[0] for a,b in zip(v,v[1:])) for v in ds.values()))
  check(student+name+' required enrollment',len(rs)==(4 if student=='KAIRA' and sem==2 else 3) and all(r[0]!=6 for r in rs))
  patterns+=len(ds);required[student,sem]=rs
 check(student+' has all five full semester bodies',semester_count==5)
weekdays=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
records=[];day_records=[];shared=collections.defaultdict(list);study=[];math_count=0;conventional=0;rest=0;primary_sem=[]
for student,expected in [('KAIRA',256),('ILLI',240),('ELAIRA',240)]:
 t=txt(T+'/CALENDARS/'+student+'_FIVE_SEMESTERS_ALL_SUBJECTS_DAILY_v5.md')
 chunks=re.split(r'(?m)^### Semester (\d) · Day (\d+) · Week (\d+) · (\w+)\n',t)
 check(student+' exactly 480 entries',len(chunks)==1+480*5)
 seen=[];student_classes=[]
 for i in range(1,len(chunks),5):
  sem,day,week,wd,body=chunks[i:i+5];sem,day,week=map(int,[sem,day,week]);seen.append((sem,day))
  check(student+f' S{sem} D{day} week/day alignment',week==(day-1)//6+1 and wd==weekdays[(day-1)%6])
  entries=re.split(r'(?m)^#### (\d\d:\d\d[–—-]\d\d:\d\d) — (.+)\n',body)
  if len(entries)==1:
   check(student+f' S{sem} D{day} no-class/study scope','**Required classes:** None.' in body and '**Knowledge cutoff:**' in body)
   ref=re.search(r'\*\*Author-level study reference:\*\* (.+)',body);check('study reference supplied',bool(ref))
   study.append((student,sem,day,week,ref[1]))
  if wd=='Aiven':
   rest+=1;check(student+f' S{sem} D{day} protected Aiven',len(entries)==1 and 'no compulsory academic work' in body)
  for j in range(1,len(entries),3):
   time,course,lesson=entries[j:j+3];a,b=map(int,re.findall(r'(\d\d):00',time))
   topics=re.findall(r"\*\*Today's exact lesson:\*\* (.+)",lesson)
   check('one exact topic and two-hour required slot',len(topics)==1 and b-a==2)
   c={'student':student,'semester':sem,'day':day,'week':week,'weekday':wd,'start':a,'end':b,'course':course,'topic':topics[0]}
   records.append(c);student_classes.append(c);shared[sem,course,week].append((day,wd,a,b,topics[0],lesson))
   if '**Complete lesson delivery plan (v5, proposed):**' in lesson:
    math_count+=1
    mins=re.findall(r'(?m)^- \*\*[^\n]*?\((\d+) min\):\*\*',lesson)
    check('Genesis 120-minute budget',list(map(int,mins))==[15,30,30,30,15])
    primary=int(re.search(r'Verified mathematical lesson anchor — Chapter (\d+)',lesson)[1])
    seminar=int(re.search(r'Source-specific mathematical seminar.*?Formal Chapter (\d+)\)',lesson)[1])
    ex=re.search(r'\*\*Worked board problem:\*\* (.+)',lesson)[1]
    primary_sem.append((c,primary,seminar,ex))
   else:
    conventional+=1
    check('conventional proposed 120-minute budget and discipline boundary',all(x in lesson for x in ['0–15','15–45','45–75','75–100','100–115','115–120','not** extracted from']))
  day_records.append((student,sem,day,week,wd))
 check(student+' ordered unique days, all semesters',seen==[(s,d) for s in range(1,6) for d in range(1,97)])
 check(student+' declared required class count',len(student_classes)==expected)
 for sem in range(1,6):
  actual=collections.Counter(((c['day']-1)%6+1,c['start'],c['end'],c['course']) for c in student_classes if c['semester']==sem)
  check(student+f' S{sem} all 16 weekly meetings match current owner',actual==collections.Counter({r:16 for r in required[student,sem]}))
check('160 shared groups match full lesson text/date/time',sum(len(v)>1 for v in shared.values())==160 and all(len(set(v))==1 for v in shared.values()))
syll={};sem=None;course=None
for l in txt(T+'/SYLLABUS/COMPLETE_FIVE_SEMESTERS_ALL_COURSES_16_WEEK_SYLLABUS_v5.md').splitlines():
 m=re.match(r'## Semester (\d)',l)
 if m:sem=int(m[1])
 if l.startswith('### '):course=l[4:]
 m=re.match(r'\| (\d+) \| (\d+) \| (\w+) \| (.+) \|$',l)
 if m:
  week,day,wd,topic=m.groups();key=(sem,course,int(week));check('unique master row',key not in syll);syll[key]=(int(day),wd,topic)
check('master covers 32 course sections / 512 weekly lessons exactly',len(syll)==512 and set(syll)==set(shared) and all({k[2] for k in syll if k[:2]==sc}==set(range(1,17)) for sc in {k[:2] for k in syll}))
check('all 736 exact topics match master',all(syll[c['semester'],c['course'],c['week']]==(c['day'],c['weekday'],c['topic']) for c in records))
check('EDU-01 and EDU-02 remain resolved',all((3,11,13,'Quantum Field Theory I') in required[s,3] for s in ['KAIRA','ILLI']) and (5,11,13,'Chemistry I') in required['ELAIRA',3] and (3,17,19,'Differential Geometry II') in required['ELAIRA',3])
check('Kaira Semester II Ailor course preserved',(4,15,17,'Introduction to Sigil Architecture') in required['KAIRA',2])
notes=txt(T+'/READING_NOTES.md')
check('source corrections / readiness / operation scope documented',all(x in notes for x in ['First fold | and its address structure','Prime cell 0|0: identity versus occurrence','**not** a topology','215','T01','T02','T03','T04','T05','**positive** Hermitian','Resolve organizes/introduces basin energy','OPEN']))
# Optional review/preparation entries refer to earlier/future scheduled lessons in the same week.
def eff(c):
 if c['semester']==1 and c['course']=='Genesis Field Theory I' and c['week']==2:return 'First fold | and its address structure'
 if c['semester']==1 and c['course']=='Genesis Field Theory I' and c['week']==3:return 'Prime cell 0|0: identity versus occurrence'
 return c['topic'].rstrip('.')
for student,sem,day,week,ref in study:
 if (day-1)%6==5:continue
 cs=sorted((c for c in records if c['student']==student and c['semester']==sem and c['week']==week),key=lambda c:c['day'])
 earlier=[c for c in cs if c['day']<day];future=[c for c in cs if c['day']>day]
 expected=' '.join(label+': '+', '.join(c['course']+': '+eff(c) for c in subset)+'.' for label,subset in [('Optional review',earlier),('Optional preparation',future)] if subset)
 check(student+f' S{sem} D{day} review/preparation cutoff',ref==expected)
check('400 Genesis, 336 conventional, 704 nonclass, 240 protected rest',(math_count,conventional,len(study),rest)==(400,336,704,240))
math={};sem=None
for l in txt(W+'/PRIOR_V4/SYLLABUS/FIVE_SEMESTERS_16_WEEK_MATHEMATICS_SEQUENCE_v4.md').splitlines():
 m=re.match(r'## Semester (\d)',l)
 if m:sem=int(m[1])
 m=re.match(r'\| (\d+) \| Formal (\d+) — (.*?) \| (.*?) \|',l)
 if m:math[sem,int(m[1])]=(int(m[2]),m[4])
differences=[];dual=[]
for c,primary,seminar,example in primary_sem:
 meta={k:c[k] for k in ['student','semester','day','week','course']}
 if primary!=seminar:dual.append(dict(meta,primary_chapter=primary,seminar_chapter=seminar))
 expected,ex=math[c['semester'],c['week']]
 if expected!=seminar or example!=ex:differences.append(dict(meta,v4_outline_chapter=expected,v5_seminar_chapter=seminar,v4_example=ex,v5_example=example))
dis=json.loads(read(C+'/SOURCE_DISCREPANCIES.json'))
check('all 70 v4 outline differences documented exactly',len(differences)==70 and differences==dis['v4_outline_comparison']['records'])
check('all 215 dual-anchor entries documented exactly',len(dual)==215 and dual==dis['different_primary_and_seminar_anchors']['records'])
sr=json.loads(read(C+'/SOURCE_REVIEW.json'))
refs=set()
for x in members.values():
 if x['repository_path'].endswith('.md'):
  refs.update(re.findall(r'https://github.com/xApologies/_bricked/blob/bootstrap/canonical-architecture/(genesis_mathematics/[^)\s]+)',txt(x['repository_path'])))
available={e['path'] for e in sr['bricked']['files']}
check('every cited source path in pinned reviewed corpus',refs<=available and len([n for n in refs if '/FORMAL/' in n])==18)
check('pins and five AERA reads unchanged',sr['bricked']['commit']=='c89676fc26000ae6f5fdad66a56e118b285d9b1d' and sr['AERA']['commit']=='42437950ad2aa72ad885ff1a9129226da23d9286' and len(sr['AERA']['files'])==5)
# Direct finite topology check: nested family passes, literal singleton fails.
X=frozenset('abc');tau=frozenset([frozenset(),frozenset('a'),X])
def topology(family):
 return frozenset() in family and X in family and all(a<=X for a in family) and all(a|b in family and a&b in family for a in family for b in family)
check('topology alternative readings checked',topology(tau) and not topology(frozenset([tau])))
modified=['.gitattributes','AGENTS.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE.md',E+'/GENESIS_TRANSDUCTION_PROPOSED_SYLLABUS.md']+[E+'/'+s+'_PRIMARY.md' for s in ['KAIRA','ILLI','ELAIRA']]
added=[x['repository_path'] for x in members.values() if x['operation']=='preserve new source bytes']+[W+'/SOURCE_MAP.json',T+'/README.md',T+'/READING_NOTES.md']+[C+'/'+n for n in ['INTEGRATION_REPORT.md','REVERSE_DIFF.md','SOURCE_REVIEW.md','SOURCE_REVIEW.json','SOURCE_DISCREPANCIES.json','validate_checkpoint.py','VALIDATION.json']]
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('exact scope: 21 added, 11 modified, zero deletions',len(added)==21 and len(modified)==11 and actual==set(added+modified) and not git('diff','--name-only','--diff-filter=D',BASE).strip())
for n in modified:
 old=git('show',BASE+':'+n);now=read(n)
 if n.endswith('.md'):check(n+' entire old bytes retained',now.endswith(old))
 elif n=='.gitattributes':check('old attributes preserved',now.startswith(old))
 else:
  a=json.loads(old);b=json.loads(now);entry=b['subsequent_deliveries'].pop();check('registry exactly one append',a==b and entry['id']=='MK163_BLACKSTONE_CURRICULUM_V5')
prior_blobs={}
for entry in git('ls-tree','-r','-z',BASE).split(b'\0'):
 if not entry:continue
 meta,path=entry.split(b'\t',1);prior_blobs[path.decode()]=meta.split()[2].decode()
prior=list(prior_blobs)
for n in sorted(set(prior)-set(modified)):
 data=read(n);blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 check(n+' unchanged',blob==prior_blobs[n])
check('all story/history preserved; inbox excluded',len(prior)==850 and not any(n.startswith(('BOOKS/','CONTINUITY/','WORLD_CLOCK/L0_','WORLD_CLOCK/L1_','WORLD_CLOCK/L3_')) for n in actual) and not git('ls-files','_inbox').strip())
broken=[]
new_originals={x['repository_path'] for x in members.values()}
for n in sorted(set(added+modified)):
 if not n.endswith('.md') or n in new_originals:continue
 t=txt(n).split('## Earlier record',1)[0]
 for dest in re.findall(r'\]\(([^)]+)\)',t):
  dest=dest.split('#',1)[0].strip('<>')
  if not dest or '://' in dest:continue
  target=(R/n).parent.joinpath(dest).resolve()
  if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([n,dest])
check('new local links resolve '+json.dumps(broken),not broken)
check('whitespace',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf8')
check('repository structural validation',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_PROPOSAL_LIMITATIONS','baseline':BASE,'manifest_hashes':11,'supplied_members':12,'reused_members':1,'student_days':1440,'student_class_entries':736,'classes_by_student':{'Kaira':256,'illi':240,'Elaira':240},'semester_course_sections':32,'master_weekly_lessons':512,'shared_full_lesson_groups':160,'recurring_daily_patterns':patterns,'protected_rest_days':rest,'nonclass_days':len(study),'genesis_related_classes':math_count,'conventional_classes':conventional,'v4_outline_differences':len(differences),'dual_anchors':len(dual),'EDU-01':'RESOLVED','EDU-02':'RESOLVED','material_conflicts':[],'added':sorted(added),'modified':sorted(modified),'deleted':[],'counts':{'added':len(added),'modified':len(modified),'deleted':0,'prior_unchanged':850-len(modified)},'checks':checks,'repository_validation':json.loads(run.stdout),'limits':['Proposed instruction only; no completed attendance or learning','Topology intended typography OPEN','Conventional weekly examples, solutions and prerequisite support OPEN','Individual Astrius/Vera book inventory OPEN','Separate prior v3/v4 daily files and claimed original v8 daily ledger unavailable; no predecessor completeness claim']}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','manifest_hashes','student_days','student_class_entries','master_weekly_lessons','shared_full_lesson_groups','counts']},indent=2))
