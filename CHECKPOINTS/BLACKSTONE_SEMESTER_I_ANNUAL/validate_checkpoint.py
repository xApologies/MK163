"""Validate complete supplied Semester I, reconciled current views and preserved baseline."""
from pathlib import Path
import argparse,collections,csv,hashlib,io,json,os,re,shutil,subprocess,zipfile
q=argparse.ArgumentParser();q.add_argument('--root',default='.');a=q.parse_args()
R=Path(a.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
BASE='9e1f558043731ad33ba3517af1e3318e13d5bf0c'
E='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION'
L=E+'/SEMESTER_I_LIVE_MODEL';W='PROVENANCE/WORKSHOP/BLACKSTONE_SEMESTER_I';C='CHECKPOINTS/BLACKSTONE_SEMESTER_I_ANNUAL'
Y='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_ACADEMIC_CALENDAR.md'
D='CONTINUITY/RED_RUNNING_DAY_LEDGER.md';A='BOOKS/RED/ARCS/ARC_004/ARC.md'
checks=[]
def git(*args):return subprocess.check_output([G,'-c','core.autocrlf=false','-C',str(R),*args])
def read(n):return (R/n).read_bytes()
def txt(n):return read(n).decode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members']
def original(n):
 x=members[n]
 if 'container' in x:
  with zipfile.ZipFile(R/x['container']) as z:return z.read(x['member'])
 return read(x['repository_path'])
check('all 195 original members losslessly preserved or reused',len(members)==195 and all(sha(original(n))==x['sha256'] and len(original(n))==x['bytes'] for n,x in members.items()))
check('23 exact existing curriculum members reused, 172 new originals',sum('container' in x for x in members.values())==23 and len({x['repository_path'] for x in members.values() if 'repository_path' in x})==172)
manifest_checks=[];covered=set()
for n in ['SEMESTER_I_COMPLETE/ARCHIVE_MANIFEST_SHA256.txt','BLACKSTONE_INSTITUTION/NEW_FILES_SHA256.txt']:
 for line in original(n).decode().splitlines():
  m=re.fullmatch(r'([0-9a-f]{64})\s+(.+)',line)
  if not m:continue
  h,path=m.groups();path=path.lstrip('*');b=original(path);mode='whole current member'
  if path=='EXECUTABLE.md' and sha(b)!=h and n.startswith('SEMESTER_I_COMPLETE/'):
   b=b[b.index('# EXECUTABLE.md — Codex handoff for MK163 Semester I'.encode()):];mode='verbatim retained original handoff'
  manifest_checks.append({'manifest':n,'member':path,'mode':mode,'pass':sha(b)==h});covered.add(path)
check('all 194 outer declarations valid in documented scope',len(manifest_checks)==194 and all(x['pass'] for x in manifest_checks))
check('193 distinct payload members covered; only two manifests self-hashed',len(covered)==193 and set(members)-covered=={'SEMESTER_I_COMPLETE/ARCHIVE_MANIFEST_SHA256.txt','BLACKSTONE_INSTITUTION/NEW_FILES_SHA256.txt'})
nested=0
for who in ['Kaira','illi','Elaira']:
 for n,h in json.loads(original('SOURCES/'+who+'/MANIFEST.json'))['files'].items():
  check('nested '+who+'/'+n,sha(original('SOURCES/'+who+'/'+n))==h);nested+=1
check('20 nested curriculum declarations verified',nested==20)
archive=R/'_inbox'/source['physical_filename']
if archive.exists():check('source archive hash unchanged',sha(archive.read_bytes())==source['archive_sha256'])
def rows(s):
 out=[]
 for line in s.splitlines():
  if not line.startswith('|'):continue
  cols=[c.strip() for c in line.strip('|').split('|')]
  m=re.fullmatch(r'(\d\d):00[–—-](\d\d):00',cols[0])
  if m:
   assert len(cols)==4,cols
   out.append([*map(int,m.groups()),*cols[1:]])
 return out
def complete(v):return v and v[0][0]==0 and v[-1][1]==31 and all(r[0]<r[1] for r in v) and all(x[1]==y[0] for x,y in zip(v,v[1:]))
origdays={};days={};coverage=[]
for d in range(224,320):
 w=(d-224)//6+1;n=f'WEEK_{w:02d}/DAY_{d}.md'
 origdays[d]=rows(original(n).decode());days[d]=rows(txt(L+'/'+n))
 check('Day '+str(d)+' original and effective 31-hour three-character tables',complete(origdays[d]) and complete(days[d]))
 if d!=224:check('Day '+str(d)+' unchanged original',read(L+'/'+n)==original(n))
 coverage.append({'day':d,'week':w,'source_member':n,'current_owner':L+'/'+n,'current_blocks':len(days[d]),'status':'published outline retained by user' if d==224 else 'exact supplied author planning'})
check('exact 96 unique canonical day files',len(list((R/L).glob('WEEK_*/DAY_[0-9][0-9][0-9].md')))==96)
check('baseline sleep is labeled as template rather than an invented scene',all('recurring template' in r[2] for r in days[224] if r[0]==0))
check('source 1018 intervals; effective 1017; 2976 hours per student',sum(map(len,origdays.values()))==1018 and sum(map(len,days.values()))==1017 and sum(sum(r[1]-r[0] for r in v) for v in days.values())==2976)
csvcount=0;csvrows=0
for w in range(1,17):
 n=f'WEEK_{w:02d}/combined_schedule.csv'
 if n not in members:check('Week 3 has six supplied Markdown days and no fabricated CSV',w==3 and not (R/L/n).exists());continue
 csvcount+=1
 for label,b,expected in [('source',original(n),origdays),('current',read(L+'/'+n),days)]:
  by=collections.defaultdict(list)
  for x in csv.DictReader(io.StringIO(b.decode('utf-8-sig'))):
   d=int(x.get('day',x.get('story_day')));by[d].append([*map(int,re.findall(r'(\d\d):00',x['time'])),x['Kaira'],x['illi'],x['Elaira']])
  check(f'Week {w} {label} CSV exact text/time match to six Markdown tables',set(by)==set(range(224+6*(w-1),230+6*(w-1))) and all(v==expected[d] for d,v in by.items()))
  if label=='current':csvrows+=sum(map(len,by.values()))
check('all 15 supplied CSVs retained and current views checked',csvcount==15)
def cell(d,start,end,col):return next(r[col] for r in days[d] if (r[0],r[1])==(start,end))
required=collections.Counter()
for d,v in days.items():
 wd=(d-224)%6
 for student,col in [('Kaira',2),('illi',3),('Elaira',4)]:
  exp=(11,13,'Genesis Field Theory I') if wd==0 else (11,13,'Topology I') if wd==2 else (16,18,'Cardsmithing Fundamentals I') if wd==4 and student=='Kaira' else (18,20,'Native Genesis Control I' if student=='illi' else 'Anatomy I') if wd==4 else None
  if exp and d!=244:
   assert exp[2] in cell(d,*exp[:2],col),(d,student,exp);required[student]+=1
check('141 dated required class/student instances match primary times; Games exception explicit',dict(required)=={'Kaira':47,'illi':47,'Elaira':47} and all('Founders Games' in cell(244,11,15,c) for c in [2,3,4]) and 'catch-up' in cell(250,11,13,2))
check('current Day 224 explicit user decision',len(days[224])==10 and 'Woken by illi' in cell(224,9,10,2) and 'professor meeting' in cell(224,16,20,2) and all('Campus walk' in cell(224,21,22,c) for c in [2,3,4]))
check('original Day 224 alternative and Week 1 CSV retained separately',members['WEEK_01/DAY_224.md']['repository_path'].endswith('/SOURCE_DAY_224.md') and members['WEEK_01/combined_schedule.csv']['repository_path'].endswith('/SOURCE_combined_schedule.csv'))
check('no professor appointments after 306 or on Aiven/Games',all(not any('professor' in re.sub(r'no professor visit','',s.lower()) for r in days[d] for s in r[2:]) for d in days if d>=307 or (d-224)%6==5 or d==244))
check('last professor session is 306', 'final regular professor session' in cell(306,16,18,2))
check('explicit milestones and no premature Elaira construction', 'communication' in cell(237,16,18,2) and 'Violet' in cell(248,21,25,2) and 'humanoid' in cell(251,16,18,2) and 'gift to illi' in cell(253,23,25,2) and 'order rings' in cell(259,19,21,2) and 'begin E' in cell(293,21,25,2))
for d,course in [(278,'Genesis Field Theory I'),(280,'Topology I')]:
 check('second examination '+str(d),all(course in cell(d,11,13,c) and 'Second Examination' in cell(d,11,13,c) for c in [2,3,4]))
check('second specialist exams exact slots',all('Second Examination' in cell(282,*hrs,col) for hrs,col in [((16,18),2),((18,20),3),((18,20),4)]))
check('final exams 314/316/318 exact slots',all('FINAL' in cell(d,*hrs,c) for d,hrs,c in [(314,(11,13),2),(314,(11,13),3),(314,(11,13),4),(316,(11,13),2),(316,(11,13),3),(316,(11,13),4),(318,(16,18),2),(318,(18,20),3),(318,(18,20),4)]))
check('Day 295 six-hour event for all and no simultaneous craft block',all('seven realm representatives' in cell(295,19,25,c) for c in [2,3,4]) and not any(r[0]==23 for r in days[295]))
check('Day 319 symposium, feast, celebration all three',all('Symposium' in cell(319,13,17,c) and 'Feast' in cell(319,19,23,c) and 'Celebration' in cell(319,23,25,c) for c in [2,3,4]))
periods=[('Semester I',224,319,96),('Break I',320,340,21),('Semester II',341,436,96),('Break II',437,457,21),('Semester III',458,553,96),('Break III',554,574,21),('Administrative transition',575,576,2)]
check('annual exact ranges, inclusive lengths and 353-day total',all(f'| {n} | {s} | {e} | {k} |' in txt(Y) and e-s+1==k for n,s,e,k in periods) and sum(x[3] for x in periods)==353 and all(x[2]+1==y[1] for x,y in zip(periods,periods[1:])))
weekdays=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
check('continuous semester weekday phase',[(d,weekdays[(d-224)%6]) for d in [224,341,458,577]]==[(224,'Ailar'),(341,'Ailor'),(458,'Ailar'),(577,'Aiven')])
cov=json.loads(read(C+'/COVERAGE.json'));modified=cov['modified'];added=cov['added']
prior={}
for line in git('ls-tree','-r','-z',BASE).split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t',1);prior[path.decode()]=meta.split()[2].decode()
drift=[]
for n in sorted(set(prior)-set(modified)):
 b=read(n)
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=prior[n]:drift.append(n)
check('879 untargeted baseline files byte-identical '+json.dumps(drift),len(prior)==895 and not drift)
ledgerlines=re.findall(r'(?m)^\| \d+ \|.*$',txt(D))
check('320 unique primary daily rows and 24 historical summary rows retained',len(ledgerlines)==344 and [int(re.match(r'\| (\d+) \|',s)[1]) for s in ledgerlines[:320]]==list(range(320)))
monthdefs=[('Aelor',33),('Aerith',32),('Aelora',31),('Aevrin',33),('Aelis',31),('Aevor',32),('Aelith',33),('Aerion',32),('Aeveth',31),('Aesith',33),('Aeleth',32)]
for day in range(225,320):
 offset=(69+day)%353
 for m,l in monthdefs:
  if offset<l:dom=offset+1;break
  offset-=l
 assert ledgerlines[day].startswith(f'| {day} | {m} | {dom} | — | {weekdays[(day-224)%6]} |'),day
for n in modified:
 old=git('show',BASE+':'+n);now=read(n)
 if n==D:
  s=now.decode()
  for line in ledgerlines[225:320]:s=s.replace('\n'+line,'',1)
  check('entire earlier ledger preserved with only 95 inserted rows',s.encode().endswith(old))
 elif n.endswith('.md'):check(n+' complete earlier body retained',now.endswith(old))
 elif n=='.gitattributes':check('old attributes retained',now.startswith(old))
 else:
  x=json.loads(old);y=json.loads(now);v=y['subsequent_deliveries'].pop()
  check('single appended delivery registry entry',x==y and v['id']=='MK163_BLACKSTONE_SEMESTER_I_ANNUAL')
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('exact intended inventory, no deleted files or inbox tracking',len(added)==183 and len(modified)==16 and actual==set(added+modified) and not git('diff','--name-only','--diff-filter=D',BASE).strip() and not git('ls-files','_inbox').strip())
dec=json.loads(read(C+'/AUTHOR_RESOLUTIONS.json'))
check('two direct author resolutions recorded',dec['day224']['decision']=='Keep the published Day 224 outline' and dec['names']['decision']=='Confirm Aiselle = Alchemist; Caelor = Headmaster')
canon=txt('WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md').split('## Earlier record',1)[0]
check('confirmed names integrated without professor identity invention','Aiselle is the Alchemist; Caelor' in canon)
check('all primary/teaching, Orange/Yellow, image and historical checkpoint paths untouched',not any(n.startswith((E+'/TEACHING/','BOOKS/RED/ARCS/ARC_002/','BOOKS/RED/ARCS/ARC_003/','CONSTITUTIONS/','WORLD_CLOCK/L0_','CHECKPOINTS/')) or n.endswith(('_PRIMARY.md','.png','.jpg','.jpeg','.pdf','.zip')) for n in modified))
broken=[]
originalpaths={x['repository_path'] for x in members.values() if 'repository_path' in x}
for n in sorted(set(added+modified)-originalpaths):
 if not n.endswith('.md'):continue
 s=txt(n).split('## Earlier record · preserved verbatim',1)[0]
 for dest in re.findall(r'\]\(([^)]+)\)',s):
  dest=dest.split('#',1)[0].strip('<>')
  if not dest or '://' in dest:continue
  target=(R/n).parent.joinpath(dest).resolve()
  if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([n,dest])
check('all generated local links resolve '+json.dumps(broken),not broken)
check('Git whitespace check',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf8')
check('repository structural validator',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_OPEN_ITEMS','baseline':BASE,'supplied_members':195,'new_originals':172,'reused_source_zip_members':23,'effective_outer_payload_hashes':193,'outer_declarations_verified':194,'nested_hashes_verified':nested,'days':96,'characters':3,'hours_per_student':2976,'original_table_rows':1018,'current_table_rows':1017,'weekly_csvs':15,'current_csv_rows':csvrows,'required_class_instances':dict(required),'running_primary_days':320,'annual_cycle_days':353,'phase':{str(d):weekdays[(d-224)%6] for d in [224,341,458,577]},'counts':{'added':len(added),'modified':len(modified),'deleted':0,'prior_unchanged':879},'added':added,'modified':modified,'deleted':[],'blocking_conflicts':[],'retained_open_items':'See CONFLICTS_AND_SUPERSESSIONS.md; no invented overlap resolution, grades, mastery or robe completion','checks':checks,'manifest_checks':manifest_checks,'repository_validation':json.loads(run.stdout)}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','supplied_members','effective_outer_payload_hashes','outer_declarations_verified','nested_hashes_verified','days','weekly_csvs','required_class_instances','counts','blocking_conflicts']},indent=2))
