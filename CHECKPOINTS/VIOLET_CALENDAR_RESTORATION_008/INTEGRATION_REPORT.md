# Violet Calendar Restoration 008 · integration and reverse diff

This scoped correction applies the author's `MK163_Violet_Calendar_Restoration_008.zip` to published baseline `5260cefdf22f59c297f4ab66ade132f6ec8584a6`. It supersedes the 007 rotated weekday order and Violet event schedule. It does not reintegrate the cumulative atlas or other arcs. [Execution instructions](../../PROVENANCE/WORKSHOP/VIOLET_CALENDAR_RESTORATION_008/EXECUTABLE.md) · [Pre-edit dependency inventory](DEPENDENCIES.md) · [Validation results](VALIDATION.json).

## Coverage and supersessions

| Topic | Before | Applied correction and owner |
|---|---|---|
| Weekday ordinals | 007 rotated the civil order to begin with Aiven | Restore Ailar 1, Aiden 2, Aiveth 3, Ailor 4, Aithen 5, Aiven 6. Formula `((d + 4) % 6) + 1`, Day 0 Aelora 5/Aithen. [Calendar owner](../../WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md). |
| Recurring games | Royal Ailor/5 and local Aiven/1 | Royal Aithen/5 and local Aiven/6, including both local-tournament recurrence statements in the [games owner](../../WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md). Earlier Blue visits and results remain verbatim. |
| Opening six days | Vaelum arrangements, royal game on 1085 and return/preparation on 1086 | Days 1081–1086 are recovery, personal time and ordinary slice-of-life, with no selected royal travel or game. The seven-person vaelum was already accepted at the Day 1080 dinner. |
| First Violet royal visit | Game on 1085, then general downtime after the Yellow expedition | Royal game 1098/Aithen, illi 1099–1100, Blue return 1101, preparation 1102. |
| Second Violet royal visit | Game 1139/Ailor and illi 1140–1141 | Downtime 1136–1139, royal game 1140/Aithen, illi 1141 and return to Blue/staging 1142. |
| Expedition schedules | Four selected intervals and eleven registered routes | Preserve VTR-09 1087–1097 (4+3+4 = 11 days), VTR-01 1103–1117 (8+7 = 15), VTR-02 1123–1135 (7+6 = 13), VTR-10 1143–1159 (7+3+7 = 17). No route geometry, node, passage, destination, equipment or roster change. |
| Ordinary downtime | Day 1120 tournament already omitted | Retain no selected tournament on 1120 and the supplied downtime intervals. Absence of Kaira's participation does not close the shop. |
| Single active schedule | Active 007 Markdown/CSV pair | Replace with the complete [008 Markdown](../../BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_008.md) and [008 CSV](../../BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_008.csv). Update arc, model index, operating guidance, continuity and dependent links. |

The [running ledger](../../CONTINUITY/RED_RUNNING_DAY_LEDGER.md) retains every Day 0–1080 row exactly. Its 79 subsequent rows adopt the complete supplied events, preserving civil month/day, named weekday and continuity navigation. The supplied 80-row Violet schedule includes Day 1080 as a closure reference, without replacing the detailed Blue closeout. Day 1021 remains Kaira's return with no tournament attendance or replacement Blue placement.

## Cleanup and historical evidence

Only these obsolete active files are removed:

- `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_007.md`
- `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_007.csv`

Their exact integrated versions remain in [the baseline Git tree](https://github.com/xApologies/MK163/tree/5260cefdf22f59c297f4ab66ade132f6ec8584a6/BOOKS/RED/ARCS/ARC_006). The original 006/007 supplied schedules, literal earlier author replies, manifests and all workshop evidence remain untouched under `PROVENANCE/WORKSHOP/VIOLET_CUMULATIVE_007/`. No active 006 schedule or additional redundant active alias was present. The [007 report](../VIOLET_CUMULATIVE_007/INTEGRATION_REPORT.md) receives only an explicit historical banner and a pinned old-ledger link; its original text remains available in Git. Its unchanged validation receipt and source map describe that historical baseline, not a second current calendar.

All five 008 ZIP members are preserved byte-for-byte in [the source folder](../../PROVENANCE/WORKSHOP/VIOLET_CALENDAR_RESTORATION_008/README.md). [The source map](../../PROVENANCE/WORKSHOP/VIOLET_CALENDAR_RESTORATION_008/SOURCE_MAP.json) records their sizes and SHA-256 hashes and the archive hash. The ZIP contains no checksum manifest. Its supplied `VALIDATION.json` is preserved as an arithmetic claim, independently checked here. Path safety, case collisions and ZIP CRC are verified. Active CSV line endings are normalized to LF; original CSV bytes remain intact. Active `Illi` typography becomes protected lowercase `illi`, with no other event-text normalization.

The repeated Yellow-stratum encounter note on each return row describes the selected Days 1153–1159 interval. It does not establish seven different encounters or an exact encounter day. The earlier one-day delay remains part of the unchanged selected seven-day ascent and route account.

## Validation and boundaries

The reproducible [checkpoint validator](validate_checkpoint.py) checks all 1,160 consecutive running-ledger dates, all 80 supplied schedule rows and their original month/day and weekday ordinals, complete source-event transfer, the four expedition intervals, royal dates, visits, returns, protected history, source hashes, deletion scope, single active schedule and local links. The existing structural validator is also run with `--structural-only` against `LIVE_MODEL_003_DELIVERY_MANIFEST.json`. Exact results and changed/deleted paths are recorded in [VALIDATION.json](VALIDATION.json).

No supplied information in this five-file correction is omitted. No new canon conflict remains. Detailed expedition outcomes, exact encounter timing, CSR manufacture, unresolved companion identities, and broader astronomical/seasonal questions retain their previous OPEN status. The separate 007 limitation concerning an unavailable original 006 ZIP remains historical; this correction makes no new claim about that carry-forward or literal transcript completeness. No inherited repository, atlas asset, earlier arc, Blackstone timetable, source archive or unrelated canon is changed. `_inbox` remains local and untracked. Publication and remote SHA verification follow successful validation.
