# executable.me / execution.md — MK163 Delta 005 authoritative Codex handoff

## Objective
Apply the **substantive, topic-specific missing MK163 workshop content** in this archive to the existing `xApologies/MK163` repository. This is an ADDITIVE REVERSE-DIFF reconciliation, not a repository replacement, not an import of upstream corpora, and not a request to author new chapters.

## Repository and verified baseline
- Target: https://github.com/xApologies/MK163
- Branch observed: `main`
- Git tree SHA observed: `bfd51233d73c4e572fdedc2a0fca51af50af81b2`
- Complete recursive Git tree enumerated: 336 entries.
- Principal current MK163 owner files inspected: 18 (listed in `BASELINE_REPOSITORY_AUDIT.json`).
- Governing documents reviewed: `AGENTS.md`, Constitutions 00, 08, 09, 10, 11, 12, 13, World Clock index and current Arc 1/2, selected L2/L3 records.
- This baseline is NOT a claim that every file was semantically read. Before applying, Codex must check HEAD and finish content comparison with all relevant owners.

## Procedure
1. Open the existing local MK163 Git working tree. Read `AGENTS.md`, `CONSTITUTIONS/00_AUTHORITY.md`, `CONSTITUTIONS/08_CODEX_WORKFLOW.md`, `CONSTITUTIONS/09_CHANGE_CONTROL.md`, `CONSTITUTIONS/10_EXHAUSTIVE_LIVE_MODEL.md`, `CONSTITUTIONS/11_LIVE_MODEL_MIRROR.md`, `CONSTITUTIONS/12_EXPORT_ACCEPTANCE_AND_CANON_GUARDS.md`, `CONSTITUTIONS/13_ARC_PIPELINE_AND_LEAN_INHERITANCE.md`, `WORLD_CLOCK/CURRENT_MODEL_INDEX.md`, and relevant continuity/provenance.
2. Record branch, HEAD SHA and clean/dirty status. If local changes conflict, STOP and report. Do not reset, force push, clean or delete.
3. Extract this ZIP into a safe temporary directory OUTSIDE the tracked repository. Never commit the ZIP or stage ignored `_inbox`. Markdown is a Codex prompt, not a shell script. Reject symlinks, absolute paths, `..`, unsafe destinations and case-insensitive path collisions.
4. Verify each payload file against `MANIFEST.json` SHA256 and byte count. Compare `BASELINE_REPOSITORY_AUDIT.json` with the actual current tree; if HEAD changed, use current canon with explicit conflict reporting.
5. For each payload file, identify the ONE active canonical owner under existing World Clock, BOOKS, CONTINUITY or PROVENANCE. Perform a real **reverse diff**: inspect what the current repository already says, isolate the workshop statements that are absent, and add only those. Keep the full detailed payload record as linked provenance/supplement if the owner would otherwise lose context. Do NOT copy unchanged upstream AERA, MK147, MK157, MK727, MK Ultra, API or `_bricked` files into this repo.
6. Preserve exact original 26 city key names plus three approved additions, the spatial-ledger rules, Blacksmith Row corrected architecture, alchemical paste, table modes, royal agriculture history, numeric domai radii, White Dust political economy, and Kaira's Awakened/Afflicted noble-origin rumor. Never flatten detailed source evidence to a brief synopsis.
7. Correct Arc One active chapter order: C1 apothecary/card/departure; C2 day-one delivery + day-two collapse + Stone Hollow gate; C3 alchemist, healing, White-heavy Awakening; C4 return route and escape; final 2–3 chapters caravan transfers and Violet city arrival. This supersedes the old 5-beat outline only in explicitly changed areas. **She does not return to smithy for possessions.** Preserve other existing Arc One material.
8. Preserve Arc Two's existing macro plot and Nyx ecology. Opening scene is first of three apartment viewings with failed haggling. Arc Two ends with first robe completion/public reveal. Arc Three owns first Black Sprite Binding. Do not invent street coordinates, named merchants, noble lineage, prices or extra chapters.
9. Add series-wide status motif: visibly Awakened with retained Afflicted pigmentation, commoner/noble reactions, presumed estranged noble origin, rumors expanding with fashion prominence. Kaira is not secretly noble by fiat.
10. Verify all quantitative locks: 31-hour day; 6.6-mile hub→Riverbend and 9.4-mile Oak Hollow→Stone Hollow; delivery itinerary 2→5→3→8→7→5; seven mushrooms minus three potion minus one alchemist equals three retained; domai exterior radii 3/5/7/11/13/17 miles, interior ×1.7; 29 city-key entries 26+3; 10×10-mile city = 100 square miles; 660-ft eighth-mile block; three city gates per side; Blacksmith Row upper suites RECESSED and NO overhang.
11. Read `PROVENANCE/DELTA_005_VERBATIM_AUTHOR_EVIDENCE_EXCERPTS.md`. These are excerpts, not a full raw transcript. Do not manufacture missing quotes. Record any unresolved source fidelity limitation in import report. Keep historical quotes' dictation spelling, normalize active Kaira, Nyx, vaen, raeon, maege/maegi.
12. Update existing topic owners, World Clock index, arc contracts, continuity ledger, corrections, source register, and coverage matrix. Preserve existing detailed evidence and prior decisions. Do not create a parallel 'V2' World Clock.
13. Produce `PROVENANCE/DELTA_005_IMPORT_REPORT.md` and JSON with topic IDs, target owners, added/modified/skipped/conflicted paths, before/after SHA256, unresolved details, and semantic preservation checks. Verify no existing detailed content was shortened or removed.
14. Validate links, Markdown, naming, Windows case collisions, current author corrections, no unrelated changes, no file larger than repo policy, and all hard checks of Constitution 12. Inspect full `git diff` and `git diff --stat`. Halt on destructive conflict.
15. Commit and push only under existing authorized workflow and after successful validation. Never force push. Fetch remote HEAD after push and report actual commit SHA and import report.

## Important scope guard
The user explicitly requested **no imported copies of upstream or already-present files** merely to inflate ZIP size. The package contains new detailed MK163 workshop records, provenance, baseline audit, coverage and instructions. It is not a backup of MK163, and missing ZIP files never authorize deletion.

## Acceptance gate
This is a substantive integration delivery. **Do not claim COMPLETE—WORKSHOP unless every accessible author decision in this thread has a source/evidence path and coverage check.** If full raw transcript is unavailable, state the limitation plainly. Do not reject all usable author-approved additions merely because the original chat transcript cannot be recovered byte-for-byte; reconcile nonconflicting verified decisions, and separately report source-fidelity limitations.

## Additional mandatory handoff files
Read `COVERAGE_MATRIX.json`, `COVERAGE_MATRIX.md`, and `RECONCILIATION_RULES.md` before merging. Each coverage row has an exact target owner. Do not ignore any row. Produce a row-by-row import report with status merged/already-present/conflict/open and source citation. Do not treat duplicate explanatory transport records as competing canon.
