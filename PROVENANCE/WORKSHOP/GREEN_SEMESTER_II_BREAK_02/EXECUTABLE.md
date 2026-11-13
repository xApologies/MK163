# EXECUTABLE.md — Codex integration handoff, MK163 Semester II Break Checkpoint 02

## Target and boundaries
Repository: `https://github.com/xApologies/MK163`.
This is the **final cumulative break checkpoint of the new Semester II series**. It supersedes the separate Break Checkpoint 01 ZIP. Do not ingest both as separate additive patches, and **do not** re-import the completed Semester I ZIP. If the Semester I handoff has not yet been integrated, report that dependency and avoid overwriting or silently reconstructing it.

## Execution
1. Inspect the checked-out repository, branch, HEAD, status and relevant current owners before editing. Do not assume a prior ZIP was pushed.
2. Unpack into a temporary directory, reject unsafe ZIP paths and symlinks, check CRC, and verify `MANIFEST_SHA256.txt` for every member except the manifest itself.
3. Read `README.md`, all `CANON/*.md`, `CONTINUITY/BREAK_LEDGER.csv` and the unchanged author-supplied map before changing repository files.
4. Integrate Day 319 Alchemist feast addendum, Days 320–340 break chronology and Day 341 Semester II anchor into the existing Green Arc narrative owner (`BOOKS/RED/ARCS/ARC_004/ARC.md`) or an appropriately linked Green Arc continuity file. Do not overwrite existing prose, invent completed scenes or create duplicate day-ledger entries.
5. Integrate **Princess aina** (exact lowercase), illi's older sister and Blue Domain ruling princess, her **White District palace**, and the two personal commissions in existing character and chainmail owners. Preserve illi's existing personal residence and her relationship with the Alchemist. Do not invent a palace name, commission prices or ring delivery.
6. Reconcile with existing institutional/economic owners: `WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/PROFESSIONS/BLACKSMITH_ROW_AND_ARTISANS.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/ARMOR_AND_CHAINMAIL_PRICES.md`, and the established Yellow-to-Green/Blue travel and Alchemist records. The prestigious Blacksmith Rows are in **Yellow District**, not White/Blue/Green; the Alchemist lives in **Blue District**; aina's palace is in **White District**, all within the Blue Domain capital.
7. Preserve the approved **353-day academic cycle** and Semester I's completed 96-day model. Place Nyx's living Red-to-Violet flower wall in the existing creature/environment owner as a retrospective Semester I development; it is not first created on Day 320 and is not transported to the Alchemist's apartment.
8. Record E's gift robe completed during Kaira's visit and presented on Day 331. Day 332 ring order is for **two different new robes**: Princess aina's and the unnamed smith's. Keep Registry-managed originals, knockoffs and personal commissions distinct; capacity is not guaranteed sales.
9. Preserve exact terms and names: `Kaira`, `illi`, `aina`, `Elaira`, `Nyx`, `raeon`, `vaen`, `Black Sprite`. The Black Sprite is distinct from the mature Sprite Professor, whose standing mentorship has ended. Never infer new biological powers from the wall or from Kaira's bond.
10. Check whether the original conceptual domain map is already present before adding `SOURCES/AUTHOR_DOMAIN_MAP.jpeg` to provenance; avoid duplicate assets. The violet map marker in the Blue Domain identifies the Blue capital, not the Violet Domain.
11. Update links/indexes and the single running day ledger with scoped, nonduplicative references. Do not invent a new top-level Blackstone directory if the institutional owner already exists.
12. Run repository checks and `git diff --check`, inspect the full diff for unintended changes, then commit and push to the authorized repository branch **only if permissions and credentials permit**. Report changed files, commit SHA, push result, checks and unresolved issues. Do not claim success without a successful remote push.

## Scope caveat
The user has selected these macro-events, but the full 21-day daily schedules, scene dialogue, commission details, exact smith identity, ring quantities and arrival dates remain OPEN. Treat `CANON/BREAK_320_340_AUTHOR_OUTLINE.md` as the current authority over older outline placements.
