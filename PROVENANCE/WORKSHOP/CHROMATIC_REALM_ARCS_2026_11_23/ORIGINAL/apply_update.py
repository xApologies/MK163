#!/usr/bin/env python3
"""Apply author-selected chromatic realm arc deltas to a local MK163 checkout.
Fail closed on missing source anchors; idempotent; preserve historical material.
"""
from pathlib import Path
import argparse, sys

P = argparse.ArgumentParser()
P.add_argument('--repo', required=True, help='Path to local MK163 repository root')
P.add_argument('--check', action='store_true', help='Validate only, do not write')
a=P.parse_args(); root=Path(a.repo).resolve()
if not (root/'.git').exists(): sys.exit('ERROR: --repo must be a Git checkout of MK163')

# Targeted additive author deltas. No book White edits. The BOOK/ARC headings are
# used to insert exactly at the story location, never at a similarly colored realm.
entries={
'BOOKS/ORANGE/BOOK_MACRO_OUTLINE.md':[
 ('## Red Arc', '''**Chromatic Green Realm visit — author update 2026-11-23:** This is a homecoming for Kaira's *already bonded* Black Sprite, not a transfer, abandonment or new bond. Kaira and the Sprite travel together, accompanied by Princess illi as previously established, to reconnect the Sprite with its native realm and a Sprite community. Community identity, ruling-body interaction and scenes remain OPEN. The Black Sprite stays bonded to Kaira and returns with her.'''),
 ('## Yellow Arc', '''**Chromatic Orange Realm — living-city nexus (author update 2026-11-23):** The Vaelith live symbiotically with a city formed from interconnected living biological structures (potentially tree networks). Its "heart" is **not an anatomical heart**: it is a Genesis-energy nexus sustaining the city's living distributed coherence network. Recursive ELDRIS-origin corruption threatens the nexus. The Black Vaelith's condition for consenting to the bond is that Kaira help heal the city. Kaira and the independently consenting Black Vaelith bond; their reciprocal amplification enables Vaelith topological/coherence-based restoration of the nexus and saves the city. This is a local city restoration, not a natural velis anchoring operation or the Book White planetary solution. Precise biology, scenes and mechanism remain OPEN.''')],
'BOOKS/YELLOW/BOOK_MACRO_OUTLINE.md':[
 ('## Yellow Arc — Red Realm and Dragon egg', '''**Chromatic Red Realm — Dragon conflict (author update 2026-11-23):** The Red Realm is experiencing an age-old war involving a hostile faction/brood led by a Chirality-specialist Dragon. All Dragons can access **Elemental Transduction**, **Dimensional Transduction / Dimensional Geometry** (CSR, Continuous Spatial Resolution, for flight), and **Chirality**, but individuals specialize differently; these are **not three mutually exclusive species**. Dragon energy budgets are comparatively limited despite Chirality's dangerous admissibility effects. During the Red Realm journey Kaira confronts the faction, ultimately defeats and kills its leader, ending this specific long-running war. The existing Black Dragon **egg** bond still occurs in Yellow Arc; do not imply the egg is grown or battle-ready. War origins, battle detail and faction name remain OPEN.'''),
 ('## Green Arc — Blackstone education and military recruitment', '''**Dragon capability correction (author update 2026-11-23):** The historical six-Dragon-domain list in this macro is superseded **only as a native Dragon capability assignment**. Dragons have three accessible native domains: Elemental Transduction, Dimensional Transduction / Geometry (CSR flight), and Chirality, with differing individual specializations. Genesis Field Topology is assigned to Unicorns, Genesis Expression to Leviathans, and Resonance to Primordials. The existing three-semester advanced-study milestone remains; its exact revised syllabus is OPEN. Do not silently retain six *Dragon-native* domains as the curriculum's premise.''')],
'BOOKS/GREEN/BOOK_MACRO_OUTLINE.md':[
 ('## Green Arc — Unicorn bond and operational synchronization', '''**Chromatic Violet Realm — Genesis Sanctuary trial (author update 2026-11-23; supersedes the palace-based bond location):** Following the established rescue and return, Kaira travels to the **Violet Realm** for the fourth Black bond. Unicorns already recognize Kaira as the current Black Singularity; identity verification is not the trial's purpose. At the Unicorns' Genesis Sanctuary, she must **pass a Genesis Field trial** before she is permitted to bond with the independently consenting living Black Unicorn. The precise trial, stages, challenges and Genesis Field mechanics are OPEN: **no six-stage trial is selected**. If no candidate succeeds and the Black Unicorn dies, the prophetic cycle can begin anew with another Black Unicorn emerging later; exact identity/recurrence mechanism remains OPEN. Preserve the preexisting Green Arc operational synchronization/training after the bond. Earlier text locating this bond at the White palace via delegation interview is SUPERSEDED in that scope; the delegation's other history is not silently invented. Princess illi's participation in the Violet journey is OPEN.''')],
'BOOKS/BLUE/BOOK_MACRO_OUTLINE.md':[
 ('## Red Arc — Recognition and Violet Realm', '''**Continuity clarification (author update 2026-11-23):** This is a **later return visit** to the Violet Realm **with the already-bonded Black Unicorn**, distinct from the Book Green Green Arc first Violet Realm visit and Genesis Sanctuary trial. Preserve this Red Arc's Black Primordial intelligence, second King's Tournament, travel restrictions and other established events.'''),
 ('## Yellow Arc — Yellow Realm expedition', '''**Chromatic Yellow Realm — natural velis stabilization (author update 2026-11-23):** Yellow's singularity is in elevated neon flux and its realm suffers especially severe ELDRIS formation. In addition to the established fifth Black Primordial geode/crystalline egg-like bond, Kaira travels among **multiple naturally occurring velis**, stabilizing enough significant local anchors to bring the Yellow Realm into safer conditions and greatly reduce ELDRIS formation. The realm is immense; she does **not** visit or repair every velis. She encounters and battles some hostile Primordials; do not characterize the entire race as hostile. This is **intra-Yellow realm stabilization**, not the cross-realm/White-planet anchoring reserved for Book White. Exact route, number, operators, combat and stabilization thresholds remain OPEN.''')],
'BOOKS/VIOLET/BOOK_MACRO_OUTLINE.md':[
 ('## Orange — Blue Realm and sixth Black bond', '''**Chromatic Blue Realm — Paragon restoration (author update 2026-11-23):** The Leviathans' ancient matriarch/patriarch, provisionally titled **Paragon**, has accumulated ELDRIS-inflicted wounds over years of defending the realm. Recursive Genesis corruption persists and spreads through the Paragon's immense body despite Leviathans' overwhelming Genesis Expression combat capacity. Kaira, with her existing Black Sprite (Resolution) and Black Vaelith (topological coherence/regeneration), heals the Paragon using their complementary abilities and reciprocal Black-bond amplification. This act secures access/consent to the **Black Leviathan egg**; preserve the already-established sixth bond, hatching and juvenile growth to approximately 30–40 feet before departure. Paragon title, lineage, specific healing mechanics and egg custodianship remain OPEN. Leviathans can express Genesis beams, orbs, bursts, shields, barriers and domes through native Genesis Expression and vast Bandwidth.''')],
'WORLD_CLOCK/L3_CHARACTERS_EVENTS/EVENTS/SIX_BLACK_BONDS.md':[
 ('# Sixth bond and companion travel · 2026-11-21', '''**Author chronology correction · 2026-11-23:** The fourth Black Unicorn bond still occurs in **Book Green, Green Arc**, but now **in the Violet Realm at the Genesis Sanctuary after Kaira passes a Genesis Field trial**. The older White-palace delegation interview/bond location is SUPERSEDED only in that scope. The Book Blue Red Arc Violet Realm visit remains a subsequent visit with the already-bonded Unicorn. Six-bond order, independent agency and companion-travel restrictions remain unchanged. The trial's stages/mechanics are OPEN; the Black Unicorn's death without a successful bond may restart its prophetic emergence cycle, exact mechanics OPEN.''')],
'WORLD_CLOCK/L1_FANTASY/OPERATIONAL_DOMAINS.md':[
 ('## Six realm-to-specialization assignments (LATEST, AUTHOR-LOCKED)', '''**Author native-capability amendment · 2026-11-23:** All Dragons have access to **Elemental Transduction, Dimensional Transduction / Dimensional Geometry (CSR flight), and Chirality**, while individuals specialize in one or another; not three mutually exclusive species. **Genesis Field Topology** is assigned to **Unicorns**; **Resonance** to **Primordials** (self-augmentation, reinforced structure, strength, speed, jumping and durability); **Genesis Expression** to **Leviathans** (beams, orbs, bursts, shields, barriers, domes). Vaelith topology/coherence and Sprite Resolution remain unchanged. This newer native-capability assignment supersedes the historical *six Dragon-associated capabilities* paragraph below, **not** the universal L1 operational taxonomy or established realm-to-specialization table.''')]
}

arc_notes={
'BOOKS/ORANGE/ARCS/ARC_001/ARC.md':'Green Realm homecoming: Kaira, Princess illi and the already-bonded Black Sprite visit the Sprite community and ruling body. The bond continues; the Sprite departs with Kaira. Community and reunion details OPEN.',
'BOOKS/ORANGE/ARCS/ARC_003/ARC.md':'Orange Realm: Kaira and the Black Vaelith bond under the condition that they heal the living Vaelith city. Its "heart" is a Genesis-energy nexus in an interconnected living biological network, not an anatomical organ. Their amplified topological restoration removes ELDRIS-origin recursive corruption and saves the city.',
'BOOKS/YELLOW/ARCS/ARC_003/ARC.md':'Red Realm: Kaira intervenes in an age-old Dragon war and defeats/kills the leader of a hostile Chirality-specialist faction. Every Dragon can use Elemental Transduction, CSR Dimensional Transduction and Chirality, with individual specializations. The Red Black Dragon egg bond remains; the egg is not a mature combatant.',
'BOOKS/GREEN/ARCS/ARC_004/ARC.md':'Violet Realm: Kaira visits the Unicorns’ Genesis Sanctuary and must pass a Genesis Field trial before the fourth Black Unicorn bond. Unicorns already recognize her prophetic identity; trial mechanics and stages remain OPEN. This supersedes the older White-palace bond location, not the subsequent operational synchronization training.',
'BOOKS/BLUE/ARCS/ARC_001/ARC.md':'This is a later Violet Realm visit with the already-bonded Black Unicorn, following the first Violet Realm visit and sanctuary trial in Book Green Green Arc. Existing tournament and intelligence beats remain unchanged.',
'BOOKS/BLUE/ARCS/ARC_003/ARC.md':'Yellow Realm: alongside the fifth Black Primordial bond, Kaira travels to multiple natural velis, stabilizes enough anchors to bring high-neon Yellow into safer conditions and greatly reduce ELDRIS formation; encounters include hostile Primordials. This does not perform Book White’s cross-realm anchoring.',
'BOOKS/VIOLET/ARCS/ARC_002/ARC.md':'Blue Realm: Kaira and her bonded Black Sprite and Black Vaelith heal years of accumulated recursive ELDRIS corruption in the ancient Leviathan Paragon, securing the Black Leviathan egg. Existing hatching and approximately 30–40-foot juvenile departure remain unchanged.'
}
for path,note in arc_notes.items(): entries[path]=[('## Major events', '**Author-selected chromatic realm event · 2026-11-23:** '+note)]

# Keep source history intact. Add scoped update immediately under owning heading.
marker='<!-- MK163_CHROMATIC_REALM_DELTA_2026_11_23 -->'
changes=[]; outputs={}
for path,items in entries.items():
    f=root/path
    if not f.is_file(): sys.exit('ERROR missing '+path)
    original=f.read_text(encoding='utf-8'); updated=original
    for heading,note in items:
        if heading not in updated: sys.exit('ERROR missing heading '+heading+' in '+path)
        # per heading: check whether this update already present in its local section
        pos=updated.index(heading)+len(heading)
        nexthead=updated.find('\n## ',pos)
        segment=updated[pos:nexthead if nexthead>=0 else None]
        if marker in segment: continue
        updated=updated[:pos]+'\n\n'+marker+'\n'+note+'\n'+updated[pos:]
    if updated!=original:
        changes.append(path);outputs[f]=updated
if not a.check:
    for f,updated in outputs.items():f.write_text(updated,encoding='utf-8')
print(('WOULD UPDATE' if a.check else 'UPDATED')+f' {len(changes)} files:')
for x in changes:print(' - '+x)
if not changes: print('All update markers already present; no changes required.')
