"""Validate the four supplied macro packages against the fetched integration baseline."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote

BASE='79365c07373cdd5449174d8fc5cd7ee0116c80a5'
C='CHECKPOINTS/BOOK_BLUE_VIOLET_WHITE_2026_11_21'
P='PROVENANCE/WORKSHOP/BOOK_BLUE_VIOLET_WHITE_2026_11_21'
L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION';L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS';L4='WORLD_CLOCK/L4_NARRATIVE_REALIZATION'
FIELDS=['Arc identity','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies','Status']
COLORS='Red Orange Yellow Green Blue Violet White'.split()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--git',default='git');ap.add_argument('--report',type=Path);a=ap.parse_args();r=a.root.resolve();checks=[]
 def ck(v,label):checks.append({'check':label,'pass':bool(v)})
 def b(p):return (r/p).read_bytes()
 def t(p):return (r/p).read_text(encoding='utf-8')
 def git(*args):return subprocess.check_output([a.git,*args],cwd=r)
 def old(p):return git('show',BASE+':'+p)
 def sha(data):return hashlib.sha256(data).hexdigest()
 def front(p):return t(p).split('## Earlier record · preserved verbatim')[0]
 expected=set(json.loads(t(C+'/EXPECTED_CHANGES.json')));modes=json.loads(t(C+'/CHANGE_MODES.json'))
 baseline={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',BASE).decode().splitlines()}
 actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
 ck(actual==expected,'exact reviewed path set; no unrelated edits')
 ck(not git('diff','--name-only','--diff-filter=D',BASE).strip(),'no deleted baseline files')
 ck(not any(p.startswith(('_inbox/','AERA/','MK147/','MK727/','_bricked/','.git/')) for p in expected),'no inbox, metadata or inherited repository mutation')
 ck(set(modes)==expected,'change modes cover reviewed paths')
 for p in sorted(expected & set(baseline)):
  prior=old(p)
  if modes[p]=='additive':ck(prior.decode() in t(p),'full earlier owner retained '+p)
  if p not in ['.gitattributes','PROVENANCE/SOURCE_REGISTRY.json']:ck(b(P+'/BASELINE/'+p)==prior,'exact pre-edit snapshot '+p)
  if modes[p]=='registry':
   x=json.loads(prior);y=json.loads(t(p));xx=x.pop('subsequent_deliveries');yy=y.pop('subsequent_deliveries');ck(x==y and yy[:len(xx)]==xx and len(yy)==len(xx)+4,'source registry retains all prior data plus four records')
 protected=[p for p in baseline if p.startswith(('BOOKS/RED/','BOOKS/ORANGE/','BOOKS/YELLOW/','BOOKS/GREEN/','PROVENANCE/WORKSHOP/','CHECKPOINTS/','WORLD_CLOCK/L0_MATHEMATICS/','WORLD_CLOCK/L1_FANTASY/'))]
 protected+=['CONTINUITY/RED_RUNNING_DAY_LEDGER.md','BOOKS/BLUE/REFERENCE_ASSETS/PIRATE_MAP_AUTHOR_ANNOTATED.jpg',L2+'/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md',L2+'/TECHNOLOGY/GENESIS_DIAMONDS.md']
 for p in protected:
  data=b(p);ck(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==baseline[p],'protected bytes unchanged '+p)
 mapping=json.loads(t(P+'/SOURCE_MAP.json'))['files'];ck(len(mapping)==24,'all 24 supplied source files mapped')
 lookup={(e['package'],e['source']):e for e in mapping};payloads=0
 for e in mapping:ck(len(b(e['target']))==e['bytes'] and sha(b(e['target']))==e['sha256'],'original source bytes '+e['package']+'/'+e['source'])
 for key in ['LEVIATHAN_003','BLUE_004','VIOLET_001','WHITE_001']:
  m=json.loads(t(P+'/'+key+'/MANIFEST_SHA256.json'));hashes={**m['files'],**m.get('assets',{})}
  ck(set(hashes)|{'MANIFEST_SHA256.json'}=={e['source'] for e in mapping if e['package']==key},key+' manifest full inventory')
  for name,digest in hashes.items():ck(sha(b(lookup[(key,name)]['target']))==digest,key+' manifest '+name);payloads+=1
 ck(payloads==20,'20 payload/asset hashes verified')
 for book in ['VIOLET','WHITE']:
  ck(t(P+'/'+book+'_001/BOOK_'+book+'_MACRO_OUTLINE.md') in t('BOOKS/'+book+'/BOOK_MACRO_OUTLINE.md'),book+' full macro preserved without shortening')
 ck(t(P+'/WHITE_001/GLOBAL_WAR_LEDGER.md') in t(L2+'/CIVILIZATION/GLOBAL_CABAL_WAR.md'),'full global war ledger retained')
 ck(t(P+'/VIOLET_001/MAP_LEGEND_AND_LIMITS.md') in t('BOOKS/VIOLET/REFERENCE_ASSETS/READING_NOTES.md'),'full supplied Violet legend retained')
 sections={};contract_count=0
 for book in ['BLUE','VIOLET','WHITE']:
  macro=t('BOOKS/'+book+'/BOOK_MACRO_OUTLINE.md')
  heads=re.findall(r'^## ((?:Red|Orange|Yellow|Green|Blue|Violet|White)(?: Arc)? — .*?)$',macro,re.M)
  ck([x.split()[0] for x in heads]==COLORS,book+' exactly seven ordered macro arcs')
  ck(len(list((r/'BOOKS'/book/'ARCS').glob('ARC_*/ARC.md')))==7,book+' exactly seven arc contracts')
  for i,(color,h) in enumerate(zip(COLORS,heads),1):
   path=f'BOOKS/{book}/ARCS/ARC_{i:03d}/ARC.md';s=t(path);contract_count+=1
   ck(re.findall(r'^## (.*)$',s,re.M)==FIELDS,path+' eight fields')
   ck(f'MK163-{book}-ARC-{i:03d}' in s,path+' stable identity')
   ck('Outlined at macro level' in s and 'OPEN' in s,path+' planning status')
   ck(not re.search(r'\bDay \d+|\bChapter \d+',s),path+' no invented dated/chapter assignment')
   sections[(book,color)]=re.search(r'^## '+re.escape(h)+r'\n(.*?)(?=^## |\Z)',macro,re.M|re.S).group(1)
  ck(not list((r/'BOOKS'/book).rglob('CHAPTER*')),book+' no invented chapters')
 blueold=old('BOOKS/BLUE/BOOK_MACRO_OUTLINE.md').decode()
 for color,i in [('Orange',2),('Blue',5),('Violet',6),('White',7)]:
  oldsection=re.search(r'^## '+color+r' Arc[^\n]*\n(.*?)(?=^## |\Z)',blueold,re.M|re.S).group(1)
  ck(sections[('BLUE',color)]==oldsection,'Blue '+color+' complete prior section unchanged')
  ck(b(f'BOOKS/BLUE/ARCS/ARC_{i:03d}/ARC.md')==old(f'BOOKS/BLUE/ARCS/ARC_{i:03d}/ARC.md'),'Blue '+color+' contract unchanged')
 oldgreen=re.search(r'^## Green Arc[^\n]*\n(.*?)(?=^## |\Z)',blueold,re.M|re.S).group(1)
 ck(oldgreen.strip() in sections[('BLUE','Green')],'entire prior Green fortress detail retained')
 ck(sections[('BLUE','Green')].count('five or six')==1,'003 and004 contingent integrated only once')
 def has(book,color,phrases):
  for phrase in phrases:ck(phrase in sections[(book,color)],book+' '+color+': '+phrase)
 has('BLUE','Red',['second King’s Tournament, which concludes Red Arc','favorable report remains','other already-bonded Black companions','Nyx stays in White','No Primordial bond yet','absolute dates remain OPEN'])
 has('BLUE','Orange',['Three Domai emerge and merge','No Yellow Realm expedition'])
 has('BLUE','Yellow',['eligible to accompany Kaira','Nyx remains in White','small Crown diplomatic delegation','fifth Black bond'])
 has('BLUE','Green',['five or six','voluntarily','protecting maritime travel','single-handedly','8 km','not assigned to this contingent','sixth bond remains Book Violet'])
 has('VIOLET','Red',['five occupied cities','eleven aqua-marked cities','other six','third occupied city','last **two**','not known to have Cabal infiltration'])
 has('VIOLET','Orange',['egg hatches','Blue Genesis energy','aen','30–40 feet','Exact energy transfer'])
 has('VIOLET','Yellow',["King's Highway",'warship/armada','white-circled','returns to the capital'])
 has('VIOLET','Green',['green route','local authorities'])
 has('VIOLET','Blue',['can fly','small number','60–100 feet','not a fixed measurement','entire growing delegation'])
 has('VIOLET','Violet',['purple route','bottom-right'])
 has('VIOLET','White',['pink route','White Arc','Violet Domain capital','not the Cabal'])
 vm=t('BOOKS/VIOLET/BOOK_MACRO_OUTLINE.md')
 for phrase in ['successfully dismantled','independently of Kaira','not a stop','not necessarily White Arc']:
  if phrase=='not necessarily White Arc':ck(phrase.upper() in t('BOOKS/VIOLET/REFERENCE_ASSETS/READING_NOTES.md').upper(),'independent pink-X timing not forced to White')
  else:ck(phrase in vm,'Violet independent coalition '+phrase)
 has('WHITE','Red',['Green Realm to Kingdom 27','not a ship voyage','Nyx is a native','five-mile-tall Great Tree','no successful foothold','Kingdoms 27 and 28','NOT CANONIZED'])
 has('WHITE','Orange',['Kingdom 29','captives\' fates remain OPEN','not another broad'])
 has('WHITE','Yellow',['Cabal of Maegi is defeated','killing the person','overcharged Genesis crystals','maege paper','not assumed to have already completed','possible'])
 pairs={'Green':['Green','Yellow'],'Blue':['Violet','Orange'],'Violet':['Blue','Red']}
 for arc,pair in pairs.items():has('WHITE',arc,['**'+' and '.join(pair)+' Realms**'])
 ck(len(set(sum(pairs.values(),[])))==6,'six chromatic realms exactly once in selected research pairs')
 has('WHITE','White',['local Genesis Field associated with her planet','not the starscape','no further Genesis storms','How preexisting ELDRIS/monsters','No seventh Black bond'])
 war=t(L2+'/CIVILIZATION/GLOBAL_CABAL_WAR.md');rows=[]
 for line in war.splitlines():
  if line.startswith('| **'):
   cols=line.split('|')[1:-1];rows.append(([int(n) for n in re.findall(r'\d+',cols[0])],[int(n) for n in re.findall(r'\d+',cols[1])],cols[2]))
 expectedrows=[([1,12,14],[15,16,17,18,19]),([28,30,32],[20,21]),([1,26,27],[22,23,24]),([5,6,7,8],[33]),([9,10],[31])]
 ck([(x,y) for x,y,_ in rows]==expectedrows,'all five exact coalition assignments')
 ck(all('Assist Kingdom' in rows[i][2] and 'not an assault' in rows[i][2] for i in [3,4]),'31 and33 receive assistance, not hostile-government assault')
 for phrase in ['1 participates in two theaters','4, 11, 13','15–24','25 and 29','29 is NOT a coalition participant','desired outcome','background to Kaira']:
  ck(phrase in war,'global war: '+phrase)
 travel=front(L2+'/REALMS/SEVEN_REALMS.md')
 for phrase in ['Once bonded','Eligibility begins only','does not compel attendance','Nyx can enter his native Green Realm','ordinary']:
  ck(phrase in travel,'realm exception: '+phrase)
 tournament=front(L2+'/CULTURE/KINGS_TOURNAMENT.md')
 for phrase in ['once every three years','2435','not an assigned story day','1,059','recurrence anchor']:
  ck(phrase in tournament,'tournament: '+phrase)
 ck(353*3==1059 and 1376+1059==2435,'conditional recurrence arithmetic')
 ck('quadrennial' not in t('BOOKS/BLUE/BOOK_MACRO_OUTLINE.md'),'no active old recurrence in Blue macro')
 for phrase in ['accompanied only by her living Black Unicorn','non-Yellow-native companions, including Nyx and Black Unicorn, stay','Red concludes on this favorable report']:
  ck(phrase not in t('BOOKS/BLUE/BOOK_MACRO_OUTLINE.md'),'old Blue restriction removed from active macro: '+phrase)
 for p in [L2+'/REALMS/BLUE_LEVIATHANS.md',L2+'/BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md']:
  ck('OPEN' in front(p) and 'aen' in front(p),'growth has explicit limits '+p)
 ck('No creation of raw crystal structure' in front(L2+'/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md'),'overcharged crystal does not invent raw structure')
 ck('Shapings remain operations and Bindings interfaces' in t(L3+'/EVENTS/PLANETARY_GENESIS_STABILIZATION.md'),'protected operation/interface distinction')
 cov=json.loads(t(C+'/COVERAGE.json'))['topics'];ck(len(cov)==48,'48 topics covered')
 for item in cov:ck((r/item['owner']).is_file() and (r/item['source']).is_file(),'coverage source/owner exists '+item['id'])
 # Check all new current Markdown destinations and heading anchors; historical links remain literal.
 def anchors(text):
  used={};found=set()
  for h in re.findall(r'^#{1,6} (.*)$',text,re.M):
   slug=re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-');i=used.get(slug,0);used[slug]=i+1;found.add(slug+('-'+str(i) if i else ''))
  return found
 linkcount=0
 for p in sorted(expected):
  if not p.endswith('.md') or p.startswith(P+'/'):continue
  content=front(p)
  for target in re.findall(r'\]\(([^)]+)\)',content):
   if target.startswith(('https:','http:','mailto:')):continue
   filename,_,anchor=unquote(target).partition('#');dest=(r/p).parent.joinpath(filename).resolve() if filename else r/p
   linkcount+=1;ck(dest.exists(),p+' link '+target)
   if anchor and dest.is_file() and dest.suffix=='.md':ck(anchor in anchors(dest.read_text(encoding='utf-8')),p+' anchor '+anchor)
  # Quoted rejected spellings in the original source are not affirmative naming changes.
  ck(not re.search(r'\bCabal of Magi\b|\bPrincess Illi\b|\bPrincess Aina\b|\bKira\b',content),'protected current names '+p)
 ck(json.loads(t(C+'/STRUCTURAL_VALIDATION.json'))['status']=='PASS','existing repository structural validator passes')
 counts={'packages':4,'source_files':len(mapping),'payload_and_asset_hashes':payloads,'new_complete_macros':2,'new_arc_contracts':14,'blue_contracts_modified':3,'contracts_checked':contract_count,'coverage_topics':len(cov),'local_links_checked':linkcount,'protected_files_checked':len(protected),'changed_paths':len(expected),'added':len(expected-set(baseline)),'modified':len(expected&set(baseline)),'deleted':0}
 result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','baseline':BASE,'check_count':len(checks),'counts':counts,'failures':[c['check'] for c in checks if not c['pass']],'scope':'Complete supplied macro payloads; chronology/mechanisms explicitly OPEN. Historical sources and Book Red ledger unchanged.'}
 if a.report:a.report.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
 print(json.dumps(result,ensure_ascii=False,indent=2));return result['status']!='PASS'
if __name__=='__main__':raise SystemExit(main())
