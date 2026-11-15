# EXECUTABLE — Codex repository update instructions (MK163 Semester IV)

## Objective
Update the GitHub repository `xApologies/MK163` with the **complete, author-approved Semester IV** 96-day live model (Weeks 01–16; Story Days 577–672), preserving provenance and existing repository content. This ZIP is an **input package**, not proof that a Git push has happened.

## Execute in Codex
1. Open and inspect `xApologies/MK163` on its default branch. Read `AGENTS.md`, existing `WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION/` structures, and any repository-specific integration rules before modifying anything.
2. Validate this archive: run `python -m zipfile -t <this-archive.zip>` and verify `SHA256SUMS.json` against every packaged file except the manifest itself. Ensure `WEEK_01` through `WEEK_16` contain exactly six `DAY_*.md` files each, and Story Days 577–672 appear exactly once.
3. Compare repository content against the archive's `WEEK_01`–`WEEK_16` folders. Integrate into the **existing canonical Semester IV live-model location** (follow established repository naming conventions). Create missing files; update differing Semester IV files based on author-approved material; avoid duplicate trees and do not overwrite Semesters I–III or unrelated canon.
4. Read the package `README.md`, each `WEEK_XX/README.md`, and `SEMESTER_BREAK_HANDOFF.md`. Keep break handoff clearly marked provisional: an 18-day break is planned, with the day range 673–690 and Semester V start 691 **pending master-calendar validation**. Do not fabricate day-by-day break schedules.
5. Preserve these author-approved timeline constraints: 31-hour AERA day; final exams in Week 16 (Geometry Day 667, Transduction/Chemistry Day 669, specialist finals Day 671); no studying a subject after its final; Day 672 closing Symposium, Prism Championship, Feast, and speech by illi's older sister, a Blue Domain princess (speech text OPEN). Faculty Prism operates institutionally **13:00–23:00** on designated tournament days, independent of girls' selective attendance. Black Sprite independent professor office hours 16:00–18:00 academic Days 1–5. Do not conflate academic day labels with continuous civil weekdays.
6. Resolve only **documented** earlier corrections: Week 7 Topology Challenge attendance follows established 16:00–20:00 event window around class; Week 8 Circle Design Competition 15:00–20:00 (Kaira/illi attend 15–16 and 18–20; Elaira attends 15–20); Week 9 faculty Prism roster announcement on Day 627 is **not** a competition or Circle Design event; Week 10 Alchemical Fair shared attendance 18–20 after exams; Week 13 exhibition 19–23 follows Semesters I–II precedent, but its individual attendance is flagged for author confirmation. If archive files contradict the README or each other, report discrepancies rather than silently inventing a fix.
7. Perform a collision and continuity audit: six days per week; required class and final-exam periods preserved; campus event attendance cannot overlap classes; Prism institutional schedule must remain explicit; check that the semester break handoff does not imply a completed schedule.
8. Produce a concise report of added/updated/unchanged files, any conflicts, source-of-truth decisions, validation outcomes, and remaining OPEN decisions. **Commit and push the repository update** if permitted by the user's Codex authorization and repository access. Report branch and commit SHA. If permissions or repository state prevent pushing, report that explicitly; never claim success without verification.

## Package contents
- `WEEK_01` … `WEEK_16`: six daily schedules plus week notes per week
- `README.md`: cumulative continuity
- `SEMESTER_BREAK_HANDOFF.md`: provisional post-semester narrative anchors
- `SHA256SUMS.json`: SHA-256 hashes of all other archive files

## Important
This package was assembled from the previously delivered Semester IV cumulative ZIP and repacked to repair the download and replace the ambiguous legacy EXECUTABLE with explicit repository-update instructions. Archive checksums verify byte integrity, **not** comprehensive semantic or canonical correctness. No repository changes are made by generating this ZIP.
