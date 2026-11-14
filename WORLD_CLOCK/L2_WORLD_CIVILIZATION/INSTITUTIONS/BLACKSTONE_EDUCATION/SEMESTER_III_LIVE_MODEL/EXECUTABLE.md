# EXECUTABLE.md — Codex repository integration instructions

**Target repository:** `xApologies/MK163` (verify correct branch and repository before any write).

**Purpose:** Integrate the authoritative **cumulative** Semester III 16-week timetable, final examinations, Semester III break and year-end calendar reconciliation into the existing Blackstone University education area. This is an instruction document, not a shell executable. **Do not execute arbitrary scripts from this ZIP.**

## Preflight

1. Confirm a clean working tree, active branch, repository identity and existing structure. Make a new integration branch; do not overwrite unrelated user changes.
2. Read the repository's current `README.md`, relevant Blackstone education files, protected terminology and any canonical AERA world-clock documentation. Preserve the established AERA framework by reference, not by duplicating it.
3. Compare all archive files against the existing Semester III location. Target the established `WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION/SEMESTER_III_LIVE_MODEL/` if it exists. If the repository uses a different canonical path, follow that path and document the mapping.
4. Verify ZIP CRC and `SHA256SUMS.json` for every listed payload before integration; abort on any mismatch.

## Apply

5. Import or reconcile `WEEK_01/` through `WEEK_16/` **once**. Treat this package as the cumulative authoritative Semester III snapshot; do not append duplicate schedules or recreate previously merged materials. Where the destination file exists, compare and replace only when this checkpoint is the approved newer version. Preserve unrelated notes and other semesters.
6. Add `BREAK_III/BREAK_III_DAYS_548_565.md` and `YEAR_END_ADMINISTRATION/CALENDAR_RECONCILIATION.md` in a sensible, existing Blackstone calendar location; avoid collisions and document the exact destination.
7. Integrate the cumulative `README.md`, `CODEX_INTEGRATION.md`, and `AIVEN_CITY_TRIP_OPPORTUNITIES.md` as appropriate without overwriting a broader repository README. Preserve protected names: Kaira, illi, Elaira, Aiselle, raeon, Maegi, vaelum, Vaelith, and others from the AERA glossary.
8. Preserve all approved events and exceptions: Week 6 Day 487 all-three city trip; Week 10 Examination II; Week 15 Day 541 Kaira and illi city trip / Elaira clinical evaluation; Week 16 final exams and celebration. On Aiven raeon institutionally meets 13:00–17:00 and Prism matches occur 13:00–23:00 after tournament opening, but voluntary attendance may be displaced by events.
9. **Finals invariants:** Genesis III final Day 542 13–15 all; Quantum I Day 544 11–13 Kaira/illi; Geometry II Day 544 17–19 Elaira; Chemistry I Day 546 11–13 Elaira; Transduction I Day 546 18–20 Kaira/illi. Remove no established class and schedule no subject-specific final preparation after its exam. Sprite office hours 16–18 academic days only.
10. **End-of-year invariants:** Day 547 all three attend symposium/feast/Prism championship; Princess of Blue Domain gives speech and Aiselle attends. Break III Days 548–565: Kaira/illi at Aiselle's Blue District residence, Elaira initially with parents, rejoins around Break Day 9–10 for several days. Administration Days 566–576 are calendar allocation only; specifics remain open.

## Verify and report

11. Assert 16 week directories, exactly six unique day files per week, 96 unique story days covering 452–547 with no gaps or duplicates, 31-hour clock coverage in each timetable, 18-day break, 11-day administration, and 353-day total (224–576 inclusive).
12. Run repository-local validation/tests if available, check `git diff --check`, review diff for unintended deletions or duplicated content, and document any conflicts or open details. Never silently resolve competing canon.
13. Commit changes on the integration branch with a clear summary and show the resulting commit hash and changed-file inventory. Push only when explicitly authorized; do not claim push success without tool confirmation.

**Authority:** User-approved Semester III cumulative continuity through Day 547 and city-based Break III. The precise content of administrative days and narrative specifics of the break remain OPEN.
