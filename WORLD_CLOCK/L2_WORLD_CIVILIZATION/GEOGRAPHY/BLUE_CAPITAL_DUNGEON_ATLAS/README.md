# Blue Capital Dungeon — numbered 3D network, revision 002

**340 nodes · 709 passages · 60 inter-stratum links · 32 lateral dead-end tips · 370 independent cycles.**

This is a computational **spatial design proposal** under the author's selected dimensions. It is not a claim that all coordinates, node counts, passage lengths or ecological locations already existed in canon. The adopted constraints and draft choices are separated in `AUTHOR_DECISIONS_AND_SCOPE.md`.

## Open first
- `BLUE_CAPITAL_DUNGEON_ATLAS_002.pdf`: two-page guide, both depth elevations, five numbered stratum plans and a common-scale overlay.
- `DUNGEON_EXPLORER.html`: self-contained offline viewer; search stable node IDs or width-order aliases, rotate the 3D projection, inspect neighbors, pan and zoom.
- `data/dungeon_graph.json`: authoritative working graph for this revision.
- `data/nodes.csv`, `edges.csv`, `adjacency.csv`, `view_index.csv`, `stratum_connections.csv`: readable editing and lookup tables.
- `data/dungeon_graph.graphml`: graph-software interchange format.
- `data/VALIDATION.json`: actual computational integrity tests and counts.

| Stratum | Permanent IDs | Nodes | Depth (mi) | Principal E-W span (mi) | Internal passages |
|---|---|---:|---|---:|---:|
| Red | R001–R040 | 40 | 0–1.5 | 3 | 76 |
| Orange | O001–O052 | 52 | 1.5–3.5 | 5 | 100 |
| Yellow | Y001–Y068 | 68 | 3.5–6.5 | 8 | 130 |
| Green | G001–G080 | 80 | 6.5–11.5 | 11 | 152 |
| Blue | B001–B100 | 100 | 11.5–17 | 16 | 191 |

The internal-passage column sums to 649; 60 additional passages connect adjacent strata, for 709 total. There is no Violet stratum in this graph.

## Stable identity, separate view order
`Y023` is one physical node in every map. Its west-to-east sorting alias in this revision is `Y-W015`; its global record index is 115. It is **not renamed** when viewed from above. Its coordinates are x = -2.777095 mi, y = -0.440179 mi, depth = 4.678719 mi. Its eight neighbors are O036, Y004, Y006, Y020, Y021, Y025, Y039 and Y041.

Permanent IDs use R/O/Y/G/B plus three digits. Initial numbering follows depth within each stratum. Future additions append unused IDs; do not renumber existing nodes to make a new map look tidy. Width/north indexes are derived view order and may change when locations are added or edited. `global_index` is a convenient table index, not a second identity.

## Coordinate convention
The surface entrance R001 is (0,0,0). x increases east, y increases north, and z increases downward. All distances are in miles. Plan maps use true equal horizontal units and local zoom. The common-scale overlay and viewer's common-scale checkbox permit footprint comparison without confusing zoom with physical width. Depth elevations use an enlarged vertical scale for legibility and state that explicitly.

North-south principal design spans are provisionally 2.4 / 3.8 / 6.4 / 8.8 / 12.0 miles. They are not selected canon. Lateral terminal arms take the complete E-W design extent beyond the principal spans; Blue's draft outer span is about 26.489 miles, not a new mandated outer boundary.

## Topology and interpretation
The model is an undirected spatial graph. 258 principal-network nodes form a vertex-biconnected core: no single internal core node separates that core into disconnected pieces. 82 additional nodes form 32 deliberately attached terminal arms. These arms are real destinations in the design, not downward routes, and keep their attachment depth. Geological connectivity is distinct from practical accessibility for Kaira, Nyx or any other party.

Every edge has a permanent ID and one polyline in 3D. All maps project those same vertices; no plan is independently drawn. Crossing lines do not connect unless they share a node. A line is an abstract natural passage centerline, not a constructed bridge. Modeled centerline distances are calculated from proposed coordinates and are not surveyed travel distances, walkability assurances or journey times.

No route is declared the Tournament route, no marker is positioned, and no historical research/rescue site is relocated. Biomes, chamber boundaries, watercourse flow, passage width, clearances, climbing requirements and party-specific traversal remain OPEN.

## Extend without breaking continuity
Edit the authoritative graph or introduce scoped new records; retain permanent IDs and supersession notes. Maintain a separate time-dependent conditions layer for ELDRIS, congestion, oscillations and temporary obstructions. A newly discovered shortcut is not automatically a newly created cave. Ordinary oscillation does not rearrange the physical passage map. The biological/geographic map and each expedition's knowledge stay distinct.

Run `python tools/validate_graph.py --atlas-dir .` from this folder after any graph edit, then regenerate views with `python tools/render_atlas.py --atlas-dir .`. `tools/generate_proposal_002.py` is the reproducible initial generator, not an instruction to overwrite an edited graph.

[Violet route register](../../../../BOOKS/RED/ARCS/ARC_006/TRAINING_ROUTES_005/README.md) · [Integration and authority audit](../../../../CHECKPOINTS/VIOLET_CUMULATIVE_007/INTEGRATION_REPORT.md)
