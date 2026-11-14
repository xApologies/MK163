# Verifying the completed Semester III live model

## Inventory and integrity

1. Confirm the repository is `xApologies/MK163`, identify the review branch and inspect its diff against the approved baseline. For documentation changes, compare the dated schedules, break record and administration record byte for byte with that baseline.
2. Enumerate `WEEK_01` through `WEEK_16`. Each contains six unique `DAY_*.md` files. The directory, heading, weekday and story day must agree. Days 452–547 occur once each, and each student timetable covers 00:00–31:00 without gaps or overlaps.
3. Compare the file inventory with `SHA256SUMS.json`. The manifest lists every file below this directory except itself. For approved edits, update only the affected SHA-256 values in the existing format, then hash every listed file and compare.
4. Run the repository structural validator and `git diff --check`. Review the changed paths before staging. Preserve prior checkpoints and record any source disagreements in the integration notes.

## Examination timetable

Examinations use the established class slots. Read across a row for the three examination cycles.

| Course | Students | Time | Week 5 · Exam I | Week 10 · Exam II | Week 16 · Final |
|---|---|---|---:|---:|---:|
| Genesis Field Theory III | All three | 13:00–15:00 | 476 | 506 | 542 |
| Quantum Field Theory I | Kaira and illi | 11:00–13:00 | 478 | 508 | 544 |
| Differential Geometry II | Elaira | 17:00–19:00 | 478 | 508 | 544 |
| Chemistry I | Elaira | 11:00–13:00 | 480 | 510 | 546 |
| Transduction Theory I | Kaira and illi | 18:00–20:00 | 480 | 510 | 546 |

Check subsequent student blocks in the Exam II and finals weeks. Preparation for each course ends when that examination finishes. Ordinary subject review in Week Five has its own dated entries. [Week Five](WEEK_05/README.md) · [Week Ten](WEEK_10/README.md) · [Finals](WEEK_16/README.md)

## Events and calendar

- Compare the Aiven attendance index against each dated schedule. Check the 13:00–17:00 raeon window and the 13:00–23:00 Prism window from Day 505. Account separately for selected attendance, city outings, Elaira’s clinical commitments and optional spectating. [Aiven index](AIVEN_CITY_TRIP_OPPORTUNITIES.md)
- Check the Black Sprite’s independent 16:00–18:00 professor visits beginning Day 454 on Ailar–Aithen. Read the Week One prose and the later Sprite columns, including split-hour cells. Aiven has no appointment. [First visit](WEEK_01/DAY_454.md)
- Check seven contiguous calendar periods, three 96-day semesters, three 18-day breaks and 11 administrative days, across Story Days 224–576. Verify Break III against its city-based record. Administrative activities remain OPEN. [Break III](BREAK_III/BREAK_III_DAYS_548_565.md) · [Annual calendar](YEAR_END_ADMINISTRATION/CALENDAR_RECONCILIATION.md)
