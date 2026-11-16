# Codex integration and validation directive

Repository: `xApologies/MK163`, branch `main`. Start by fetching current HEAD; expect BLUE_ARC_012 integration commit `b6706dd29ec757234976f840deba6fa8a6336f31` to be in history, but do not assume HEAD is unchanged.

1. Verify ZIP CRC and SHA-256 manifest; read all files. Treat this as a corrective delta only. No copying of historical Blue Arc 012 payload back into active files.
2. Audit `CONTINUITY/RED_RUNNING_DAY_LEDGER.md` from 0 to 1049: exactly 1050 unique sequential days, Day 0=Aithen, weekday `['Ailar','Aiden','Aiveth','Ailor','Aithen','Aiven'][(day+4)%6]`. Do not change weekday names or ordinal numbering. Check month/day fields remain unchanged.
3. Search all active narrative and World Clock files for dated King's raeon salons and local raeon tournaments, including pre-945 dates. The early Aiven tournaments should remain untouched. Distinguish recurring official tournaments from casual card games, King's Tournament (dungeon race), and historical quotes.
4. Apply `01_EVENT_RESCHEDULE.md` consistently to canonical ledger, `BOOKS/RED/ARCS/ARC_005/ARC.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md`, royal visit/event/character files and any active indexes. Preserve original provenance with an explicit supersession crosswalk. No double-booking; adjust surrounding ordinary-life/travel allocations only as specified.
5. Canonical King's salon weekday=5 **Aithen**; local card-shop tournament weekday=6 **Aiven**. Fix active misleading phrases including 'Aiden fifth day', 'Aiveth sixth day', and old historical 'King's last day' when they appear as live assertions. Retain history in source archives with authority notes.
6. Apply `02_VELIS_CANON.md` in MK163 World Clock and research-expedition references. Do not push AERA changes.
7. Validate all seven corrected event dates, surrounding travel, preserved major dates, links, protected terms, and all 1050 ledger weekday values. Run repository tests, report new HEAD, paths modified, unresolved collisions and audit outcome. If checks pass, commit and push to `main` (or PR if required by policy). If checks fail, do not claim success.

**Important:** This package proposes a minimal reconciliation of seven identified Blue Arc conflicts, not a guarantee that every older file is clean. Search comprehensively and document any other issues rather than silently changing dates.
