# Blackstone v5.1 · targeted integration audit

Date: 2026-11-13. Repository: xApologies/MK163; target main. Baseline **2d4881f32076bb22c84701bff76b37a0b051f8fc**, clean and freshly fetched. Branch: codex/blackstone-curriculum-v5-1.

Package: MK163_BLACKSTONE_V5_1_TARGETED_CURRICULUM_CORRECTIONS_CODEX.zip. Archive SHA-256: **6f62f4874b378240d8af9bd46653e2280b3bab498c0969608bbec3213a58cd5e**. The actual handoff filename is executable.md, read under the user's request. Prior source instructions remained data.

## Exact scope and preservation

Only four teaching payload files are replaced, using the exact supplied PATCHED bytes. Six navigation/provenance documents and Git attributes carry the scoped current status; no schedule owner, story arc, narrative ledger, mathematics or inherited repository changes. The original four v5 files are preserved under PROVENANCE/WORKSHOP/BLACKSTONE_CURRICULUM_V5/ORIGINAL_DELIVERY, with all twelve original v5 members resolvable through the new [source map](../../PROVENANCE/WORKSHOP/BLACKSTONE_CURRICULUM_V5_1/SOURCE_MAP.json). The original v5 manifest, historical source map and all checkpoint/audit files are unchanged.

The [exact four-file Git diff](TEACHING_PATCH.diff) is recorded alongside reproducible validation. Reversing only the authorized title edits, authority paragraphs, optional headings and conventional prompt replacements reconstructs each original calendar exactly; the master differs only in two escaped-pipe title rows. No supporting mathematical content is discarded.

| Current file relative to TEACHING/V5 | Original SHA-256 | Result SHA-256 |
|---|---|---|
| CALENDARS/KAIRA_FIVE_SEMESTERS_ALL_SUBJECTS_DAILY_v5.md | 3846109c3c0fd78d5f925153228770e703efa7a607ea5ddbead42be4d652aad2 | 1434aa359547f139dcbd982cabc9db320efd296553550aba39d663e76c23273a |
| CALENDARS/ILLI_FIVE_SEMESTERS_ALL_SUBJECTS_DAILY_v5.md | 5726e3c198e5b8218adce82e22c8d929ac0052d0268c4a83ce434bef87a262ff | 3e9c86321dd0cbbb68299d56c771722420cb4244f7cb1777d933fe4aea4797bc |
| CALENDARS/ELAIRA_FIVE_SEMESTERS_ALL_SUBJECTS_DAILY_v5.md | 17688e8269b6a1c7cbd8998c6ccd5b7339528d67bd026441f93b6ed67b5fa30b | f4c1a82e5dbc926dd0caffd879e3574fccd4ddfb12adcc29bea27ebea6c66db0 |
| SYLLABUS/COMPLETE_FIVE_SEMESTERS_ALL_COURSES_16_WEEK_SYLLABUS_v5.md | 84a499f9f00ee8d3df82619c01118add42a386f257191b1c20215f0465410ad2 | 9e30ddf1a02ac71ed4d60d24993991ad187c12d591b3ca24d0a718f8b5b04505 |

## Validation

Final inventory: **13 files added, 11 modified, 0 deleted**. All 860 untargeted prior files are byte-identical. This includes every schedule owner, story arc, narrative ledger, historical checkpoint and pre-existing provenance file.

All four base hashes matched the working tree and fetched main before editing. All seven declared new hashes pass; the eighth member, the manifest, is also hashed in the source map. ZIP CRC/path/case/symlink/encryption/size checks pass.

The three calendars retain 480 days each, five semesters of Days 1–96, sixteen six-day weeks, and Kaira 256 / illi 240 / Elaira 240 class entries. All 736 required entries match existing class names and times; 512 master rows cover 32 semester/course sections; all 160 shared weekly groups agree. Aiven rest, EDU-01/02 and Kaira Semester II Ailor 15:00–17:00 remain intact. The story stays at end of Day 217.

The six corrected daily titles and two master rows preserve the mathematical pipe. All 400 Genesis entries have exactly one primary source paragraph and one explicitly OPTIONAL preserved seminar; 215 refer to different supporting chapters and 185 repeat the primary chapter. All 336 conventional prompts name their actual topic and discipline. No old double-brace example remains in current calendars.

Current source ref checks confirm _bricked bootstrap/canonical-architecture **c89676fc26000ae6f5fdad66a56e118b285d9b1d** and AERA main **42437950ad2aa72ad885ff1a9129226da23d9286**. Primary formal passages and primary/supporting chapter numbers are unchanged from the verified v5 corpus; that [pinned audit](../BLACKSTONE_CURRICULUM_V5/SOURCE_REVIEW.md) is reused, not represented as a new whole-corpus proof. Fifteen chapters are primary anchors; 43, 49 and 56 occur only among supporting references. All eighteen FORMAL/39–56 source paths remain accounted for.

[VALIDATION.json](VALIDATION.json) records exact file counts, all source hashes, preservation and structural checks. No material canon or scheduling conflict remains.

## Resolved corrections and remaining limits

The earlier split-title and topology ambiguity findings are resolved for current lesson titles/prompts. The distinction between primary and supporting material is explicit. Some inherited short transfer/objective labels and detached after-class fragments remain in the exact patch; the corrected full title governs them. Generic delivery-plan references to a board/independent problem are governed by the new primary-authority paragraph, not a requirement to teach the optional seminar. [Current reading notes with all earlier audit history](../../WORLD_CLOCK/L2_WORLD_CIVILIZATION/INSTITUTIONS/BLACKSTONE_EDUCATION/TEACHING/V5/READING_NOTES.md).

Conventional prompts still require actual problem selection, solutions and prerequisite support before scene writing. They are not 336 verified worked solutions. Attendance, mastery and experiments remain narrative questions. V4 allocation differences, unavailable predecessor daily files, the old inaccurate v8-ledger inclusion claim and individual Astrius/Vera volume references remain documented. No new theorem, ability, extra course or completed event is inferred.

## Reproduce and publication

~~~text
python -B -X utf8 CHECKPOINTS/BLACKSTONE_CURRICULUM_V5_1/validate_checkpoint.py --root .
git log -1 --format=%H -- CHECKPOINTS/BLACKSTONE_CURRICULUM_V5_1/INTEGRATION_REPORT.md
~~~

Historical v5 reports/validator describe their own commit; the current v5.1 validator checks both original and patched payloads through the preservation map. The final execution response gives the actual new SHA and remote verification after normal push; this precommit report does not claim a future push has already succeeded.
