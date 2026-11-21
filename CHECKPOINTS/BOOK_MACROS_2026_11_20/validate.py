"""Read-only validation of four complete macro payloads and scoped integration."""
import argparse,hashlib,json,posixpath,re,subprocess
from pathlib import Path
from urllib.parse import unquote

BASE='6d1010357e0499887b23dda9a0b4db361c79ed71'
C='CHECKPOINTS/BOOK_MACROS_2026_11_20';P='PROVENANCE/WORKSHOP/BOOK_MACROS_2026_11_20'
BOOKS=['ORANGE','YELLOW','GREEN','BLUE'];COLORS='Red Orange Yellow Green Blue Violet White'.split()
FIELDS=['Arc identity','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies','Status']
L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION';L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS';L4='WORLD_CLOCK/L4_NARRATIVE_REALIZATION'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--git',default='git');ap.add_argument('--report',type=Path);a=ap.parse_args();r=a.root.resolve();checks=[]
    def ck(v,label):checks.append({'check':label,'pass':bool(v)})
    def b(p):return (r/p).read_bytes()
    def t(p):return (r/p).read_text(encoding='utf-8')
    def sha(v):return hashlib.sha256(v).hexdigest()
    def git(*args):return subprocess.check_output([a.git,*args],cwd=r)
    def old(p):return git('show',BASE+':'+p)
    baseline={l.split('\t',1)[1]:l.split()[2] for l in git('ls-tree','-r',BASE).decode().splitlines()}
    def sameblob(path):
        data=b(path);return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==baseline[path]
    expected=set(json.loads(t(C+'/EXPECTED_CHANGES.json')))
    actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    ck(actual==expected,'exact reviewed path set; no unrelated changes')
    ck(not git('diff','--name-only','--diff-filter=D',BASE).strip(),'no deleted baseline files')
    ck(all(not p.startswith(('_inbox/','.git/')) for p in expected),'no inbox or Git metadata staged')
    # Existing owners are additive in full; bookkeeping preserves all prior registry data.
    for p in sorted(expected & set(baseline)):
        before=old(p)
        if p=='PROVENANCE/SOURCE_REGISTRY.json':
            x=json.loads(before);y=json.loads(t(p));olditems=x.pop('subsequent_deliveries');newitems=y.pop('subsequent_deliveries');ck(x==y and newitems[:len(olditems)]==olditems and len(newitems)==len(olditems)+4,'source registry preserves prior data and adds four deliveries')
        else:ck(before.decode() in t(p),'entire earlier text retained '+p)
        if p not in ['.gitattributes','PROVENANCE/SOURCE_REGISTRY.json']:ck(b(P+'/BASELINE/'+p)==before,'exact baseline snapshot '+p)
    protected=[p for p in baseline if p.startswith(('BOOKS/RED/','BOOKS/VIOLET/','BOOKS/WHITE/','PROVENANCE/WORKSHOP/','CHECKPOINTS/'))]
    for p in protected:ck(sameblob(p),'unchanged protected bytes '+p)
    ck(sameblob('CONTINUITY/RED_RUNNING_DAY_LEDGER.md'),'complete Day 0–1637 ledger unchanged')
    ck(sameblob('WORLD_CLOCK/L1_FANTASY/OPERATIONAL_DOMAINS.md'),'existing operational taxonomy unchanged')
    ck(not any(p.startswith(('AERA/','MK147/','MK727/','_bricked/')) for p in expected),'no inherited repository copy or mutation')
    mapping=json.loads(t(P+'/SOURCE_MAP.json'))['files'];lookup={(e['book'],e['source']):e for e in mapping}
    ck(len(mapping)==20,'all 20 original files mapped')
    hashes=0
    for e in mapping:ck(sha(b(e['target']))==e['sha256'] and len(b(e['target']))==e['bytes'],'exact source bytes '+e['book']+'/'+e['source'])
    for book in BOOKS:
        mf='MANIFEST.json' if book=='ORANGE' else 'MANIFEST_SHA256.json';m=json.loads(t(P+'/'+book+'/'+mf))
        ck(set(m['files'])|{mf}=={e['source'] for e in mapping if e['book']==book},book+' full manifest inventory')
        for name,digest in m['files'].items():ck(sha(b(lookup[(book,name)]['target']))==digest,book+' manifest '+name);hashes+=1
    ck(hashes==16,'16 manifest payload hashes')
    arc_count=0;macro_sections={}
    for book in BOOKS:
        macro=f'BOOKS/{book}/BOOK_MACRO_OUTLINE.md';source=t(P+'/'+book+f'/BOOK_{book}_MACRO_OUTLINE.md')
        ck(source in t(macro),book+' complete macro text retained without shortening')
        headers=re.findall(r'^## ((?:Red|Orange|Yellow|Green|Blue|Violet|White) Arc[^\n]*)$',t(macro),re.M)
        ck([h.split()[0] for h in headers]==COLORS,book+' seven-color macro order')
        ck(len(list((r/'BOOKS'/book/'ARCS').glob('ARC_*/ARC.md')))==7,book+' exactly seven current arc contracts')
        for i,color in enumerate(COLORS,1):
            path=f'BOOKS/{book}/ARCS/ARC_{i:03d}/ARC.md';s=t(path);arc_count+=1
            ck(re.findall(r'^## (.*)$',s,re.M)==FIELDS,path+' eight constitutional fields')
            ck(f'MK163-{book}-ARC-{i:03d}' in s,path+' correct stable identity')
            ck('calendar dates' in s and 'OPEN' in s and 'Outlined at macro level' in s,path+' macro-only status')
            ck(not re.search(r'\bDay \d+|\bChapter \d+',s),path+' no new calendar/chapter assignment')
            m=re.search(r'^## '+re.escape(headers[i-1])+r'\n(.*?)(?=^## |\Z)',t(macro),re.M|re.S);macro_sections[(book,color)]=m.group(1)
        ck(not list((r/'BOOKS'/book).rglob('CHAPTER*')),book+' no invented chapter files')
    def includes(book,color,phrases):
        s=macro_sections[(book,color)]
        for phrase in phrases:ck(phrase in s,f'{book} {color} selected scope: {phrase}')
    includes('ORANGE','Red',['vaelum disbands','eight trained blacksmiths','ransom was PAID','NOT slave trafficking'])
    includes('ORANGE','Orange',['No bond yet','several dungeon delves'])
    includes('ORANGE','Yellow',['bonds with the Black Vaelith'])
    includes('ORANGE','Green',['investigating the repeated kidnapping/ransom'])
    includes('ORANGE','Blue',['without joining a permanent vaelum','need not be connected'])
    includes('ORANGE','Violet',['Yellow-ranked','informant','Do not assume the noble controls'])
    includes('ORANGE','White',['cartel is dismantled','power vacuum','Kidnapping and ransom do not end'])
    includes('YELLOW','Orange',['every five years','six or seven','six chromatic realms','cannot ordinarily enter other chromatic realms'])
    includes('YELLOW','Yellow',['Red Black Dragon egg','Do not assert a fully grown'])
    includes('YELLOW','Green',['three semesters','regular ELDRIS/Domai military branch','NOT Special Projects','graduates'])
    includes('YELLOW','Blue',['first operational entry into a Domai'])
    includes('YELLOW','Violet',['merged Domai engagement','do not invent'])
    includes('YELLOW','White',['possible, not yet specified','recruited to the Crown/kingdom\'s Special Projects'])
    includes('GREEN','Green',['Former Blue Arc training is consolidated into Green','independent repeated Violet Dungeon delves','interview Kaira','does not travel to the Violet Realm'])
    includes('GREEN','Blue',['Former Violet Arc moves to Blue','merchant city-states'])
    includes('GREEN','Violet',['move to Violet','helps defeat','merged Domai','distinct from Book Yellow'])
    includes('GREEN','White',['continent-wide disruption','without eliminating','Book Blue milestone'])
    includes('BLUE','Red',['only by her living Black Unicorn','No Primordial bond yet'])
    includes('BLUE','Orange',['Three Domai','coordinated division','No Yellow Realm expedition'])
    includes('BLUE','Yellow',['fifth Black bond','geode/crystalline egg-like','stay in the White Realm'])
    includes('BLUE','Green',['floating fortresses','not transferred to the navy','Do not place the central resource-island'])
    includes('BLUE','Blue',['central pink-marked region','primary operational role is land-based'])
    includes('BLUE','Violet',['numbered 1','2 and 3','independent political territories','automatic abolition'])
    includes('BLUE','White',['circled in red','collective infrastructure','Cabal of Maegi','interrogated','centuries','manipulating','do not resolve the Cabal'])
    economy=t(L2+'/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md').split('## Earlier record')[0]
    ck(all(x in economy for x in ['26 assemblers','**78','conditional capacity 24','not guaranteed sales','No new rent']), 'enterprise capacity and financial boundaries')
    ck(18+8==26 and 54+8*3==78,'enterprise arithmetic')
    military=t(L2+'/INSTITUTIONS/CROWN_MILITARY_AND_SPECIAL_PROJECTS.md')
    ck(all(x in military for x in ['regular branch','only in White','independent command','Crown Intelligence','not transferred to the navy','not** a Special Projects operative']),'institutional distinctions and illi role')
    for p in [L2+'/HOSTILE_ORGANIZATIONS/CABAL_OF_ASH_AND_CROWN.md',L4+'/ANTAGONIST_VISIBILITY.md']:
        s=t(p).split('## Earlier record')[0];ck('Maegi' in s and ('manipulat' in s) and 'Blue' in s and 'White' in s,p+' established scoped revelation')
    ck('world-domination' in t(L2+'/HOSTILE_ORGANIZATIONS/CABAL_OF_ASH_AND_CROWN.md') or 'world domination' in t(L2+'/HOSTILE_ORGANIZATIONS/CABAL_OF_ASH_AND_CROWN.md'),'Cabal goal preserved')
    mapfile='BOOKS/BLUE/REFERENCE_ASSETS/PIRATE_MAP_AUTHOR_ANNOTATED.jpg';ck(sha(b(mapfile))=='a792a7959541505aa8fc62d213e60e98387a1ec257560d387b669fe53e896057','original annotated map hash')
    ck(sum(e['target']==mapfile for e in mapping)==1,'one mapped original image')
    ck(len(json.loads(t(C+'/COVERAGE.json'))['topics'])==41,'41 coverage topics')
    # New local Markdown links and anchors. Historical source links are not rewritten.
    link_count=0
    def anchors(text):
        used={};out=set()
        for h in re.findall(r'^#{1,6} (.*)$',text,re.M):
            slug=re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-');num=used.get(slug,0);used[slug]=num+1;out.add(slug+('-'+str(num) if num else ''))
        return out
    for path in sorted(expected):
        if not path.endswith('.md') or path.startswith(P+'/'):continue
        text=t(path).split('## Earlier record')[0]
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('https:','http:','mailto:')):continue
            file,_,anchor=unquote(target).partition('#');dest=(r/path).parent.joinpath(file).resolve() if file else r/path
            link_count+=1;ck(dest.exists(),path+' target '+target)
            if anchor and dest.is_file() and dest.suffix=='.md':ck(anchor in anchors(dest.read_text(encoding='utf-8')),path+' anchor '+anchor)
    for p in expected:
        if p.endswith('.md') and not p.startswith(P+'/'):
            active=t(p).split('## Earlier record')[0]
            # A correction may quote the forbidden form, so only affirmative active variants are checked.
            ck(not re.search(r'\bCabal of Magi\b|\bPrincess Illi\b|\bPrincess Aina\b|\bKira\b',active),'protected active spellings '+p)
    result={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','baseline':BASE,'check_count':len(checks),'failures':[x['check'] for x in checks if not x['pass']],'counts':{'packages':4,'source_files':20,'payload_hashes':hashes,'complete_macros':4,'arc_contracts':arc_count,'coverage_topics':41,'local_links_checked':link_count,'expected_changed_paths':len(expected)},'preservation':'All earlier text retained in changed owners; Book Red/daily ledger, Violet/White books and historical sources remain unchanged.','scope':'Complete supplied macro checkpoints; no literal workshop transcript or full manuscript claim. Referenced Kingdoms map identity remains pending recovery.'}
    if a.report:a.report.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(result,ensure_ascii=False,indent=2));return result['status']!='PASS'
if __name__=='__main__':raise SystemExit(main())
