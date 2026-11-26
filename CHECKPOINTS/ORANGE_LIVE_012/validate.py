from pathlib import Path
from collections import Counter
import hashlib,json,re,subprocess,sys,zipfile,stat,os,difflib
R=Path(__file__).resolve().parents[2];os.chdir(R)
C=Path('CHECKPOINTS/ORANGE_LIVE_012');P=Path('PROVENANCE/WORKSHOP/ORANGE_LIVE_012')
G='C:/Users/rando/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
B='e0e9a568a63057f2cea643b87c611ca9fe820b7c'
errors=[];checks=0
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def git(*a):return subprocess.check_output([G,*a])
def read(p):return Path(p).read_text('utf-8')
def original(p):return git('show',B+':'+p).decode()
mapping=json.loads(read(P/'SOURCE_MAP.json'))['files'];byname={x['source']:x for x in mapping}
for x in mapping:
 b=Path(x['target']).read_bytes();check(hashlib.sha256(b).hexdigest()==x['sha256'] and len(b)==x['bytes'],'Source bytes '+x['source'])
hashes=read(byname['SHA256SUMS.txt']['target']).splitlines()
for line in hashes:
 h,n=line.split(maxsplit=1);check(byname[n]['sha256']==h,'Publisher hash '+n)
check(len(set(x['target'] for x in mapping))==len(mapping)-1,'Exactly one duplicate city-map byte alias')
def rows(t):return [l for l in t.splitlines() if re.match(r'^\|\s*\d+\s*\|',l)]
def cells(row):return [v.strip() for v in row.split('|')[1:-1]]
months=[('Aelor',33),('Aerith',32),('Aelora',31),('Aevrin',33),('Aelis',31),('Aevor',32),('Aelith',33),('Aerion',32),('Aeveth',31),('Aesith',33),('Aeleth',32)]
week=['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven']
def calendar(d):
 v=(d+69)%353
 for m,n in months:
  if v<n:return m,v+1,week[(d+4)%6],(d+4)%6+1
  v-=n
red=rows(read('CONTINUITY/RED_RUNNING_DAY_LEDGER.md'));oldred=rows(original('CONTINUITY/RED_RUNNING_DAY_LEDGER.md'))
check([int(cells(r)[0]) for r in red[:1638]]==list(range(1638)),'Complete consecutive Book Red0–1637')
for d,(r,b) in enumerate(zip(red[:1638],oldred[:1638])):
 check(cells(r)[:5]==cells(b)[:5],f'Red date/weekday unchanged {d}')
 if not (d<=211 or 787<=d<=859):check(r==b,f'Unrelated Red event unchanged {d}')
check(red[1638:]==oldred[1638:],'Historical secondary ledger rows unchanged')
changed_business=set(range(787,818))|{820,825,827}|set(range(829,857))
check({d for d in range(787,860) if red[d]!=oldred[d]}==changed_business,'Exact62 workforce-row corrections')
for d,token in [(820,'eight-smith'),(825,'eight-table'),(827,'eight experienced'),(846,'nine robes'),(856,'eight-robe')]:check(token in red[d],f'Production milestone {d}')
check(all('eight-smith capital expansion' not in red[d] for d in range(787,818)),'No early expansion')
orange=rows(read('CONTINUITY/BOOK_ORANGE_RUNNING_DAY_LEDGER.md'));src=rows(read(byname['DAILY_LEDGER.md']['target']))
check(orange==src,'All supplied Orange rows retained verbatim')
check([int(cells(r)[0]) for r in orange]==list(range(1637,1776)),'139 consecutive Orange handoff days')
for row in orange:
 c=cells(row);d=int(c[0]);m,n,w,k=calendar(d)
 check(c[1]==f'{m} {n}' and c[2]==f'{w} — Day {k}',f'Orange calendar {d}')
check(1743-1733+1==11 and 1772-1747+1==26 and 1758-1747+1==12,'Delve duration and Violet day12')
for d,tokens in {1710:['ransom'],1712:['Registry satisfaction'],1717:['Blue'],1718:['illi'],1744:['exit'],1773:['emerges from D24'],1775:['City 21','City 40','P15','one day','Caravan remains']}.items():
 t=orange[d-1637]
 for token in tokens:check(token.lower() in t.lower(),f'Day{d} {token}')
geo=read('WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/KINGDOM_CITY_CROSSWALK.md')
for token in ['**52**','**B3 / Blue-ranked dungeon**','**46**','**V2 / Violet-ranked dungeon**','**40**','**21**','**RESOLVED**']:
 check(token in geo,'Geography '+token)
for d,token in [(202,'City 52'),(209,'City 46'),(210,'City 46'),(211,'City 40')]:check(token in red[d],f'Corrected itinerary{d}')
for n,total in [('FLORA_REGISTER.md',36),('FAUNA_REGISTER.md',13),('INVERTEBRATE_REGISTER.md',12)]:
 t=read('WORLD_CLOCK/L2_WORLD_CIVILIZATION/REALMS/GREEN_ECOLOGY/'+n)
 check(len(rows(t))==total,'Ecology counts '+n)
 check(n!='FAUNA_REGISTER.md' or 'Vaeryn' in t,'Vaeryn retained')
event=read('WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/ORANGE_GREEN_REALM_HOMECOMING.md')
check(re.findall(r'^## (G-\d{3})',event,re.M)==[f'G-{i:03d}' for i in range(6)],'All six complete G events')
for t in ['proposed MK163 refinement','multiple separate localized Genesis collapses','not one perpetually','not completed narrative prose','optional','Vaeryn']:
 check(t in event,'Green authority constraint '+t)
for n in ['001','002','003']:
 t=read(f'BOOKS/ORANGE/ARCS/ARC_{n}/ARC.md')
 check(re.findall(r'^## (.+)$',t,re.M)==['Arc identity','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies','Status'],'Arc contract fields '+n)
check(json.loads(read(C/'STRUCTURAL_VALIDATION.json'))['status']=='PASS','Existing structural validator')
inv=json.loads(read(C/'EXPECTED_CHANGES.json'))['files'];changed=set(git('diff','--name-only',B).decode().splitlines());untracked=set(git('ls-files','--others','--exclude-standard').decode().splitlines());actual=changed|{p for p in untracked if not p.startswith('_art/')}
check(actual-{str(C/'VALIDATION.json').replace('\\','/')}==set(inv)-{str(C/'VALIDATION.json').replace('\\','/')},'Exact changed paths '+repr(sorted(actual^set(inv))))
check(not git('diff','--name-only','--diff-filter=D',B).strip(),'No deletion')
check(not any(p.startswith('_inbox/') or p.endswith('.zip') for p in actual),'No inbox/ZIP tracked')
tree={}
for line in git('ls-tree','-r',B).decode().splitlines():
 meta,p=line.split('\t');tree[p]=meta.split()[2]
raw=0; normalized_historical=[]
for p,h in tree.items():
 if p in inv:continue
 check(p not in changed,'Unrelated file '+p)
 if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')):
  b=Path(p).read_bytes(); exact=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h
  if not exact and p.startswith('CHECKPOINTS/CUMULATIVE_UPDATE_001_2026_11_25/'):
   clean=b.replace(b'\r\n',b'\n');check(hashlib.sha1(b'blob '+str(len(clean)).encode()+b'\0'+clean).hexdigest()==h,'Historical LF-normalized content '+p);normalized_historical.append(p)
  else:
   check(exact,'Historical byte preservation '+p);raw+=1
links=0
for p in inv:
 if not p.endswith('.md') or p.startswith(str(P/'ORIGINAL').replace('\\','/')):continue
 t=read(p);old=original(p) if p in tree else ''
 for dest in set(re.findall(r'\[[^\]]*\]\(([^)]+)\)',t))-set(re.findall(r'\[[^\]]*\]\(([^)]+)\)',old)):
  if dest.startswith(('https:','http:')):continue
  path=dest.split('#')[0]
  check((Path(p).parent/path).exists(),'Local link '+p+' -> '+dest);links+=1
result={'status':'PASS' if not errors else 'FAIL','checks':checks,'baseline':B,'source_files':len(mapping),'publisher_hashes':len(hashes),'distinct_source_objects':len(set(x['target'] for x in mapping)),'images':sum(x['source'].startswith('VISUALS/') for x in mapping),'orange_daily_rows':139,'red_main_rows':1638,'red_workforce_rows_changed':62,'historical_files_byte_verified':raw,'unchanged_prior_CRLF_worktree_files':normalized_historical,'new_local_links_checked':links,'day202_209':'RESOLVED by explicit012 author correction','D24_atlas':'NOT AVAILABLE; author route retained, graph/depth independently unverified','errors':errors}
(C/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
