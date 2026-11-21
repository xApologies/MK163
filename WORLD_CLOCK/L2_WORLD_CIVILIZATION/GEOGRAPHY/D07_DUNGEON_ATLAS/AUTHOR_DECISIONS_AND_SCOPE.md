# D07 - authority and scope

**Revision:** `D07_ATLAS_001`  
**Scope:** First D07 structural atlas, with synchronized maps and an offline explorer.

## Selected constraints

D07 is a **Violet-ending dungeon in the Blue political Domain**. Its selected maximum modeled depth is **24 miles**, with six strata:

| Stratum | Minimum depth (mi) | Maximum depth (mi) | Thickness (mi) |
|---|---:|---:|---:|
| Red | 0 | 1.5 | 1.5 |
| Orange | 1.5 | 3.5 | 2.0 |
| Yellow | 3.5 | 6.5 | 3.0 |
| Green | 6.5 | 11 | 4.5 |
| Blue | 11 | 17 | 6.0 |
| Violet | 17 | 24 | 7.0 |

The Blue Domain identifies the political region. The dungeon's deepest stratum is Violet. All six strata have real node and passage records, including the Blue-Violet transitions.

D07 follows the established D01 mapping method and its configuration-driven adaptations. Every view derives from the same authoritative `data/dungeon_graph.json`.

## Computational proposals

The following parameters define this first build. Horizontal spans, node allocations, terminal arms, transition counts, exact coordinates, and passage bends are explicit design proposals recorded in the configuration.

| Stratum | Principal E-W span (mi) | Provisional N-S span (mi) | Principal nodes | Terminal nodes | Terminal arms | Links to next stratum |
|---|---:|---:|---:|---:|---:|---:|
| Red | 3.0 | 2.4 | 30 | 9 | 3 | 10 |
| Orange | 5.4 | 4.2 | 40 | 12 | 4 | 12 |
| Yellow | 8.5 | 6.6 | 52 | 15 | 5 | 14 |
| Green | 12.4 | 9.6 | 64 | 18 | 6 | 16 |
| Blue | 18.0 | 14.0 | 80 | 21 | 7 | 18 |
| Violet | 25.0 | 19.0 | 96 | 24 | 8 | None |

The seed is **1630701**, preserved with the implementation and dependency environment. Subsequent rendering and environmental work use the saved graph. Records carry `DESIGN_PROPOSAL_D07_001` as their geography status.

Principal widths are total east-west spans. Terminal arms extend beyond them. Placement envelopes do not establish chamber volume, passage clearance, or measured ecological boundaries.

## Shared mapping conventions

- Coordinates use miles: x east-positive, y north-positive, depth downward-positive. R001 is the surface entrance at the local origin `(0, 0, 0)`.
- Stable cross-dungeon identity is `(dungeon_id, node_id)`. `D07-V120` is shorthand for `(D07, V120)`; matching local numbers in other dungeons remain separate locations.
- Best-candidate placement and pruned Delaunay connections create looped principal networks. The adopted policy preserves biconnectivity within each principal stratum and the combined principal core.
- Terminal arms attach once and retain their attachment depth. Distributed natural passages join adjacent strata using distinct endpoints within each layer pair.
- Each passage owns a stored 3D polyline. The two elevations, six plans, common-scale overlay, and explorer project those same vertices.
- A projected crossing requires a shared node to be a junction. Geological connectivity and a party's traversal method remain separate records.

Structural validation establishes coherence of this representation and its selected policies. It does not establish in-world survey history, practical access, or a simulated geological origin.

## Current stage and open work

This handoff covers Phase 2 graph construction and includes the source work order's Phase 3 displays: nine map views and an eleven-page compiled atlas including two guides.

Environmental Companion construction remains pending. Forests, waterways, crystals, vaen, natural velis, ELDRIS formation profiles, difficulty, crossing methods, and party clearances remain OPEN. Unassigned environmental records mean not yet authored.

Structural route checks are analytical paths to the deepest modeled Violet node and back. Official markers, authored expeditions, dates, travel days, fatigue, encounters, and outcomes remain OPEN. D07's place name, world surface location, precise administration, age, and survey history also remain OPEN unless established separately.

## Continuity and provenance

D01-D06 retain their graphs, IDs, routes, and authority. D07 is a new geography owner. Existing Violet chronology, Genesis Robe work, character capabilities, and Card mechanics remain with their existing records.

The immediate implementation baseline is `MK163_D06_ATLAS_001`. Its tools are preserved under `provenance/d06_tool_baseline/`. The original mapping method remains available in `provenance/method_reference/` and `provenance/source_method.zip`. The D06 source archive is identified by its recorded hash; its full atlas is not nested inside this package.

See [provenance/REVISION_HISTORY.md](provenance/REVISION_HISTORY.md) for this first D07 revision. Actual validation results and their scope live under `validation/`. Original recovered code and later adaptations retain distinct provenance; no historical environmental-generation code is claimed.
