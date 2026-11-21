# D07 graph data dictionary

`data/dungeon_graph.json` owns the model. CSV files, GraphML, maps, and the offline explorer are derived products. The node and edge CSV headers retain the original mapping-method schema.

## Dungeon identity and metadata

`metadata.dungeon_id` is `D07`. `metadata.revision` identifies the graph revision; metadata also records the coordinate convention, seed, generation authority, stratum parameters, and measured graph metrics.

Local node IDs such as `R001` are unique within this dungeon. A cross-dungeon record must carry both `dungeon_id` and `node_id`. The human-readable shorthand `D07-R001` resolves to `(D07, R001)`; it does not replace `R001` in the existing CSV schema. Apply the same namespace rule to edge references.

D07 is Violet-ending within the Blue political Domain. Its graph contains six strata: Red, Orange, Yellow, Green, Blue, and Violet.

## Node fields

| Field | Meaning |
|---|---|
| `stratum` | Named stratum: Red, Orange, Yellow, Green, Blue, or Violet. |
| `code` | Corresponding prefix R, O, Y, G, B, or V. |
| `x_mi` | East-positive horizontal coordinate in miles. |
| `y_mi` | North-positive horizontal coordinate in miles. |
| `depth_mi` | Downward-positive depth below the local surface entrance, in miles. |
| `network_role` | `principal` or `terminal_branch`; this is a graph role, not a character role. |
| `branch_id` | Permanent terminal-arm ID; empty for principal nodes. |
| `site_type` | Structural class such as surface entrance, unassigned junction/chamber, lateral junction, or terminal chamber. This does not assign an ecosystem. |
| `node_id` | Permanent local node identity, for example `Y023`. |
| `west_to_east_index` | Derived alias sorted by x, then y, then depth. |
| `north_to_south_index` | Derived alias sorted by decreasing y, then x, then depth. |
| `global_index` | Convenient row index for this snapshot, not a durable cross-revision identity. |
| `geography_status` | The record's design/proposal authority: `DESIGN_PROPOSAL_D07_001` in this initial build. |
| `in_world_survey_status` | Separate in-world knowledge status. An authoring map is not automatically an Accord Registry survey. |
| `degree` | Number of incident undirected passages, derived from the edge list. |
| `neighbors` | Pipe-separated neighboring node IDs, derived from the same edge list. |

Coordinate decimals support reproducible computation. They do not assert that the dungeon has been surveyed to that physical precision.

Initial IDs were assigned once using the method's depth-oriented ordering. Subsequent views retain them. Future additions append unused IDs; moving a label on the page must never move or rename a physical node. Display aliases may change in a documented later revision.

## Passage fields

| Field | Meaning |
|---|---|
| `edge_id` | Permanent local passage identity, such as `E0001`. |
| `source` / `target` | Endpoint node IDs. Their storage order does not make the passage one-way. |
| `kind` | `principal_passage`, `lateral_terminal_passage`, or `inter_stratum_passage`. |
| `strata` | One stratum name, or both endpoint strata separated by a pipe. |
| `straight_line_mi` | Three-dimensional Euclidean distance between the endpoint coordinates. |
| `modeled_centerline_mi` | Sum of segment lengths along the stored polyline. |
| `depth_change_source_to_target_mi` | Target depth minus source depth; positive means descending in this coordinate convention. |
| `geometry_xyz_mi` | Ordered `[x, y, depth]` vertices, including both endpoints. Stored as a JSON array in the authoritative graph and a JSON-encoded CSV cell. |
| `direction` | `UNDIRECTED_TOPOLOGY`; directional traversal costs are a separate future overlay. |
| `traversal_method` | OPEN until deliberately assigned. |
| `travel_time` | OPEN; the model does not convert distances into days. |
| `terrain_detail` | OPEN at the structural-graph stage. |
| `geography_status` | The passage's design/proposal authority: `DESIGN_PROPOSAL_D07_001` in this initial build. |

The initial construction uses four vertices per passage. All displayed bends come from these vertices. Recompute distances from geometry after an authored change; do not retain stale lengths.

The model is a simple undirected graph with one passage per unordered node pair. Supporting parallel passages later requires an explicit schema and validator change. A visible line crossing is not a junction unless an actual node is shared.

## Derived exports

| File | Contents and role |
|---|---|
| `nodes.csv` | Node records with coordinates, IDs, roles, degrees, and neighbors. |
| `edges.csv` | Passage records with endpoint IDs, lengths, and complete polyline geometry. |
| `adjacency.csv` | Node ID, neighbors, and degree. |
| `view_index.csv` | Stable IDs, display aliases, snapshot indexes, and coordinates. |
| `stratum_connections.csv` | Every passage connecting adjacent strata. |
| `dungeon_graph.graphml` | Graph-software interchange: node attributes, endpoint connectivity, passage IDs, kinds, and length weights. It does not replace the full JSON polyline model. |
| `VALIDATION.json` | Generator checks, measured metrics, and stratum summaries. Independent validation is recorded separately under `validation/`. |

CSV files use UTF-8 with a byte-order mark and standard CSV quoting. Parse them with a CSV reader; commas inside a JSON geometry cell are not column delimiters.

## Geometry and display

The east-west elevation uses `(x, depth)`. The north-south elevation uses `(y, depth)`. Plans use `(x, y)` with equal horizontal units and north upward. Depth increases downward in elevation displays. Each plan can use local zoom; the shared-scale overlay compares all strata at one horizontal scale.

Principal width is the selected total east-west span of the principal node network. `lateral_extent_ew_mi` describes the node-envelope span including terminal arms; a polyline bend can extend slightly beyond node extrema. Neither value is a cave wall, chamber area, or hollow volume.

## Metrics and limits

For a connected undirected graph, the dimension of the cycle space is `edges - nodes + 1`. This counts independent cycles, not every possible route. Biconnectivity applies to the principal core under this build's policy; deliberate terminal arms mean the full graph can have articulation points.

Geological connectivity does not establish clearance, rope anchors, water flow, walkability, fatigue, equipment suitability, or safety. Environmental expectations and dated observations are separate future records keyed to this graph's IDs and revision. OPEN and UNASSIGNED values must not be displayed as zero, false, or confirmed absence.
