"""Read-only check of the November 8 Orange integration. Run with the original ZIP from this commit."""
import hashlib, io, json, re, stat, subprocess, sys, urllib.parse, zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath

ROOT = Path(__file__).resolve().parents[2]
SRC = 'PROVENANCE/WORKSHOP/ORANGE_ARC_2026_11_08'
BASE = '2992259ffa0cb44f2c70e9040c35feda91f5858b'
PREFIX = 'MK163_ORANGE_2026_11_08/'
BOUND = '## Earlier record · retained in full'
def need(ok, msg):
    if not ok: raise ValueError(msg)
def git(*args):
    return subprocess.check_output(['git','-c','core.autocrlf=false','-C',str(ROOT),*args])
def sha(b):
    return hashlib.sha256(b).hexdigest()
def read(p):
    return (ROOT/p).read_bytes()
def safe_names(names):
    need(len(names)==len({n.casefold() for n in names}),'Path collision')
    for n in names:
        p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and not PureWindowsPath(n).drive and '\\' not in n and ':' not in n and all(x.casefold() not in ('.','..','.git','_inbox') and x==x.rstrip(' .') and not PureWindowsPath(x).is_reserved() for x in p.parts),'Unsafe path '+n)
def validate(archive):
    catalog=json.loads(read(SRC+'/SOURCE_INDEX.json'))
    need(sha(archive.read_bytes())==catalog['archive_sha256'] and archive.stat().st_size==catalog['archive_bytes'],'Wrong source archive')
    exact=external=0
    with zipfile.ZipFile(archive) as z:
        safe_names(z.namelist());need(all(not i.is_dir() and not i.flag_bits&1 and not stat.S_ISLNK(i.external_attr>>16) and i.file_size<75_000_000 for i in z.infolist()),'ZIP metadata')
        need(z.testzip() is None,'Outer CRC')
        m=json.loads(z.read(PREFIX+'MANIFEST.json'))
        need(m['current_repository_baseline_commit']==BASE and m['target_repository']=='xApologies/MK163','Baseline/target')
        need(len(m['files'])==37 and set(z.namelist())=={PREFIX+'MANIFEST.json'}|{PREFIX+e['path'] for e in m['files']},'Manifest coverage')
        need(len(catalog['entries'])==38 and set(z.namelist())=={PREFIX+e['path'] for e in catalog['entries']},'Installed coverage')
        for e in m['files']:
            b=z.read(PREFIX+e['path']);need(sha(b)==e['sha256'] and len(b)==e['bytes'],e['path'])
            if e['path'].endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(b)) as inner:
                    safe_names(inner.namelist());need(inner.testzip() is None,'Nested CRC')
                    if 'MINI' in e['path']:
                        im=json.loads(inner.read('MANIFEST.json'))
                        for n,h in im['files'].items():
                            ib=inner.read(n);need(sha(ib)==h['sha256'] and len(ib)==h['bytes'],'Mini manifest')
                        standalone=e['path'][:-4]+'.md';need(inner.read('MINI_CHECKPOINT.md')==z.read(PREFIX+standalone),'Mini version mismatch')
                    else:
                        need(sha(b)==m['previous_cumulative_checkpoint_sha256']==json.loads(read('CHECKPOINTS/BOOK_RED_2026_11_07_VALIDATION.json'))['source_sha256'],'Parent mismatch')
        for e in catalog['entries']:
            n=e['path'];b=z.read(PREFIX+n);need(sha(b)==e['sha256'] and len(b)==e['bytes'],n)
            if e['installed_path']:
                safe_names([e['installed_path']]);need(read(e['installed_path'])==b,'Source copy '+n);exact+=1
            else: external+=1;need(n.endswith(('.zip','.pdf','.png')) and e['disposition'],'Unaccounted omission: '+n)
    # Restore five casing-only edits from the recorded original lines; all other expanded text must contain the full baseline verbatim.
    edits=json.loads(read(SRC+'/CASING_EDITS.json'))
    unchanged=modified=history=0;changed=set();beforepaths=set()
    for line in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,raw=line.split(b'\t',1);p=raw.decode();beforepaths.add(p);b=read(p)
        same=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()==meta.split()[-1]
        if same: unchanged+=1
        else:
            changed.add(p);modified+=1;before=git('cat-file','blob',meta.split()[-1].decode())
            if p in edits:
                lines=b.decode().splitlines(keepends=True)
                for e in edits[p]:
                    need(e['after']==re.sub(r'(?<![A-Za-z_])Raeon(?![A-Za-z_])','raeon',e['before']) and lines[e['line']-1]==e['after'],'Casing edit mismatch')
                    lines[e['line']-1]=e['before']
                need(''.join(lines).encode()==before,'Other change in casing-only file')
            elif p=='PROVENANCE/SOURCE_REGISTRY.json':
                a,c=json.loads(before),json.loads(b);need(c['subsequent_deliveries'][-1]['id']==PREFIX[:-1],'Delivery ID');c['subsequent_deliveries'].pop();need(a==c,'Previous registry lost')
            else:need(b.startswith(before) or b.endswith(before),'Prior content removed: '+p)
        if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')):need(same,'Historical bytes changed: '+p);history+=1
    checks=json.loads(read('CHECKPOINTS/ORANGE_2026_11_08_CHECKS.json'))['rows']
    need(len(checks)==10,'Topics')
    for i,row in enumerate(checks,1):
        text=read(row['owner']).decode().split(BOUND)[0]
        need(row['id']==f'OR-{i:02}' and row['before'] and row['after'] and row['source_sections'],'Topic disposition')
        for term in row['required']:need(term.replace('*','').casefold() in text.replace('*','').casefold(),row['id']+' '+term)
        for sec in row['source_sections']:
            if sec not in ('Event ownership and no-loss guards','Source and naming corrections'):
                need('## '+sec in text or '## '+sec.replace('Raeon','raeon') in text,'Missing topic section: '+sec)
    ev=read(SRC+'/PROVENANCE/13_AUTHOR_EVIDENCE_SELECTED_VERBATIM.md').decode()
    ids=set(re.findall(r'^## \[(A08-\d+)\]',ev,re.M));need(len(ids)==21 and ids=={v for r in checks for v in r['evidence']},'Quote coverage')
    paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1]);safe_names(list(paths))
    additions=paths-beforepaths;need(not any(p.endswith(('.zip','.pdf','.png')) for p in additions),'Unapproved attachment added')
    for p in additions|changed:
        need(not re.search(r'(^|/)_inbox(/|$)',p,re.I),'Tracked inbox')
        b=read(p);need(len(b)<100_000_000,'Oversize '+p)
        if not p.endswith(('.py','.md','.json')):continue
        text=b.decode('utf8')
        if p.endswith(('.md','.json')):
            need(not re.search(r'(?:[A-Za-z]:[/\\](?:Users|Documents and Settings)[/\\]|/Users/[^/]+/|/home/[^/]+/|/mnt/data/)',text,re.I),'Private path: '+p)
        if p.startswith(SRC+'/') or not p.endswith('.md'):continue
        cur=text.split(BOUND)[0]
        if p in edits:cur=cur.split('Source and decisions:')[0].split('Evidence:')[0]
        if p.startswith(('BOOKS/','WORLD_CLOCK/','CONSTITUTIONS/')) or p=='AGENTS.md':
            need(not re.search(r'\b(?:Raeon|RAEON|Kira|Rayon|Aethrin|Valum)\b',cur),'Current spelling: '+p)
        for t in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)',cur):
            if t.startswith(('http://','https://','#')):continue
            need((ROOT/p).parent.joinpath(urllib.parse.unquote(t.split('#')[0])).exists(),'Broken link: '+p+' '+t)
    prev=json.loads(read('CHECKPOINTS/BOOK_RED_2026_11_07_VALIDATION.json'));need(prev['status']=='PASS','Prior report')
    sc='WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md'
    nums=[int(x) for x in re.findall(r'^\| \d+ \| [^|\n]+ \| (\d+) \| [^|\n]+ \|$',read(sc).decode(),re.M)]
    need(nums==[5,5,5,4,5,4,4,4,3,4,4,3,4] and sum(nums)==54 and sum(nums)//13==4,'Support scores')
    for p in [sc,'WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/TOURNAMENT_AND_RING_ACQUISITION.md','BOOKS/RED/ARCS/ARC_007/ARC.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md',*['WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/ACCORD_REGISTRY/'+r+'.md' for r in ['GUARDIAN','OFFENSIVE','HELKIR','SUPPORT']]]:
        need(read(p)==git('show',BASE+':'+p),'Protected owner changed: '+p)
    git('check-ignore','-q','_inbox/check.zip');git('diff','--check',BASE);git('diff','--cached','--check')
    return dict(status='PASS',baseline=BASE,archive_sha256=catalog['archive_sha256'],archive_bytes=catalog['archive_bytes'],manifest_entries=37,mapped_members=38,installed_exact=exact,external_hashed=external,topics=10,evidence_groups=21,previous_files=len(beforepaths),byte_identical=unchanged,non_destructively_updated=modified,prior_checkpoint_and_workshop_byte_identical=history,added=len(additions),deleted=0,unchanged_support_score='54/91 Green',unchanged_tournament='Green/fourth, Ring at end of Red',literal_transcript_complete=False)
if __name__=='__main__':
    print(json.dumps(validate(Path(sys.argv[1])),indent=2))
