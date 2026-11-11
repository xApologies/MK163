"""Read-only verification of checkpoint 020 and its scoped repository integration."""
import argparse,csv,hashlib,io,json,math,os,re,stat,subprocess,urllib.parse,zipfile
from pathlib import Path,PurePosixPath,PureWindowsPath
BASE='c76eb272e8fce77c465170e16d5d812c0e9965be'
W='PROVENANCE/WORKSHOP/CUMULATIVE_020_2026_11_11/'
C='CHECKPOINTS/CUMULATIVE_020/'
BOUND='## Earlier record · preserved verbatim'
def need(x,s):
    if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate(root,archive,receipts=False):
    def git(*args):return subprocess.check_output([os.environ.get('MK163_GIT','git'),'-c','core.autocrlf=false','-C',str(root),*args])
    def raw(p):return (root/p).read_bytes()
    def text(p):return raw(p).decode('utf8')
    def current(p):return text(p).split(BOUND)[0]
    source=json.loads(raw(W+'SOURCE_MAP.json'))
    need(sha(archive.read_bytes())==source['archive_sha256']=='97f83c0752fd011ece795a3fcdb05f09392b4fa5d28c0d5c54eee8d4049d6a79','Archive identity')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();need(len(names)==len(set(n.casefold() for n in names)),'ZIP collision')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and not PureWindowsPath(str(p)).drive and ':' not in str(p) and '\\' not in str(p) and all(s not in ('..','.git','_inbox') and not PureWindowsPath(s).is_reserved() for s in p.parts),'ZIP path')
            need(not i.flag_bits&1 and not stat.S_ISLNK(i.external_attr>>16) and i.file_size<50_000_000,'ZIP metadata')
        need(z.testzip() is None,'CRC');data={n:z.read(n) for n in names}
    need(set(data)==set(source['members']) and len(data)==41,'Supplied coverage')
    installed={};reused=0
    for n,e in source['members'].items():
        need(len(data[n])==e['bytes'] and sha(data[n])==e['sha256'],'Source hash')
        need(raw(e['installed'])==data[n],'Installed source bytes: '+e['installed'])
        installed[e['short']]=e['installed'];reused+=e['disposition'].startswith('reused')
    need(reused==2,'Duplicate image prevention')
    passed=0;missing=[]
    for n,b in data.items():
        if 'MANIFEST' not in n or not n.endswith('.json'):continue
        doc=json.loads(b);entries=doc.get('files',doc);parent=str(PurePosixPath(n).parent)
        for key,h in entries.items():
            options=[key,parent+'/'+key]
            if key.startswith('MK163_') and '/' in key:options.append(parent+'/'+key.split('/',1)[1])
            found=[x for x in dict.fromkeys(options) if x in data]
            if not found:missing.append((key,h));continue
            need(len(found)==1 and sha(data[found[0]])==h,'Manifest '+key);passed+=1
    need(passed==113 and {h for _,h in missing}=={'85b169f49a2fc5149f09786656ef0d74a69b1f4e36e4fd903f77cb0645dc9cc4','687fcf95130f63d5718ec433789edc64f2ca957a1dcd7db2e31154ba5c6e5d94'},'Unexpected manifest failures')
    need(source['acceptance']['author_reply']=='Integrate with the gap documented','Historical gap acceptance')
    def sr(short):return text(installed[short])
    def rows(short):return list(csv.DictReader(io.StringIO(sr(short))))
    d=rows('020/CALENDAR/DAILY_LEDGER_DAY_000_167.csv')
    need(len(d)==168 and [int(x['ledger_day']) for x in d]==list(range(168)),'Daily coverage')
    months=['Aelor','Aerith','Aelora','Aevrin','Aelis','Aevor','Aelith','Aerion','Aeveth','Aesith','Aeleth'];lengths=[33,32,31,33,31,32,33,32,31,33,32];week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
    need(sum(lengths)==353 and 360-sum(lengths)==7,'Calendar arithmetic')
    need('353' in current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md') and '351' in current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md') and 'OPEN' in current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md'),'Calendar conflict disclosure')
    for i,r in enumerate(d):
        ordinal=70+i;n=ordinal;m=0
        while n>lengths[m]:n-=lengths[m];m+=1
        need((r['month'],int(r['day_of_month']),int(r['year_week']),r['weekday'])==(months[m],n,(ordinal-1)//6+1,week[(4+i)%6]),'Calendar day '+str(i))
    md=sr('020/CALENDAR/DAILY_LEDGER_DAY_000_167.md')
    mdrows=[[x.strip() for x in l.strip('|').split('|')] for l in md.splitlines() if re.match(r'^\| \d+ \|',l)]
    need(mdrows==[list(x.values()) for x in d],'CSV/Markdown agreement')
    master=text('CONTINUITY/RED_RUNNING_DAY_LEDGER.md')
    need(md.strip() in master,'Full daily source text retained')
    oldrows=rows('019/CALENDAR/DAILY_LEDGER_DAY_000_116.csv')
    for i,r in enumerate(oldrows):
        need(list(r.values())[:5]==list(d[i].values())[:5],'Inherited date changed')
        need(r['Event / status'] in d[i]['event_status'] or (i==85 and r['Event / status'].startswith('Unspecified')),'Lost 019 event '+str(i))
    attended=[19,25,37,49,55,67,73,79,91,97,109,121,127,145,151,163]
    absent=[31,43,61,85,103,115,133,139]
    need(all(d[i]['weekday']=='Aiven' for i in attended+absent+[157]),'Tournament weekday')
    terms={42:['two remain','withdraw'],85:['Green','closes'],94:['one remains'],116:['seven','home-based'],123:['Blue','closes'],137:['43 lb','0 banked'],151:['subtle','Green'],157:['OPEN'],164:['Age of Knowledge','Zero'],166:['Black Sprite','Black/Neon','Fireball'],167:['researcher','abecca']}
    for day,ts in terms.items():
        for t in ts:need(t.casefold() in d[day]['event_status'].casefold(),'Event day '+str(day)+' / '+t)
    inc=rows('017/INCOME_REFERENCE.csv');expected=[310,580,890,1290,3000,5100];rents=[50,90,175,600,1400,3750]
    need(len(inc)==6,'Income coverage')
    for r,v,rent in zip(inc,expected,rents):
        need(int(r['current_monthly_eln'])==v and int(r['average_rent_eln'])==rent and int(r['after_rent_eln'])==v-rent and int(r['annual_11_month_eln'])==v*11,'Income arithmetic')
        need(abs(float(r['rent_burden_percent'])-rent/v*100)<0.0001 and abs(float(r['current_multiplier_from_red'])-v/310)<1e-7,'Income derived ratio')
    prices=rows('017/CHAINMAIL_ROBE_RETAIL_REFERENCE.csv')
    need(len(prices)==6,'Tier coverage')
    for i,r in enumerate(prices):
        v=[int(r[k]) for k in ['ring_material_eln','labor_eln','mass_reduction_enchantment_eln','margin_eln']]
        need(sum(v)==int(r['retail_eln']) and v[2]==150,'Robe component sum')
        if i<5:need(sum(v)==350+210*(i+1),'Tier price formula')
    need(7*1550-7*1000-2*580==2690 and 6*550-1160==2140 and 3*550==1650 and math.ceil(770/260)==3 and math.ceil(770/490)==2,'Business arithmetic')
    income_owner=current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CHROMATIC_INDIVIDUAL_INCOME_SCALE.md')
    rent_owner=current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CHROMATIC_RENTAL_AVERAGES.md')
    armor_owner=current('WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md').replace('*','')
    for r,v,rent in zip(inc,expected,rents):
        need(f"| {r['district']} | {v} | {v*11} |" in income_owner,'Active income owner')
        need(f"| {r['district']} | {rent} | {v} | {v-rent} | {100*rent/v:.2f}% |" in rent_owner,'Active rent owner')
    for r in prices:
        row=' | '.join(r[k] for k in ['layers','ring_material_eln','labor_eln','mass_reduction_enchantment_eln','margin_eln','retail_eln'])
        need('| '+row+' |' in armor_owner.replace(',',''),'Active robe tier components')
    need('2690 eln' in armor_owner and '1700' in armor_owner and '1550' in armor_owner,'Active workshop model')
    actual=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1])
    paths=json.loads(raw(C+'CHANGED_PATHS.json'));expectedpaths=set(paths['added']+paths['modified'])
    prior=set();changed=set();history=0;images=0
    for line in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,n=line.split(b'\t',1);p=n.decode();prior.add(p);b=raw(p);oid=meta.split()[-1]
        same=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()==oid
        if not same:
            changed.add(p);before=git('cat-file','blob',oid.decode())
            if p=='PROVENANCE/SOURCE_REGISTRY.json':
                r=json.loads(b);last=r['subsequent_deliveries'].pop();need(r==json.loads(before) and last['id']=='MK163_CUMULATIVE_CHECKPOINT_020','Registry preservation')
            elif p=='.gitattributes':need(b.startswith(before),'Attribute preservation')
            else:need(b.endswith(before),'Prior detail lost: '+p)
        if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')):need(same,'Historical record modified: '+p);history+=1
        if p.lower().endswith(('.png','.jpg','.jpeg','.svg','.pdf')):need(same,'Prior visual/source altered');images+=1
    added=actual-prior
    need(prior<=actual and added|changed==expectedpaths,'Unexpected paths/deletion')
    need(set(paths['added'])==added and set(paths['modified'])==changed and not paths['deleted'],'Changed-path classification')
    need(not any(p.startswith('_inbox/') or p.endswith('.zip') or '/SHAPINGS/' in p for p in added),'Out-of-scope import')
    need({p for p in changed if p.startswith('BOOKS/')}=={'BOOKS/RED/ARCS/ARC_002/ARC.md','BOOKS/RED/ARCS/ARC_003/ARC.md'},'Arc scope')
    protected=['WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md','WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CARD_CLASS_PRICES.md','WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md','WORLD_CLOCK/L1_FANTASY/TRANSDUCTION_LIFECYCLE.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/TOURNAMENT_AND_RING_ACQUISITION.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/GENESIS_ROBE.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md','WORLD_CLOCK/L3_CHARACTERS_EVENTS/CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md']
    need(not set(protected)&changed,'Protected unrelated canon changed')
    baselineledger=git('show',BASE+':CONTINUITY/ORANGE_RUNNING_DAY_LEDGER.md').decode().split(BOUND)[0]
    need(all(l in master for l in baselineledger.splitlines() if l.startswith('|')),'Prior interval event lost')
    links=0
    for p in added|changed:
        need(not (root/p).is_symlink() and len(raw(p))<50_000_000,'File metadata')
        if p.startswith(W) or not p.endswith('.md'):continue
        t=current(p)
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',t):
            if target.startswith(('http://','https://','#')):continue
            dest=(root/p).parent.joinpath(urllib.parse.unquote(target.split('#')[0])).resolve()
            need(root.resolve() in dest.parents and dest.exists(),'Broken link '+p+' -> '+target);links+=1
        if p.startswith(('WORLD_CLOCK/','BOOKS/')):
            need(not re.search(r'\b(Kira|Kyra|Nix|Nicks|Magi|Aethryn|Valum)\b',t),'Protected names '+p)
    need(len(re.findall(r'^\| C020-\d+ \|',text(C+'REVERSE_DIFF.md'),re.M))==26,'Topic coverage')
    git('diff','--check',BASE);git('diff','--cached','--check');git('check-ignore','-q','_inbox/test.zip')
    result={'status':'PASS_WITH_APPROVED_HISTORICAL_GAP_AND_DISCLOSED_SOURCE_CONFLICTS','baseline':BASE,'supplied_members':41,'new_source_members':39,'reused_source_images':2,'declared_hashes_passed':passed,'missing_018_historical_ledgers':2,'accepted_by_author':True,'daily_rows':168,'inherited_019_rows_preserved_or_explicitly_updated':117,'income_rows':6,'price_rows':6,'calendar_listed_days':353,'calendar_claimed_days':351,'calendar_declared_year':360,'calendar_computed_gap':7,'calendar_source_claimed_gap':9,'calendar_total_resolution':'OPEN','year_week_alignment':'OPEN','topics':26,'prior_files':len(prior),'prior_files_byte_identical':len(prior)-len(changed),'prior_history_files_byte_identical':history,'prior_visual_files_byte_identical':images,'added':len(added),'modified':len(changed),'deleted':0,'local_links':links,'blocking_canon_conflicts':[],'literal_transcript_complete':False}
    if receipts:
        receipt=json.loads(raw(C+'VALIDATION.json'))
        for k,v in result.items():need(receipt[k]==v,'Receipt drift '+k)
        hm=json.loads(raw(C+'CHANGED_FILES_SHA256.json'))
        need(set(hm['files'])==expectedpaths-{C+'CHANGED_FILES_SHA256.json'},'Manifest coverage')
        for p,h in hm['files'].items():need(sha(raw(p))==h['sha256'] and len(raw(p))==h['bytes'],'Changed hash '+p)
        result['report_integrity']='PASS'
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--check-reports',action='store_true');a=p.parse_args()
    print(json.dumps(validate(a.root,a.archive,a.check_reports),ensure_ascii=False,indent=2))
