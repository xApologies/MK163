"""Read-only, portable White 006 preservation and continuity audit (stdlib only)."""
import argparse,csv,hashlib,io,json,re,subprocess,zipfile
from pathlib import Path

BASE='164ce15c5fa5709472c551b38613ac68fc4ecb6b'
P='PROVENANCE/WORKSHOP/WHITE_006'
A='BOOKS/RED/ARCS/ARC_007'
D='WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/D07_DUNGEON_ATLAS'
MONTHS=list(zip('Aelor Aerith Aelora Aevrin Aelis Aevor Aelith Aerion Aeveth Aesith Aeleth'.split(),[33,32,31,33,31,32,33,32,31,33,32]))
WEEK='Ailar Aiden Aiveth Ailor Aithen Aiven'.split()

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--git',default='git');p.add_argument('--report',type=Path);a=p.parse_args();root=a.root.resolve()
    checks=[]
    def ck(v,label):checks.append({'check':label,'pass':bool(v)})
    def data(path):return (root/path).read_bytes()
    def txt(path):return (root/path).read_text(encoding='utf-8')
    def sha(b):return hashlib.sha256(b).hexdigest()
    def git(*args):return subprocess.check_output([a.git,*args],cwd=root)
    baseline_oids={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',BASE).decode().splitlines()}
    def previous(path):return git('show',BASE+':'+path)
    def same_blob(path,payload):return hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()==baseline_oids[path]
    def date(day):
        n=(day+69)%353
        for m,l in MONTHS:
            if n<l:return m,n+1
            n-=l
    def zipmanifest(z,prefix):
        m=json.loads(z.read(prefix+'MANIFEST.json'));es=m.get('files',m.get('entries'))
        if isinstance(es,list):es={e['path']:e for e in es}
        names={n for n in z.namelist() if not n.endswith('/')};ck(z.testzip() is None,prefix+' CRC')
        ck(names=={prefix+'MANIFEST.json'}|{prefix+n for n in es},prefix+' complete manifest coverage')
        for n,e in es.items():ck(sha(z.read(prefix+n))==e['sha256'] and len(z.read(prefix+n))==e.get('bytes',e.get('size_bytes')),prefix+n+' original hash and size')
        return len(es)
    manifest=json.loads(txt(P+'/DELIVERY/MANIFEST.json'))
    for name,e in manifest['files'].items():ck(sha(data(P+'/DELIVERY/'+name))==e['sha256'] and len(data(P+'/DELIVERY/'+name))==e['bytes'],'outer source '+name)
    z=zipfile.ZipFile(root/P/'DELIVERY/REFERENCES/MK163_WHITE_ARC_005_CUMULATIVE_CODEX_HANDOFF.zip');zipmanifest(z,'MK163_WHITE_ARC_005_CUMULATIVE/')
    dz=zipfile.ZipFile(io.BytesIO(z.read('MK163_WHITE_ARC_005_CUMULATIVE/REFERENCES/V01(3).zip')));zipmanifest(dz,'MK163_D07_ATLAS_001/')
    mz=zipfile.ZipFile(io.BytesIO(dz.read('MK163_D07_ATLAS_001/provenance/source_method.zip')));zipmanifest(mz,'MK163_Dungeon_Mapping_Method_001_2026-11-17/')
    for e in json.loads(txt(P+'/SOURCE_MAP.json'))['records']:ck(sha(data(e['target']))==e['sha256'],'exact source map '+e['target'])
    # Every overwritten prior owner has a lossless snapshot.
    for f in (root/P/'PRE_WHITE_006').rglob('*'):
        if f.is_file():
            name=f.relative_to(root/P/'PRE_WHITE_006').as_posix();ck(f.read_bytes()==previous(name),'baseline snapshot '+name)
    baseline_names=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
    violet=[n for n in baseline_names if n.startswith('BOOKS/RED/ARCS/ARC_006/')]
    ck(len(violet)==23,'23 authoritative Violet files')
    for n in violet:ck(same_blob(n,data(n)),'Violet byte preservation '+n)
    historical=[n for n in baseline_names if n.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/'))]
    for n in historical:ck(same_blob(n,data(n)),'historical byte preservation '+n)
    for n in baseline_names:
        if n.startswith(('BOOKS/RED/ARCS/ARC_001/','BOOKS/RED/ARCS/ARC_002/','BOOKS/RED/ARCS/ARC_003/','BOOKS/RED/ARCS/ARC_004/')):ck(same_blob(n,data(n)),'earlier arc preservation '+n)
    for n in baseline_names:
        if n.startswith('WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON_ATLAS/'):ck(same_blob(n,data(n)),'B03 atlas preservation '+n)
    blue='BOOKS/RED/ARCS/ARC_005/ARC.md';expected=previous(blue).decode().replace('Green Hollowmere Dungeon in the Blue Domain.','Green Hollowmere Dungeon in **Green Domain G3** (author correction during White 006; local geometry and all Blue Arc dates unchanged).')
    ck(txt(blue)==expected,'Blue Arc only author-approved territorial correction')
    r=list(csv.DictReader(io.StringIO(txt(A+'/WHITE_DAILY_LEDGER.csv'))));ck([int(x['story_day']) for x in r]==list(range(1346,1638)),'292 consecutive White rows')
    md=txt(A+'/WHITE_DAILY_LEDGER.md')
    for x in r:
        day=int(x['story_day']);ck((x['month'],int(x['day_of_month']))==date(day),'White civil date '+str(day));ck(x['weekday']==WEEK[(day+4)%6] and int(x['weekday_number'])==(day+4)%6+1,'White weekday '+str(day))
        line=f"| {day} | {x['month']} {x['day_of_month']} | {x['weekday']} | {x['weekday_number']} | {x['event']} | {x['status']} |"
        ck(md.count(line)==1,'White Markdown/CSV exact event and status '+str(day))
    def daily(s):return {int(m[0]):m for m in re.findall(r'^\| (\d+) \| (A\w+) \| (\d+) \| ([^|]+) \| (A\w+) \| (.*) \|$',s,re.M)}
    ledger=txt('CONTINUITY/RED_RUNNING_DAY_LEDGER.md');new=daily(ledger);prior=daily(previous('CONTINUITY/RED_RUNNING_DAY_LEDGER.md').decode())
    ck(list(new)==list(range(1638)),'1,638 consecutive running days 0–1637');ck(len(prior)==1347,'1,347 prior running days')
    for day,record in prior.items():ck(new.get(day)==record,'prior daily row exact preservation '+str(day))
    for x in r[1:]:
        day=int(x['story_day']);row=new[day];ck((row[1],int(row[2]))==date(day) and row[4]==WEEK[(day+4)%6],'new running coordinate '+str(day));ck(x['event'] in row[5] and x['status'] in row[5],'new running event/status '+str(day))
    # All detailed 005 selections are retained, subject to documented threshold/ordinal/OPEN changes.
    oldrows={int(x['story_day']):x for x in csv.DictReader(io.StringIO(txt(P+'/INHERITED_005/LEDGER/WHITE_ARC_DAILY_LEDGER_1346_1484.csv')))}
    for x in r:
        day=int(x['story_day'])
        if 1347<=day<1484:
            event=oldrows[day]['event'].replace('Selected Route B to Blue checkpoint B009','Selected Route B to the G054–B009 Blue boundary, not B009 itself').replace('Route B descent toward B009','Route B descent toward the Blue boundary on G054–B009').replace('arrive B009; activate Blue-depth marker','cross the G054–B009 Blue boundary; activate Blue-depth marker').replace('Orange (2nd)','Orange (sixth under the current placement ladder)')
            if day==1431:event=event.replace('B2 route and activation passage OPEN.','Route A selected; activation at the 9.2-mile Blue boundary on G039–B022.')
            ck(event in x['event'],'full 005 daily detail retained '+str(day));ck(oldrows[day]['status'] in x['status'],'005 status retained '+str(day))
    def sec(v,point=False):
        if point:
            day,time=v.split();h,m,*s=map(int,time.split(':'));return int(day)*111600+h*3600+m*60+(s[0] if s else 0)
        d,h,m,s=map(int,v.split(':'));return d*111600+h*3600+m*60+s
    clocks=[]
    for line in txt(A+'/RACE_CHRONOMETERS_AND_STANDINGS.md').splitlines():
        cols=[x.strip() for x in line.strip('|').split('|')]
        if len(cols)==7 and re.match(r'\d{4} ',cols[1]):clocks.append(cols)
    ck(len(clocks)==9,'nine race clock records')
    for cols,start in zip(clocks,[1376,1400,1430,1460,1490,1520,1550,1580,1616]):
        name,dep,act,finish,master,elapsed,result=cols
        ck(sec(finish,True)-sec(dep,True)==sec(elapsed),name+' independent elapsed arithmetic')
        ck(sec(finish,True)-(start*111600+36000)==sec(master),name+' independent master arithmetic')
        ck(sec(dep,True)<sec(act,True)<sec(finish,True),name+' activation order')
        ck((start+4)%6==0,name+' Red opening Ailar')
    ck('**14**' in txt(A+'/RACE_CHRONOMETERS_AND_STANDINGS.md') and 4+2+1+3+4==14,'circuit points total 14')
    ck(all('PROVISIONAL' in x['status'] for x in r if 1520<=int(x['story_day'])<=1536),'Green V2 dependent clock status retained')
    routes=list((root/A/'ROUTES').glob('*.md'));candidate_count=0
    for pth in routes:
        if pth.name=='README.md':continue
        t=pth.read_text(encoding='utf-8');labels=re.findall(r'^## Route ([A-E]) ',t,re.M);ck(labels==list('ABCDE'),pth.name+' complete candidates');ck(len(re.findall(r'\(SELECTED\)',t))==1,pth.name+' one selected route');candidate_count+=len(labels)
    ck(candidate_count==40,'40 candidate records across eight dungeon route registers')
    for e in json.loads(txt('CHECKPOINTS/WHITE_006/ROUTE_VALIDATION.json'))['routes']:
        ck(e['connected'],'route graph connectivity '+e['dungeon']+' '+e['route'])
    ck('Green Domain G3' in txt('WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/WORLD_MAP_REFERENCE.md'),'author-confirmed Village Hub domain')
    ck('omit the conflicting lifetime count' in txt(P+'/AUTHOR_DECISIONS.md'),'author-confirmed Day 1369 count omission')
    ck(not any(n.startswith('_inbox/') for n in git('ls-files').decode().splitlines()),'inbox excluded from index')
    # Inspect changed/new Markdown links, excluding immutable snapshots and verbatim historical atlas docs.
    active_paths=json.loads(txt('CHECKPOINTS/WHITE_006/EXPECTED_CHANGES.json'))
    for path in active_paths:
        if not path.endswith('.md') or path.startswith(P+'/') or path.startswith(D+'/'):continue
        text=txt(path)
        # Only added lines are audited in old owners, to avoid reporting pre-existing legacy links.
        if path in baseline_names:
            oldlines=set(previous(path).decode().splitlines());text='\n'.join(l for l in text.splitlines() if l not in oldlines)
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=target.split('#')[0].replace('%20',' ')
            if not target:continue
            ck((root/path).parent.joinpath(target).exists(),'new link '+path+' -> '+target)
    actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    ck(actual==set(active_paths),'exact reviewed changes; no unrelated files')
    result={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','baseline':BASE,'check_count':len(checks),'failure_count':sum(not x['pass'] for x in checks),'failures':[x['check'] for x in checks if not x['pass']],'counts':{'violet_files_preserved':len(violet),'white_rows':len(r),'running_rows':len(new),'race_clocks':len(clocks),'route_candidates':candidate_count},'coverage':'Supplied payload and checked-out scope preserved; external source dependencies remain explicitly PARTIAL — WORKSHOP.'}
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return result['status']!='PASS'

if __name__=='__main__':raise SystemExit(main())
