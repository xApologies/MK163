# EXECUTABLE.md — Codex work order, cumulative Checkpoint 007

**Target**: `xApologies/MK163` on the user's authorized working branch. This ZIP is cumulative. Follow this work order; do not treat earlier checkpoint README/EXECUTABLE files as newer authority.

## 1. Preflight
1. Confirm repository and current branch; `git status --short`, `git log -1 --oneline`.
2. Inspect existing `CONTINUITY/RED_RUNNING_DAY_LEDGER.md`, `BOOKS/RED/ARCS/ARC_006/ARC.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON.md` and the Atlas directory if present. Preserve unrelated work; stop and report conflicts rather than overwrite.
3. This ZIP has `MK163/` as its repository-relative payload prefix. Copy **contents** of `MK163/` into the repository root (not a nested MK163 folder). Do not blindly replace existing files: compare hashes/content first and skip identical files.

## 2. Import / preserve by owner
- Ensure the complete `WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON_ATLAS/` folder exists with its **340 nodes, 709 edges**, graph CSV/JSON/GraphML, 3D coordinates, eight original map views, five environmental maps, offline viewer, validation and rendering scripts, environmental node/edge/region/waterway records. This is WORLD_CLOCK Level 2 geography. Do not edit node IDs, connections, coordinates or maps to fit story routes.
- Ensure `BOOKS/RED/ARCS/ARC_006/TRAINING_ROUTES_005/` contains VTR-01 through VTR-11, `ROUTE_INDEX.csv`, `ROUTE_PASSAGES.csv`, `ROUTE_NODE_EXPECTATIONS.csv`. VTR-01–08 = eight Red-to-Blue navigation routes. VTR-09 = Yellow ELDRIS (Y045); VTR-10 = Green ELDRIS (G076); VTR-11 = Blue ELDRIS (B017). Preserve route paths and all node-by-node expected-environment records. VTR-01 (B041) author-locked; VTR-02 (B013), VTR-09, VTR-10 have scheduled use; VTR-03–08 and VTR-11 remain proposed.
- Import `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_007.md` and `.csv`. These **supersede** 006 for active dates. Keep 006 as historical provenance; do not publish its 1137 royal-game/1141 Green departure as current canon. Link 007 and the 005 route index from `ARC_006/ARC.md`.
- Update `CONTINUITY/RED_RUNNING_DAY_LEDGER.md` with a brief, nonduplicative Violet continuation pointer and/or append Days 1081–1159 from 007 if its established structure expects daily rows. Do NOT modify or replace Days <=1080; Blue return and invitation remain Day 1080.
- Preserve world-mechanics owners in AERA and the Accord Registry's ownership of formal historical expedition records; this task updates MK163 only.

## 3. Authoritative corrected calendar
- Weekdays from Day 1081=Aiven: weekday number = `((day-1081)%6)+1`, 1 Aiven, 2 Ailar, 3 Aiden, 4 Aiveth, 5 Ailor, 6 Aithen.
- Day 1085 and **Day 1139** are both King's raeon on fifth weekday; **1137 is weekday 3 and NOT a King's game**.
- Day 1135 is weekday 1 (Aiven). Day 1139 royal game; Days 1140–1141 Princess Illi; Day 1142 return to staging; Day 1143 Green expedition starts; Day 1159 returns.
- Expedition intervals inclusive: VTR-09 1087–1097 (4+3+4=11); VTR-01 1103–1117 (8+7=15); VTR-02 1123–1135 (7+6=13); VTR-10 **1143–1159** (7+3+7=17), with Yellow ELDRIS on return. No narrative encounter numbers or resource yields invented.

## 4. Verification and integration
1. Check archive integrity, and verify all 92 Checkpoint 006 members are present **byte-for-byte**; older 006 `EXECUTABLE.md` is superseded by this root version, with its original preserved under `PROVENANCE/CHECKPOINT_006_EXECUTABLE.md`.
2. Validate 79 continuous daily rows 1081–1159, unique dates, correct weekday names/numbers, King's game weekday 5, and no overlapping expeditions.
3. Run existing graph validator; ensure 340 nodes/709 passages and verify all 11 VTR paths use real edges and known node IDs; preserve environmental joins and map files.
4. Check `git diff --check`, review changed file list and diffs, run available tests. Do not regenerate deterministic atlas unnecessarily.
5. Commit only relevant authorized changes; push only to authorized branch if access and permission exist. Report branch, commit hash, pushed/not pushed, validation results, any conflicts. Never claim a push without actual confirmation.
