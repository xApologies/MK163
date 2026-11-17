# Violet cumulative 009 · integration and reverse diff

Baseline: published 008 commit `0ee036e7e2d015ab9d181fdc665fcce7757198f7`. The six-file author-selected continuation adds Days 1160–1346. Violet closes on Day 1346 as a **complete outlined arc**, not written chapters. [Execution instructions](../../PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009/EXECUTABLE.md) · [Source hashes and preservation map](../../PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009/SOURCE_MAP.json) · [Validation and changed-file inventory](VALIDATION.json).

## Coverage and reverse diff

| Scope | Integration |
|---|---|
| 008 baseline | All 80 rows, Days 1080–1159, retained with every data field and Markdown row unchanged in the [009 cumulative ledger](../../BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_009.md) and [CSV](../../BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_009.csv). |
| Running ledger | All 1,160 existing day rows remain byte-for-byte unchanged. Exactly 187 new rows extend the single ledger to 1,347 consecutive days, 0–1346. |
| Calendar | Original 353-day civil year, eleven month lengths, Day 0 anchor and Ailar-to-Aiven ordinals remain unchanged. Calendar-owner edit is navigation only. |
| Selected attendance | Day 1165 local Blue placement; Day 1225 tournament with result OPEN; royal games 1188/1326, both Aithen/5; illi visits 1189–1190; returns 1191/1327. Recurrence implies no other attendance. |
| Routes | Six previously proposed routes become scheduled; VTR-09/VTR-10 repeat without new route IDs. All eleven route records remain. Twelve cumulative occurrences use ten routes; VTR-11 remains unused and unscheduled. |
| Closure | Arc, model index, book overview, series ledger and operating guidance select the VTR-08 surface return on Day 1346 as the outlined-arc endpoint. King's Tournament stays future and undated. |
| Detail and provenance | All six ZIP members preserved exactly, including supplied validation claims and all 187 event rows. Source `Illi` is normalized to protected lowercase `illi` in the two new active event rows. The original wording remains preserved. No other supplied event is shortened or rewritten. |

## Eight additional expedition occurrences

Distances are existing modeled route distances in miles, not new travel-time claims. Each return reverses its outbound sequence. [Full validation receipt](ROUTE_VALIDATION.json) records every node, edge ID, exact modeled distance sum and dated phase.

| Route | Destination | Days | Phase counts | Nodes / outbound edges | Outbound / round trip miles | Check |
|---|---|---|---|---|---|---|
| VTR-03 | B009 | 1170–1184 | 8 down + 7 up = 15 | 11 / 10 | 17.728 / 35.456 | PASS |
| VTR-04 | B015 | 1193–1209 | 9 down + 8 up = 17 | 13 / 12 | 20.339 / 40.678 | PASS |
| VTR-09 repeat | Y045 | 1214–1224 | 4 down + 3 combat + 4 up = 11 | 8 / 7 | 8.461 / 16.923 | PASS |
| VTR-05 | B058 | 1232–1250 | 10 down + 9 up = 19 | 19 / 18 | 27.568 / 55.136 | PASS |
| VTR-06 | B074 | 1259–1277 | 10 down + 9 up = 19 | 19 / 18 | 27.073 / 54.145 | PASS |
| VTR-10 repeat | G076 | 1282–1298 | 7 down + 3 combat + 7 up = 17 | 12 / 11 | 16.543 / 33.087 | PASS |
| VTR-07 | B053 | 1304–1320 | 9 down + 8 up = 17 | 16 / 15 | 23.609 / 47.218 | PASS |
| VTR-08 | B073 | 1328–1346 | 10 down + 9 up = 19 | 17 / 16 | 27.174 / 54.349 | PASS |

The manifest's ordered nodes match the existing VTR documents and route index. All 107 outbound edge uses and 107 reverse uses match `ROUTE_PASSAGES.csv` and Atlas 002 edges. Selected expedition intervals total 134 days without overlap. Phase/day labels are verified, without assigning individual nodes to days. The full-free-day intervals are eight days 1251–1258, four days 1278–1281 and five days 1299–1303. The reused Green route does not automatically repeat an encounter selected for the earlier trip.

## Supersession and preservation

009 is the sole active daily schedule. The complete integrated 008 [Markdown](../../PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009/BASELINE_008/VIOLET_DAILY_LEDGER_008.md) and [CSV](../../PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009/BASELINE_008/VIOLET_DAILY_LEDGER_008.csv) are preserved byte-for-byte before supersession. The old active CSV is removed. Its Markdown path becomes a short historical navigation page with no daily rows, preserving every existing running-ledger link without editing old rows. Other live navigation points directly to 009. The 008 integration receipt gains only a historical banner and an updated historical CSV link; its original report remains in Git. Prior checkpoint validation receipts and workshop sources stay untouched.

The six original VTR-03–08 files previously served as both original evidence and active records. Their exact bytes now live under `PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_009/PRIOR_ORIGINAL_ROUTES/`, with hashes matching the original 007 source map. The new source map records this preservation relocation while leaving the historical 007 map intact. All route sequences, destination parameters, distances, node expectations, passage data and atlas geometry remain unchanged; only schedule statuses, dated occurrence notes and navigation change. No route or atlas file is deleted. Blackstone, earlier arcs, the Day 1021 cancellation, equipment mechanics, upstream repositories and `_inbox` remain untouched.

## Validation and OPEN items

[The reproducible validator](validate_checkpoint.py) checks 1,347 running days, 267 cumulative rows, preservation of the first 80 rows and all earlier running rows, source hashes, all calendar coordinates, required date anchors, route/edge/distance checks, history, allowed changes and local links. The existing structural validator also passes. The ZIP has no external hash manifest; SHA-256 values are computed receipt hashes, and its `VALIDATION.json` is independently checked rather than assumed authoritative proof.

No supplied correction topic is omitted and no integration conflict remains. Still OPEN: Day 1225 and royal-game results, King's Tournament date/qualification/scenes, VTR-11 scheduling, exact node/day traversal, individual encounters and outcomes, resource yields, CSR manufacture, other previously unassigned character details and chapter prose. Nothing in the outlined closure selects those details or guarantees mastery. This is full preservation of this supplied continuation, not a claim of literal conversation recovery or completion of unrelated historical-source gaps.
