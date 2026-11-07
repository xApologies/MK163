"""Validate the 2026-11-07 delivery at its integration commit. Read-only; run in the MK163 checkout."""
import hashlib, io, json, re, stat, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f2be3e917321c0fe0efbb6e37f30c0948e7f84fa'
SRC = 'PROVENANCE/WORKSHOP/BOOK_RED_2026_11_07'
SHA = lambda b: hashlib.sha256(b).hexdigest()
def need(ok, why):
    if not ok: raise ValueError(why)
def git(*args):
    return subprocess.check_output(['git','-c','core.autocrlf=false','-C',str(ROOT),*args])
def read(p):
    return (ROOT/p).read_bytes()
def check_names(names):
    need(len(names)==len({n.casefold() for n in names}), 'Case/path collision')
    for n in names:
        p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and not PureWindowsPath(n).drive and ':' not in n and '\\' not in n
             and all(v not in ('.','..') and v.casefold() not in ('.git','_inbox') and v.rstrip(' .')==v
                     and not PureWindowsPath(v).is_reserved() for v in p.parts), 'Unsafe path: '+n)
def inspect(z):
    entries=z.infolist(); check_names([i.filename.rstrip('/') for i in entries])
    need(len(entries)<10000 and sum(i.file_size for i in entries)<300_000_000,'Oversize archive')
    need(all(not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1 and i.file_size<75_000_000 for i in entries),'Unsafe ZIP member')
    need(z.testzip() is None,'ZIP CRC')
def validate(attachment):
    inventory=json.loads(read(SRC+'/SOURCE_INVENTORY.json'))
    need(SHA(attachment.read_bytes())==inventory['archive_sha256'],'Wrong source ZIP')
    seen=set(); leaves=set(); declared=0
    def walk(data,depth=0):
        nonlocal declared
        h=SHA(data)
        if h in seen: return
        need(depth<35 and len(seen)<150,'Archive graph limit')
        seen.add(h); arc=inventory['archives'][h]; observed=[]
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            inspect(z)
            for i in z.infolist():
                if i.is_dir(): continue
                b=z.read(i); d=SHA(b)
                observed.append(dict(path=i.filename,sha256=d,bytes=len(b)))
                if i.filename.lower().endswith('.zip'): walk(b,depth+1)
                else:
                    leaves.add(d); dest=inventory['leaves'][d]['installed']
                    check_names([dest]); need(read(dest)==b,dest)
            need(observed==arc['members'],'Incorrect archive/member inventory')
            m=json.loads(z.read(next(i.filename for i in z.infolist() if i.filename.endswith('MANIFEST.json'))))
            for key in ['files','members']:
                v=m.get(key,[])
                for name,e in (v.items() if isinstance(v,dict) else [(x['path'],x) for x in v if isinstance(x,dict)]):
                    if isinstance(e,dict) and 'sha256' in e:
                        need(any((t['path']==name or t['path'].endswith('/'+name)) and t['sha256']==e['sha256'] and t['bytes']==e.get('bytes',e.get('size',t['bytes'])) for t in observed),'Inner manifest: '+name)
                        declared+=1
            for k,v in m.items():
                if k.endswith('sha256'):
                    need(v in {t['sha256'] for t in observed},'Inner manifest hash '+k);declared+=1
    with zipfile.ZipFile(attachment) as z:
        inspect(z); manifest='MK163_PUSH/MANIFEST.json'; m=json.loads(z.read(manifest))
        need(m['repository']=='xApologies/MK163' and m['archive_count']==len(m['archives'])==15,'Wrong target or count')
        rows=m['documents']+m['archives']
        need(len(rows)==26 and set(z.namelist())=={manifest}|{r['path'] for r in rows},'Outer coverage')
        for r in rows:
            b=z.read(r['path'])
            need(len(b)==r['bytes'] and SHA(b)==r['sha256'],r['path'])
            if r['path'].endswith('.zip'): walk(b)
            else: need(read(SRC+'/DELIVERY/'+r['path'].removeprefix('MK163_PUSH/'))==b,r['path'])
        need(read(SRC+'/DELIVERY/MANIFEST.json')==z.read(manifest),'Manifest bytes')
    need(seen==set(inventory['archives']) and leaves==set(inventory['leaves']),'Omitted source content')
    files=git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1];check_names(files)
    unchanged=expanded=history=0;modified=set()
    for line in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,raw=line.split(b'\t',1); p=raw.decode(); b=read(p)
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
        same=oid==meta.split()[-1]
        if same: unchanged+=1
        else:
            before=git('cat-file','blob',meta.split()[-1].decode()); modified.add(p); expanded+=1
            if p=='PROVENANCE/SOURCE_REGISTRY.json':
                a,c=json.loads(before),json.loads(b)
                need(c['subsequent_deliveries'][:-1]==a['subsequent_deliveries'] and {k:v for k,v in a.items() if k!='subsequent_deliveries'}=={k:v for k,v in c.items() if k!='subsequent_deliveries'},'Historical registry')
            else: need(b.endswith(before) or b.startswith(before),'Previous text lost: '+p)
        if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')): need(same,'Prior history changed: '+p);history+=1
    checks=json.loads(read('CHECKPOINTS/BOOK_RED_2026_11_07_CHECKS.json'))
    for row in checks:
        content='\n'.join(read(p).decode().split('Earlier text below is retained verbatim')[0] for p in row['owners'])
        for term in row['required']: need(term.casefold() in content.casefold(),row['id']+' '+term)
    # Recompute the actual thirteen recorded station rows, not the printed total.
    score=read('WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md').decode()
    rows=re.findall(r'^\| (\d+) \| [^|\n]+ \| (\d+) \| [^|\n]+ \|$',score,re.M)
    values=[int(v) for _,v in rows];need([int(n) for n,_ in rows]==list(range(1,14)) and values==[5,5,5,4,5,4,4,4,3,4,4,3,4] and sum(values)==54 and sum(values)//13==4 and round(sum(values)/13,3)==4.154,'Support score')
    for p in ['BOOKS/RED/ARCS/ARC_001/ARC.md','BOOKS/RED/ARCS/ARC_002/ARC.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md']:
        need(read(p)==git('show',BASE+':'+p),'Protected baseline: '+p)
    for i in range(4,8):
        p=f'BOOKS/RED/ARCS/ARC_{i:03}/ARC.md';t=read(p).decode()
        need(all(k in t for k in (f'MK163-RED-ARC-{i:03}','Status:','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies')),'Incomplete arc: '+p)
    baseline=set(git('ls-tree','-r','--name-only','-z',BASE).decode().split('\0')[:-1])
    for p in (set(files)-baseline)|modified:
        if p.startswith(SRC+'/') or not p.endswith('.md'): continue
        body=read(p).decode().split('Earlier text below is retained verbatim')[0]
        if p.startswith(('WORLD_CLOCK/','BOOKS/','CONSTITUTIONS/')):
            need(not re.search(r'\b(Kira|Kiru|Akira|Nix|Rayon|runae|Aethrin|Velum)\b',body,re.I),'Active spelling: '+p)
            need(not re.search(r'\braeon\b',body.replace('Raeon',''),re.I),'Raeon casing: '+p)
        for dest in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',body):
            if not dest.startswith(('https://','http://','#')):
                need((ROOT/p).parent.joinpath(dest.split('#')[0]).exists(),'Broken link: '+p+' -> '+dest)
    need(not any(p.lower().startswith('_inbox/') for p in files),'Tracked inbox')
    git('check-ignore','-q','_inbox/test.zip');git('diff','--check',BASE);git('diff','--cached','--check')
    return dict(status='PASS',baseline=BASE,source_sha256=inventory['archive_sha256'],outer_manifest_entries=26,archives_including_nested_only=len(seen),inner_declared_hashes=declared,unique_source_files=len(leaves),previous_files=len(baseline),previous_byte_identical=unchanged,previous_expanded=expanded,previous_checkpoint_and_workshop_unchanged=history,topic_checks=len(checks),score_vector=values,score='54/91; floor(54/13) = 4 (Green)',tournament='Green/fourth; Yellow rejected',working_links='PASS',literal_transcript_complete=False)
if __name__=='__main__':
    print(json.dumps(validate(Path(sys.argv[1])),indent=2))
