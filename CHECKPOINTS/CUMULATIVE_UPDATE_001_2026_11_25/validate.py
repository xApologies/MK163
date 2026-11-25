"""Validate this scoped integration against its immutable baseline; no repository edits.

Run with --git PATH when Git is outside PATH; --report writes only the requested report.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from urllib.parse import unquote
import argparse, difflib, hashlib, json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
CHECK = Path(__file__).resolve().parent
KEY = CHECK.name
P = f'PROVENANCE/WORKSHOP/{KEY}'
C = f'CHECKPOINTS/{KEY}'
S = 'WORLD_CLOCK/L1_FANTASY/GENESIS_SYSTEMS_PLANNING.md'
A = 'WORLD_CLOCK/L2_WORLD_CIVILIZATION/BIOLOGY/AEN_TRAINING_AND_THROUGHPUT.md'
N = 'WORLD_CLOCK/L2_WORLD_CIVILIZATION/CIVILIZATION/NOBILITY_AND_CIVIC_AUTHORITY.md'
parser = argparse.ArgumentParser()
parser.add_argument('--git', default='git')
parser.add_argument('--report', type=Path)
args = parser.parse_args()
inventory = json.loads((CHECK/'EXPECTED_CHANGES.json').read_text('utf-8'))
BASE = inventory['baseline']
expected = inventory['files']
checks = 0
errors = []
def check(ok, message):
    global checks
    checks += 1
    if not ok: errors.append(message)
def run(*cmd):
    return subprocess.check_output([args.git,*cmd], cwd=ROOT)
@lru_cache(None)
def old(p): return run('show', f'{BASE}:{p}').decode('utf-8')
def text(p): return (ROOT/p).read_text('utf-8')
def has(p, fragments):
    t=text(p)
    for fragment in fragments: check(fragment in t, f'Missing scoped constraint in {p}: {fragment}')
def section(t, title):
    marker='## '+title+'\n'
    part=t.split(marker,1)[1]
    return part.split('\n## ',1)[0]

# Manifest and original bytes. The root manifest deliberately does not self-hash.
mapping=json.loads(text(P+'/SOURCE_MAP.json'))
manifest=json.loads(text(P+'/ORIGINAL/MANIFEST.json'))
check(len(manifest)==4,'Expected four publisher hashes')
check(len(mapping['files'])==5,'Expected five original source files')
check(set(manifest)=={x['path'] for x in mapping['files']} - {'MANIFEST.json'},'Manifest coverage')
for src in mapping['files']:
    b=(ROOT/src['target']).read_bytes()
    h=hashlib.sha256(b).hexdigest()
    check(h==src['sha256'] and len(b)==src['bytes'], 'Original byte fidelity: '+src['path'])
    if src['path'] in manifest: check(h==manifest[src['path']], 'Publisher hash: '+src['path'])
check(mapping['archive_sha256']=='69e2994a9a25654de1bbfb10a424b9fa44df55864fbbb41b512445a4e9192c2e','ZIP hash record')
package=json.loads(text(C+'/PACKAGE_VALIDATION.json'))
check(package['zip_crc']=='PASS' and package['safe_paths']=='PASS','Recorded ZIP CRC/path validation')

# Source fidelity includes every example, limitation, number and unselected alternative.
systems=text(S)
check(systems.endswith(text(P+'/ORIGINAL/02_GENESIS_SYSTEMS.md')),'Entire supplied systems record retained in active planning owner')
matches=list(re.finditer(r'^## Book (\w+) — (\w+) System \((\w+)\)$',systems,re.M))
check([(m[1],m[2],m[3]) for m in matches]==[('Orange','Amplification','Enhance'),('Yellow','Network','Distribute'),('Green','Vector','Redirect'),('Blue','Convergence','Integrate')],'Four selected systems and placements')
allocations={
    'Orange':[['Orange','Green'],['Red'],['Yellow','Blue'],['Violet']],
    'Yellow':[['Yellow'],['Red','Green'],['Orange'],['Blue'],['Violet']],
    'Green':[['Red','Orange'],['Yellow','Violet'],['Green'],['Blue']],
    'Blue':[['Red'],['Orange'],['Yellow'],['Green'],['Blue'],['Violet']],
}
all_rows=[]
for i,m in enumerate(matches):
    part=systems[m.end(): matches[i+1].start() if i+1<len(matches) else len(systems)]
    rows=re.findall(r'^\| ([A-F]) \| ([A-Za-z +]+) \|$',part,re.M)
    values=[v.split(' + ') for _,v in rows]
    check(values==allocations[m[1]],'Exact allocations: '+m[1])
    check([label for label,_ in rows]==list('ABCDEF'[:len(rows)]),'Local component labels: '+m[1])
    check(Counter(v for row in values for v in row)==Counter(['Red','Orange','Yellow','Green','Blue','Violet']),'Six basins exactly once: '+m[1])
    all_rows+=values
    macro=text(f'BOOKS/{m[1].upper()}/BOOK_MACRO_OUTLINE.md').split('---',1)[0]
    check(f'{m[2]} System ({m[3]})' in macro and 'introduction arc' in macro and 'OPEN' in macro,'Unscheduled book-level reference: '+m[1])
check(len(all_rows)==19,'Nineteen components')
check(sum(len(v)==1 for v in all_rows)==14,'Fourteen single-basin Cards')
check(sum(len(v)==2 for v in all_rows)==5,'Five dual-basin Cards')
has(S,['Kaira maintains and directs','Other practitioners contribute Shapings','not independent conventional Shapings','no simultaneous complete systems, ordinary active Cards or White Genesis Collapse','admissibility and interface implementation remain OPEN','30 ft cube','30 ft by 20 ft','candidate development context, not a locked introduction arc','Beam plus Fireball','No new systems in Books Red, Violet or White','No catalogue entries or IDs assigned','not proof of mathematical feasibility','Reconstruction, fabrication, spatial and transmutation systems are not selected','retired specialized Black Cards'])

# Ordered event and boundary acceptance checks, independent of source-table counting.
macro=text('BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md')
orange=section(macro,'Orange Arc'); yellow=section(macro,'Yellow Arc')
orange_events=re.findall(r'^\d\. (.+)$',orange,re.M)
check(len(orange_events)==5,'Five Orange ordered beats')
for event,needle in zip(orange_events,['royal palace','independent dungeon expeditions','guests of the King','learns of the Black Vaelith','with Kaira and illi']):
    check(needle in event,'Orange beat order: '+needle)
yellow_events=re.findall(r'^\d\. (.+)$',yellow,re.M)
check(len(yellow_events)==4,'Four Yellow ordered beats')
has('BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md',['Violet-referenced equal output normalization','no automatic Binding acquisition','previously selected good performance','no Black Vaelith bond in Orange Arc','practices throughout the journey','independently consenting Black Vaelith','Their bond precedes reciprocal amplification','On the return journey, by the end of Yellow Arc','not grant expert combat mastery, maximum endurance or selective incorporation mastery','without transfer or abandonment; other companion logistics remain OPEN'])
check('companions on journey and duration OPEN.' not in yellow,'Wholly OPEN companion claim superseded')
check(not re.search(r'\bDay\s+\d+',orange+yellow),'No new Book Orange daily dates')
has(A,['Day 43 Red/Orange','Days 52–62 Yellow','Day 85 Green','Day 123 Blue','Day 248 Violet under illi','Six-ring closure is a prerequisite, not collapse mastery','no collapse instruction is inserted into Book Red','17-hour trained baseline','not Kaira-specific','11–13 hours under combat reinforcement is illustrative only','dfdc85142fa673691bcb8a93f38d9f5a8e44eb3b','fixed singular recursion','compatible native Shapings/installed Bindings','incompatible active operational Cards'])
has(N,['All members of the royal family are **White Awakened**','**almost all nobles**','uncommon in the general population','sufficiently wealthy commoners','kingdom-specific','not a universal AERA requirement','a legal condition of nobility','does not establish that all royals or nobles can perform it','non-Awakened'])

# Every old byte in appended records survives; Orange edits have a precise patch audit.
exceptions={'.gitattributes','PROVENANCE/SOURCE_REGISTRY.json','WORLD_CLOCK/L1_FANTASY/README.md','BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md','BOOKS/ORANGE/ARCS/ARC_002/ARC.md','BOOKS/ORANGE/ARCS/ARC_003/ARC.md'}
for p,mode in expected.items():
    if mode=='modified' and p not in exceptions:
        check(text(p).endswith(old(p)), 'Complete preceding content retained: '+p)
for arc in ['Red Arc','Green Arc','Blue Arc','Violet Arc','White Arc']:
    check(section(macro,arc)==section(old('BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md'),arc),'Unrelated Orange arc intact: '+arc)
city=re.search(r'\*\*Chromatic Orange Realm.*?\n\n',old('BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md'),re.S).group()
check(city in macro,'Exact 2026-11-23 city restoration note preserved')
old_macro=old('BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md')
check(macro[macro.index('## Green Arc\n'):]==old_macro[old_macro.index('## Green Arc\n'):],'Orange Green–White and trailing source/exclusion detail intact')
before=json.loads(old('PROVENANCE/SOURCE_REGISTRY.json')); after=json.loads(text('PROVENANCE/SOURCE_REGISTRY.json'))
check(after['subsequent_deliveries'][:-1]==before['subsequent_deliveries'],'Existing source registry entries preserved')
check({k:v for k,v in after.items() if k!='subsequent_deliveries'}=={k:v for k,v in before.items() if k!='subsequent_deliveries'},'Other registry fields unchanged')
check(sum(x.get('id')=='MK163_CUMULATIVE_UPDATE_001' for x in after['subsequent_deliveries'])==1,'No duplicated integration registry entry')
patch=[]
for p,mode in sorted(expected.items()):
    if mode=='modified' and p.endswith('.md'):
        patch+=difflib.unified_diff(old(p).splitlines(True),text(p).splitlines(True),fromfile='a/'+p,tofile='b/'+p)
check(text(C+'/CANON_PATCH.diff')==''.join(patch),'Exact canonical before/after patch')

# All existing contracts retain the constitutional fields and stable IDs.
fields=['Arc identity','Narrative objective','Entry state','Principal conflict','Major events','Exit state','Dependencies','Status']
contracts=sorted((ROOT/'BOOKS').glob('*/ARCS/*/ARC.md'))
for p in contracts:
    t=p.read_text('utf-8')
    # Book Red includes historical contracts with additional sections; test required fields.
    heads=re.findall(r'^## (.+)$',t,re.M)
    if p.parts[-4]!='RED':
        check(heads==fields,'Eight arc fields: '+str(p.relative_to(ROOT)))
        check(f'MK163-{p.parts[-4]}-{p.parts[-2].replace("_","-")}' in t,'Stable arc ID: '+str(p.relative_to(ROOT)))

# Compare the entire candidate tree with the immutable base and explicit inventory.
changed=set(run('diff','--name-only',BASE).decode('utf-8').splitlines())
untracked=set(run('ls-files','--others','--exclude-standard').decode('utf-8').splitlines())
actual=changed|untracked
pending_report=C+'/VALIDATION.json'
local_exclusions=set(inventory.get('unrelated_local_exclusions',[]))
check(not local_exclusions.intersection(changed),'Unrelated local files must not be staged or tracked')
check(actual - {pending_report} - local_exclusions == set(expected) - {pending_report},'Exact changed-path scope: '+repr(sorted((actual-local_exclusions)^set(expected))))
check(not run('diff','--name-only','--diff-filter=D',BASE).strip(),'No deleted files')
check(not any(p.startswith('_inbox/') or p.endswith('.zip') for p in actual),'No handoff ZIP or inbox staged/tracked')
check(all((ROOT/p).is_file() for p in expected if p!=pending_report),'All declared files exist')
tree={}
for line in run('ls-tree','-r',BASE).decode().splitlines():
    meta,p=line.split('\t',1);tree[p]=meta.split()[2]
protected=[p for p in tree if p not in expected]
for p in protected: check(p not in changed,'Unrelated tracked content unchanged: '+p)
# Direct raw-byte verification of historic sources and images as well as ledger/calendar.
raw=[p for p in protected if p.startswith(('PROVENANCE/WORKSHOP/','CHECKPOINTS/')) or Path(p).suffix.lower() in ('.jpg','.jpeg','.png','.pdf') or p=='CONTINUITY/RED_RUNNING_DAY_LEDGER.md']
for p in raw:
    b=(ROOT/p).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check(blob==tree[p],'Historical/raw byte fidelity: '+p)

# Check newly introduced Markdown links, not unrelated historical preexisting link defects.
links_checked=0
for p,mode in expected.items():
    if not p.endswith('.md') or p.startswith(P+'/ORIGINAL/'): continue
    t=text(p); prior=old(p) if mode=='modified' else ''
    links=set(re.findall(r'\[[^\]]*\]\(([^)]+)\)',t))-set(re.findall(r'\[[^\]]*\]\(([^)]+)\)',prior))
    for link in links:
        if re.match(r'https?://|mailto:',link): continue
        path,_,anchor=unquote(link).partition('#')
        target=((ROOT/p).parent/path).resolve() if path else ROOT/p
        links_checked+=1
        check(target.exists(),'Missing local link: '+p+' -> '+link)
        check(target==ROOT or ROOT in target.parents,'Escaping local link: '+p+' -> '+link)
        if anchor and target.is_file():
            heads=re.findall(r'^#+\s+(.+)$',target.read_text('utf-8'),re.M)
            slugs=[re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-') for h in heads]
            check(anchor in slugs,'Missing link anchor: '+p+' -> '+link)
struct=json.loads(text(C+'/STRUCTURAL_VALIDATION.json'))
check(struct['status']=='PASS' and not struct['errors'],'Existing structural validator passed')
coverage=json.loads(text(C+'/COVERAGE.json'))
check(len(coverage)==16 and len({t['id'] for t in coverage})==16,'Sixteen distinct supplied-scope topics covered')
for row in coverage: check((ROOT/row['owner']).is_file() and (ROOT/row['source']).is_file(),'Coverage owner/source: '+row['id'])
result={'status':'PASS' if not errors else 'FAIL','baseline':BASE,'checks':checks,'publisher_hashes_verified':4,'original_files_preserved':5,'systems':4,'components':19,'single_basin':14,'dual_basin':5,'six_basin_covers':4,'coverage_topics':16,'unrelated_baseline_files_unchanged':len(protected),'historical_and_asset_files_raw_byte_verified':len(raw),'arc_contracts_present':len(contracts),'new_local_links_checked':links_checked,'files_added':sum(v=='added' for v in expected.values()),'files_modified':sum(v=='modified' for v in expected.values()),'files_deleted':0,'upstream_collapse_revision':'dfdc85142fa673691bcb8a93f38d9f5a8e44eb3b','errors':errors,'limits':'Structural and declared-scope preservation checks; no mathematical feasibility, transcript completeness, mastery or push-success claim.'}
if args.report: args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
