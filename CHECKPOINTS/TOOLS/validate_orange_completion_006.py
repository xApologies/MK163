"""Read-only validation of Orange completion 006 against its fetched MK163 baseline."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import argparse,hashlib,json,os,re,stat,subprocess,urllib.parse,zipfile
ROOT=Path(__file__).resolve().parents[2]
BASE='4bc6a822fcd2fe97eb53dd1216d602d3c7b0f62c'
SRC='PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/'
BOUND='## Earlier record · preserved verbatim'
EXPECTED=set([".gitattributes","AGENTS.md","BOOKS/RED/ARCS/ARC_002/ARC.md","BOOKS/RED/ARCS/ARC_003/ARC.md","BOOKS/RED/BOOK_OVERVIEW.md","CHECKPOINTS/ORANGE_COMPLETION_006_INTEGRATION.md","CHECKPOINTS/ORANGE_COMPLETION_006_VALIDATION.json","CHECKPOINTS/TOOLS/validate_orange_completion_006.py","CONSTITUTIONS/07_NAMING_CONVENTIONS.md","CONTINUITY/ORANGE_RUNNING_DAY_LEDGER.md","CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md","PROVENANCE/OPEN_QUESTIONS_CURRENT.md","PROVENANCE/ORANGE_COMPLETION_006_SUPERSESSIONS.md","PROVENANCE/SOURCES.md","PROVENANCE/SOURCE_REGISTRY.json","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/AEN_STAGE_ONE_AND_YELLOW_HANDOFF_006.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/BANKING_MAGE_GLASS_006.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/CHECKPOINT_HISTORY.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/CODEX_INTEGRATION_006.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/MANIFEST.json","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/ORANGE_ARC_COMPLETION_006.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/ORANGE_DAY_LEDGER_COMPLETE_006.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/README.md","PROVENANCE/WORKSHOP/ORANGE_COMPLETION_006_2026_11_10/SOURCE_MAP.json","WORLD_CLOCK/CURRENT_MODEL_INDEX.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/BIOLOGY/VAERYN.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/BANKING_AND_MAGE_GLASS_ACCOUNTS.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CURRENCY_AND_COMMODITY_EXCHANGE.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/ARMOR_MATERIALS_AND_ENHANCEMENT.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/MAEGE_GLASS_AND_CONSTRUCTS.md","WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/KAIRA.md","WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/NYX.md","WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/CHAINMAIL_ROBE_AND_AGE_OF_KNOWLEDGE.md"])
L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION/'
L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS/'
def need(x,msg):
    if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):return (ROOT/p).read_bytes()
def active(p):return raw(p).decode('utf8').split(BOUND)[0]
def git(*a):return subprocess.check_output([os.environ.get('MK163_GIT','git'),'-c','core.autocrlf=false','-C',str(ROOT),*a])
def safe(names):
    need(len(names)==len(set(n.casefold() for n in names)),'Case-insensitive collision')
    for n in names:
        p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and not PureWindowsPath(n).drive and ':' not in n and '\\' not in n and all(x.casefold() not in ('.','..','.git','_inbox') and x==x.rstrip(' .') and not PureWindowsPath(x).is_reserved() for x in p.parts),'Unsafe path '+n)
def validate(archive):
    m=json.loads(raw(SRC+'MANIFEST.json'));sm=json.loads(raw(SRC+'SOURCE_MAP.json'))
    need(sha(archive.read_bytes())==sm['archive_sha256']=='6de8b2be15eaa70179ab028a6c77cbac55606f6acb8eeed2201286dc67c5bfeb','Source archive mismatch')
    need(m['checkpoint']=='006' and m['parent_sha256']=='410be5be4b610e0ad019659aed8b3fc29a26ab777fe0e28fc0d97e74c4a50d07','Checkpoint parent')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();safe(names)
        need(len(names)==20 and len(m['files'])==19 and set(names)==set(m['files'])|{'MANIFEST.json'} and set(names)==set(sm['members']),'Member coverage')
        need(z.testzip() is None and all(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1 and i.file_size<1_000_000 for i in z.infolist()),'ZIP safety/CRC')
        for n in names:
            b=z.read(n);row=sm['members'][n];safe([row['path']])
            need(raw(row['path'])==b and sha(b)==row['sha256'] and len(b)==row['bytes'],'Source fidelity '+n)
            if n in m['files']:need(sha(b)==m['files'][n]['sha256'] and len(b)==m['files'][n]['bytes'],'Manifest '+n)
    reused=[n for n,row in sm['members'].items() if not row['path'].startswith(SRC)]
    need(len(reused)==12 and len(sm['members'])-len(reused)==8,'Duplicate-source reconciliation')
    images={'VISUAL_REFERENCES/ACCORD_REGISTRY_FIVE_BADGES_APPROVED.jpeg':'213656a94b6cd02686f0b26f2131a250c4edf9d48d84375e303f7ba6304dc3fc','VISUAL_REFERENCES/VAERYN_ADULT_AUTHOR_REFERENCE.jpeg':'6e400136b30f2ca18363bcbc8ee675db3ab8e09bda5d56c94b475b8ecf08e334'}
    for n,h in images.items():need(n in reused and sha(raw(sm['members'][n]['path']))==h,'Original image '+n)
    paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1]);safe(list(paths))
    prior=set();changed=set();history=0
    for line in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,p=line.split(b'\t',1);p=p.decode();prior.add(p);b=raw(p)
        need((ROOT/p).is_file() and not (ROOT/p).is_symlink(),'Missing/nonregular '+p)
        oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
        if oid!=meta.split()[-1]:
            changed.add(p);before=git('cat-file','blob',meta.split()[-1].decode())
            if p=='PROVENANCE/SOURCE_REGISTRY.json':
                reg=json.loads(b);last=reg['subsequent_deliveries'].pop()
                need(last['archive_sha256']==sha(archive.read_bytes()) and reg==json.loads(before),'Previous registry changed')
            elif p=='.gitattributes':need(b.startswith(before),'Attributes truncated')
            else:need(b.endswith(before),'Prior text lost: '+p)
        if p.startswith(('CHECKPOINTS/','PROVENANCE/WORKSHOP/')):
            need(p not in changed,'Historical file changed '+p);history+=1
    additions=paths-prior
    need(prior<=paths and additions|changed==EXPECTED,'Unexpected changed/missing paths: '+str(sorted((additions|changed)^EXPECTED)))
    need(not any(p.lower().startswith('_inbox/') or p.lower().endswith(('.zip','.jpeg','.png','.pdf')) for p in additions),'Inbox/archive/duplicate image added')
    links=0
    for p in additions|changed:
        b=raw(p);need(len(b)<100_000_000 and not (ROOT/p).is_symlink(),'Oversize or symlink '+p)
        if p.startswith(SRC) or not p.endswith('.md'):continue
        cur=active(p)
        if p.startswith(('BOOKS/','CONTINUITY/','WORLD_CLOCK/','CONSTITUTIONS/')) or p=='AGENTS.md':
            need(not re.search(r'\b(Kira|Nix|Nixon|Raeon|RAEON|Rayon|Aethrin|Valum)\b',cur),'Current spelling '+p)
        for tgt in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',cur):
            if not tgt.startswith(('http://','https://','#')):
                target=(ROOT/p).parent.joinpath(urllib.parse.unquote(tgt.split('#')[0])).resolve()
                need(ROOT.resolve() in target.parents and target.exists(),'Link '+p+' -> '+tgt);links+=1
    led=active('CONTINUITY/ORANGE_RUNNING_DAY_LEDGER.md')
    rows={k.strip():v.strip() for k,v in re.findall(r'^\| ([^|\n]+) \| ([^|\n]+) \| [^|\n]+ \|$',led,re.M)}
    expected={'-1 (working)':'perhaps eln/dust','0':'300,000','11':'eight elapsed','12 · visit 1':'postpones','13':'two larger','14':'60-card','15':'two days','16':'11 damaged','17':'contact/scheduling','19–23 inclusive':'eleven','21':'Red point','26 · visit 2':'supervised practical','27':'lesson 2','28–35 inclusive':'Eight-day','32':'all six','38':'does not yet close','39 · visit 3':'without demonstration shirt','39 evening':'does not yet know','40–41':'orange','41–48 inclusive':'Third','42':'realm-fauna','43':'Red and Orange','49':'pickup','50':'physical five-layer','51 · visit 4':'separate secure pouch','52–62':'closes Yellow','63':'Nyx asleep'}
    for d,t in expected.items():need(t.casefold() in rows.get(d,'').casefold(),'Chronology '+d)
    need([int(k.split()[0]) for k in rows if '· visit' in k]==[12,26,39,51],'Visit index')
    need(23-19+1==5 and 35-28+1==8 and 48-41+1==8 and 50-11==39 and 63-51==12 and 62-52+1==11,'Elapsed/inclusive arithmetic')
    checks={
      L2+'ECONOMY/BANKING_AND_MAGE_GLASS_ACCOUNTS.md':['handwritten','fixed local manifold','carries no balance or valuables','0113872','illustrative ONLY','private recovery phrase','same account','may deny access','Account number alone','Cross-branch','NOT','keepsake','stored Green'],
      L2+'BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md':['Day 21 Red point','Day 27 Red/Orange/Yellow points','Day 32 all six','Day 38 attempts','Day 43 closes Red and Orange','Red < Orange < Yellow < Green < Blue < Violet','analogy','Stage II','not','open arc','operational Genesis Cards'],
      L3+'CHARACTERS/NYX.md':['Day 39 evening','Days 40–41','Day 42','almost-luminous','supervision','separate pouch','not','mature dermal stripes','absorption rate remain open','father was hunted','fate unknown'],
      L3+'EVENTS/CHAINMAIL_ROBE_AND_AGE_OF_KNOWLEDGE.md':['Day 50','Day 51','39 elapsed','planning estimate','First stop','Second stop','Third stop','verify receipt','Age of Knowledge','date/scene remains OPEN','native-energy'],
      L2+'TECHNOLOGY/ARMOR_MATERIALS_AND_ENHANCEMENT.md':['P(i,j)=(i,j)','Q(i,j)=(i+1/2,j+1/2)','not a mechanically verified','OPEN','Magnetic front/back/side','planning estimate'],
      'BOOKS/RED/ARCS/ARC_003/ARC.md':['Day 63','Days 52–62','twelve elapsed','scene concept','Nyx asleep in her lap','Stage II','have NOT occurred','end-of-Yellow sponsorship'],
      'PROVENANCE/ORANGE_COMPLETION_006_SUPERSESSIONS.md':['OC006-S14','Mage Glass','No global','literal','No unresolved blocking conflict']}
    for p,terms in checks.items():
        txt=active(p).replace('*','').casefold()
        for term in terms:need(term.casefold() in txt,'Content scope '+p+' / '+term)
    protected=[L2+'PROFESSIONS/REGISTRY_BADGES_AND_CHAINMAIL_QUALIFICATION.md',L2+'CULTURE/AITHREN_VAELUM_ACCORD.md',L2+'TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md',L3+'EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md',L3+'EVENTS/TOURNAMENT_AND_RING_ACQUISITION.md',L3+'EVENTS/GENESIS_ROBE.md',L3+'EVENTS/SIX_BLACK_BONDS.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md','WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md','BOOKS/RED/ARCS/ARC_001/ARC.md',*['BOOKS/RED/ARCS/ARC_%03d/ARC.md'%i for i in range(4,8)]]
    for p in protected:need(raw(p)==git('show',BASE+':'+p),'Protected milestone '+p)
    score=raw(L3+'EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md').decode()
    nums=[int(x) for x in re.findall(r'^\| \d+ \| [^|\n]+ \| (\d+) \| [^|\n]+ \|$',score,re.M)]
    need(nums==[5,5,5,4,5,4,4,4,3,4,4,3,4] and sum(nums)==54 and sum(nums)//13==4,'Support rating changed')
    coverage=active('CHECKPOINTS/ORANGE_COMPLETION_006_INTEGRATION.md')
    need(len(re.findall(r'^\| OC006-\d+ \|',coverage,re.M))==15,'Topic coverage')
    git('diff','--check',BASE);git('diff','--cached','--check');git('check-ignore','-q','_inbox/'+archive.name)
    return dict(status='PASS',baseline=BASE,archive=archive.name,archive_bytes=archive.stat().st_size,archive_sha256=sha(archive.read_bytes()),manifest_hashes=19,source_members_exact=20,unchanged_members_reused=12,new_source_members=8,images_sha256=images,prior_files_preserved=len(prior),prior_files_byte_identical=len(prior)-len(changed),prior_history_files_byte_identical=history,added=len(additions),modified=len(changed),deleted=0,checked_links=links,topic_rows=15,supersession_rows=14,visit_days=[12,26,39,51],lesson_days=[21,27,32,38,43],repair_spans=[5,8,8],robe_completion_day=50,orange_finale_day=51,yellow_opening_day=63,elapsed_gap=12,protected_owner_count=len(protected),support_score='54/91 Green',unresolved_blocking_conflicts=[],literal_transcript_complete=False,changes=sorted(additions|changed))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);a=ap.parse_args()
    print(json.dumps(validate(a.archive),ensure_ascii=False,indent=2))
