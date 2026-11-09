"""Validate the Orange 005 integration at its commit, against the original rebuilt ZIP."""
import hashlib,json,re,stat,subprocess,sys,urllib.parse,zipfile
from pathlib import Path,PurePosixPath,PureWindowsPath
ROOT=Path(__file__).resolve().parents[2]
BASE='4494f1fa4a045de471bbdc801af1dd9bd9eb745b'
SRC='PROVENANCE/WORKSHOP/ORANGE_CUMULATIVE_005_2026_11_09/'
BOUND='## Earlier record · preserved verbatim'
BAD='VISUAL_REFERENCES/ACCORD_REGISTRY_FIVE_BADGES_APPROVED.jpeg'
CAT='VISUAL_REFERENCES/VAERYN_ADULT_AUTHOR_REFERENCE.jpeg'
L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION/';L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS/'
def need(ok,why):
    if not ok:raise ValueError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-c','core.autocrlf=false','-C',str(ROOT),*args])
def raw(p):return (ROOT/p).read_bytes()
def text(p):return raw(p).decode('utf8')
def active(p):return text(p).split(BOUND)[0]
def safe(names):
    need(len(names)==len({x.casefold() for x in names}),'Case collision')
    for n in names:
        p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and not PureWindowsPath(n).drive and ':' not in n and '\\' not in n and all(x not in ('.','..','.git','_inbox') and x==x.rstrip(' .') and not PureWindowsPath(x).is_reserved() for x in p.parts),'Unsafe path '+n)
def validate(archive):
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();safe(names)
        need(len(names)==15 and all(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1 and i.file_size<1_000_000 for i in z.infolist()) and z.testzip() is None,'Unsafe ZIP or CRC error')
        m=json.loads(z.read('MANIFEST.json'));need(m['checkpoint']=='005' and m['cumulative_from']==['001','002','003','004'] and set(names)==set(m['files'])|{'MANIFEST.json'},'Manifest coverage')
        for n in names:
            b=z.read(n);need(raw(SRC+n)==b,'Changed original: '+n)
            if n!='MANIFEST.json':need(len(b)==m['files'][n]['bytes'] and sha(b)==m['files'][n]['sha256'],'Hash/size: '+n)
        expected={BAD:'213656a94b6cd02686f0b26f2131a250c4edf9d48d84375e303f7ba6304dc3fc',CAT:'6e400136b30f2ca18363bcbc8ee675db3ab8e09bda5d56c94b475b8ecf08e334'}
        need(all(sha(z.read(n))==digest for n,digest in expected.items()),'Image identity')
    paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1]);safe(list(paths))
    prior=set();changed=set();history=0
    for row in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,p=row.split(b'\t',1);p=p.decode();prior.add(p);b=raw(p)
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
        if oid!=meta.split()[-1]:
            changed.add(p);before=git('cat-file','blob',meta.split()[-1].decode())
            if p=='PROVENANCE/SOURCE_REGISTRY.json':
                reg=json.loads(b);last=reg['subsequent_deliveries'].pop()
                need(last['archive_sha256']==sha(archive.read_bytes()) and reg==json.loads(before),'Previous registry lost')
            else:need(b.startswith(before) if p=='.gitattributes' else b.endswith(before),'Baseline text lost: '+p)
        if p.startswith(('CHECKPOINTS/','PROVENANCE/WORKSHOP/')):need(p not in changed,'Historical source/report changed: '+p);history+=1
    additions=paths-prior;need(prior<=paths and not any(p.endswith('.zip') for p in additions),'Unexpected deletion/ZIP')
    for p in additions|changed:
        b=raw(p);need(len(b)<100_000_000,'Oversize: '+p)
        if not p.endswith(('.md','.py','.json')):continue
        t=b.decode('utf8')
        if p.startswith(SRC) or not p.endswith('.md'):continue
        cur=t.split(BOUND)[0]
        if p.startswith(('BOOKS/','CONTINUITY/','WORLD_CLOCK/','CONSTITUTIONS/')):
            need(not re.search(r'\b(Kira|Nix|Raeon|RAEON|Aethrin|Valum|Sigilwright)\b', cur.replace("'Sigilwright' was an unselected naming suggestion",'')),'Active vocabulary: '+p)
        for tgt in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',cur):
            if not tgt.startswith(('http://','https://','#')):
                need((ROOT/p).parent.joinpath(urllib.parse.unquote(tgt.split('#')[0])).exists(),'Link: '+p+' -> '+tgt)
    ledger=text('CONTINUITY/ORANGE_RUNNING_DAY_LEDGER.md')
    rows={k:v for k,v in re.findall(r'^\| ([^|\n]+) \| ([^|\n]+) \| [^|\n]+ \|$',ledger,re.M)}
    checks={'0':'1,000 eln','~3':'~80,000','~6':'Second','~9':'Third','11':'eight elapsed','12 · visit 1':'postpones','13':'two larger stones','14':'60-card','15':'two days','16':'11 damaged','17':'contact/scheduling','18':'Preparation','19':'evening','19–23 inclusive':'eleven','24':'same independent freight','25':'eleven','26 · visit 2':'supervised practical','27':'master mailwright','28':'Second shipment','28–35 inclusive':'Eight-day','36':'dispatch','37':'picks up','38':'freight','39 · visit 3':'without demonstration shirt'}
    for day,term in checks.items():need(term.casefold() in rows.get(day,'').casefold(),'Ledger: '+day)
    need(23-19+1==5 and 35-28+1==8 and [int(k.split()[0]) for k in rows if '· visit' in k]==[12,26,39],'Visit/repair spans')
    checks2={
      L2+'CULTURE/AITHREN_VAELUM_ACCORD.md':['appropriate recognized rank','Independent private contracts do not','Green District','Yellow District','Ground floor','Second floor','Third floor','Underground basement','100 feet radius','standard material allowance'],
      L2+'PROFESSIONS/REGISTRY_BADGES_AND_CHAINMAIL_QUALIFICATION.md':['Transduction','Craftsmanship','Alchemy','Architect','Sigilcraft','Red | Ruby','Orange | Citrine','Yellow | Topaz','Green | Emerald','Blue | Sapphire','Violet | Amethyst','White | Diamond','second from the left','magnetic backing','without piercing','phase field','input quality control','Closure','Flat weave','Joining/integrity','Shaping','Finishing','Advanced technique','duration are not locked','WHITE rank in CHAINMAIL ARMORSMITHING','Kaira did NOT manufacture those rings'],
      L3+'CHARACTERS/KAIRA.md':['two inches','all seven books','3 consumed','1 given','3 retained','cultivation','around 16'],
      L2+'CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md':['60-card deck','one or two casual games','The Geometry of Existence','literary crossover'],
      L2+'BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md':['six cutaneous','open arc','skin surface','prepared Bindings','NO aen throughput boost','Day 17'],
      L2+'BIOLOGY/VAERYN.md':['Green Realm native','four feet at shoulder','Males: Green ↔ Blue ↔ Violet','Females: Red ↔ Orange ↔ Yellow','no visible adult dermal striping','not carnivorous','exact','reference'],
      L3+'CHARACTERS/NYX.md':['father was hunted','fate','mother’s death is confirmed','hostile Transduction','aftermath','shallow','mewing','seven weeks','without her demonstration chainmail shirt'],
      'BOOKS/RED/ARCS/ARC_002/ARC.md':['asks to list','three mineral vaen','20 eln illustrative','repair-specific compatible rings','five-day','dinner','third','No early Sprite or Ring']}
    for p,terms in checks2.items():
        v=active(p).replace('*','').casefold()
        for t in terms:need(t.casefold() in v,p+': '+t)
    for p in [L2+'INSTITUTIONS/ACCORD_REGISTRY/'+r+'.md' for r in ('GUARDIAN','OFFENSIVE','HELKIR','SUPPORT')]+[L2+'INSTITUTIONS/ACCORD_REGISTRY_EXAMINATIONS.md',L3+'EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md',L3+'EVENTS/TOURNAMENT_AND_RING_ACQUISITION.md','BOOKS/RED/ARCS/ARC_001/ARC.md','BOOKS/RED/ARCS/ARC_003/ARC.md','BOOKS/RED/ARCS/ARC_007/ARC.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md',L2+'TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md']:
        need(raw(p)==git('show',BASE+':'+p),'Protected owner: '+p)
    git('diff','--check',BASE);git('diff','--cached','--check');git('check-ignore','-q','_inbox/'+archive.name)
    return dict(status='PASS',baseline=BASE,attachment=archive.name,archive_bytes=archive.stat().st_size,archive_sha256=sha(archive.read_bytes()),manifest_hashes=14,source_members_exact=15,images_sha256=expected,prior_files_preserved=len(prior),prior_files_byte_identical=len(prior)-len(changed),prior_checkpoint_and_workshop_byte_identical=history,added=len(additions),modified=len(changed),deleted=0,visit_days=[12,26,39],first_repair_items=11,first_cycle_days=5,second_cycle_days=8,local_links='PASS',changes=sorted(additions|changed),literal_transcript_complete=False)
if __name__=='__main__':print(json.dumps(validate(Path(sys.argv[1])),indent=2))
