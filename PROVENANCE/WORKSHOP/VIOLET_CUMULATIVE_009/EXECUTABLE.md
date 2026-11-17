# EXECUTABLE.md — MK163 Violet cumulative closure 009

Target: `xApologies/MK163`, default branch. This ZIP is the authoritative author-selected **continuation** of Violet 008, not a request to replace or delete historical canon.

## 1. Preflight and source of truth

1. Check out current branch and inspect `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_008.md` and `.csv`, `CONTINUITY/RED_RUNNING_DAY_LEDGER.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md`, and `BOOKS/RED/ARCS/ARC_006/TRAINING_ROUTES_005/`.
2. Verify active 008 contains 80 rows, Days 1080–1159, and its calendar has original weekday ordinals. **Do not modify Days 0–1159 or Blackstone.** If baseline differs, stop for review rather than overwriting it.
3. Read `VIOLET_EXTENSION_1160_1346.csv` and `.md` and `EXPEDITION_NODE_ROUTE_MANIFEST.md`. Check 187 unique consecutive extension rows and all required routes.

## 2. Integrate cumulative ledger

1. Create `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_009.md` and `.csv` containing **all 267 days, 1080–1346 inclusive**: exact 008 rows unchanged + exact extension rows 1160–1346. Update title and provenance only, not events in 008.
2. Extend `CONTINUITY/RED_RUNNING_DAY_LEDGER.md` with exactly Days 1160–1346 (preserve existing Day 0–1159 rows byte-for-byte when possible), matching the project's existing columns and link style. Preserve single active running ledger, no duplicate day rows.
3. Update `BOOKS/RED/ARCS/ARC_006/ARC.md`, `WORLD_CLOCK/CURRENT_MODEL_INDEX.md`, `BOOKS/RED/BOOK_OVERVIEW.md`, `CONTINUITY/SERIES_STATE_AND_EVENT_LEDGER.md` and appropriate navigation/README references to 009 as **the sole active Violet schedule**. Mark Violet complete **as an outlined arc**, not written chapters. King's Tournament remains future and unscheduled; do not invent its day.
4. Supersede active 008 schedule files only after the 009 cumulative pair has been validated and all live references updated. Retain 008 in Git history and historical provenance; **do not delete route files, atlas files, Blackstone, or workshop evidence**. Avoid broad destructive cleanup.
5. Explicitly preserve Kaira's Day 1165 local raeon placing **Blue**; Day 1225 tournament attendance with result OPEN; Illi spelled I-L-L-I. King's games Days 1188 and 1326, both Aithen/5. No other attendance inferred from recurrence.
6. Reused VTR-09 and VTR-10 are repeat expeditions, **not additional distinct route IDs**. VTR-11 remains unused. VTR-03/04/05/06/07/08 become scheduled as author-selected, but preserve route graph and provenance. Keep 11 original route records.

## 3. Route validation and narrative handoff

1. For each of eight scheduled expedition occurrences in `EXPEDITION_NODE_ROUTE_MANIFEST.md`, compare node sequence to the original `VTR-XX.md` and `ROUTE_PASSAGES.csv`/`ROUTE_INDEX.csv`.
2. Check each adjacent pair corresponds to an actual Atlas 002 edge; validate return reverses it. Report all route IDs, nodes, distances, edge validity, dates and phase counts.
3. Preserve separate destination/route statuses and original atlas geometry. Do not invent node-to-day allocations, combat encounters, equipment, traversability, travel times or ELDRIS results.
4. Create a compact `CHECKPOINTS/VIOLET_CUMULATIVE_009/INTEGRATION_REPORT.md` and validation receipt listing 008 baseline SHA, all added/modified/deleted files, exact day coverage, route checks, and unresolved narrative choices.

## 4. Required tests before commit

- 1,347 consecutive distinct running-ledger rows, Days 0–1346, with no gaps/duplicates.
- 267 consecutive active Violet 009 rows, Days 1080–1346; first 80 identical in all data fields to 008.
- For every row, original weekday number `((d+4)%6)+1`, weekday name, civil month/day derived from Day 0 = Aelora 5 and 353-day year; do not reset weekday at year/month boundaries.
- 1165 Aevor 16 Aiven/6 Blue placement; 1188 Aelith 7 Aithen/5 royal; 1209 Aelith 28 Aiden/2 surface return; 1225 Aerion 11 Aiven/6 tournament; 1250 Aeveth 4 Ailar/1; 1277 Aeveth 31 Ailor/4; 1298 Aesith 21 Ailar/1; 1320 Aeleth 10 Aithen/5; 1326 Aeleth 16 Aithen/5 royal; 1346 Aelor 4 Ailar/1 final surface return.
- All eight expedition occurrences have exact inclusive lengths and correct endpoints; no overlap with selected royal visits or downtime.
- No accidental duplicate active Violet ledger, broken links, or deletion of route/atlas/Blackstone data.

If any test fails, do not claim success or commit. Otherwise commit and report commit SHA, summary, and any remaining open narrative choices.
