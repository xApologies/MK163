"""Validate source fidelity, author-note placement and scoped realm-arc reconciliation."""
import argparse,ast,hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote

BASE='f4b7064cb403204e16601e0c438cdf2d5124788a'
C='CHECKPOINTS/CHROMATIC_REALM_ARCS_2026_11_23';P='PROVENANCE/WORKSHOP/CHROMATIC_REALM_ARCS_2026_11_23'
L1='WORLD_CLOCK/L1_FANTASY';L2='WORLD_CLOCK/L2_WORLD_CIVILIZATION';L3='WORLD_CLOCK/L3_CHARACTERS_EVENTS'
MARKER='<!-- MK163_CHROMATIC_REALM_DELTA_2026_11_23 -->'
FIELDS=['Arc identity','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies','Status']
COLORS='Red Orange Yellow Green Blue Violet White'.split()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--git',default='git');ap.add_argument('--report',type=Path);a=ap.parse_args();r=a.root.resolve();checks=[]
 def ck(v,n):checks.append({'check':n,'pass':bool(v)})
 def b(p):return (r/p).read_bytes()
 def t(p):return (r/p).read_text(encoding='utf-8')
 def front(p):return t(p).split('## Earlier record · preserved verbatim')[0]
 def git(*args):return subprocess.check_output([a.git,*args],cwd=r)
 def old(p):return git('show',BASE+':'+p)
 def sha(data):return hashlib.sha256(data).hexdigest()
 baseline={x.split('\t',1)[1]:x.split()[2] for x in git('ls-tree','-r',BASE).decode().splitlines()}
 expected=set(json.loads(t(C+'/EXPECTED_CHANGES.json')));modes=json.loads(t(C+'/CHANGE_MODES.json'))
 actual=set(git('diff','--name-only',BASE).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
 ck(actual==expected,'exact reviewed changes; no unrelated files');ck(set(modes)==expected,'change-mode inventory complete')
 ck(not git('diff','--name-only','--diff-filter=D',BASE).strip(),'no deleted files')
 ck(not any(p.startswith(('_inbox/','.git/','AERA/','MK147/','MK727/','_bricked/','BOOKS/RED/','BOOKS/WHITE/')) for p in expected),'no inbox/upstream/Book Red/Book White edits')
 def retained_lines(before,after):
  it=iter(after.splitlines());return all(any(x==line for x in it) for line in before.splitlines())
 for p in sorted(expected&set(baseline)):
  prior=old(p)
  if p not in ['.gitattributes','PROVENANCE/SOURCE_REGISTRY.json']:ck(b(P+'/BASELINE/'+p)==prior,'exact baseline snapshot '+p)
  if p=='PROVENANCE/SOURCE_REGISTRY.json':
   x=json.loads(prior);y=json.loads(t(p));xx=x.pop('subsequent_deliveries');yy=y.pop('subsequent_deliveries');ck(x==y and yy[:len(xx)]==xx and len(yy)==len(xx)+1,'registry retains all data plus one delivery')
  elif '/ARCS/ARC_' not in p:ck(retained_lines(prior.decode(),t(p)),'all prior owner lines retained in order '+p)
 protected=[p for p in baseline if p.startswith(('BOOKS/RED/','BOOKS/WHITE/','PROVENANCE/WORKSHOP/','CHECKPOINTS/','WORLD_CLOCK/L0_MATHEMATICS/')) or p.lower().endswith(('.png','.jpg','.jpeg','.gif','.pdf','.zip'))]
 protected+=['CONTINUITY/RED_RUNNING_DAY_LEDGER.md',L1+'/TRANSDUCTION_LIFECYCLE.md',L2+'/REALMS/SEVEN_REALMS.md',L2+'/CULTURE/KINGS_TOURNAMENT.md',L2+'/TECHNOLOGY/GENESIS_DIAMONDS.md',L2+'/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md',L3+'/EVENTS/PLANETARY_GENESIS_STABILIZATION.md']
 for p in sorted(set(protected)):
  data=b(p);ck(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==baseline[p],'protected bytes unchanged '+p)
 mapping=json.loads(t(P+'/SOURCE_MAP.json'));ck(len(mapping['files'])==3,'all three original files retained')
 ck('No publisher' in mapping['manifest_status'],'publisher-manifest absence explicit')
 for e in mapping['files']:ck(sha(b(e['target']))==e['sha256'] and len(b(e['target']))==e['bytes'],'source byte hash '+e['source'])
 script=t(P+'/ORIGINAL/apply_update.py');nodes=ast.parse(script).body
 vals={n.targets[0].id:ast.literal_eval(n.value) for n in nodes if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['entries','arc_notes']}
 entries=vals['entries'];notes=vals['arc_notes'];notes_total=0
 for path,items in entries.items():
  for heading,note in items:
   text=t(path);ck(note in text,'exact supplied note '+path+' '+heading);notes_total+=1
   m=re.search(r'^'+re.escape(heading)+r'[^\n]*\n(.*?)(?=^## |\Z)',text,re.M|re.S)
   ck(m is not None and note in m.group(1),'correct owning heading '+path+' '+heading)
  ck(t(path).count(MARKER)==len(items),'no duplicate author markers '+path)
 for path,note in notes.items():
  ck('**Author-selected chromatic realm event · 2026-11-23:** '+note in t(path),'exact arc note '+path);notes_total+=1
  ck(t(path).count(MARKER)==1,'one arc marker '+path)
 ck(notes_total==17 and len(set(entries)|set(notes))==14,'17 original notes in14 targets')
 ck(len(json.loads(t(C+'/COVERAGE.json'))['topics'])==notes_total,'coverage inventory accounts for every exact note')
 result=subprocess.run([__import__('sys').executable,str(r/P/'ORIGINAL/apply_update.py'),'--repo',str(r),'--check'],capture_output=True,text=True)
 ck(result.returncode==0 and 'WOULD UPDATE 0 files:' in result.stdout,'supplied script idempotent after full reconciliation')
 sections={};contracts=0
 def splitfields(s):return {h:body for h,body in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',s,re.M|re.S)}
 allow={('ORANGE',1):['Major events','Dependencies'],('ORANGE',3):['Major events','Principal conflict','Exit state','Dependencies'],('YELLOW',3):['Major events','Principal conflict','Exit state','Dependencies'],('YELLOW',4):['Principal conflict','Dependencies'],('GREEN',4):['Major events','Entry state','Principal conflict','Dependencies'],('BLUE',1):['Major events','Dependencies'],('BLUE',3):['Major events','Exit state','Dependencies'],('VIOLET',2):['Major events','Principal conflict','Dependencies']}
 for book in ['ORANGE','YELLOW','GREEN','BLUE','VIOLET']:
  path='BOOKS/'+book+'/BOOK_MACRO_OUTLINE.md';s=t(path);before=old(path).decode()
  headers=re.findall(r'^## ((?:Red|Orange|Yellow|Green|Blue|Violet|White)(?: Arc)?(?: — [^\n]+)?)$',s,re.M)
  ck([h.split()[0] for h in headers]==COLORS,book+' seven ordered arc headings')
  ck(re.findall(r'^## .+$',s,re.M)==re.findall(r'^## .+$',before,re.M),book+' all existing macro headings preserved')
  for i,(color,h) in enumerate(zip(COLORS,headers),1):
   sections[(book,color)]=re.search(r'^## '+re.escape(h)+r'\n(.*?)(?=^## |\Z)',s,re.M|re.S).group(1)
   cp=f'BOOKS/{book}/ARCS/ARC_{i:03d}/ARC.md';ct=t(cp);fields=splitfields(ct);oldfields=splitfields(old(cp).decode());contracts+=1
   ck(list(fields)==FIELDS,cp+' eight constitutional fields')
   ck(f'MK163-{book}-ARC-{i:03d}' in ct,cp+' stable ID')
   ck('Outlined at macro level' in ct and 'OPEN' in ct,cp+' macro-only status')
   ck(not re.search(r'\bDay \d+|\bChapter \d+',ct),cp+' no date/chapter invention')
   for field in FIELDS:
    if field not in allow.get((book,i),[]):ck(fields[field]==oldfields[field],cp+' unrelated field unchanged: '+field)
   if 'Major events' in allow.get((book,i),[]):ck(oldfields['Major events'].strip() in fields['Major events'],cp+' complete old major-events reference retained')
  current={p.relative_to(r).as_posix() for p in (r/'BOOKS'/book/'ARCS').rglob('*') if p.is_file()}
  prev={p for p in baseline if p.startswith('BOOKS/'+book+'/ARCS/')}
  ck(current==prev,book+' no new arc/chapter files')
 def contains(book,color,phrases):
  for phrase in phrases:ck(phrase in sections[(book,color)],book+' '+color+': '+phrase)
 contains('ORANGE','Red',['already bonded','Princess illi','not a transfer, abandonment or new bond','returns with her'])
 contains('ORANGE','Yellow',['not an anatomical heart','condition for consenting','reciprocal amplification','saves the city','not a natural velis'])
 contains('YELLOW','Yellow',['defeats and kills','ending this specific','not three mutually exclusive species','comparatively limited','egg** bond','battle-ready'])
 contains('YELLOW','Green',['three semesters','exact revised syllabus is OPEN','six Dragon-native capability assignment below is superseded'])
 contains('GREEN','Green',['travels to the **Violet Realm**','pass a Genesis Field trial','identity verification is not','no six-stage trial','cycle can begin anew','illi\'s participation','Historical 002 palace-delegation account','Former Blue Arc training is consolidated into Green'])
 contains('BLUE','Red',['later return visit','already-bonded Black Unicorn','second King’s Tournament, which concludes Red Arc'])
 contains('BLUE','Yellow',['elevated neon flux','multiple naturally occurring velis','greatly reduce ELDRIS','not** visit or repair every velis','some hostile Primordials','intra-Yellow realm stabilization','fifth Black bond'])
 contains('VIOLET','Orange',['Paragon','Recursive Genesis corruption','Black Sprite (Resolution)','Black Vaelith (topological coherence/regeneration)','reciprocal Black-bond amplification','access/consent','30–40 feet','beams, orbs, bursts, shields, barriers and domes'])
 ops=t(L1+'/OPERATIONAL_DOMAINS.md');opold=old(L1+'/OPERATIONAL_DOMAINS.md').decode()
 ck(re.findall(r'^\|.*$',ops,re.M)==re.findall(r'^\|.*$',opold,re.M),'primary realm-emphasis table unchanged')
 universal='# Six operational domains — not colors, professions, or lifecycle stages'
 ck(ops.split(universal)[1]==opold.split(universal)[1],'universal operations and original evidence unchanged')
 for phrase in ['All Dragons have access','Genesis Field Topology','Resonance','Genesis Expression','self-augmentation, reinforced structure, strength, speed, jumping and durability','Historical native-capability assignment']:
  ck(phrase in ops,'native capability amendment: '+phrase)
 green=splitfields(t('BOOKS/GREEN/ARCS/ARC_004/ARC.md'))
 ck('delegates await privately' not in green['Entry state'] and 'An interview precedes' not in green['Principal conflict'],'no active palace/delegation entry or interview conflict')
 ck('exact revised syllabus is OPEN' in front(L2+'/INSTITUTIONS/BLACKSTONE.md').replace('**',''),'Blackstone premise corrected with syllabus OPEN')
 ck('not an anatomical heart' in front(L2+'/REALMS/ORANGE_VAELITH.md'),'city nexus distinct from individual biology')
 ck('not an assigned death' in front(L2+'/REALMS/VIOLET_UNICORNS.md'),'Unicorn recurrence remains conditional')
 ck('not retroactively upgrade' in front(L2+'/REALMS/GREEN_SPRITES.md'),'Sprite earlier healing limits retained')
 ck('the entire race is not hostile' in front(L2+'/REALMS/YELLOW_PRIMORDIALS.md'),'hostile Primordials scoped')
 ck('name/sex/title/lineage' in front(L2+'/REALMS/BLUE_LEVIATHANS.md'),'Paragon identity OPEN')
 # Current/new links only; old source bytes and their quoted instructions stay literal.
 def anchors(text):
  seen={};found=set()
  for h in re.findall(r'^#{1,6} (.*)$',text,re.M):
   slug=re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-');i=seen.get(slug,0);seen[slug]=i+1;found.add(slug+('-'+str(i) if i else ''))
  return found
 links=0
 for p in sorted(expected):
  if not p.endswith('.md') or p.startswith(P+'/'):continue
  content=front(p)
  for target in re.findall(r'\]\(([^)]+)\)',content):
   if target.startswith(('https:','http:','mailto:')):continue
   filename,_,anchor=unquote(target).partition('#');dest=(r/p).parent.joinpath(filename).resolve() if filename else r/p
   links+=1;ck(dest.exists(),p+' link '+target)
   if anchor and dest.is_file() and dest.suffix=='.md':ck(anchor in anchors(dest.read_text(encoding='utf-8')),p+' anchor '+anchor)
  ck(not re.search(r'\bPrincess Illi\b|\bPrincess Aina\b|\bCabal of Magi\b',content),'protected current names '+p)
 ck(json.loads(t(C+'/STRUCTURAL_VALIDATION.json'))['status']=='PASS','existing repository structural checks pass')
 final={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','baseline':BASE,'check_count':len(checks),'failures':[c['check'] for c in checks if not c['pass']],'counts':{'source_files':3,'publisher_manifest_hashes':0,'computed_source_hashes':3,'exact_author_notes':notes_total,'script_targets':14,'realm_entry_touchpoints':7,'contracts_checked':contracts,'protected_files_checked':len(set(protected)),'links_checked':links,'changed_paths':len(expected),'added':len(expected-set(baseline)),'modified':len(expected&set(baseline)),'deleted':0},'source_limit':'No publisher hash manifest supplied. ZIP CRC and computed intake/source-preservation hashes checked.','scope':'Book Red, Book White, maps, earlier sources, ledger and inherited repositories unchanged; no invented dates/scenes/mechanics.'}
 if a.report:a.report.write_bytes((json.dumps(final,ensure_ascii=False,indent=2)+'\n').encode())
 print(json.dumps(final,ensure_ascii=False,indent=2));return final['status']!='PASS'
if __name__=='__main__':raise SystemExit(main())
