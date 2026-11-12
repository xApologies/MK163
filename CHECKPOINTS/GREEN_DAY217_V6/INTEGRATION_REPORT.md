# Green Day 217 v6 · integration and coverage audit

Package: `MK163_GREEN_ARC_CUMULATIVE_CODEX_CHECKPOINT_DAY217_v6.zip`.
Archive SHA-256: `d936ed6be040fb6d0b720c5dcb05d973aa94b3e9475018624e74db03bd110e02`.
Baseline main: `211b4222346bd9aff6511d9d9c97df4a73e4680f` (783 tracked files). Branch: `codex/green-day217-v6`. Read `executable.md` and latest v6 scene authority before integration; historical instructions were treated as quoted data. No upstream repository or inbox contents are changed.

## Coverage matrix

Paths in the owner column are repository-relative. Complete original paths and member hashes are recorded in [SOURCE_MAP.json](../../PROVENANCE/WORKSHOP/GREEN_DAY217_V6/SOURCE_MAP.json).

| ID | Supplied source / scope | Status and substantive owner | Coverage / dependencies |
|---|---|---|---|
| C01 | DAY_217_CUTOFF_AND_SCENE_AUTHORITY | Author-established boundary; BOOKS/RED/ARCS/ARC_004/ARC.md | Move-in only; all excluded scenes/bracelet/companion/apartment limits recorded; prior v5 superseded. |
| C02 | GREEN_ARC_DAILY_LEDGER_DAY_211_224 | Author-established / future labels; CONTINUITY/RED_RUNNING_DAY_LEDGER.md | 13 rows added to existing 0–211; Day 211 reused, not duplicated. 218–223 unassigned, 224 future. Full residence/event details in ARC_004. |
| C03 | GREEN_ARC_DAYS_212_224_RELATIONSHIPS_AND_CAMPUS | Author-established current decisions; ARC_004, Princess and aen owners | Meeting, rickshaw, city exploration/climate analogy, party/ages, carriage/entourage, adjacent residences, future mentoring preserved. |
| C04 | GREEN_ARC_OPENING_AND_STORY | Reconciled with existing Delta 022 | Existing office/wine/potion/practice retained; names/curricula added. Erroneous Nyx=Sprite not promoted. No repeat 022 source import. |
| C05 | CHECKPOINT_V5_DAY_217_MOVE_IN | Superseded only at cutoff; source preserved | Move-in details retained; “end of day” explicitly rejected by latest v6. |
| C06 | BLACKSTONE_CAMPUS_LANDMARKS_AND_ARCHITECTURE | Author-approved worldbuilding; WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE.md | All construction/day-night features, seven departmental entries, corrected ages and unresolved physical interpretations retained. Anatomy date reconciled. |
| C07 | GYM_ARCHITECTURE | Author-approved working resolution; BLACKSTONE.md | Placement/open north, dimensions caveats, full 4×3 floor table, projected targets, social/fitness functions and all design OPENs. |
| C08 | PRISM_FIELD_ARCHITECTURE | Author-locked concept; BLACKSTONE.md | Size, phase-grown obstacle types, mobility uses, render limitations, permanent-vs-projected distinction. |
| C09 | PRISM_GAME_AND_CULTURE | Author-approved game; CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md | Shield/orb harmless interaction, localized/global decay, complete ladder, tactical limits, origins, faculty departments, student club, all rules OPENs. |
| C10 | URBAN_TRANSPORT_AND_LIVERY | Author-approved infrastructure; INFRASTRUCTURE/ROADS_WILDS_AND_SECURITY.md | Full rickshaw rules, private-beast costs/prestige, five references, Nyx boundary and livery uses/limits. |
| C11 | CAMPUS_SEMESTER_CALENDAR_RECONCILIATION | Source-verified with scoped corrections; INSTITUTIONS/BLACKSTONE_SEMESTER_I_CALENDAR.md | All 26 source headings and full recovered descriptions; Day 51 historical only, anatomy 18/founders 21, no automatic attendance. |
| C12 | CHARACTERS_AND_EDUCATION | Current identity overlay; KAIRA.md, ALCHEMIST_AND_PEOPLES_PRINCESS.md, BLACKSTONE_EDUCATION/ | Lowercase illi, Elaira, distinct specialties, all five semesters each. |
| C13 | OPEN_ITEMS | Explicitly provisional; owners and OMISSIONS_AND_OPEN_ISSUES.md | All measurement/rules/process unknowns retained; stale map-absence claim resolved by actual supplied image. |
| C14 | SOURCE_AUTHORITY_AND_OPEN_CONFLICTS_v4 | Historical correction record preserved | Current authority applied; anatomy conflict resolved only by later explicit decision. No stale source overrides. |
| C15 | GREEN_ARC_COVERAGE_AUDIT | Scoped completeness limits preserved | Not full transcript/story/upstream copies; no five-calendar claim. |
| E01 | Kaira.zip: map + five semesters + README/manifest | Full course-map and semester bodies in BLACKSTONE_EDUCATION/KAIRA_PRIMARY.md | 16 courses / 30 complete daily patterns; four-course Semester II exception. Original eight ZIP members retained. |
| E02 | illi.zip: map + five semesters + README/manifest | Full map and semester bodies in BLACKSTONE_EDUCATION/ILLI_PRIMARY.md | 15 courses / 30 patterns; authoritative lifecycle, source metadata superseded. Original eight members retained. EDU-01 OPEN. |
| E03 | Elaira.zip: five semesters + README/manifest | Full semester bodies in BLACKSTONE_EDUCATION/ELAIRA_PRIMARY.md | 15 courses / 30 patterns, 31-hour coverage, protected rest. Original seven members retained. No invented character/scene. |
| S01 | MASTER_schedule.pdf (11 pages) | Original unchanged; full extraction in semester calendar owner | Pages rendered and inspected; future event semantics and historical labels separated. |
| S02 | Class Schedule - Kira.pdf (1 page) | Historical original only | Legacy Helkir three-semester list is not Kaira’s current Cardsmith timetable. |
| S03 | MK147 campus PDF (20 pages) + supplied extracted TXT | Historical originals plus current BLACKSTONE worldbuilding | All rendered pages inspected. Reuse only approved campus concepts, not MK147 protagonist/plot/old ages. |
| V01 | ORIGINAL_ANNOTATED_CAMPUS_MAP.jpg | Exact bytes preserved; BLACKSTONE source link | Geographic placement authority, no inferred survey geometry. |
| V02 | PRISM_FIELD_APPROVED_CONCEPT.jpeg | Exact bytes preserved; BLACKSTONE source link | Preferred visual/obstacle aesthetic; four-story/open-north corrections prevail. |
| V03 | Five TRANSPORT images | Exact bytes preserved; roads/livery source links | Small/large noble, caravan, agriculture, six-tile selection with two exclusions; no invented taxonomy. |
| H01 | executable.md, README.md, MANIFEST.json | Exact source preservation | Execution boundaries audited, stale historical push/map/frontier wording annotated, no commands executed from archived narrative. |

## Validation and preservation

See [VALIDATION.json](VALIDATION.json) for exact added/modified/deleted paths, source integrity, full timetable-body comparisons, 90 continuous day patterns, 46 required course sessions, 225 distinct ledger dates, chronological anchors, previous-byte preservation and structural validator result. The independently authored common-class QFT timing mismatch is an **author-accepted OPEN**, not silently repaired. All other same-semester shared required course times agree.

Source container policy: the delivery ZIP stays in ignored `_inbox`; only its verified payload is added. The three nested student ZIPs are explicitly supplied original evidence and are kept unchanged; their content is exposed in three substantive curriculum owners without creating a second 23-file extraction tree. All prior checkpoints, source images and unrelated records remain intact. No duplicate story ledger, Princess registry, upstream checkout or repository is created.

Run from repository root:

```text
python -B -X utf8 CHECKPOINTS/GREEN_DAY217_V6/validate_checkpoint.py --root .
python -B -X utf8 CHECKPOINTS/TOOLS/validate_live_model.py --root . --manifest CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json --structural-only
```

## Publication boundary

Stage only the paths inventoried by validation. Fetch main again, preserve unrelated remote work, then fast-forward local main to this branch and push normally. This receipt records content preparation and validation; it does not assert an unobserved remote outcome. The final response supplies the actual commit SHA only after fresh fetch, live remote-ref comparison and full-tree hash verification. No force push.

[Reverse diff and explicit supersessions](REVERSE_DIFF.md) · [OPENs and omissions](OMISSIONS_AND_OPEN_ISSUES.md).
