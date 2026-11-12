"""Reproduce v8 source, preservation, timeline and curriculum checks."""
from pathlib import Path
import argparse,hashlib,io,json,os,re,shutil,subprocess,zipfile
parser=argparse.ArgumentParser();parser.add_argument('--root',default='.');args=parser.parse_args();R=Path(args.root).resolve()
G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Git required on PATH or MK163_GIT.')
BASE='ec3c96593c9d90c116545263becde745395066be';W='PROVENANCE/WORKSHOP/GREEN_DAY217_V8';C='CHECKPOINTS/GREEN_DAY217_V8';I='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS';E=I+'/BLACKSTONE_EDUCATION';checks=[]
def git(*a):return subprocess.check_output([G,'-C',str(R),*a])
def read(p):return (R/p).read_bytes()
def text(p):return read(p).decode('utf-8')
def head(p):return text(p).split('## Earlier record',1)[0]
def sha(b):return hashlib.sha256(b).hexdigest()
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)})
    if not ok:raise AssertionError(name)
sm=json.loads(read(W+'/SOURCE_MAP.json'));members=sm['members'];mf=json.loads(read(W+'/MANIFEST_v8.json'))['files']
check('41 mapped members and all 40 current hashes/sizes',len(members)==41 and set(mf)==set(members)-{'MANIFEST_v8.json'} and all(sha(read(members[n]['repository_path']))==v['sha256'] and len(read(members[n]['repository_path']))==v['bytes'] for n,v in mf.items()))
check('all mapped hashes including current manifest',all(sha(read(v['repository_path']))==v['sha256'] for v in members.values()))
check('34 exact reuses and seven new sources',sum(v['operation']=='reuse exact existing bytes' for v in members.values())==34 and sum(v['operation']=='preserve new source bytes' for v in members.values())==7)
new_sources={n for n,e in members.items() if e['operation']=='preserve new source bytes'}
check('no duplicate source tree', {p.relative_to(R/W).as_posix() for p in (R/W).rglob('*') if p.is_file()}==new_sources|{'SOURCE_MAP.json','REFERENCES/README.md'})
previous=json.loads(read('PROVENANCE/WORKSHOP/GREEN_DAY217_V7/SOURCE_MAP.json'))['members']
check('all 33 non-handoff inherited v7 members identical',all(members[n]['sha256']==v['sha256'] for n,v in previous.items() if n!='executable.md') and len(previous)==34)
check('ELDRIS image reused from existing original',members['REFERENCES/ELDRIS_RECURSIVE_SOURCE_USER.PNG']['repository_path']=='PROVENANCE/WORKSHOP/BOOK_RED_2026_11_07/SOURCES/LM_010/REFERENCES/USER_SUPPLIED_REFERENCE_02.png')

patterns=0;semester_count=0;nested_members=0;inner_hashes=0;classes={};required={}
for student,upper in [('Kaira','KAIRA'),('illi','ILLI'),('Elaira','ELAIRA')]:
    with zipfile.ZipFile(io.BytesIO(read(members['SOURCES/EDUCATION/'+student+'.zip']['repository_path']))) as z:
        check(student+' ZIP CRC',z.testzip() is None);inner={n:z.read(n) for n in z.namelist()}
    nested_members+=len(inner);manifest=json.loads(inner['MANIFEST.json'])['files'];inner_hashes+=len(manifest)
    check(student+' nested declared hashes',all(sha(inner[n])==h for n,h in manifest.items()))
    extra=set(inner)-set(manifest)-{'MANIFEST.json'}
    check(student+' nested member accounting',extra==({'EDU_RECONCILIATION_2026-11-12.md'} if student=='illi' else set()))
    if extra:check('inner reconciliation note equals outer verified note',inner[next(iter(extra))]==read(members['EDU_RECONCILIATION_v7.md']['repository_path']))
    canonical=read(E+'/'+upper+'_PRIMARY.md')
    for n,b in inner.items():
        if 'COURSE_MAP' in n or re.search(r'SEMESTER_0[1-5]\.md$',n):
            start=('<!-- BEGIN ORIGINAL '+n+' -->\n').encode();end=('\n<!-- END ORIGINAL '+n+' -->').encode()
            check(student+'/'+n+' complete unchanged canonical body',canonical.count(start)==1 and canonical.split(start,1)[1].split(end,1)[0]==b)
        if not re.search(r'SEMESTER_0[1-5]\.md$',n):continue
        sem=int(re.search(r'_0([1-5])',n).group(1));semester_count+=1;days={};day=None;req=[]
        for line in b.decode('utf-8').splitlines():
            h=re.match(r'^#{2,3} Day ([1-6])\b',line)
            if h:day=int(h.group(1));days[day]=[]
            if not line.startswith('|') or day is None:continue
            cells=[v.strip().replace('**','') for v in line.strip('|').split('|')];t=re.fullmatch(r'(\d\d?):00[–—-](\d\d?):00',cells[0])
            if not t:continue
            a,b=map(int,t.groups());days[day].append((a,b));activity=cells[1];detail=' '.join(cells[2:])
            if re.search(r'REQUIRED|COMPULSORY',activity) or (re.search(r'^Required',detail,re.I) and not re.search(r'optional',activity,re.I)):
                title=re.sub(r'REQUIRED|COMPULSORY','',activity).strip(' —–:-');req.append((day,a,b,title));classes.setdefault((sem,title),[]).append((student,day,a,b))
        check(student+'/'+n+' six continuous 31-hour days',set(days)==set(range(1,7)) and all(v[0][0]==0 and v[-1][1]==31 and all(a[1]==b[0] for a,b in zip(v,v[1:])) for v in days.values()))
        check(student+'/'+n+' required class count / protected rest',len(req)==(4 if student=='Kaira' and sem==2 else 3) and all(row[0]!=6 for row in req))
        required[(student,sem)]=req;patterns+=len(days)
check('all 15 semesters / 90 patterns / 24 source members / 20 hashes',(semester_count,patterns,nested_members,inner_hashes)==(15,90,24,20))
check('shared required sections consistent',all(len({tuple(v[1:]) for v in values})==1 for values in classes.values()))
check('EDU-01 remains resolved',classes[(3,'Quantum Field Theory I')]==[('Kaira',3,11,13),('illi',3,11,13)])
check('EDU-02 remains resolved',(5,11,13,'Chemistry I') in required[('Elaira',3)] and (3,17,19,'Differential Geometry II') in required[('Elaira',3)] and all(not(d==3 and a<20 and b>19) for student in ['Kaira','illi','Elaira'] for d,a,b,_ in required[(student,3)]))
syfile=E+'/GENESIS_TRANSDUCTION_PROPOSED_SYLLABUS.md';sy=read(members['CURRICULUM/BLACKSTONE_GENESIS_TRANSDUCTION_FIVE_SEMESTERS_v1.md']['repository_path'])
check('complete unshortened 9366-byte proposed syllabus',len(sy)==9366 and read(syfile).split(b'<!-- BEGIN SUPPLIED V8 SYLLABUS -->\n',1)[1].split(b'\n<!-- END SUPPLIED V8 SYLLABUS -->',1)[0]==sy and '**PROPOSED teaching sequence' in text(syfile))
sytext=sy.decode('utf-8');syentries=re.findall(r'^\*\*([^*]+)\*\* \(([^)]+)\):',sytext,re.M)
check('16 proposed Genesis course entries match existing required titles',len(syentries)==16 and all(any(title==name for _,title in classes) for name,_ in syentries))
check('no new compulsory course/schedule inferred','Ordinary anatomy, biology, chemistry' in sytext and 'No student required hours, dates, sections, or course names are changed.' in sytext)

ledger='CONTINUITY/RED_RUNNING_DAY_LEDGER.md';rows=re.findall(r'^\| (\d+) \| ([A-Za-z]+) \| (\d+) \| ([^|]+) \| ([A-Za-z]+) \| (.*?) \|$',text(ledger),re.M)
check('225 original dated rows 0–224',[int(x[0]) for x in rows]==list(range(225)))
months=[('Aelor',33),('Aerith',32),('Aelora',31),('Aevrin',33),('Aelis',31),('Aevor',32),('Aelith',33),('Aerion',32),('Aeveth',31),('Aesith',33),('Aeleth',32)];week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
def date(day):
    n=70+day
    for m,l in months:
        if n<=l:return m,n,week[(day+4)%6]
        n-=l
check('dates and weekdays unchanged under 353-day calendar',sum(x[1] for x in months)==353 and all((m,int(d),wd)==date(int(day)) for day,m,d,_,wd,_ in rows))
check('current ledger end-of-217 boundary and future-only 224','END OF DAY 217' in head(ledger) and '**Day 166' in head(ledger) and '**Day 167' in head(ledger) and '**Day 217' in head(ledger) and 'future first-day planning only' in head(ledger))
arc=head('BOOKS/RED/ARCS/ARC_004/ARC.md')
check('selected complete continuation and narrative limits',all(x in arc for x in ['Grand Archives','bookstore','dimensional storage bracelet','telepathically','approximately one month','Days 218–223','NOT completed Day 217','09:00','11:00–13:00','illi — Kaira — Elaira']))
check('unresolved future routine/Convocation explicitly retained',all(term in head('PROVENANCE/OPEN_QUESTIONS_CURRENT.md') for term in ['reconciliation','09:00','Convocation','OPEN']))
up=json.loads(read(C+'/UPSTREAM_VERIFICATION.json'))
check('pinned upstream verification inventory',up['bricked']['commit']=='c89676fc26000ae6f5fdad66a56e118b285d9b1d' and up['aera']['commit']=='42437950ad2aa72ad885ff1a9129226da23d9286' and len(up['bricked']['files_read'])==21 and len(up['aera']['files_read'])==9)
check('book and biological mechanisms remain OPEN',up['individual_books']['status']=='OPEN' and not up['individual_books']['assignments'] and up['biological_mechanism'].startswith('OPEN'))

modified=['.gitattributes','AGENTS.md','BOOKS/RED/ARCS/ARC_003/ARC.md','BOOKS/RED/ARCS/ARC_004/ARC.md','CONTINUITY/RED_RUNNING_DAY_LEDGER.md','CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md','WORLD_CLOCK/L1_FANTASY/PROPHECIES/FRAMEWORK_AND_CORRESPONDENCE.md',I+'/BLACKSTONE.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/REALMS/GREEN_SPRITES.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/BIOLOGY/SEVEN_DENIZENS_VISUAL_POWER.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/KAIRA.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/NYX.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/SIX_BLACK_BONDS.md']+[E+'/'+s+'_PRIMARY.md' for s in ['KAIRA','ILLI','ELAIRA']]
added=[W+'/'+p for p in sorted(new_sources)]+[W+'/SOURCE_MAP.json',W+'/REFERENCES/README.md',syfile,'WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/BLACKSTONE_SPRITE_PROFESSOR.md']+[C+'/'+n for n in ['INTEGRATION_REPORT.md','REVERSE_DIFF.md','UPSTREAM_VERIFICATION.json','UPSTREAM_VERIFICATION.md','VALIDATION.json','validate_checkpoint.py']]
expected=set(added+modified);actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual.add(C+'/VALIDATION.json')
check('only declared integration paths',actual==expected)
for path in modified:
    old=git('show',BASE+':'+path);now=read(path)
    if path.endswith('.md'):check(path+' entire baseline bytes retained',now.endswith(old))
    elif path=='.gitattributes':check('prior attributes retained',now.startswith(old))
    else:
        oldj=json.loads(old);newj=json.loads(now);entry=newj['subsequent_deliveries'].pop();check('source registry append-only',newj==oldj and entry['id']=='MK163_GREEN_DAY217_V8')
check('no deleted files or inbox tracking',not git('diff','--name-only','--diff-filter=D',BASE).strip() and not git('ls-files','_inbox').strip())
protected=('BOOKS/RED/ARCS/ARC_002/','WORLD_CLOCK/L0_','WORLD_CLOCK/L1_FANTASY/PROPHECIES/MANUSCRIPTS/','PROVENANCE/WORKSHOP/GREEN_DAY217_V6/','PROVENANCE/WORKSHOP/GREEN_DAY217_V7/','CHECKPOINTS/GREEN_DAY217_V6/','CHECKPOINTS/GREEN_DAY217_V7/')
check('Orange, prophecy manuscripts, L0 and historical v6/v7 unchanged',not any(p.startswith(protected) for p in actual))
broken=[]
for path in expected:
    if not path.endswith('.md') or (path.startswith(W+'/') and path!=W+'/REFERENCES/README.md'):continue
    t=head(path).split('<!-- BEGIN SUPPLIED V8 SYLLABUS -->',1)[0]
    for dest in re.findall(r'\]\(([^)]+)\)',t):
        dest=dest.split('#',1)[0].strip('<>')
        if not dest or '://' in dest:continue
        target=(R/path).parent.joinpath(dest).resolve()
        if not target.exists() and target!=R/C/'VALIDATION.json':broken.append([path,dest])
check('all new local links resolve '+json.dumps(broken),not broken)
check('whitespace clean',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)
run=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf-8')
check('existing structural validator',run.returncode==0)
out={'status':'PASS_WITH_DOCUMENTED_OPEN_PARAMETERS','baseline':BASE,'source_members':41,'current_outer_hashes':40,'nested_manifest_hashes':inner_hashes,'source_reuses':34,'new_source_members':7,'semesters':semester_count,'daily_patterns':patterns,'required_course_sessions':sum(len(x) for x in required.values()),'syllabus_status':'PROPOSED','syllabus_course_entries':len(syentries),'ledger_rows_unchanged':225,'frontier':'end of Day 217','EDU-01':'RESOLVED','EDU-02':'RESOLVED','added':sorted(added),'modified':sorted(modified),'deleted':[],'counts':{'added':len(added),'modified':len(modified),'deleted':0,'prior_unchanged_files':833-len(modified)},'checks':checks,'repository_validation':json.loads(run.stdout),'open':'Individual Astrius/Vera volumes, Sprite morphology mechanism/date, professor identifiers, future first-day routine and Convocation timing, and other scoped narrative parameters; see integration/source reports.'}
(R/C/'VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:out[k] for k in ['status','current_outer_hashes','nested_manifest_hashes','daily_patterns','required_course_sessions','syllabus_course_entries','ledger_rows_unchanged','counts']},indent=2))
