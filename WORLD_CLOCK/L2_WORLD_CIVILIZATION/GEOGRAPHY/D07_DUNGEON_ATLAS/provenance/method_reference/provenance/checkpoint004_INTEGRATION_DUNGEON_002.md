# Codex integration — cumulative Dungeon Atlas 002

Read this supplement together with the unchanged `INTEGRATION_FOR_CODEX.md`. This revision adds local dungeon geography only; it does not broaden authorization to unrelated projects or replace whole repositories.

## Destination

Map package prefix `MK163/` to `xApologies/MK163` with that prefix removed. New local geography lives at:

`WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON_ATLAS/`

Retain one data authority (`data/dungeon_graph.json`) plus synchronized exports, diagrams, viewer, validation and tooling. Add a scoped link from `WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON.md`, the World Clock index, and `BOOKS/RED/ARCS/ARC_006/ARC.md`. Reuse existing index conventions. Do not duplicate the 1,245-record Shaping catalogue into this folder or relocate it to MK163 Level 1.

The original AERA/MK727/MK163 payload and original integration instructions remain intact. Reconcile each original file against live HEAD; do not reapply already integrated changes or replace newer remote edits.

## Required authority treatment

Preserve author-selected vertical bands and E-W principal widths 3/5/8/11/16 miles. Record natural forests, waterways, shafts, chasms, loops and terminal branches; no constructed or carved bridges. The 70/30 Yellow forest composition is illustrative, not universal.

Label exact node coordinates, north-south spans, edge centerlines and node counts as design proposals. Do not promote every generated value to locked physical canon simply because it is in a CSV. No Violet layer, no new absolute-bottom assertion, no new Tournament marker, no dated expedition, no automatic historical-site relocation.

Existing research/harvest/rescue places must be anchored deliberately in a future pass. Keep their old authority and depths intact. Do not interpret graph distances as travel-time facts or infer fly-through accessibility.

## Procedure

1. Inspect live remote branch/HEAD and destination files; record actual SHAs. This package contains no claim to a current remote HEAD.
2. Validate root manifest SHA-256 values, inherited six-file preservation, catalogue identity and graph consistency.
3. Integrate new folder and links, preserving existing detailed canon. In the ARC_006 narrative, retain the author correction that the Genesis Robe demonstrates potential Architect capacity; do not introduce formal Architect status from an old overview phrase.
4. Run `python tools/validate_graph.py --atlas-dir <destination>` from the atlas tools or equivalent validation. All node IDs, endpoints, polylines, depths, widths and terminal constraints must pass.
5. Regenerate views only from the same JSON. Never redraw top-down maps independently or renumber nodes by view. Append future IDs rather than reusing them.
6. Add `CHECKPOINTS/VIOLET_DUNGEON_002/INTEGRATION_REPORT.md` with source package hash, files changed, previous/new HEAD, validations, and open issues. If a prior checkpoint name is already used, reconcile rather than duplicate.
7. Commit and push only within the authorized repositories and permissions. Report actual remote SHAs or PR/block status; never claim a push without verification.

## Carry-forward rule

New workshop checkpoints must retain all compatible prior payload and catalogue content; preserve superseded evidence with an explicit supersession record. Root manifest updates are normal, but old evidence must not disappear. This package preserves the prior manifest in provenance and keeps all six original payload files byte-identical.
