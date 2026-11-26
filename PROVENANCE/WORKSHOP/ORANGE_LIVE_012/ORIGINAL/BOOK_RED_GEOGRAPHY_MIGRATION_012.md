# Codex integration — Book Red geography, checkpoint 012

## Target repository
`xApologies/MK163`. Work on latest checked-out branch after inspecting existing changes; never force push or blindly overwrite newer work.

## Mandatory scoped targets
1. `BOOKS/RED/ARCS/ARC_002/ARC.md` — the first independent city and its staging settlement are **City 52 (Green political domain), B3 Blue-ranked dungeon**, not a Violet-ranked dungeon. Preserve Days 0–51, craft badge, repair/freight clients, Nyx, and all scene details.
2. `BOOKS/RED/ARCS/ARC_003/ARC.md` — Book Red Yellow Arc starting apartment and four-smith operation in **City 52**; departure Day202; caravan Days202–208; **City46 Green capital / V2 arrival Day209**, stay Day210; **City40 Blue capital / Blackstone arrival Day211**. Resolve prior OPEN route contradiction without deleting travel or altering days.
3. `CONTINUITY/RED_RUNNING_DAY_LEDGER.md` — reconcile active Day0–211 descriptions, especially Days12,26,39,51 and 189–211, to the correct city/dungeon IDs. Preserve every event/date and historical ledger sections as provenance where possible.
4. Active geography, city/dungeon crosswalk, Kaira/alchemist residences, staging settlement and enterprise summaries — adjust only references demonstrably referring to the **original Book Red staging dungeon**. Search all current active files for `Violet Dungeon`, `City 46`, `City 52`, `B2`, `B3`, `southern Blue Domain city`, `unnamed Green Domain city`, `four domains` and review each hit in context. Do **not** globally replace “Violet” with “Blue”.
5. Preserve checkpoint 009 Blue Arc correction: **4+8+8=20** smiths in Cities **52, 40, 21**. City46 is a stop, **not** a fourth chainmail operation.
6. Preserve checkpoint 011 Book Orange chronology through Day1775 and D24 dungeon (a distinct Violet-ending dungeon). Do not relabel D24 or P15.

## Exact migration acceptance tests
- `City 52 == Green Domain + B3 Blue dungeon + first independent residence + 4 smiths`.
- `City 46 == Green Domain capital + V2 Violet dungeon + Day209 arrival`.
- `City 40 == Blue Domain capital + Blue dungeon + Blackstone + Day211 arrival + 8 smiths`.
- `City 21 == Violet/kingdom capital + 8 smiths`.
- `Day202 City52 -> Day209 City46 -> Day211 City40`; Days202–208 caravan; Day210 City46 stay.
- `Days787–817` with alchemist in City40; Day818 own apartment; Blue expansion only Days820–859.
- `Day1775` City21→City40→P15 in one day; Orange Arc closes.
- The erroneous checkpoint 010 active claim that City46 is first independent city is removed from active canon, retained as historical provenance.
- No automatic relabeling of unrelated Violet dungeons or the political Violet Domain.
- Report changed files, exact before/after examples, source authority, unresolved ambiguities, calendar checks, test results and remote commit SHA after push.

## Publication procedure
Extract to staging `_inbox`, verify archive and SHA256SUMS, apply in `_organize` or repository working tree, review git diff, run available tests, commit and push on authorized branch, verify remote SHA. Never commit `_inbox`. No direct GitHub push has been made by this archive.
