"""Revalidate the supplied Green checkpoint, preservation and declared OPEN boundaries."""
from pathlib import Path
import argparse,hashlib,io,json,os,re,shutil,subprocess,zipfile

parser=argparse.ArgumentParser();parser.add_argument('--root',default='.');args=parser.parse_args()
R=Path(args.root).resolve();G=os.environ.get('MK163_GIT') or shutil.which('git')
if not G:raise SystemExit('Git executable required (PATH or MK163_GIT).')
W='PROVENANCE/WORKSHOP/GREEN_DAY217_V6';C='CHECKPOINTS/GREEN_DAY217_V6';I='WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS'
BASE='211b4222346bd9aff6511d9d9c97df4a73e4680f';checks=[]
def git(*a):return subprocess.check_output([G,'-C',str(R),*a])
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return (R/path).read_bytes()
def text(path):return read(path).decode('utf-8')
def check(name,condition):
    checks.append({'check':name,'pass':bool(condition)})
    if not condition:raise AssertionError(name)
source=json.loads(read(W+'/SOURCE_MAP.json'))
manifest=json.loads(read(W+'/MANIFEST.json'))['files']
check('31 declared outer hashes and sizes',len(manifest)==31 and all(sha(read(W+'/'+n))==e['sha256'] and len(read(W+'/'+n))==e['size_bytes'] for n,e in manifest.items()))
check('all 32 supplied source files unchanged',len(source['members'])==32 and all(sha(read(e['repository_path']))==e['sha256'] for e in source['members'].values()))
check('source directory contains no extra extracted duplicate tree', {p.relative_to(R/W).as_posix() for p in (R/W).rglob('*') if p.is_file()}==set(source['members'])|{'SOURCE_MAP.json'})
patterns=0;semester_count=0;nested_hashes=0;nested_members=0;classes={};qft=[]
for student,upper in [('Kaira','KAIRA'),('illi','ILLI'),('Elaira','ELAIRA')]:
    path=I+'/BLACKSTONE_EDUCATION/'+upper+'_PRIMARY.md';canonical=read(path)
    with zipfile.ZipFile(io.BytesIO(read(W+'/SOURCES/EDUCATION/'+student+'.zip'))) as z:
        check(student+' ZIP integrity',z.testzip() is None)
        entries={n:z.read(n) for n in z.namelist()};nested_members+=len(entries)
    inner=json.loads(entries['MANIFEST.json'])['files'];nested_hashes+=len(inner)
    check(student+' nested manifest coverage and hashes',set(inner)==set(entries)-{'MANIFEST.json'} and all(sha(entries[n])==h for n,h in inner.items()))
    for name,data in entries.items():
        if 'COURSE_MAP' in name or re.search('SEMESTER_0[1-5]\\.md$',name):
            start=('<!-- BEGIN ORIGINAL '+name+' -->\n').encode();end=('\n<!-- END ORIGINAL '+name+' -->').encode()
            check(student+'/'+name+' complete original body',canonical.count(start)==1 and canonical.split(start,1)[1].split(end,1)[0]==data)
        if not re.search('SEMESTER_0[1-5]\\.md$',name):continue
        semester_count+=1;sem=int(re.search(r'_0([1-5])',name).group(1));days={};day=None;required=[]
        for line in data.decode('utf-8').splitlines():
            h=re.match(r'^#{2,3} Day ([1-6])\b',line)
            if h:day=int(h.group(1));days[day]=[]
            if not line.startswith('|') or day is None:continue
            cells=[v.strip().replace('**','') for v in line.strip('|').split('|')]
            t=re.fullmatch(r'(\d\d?):00[–—-](\d\d?):00',cells[0])
            if not t:continue
            a,b=map(int,t.groups());days[day].append((a,b));activity=cells[1];detail=' '.join(cells[2:])
            if re.search(r'REQUIRED|COMPULSORY',activity) or (re.search(r'^Required',detail,re.I) and not re.search(r'optional',activity,re.I)):
                title=re.sub(r'REQUIRED|COMPULSORY','',activity).strip(' —–:-');required.append((day,a,b,title))
                classes.setdefault((sem,title),[]).append((student,day,a,b))
        check(student+'/'+name+' six continuous 31-hour patterns',set(days)==set(range(1,7)) and all(v[0][0]==0 and v[-1][1]==31 and all(a[1]==b[0] for a,b in zip(v,v[1:])) for v in days.values()))
        check(student+'/'+name+' protected rest day',all(row[0]!=6 for row in required))
        check(student+'/'+name+' required course count',len(required)==(4 if student=='Kaira' and sem==2 else 3))
        patterns+=len(days)
check('15 semesters, 90 daily patterns, 23 nested members and 20 declared inner hashes',(semester_count,patterns,nested_members,nested_hashes)==(15,90,23,20))
conflicts={f'{sem}:{title}':v for (sem,title),v in classes.items() if len({tuple(x[1:]) for x in v})>1}
check('only known required same-semester class timing mismatch',list(conflicts)==['3:Quantum Field Theory I'])
check('EDU-01 author decision recorded without retiming','Preserve both schedules and explicitly mark the shared-class timing OPEN' in text(C+'/REVERSE_DIFF.md') and conflicts['3:Quantum Field Theory I']==[('Kaira',3,11,13),('illi',3,13,15)])

ledger='CONTINUITY/RED_RUNNING_DAY_LEDGER.md';raw=read(ledger)
rows=[]
for line in raw.decode('utf-8').splitlines():
    m=re.match(r'^\| (\d+) \| ([A-Za-z]+) \| (\d+) \| ([^|]+) \| ([A-Za-z]+) \| (.*?) \|$',line)
    if m:rows.append(m.groups())
check('single 225-row dated ledger 0 through 224',[int(x[0]) for x in rows]==list(range(225)))
months=[('Aelor',33),('Aerith',32),('Aelora',31),('Aevrin',33),('Aelis',31),('Aevor',32),('Aelith',33),('Aerion',32),('Aeveth',31),('Aesith',33),('Aeleth',32)]
week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
def date(day):
    ordinal=70+day
    for month,length in months:
        if ordinal<=length:return month,ordinal,week[(day+4)%6]
        ordinal-=length
    raise ValueError(day)
check('225 dates/weekday labels match unchanged 353-day calendar',sum(n for _,n in months)==353 and all((m,int(d),wd)==date(int(day)) for day,m,d,_,wd,_ in rows))
check('frontier and future labels', 'move-in ONLY' in rows[217][-1] and all('FUTURE / UNSCHEDULED' in rows[d][-1] for d in range(218,224)) and 'FUTURE ANCHOR' in rows[224][-1])
baseline_ledger=git('show',BASE+':'+ledger)
retained=raw.split(b'## Prior framing and extended single daily table\n\n',1)[1]
retained=b''.join(l for l in retained.splitlines(keepends=True) if not re.match(rb'^\| (21[2-9]|22[0-4]) \|',l))
check('all earlier ledger bytes and intervals preserved',retained==baseline_ledger)
check('semester anchors 224/241/244',date(217)==('Aeveth',30,'Aiven') and date(224)==('Aesith',6,'Ailar') and date(241)==('Aesith',23,'Aiven') and date(244)==('Aesith',26,'Aiveth'))

modified=['.gitattributes','AGENTS.md','BOOKS/RED/ARCS/ARC_004/ARC.md','CONSTITUTIONS/07_NAMING_CONVENTIONS.md',ledger,'CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md','PROVENANCE/OPEN_QUESTIONS_CURRENT.md','PROVENANCE/SOURCES.md','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/CURRENT_MODEL_INDEX.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/INFRASTRUCTURE/ROADS_WILDS_AND_SECURITY.md',I+'/BLACKSTONE.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/KAIRA.md']
added=[W+'/'+n for n in source['members']]+[W+'/SOURCE_MAP.json',I+'/BLACKSTONE_SEMESTER_I_CALENDAR.md']+[I+'/BLACKSTONE_EDUCATION/'+n+'_PRIMARY.md' for n in ['KAIRA','ILLI','ELAIRA']]+[C+'/'+n for n in ['INTEGRATION_REPORT.md','REVERSE_DIFF.md','OMISSIONS_AND_OPEN_ISSUES.md','validate_checkpoint.py','VALIDATION.json']]
expected=set(modified+added)
actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
actual.add(C+'/VALIDATION.json')
check('only declared added/modified files',actual==expected)
for path in modified:
    old=git('show',BASE+':'+path);now=read(path)
    if path.endswith('.md') and path!=ledger:check(path+' previous body retained',now.endswith(old))
    if path=='.gitattributes':check('prior attributes preserved',now.startswith(old))
    if path=='PROVENANCE/SOURCE_REGISTRY.json':
        prev=json.loads(old);new=json.loads(now);delivery=new['subsequent_deliveries'].pop()
        check('registry previous entries unchanged',prev==new and delivery['id']=='MK163_GREEN_DAY217_V6')
check('no baseline files deleted',not git('diff','--name-only','--diff-filter=D',BASE).strip())
check('no inbox or inherited or completed arc changes',not any(p.startswith(('_inbox/','BOOKS/RED/ARCS/ARC_002/','BOOKS/RED/ARCS/ARC_003/','WORLD_CLOCK/L0_')) for p in actual))
check('no inbox tracked',not git('ls-files','_inbox').strip())
check('whitespace clean',subprocess.run([G,'-C',str(R),'diff','--check',BASE],capture_output=True).returncode==0)

# Check new integration links only; quoted historical member bodies are not rewritten.
broken=[]
for path in sorted(expected):
    if not path.endswith('.md') or path.startswith(W+'/'):continue
    content=text(path).split('## Earlier record · preserved verbatim',1)[0].split('## Preserved member:',1)[0].split('## Complete recovered source text',1)[0]
    for dest in re.findall(r'\]\(([^)]+)\)',content):
        dest=dest.split('#',1)[0].strip('<>')
        if not dest or '://' in dest:continue
        target=(R/path).parent.joinpath(dest).resolve()
        if not target.exists() and target != R/C/'VALIDATION.json':broken.append([path,dest])
check('new local Markdown links resolve: '+json.dumps(broken),not broken)

validator=subprocess.run([os.sys.executable,'-B','-X','utf8',str(R/'CHECKPOINTS/TOOLS/validate_live_model.py'),'--root',str(R),'--manifest',str(R/'CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json'),'--structural-only'],capture_output=True,text=True,encoding='utf-8')
check('existing repository structural validator',validator.returncode==0)
structural=json.loads(validator.stdout)
result={'status':'PASS_WITH_AUTHOR_ACCEPTED_OPEN','baseline':BASE,'source_outer_files':32,'outer_manifest_hashes':31,'nested_members':nested_members,'nested_manifest_hashes':nested_hashes,'semesters':semester_count,'daily_patterns':patterns,'required_course_sessions':sum(len(v) for v in classes.values()),'daily_ledger_rows':len(rows),'added':sorted(added),'modified':sorted(modified),'deleted':[],'counts':{'added':len(added),'modified':len(modified),'deleted':0,'baseline_files_unchanged':783-len(modified)},'accepted_open':{'EDU-01':conflicts},'checks':checks,'repository_structural_validation':structural,'limitations':'Mechanical integrity is not a claim of literal transcript completeness or future scene attendance; see omissions report.'}
(R/C/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:result[k] for k in ['status','counts','source_outer_files','outer_manifest_hashes','nested_manifest_hashes','semesters','daily_patterns','required_course_sessions','daily_ledger_rows']},indent=2))
