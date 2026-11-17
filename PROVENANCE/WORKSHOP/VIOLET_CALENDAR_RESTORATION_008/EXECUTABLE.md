# Codex execution instructions — MK163 calendar restoration and Violet schedule replacement

Target repository: `xApologies/MK163`.

## Objective

Replace the **incorrect active Violet Checkpoint 007 calendar and daily schedule** with `VIOLET_CORRECTED_DAILY_LEDGER.md` and `.csv` from this ZIP. This is an author-approved schedule replacement. The earlier rotated weekday list is **invalid**. Preserve the historical Blue/Green/Blackstone storyline and all other canonical material.

## Source authority and calendar (NON-NEGOTIABLE)

- Original weekday order: **1 Ailar, 2 Aiden, 3 Aiveth, 4 Ailor, 5 Aithen, 6 Aiven**.
- Day 0 = **Aelora 5, Aithen (weekday 5)**.
- Original eleven month lengths: Aelor 33, Aerith 32, Aelora 31, Aevrin 33, Aelis 31, Aevor 32, Aelith 33, Aerion 32, Aeveth 31, Aesith 33, Aeleth 32; total 353.
- Weekday number for nonnegative story day d = `((d + 4) % 6) + 1`.
- King's weekly raeon salon = **Aithen, weekday 5**; local shop tournament = **Aiven, weekday 6**.
- Story day, civil month/day, and weekday are distinct coordinates. Never reset weekday sequence at month or semester boundaries.

## Required operations

1. Inspect the current default branch and identify all **active** references to the erroneous Violet 007 rotated weekday ordering, the royal games on 1085/1139, and the invalid 1081–1086 vaelum-arrangement/travel text. Produce a list of paths and their roles before editing.
2. Replace `BOOKS/RED/ARCS/ARC_006/VIOLET_DAILY_LEDGER_007.md` as an active authority with the supplied `VIOLET_CORRECTED_DAILY_LEDGER.md` content, preferably at a clearly versioned `VIOLET_DAILY_LEDGER_008.md` and corresponding `.csv`. Update `ARC_006/ARC.md` and the current model index to point to 008, not 007. Do not leave two competing **active** daily schedules.
3. Update the Day 1081–1159 rows of `CONTINUITY/RED_RUNNING_DAY_LEDGER.md` to match the supplied CSV, retaining the existing month/date and unrelated continuity links where applicable. Keep Day 1080 Blue closure intact.
4. Restore the original weekday order in `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ASTRONOMY/STARSCAPE_AND_CALENDAR.md` and remove or supersede the 007 rotated ordinal rule from active text. Preserve the historical 353-day calendar, original month lengths and earlier source evidence.
5. Correct `WORLD_CLOCK/L2_WORLD_CIVILIZATION/CULTURE/GAMES_SPORTS_AND_DAILY_LIFE.md`: King Aithen (weekday 5); local card shop Aiven (weekday 6). Preserve historical Blue salons and local tournament dates. Remove false active assertions that Ailor is weekday 5 or Aiven is weekday 1.
6. **Remove obsolete corrupted active Violet files** (including superseded 006/007 schedule copies and redundant active aliases) only after determining their exact dependency references. Delete outdated duplicate schedule files from active story directories if they are no longer referenced, and update all links. **Do not bulk-delete unrelated files, Blackstone timetables, route atlas assets, expedition records, provenance/workshop evidence, or prior source documents.** Retain a concise supersession record in the repository explaining what was removed and why. Preserve historical original material in Git history; no force-push or history rewrite.
7. Reconcile `WORLD_CLOCK/CURRENT_MODEL_INDEX.md`, relevant checkpoint index/readmes and Violet ARC_006 references so 008 is the only active Violet daily ledger. Historical checkpoint notes may remain explicitly marked historical, but must not masquerade as current canon.
8. Preserve expedition durations/routes and the author's selected events exactly; do not shift 1087–1097, 1103–1117, 1123–1135, 1143–1159. No new royal game on 1085/1139, no invented capital visit during 1081–1086, no tournament on 1120.

## Validation and reporting — REQUIRED BEFORE COMMIT

- Verify 80 consecutive story days 1080–1159 (including Blue closure), all original month/day coordinates, and all weekday names/ordinals.
- Verify no event on 1085/1139 is called a King's salon; 1098 and 1140 are both Aithen/5.
- Verify 1081–1086 are six recovery/slice-of-life days; Illi visits 1099–1100 and 1141; returns 1101 and 1142.
- Verify Yellow 11 days, Blue navigation 15 and 13 days, Green 17 days; exact endpoints retained.
- Validate all 1,160 running-ledger rows (Day 0–1159) against original calendar, flagging any mismatch without changing historical scenes.
- Check broken links, duplicate active authorities, and unintended deletion; summarize changed/deleted paths.
- Commit the changes only after validations pass; provide commit SHA, diff summary and validation counts. If any unexpected dependency or ambiguity arises, STOP and report it rather than inventing an answer.

**Destructive-operation boundary:** User explicitly authorizes deletion of obsolete corrupted Violet schedule copies. This does NOT authorize deletion of entire checkpoints, provenance, original source archives, or unrelated story content.
