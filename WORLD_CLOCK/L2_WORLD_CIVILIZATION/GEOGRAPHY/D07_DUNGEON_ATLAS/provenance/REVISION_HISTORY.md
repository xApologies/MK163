# D07 revision history

## D07_ATLAS_001 - first structural build

This is the first D07 atlas in the established MK163 mapping system. D07 is Violet-ending in the Blue political Domain, with a selected maximum modeled depth of 24 miles and boundaries `0 / 1.5 / 3.5 / 6.5 / 11 / 17 / 24` miles.

The immediate implementation baseline is D06, continuing the configuration-driven adaptations of Dungeon Mapping Method 001. D07 uses its own parameters and seed **1630701**. Six strata, Red through Violet, are represented by real graph records; the Blue and Violet plans are generated from those records.

The resulting graph is the continuing D07 spatial model. Node and passage IDs are assigned once and remain stable for subsequent displays and overlays. Local IDs are scoped by `dungeon_id: D07`.

## Preserved provenance

- `provenance/method_reference/` retains the original method package with its supporting D01 files and working relative links.
- `provenance/source_method.zip` retains the exact original method archive.
- `provenance/d06_tool_baseline/` retains the adapted D06 tools used as the implementation baseline.
- The source record identifies the D06 archive by hash. Its full atlas is not recursively bundled inside D07.

Original reference code, later adaptations, and D07 data retain distinct provenance. Historical validation belongs to its named source. D07 checks must reference D07's actual graph and output files.

## Scope and continuity

The handoff includes the structural graph, synchronized exports, nine map views, two guides assembled with those views into an eleven-page PDF, an offline explorer, reproducible tools, and validation evidence as performed.

Environmental assignments, difficulty, expedition authoring, elapsed days, and encounters remain later work. D01-D06 keep their existing geography and references. This first D07 revision supersedes none of those atlases or the Violet project checkpoints.

Repository integration has not been performed by creating this package. It is a standalone D07 handoff, not a full repository export or cumulative story archive.
