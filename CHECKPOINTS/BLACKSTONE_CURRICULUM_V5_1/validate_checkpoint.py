"""Validate the scoped v5.1 correction and preserve the complete original v5."""
from pathlib import Path
import argparse,collections,hashlib,json,os,re,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',default='.');a=p.parse_args()
R=Path(a.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Git required: set MK163_GIT or PATH.')
BASE='2d4881f32076bb22c84701bff76b37a0b051f8fc'
E='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION';T=E+'/TEACHING/V5'
W='PROVENANCE/WORKSHOP/BLACKSTONE_CURRICULUM_V5_1';OLD='PROVENANCE/WORKSHOP/BLACKSTONE_CURRICULUM_V5';C='CHECKPOINTS/BLACKSTONE_CURRICULUM_V5_1'
checks=[]
def git(*args):return subprocess.check_output([G,'-c','core.autocrlf=false','-C',str(R),*args])
def read(n):return (R/n).read_bytes()
def txt(n):return read(n).decode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,ok):
 checks.append({'check':n,'pass':bool(ok)})
 if not ok:raise AssertionError(n)
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members'];originals=source['original_v5_members']
base_hashes=json.loads(read(W+'/BASE_SHA256.json'));manifest=json.loads(read(W+'/SHA256_MANIFEST.json'))
check('eight exact current package members',len(members)==8 and all(len(read(x['repository_path']))==x['bytes'] and sha(read(x['repository_path']))==x['sha256'] for x in members.values()))
check('seven declared hashes and full accounting',set(manifest)==set(members)-{'SHA256_MANIFEST.json'} and all(h==members[n]['sha256'] for n,h in manifest.items()))
check('four expected baseline hashes match actual baseline Git objects',len(base_hashes)==4 and all(sha(git('show',BASE+':'+T+'/'+n))==h for n,h in base_hashes.items()))
check('all twelve original v5 members preserved exactly',len(originals)==12 and all(sha(read(x['repository_path']))==x['sha256'] and len(read(x['repository_path']))==x['bytes'] for x in originals.values()))
old_manifest=json.loads(read(originals['SHA256_MANIFEST.json']['repository_path']))
check('original eleven v5 hashes still validate through preservation map',set(old_manifest)==set(originals)-{'SHA256_MANIFEST.json'} and all(originals[n]['sha256']==h for n,h in old_manifest.items()))
check('historical v5 source map unchanged',sha(read(OLD+'/SOURCE_MAP.json'))==source['historical_v5_source_map_sha256'] and read(OLD+'/SOURCE_MAP.json')==git('show',BASE+':'+OLD+'/SOURCE_MAP.json'))
check('four old/new file mappings exact',len(source['replacements'])==4 and all(sha(read(x['original_path']))==x['before_sha256'] and sha(read(x['path']))==x['after_sha256'] for x in source['replacements']))
required={};patterns=0
for student in ['KAIRA','ILLI','ELAIRA']:
 owner=txt(E+'/'+student+'_PRIMARY.md');count=0
 for name,body in re.findall(r'<!-- BEGIN ORIGINAL (.+?SEMESTER_0[1-5]\.md) -->\n(.*?)\n<!-- END ORIGINAL',owner,re.S):
  sem=int(re.search(r'_0([1-5])',name)[1]);count+=1;day=None;ds={};rs=[]
  for line in body.splitlines():
   m=re.match(r'^#{2,3} Day ([1-6])\b',line)
   if m:day=int(m[1]);ds[day]=[]
   if day is None or not line.startswith('|'):continue
   cells=[v.strip().replace('**','') for v in line.strip('|').split('|')]
   m=re.fullmatch(r'(\d\d?):00[–—-](\d\d?):00',cells[0])
   if not m:continue
   start,end=map(int,m.groups());ds[day].append((start,end));act=cells[1];detail=' '.join(cells[2:])
   if re.search(r'REQUIRED|COMPULSORY',act) or (re.search('^Required',detail,re.I) and not re.search('optional',act,re.I)):
    rs.append((day,start,end,re.sub(r'REQUIRED|COMPULSORY','',act).strip(' —–:-')))
  check(student+f' semester {sem} 31-hour patterns',set(ds)==set(range(1,7)) and all(v[0][0]==0 and v[-1][1]==31 and all(a[1]==b[0] for a,b in zip(v,v[1:])) for v in ds.values()))
  check(student+f' semester {sem} enrollment',len(rs)==(4 if student=='KAIRA' and sem==2 else 3) and all(r[0]!=6 for r in rs))
  required[student,sem]=rs;patterns+=6
 check(student+' five full semester records',count==5)
weekday=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
records=[];shared=collections.defaultdict(list);counts=collections.Counter();primary_chapters=set();all_chapters=set()
title_pairs=[('First fold | and its address structure.','First fold.'),('Prime cell 0|0: identity versus occurrence.','Prime cell 0.')]
day_regex=r'(?m)^### Semester (\d) · Day (\d+) · Week (\d+) · (\w+)\n'
for student,expected in [('KAIRA',256),('ILLI',240),('ELAIRA',240)]:
 member='CALENDARS/'+student+'_FIVE_SEMESTERS_ALL_SUBJECTS_DAILY_v5.md'
 old=txt(originals[member]['repository_path']);new=txt(T+'/'+member)
 before=re.split(day_regex,old);after=re.split(day_regex,new)
 check(student+' unchanged introduction and 480 entries',len(before)==len(after)==2401 and before[0]==after[0])
 check(student+' topology double-brace example removed','{{∅,{a},X}}' not in new)
 seen=[];classes=[]
 for i in range(1,len(after),5):
  sem,day,week,wd,body=after[i:i+5];ob=before[i+4];sem,day,week=map(int,[sem,day,week]);seen.append((sem,day))
  assert after[i:i+4]==before[i:i+4]
  assert week==(day-1)//6+1 and wd==weekday[(day-1)%6]
  headings=re.findall(r'^#### (\d\d):00[–—-](\d\d):00 — (.+)',body,re.M)
  if not headings:
   assert body==ob and '**Required classes:** None.' in body and '**Knowledge cutoff:**' in body
   counts['nonclass']+=1
   if wd=='Aiven':counts['rest']+=1;assert 'no compulsory academic work' in body
   continue
  assert len(headings)==1 and wd!='Aiven'
  start,end,course=headings[0];start,end=map(int,[start,end]);assert end-start==2
  topic=re.search(r"\*\*Today's exact lesson:\*\* (.+)",body)[1]
  c=(student,sem,day,week,wd,start,end,course,topic);classes.append(c);records.append(c)
  shared[sem,course,week].append((day,wd,start,end,topic,body))
  normalized=body
  authority=re.findall(r'\*\*Instructional authority for this class:\*\* Primary Chapter (\d+) .*?; Chapter (\d+) [^\n]+',body)
  if authority:
   assert len(authority)==1;primary,support=map(int,authority[0]);counts['primary']+=1;counts['distinct_support']+=primary!=support
   primary_chapters.add(primary);all_chapters.update([primary,support])
   assert primary==int(re.search(r'Verified mathematical lesson anchor — Chapter (\d+)',body)[1])
   assert support==int(re.search(r'OPTIONAL supporting-source seminar.*?Formal Chapter (\d+)\)',body)[1])
   assert body.count('**OPTIONAL supporting-source seminar')==1
   assert 'is optional supporting/enrichment reading' in body and 'NOT an additional 120-minute session' in body and 'not considered learned unless a later narrative explicitly teaches them' in body
   mins=re.findall(r'(?m)^- \*\*[^\n]*?\((\d+) min\):\*\*',body);assert list(map(int,mins))==[15,30,30,30,15]
   normalized=re.sub(r'\*\*Instructional authority for this class:\*\* [^\n]+\n\n','',normalized)
   normalized=normalized.replace('**OPTIONAL supporting-source seminar — not a second required lesson and not assumed taught (new teaching design):**','**Source-specific mathematical seminar (new teaching design):**')
  else:
   counts['conventional']+=1
   line=re.search(r'(?m)^- \*\*Worked teaching example \(topic-specific, instructor-developed\):\*\* .+',body)[0]
   expected_line='- **Worked teaching example (topic-specific, instructor-developed):** Build a worked example specifically for **'+topic+'**. First state the definitions and prerequisites already introduced by this date; work through one representative case and one contrasting case, then explain the conclusion in the terminology of '+course+'. Do not reuse a later-course example or assert an experiment or outcome that has not been specified.'
   assert line==expected_line
   oldline=re.search(r'(?m)^- \*\*Worked teaching example:\*\* .+',ob)[0]
   normalized=normalized.replace(line,oldline)
   assert all(s in body for s in ['0–15','15–45','45–75','75–100','100–115','115–120'])
  for newtitle,oldtitle in title_pairs:
   token="**Today's exact lesson:** "+newtitle
   if token in normalized:
    counts['titles']+=1
    assert sem==1 and course=='Genesis Field Theory I' and day==(7 if 'First fold' in newtitle else 13)
    normalized=normalized.replace(token,"**Today's exact lesson:** "+oldtitle)
  assert normalized==ob,(student,sem,day,'unapproved change')
 check(student+' all calendar changes exactly reversible and scoped',seen==[(s,d) for s in range(1,6) for d in range(1,97)] and len(classes)==expected)
 for sem in range(1,6):
  actual=collections.Counter(((c[2]-1)%6+1,c[5],c[6],c[7]) for c in classes if c[1]==sem)
  check(student+f' semester {sem} exact 16-week timetable',actual==collections.Counter({r:16 for r in required[student,sem]}))
check('400 primary, 215 distinct supporting, 336 prompts, 6 titles',dict(counts)=={'primary':400,'distinct_support':215,'nonclass':704,'conventional':336,'rest':240,'titles':6})
check('15 primary chapters and all 18 total anchors',primary_chapters==set(range(39,57))-{43,49,56} and all_chapters==set(range(39,57)))
check('all 160 shared groups identical including full lesson text',sum(len(v)>1 for v in shared.values())==160 and all(len(set(v))==1 for v in shared.values()))
master='SYLLABUS/COMPLETE_FIVE_SEMESTERS_ALL_COURSES_16_WEEK_SYLLABUS_v5.md'
old=txt(originals[master]['repository_path']);new=txt(T+'/'+master)
expected=old.replace('| 2 | 7 | Ailar | First fold. |','| 2 | 7 | Ailar | First fold \\| and its address structure |').replace('| 3 | 13 | Ailar | Prime cell 0. |','| 3 | 13 | Ailar | Prime cell 0\\|0: identity versus occurrence |')
check('master has only two authorized escaped-pipe title corrections',new==expected and new!=old)
syll={};sem=None;course=None
for line in new.splitlines():
 m=re.match(r'## Semester (\d)',line)
 if m:sem=int(m[1])
 if line.startswith('### '):course=line[4:]
 m=re.match(r'^\| (\d+) \| (\d+) \| (\w+) \| (.+) \|$',line)
 if m:
  week,day,wd,topic=m.groups();key=(sem,course,int(week));assert key not in syll
  syll[key]=(int(day),wd,topic.replace('\\|','|').rstrip('.'))
check('512 master rows, 32 course sections, all calendar topics agree',len(syll)==512 and set(syll)==set(shared) and all(syll[c[1],c[7],c[3]]==(c[2],c[4],c[8].rstrip('.')) for c in records))
check('EDU-01/02 and Ailor preserved',all((3,11,13,'Quantum Field Theory I') in required[s,3] for s in ['KAIRA','ILLI']) and (5,11,13,'Chemistry I') in required['ELAIRA',3] and (3,17,19,'Differential Geometry II') in required['ELAIRA',3] and (4,15,17,'Introduction to Sigil Architecture') in required['KAIRA',2])
sv=source['source_verification'];prior_audit=json.loads(read(sv['prior_audit']))
check('pinned prior audit unchanged',sha(read(sv['prior_audit']))==sv['prior_audit_sha256'] and prior_audit['bricked']['commit']==sv['bricked_commit'] and prior_audit['AERA']['commit']==sv['AERA_commit'])
available={x['path'] for x in prior_audit['bricked']['files']}
refs=set()
for n in base_hashes:
 refs.update(re.findall(r'https://github.com/xApologies/_bricked/blob/bootstrap/canonical-architecture/(genesis_mathematics/[^)\s]+)',txt(T+'/'+n)))
check('all 18 formal reference paths in audited source corpus',refs<=available and len([n for n in refs if '/FORMAL/' in n])==18)
notes=txt(T+'/READING_NOTES.md').split('## Earlier v5 record',1)[0]
check('resolved scope and remaining limitations explicit',all(x in notes for x in ['T01 — RESOLVED','T02 — RESOLVED','215','185','336','not solved','course-transfer labels','primary board demonstration and assigned exercise','OPEN','end of Day 217']))
payload=[T+'/'+n for n in base_hashes]
modified=payload+['.gitattributes','AGENTS.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json',T+'/README.md',T+'/READING_NOTES.md']
added=[OLD+'/ORIGINAL_DELIVERY/'+n for n in base_hashes]+[W+'/'+n for n in ['executable.md','README.md','BASE_SHA256.json','SHA256_MANIFEST.json','SOURCE_MAP.json']]+[C+'/'+n for n in ['INTEGRATION_REPORT.md','TEACHING_PATCH.diff','VALIDATION.json','validate_checkpoint.py']]
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('exact scoped inventory: 13 added, 11 modified, no deletion',len(added)==13 and len(modified)==11 and actual==set(added+modified) and not git('diff','--name-only','--diff-filter=D',BASE).strip())
for n in modified:
 if n in payload:continue
 old=git('show',BASE+':'+n);now=read(n)
 if n.endswith('.md'):check(n+' earlier body preserved',now.endswith(old))
 elif n=='.gitattributes':check('prior attributes unchanged',now.startswith(old))
 else:
  x=json.loads(old);y=json.loads(now);entry=y['subsequent_deliveries'].pop()
  check('single append-only registry record',x==y and entry['id']=='MK163_BLACKSTONE_CURRICULUM_V5_1')
prior={}
for line in git('ls-tree','-r','-z',BASE).split(b'\0'):
 if not line:continue
 meta,path=line.split(b'\t',1);prior[path.decode()]=meta.split()[2].decode()
drift=[]
for n in sorted(set(prior)-set(modified)):
 b=read(n)
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=prior[n]:drift.append(n)
check('all 860 untargeted files byte-identical '+json.dumps(drift),len(prior)==871 and not drift)
check('no story/ledger/schedule-owner edits or inbox tracking',not any(n.startswith(('BOOKS/','CONTINUITY/','WORLD_CLOCK/L0_','WORLD_CLOCK/L1_','WORLD_CLOCK/L3_')) or n.endswith('_PRIMARY.md') for n in modified) and not git('ls-files','_inbox').strip())
patch=git('diff','--no-ext-diff','--no-color','--abbrev=40','--binary',BASE,'--',*payload)
check('stored exact four-file diff matches current Git comparison',patch==read(C+'/TEACHING_PATCH.diff'))
broken=[]
for n in sorted(set(added+modified)):
 if not n.endswith('.md') or n in payload or n.startswith((W+'/',OLD+'/ORIGINAL_DELIVERY/')):continue
 for dest in re.findall(r'\]\(([^)]+)\)',txt(n).split('## Earlier v5 record',1)[0]):
  dest=dest.split('#',1)[0].strip('<>')
  if not dest or '://' in dest:continue
  target=(R/n).parent.joinpath(dest).resolve()
  if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([n,dest])
check('new links resolve '+json.dumps(broken),not broken)
check('whitespace check',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf8')
check('repository structural validator',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_TEACHING_LIMITATIONS','baseline':BASE,'base_hashes_verified':4,'current_manifest_hashes':7,'original_v5_hashes_verified':11,'current_package_members':8,'original_v5_members_preserved':12,'student_days':1440,'class_entries':736,'classes_by_student':{'Kaira':256,'illi':240,'Elaira':240},'master_weekly_lessons':512,'shared_full_lesson_groups':160,'recurring_daily_patterns':patterns,'correction_counts':dict(counts),'primary_chapters':sorted(primary_chapters),'EDU-01':'RESOLVED','EDU-02':'RESOLVED','material_conflicts':[],'added':sorted(added),'modified':sorted(modified),'deleted':[],'counts':{'added':len(added),'modified':len(modified),'deleted':0,'prior_unchanged':860},'checks':checks,'repository_validation':json.loads(run.stdout),'remaining_limits':['Conventional prompts still require actual problems, worked solutions and prerequisite support','Supporting seminars not assumed taught; no completed attendance or mastery','Inherited shorthand governed by corrected exact titles and primary-authority paragraph','Predecessor daily files and individual Astrius/Vera volumes remain unavailable/unverified']}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','base_hashes_verified','current_manifest_hashes','original_v5_hashes_verified','student_days','class_entries','correction_counts','counts']},indent=2))
