"""Read-only archive, source-map and numerical checks for diplomatic pouch 015."""
import csv,hashlib,io,itertools,json,math,re,stat,zipfile
from fractions import Fraction
from pathlib import Path,PurePosixPath,PureWindowsPath
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,why):
    if not ok:raise ValueError(why)
def safe(names):
    need(len(names)==len(set(n.casefold() for n in names)),'Case-insensitive path collision')
    for n in names:
        p=PurePosixPath(n)
        need(str(p)==n and not p.is_absolute() and not PureWindowsPath(n).drive and ':' not in n and '\\' not in n and all(x.casefold() not in ('.','..','.git','_inbox') and not PureWindowsPath(x).is_reserved() and x.rstrip(' .')==x for x in p.parts),'Unsafe path '+n)
def inspect_package(path):
    arcs={};leaves={};declared=[];unlisted=[]
    def walk(b,label,depth=0):
        h=sha(b)
        if h in arcs:return
        need(depth<20 and len(arcs)<100,'Archive nesting limit')
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            names=z.namelist();safe(names)
            need(z.testzip() is None and sum(i.file_size for i in z.infolist())<150_000_000,'CRC/size limit')
            need(all(not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1 and i.file_size<100_000_000 for i in z.infolist()),'ZIP metadata')
            contents={n:z.read(n) for n in names if not n.endswith('/')}
            manifests=[n for n in names if n.upper().endswith(('MANIFEST.JSON','MANIFEST_SHA256.JSON'))]
            covered=set()
            for mn in manifests:
                data=json.loads(contents[mn]);entries=data.get('files',data)
                for key,val in entries.items():
                    targets=([key] if key in contents else [str(PurePosixPath(mn).parent/key)] if str(PurePosixPath(mn).parent/key) in contents else [n for n in contents if n.endswith('/'+key)])
                    need(len(targets)==1,'Ambiguous manifest entry '+key)
                    n=targets[0];v=contents[n];digest=val.get('sha256') if isinstance(val,dict) else val
                    need(sha(v)==digest,'Manifest hash '+label+' / '+key)
                    if isinstance(val,dict) and 'bytes' in val:need(len(v)==val['bytes'],'Manifest size '+key)
                    covered.add(n);declared.append((h,mn,n))
            need(bool(manifests),'Missing manifest '+label)
            unlisted.extend({'archive':h,'path':n} for n in contents if n not in covered and n not in manifests)
            rows=[]
            arcs[h]={'label':label,'bytes':len(b),'depth':depth,'members':rows}
            for n,v in contents.items():
                vh=sha(v);rows.append({'path':n,'bytes':len(v),'sha256':vh})
                if n.lower().endswith('.zip'):walk(v,n,depth+1)
                else:
                    entry=leaves.setdefault(vh,{'bytes':len(v),'sources':[],'data':v})
                    need(entry['data']==v,'Hash collision');entry['sources'].append({'archive':h,'path':n})
    walk(path.read_bytes(),path.name)
    need(len(arcs)==10,'Unexpected cumulative archive inventory')
    need(all(r['path']=='ARCHIVE/MK163_CUMULATIVE_013_NATIVE_WHITE_CHARGING.zip' for r in unlisted),'Unexpected undeclared payload')
    return {'archive_sha256':sha(path.read_bytes()),'archives':arcs,'leaves':leaves,'declared_hashes':len(declared),'unlisted_nested_members':unlisted}
def member(inv,suffix):
    choices=[v['data'] for v in inv['leaves'].values() if any(x['path']==suffix or x['path'].endswith('/'+suffix) for x in v['sources'])]
    need(len(choices)==1,'Ambiguous source '+suffix);return choices[0]
def numeric(inv):
    def rows(n):return list(csv.DictReader(io.StringIO(member(inv,'014/'+n).decode('utf8'))))
    names=['Red','Orange','Yellow','Green','Blue','Violet']
    refs=[8,7,5,3,2,1];thresholds=[1,3,9,18,36,72];old=[1,13,143,1001,5005,15015];prices=[20,35,60,110,230,500]
    rates=dict(zip(names,[Fraction(1,t) for t in refs]));white=sum(rates.values())/6;vol=Fraction(25,7)**3
    need(white==Fraction(1933,5040) and vol==Fraction(15625,343),'Exact reference arithmetic')
    def near(a,b,why,ab=1e-8):need(math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=ab),why+': '+str(a)+' != '+str(b))
    comb=rows('ALL_63_DIRECT_BASIN_COMBINATIONS.csv');full=rows('ALL_768_CHARGING_OUTCOMES.csv');nw=rows('NATIVE_WHITE_12_CHARGING_OUTCOMES.csv');mass=rows('ALL_12_MASS_AND_CRYSTAL_PRICE_RECORDS.csv')
    need((len(comb),len(full),len(nw),len(mass))==(63,768,12,12),'Matrix dimensions')
    combos={tuple(r['input_configuration'].split(' + ')) for r in comb}
    need(combos=={s for k in range(1,7) for s in itertools.combinations(names,k)},'Missing/duplicate basin subsets')
    for r in comb:
        ch=r['input_configuration'].split(' + ');rate=sum(rates[n] for n in ch)
        need(int(r['basin_count'])==len(ch),'Basin count')
        near(r['red_equivalent_rate_per_hour'],rate,'Combination rate');near(r['red_charge_hours_7mm'],1/rate,'7mm Red');near(r['red_charge_hours_25mm'],vol/rate,'25mm Red')
    keys=set();white_rows=[];max_err=0
    for r in full:
        size=int(r['cube_edge_mm']);idx=names.index(r['target_state']);iswhite=r['pathway']=='native_white_equal_six_component'
        need(size in (7,25) and r['pathway'] in ('native_white_equal_six_component','direct_independent_basins'),'Row dimensions')
        ch=r['input_configuration'].split(' + ') if not iswhite else names
        rate=white if iswhite else sum(rates[n] for n in ch)
        need(int(r['input_basin_count'])==len(ch),'Input basin count')
        if iswhite:need(r['input_configuration']=='Native White (equal accessible six-basin composition)','White configuration');white_rows.append(r)
        key=(r['pathway'],r['input_configuration'],size,idx);need(key not in keys,'Duplicate charging outcome');keys.add(key)
        delta=thresholds[idx]-(thresholds[idx-1] if idx else 0)
        need(int(r['red_equivalent_threshold'])==thresholds[idx] and int(r['incremental_red_equivalents'])==delta,'Threshold ladder')
        near(r['combined_red_equivalents_per_hour'],rate,'Outcome rate')
        total=thresholds[idx]*Fraction(size,7)**3/rate;inc=delta*Fraction(size,7)**3/rate
        near(r['from_empty_active_hours'],total,'Cumulative hours');near(r['from_previous_active_hours'],inc,'Incremental hours')
        max_err=max(max_err,abs(float(r['from_empty_active_hours'])-float(total)))
    need(white_rows==nw and len(white_rows)==12,'White subset identity')
    masskeys=set()
    for r in mass:
        k=names.index(r['basin']);edge=int(r['edge_mm']);masskeys.add((k,edge))
        need(r['structural_coordinate']==str(k+1)+'/7' and int(r['historical_mass_law_factor'])==old[k] and int(r['revised_charge_threshold_red_equivalents'])==thresholds[k],'Separate mass/charge factors')
        raw=100*(1+0.2*math.log10(old[k]))*(edge/25)**3;carbon=3.515*(edge/10)**3
        near(r['raw_genesis_crystal_g'],raw,'Raw mass');near(r['uncharged_diamond_carbon_g'],carbon,'Carbon mass');near(r['charged_diamond_total_g'],raw+carbon,'Additive diamond mass')
        near(r['genesis_crystal_price_eln_per_100g'],prices[k],'Unchanged raw price');near(r['same_volume_crystal_price_eln'],raw/100*prices[k],'Derived raw-crystal price')
    need(masskeys=={(k,s) for k in range(6) for s in (7,25)},'Mass row coverage')
    data=json.loads(member(inv,'014/CHARGING_DATA.json'))
    need(data['metadata']['ladder']==thresholds and data['metadata']['previous_ladder']==old and data['metadata']['white_rate_fraction']=='1933/5040','JSON metadata')
    for group,csvrows in [('charging',full),('mass',mass)]:
        need(len(data[group])==len(csvrows),'JSON/CSV counts')
        for a,b in zip(data[group],csvrows):
            need(set(a)==set(b),'JSON/CSV fields')
            for k in b:
                if isinstance(a[k],(int,float)):near(a[k],b[k],'JSON/CSV '+k)
                else:need(a[k]==b[k],'JSON/CSV text '+k)
    return {'status':'PASS','direct_configurations':63,'native_white_configurations':1,'charging_outcomes':768,'native_white_outcomes':12,'mass_price_records':12,'all_six_rate':'1933/840','native_white_rate':'1933/5040','volume_ratio':'15625/343','thresholds':thresholds,'frozen_mass_factors':old,'max_float_error_hours':max_err,'white_7mm_yellow_hours':float(9/white),'white_25mm_yellow_hours':float(9*vol/white),'white_25mm_violet_hours':float(72*vol/white),'all_six_25mm_violet_hours':float(72*vol/(white*6))}

BASE='05c6977aebd5b5c6388fe9517f9435910538d793'
SOURCE='PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/'
REPORT='CHECKPOINTS/DIPLOMATIC_POUCH_015/'
BOUND='## Earlier record · preserved verbatim'
EXPECTED=set([".gitattributes","BOOKS/RED/ARCS/ARC_003/ARC.md","CHECKPOINTS/DIPLOMATIC_POUCH_015/CHANGED_FILES_SHA256.json","CHECKPOINTS/DIPLOMATIC_POUCH_015/CHANGED_PATHS.json","CHECKPOINTS/DIPLOMATIC_POUCH_015/INTEGRATION_REPORT.md","CHECKPOINTS/DIPLOMATIC_POUCH_015/OPEN_ISSUES.md","CHECKPOINTS/DIPLOMATIC_POUCH_015/REVERSE_DIFF.md","CHECKPOINTS/DIPLOMATIC_POUCH_015/SHAPINGS_MIGRATION_PLAN.md","CHECKPOINTS/DIPLOMATIC_POUCH_015/UPSTREAM_REVIEW.json","CHECKPOINTS/DIPLOMATIC_POUCH_015/VALIDATION.json","CHECKPOINTS/TOOLS/validate_pouch_015.py","PROVENANCE/SOURCES.md","PROVENANCE/SOURCE_REGISTRY.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/007/CODEX_HANDOFF.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/007/CRYSTAL_DATA.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/007/GENESIS_CRYSTAL_STANDARD.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/007/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/CODEX_INTEGRATION.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/GENESIS_CRYSTAL_DIAMOND_MASS_AND_PRICES.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/REFERENCE_DATA.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/REFERENCE_TABLE.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/008/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/CHARGING_LADDER.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/CHARGING_LADDER.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/CODEX_HANDOFF.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/DIAMOND_AND_ENERGY_STRUCTURING.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/009/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/010/AUDIT_AND_25MM_CHARGING.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/010/CHARGING_7MM_AND_25MM.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/010/CHARGING_7MM_AND_25MM.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/010/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/010/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/011/DIRECT_BASIN_CHARGING.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/011/DIRECT_BASIN_CHARGING.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/011/DIRECT_BASIN_CHARGING.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/011/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/011/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/ALL_63_BASIN_COMBINATIONS.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/ALL_756_CHARGING_OUTCOMES.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/ALL_756_CHARGING_OUTCOMES.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/CODEX_HANDOFF.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/012/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/013/CODEX_HANDOFF.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/013/NATIVE_WHITE_7MM_25MM_CHARGING.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/013/NATIVE_WHITE_7MM_25MM_CHARGING.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/013/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/013/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/ALL_12_MASS_AND_CRYSTAL_PRICE_RECORDS.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/ALL_63_DIRECT_BASIN_COMBINATIONS.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/ALL_768_CHARGING_OUTCOMES.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/CHARGING_DATA.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/CODEX_HANDOFF.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/MASTER_GENESIS_DIAMOND_AND_CRYSTAL_REFERENCE.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/NATIVE_WHITE_12_CHARGING_OUTCOMES.csv","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/014/SHA256_MANIFEST.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/AUDIT/VALIDATION_PLAN.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/CANON/CHARGING_REFERENCE.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/CANON/DIAMOND_EXCHANGE_AND_AITHREN.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/CANON/GENESIS_CRYSTALS_VS_DIAMONDS.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/CANON/SHAPINGS_CARDS_BINDINGS.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/MANIFEST_SHA256.json","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/NARRATIVE/YELLOW_ARC_ONLY.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/PROVENANCE/DECISION_LEDGER.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/PROVENANCE/SOURCE_POINTERS.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/015/executable.fd","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/README.md","PROVENANCE/WORKSHOP/DIPLOMATIC_POUCH_015_2026_11_10/SOURCE_INVENTORY.json","WORLD_CLOCK/CURRENT_MODEL_INDEX.md","WORLD_CLOCK/L1_FANTASY/BINDING_CIRCLES_AND_INSTALLATION.md","WORLD_CLOCK/L1_FANTASY/FATIGUE_AND_CROSS_INTERFACE_CONCURRENCY.md","WORLD_CLOCK/L1_FANTASY/GENESIS_CARDS.md","WORLD_CLOCK/L1_FANTASY/TRANSDUCTION_LIFECYCLE.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/CURRENCY_AND_COMMODITY_EXCHANGE.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CARD_CLASS_PRICES.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md","WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md"])
def validate_repository(root,inv):
    import os,subprocess,urllib.parse
    def git(*a):return subprocess.check_output([os.environ.get('MK163_GIT','git'),'-c','core.autocrlf=false','-C',str(root),*a])
    def raw(p):return (root/p).read_bytes()
    def cur(p):return raw(p).decode('utf8').split(BOUND)[0]
    catalog=json.loads(raw(SOURCE+'SOURCE_INVENTORY.json'))
    need(catalog['archive_sha256']==inv['archive_sha256'] and catalog['archives']==inv['archives'],'Archive graph fidelity')
    need(set(catalog['leaves'])==set(inv['leaves']),'Leaf inventory')
    reused=0
    for h,e in catalog['leaves'].items():
        safe([e['installed']]);actual=inv['leaves'][h]
        need(e['bytes']==actual['bytes'] and e['sources']==actual['sources'] and raw(e['installed'])==actual['data'],'Source member fidelity '+e['installed'])
        if e['disposition'].startswith('reused'):reused+=1;need(not e['installed'].startswith(SOURCE),'Duplicate 006 import')
    need(reused==20,'Orange original reuse')
    paths=set(git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0')[:-1]);safe(list(paths))
    prior=set();changed=set();history=0
    for line in git('ls-tree','-r','-z',BASE).split(b'\0')[:-1]:
        meta,name=line.split(b'\t',1);p=name.decode();prior.add(p);b=raw(p)
        need((root/p).is_file() and not (root/p).is_symlink(),'Missing original '+p)
        same=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()==meta.split()[-1]
        if not same:
            changed.add(p);before=git('cat-file','blob',meta.split()[-1].decode())
            if p=='PROVENANCE/SOURCE_REGISTRY.json':
                reg=json.loads(b);last=reg['subsequent_deliveries'].pop()
                need(reg==json.loads(before) and last['archive_sha256']==inv['archive_sha256'],'Previous source registry changed')
            elif p=='.gitattributes':need(b.startswith(before),'Attribute preservation')
            else:need(b.endswith(before),'Historical content lost: '+p)
        if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')):
            need(same,'Historical source/checkpoint changed '+p);history+=1
    additions=paths-prior
    need(prior<=paths and (additions|changed)==EXPECTED,'Unexpected changed paths '+str(sorted((additions|changed)^EXPECTED)))
    need(not any(p.lower().endswith(('.zip','.jpeg','.png','.jpg','.pdf')) or p.lower().startswith('_inbox/') for p in additions),'Duplicate archive/image/inbox')
    need(not any('SHAPINGS/' in p for p in additions),'Unauthorized catalog creation')
    need({p for p in changed if p.startswith('BOOKS/')}=={'BOOKS/RED/ARCS/ARC_003/ARC.md'},'Narrative scope')
    L1='WORLD_CLOCK/L1_FANTASY/';L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION/';L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS/'
    protected=['AGENTS.md','BOOKS/RED/ARCS/ARC_002/ARC.md','BOOKS/RED/BOOK_OVERVIEW.md','CONTINUITY/ORANGE_RUNNING_DAY_LEDGER.md','CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md',L3+'CHARACTERS/KAIRA.md',L3+'CHARACTERS/NYX.md',L3+'CHARACTERS/ALCHEMIST_AND_PEOPLES_PRINCESS.md',L2+'BIOLOGY/VAERYN.md',L2+'BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md',L2+'ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md',L2+'ECONOMY/BANKING_AND_MAGE_GLASS_ACCOUNTS.md',L2+'TECHNOLOGY/ARMOR_MATERIALS_AND_ENHANCEMENT.md',L3+'EVENTS/CHAINMAIL_ROBE_AND_AGE_OF_KNOWLEDGE.md',L2+'PROFESSIONS/REGISTRY_BADGES_AND_CHAINMAIL_QUALIFICATION.md',L3+'EVENTS/GENESIS_ROBE.md',L3+'EVENTS/SIX_BLACK_BONDS.md',L3+'EVENTS/TOURNAMENT_AND_RING_ACQUISITION.md',L3+'EVENTS/KAIRA_FIRST_SUPPORT_CERTIFICATION.md','PROVENANCE/LIVE_MODEL_009_BLACK_CARD_RETIREMENT.md']
    protected+=sorted(p for p in prior if p.startswith(('BOOKS/ORANGE/','BOOKS/YELLOW/')) or p.lower().endswith(('.jpeg','.jpg','.png')))
    for p in protected:need(p not in changed and raw(p)==git('show',BASE+':'+p),'Protected Orange/milestone/image '+p)
    links=0
    for p in additions|changed:
        b=raw(p);need(len(b)<100_000_000 and not (root/p).is_symlink(),'Size/symlink '+p)
        if p.startswith(SOURCE) or not p.endswith('.md'):continue
        t=cur(p)
        if p.startswith(('WORLD_CLOCK/','BOOKS/')):
            need(not re.search(r'\b(Kira|Nix|Raeon|RAEON|Aethryn|Aethrin|Valum)\b',t),'Protected spelling '+p)
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',t):
            if not target.startswith(('http://','https://','#')):
                d=(root/p).parent.joinpath(urllib.parse.unquote(target.split('#')[0])).resolve()
                need(root.resolve() in d.parents and d.exists(),'Broken link '+p+' -> '+target);links+=1
    # Compare the original price tables, not merely a matching summary sentence.
    cp=cur(L2+'ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md')
    allcp=raw(L2+'ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md').decode()
    for row in ['| Red | 200 | 20 | 0.20 |','| Orange | 350 | 35 | 0.35 |','| Yellow | 600 | 60 | 0.60 |','| Green | 1100 | 110 | 1.10 |','| Blue | 2300 | 230 | 2.30 |','| Violet | 5000 | 500 | 5.00 |','| White | 31000 | 3100 | 31.00 |']:need(row in allcp,'Raw price row')
    allcard=raw(L2+'ECONOMY/GENESIS_CARD_CLASS_PRICES.md').decode()
    for name,num in [('FOUNDATIONAL',100),('COMMON_SPECIALIZATION',230),('ADVANCED',540),('POWERFUL',1300),('EXCEPTIONAL',3100)]:need('| '+name+' | '+str(num)+' |' in allcard,'Card benchmark row')
    texts={
      L2+'TECHNOLOGY/GENESIS_DIAMONDS.md':['fatigue was paid upfront','retired from the active progression','7 mm','Selective discharge','1,3,9,18,36,72','1933/5040','23.46611484738748','1068.9738906426512','mass factors','five-day','All_768'],
      L2+'TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md':['cannot create','intrinsic','cannot replace','White cube mass/density remain OPEN','0.2 log10','154.921875','screening check','vaen'],
      L1+'GENESIS_CARDS.md':['six Foundational','not a solved implementation','zero single-basin Foundational','disjoint sets','no aen Card boost','Black Card retirement'],
      L1+'FATIGUE_AND_CROSS_INTERFACE_CONCURRENCY.md':['does not itself incur basin-extraction fatigue','does not establish elimination','Selective','OPEN'],
      'BOOKS/RED/ARCS/ARC_003/ARC.md':['Day 63','first Chainmail Robe commission','1,550','850 + 150 + 300 + 250','working','Vintage 137 is a proposal','wearable without underclothes','Blacksmith’s Row'],
      REPORT+'SHAPINGS_MIGRATION_PLAN.md':['PT-0001','PT-0002','PT-0003','SE-0001','source_id','interface metadata','not executed','zero single-basin Foundational'],
      REPORT+'OPEN_ISSUES.md':['Do not commit or push until user explicitly approves','Selective discharge','White raw crystal mass','not claimed']}
    for p,terms in texts.items():
        t=cur(p).replace('*','').casefold()
        for term in terms:need(term.casefold() in t,'Scope '+p+' / '+term)
    cross=cur(REPORT+'REVERSE_DIFF.md')
    need(len(re.findall(r'^\| P015-\d+ \|',cross,re.M))==20,'Crosswalk coverage')
    need(850+150+300+250==1550 and 6*100==600,'Retail/capital arithmetic')
    git('diff','--check',BASE);git('diff','--cached','--check');git('check-ignore','-q','_inbox/test.zip')
    return {'status':'PASS','baseline':BASE,'prior_files_preserved':len(prior),'prior_files_byte_identical':len(prior)-len(changed),'prior_checkpoint_workshop_files_byte_identical':history,'added':len(additions),'modified':len(changed),'deleted':0,'protected_owner_and_image_count':len(protected),'current_local_links':links,'reverse_diff_topics':20,'source_leaves':77,'reused_006_leaves':20,'new_source_leaves':57,'blocking_conflicts':[],'changes':sorted(additions|changed),'literal_transcript_complete':False}
def validate_reports(root,result):
    def read(p):return json.loads((root/REPORT/p).read_text(encoding='utf8'))
    receipt=read('VALIDATION.json')
    for k in result:need(receipt[k]==result[k],'Validation receipt drift: '+k)
    need(receipt['structural_regression']['status']=='PASS','Structural regression receipt')
    paths=read('CHANGED_PATHS.json')
    need(paths['baseline']==BASE and paths['deleted']==[] and set(paths['added'])|set(paths['modified'])==EXPECTED,'Changed-path receipt')
    need(len(paths['added'])==68 and len(paths['modified'])==14,'Change counts')
    manifest=read('CHANGED_FILES_SHA256.json')
    need(set(manifest['files'])==EXPECTED-{REPORT+'CHANGED_FILES_SHA256.json'},'Hash manifest coverage')
    for p,entry in manifest['files'].items():
        b=(root/p).read_bytes()
        need(sha(b)==entry['sha256'] and len(b)==entry['bytes'],'Reviewed hash drift: '+p)
    return {'status':'PASS','changed_paths':len(EXPECTED),'file_hashes':len(manifest['files']),'self_reference_excluded':REPORT+'CHANGED_FILES_SHA256.json'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--root',type=Path);p.add_argument('--check-reports',action='store_true');a=p.parse_args()
    inv=inspect_package(a.archive)
    result={'status':'PASS','archive_sha256':inv['archive_sha256'],'archive_count':len(inv['archives']),'declared_hashes':inv['declared_hashes'],'unlisted_nested_members':inv['unlisted_nested_members'],'numbers':numeric(inv)}
    if a.root:result['repository']=validate_repository(a.root,inv)
    if a.check_reports:
        need(a.root is not None,'--check-reports requires --root')
        result['report_integrity']=validate_reports(a.root,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
