# MK163 / AERA / MK727 cumulative handoff — 2026-11-17

## Purpose
Integrate *new* author-approved mechanics, prices, and Violet Arc traversal details into the correct repository owners. This package is **cumulative for the current Violet CSR workshop**, not an export of all historic book arcs. Do not treat it as permission to replace unrelated files or copy entire AERA into MK163.

## Target mapping
| Package path | Destination | Action |
|---|---|---|
| `MK727/catalogues/genesis-cards/MK727_GENESIS_CARD_MASTER_1245.csv` | `xApologies/MK727` same path | **RECONCILE**, not blind overwrite: compare live HEAD and original 56 columns; preserve any newer remote changes; apply binding pricing fields and DG-0031 O/Y/B/V revision; detect conflicts |
| `AERA/L1/INTERFACES/05_BINDING_CARD_BASIN_SUPPLY_AND_CSR.md` | `xApologies/AERA` same path | Add new mechanics note; link from L1 interface index; retain source docs |
| `AERA/L2/TECHNOLOGY/CSR_AND_DIMENSIONAL_EXPEDITION_EQUIPMENT.md` | `xApologies/AERA` same path | Add technology/civilization crosswalk; link from L2 index; do not rewrite dimensional master |
| `MK163/WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/VIOLET_VAELUM_TRAVERSAL_LOGISTICS.md` | `xApologies/MK163` same path | Add world/civilization logistics; cross-link to L3/ARC_006 |
| `MK163/BOOKS/RED/ARCS/ARC_006/VIOLET_CSR_TRAVERSAL_HANDOFF.md` | `xApologies/MK163` same path | Add Violet scene-planning handoff; link from existing ARC.md without replacing content |

**Authority:** AERA L0 foundational energy structure; AERA L1 Shaping interfaces and basin/bandwidth/fatigue rules; AERA L2 technologies and world civilization; MK727 catalogue of 1,245 Shapings/prices; MK163 L2 local culture/logistics and L3/Book Red character-specific continuity. The catalogue is not to be duplicated into AERA or MK163.

## Critical source/merge constraints
- CSV input has **1,245 rows, 65 columns**, first 56 unchanged from user-uploaded `Genesis Cards.csv` **except one intentional edit**: DG-0031 `required_basins` becomes `["Orange", "Yellow", "Blue", "Violet"]`. Nine new columns cover seven Binding rank prices, status, and basis. Validate source header, row count, IDs, and per-row data before commit.
- Red Binding base schedule: FOUNDATIONAL 700; COMMON_SPECIALIZATION 1200; ADVANCED 2200; POWERFUL 3700; EXCEPTIONAL 5700 eln. Corresponding Red Card schedule 1700,3100,5700,11000,17000 eln. Orange–White Binding prices in CSV are **provisional**; do not misrepresent as final canon. 229 summon records have no source pricing class and remain unpriced.
- CSR Binding working ~60% installed bandwidth. **Unresolved** whether basin-access Bindings count inside 60%. Do not assign numerical footprint to other Bindings or fabricate a global formula.
- Bindings can share basin energy concurrently if control/endurance allows; Cards exclusively occupy all their active basins across all interfaces. Native White-superposed reserve can fill projected manifold in emergencies; not unlimited power. AERA current fatigue model is endurance-like, not an arbitrary mana bar.
- CSR binding and CSR Card require the same four basins, but only Card activation imposes exclusive basin lockout. Exact Card/ongoing-Shaping precedence OPEN.
- Dimensional bracelet is a form factor of existing recursive-topology conservation technology. Do not invent pocket dimensions, inventory UIs, or exact capacity. Leader's bracelet is author-selected as higher-capability expedition storage; backup ring bearer OPEN.
- No boat hauled as standard expedition equipment. Crossing engineering specifics OPEN.
- Do not alter established Day 1080/1081 chronology, King's Tournament rules, the Blue rescue, Genesis Robe semantics, or existing Shield/Beam/Fireball basin engineering.
- Protect spellings: Kaira, Nyx, vaelum, aithren, vaen, maege, maege-glass, ru’ne, aen, ELDRIS, eln.

## Codex procedure
1. Inspect live HEAD of **all three** repositories and existing index references before editing; stop if any remote file has newer conflicting authority.
2. Produce diff for CSV against current MK727 master; apply intentional changes only and preserve any upstream nonconflicting additions. Verify class mappings and CSR row.
3. Add scoped new notes, link from appropriate indices and Violet ARC.md; do not overwrite original prose wholesale.
4. Validate all markdown relative links, CSV row/column counts, canonical spellings, continuity dates, and absence of duplicate catalogue copies.
5. Show change summary and actual commit/push SHAs. If push not authorized/available, report staging only. Never claim pushed without verification.
