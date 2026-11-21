# D07 - Violet dungeon in the Blue Domain, revision 001

**461 nodes · 965 passages · 70 inter-stratum links · 33 lateral terminal arms · 505 independent cycles.**

D07's first structural atlas uses the established MK163 mapping system. It is **Violet-ending**, reaches a selected maximum modeled depth of **24 miles**, and contains all six strata: Red, Orange, Yellow, Green, Blue, and Violet. Its political location is the Blue Domain.

One saved 3D graph supplies every elevation, plan, and explorer view. Depth bands are selected constraints; horizontal spans, counts, exact coordinates, and passage bends are explicit design proposals recorded in [AUTHOR_DECISIONS_AND_SCOPE.md](AUTHOR_DECISIONS_AND_SCOPE.md).

## Open first

- [MK163_D07_ATLAS_001.pdf](MK163_D07_ATLAS_001.pdf) - eleven-page atlas: two guides, two depth elevations, six stratum plans, and a common-scale overlay. Start here for reading on a phone or tablet.
- [DUNGEON_EXPLORER.html](DUNGEON_EXPLORER.html) - offline node search, neighbor inspection, projection switching, rotation, pan, and zoom. Open it in a browser that permits local HTML scripting.
- [Master depth map](maps/01_MASTER_DEPTH_NETWORK.png) - the complete top-to-bottom network. All nine map views also have SVG and PDF exports in `maps/`.
- [Violet plan](maps/08_VIOLET_PLAN.png) - the deepest stratum, with its actual Blue connection endpoints.
- [Common-scale overlay](maps/09_COMMON_SCALE_OVERLAY.png) - all six horizontal footprints at one scale.
- [Authoritative graph](data/dungeon_graph.json) - D07's continuing spatial model, with synchronized CSV and GraphML exports.
- [EXECUTABLE.md](EXECUTABLE.md) - package verification, graph validation, display rebuilding, and isolated reproduction commands.

## Strata and permanent IDs

| Stratum | Permanent local IDs | Nodes | Depth below entrance (mi) | Principal E-W span (mi) | Internal passages |
|---|---|---:|---|---:|---:|
| Red | R001-R039 | 39 | 0-1.5 | 3.0 | 75 |
| Orange | O001-O052 | 52 | 1.5-3.5 | 5.4 | 100 |
| Yellow | Y001-Y067 | 67 | 3.5-6.5 | 8.5 | 129 |
| Green | G001-G082 | 82 | 6.5-11 | 12.4 | 159 |
| Blue | B001-B101 | 101 | 11-17 | 18.0 | 197 |
| Violet | V001-V120 | 120 | 17-24 | 25.0 | 235 |

The **895 internal passages** are joined by **70 adjacent-stratum passages**: Red-Orange 10, Orange-Yellow 12, Yellow-Green 14, Green-Blue 16, and Blue-Violet 18. The principal network contains 362 nodes; another 99 form 33 constant-depth terminal arms. The deepest modeled node is **D07-V120 at 24 miles**.

Principal widths are total spans of the main network. Terminal arms extend farther: Violet's full proposed node envelope spans approximately **43.163 miles** east-west. These dimensions describe placement, not cave walls or one hollow chamber.

## Read every view consistently

The entrance **D07-R001** is `(0, 0, 0)`. Coordinates are miles: x east-positive, y north-positive, and depth downward-positive. The cross-dungeon key is `(D07, R001)`; local tables retain `R001`. Identically numbered nodes in other dungeons remain separate locations.

| Mark | Meaning |
|---|---|
| Solid colored line | Principal natural passage. |
| Dashed colored line | Lateral terminal-arm passage. |
| Dotted gray line | Passage joining adjacent strata. |
| Hollow square | Terminal tip. |
| Hollow diamond on a plan | Neighboring stratum endpoint at its actual coordinates. |
| Star | Surface entrance. |

Every passage owns one stored 3D polyline. Elevations project `(x, depth)` or `(y, depth)`; plans project `(x, y)`. Plans use equal horizontal units and local zoom; the overlay provides a shared scale. A drawn crossing is a junction only when it shares a node.

## Stable geography and validation

The graph stays fixed during viewing and rendering. Seed **1630701**, the executable specification, and preserved code support isolated reproduction. Future additions append IDs; authored geographical changes receive scoped revision records.

Validation evidence lives under `validation/`. The [independent audit](validation/INDEPENDENT_AUDIT.json) checks D07's six-stratum specification, topology, polylines, and exports. [Render coverage](validation/RENDER_COVERAGE.json) identifies records used by each map. Reproduction, overwrite protection, structural routing, viewer logic, and visual-review reports describe the checks actually performed.

The adopted principal-core policy preserves biconnectivity; deliberate terminal arms give the full graph articulation points. Structural consistency does not establish practical traversal or survey history. Viewer logic checks also do not certify mobile layout or touch behavior.

## Later work and provenance

Environmental regions, waterways, resources, natural velis, ELDRIS profiles, difficulty, clearances, crossing methods, fatigue, and elapsed days remain OPEN. A structural path to Violet and back is analytical; it selects no official marker or dated expedition.

The [mapping standard](provenance/method_reference/DUNGEON_MAPPING_STANDARD.md), its supporting files, and exact source ZIP are preserved. `provenance/d06_tool_baseline/` records the immediate implementation baseline. D07 has its own parameters and geography; see [REVISION_HISTORY.md](provenance/REVISION_HISTORY.md).

D01-D06 and existing story records retain their separate owners. This is a standalone D07 handoff. [INTEGRATION_FOR_CODEX.md](INTEGRATION_FOR_CODEX.md) describes repository reconciliation; producing this package has not changed or pushed the repository.
