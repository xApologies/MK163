"""Validate the v7 education repair without changing historical checkpoint evidence."""
from pathlib import Path
import argparse,hashlib,io,json,os,re,shutil,subprocess,zipfile
parser=argparse.ArgumentParser();parser.add_argument('--root',default='.');args=parser.parse_args()
R=Path(args.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Git is required (PATH or MK163_GIT).')
BASE='8f23e7cad7761e7889ab1a8c0f8253fd1cc83085';W='PROVENANCE/WORKSHOP/GREEN_DAY217_V7';OLD='PROVENANCE/WORKSHOP/GREEN_DAY217_V6';C='CHECKPOINTS/GREEN_DAY217_V7';I='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS'
checks=[]
def git(*a):return subprocess.check_output([G,'-C',str(R),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return (R/p).read_bytes()
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)})
    if not ok:raise AssertionError(name)
source=json.loads(read(W+'/SOURCE_MAP.json'));members=source['members']
check('all 34 mapped members match supplied hashes and sizes',len(members)==34 and all(sha(read(e['repository_path']))==e['sha256'] and len(read(e['repository_path']))==e['bytes'] for e in members.values()))
manifest=json.loads(read(W+'/MANIFEST_v7.json'))['files_sha256']
check('all 33 current outer manifest entries verified',set(manifest)==set(members)-{'MANIFEST_v7.json'} and all(sha(read(members[n]['repository_path']))==h for n,h in manifest.items()))
check('30 exact reused files and four new sources',sum(e['operation']=='reuse existing exact bytes' for e in members.values())==30 and sum(e['operation']=='preserve new source bytes' for e in members.values())==4)
check('no duplicated cumulative source tree',{p.relative_to(R/W).as_posix() for p in (R/W).rglob('*') if p.is_file()}=={n for n,e in members.items() if e['operation']=='preserve new source bytes'}|{'SOURCE_MAP.json'})
historical=json.loads(read(OLD+'/MANIFEST.json'))['files']
stale={n for n,e in historical.items() if sha(read(members[n]['repository_path']))!=e['sha256']}
check('only two declared historical outer hashes superseded',stale=={'executable.md','SOURCES/EDUCATION/illi.zip'})
check('historical manifest still validates original v6 files',all(sha(read(OLD+'/'+n))==e['sha256'] for n,e in historical.items()))
all_inner={};pattern_count=0;semester_count=0;nested_count=0;hashes=0;classes={};required={};current_body=None;old_body=None
for student,upper in [('Kaira','KAIRA'),('illi','ILLI'),('Elaira','ELAIRA')]:
    archive=read(members['SOURCES/EDUCATION/'+student+'.zip']['repository_path'])
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        check(student+' source ZIP integrity',z.testzip() is None);inner={n:z.read(n) for n in z.namelist()}
    all_inner[student]=inner;nested_count+=len(inner);declared=json.loads(inner['MANIFEST.json'])['files'];hashes+=len(declared)
    check(student+' inner declared hashes',all(sha(inner[n])==h for n,h in declared.items()))
    extra=set(inner)-set(declared)-{'MANIFEST.json'}
    check(student+' inner member accounting',extra==({'EDU_RECONCILIATION_2026-11-12.md'} if student=='illi' else set()))
    if extra:check('unlisted inner note verified by matching outer hash-covered note',inner[next(iter(extra))]==read(W+'/EDU_RECONCILIATION_v7.md'))
    canonical=read(I+'/BLACKSTONE_EDUCATION/'+upper+'_PRIMARY.md')
    check(student+' current status resolved',b'EDU-01 RESOLVED' in canonical.split(b'## Earlier record',1)[0] and b'EDU-02 RESOLVED' in canonical.split(b'## Earlier record',1)[0])
    for name,data in inner.items():
        if 'COURSE_MAP' in name or re.search(r'SEMESTER_0[1-5]\.md$',name):
            start=('<!-- BEGIN ORIGINAL '+name+' -->\n').encode();end=('\n<!-- END ORIGINAL '+name+' -->').encode()
            check(student+'/'+name+' exact full canonical source body',canonical.count(start)==1 and canonical.split(start,1)[1].split(end,1)[0]==data)
        if not re.search(r'SEMESTER_0[1-5]\.md$',name):continue
        sem=int(re.search(r'_0([1-5])',name).group(1));semester_count+=1;day=None;days={};req=[]
        for line in data.decode('utf-8').splitlines():
            h=re.match(r'^#{2,3} Day ([1-6])\b',line)
            if h:day=int(h.group(1));days[day]=[]
            if not line.startswith('|') or day is None:continue
            cells=[v.strip().replace('**','') for v in line.strip('|').split('|')];t=re.fullmatch(r'(\d\d?):00[–—-](\d\d?):00',cells[0])
            if not t:continue
            a,b=map(int,t.groups());days[day].append((a,b));activity=cells[1];detail=' '.join(cells[2:])
            if re.search(r'REQUIRED|COMPULSORY',activity) or (re.search(r'^Required',detail,re.I) and not re.search(r'optional',activity,re.I)):
                title=re.sub(r'REQUIRED|COMPULSORY','',activity).strip(' —–:-');req.append((day,a,b,title));classes.setdefault((sem,title),[]).append((student,day,a,b))
        check(student+'/'+name+' continuous 31-hour days without gaps/overlaps',set(days)==set(range(1,7)) and all(v[0][0]==0 and v[-1][1]==31 and all(a[1]==b[0] for a,b in zip(v,v[1:])) for v in days.values()))
        check(student+'/'+name+' expected instruction and protected rest',len(req)==(4 if student=='Kaira' and sem==2 else 3) and all(row[0]!=6 for row in req))
        required[(student,sem)]=req;pattern_count+=len(days)
check('15 semesters, 90 patterns, 24 source members, 20 declared inner hashes',(semester_count,pattern_count,nested_count,hashes)==(15,90,24,20))
check('all same-semester shared required classes agree',all(len({tuple(v[1:]) for v in values})==1 for values in classes.values()))
qft=classes[(3,'Quantum Field Theory I')]
check('EDU-01 resolved at 11:00–13:00 Aiveth',qft==[('Kaira',3,11,13),('illi',3,11,13)])
check('EDU-02 Elaira required slots preserved',(5,11,13,'Chemistry I') in required[('Elaira',3)] and (3,17,19,'Differential Geometry II') in required[('Elaira',3)])
check('EDU-02 all three free from required class 19:00–20:00',all(not (d==3 and a<20 and b>19) for student in ['Kaira','illi','Elaira'] for d,a,b,_ in required[(student,3)]))
check('Elaira still in required class during 18:00–19:00',any(d==3 and a<=18 and b>=19 for d,a,b,_ in required[('Elaira',3)]))
for student in ['Kaira','Elaira']:
    check(student+' original archive unchanged',read(members['SOURCES/EDUCATION/'+student+'.zip']['repository_path'])==read(OLD+'/SOURCES/EDUCATION/'+student+'.zip'))
with zipfile.ZipFile(io.BytesIO(read(OLD+'/SOURCES/EDUCATION/illi.zip'))) as z:old_inner={n:z.read(n) for n in z.namelist()}
new_inner=all_inner['illi'];changed_inner={n for n in old_inner if old_inner[n]!=new_inner.get(n)}
check('only illi Semester III and its manifest changed; one note added',changed_inner=={'PRINCESS_SEMESTER_03.md','MANIFEST.json'} and set(new_inner)-set(old_inner)=={'EDU_RECONCILIATION_2026-11-12.md'})
current_body=new_inner['PRINCESS_SEMESTER_03.md'];old_body=old_inner['PRINCESS_SEMESTER_03.md']
old_days=re.split(rb'(?m)^## Day ',old_body);new_days=re.split(rb'(?m)^## Day ',current_body)
check('all five untargeted illi Semester III days byte-identical',all(old_days[d]==new_days[d] for d in [1,2,4,5,6]))
check('corrected optional blocks explicitly represented',all(x in current_body for x in [b'| 13:00',b'| 18:00',b'| 19:00']) and b'All three available after' in current_body)

modified=['.gitattributes','AGENTS.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md',I+'/BLACKSTONE.md']+[I+'/BLACKSTONE_EDUCATION/'+s+'_PRIMARY.md' for s in ['KAIRA','ILLI','ELAIRA']]
added=[W+'/'+n for n,e in members.items() if e['operation']=='preserve new source bytes']+[W+'/SOURCE_MAP.json']+[C+'/'+n for n in ['INTEGRATION_REPORT.md','validate_checkpoint.py','VALIDATION.json']]
expected=set(added+modified);actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('only declared focused changes',actual==expected)
for path in modified:
    old=git('show',BASE+':'+path);now=read(path)
    if path.endswith('.md'):
        if path.endswith('/ILLI_PRIMARY.md'):
            after=now.split(b'\n---\n\n',1)[1];after=after.replace(current_body,old_body,1).replace(sha(current_body).encode(),sha(old_body).encode(),1)
            check('prior illi owner recoverable exactly by reversing authorized member update',after==old)
        else:check(path+' all prior bytes retained',now.endswith(old))
    elif path=='.gitattributes':check('prior Git attributes retained',now.startswith(old))
    elif path.endswith('SOURCE_REGISTRY.json'):
        before=json.loads(old);after=json.loads(now);entry=after['subsequent_deliveries'].pop();check('registry is one append-only delivery',before==after and entry['id']=='MK163_GREEN_DAY217_V7')
check('no deletions, inbox tracking, or narrative/chronology edits',not git('diff','--name-only','--diff-filter=D',BASE).strip() and not git('ls-files','_inbox').strip() and not any(p.startswith(('BOOKS/','CONTINUITY/','WORLD_CLOCK/L0_')) for p in actual))
check('historical v6 tree and reports unchanged',not any(p.startswith((OLD+'/', 'CHECKPOINTS/GREEN_DAY217_V6/')) for p in actual))
broken=[]
for path in expected:
    if not path.endswith('.md') or path.startswith(W+'/'):continue
    content=read(path).decode('utf-8').split('## Earlier record',1)[0]
    for dest in re.findall(r'\]\(([^)]+)\)',content):
        dest=dest.split('#',1)[0].strip('<>')
        if not dest or '://' in dest:continue
        target=(R/path).parent.joinpath(dest).resolve()
        if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([path,dest])
check('new local links resolve '+json.dumps(broken),not broken)
check('whitespace check',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf-8')
check('repository structural validator',run.returncode==0)
out={'status':'PASS','baseline':BASE,'outer_hashes_verified':33,'nested_hashes_verified':hashes,'source_members':34,'reused_members':30,'new_source_members':4,'nested_members':nested_count,'semesters':semester_count,'daily_patterns':pattern_count,'required_course_sessions':sum(len(v) for v in required.values()),'EDU-01':'RESOLVED','EDU-02':'RESOLVED','new_schedule_conflicts':[],'added':sorted(added),'modified':sorted(modified),'deleted':[],'counts':{'added':len(added),'modified':len(modified),'deleted':0,'prior_unchanged_files':825-len(modified)},'checks':checks,'repository_validation':json.loads(run.stdout),'manifest_notes':'Two historical v6 outer entries superseded. The unlisted inner reconciliation note exactly matches the outer hash-covered note; all members accounted for.'}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','outer_hashes_verified','nested_hashes_verified','daily_patterns','required_course_sessions','EDU-01','EDU-02','counts']},indent=2))
