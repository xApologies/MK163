# Green Day 217 v7 · focused curriculum repair

Baseline: `8f23e7cad7761e7889ab1a8c0f8253fd1cc83085`, clean and freshly fetched from xApologies/MK163 main. Work branch: `codex/green-day217-v7`. Package: `MK163_GREEN_DAY217_EDU_SCHEDULE_RECONCILIATION_v7.zip`; SHA-256 `c2accbea0042e093824cf40f6a7388aacc801934da974d7fd01096b694d97535`.

The user requested integration under `executable.md` (the actual archive spelling). Its current education correction was read as the authorized handoff; historical material remained evidence, not new execution permission. This is an accumulated repair, not a repeat v6 integration.

## Coverage and reverse diff

| Topic | Before | Current change / target | Preservation boundary |
|---|---|---|---|
| EDU-01 | Same-section requirement, Kaira 11:00–13:00 versus illi 13:00–15:00, explicitly OPEN | RESOLVED: both Semester III QFT I Aiveth 11:00–13:00. illi 13:00–15:00 optional review. Corrected full member in existing BLACKSTONE_EDUCATION/ILLI_PRIMARY.md | Original v6 illi archive remains exact; Kaira required rows unchanged |
| EDU-02 | illi Aiveth notes misplaced Elaira Chemistry; shared 18:00–20:00 overlapped her lecture | RESOLVED: Elaira Chemistry I Aithen 11:00–13:00; DG II Aiveth 17:00–19:00. illi optional block split 18:00–19:00 Kaira/illi, 19:00–20:00 all three | Elaira original rows unchanged; optional means optional, not completed attendance |
| Other education | Fifteen semester records and course maps | All checked: 90 continuous 31-hour daily patterns and 46 required course sessions; shared required sections agree | Other fourteen semesters, course maps and every untargeted row unchanged; no new timing discrepancy found |
| Current references | OPEN labels in curriculum prefaces, Blackstone, AGENTS, index and current OPEN register | New scoped RESOLVED authority plus current source links | Earlier labels retained as dated history; historical checkpoint reports/validators unchanged |
| Cumulative payload | Repeats v6 canon/images/PDFs/student sources | Reuse 30 exact hash-matched files; preserve four new/changed files and a source map | No full duplicate checkpoint, new repository, inherited edits or source shortening |
| Narrative and chronology | Day 217 move-in only; future unscheduled 218–223; semester starts 224 | No change | Green narrative owner and running ledger byte-identical; researcher/lunch scene remains unapproved; Orange/Yellow untouched |

## Manifest and source treatment

Current `MANIFEST_v7.json` covers all other 33 archive members and passes every SHA-256. The retained v6 `MANIFEST.json` is explicitly historical: its old `executable.md` and `illi.zip` hashes refer to the unchanged v6 originals, not the new v7 versions. Those two expected differences are recorded, not hidden as current-manifest failures.

All 20 declared hashes in the three student ZIP manifests pass. New illi ZIP contains nine members: six unchanged originals, corrected Semester III, refreshed inner manifest and a reconciliation note. The note is not enumerated in the inner manifest; its bytes exactly equal `EDU_RECONCILIATION_v7.md`, verified against the current outer manifest. All 24 nested source members are accounted for. No source metadata is silently repaired. The corrected semester-body SHA-256 is `47c08f9554e1e83d5de5ec63c1e1c7034f9d1a4bef358de1b9ed9bec84422ec9`.

The full original corrected Semester III document is retained in the current owning file; its former v6 body remains recoverable in the unchanged v6 source ZIP and Git history. Only the author-selected Day 3 rows, status and alignment wording differ. All source bytes, including seven images and three PDFs reused from v6, remain accounted for by [SOURCE_MAP.json](../../PROVENANCE/WORKSHOP/GREEN_DAY217_V7/SOURCE_MAP.json).

## Validation and remaining scope

[VALIDATION.json](VALIDATION.json) records hashes, source reuse, exact-body preservation, all-student/five-semester timetable checks, shared-section alignment, optional-study eligibility, unchanged historical content and exact file inventory. The existing structural validator also passes. EDU-01 and EDU-02 have no remaining unresolved conflict. Unrelated v6 OPENs remain; this limited repair does not claim complete conversation recovery or finish the Green narrative.

Reproduce from repository root:

```text
python -B -X utf8 CHECKPOINTS/GREEN_DAY217_V7/validate_checkpoint.py --root .
python -B -X utf8 CHECKPOINTS/TOOLS/validate_live_model.py --root . --manifest CHECKPOINTS/LIVE_MODEL_003_DELIVERY_MANIFEST.json --structural-only
```

Only verified paths are staged. Publication uses a normal push after a fresh fetch, followed by remote-SHA and complete Git-tree verification. The actual commit SHA and remote status are reported after those checks; this preparation receipt does not predict their result.
