# Dungeon Mapping Standard
## Reproducible graph construction, aligned atlas rendering, environmental companions, and route reports

**Method edition:** 001 · **Date:** 2026-11-17  
**Project:** MK163 / AERA high-fantasy worldbuilding  
**Reference:** Blue Capital Dungeon, Atlas 002 + Environmental Companion 003 + First Trial 004  
**Purpose:** Preserve the actual successful mapping method so another city’s dungeon can be built to the same standard without copying this dungeon’s particular geography.

> **Build one authoritative three-dimensional graph. Derive every map, environmental lookup, and route report from its permanent IDs and coordinates. Never draw a second, independently invented network to represent the same dungeon.**

This manual is a separate reusable-method package. It does not replace, regenerate in place, or alter the cumulative Violet checkpoint 004. The reference files included here are copies for reproduction and regression testing. They are not competing live versions of the MK163 atlas.

### How to read this manual

There are three distinct kinds of material:

**Recovered implementation** describes what the supplied source scripts and datasets actually do. **Reference-world decisions** describe the author’s selected Blue Capital constraints and later corrections. **Recommended future procedure** describes a standard for a new dungeon or an extension that the original scripts do not yet implement. A recommendation does not retroactively become a historical generation step or new story canon.

Read sections 01–07 before creating anything; sections 08–18 explain construction and rendering; sections 19–25 explain the environmental and route layers; sections 26–32 govern validation, continuity, and execution. Appendices provide exact file schemas and reusable templates.

### Source register

The source for this edition is the actual local archive `MK163_Violet_Cumulative_004_First_Trial_R001_B041.zip`, not a remembered summary of the conversation. See [the source inventory](provenance/SOURCE_REGISTER.json) for original archive paths, SHA-256 hashes, and preserved copies. No current GitHub HEAD is asserted.

| Reference | Preserved evidence | What it supports |
|---|---|---|
| S1 | [Graph JSON](reference/blue_capital/data/dungeon_graph.json) | Actual coordinates, edges, polylines, metadata, and counts |
| S2 | [Original generator](reference/blue_capital/tools/generate_proposal_002.py) | Exact initial generation algorithm and parameters |
| S3 | [Original renderer](reference/blue_capital/tools/render_atlas.py) | Exact elevation, plan, overlay, labeling, and export procedures |
| S4 | [Original viewer builder](reference/blue_capital/tools/build_viewer.py) | Offline HTML interface and display projections |
| S5 | [Original validator](reference/blue_capital/tools/validate_graph.py) | Existing integrity and export checks |
| S6 | [Environment scope](reference/blue_capital/ENVIRONMENT_COMPANION_003.md) and `reference/blue_capital/data/environment_*` | Saved environmental assignments, not an absent generator |
| S7 | [First trial](reference/first_trial/FIRST_VAELUM_TRIAL_R001_B041.md) | Author-locked route, marker, return policy, and open dates |
| S8 | [Authority and scope](reference/blue_capital/AUTHOR_DECISIONS_AND_SCOPE.md) | Selected dimensions versus design proposals and historical constraints |
| S9 | [Data dictionary](reference/blue_capital/DATA_DICTIONARY.md) | Meaning of graph fields and distinct authority of derived exports |
| S10 | Current author instructions in this workshop | Preserve a cumulative live model; use this method for future dungeon maps |

---

## 01. What this method produces

The deliverable is a **queryable spatial atlas**, not merely an attractive picture. It must answer questions such as: which nodes connect; what lies at a selected node; which passages reach the required stratum; which route avoids a formation hotspot; and what remains unknown before a party attempts the route.

The core deliverables are an authoritative graph JSON, synchronized CSV tables, a graph-interchange export, a top-to-bottom elevation, a complementary elevation, one top-down plan per included stratum, a common-scale footprint overlay, a searchable offline viewer, environmental companion tables, and validation results. Route reports are generated from that foundation rather than invented independently.

The successful reference has 340 nodes, 709 passages, 60 adjacent-stratum connections, 32 lateral terminal arms, and 370 independent cycles. These are properties of this particular graph, not required counts for every future dungeon. The full network is connected. Its 258 principal nodes form a vertex-biconnected core; 82 further nodes lie on terminal arms. [S1–S2]

The method should remain useful for a smaller Green dungeon, a larger Blue dungeon, or a later Violet dungeon. Select that dungeon’s actual extent first. Do not add Violet merely because a template supports it, and do not force every dungeon to be a 17-mile-deep copy of Blue Capital.

## 02. Authority, ownership, and World Clock placement

AERA’s fantasy mechanics constrain what the world permits; the local dungeon atlas selects what exists at this location. Keep those responsibilities separate.

| Owner | Proper content |
|---|---|
| AERA Level 1 | Transduction, interfaces, basin restrictions, Binding concurrency, fatigue principles |
| World Clock Level 2 | Local geological graph, caverns, waterways, ecosystems, resources, formation zones, navigation conditions |
| World Clock Level 3 | Dated expeditions, actual encounters, selected character routes, observed outcomes |
| Book / arc outline | Narrative selection and sequencing; cross-references to geographic records |
| Accord Registry in-world | Professional maps, surveys, expedition histories, harvest records, and published observations |
| Repository methodology / tools | Generation standards, renderers, validators, schemas, and workflow instructions |

A reusable manual is a repository method, not a newly invented fantasy law. The recommended integration home is `METHODS/DUNGEON_ATLAS/`, with a reference from the relevant geography index. That is a proposed repository path to reconcile with existing conventions, not a claim that it already exists.

The reference atlas’s current owner is:

```text
MK163/WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/
  BLUE_CAPITAL_DUNGEON_ATLAS/
```

A new city gets a separate atlas directory and a unique dungeon identifier. Local IDs such as `R001` can recur across dungeons only if every cross-dungeon reference also carries `dungeon_id`. The pair `(dungeon_id, node_id)` is the durable global key.

Do not copy the entire 1,245-Shaping catalogue into every atlas. Refer to its designated catalogue owner and revision. This methodology package does not modify Card prices, CSR basin assignments, Binding costs, or the existing cumulative CSV.

## 03. Separate five kinds of truth

Every future build must distinguish the following:

1. **Author-selected constraints:** dimensions, allowed strata, natural-only crossings, existing historical sites, and explicit story choices.
2. **Computational design proposals:** generated node placement, exact passage geometry, lateral extents not selected by the author, and environmental allocations awaiting review.
3. **Structural validation:** unique IDs, correct links, reproducible data, graph connectivity, and consistent projections.
4. **In-world survey knowledge:** what the Accord Registry or a particular expedition has actually mapped and documented.
5. **Current conditions:** ELDRIS presence, harvestable abundance, obstruction, local field phase, traffic, and temporary safety.

A structural PASS does not certify geological realism, safe traversal, ecological equilibrium, or historical truth. Equally, a 99%-surveyed in-world dungeon does not imply that 99% of its current monsters, resources, and hazards are predictable.

The reference is described as centuries old, approximately two or three hundred years, and approximately 99% surveyed. Those are broad worldbuilding decisions. Do not invent an exact founding date or mark three or four randomly selected graph nodes “the unmapped 1%.” Survey percentage has not been defined as a percentage of these 340 abstract nodes.

Preserve `OPEN`, `UNASSIGNED`, `PROPOSED`, and `AUTHOR_LOCKED` states. A locked itinerary does not lock every proposed environmental feature along it. Conversely, earlier proposal labels do not cancel a later explicit route decision. [S6–S8]

## 04. Establish a dungeon specification before generation

Use [the new-dungeon specification template](templates/NEW_DUNGEON_SPEC.json) as an authoring checklist. It is deliberately not executable configuration for the preserved original generator, which uses constants inside its source. A new implementation must explicitly load the configuration or an engineer must adapt a copied generator.

Specify the dungeon ID, city, included strata, depth boundaries, total principal east–west width at each stratum, proposed north–south width, entrance count and positions, target graph density, terminal-branch policy, cross-layer connection targets, protected historical constraints, and status of each decision.

Also record what has **not** been selected: chamber dimensions, tunnel clearances, river flow, walking times, rest schedules, resource quantities, encounter counts, and official marker locations. Absence of a value is not permission for a renderer to invent it.

The reference parameters, recovered from S2, are:

| Stratum | Depth below entrance, mi | Principal E–W span, mi | Proposed N–S span, mi | Principal nodes | Terminal nodes | Terminal arms | Links to next stratum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Red | 0–1.5 | 3 | 2.4 | 30 | 10 | 4 | 12 |
| Orange | 1.5–3.5 | 5 | 3.8 | 40 | 12 | 5 | 14 |
| Yellow | 3.5–6.5 | 8 | 6.4 | 52 | 16 | 6 | 16 |
| Green | 6.5–11.5 | 11 | 8.8 | 60 | 20 | 8 | 18 |
| Blue | 11.5–17 | 16 | 12.0 | 76 | 24 | 9 | None |

The depth boundaries and 3/5/8/11/16-mile east–west spans are selected constraints. The north–south spans, node counts, and exact embedding were computational proposals. The seed is **1631081**. [S1–S2, S8]

For a new dungeon, choose fresh values rather than inheriting all of these as defaults. Graph density should be sufficient for multiple meaningful routes and readable subdivisions. It should not be made dense by connecting every point to every other point.

## 05. Width, area, depth, and cave volume are different

“Sixteen miles wide” in this reference means a **total principal east–west span**, not a 16-mile radius. The initial principal-network anchors are placed at `x = -width/2` and `x = +width/2`.

The width applies to the main connected route network. Terminal branches can extend beyond it. The complete Blue design has a larger outer envelope, approximately 26.489 miles east to west, but that does not retroactively change the selected 16-mile principal width. [S1, S8]

An enclosing rectangle, ellipse, or bounding box is a placement envelope. It is not one excavated chamber. Do not multiply width, length, and depth and call the resulting rectangular volume hollow cave space. Most of that envelope may be rock.

A point representing a cavern does not define the cavern’s footprint or ceiling height. A polyline representing a passage does not define its width, headroom, slope at every scale, or physical surface. Those are later geometric attributes. Add polygons, cross-sections, or local subgraphs when they become relevant; do not pretend they already exist in a centerline graph.

Similarly, a river-associated node need not be wholly underwater. A forest-region membership is not a filled polygon, and an environmental map should not draw a precise forest boundary without corresponding boundary data.

## 06. The mathematical object and its coordinate system

Treat the atlas as an embedded graph `G = (V, E)`.

- Each node `v` has a permanent ID and a point `p(v) = (x, y, z)`.
- Each edge `e` joins two node IDs and has a three-dimensional polyline.
- Metadata specifies the strata, units, reference origin, revision, and authority.
- Separate tables attach environmental features and traversal classifications.

For the reference, the surface entrance is **R001 at (0, 0, 0)**. `x` increases east, `y` increases north, and `z` increases **downward**. All three are in miles. A positive change in `z` therefore means descending, not rising. [S1, S9]

The graph is undirected geological connectivity. An edge stored with `source=A` and `target=B` is not automatically one-way. It may nevertheless require different effort in each direction. Keep a future directed traversal-cost overlay distinct from the geological graph.

The existing implementation is a simple graph: one edge per unordered node pair. A future cavern may need two distinct passages with the same endpoints. That is a deliberate schema migration to a multigraph, not an excuse to let NetworkX silently overwrite one passage. In a multigraph, route records must contain edge IDs as well as nodes because a node sequence alone is ambiguous.

A projected crossing is never a connection merely because two drawn lines intersect. A connection requires a shared node record. If later authoring establishes an actual junction, add a node and split the passages explicitly, preserving provenance and any affected route references.

## 07. Permanent identity versus display ordering

Use stratum prefixes and zero-padded local integers: `R001`, `O001`, `Y001`, `G001`, `B001`. Add `V` only for an explicitly included Violet stratum in a future atlas.

In the original build, local IDs were assigned after sorting each stratum’s nodes by `(depth, x, y)`. That was a one-time initialization step. Once referenced in a route, event, region, or discussion, the IDs are permanent.

Separate view-order aliases support alternative indexing:

```text
west_to_east_index: sort by x, then y, then depth
north_to_south_index: sort by decreasing y, then x, then depth
global_index: convenient snapshot row order, not permanent identity
```

For example, Y023 is also Y-W015 in the reference west-to-east index. It remains Y023 in elevation, plan, environmental tables, and route records. [S1, S9]

Never rename nodes to make the labels appear numerically neat from a new viewing direction. When adding a node, append an unused permanent ID. When recomputing view-order aliases, record the new revision so an old width alias is not mistaken for a timeless identifier.

Edge IDs are similarly stable: `E0001`, `E0002`, and so on. Do not renumber all edges after adding a passage. Region IDs, watercourse IDs, route IDs, and observation IDs each need their own stable namespaces.

## 08. Recovered placement algorithm: irregular, well-spaced principal nodes

The original generator uses NumPy’s `default_rng(1631081)`. It processes strata in Red-to-Blue order. The ordering matters because all stochastic draws share that generator. A seed without the code and operation order is not enough to guarantee reproduction. [S2]

For each stratum, the generator begins with two width anchors at `(-w/2, -0.08*ns)` and `(w/2, 0.13*ns)`. Red also begins with the entrance at `(0,0)`.

For each remaining principal point:

1. Sample candidate horizontal points uniformly within the rectangle `[-w/2,w/2] × [-ns/2,ns/2]`.
2. Retain candidates satisfying `(x/(w/2))² + (y/(ns/2))² < 1.05`.
3. Collect **90** acceptable candidates.
4. For each candidate, compute its squared distance to the nearest existing point after scaling horizontal coordinates by `(w, ns)`.
5. Select the candidate whose nearest-neighbor distance is largest.
6. Repeat until the principal-node target is reached.

This best-candidate procedure spreads points across the available area without imposing a tidy grid or allowing random clumps to dominate the figure. It is a design heuristic, not a simulation of cave formation.

For a new city, irregular polygonal placement envelopes, exclusion regions, or multiple connected lobes can replace the ellipse. Document that as an adapted generation method. Validate that the sampling loop can actually satisfy the requested count and spacing; use a bounded retry budget and report failure rather than looping indefinitely.

Protected pre-existing sites should be inserted as hard constraints before filling remaining space. Do not discover halfway through writing that a historical nine-mile research site was randomly moved to another depth.

## 09. Recovered depth assignment

The reference correlates depth with north–south position within each stratum, plus bounded random variation:

```text
f = 0.10 + 0.80 * (y/ns + 0.5) + random_uniform(-0.13, 0.13)
f = clamp(f, 0.055, 0.945)
z = stratum_min_depth + stratum_thickness * f
```

The Red entrance is then fixed to depth zero. In Blue, the deepest principal node is set to exactly 17 miles. Other points stay within their assigned bands. Coordinates are stored to six decimal places. Those decimals are for computational reproduction, not a claim of millimeter-level survey accuracy. [S2]

This procedure produces spatial variation but is still a coarse embedding. It does not encode every ledge, local reversal, or shaft. An internal edge’s stored depth can be inspected independently of the two-dimensional plan.

For future dungeons, the north–south/depth correlation is optional. It must not become a law that all caves descend northward. Another dungeon might have several descending lobes, folded routes, or distinct deep shafts. Preserve the common coordinate convention even if the generation policy changes.

A dungeon-ending marker should not determine geological maximum depth unless explicitly selected. A graph can contain nodes deeper than a training objective. The reference first trial ends at B041; the graph still contains B100 at 17 miles.

## 10. Recovered internal connectivity: Delaunay candidates, then pruning

The original generator performs a **two-dimensional Delaunay triangulation of the horizontal principal-node coordinates within each stratum**. It does not use a three-dimensional tetrahedralization. The depth coordinate is already attached to those nodes, so the resulting links become a spatially embedded three-dimensional route graph. [S2]

Every triangle supplies its three undirected candidate edges. The generator then ranks candidate edges by normalized horizontal length, perturbed by a factor between 0.8 and 1.2, longest first.

It attempts to remove longer links until approximately `round(2.2 * principal_node_count)` internal core edges remain. A removal is rejected if either endpoint would be pruned below the degree guard or if removing the edge would destroy vertex-biconnectivity. The reference target is achieved for its five strata.

This is why the result has loops and cross-connections instead of a tree with one inevitable route. The principal graph remains connected after removal of any single principal node. That property is useful for an atlas intended to support alternative routes, but it is a **design policy**, not a universal fact about caves.

The full graph has articulation points because terminal arms intentionally depend on their attachment. Do not claim that removing any node anywhere leaves the entire dungeon connected. The biconnectivity statement applies to the principal core.

A new dungeon may legitimately have authored choke points. In that case, do not silently override them to satisfy a generic biconnectivity test. Record a different topology policy and validate the intended structure. The validator must enforce the selected policy, not impose a story-changing convenience.

## 11. Recovered lateral terminal branches

The terminal-arm system is not decorative. It creates extensive lateral destinations that need not help a party reach the next stratum.

For each stratum, divide its terminal-node allocation among its terminal arms, distributing any remainder one node at a time. The reference uses 10/4, 12/5, 16/6, 20/8, and 24/9 terminal nodes/arms. Each arm therefore contains more than a single tip in most cases. [S2]

Arm directions alternate roughly east and west, each perturbed by a random angle from -0.65 to +0.65 radians. The attachment is selected from unused principal nodes furthest along the chosen lateral direction. Arm length is 20–42% of the principal east–west width, with a perpendicular sinusoidal bend whose amplitude is between -11% and +11% of that width.

For each arm, intermediate nodes form a chain from its attachment. **All nodes and all polyline points on that arm stay at the attachment depth.** The endpoint has degree one. Terminal nodes are excluded from the inter-stratum matching procedure.

Consequently, the arm can extend well outside the principal width but does not secretly become a downward shortcut. It may later contain a forest, lake, velis site, or resource region. “Dead end” means no further geological connection in this representation; it does not mean empty or economically worthless.

Future additions can explicitly reconnect an arm, but that is a topology revision. Update its role, route implications, validation expectations, and provenance rather than retaining contradictory “terminal” labels.

## 12. Recovered inter-stratum links

The reference creates **12 Red–Orange, 14 Orange–Yellow, 16 Yellow–Green, and 18 Green–Blue passages**. These 60 links provide multiple distributed transitions. Only neighboring strata are linked. [S2]

The variable name `portals` in the original Python script refers to these ordinary cross-layer links. It does **not** mean magical spatial portals, spatial corridors, gateways, or teleportation.

The procedure takes a sufficiently large pool of deeper principal nodes from the upper stratum and shallower principal nodes from the lower stratum. Each pool contains at least `needed + 4` nodes or 60% of the corresponding principal nodes, whichever is greater, subject to the available list length.

Candidate upper/lower pairs receive a three-dimensional Euclidean distance score with a 0.93–1.07 random multiplier. The procedure greedily selects short candidates while using each upper endpoint and each lower endpoint at most once in that layer-pair matching. It stops at the selected link count.

This is greedy distributed matching, not an optimal global matching theorem. Different adjacent layer-pairs can use the same middle-stratum node. The resulting graph is then validated globally.

A new implementation must check that enough distinct endpoints exist. It must also ensure the interior polyline traverses the selected bands coherently, not merely that the endpoints belong to neighboring colors. For more complex curved geometries, inspect intermediate vertices as well as node depths.

## 13. Edge geometry, distance, and honest limitations

Each reference passage contains four three-dimensional vertices: the source, two intermediate bends, and the target. Let `p` and `q` be endpoint coordinates. The bend direction is horizontal and perpendicular to the horizontal component of `q-p`. Its amplitude is 3–11% of the three-dimensional chord length. [S2]

The intermediate points occur at one third and two thirds of the chord. Their lateral offsets have factors +1 and -0.5. Depth interpolates linearly along this initial polyline. If there is no horizontal component, the perpendicular displacement is zero.

Two distances are stored:

```text
straight_line_mi = Euclidean distance between endpoint coordinates
modeled_centerline_mi = sum of Euclidean lengths of successive polyline segments
```

The centerline must not be shorter than the endpoint chord. Recalculate it from geometry after any edit. Never keep an old distance when moving a node or adjusting a bend.

These distances are **model lengths**, not empirically surveyed walking distances. The four-vertex representation may omit switchbacks, climbing surfaces, chamber detours, or obstacle approaches. Do not convert it into an expedition duration by dividing by an invented speed.

Some passages are steep in this reference. That is a reason to develop clearance and traversal data, not evidence that everyone can walk the line. A connection means geology connects; a suitable movement method remains a separate question.

For natural shafts and chasms, a line does not imply a bridge. For lakes, a line does not imply a boat or dry surface. For Nyx, endpoint connectivity does not prove sufficient width, headroom, traction, or a safe crossing. These limits must remain explicit until authored.

## 14. Authoritative data and synchronized exports

`data/dungeon_graph.json` is the reference authority. The CSV and GraphML files are derived views of that model, not independent competing sources to edit at random. [S1, S9]

The generator exports eight graph files:

```text
dungeon_graph.json
nodes.csv
edges.csv
adjacency.csv
view_index.csv
stratum_connections.csv
dungeon_graph.graphml
VALIDATION.json
```

`nodes.csv` includes permanent identity, coordinates, network role, branch membership, site type, indexes, degree, adjacency, and status. `edges.csv` includes endpoints, kind, 3D geometry encoded as JSON text, chord and centerline length, signed depth change, and unresolved traversal attributes.

The adjacency and degree fields are derived from edges. The view-order indexes are derived from coordinates. The graph validator must compare these against the graph, not simply assume that because they are in the same folder they agree.

GraphML preserves node coordinates and weighted connectivity in the supplied exporter. It is not a complete substitute for the JSON’s polyline and environmental data. Do not round-trip through a format with fewer fields and silently delete the fields it could not represent.

Use UTF-8 and explicit CSV handling. The reference CSVs use UTF-8 with a byte-order mark. Parse quoted cells correctly, especially embedded JSON arrays and pipe-separated membership lists. Do not use naive string splitting on commas.

For live edits, use a controlled JSON-edit/export tool or a documented CSV-import procedure that updates JSON, derived indexes, all exports, and tests together. Rerunning the original random generator is **not** the update procedure for an established atlas.

## 15. Render every view from the same coordinates

The required projections are:

| View | Coordinates retained | Coordinate omitted | Purpose |
|---|---|---|---|
| East–west elevation | `(x, z)` | north–south `y` | Top-to-bottom network across width |
| North–south elevation | `(y, z)` | east–west `x` | Complementary depth view |
| Stratum plan | `(x, y)` | depth shown by metadata/lookup | Top-down local connections |
| Common-scale plan overlay | `(x, y)` for all strata | depth separated by stratum colors | Compare actual horizontal footprints |
| Rotating viewer view | explicit projection of `(x,y,z)` | none in source data | Explore overlapping geometry visually |

In elevation plots, invert the displayed depth axis so larger positive depth appears lower. In plans, north-positive `y` appears upward. Screen SVG coordinates increase downward, so the viewer uses `(x, -y)` for plans. These are display conventions; do not negate stored coordinates to make one view look correct. [S3–S4]

Use equal physical units for east–west and north–south axes in plan views. Individual stratum maps may use local zoom for legibility. Make the different zoom explicit and provide a common-scale overlay so Red does not appear physically as wide as Blue just because both fill a page.

The reference elevations enlarge vertical display scale for readability and say so. A slope measured from the printed image is therefore not a physical gradient. Calculate slope from coordinates, not from the page.

Prefer labels such as **“North–south elevation (y versus depth)”** instead of an ambiguous camera direction. What matters is which coordinates are projected, not a vague phrase such as “looking north to south.”

## 16. Recovered static rendering procedure

The original renderer uses Matplotlib with the noninteractive Agg backend, then exports each view as PNG, SVG, and PDF. It also writes an eight-page `maps/NETWORK_MAPS.pdf`. [S3]

Reference layout settings are:

| Output | Reference figure size | Key settings |
|---|---|---|
| Master east–west elevation | 22 × 28 inches | all 340 labels; depth bands; entrance star |
| Complementary elevation | 16.54 × 23.39 inches | same nodes, alternative projection |
| Each stratum plan | 16.54 × 11.69 inches | equal horizontal units; local zoom; neighboring-layer ghosts |
| Shared footprint overlay | 16.54 × 11.69 inches | equal units; all strata; labels intentionally omitted |
| PNG export | 115 dots per inch | reference output setting, not a universal print requirement |

The original colors are Red `#a8303c`, Orange `#ba5c16`, Yellow `#94720c`, Green `#22764d`, and Blue `#245b9a`. They encode the author’s actual strata. Do not reuse the same color legend for both stratum and difficulty without a clear separate key.

Principal passages are solid. Lateral terminal arms are dashed. Adjacent-stratum passages are dotted gray. Terminal tips use hollow squares. Neighboring-layer nodes shown on a plan use hollow diamonds. The surface entrance uses a star.

A stratum plan includes all local nodes and every edge incident to them. Neighboring endpoints appear as faded ghost nodes with their real IDs. This lets a reader trace a cross-layer connection into the next plan without inventing a separate portal identity.

Vertical guides at `±principal_width/2` identify principal span, **not cave walls**. Include lateral arms beyond them. Do not crop a terminal branch merely because it exceeds the main network’s width.

The supplied renderer contains hard-coded Blue Capital titles, counts, five-stratum colors, ticks, and depth limits. Adapt these before reusing it for another dungeon. The actual graph data must determine printed counts; stale headings are a validation error, even if the lines underneath are correct.

## 17. Label placement and readability

Permanent labels are part of the atlas’s functionality. A beautifully colored map with unreadable or missing IDs fails the purpose of this method.

The reference annotation function places labels in display-pixel space after the axes have been drawn. It tries twelve offsets around each node, estimates a text rectangle, penalizes overlap with already placed labels, penalizes crossing the plot boundary, and mildly penalizes long offsets. It chooses the lowest-scoring position and adds a thin leader line when necessary. [S3]

The labels move; the nodes do not. Moving physical nodes just to improve typography would change the geography and all route lengths.

The original code’s comment mentions dense neighborhoods, but its actual ordering is by ghost status, terminal status, and node ID. It is not a full neighborhood-density optimization. Its rectangles are estimated from font size, so it is not a guarantee of zero overlap. The offline viewer uses simpler fixed-offset labels and may need zoom for crowded areas.

For a future atlas, first enlarge the page, adjust annotation offsets, use vector output, add sector views, or expose labels at interactive zoom. Do not solve crowding by deleting useful graph connections or renumbering the network.

Visual quality control must check the dense center, the entrance, inter-stratum links, the outermost terminal tips, and footer/legend margins. Review at a realistic reading size as well as zoomed-in. Confirm that adjacent-layer labels are distinguishable from local labels without being invisible.

## 18. Offline viewer: what it does and does not do

The supplied `build_viewer.py` embeds the graph JSON in a self-contained HTML file. It uses inline CSS, SVG, and JavaScript; it does not require an external library or a live server to fetch graph data. [S4]

The interface provides elevation views, per-stratum plans, all-strata top-down view, rotation, pan, zoom, label visibility, terminal-arm visibility, common plan scale, node search, neighbor navigation, and coordinate inspection. Searching `Y023` or `Y-W015` finds the same reference node. It also accepts unpadded input such as `R1`.

The viewer’s “3D” display is a rotating two-dimensional projection of 3D coordinates, not a full depth-tested perspective renderer. The actual projection is:

```text
screen_horizontal = x*cos(angle) - y*sin(angle)
screen_vertical = 0.88*z + 0.45*(x*sin(angle) + y*cos(angle))
```

This is useful for seeing relationships but does not prove physical occlusion or passage collision. The source polylines remain authoritative.

The viewer is a graph explorer, not an embedded tournament simulator. It does not automatically calculate route time, stamina, environmental exposure, or encounters. Its original node panel describes the graph layer and does not automatically ingest the separate environmental CSVs.

When extending the viewer, join environmental records by stable ID, display proposal status, and keep overlays independently switchable. A node’s “not assigned” resource field must not be displayed as a confirmed absence. If some layer is hidden, explain whether route highlighting still includes hidden nodes.

For another dungeon, replace the hard-coded title, counts, layer options, search prefixes, palette, and “No Violet stratum” statement as appropriate. Do not add a Violet menu item without actual Violet data.

## 19. Environmental Companion: second dataset, same graph

The environmental companion describes what a party would **expect**, given known geography and formation conditions. It does not decide what actually happens on a particular day.

The preserved 003 overlay has 340 node profiles, 709 passage profiles, 44 regional features, and 24 water features. Its passage classifications are 213 low, 417 medium, and 79 hard. These values were checked against the actual tables for this package. [S6; validation/REFERENCE_ATLAS_AUDIT.json]

A critical source boundary: **the cumulative archive does not include the program that originally generated the environmental overlay or its exact classification thresholds.** Its outputs and explanatory notes are preserved, but its full stochastic procedure cannot be reconstructed honestly from those alone.

To reproduce this exact overlay, preserve and reuse the saved tables. To create a new city’s overlay, implement and version a new procedure, record its seed and parameters, and mark its allocations as proposals. The procedure below is a recommended future workflow, not a claim that it is the recovered original algorithm.

Begin with geology and large coherent regions; add connected hydrology; attach flora and resource conditions; classify passages; then review against protected history and party needs. Do not decorate each node independently with random feature labels. A river must connect; a regional forest should not jump between disconnected caverns merely because the colors look attractive.

## 20. Correct environmental taxonomy

The author’s corrected vocabulary governs the maps:

| Category | What belongs in the atlas | What must not be inferred |
|---|---|---|
| Geology | Caverns, tunnels, shafts, chasms, boulder chambers, natural shelves and rock spans | Man-made bridges, carved routes, or guaranteed walkability |
| Hydrology | Rivers, streams, lake basins, waterfalls, flooded passages | Navigable boat channels or exact flow without data |
| Flora | Ordinary flora and first-stage Genesis-expressed flora supported by local basin conditions | Every plant is vaen; every forest has a measured 70:30 ratio |
| Other organisms | Sparse larger fauna; possible Genesis-expressed invertebrates | A complete animal roster or exact species at every node |
| Crystals | Favorable formation regions and recurring deposits | Guaranteed harvest amount or a universal mine mechanic |
| Vaen | Recurring second-stage identity-bearing formation hotspots | First-stage expression alone makes an item vaen |
| Natural velis | Local field structures occurring naturally and available for study | Floating physical ru’ne or naturally inscribed sigils everywhere |
| ELDRIS | Formation propensity and local field conditions | Fixed populations, conventional breeding ecology, or guaranteed encounters |
| Genesis Dust | Recovery potential from destroyed ELDRIS | Naturally growing dust seams or geological dust deposits |

A forest’s energy support comes from the relevant stratum’s Genesis basin in the selected worldbuilding. Do not substitute a real-world illumination requirement as though that were already the authored mechanism. Exact organism-level processes remain available for later development.

The roughly 70% first-stage Genesis-expressed flora / 30% ordinary flora composition is an illustrative ecological mosaic. Vaen arise through a further specialized identity-bearing realization. Resource clusters may overlap a forest without making the entire forest a second-stage resource.

Natural velis and Architect-created velis are both local Genesis-field structures; their origin differs. Physical ru’ne are inscription components, and sigils are realized arrangements on substrates. The atlas should map **natural velis**, not free-floating manufactured glyphs. Historical research-site wording that uses older terms needs scoped reconciliation, not silent erasure of its provenance.

Map Genesis crystal formations within the dungeon without automatically redefining every formation field as a separate single-basin Genesis Mine. The framework distinguishes those environments and their rules.

## 21. Regions, nodes, and passages must remain separate

Use one node record for local attributes, one passage record for movement between nodes, and a separate regional record for features spanning multiple locations. A long river or extensive forest cannot be represented faithfully by an isolated point tag alone.

The reference environmental regions include 12 Genesis forests, 8 crystal fields, 7 vaen-formation regions, 8 natural-velis regions, and 9 ELDRIS-formation regions. Every saved region’s node membership induces a connected subgraph in the reference. [S6; current audit]

For a future implementation, select regional seed nodes according to geology and author constraints. Grow membership along actual adjacent passages, respecting strata and environmental constraints. Record the membership list, feature type, assignment status, and source decision. Apply a documented size policy rather than silently expanding every region to a fixed number of nodes.

Connectivity is necessary but not sufficient to describe physical extent. A connected five-node forest could occupy a small cluster or stretch across miles. Its actual area remains open until supplied. The hull of its nodes is only a display approximation, not automatically a forest boundary.

Overlapping regions are permitted when meaningful: a forest can contain a stream, crystal growth, and a velis observation area. Validate combinations rather than forcing mutually exclusive labels. Conversely, do not assign every valuable feature to every node; the map should create different expedition purposes and route choices.

The existing G062 high-formation region is proposed, based on an illustrative author example, not a preexisting documented sighting. The R001 forest region overlaps the surface entrance and remains an explicit review item. Preserve those qualifications when using the reference.

## 22. Waterways and lakes

The saved overlay contains 12 river features, 3 subterranean-stream features, and 9 lake anchors. Watercourse rows list an ordered node chain and the real passage IDs linking it. Lake rows are anchored at nodes; their shorelines and extent are not defined. [S6]

For each watercourse, verify that every consecutive pair of nodes shares the listed passage. A collection of connected nodes is not enough if the ordered edge list refers to different connections. Store explicit sources, sinks, flow direction, water surface elevations, and seasonal behavior only when authored or modeled.

A graph path alone is not a hydrological simulation. Gravity-driven flow requires a consistent hydraulic interpretation; increasing depth ordinarily means lower elevation in this convention, but a cavern node’s representative center is not necessarily its river’s water surface. Do not infer physical flow solely from node-center depth.

Treat **a passage following a river** differently from **a passage requiring a river crossing**. The same water feature can run alongside a dry ledge for miles before a single unavoidable crossing. A `river_or_stream` node tag does not imply that every incident edge crosses water.

For lakes, map access shores, natural ledges, inflows, outflows, and any relevant alternative routes as they are selected. Do not assume a lake can be crossed merely because a line connects two nodes through its region. Do not supply a carried boat to this vaelum; the author has explicitly rejected that default solution.

If a future watercourse crosses a stratum boundary, its own record can reference cross-layer geology. That does not authorize ELDRIS to cross their stratum confinement boundary.

## 23. Traversal difficulty: low, medium, hard

Difficulty is an edge property because the problem is moving **from one location to another**. A node can also summarize local maneuvering conditions, but it should not replace passage-specific records.

The current 003 labels are explicitly a heuristic based on length, elevation change, and water association. The exact numeric thresholds were not preserved. Do not claim a recovered formula or overwrite those saved labels with a guessed threshold scheme. [S6]

For a new classifier, define the perspective first: ordinary equipped aithren, current seven-person vaelum including Nyx, or another named party. Then document the variables, thresholds, missing-data behavior, and version. Keep physical traversal separate from ELDRIS risk and environmental field exposure.

| Label | Recommended interpretation for future authoring |
|---|---|
| Low | Comparatively manageable navigation under the stated equipment profile; no known major crossing bottleneck |
| Medium | A meaningful navigation, terrain, water, length, or coordination burden; preparation may be needed |
| Hard | Severe or combined obstacles, constrained clearance, major crossing/vertical challenge, or high setup burden |

These are ordinal labels, not invented times or probabilities. “Low” does not mean no monsters, no fatigue, or safe ambient Genesis conditions. “Hard” does not mean impassable. `OPEN` or `UNVERIFIED` is preferable to pretending missing geometry has been checked.

The current graph can supply centerline length, net depth change, segment gradients, and connectivity. It cannot supply unseen tunnel width, rope-anchor quality, water velocity, Nyx clearance, or the party’s actual skill without new data. Exact obstacles and crossing methods should be selected at the relevant passage, not inferred from line steepness alone.

When plotting difficulty, retain stratum identity by node color, prefix, or panel title and use edge style or a separate legend for difficulty. A second color system must never obscure which color represents a basin.

## 24. Dynamic conditions and professional knowledge

Keep changing conditions in a separate revisioned or dated layer. The stable graph persists through ordinary field oscillation. Monster formation, available crystals, vaen emergence, water level, congestion, and fatigue-related usability can change without rearranging the cave passages.

ELDRIS hotspots represent higher formation potential due to local Genesis-field topology and stratum conditions. They are not static monster placements. A transit expedition may avoid a hotspot while a Genesis Dust expedition intentionally seeks it. Dust appears through ELDRIS destruction, not simply because the node has high formation potential.

For a future condition record, use fields such as `node_id` or `edge_id`, observation time or story day, observation type, value, uncertainty, source, expiry/review date, and institutional owner. Do not fill them with invented expeditions just to make the map look complete.

The Accord Registry owns professional expedition and historical records in-world. The companion may describe expected conditions but must not claim to be a completed Registry survey unless that status has been selected. A mature dungeon can be well known while the author’s current digital atlas still contains proposed placements.

A physical collapse is a different kind of change from an oscillation. Record a scoped geological event and whether it temporarily blocks, permanently removes, or later restores a passage. Preserve the old topology with its validity period rather than deleting the evidence of earlier journeys.

## 25. Party capabilities and fantasy mechanics are route constraints

The topology does not itself decide who can traverse an edge. Build a separate party profile when movement simulation becomes necessary. It can record each member’s relevant movement capabilities, equipment access, clearances, and fatigue state without embedding those properties permanently in the cave.

For the current Violet group, the known design considerations include conventional ropes and equipment, the leader’s dimensional bracelet, a possible backup ring with owner unresolved, an air-specialist Offensive Specialist, existing leader CSR, later Kaira-crafted CSR, and demanding Sprite assistance for Nyx. Exact use at individual edges remains open. These are not universal equipment requirements for every future party.

Dimensional devices inherit their existing AERA mechanism; they are not unlimited pocket spaces invented by the atlas. Carrying equipment does not make a crossing instant. Access to a rope does not prove a usable anchor, and Nyx cannot be treated as another person who can use every rope crossing.

Keep CSR’s four-basin assignment—Orange, Yellow, Blue, Violet—consistent with the current catalogue revision when evaluating it. Active Genesis Cards impose exclusive basin occupancy; skilled Binding operation can share required basins subject to installed bandwidth, access, control, and fatigue. Do not assume a CSR Card can run simultaneously with every shield or attack merely because the inventory contains those Cards.

The approximate flight-duration bands and speed-dependent fatigue discussed in the workshop are not a calibrated movement simulator. Do not assign a universal flight speed, convert hours into guaranteed miles, or reset fatigue simply because a Card is deactivated. Preserve these as constraints to develop rather than unexplained routing advantages.

## 26. Route analysis and a reproducible worked test

For positive distance weights, a shortest-path computation can minimize total `modeled_centerline_mi`. The result is a shortest **model-distance** route, not automatically the quickest, safest, easiest, or best tournament route.

A large cyclic graph can contain very many possible simple routes. Do not promise to enumerate “every path” or attempt unrestricted enumeration. Ask for a bounded set of useful alternatives, an authored path, or a clearly defined optimization objective. An example future comparison might inspect the first few shortest simple routes, then evaluate hazards and equipment requirements separately.

For a route report, verify every consecutive node pair against an actual edge. Join node conditions by `node_id`, passage conditions by `edge_id`, and preserve source revisions. A row should identify the current node, depth, cumulative modeled distance, expected environment, the outgoing passage and next node, provisional difficulty, and all unresolved values.

The reference has two distinct tests:

| Route | Role | One-way modeled distance | Endpoint depth |
|---|---|---:|---:|
| R001 to B100 | Initial shortest-model-distance analysis to deepest numbered Blue node | 24.479642 mi | 17.000000 mi |
| R001 to B041 | Author-selected first vaelum trial itinerary | 17.787460 mi | 14.042512 mi |

The selected trial is:

```text
R001 → R018 → R023 → R025
     → O031 → O039 → O042
     → Y036 → Y055
     → G038 → G067
     → B041
```

Its passages are:

```text
E0001, E0041, E0039, E0661, E0150, E0129,
E0667, E0246, E0679, E0384, E0692
```

There are 12 node visits and 11 passages. The modeled same-path round trip is **35.574920 miles**. Traversal labels are 2 low, 3 medium, and 6 hard. The current package retested the exact selected sequence; it was not replaced by a newly optimized route. [S7; validation/FIRST_TRIAL_ROUTE_TEST.json]

B041 is inside Blue, not exactly at the 11.5-mile upper boundary and not at the 17-mile absolute modeled bottom. The official tournament marker is not established by this training choice. The first trial selects B041 as its marker and turnaround point; exact departure day, duration, encounters, and outcome remain open.

Removing B073, B072, B085, and B100 from the trial itinerary did not delete those nodes or their passages from the graph. Preserve that distinction whenever an expedition is shortened.

Use the included `tools/route_report.py` for a saved authored sequence or a shortest modeled-distance query. It intentionally does not calculate travel time or fabricate encounter counts.

## 27. Travel realism, fatigue, and marker objectives

For a new race or expedition, define the objective explicitly: a particular marker node, any eligible node in a target stratum, a resource site, a research site, or a return to a specified entrance. These are different routing problems.

If the objective is entry into a stratum, identify where entry actually occurs. A coarse inter-stratum edge may cross the boundary well before its deeper endpoint. Either specify a marker node inside the stratum, insert an explicit boundary node as an authored graph refinement, or use an edge-position objective with proper geometry. Do not silently equate “first Blue label” with the exact boundary crossing.

The selected Blue training marker at B041 is already explicit. Do not move it upward to 11.5 miles because a shortest-entry calculation finds an earlier point. An authored route is not invalid merely because an algorithm can find a shorter alternative.

Travel simulation requires more data than distance: speed by terrain, directional climbing costs, setup times, rest, environmental protection, combat or avoidance, congestion, loads, and cumulative fatigue. A trip with a short distance can still take many days if these demands dominate.

Preserve the earlier Blue Arc expedition chronology. The seven-day descent to Yellow was an established journey, not a calibration error to erase when a simplified graph shows a short centerline. Where a historical site has not yet been assigned a node, keep it unanchored until deliberately reconciled.

A race is a descent **and** a return. A faster descent may leave the party unable to survive or ascend. Future routing can compare time, risk, and fatigue as separate objectives; do not combine them into a numerical score without stating units, weights, and the intended decision.

## 28. Validation: structural, semantic, visual, and narrative

Validation is not one checkbox. Use four passes.

### Structural pass

Check unique node and edge IDs, finite coordinates, valid endpoints, no unintended self-loops or duplicate undirected edges, selected connectivity, correct strata and depth ranges, selected principal-width constraints, and exact polyline endpoint agreement. Recompute edge lengths and verify they are positive and no shorter than endpoint chords.

Check branch policy, terminal tips, adjacent-stratum linking, and biconnectivity only where selected. Recompute degree and neighbors. Compare JSON against node/edge CSVs, view indexes, adjacency exports, and GraphML. Compare graph geometry hashes before and after overlay generation to prove the overlay did not secretly alter the map.

### Environmental pass

Require exactly one profile per intended node and passage. Validate foreign keys, repeated coordinates, allowed difficulty labels, region connectivity, watercourse edge order, and graph revision/hash. Keep quantities, species, encounters, and times open where not established. Check the dust, vaen, velis, natural-crossing, and Accord Registry rules.

The included read-only audit performs 10,131 checks on the supplied reference without structural failure. Its remaining review items are explicit: R001’s proposed forest overlap and the absent original environmental generation code. This is not a complete geological or ecological certification.

### Visual pass

Render the pages, then inspect labels, clipped branches, axes, legends, adjoining-layer ghost endpoints, and the distinction between line crossings and junctions. Compare the same node in two plans/elevations and in the viewer. Check a region in its data before believing a colored shape in a map.

The actual source renderer was rerun for this methodology package. Its eight map pages and viewer rebuilt; the Yellow plan was visually inspected. This is not a claim that every font/renderer/platform will produce byte-identical PDF files or that a fresh city’s labels need no review.

### Narrative pass

Protect existing sites, dates, roles, and selected routes. Validate that a locked path still exists after edits. Do not award the party completed CSR, a new role, an official tournament marker, or a historical observation through a map-generation script. Check that proposed terrain has not quietly become a narrated event.

## 29. Exact reproduction versus adaptation

The preserved original generator was rerun in a fresh directory during creation of this manual. All **eight graph outputs matched the preserved reference byte-for-byte**, including the authoritative JSON. The exact graph SHA-256 is:

```text
2f5139f399f48a62f5ee0f3eff9e05f4ff9a89badecd9841305855ef2651f4f2
```

See [the reproduction report](validation/REPRODUCTION_REPORT.json). The tested Python and package versions are recorded in [TESTED_ENVIRONMENT.json](validation/TESTED_ENVIRONMENT.json), and dependency pins are in [requirements-tested.txt](requirements-tested.txt). These are the environment actually tested here, not a fabricated claim about the historical authoring machine.

Original dependency lists were unpinned. A future NumPy, SciPy, NetworkX, or rendering change may affect stochastic execution, Delaunay ordering, serialization, or glyph layout. Preserve the source scripts and graph outputs in addition to the seed. Never assume “same seed” proves “same atlas.”

The supplied original renderer creates eight map pages and individual image/vector exports. The earlier compiled atlas PDF also had guide material; the assembly script for that editorial wrapper is not included in checkpoint 004. The reusable map rendering is recovered; the exact guide-wrapper generation is not claimed.

For the environmental layer, exact reuse means copying the saved overlay tables with provenance. There is no original environmental generator in the archive to rerun. A new implementation must be identified as new and tested rather than described as recovered.

## 30. New-city adaptation checklist

Copy the reference implementation into a **new working directory**, not the existing Blue Capital live atlas. Give the new dungeon its own identity, selected strata, geometry, and seed. Then adapt every hard-coded assumption, not just the title.

| Component | Necessary adaptation |
|---|---|
| Generator | seed, `specs`, link counts, layer count, entrance choices, last-layer depth override, metadata, notes, expected layer set |
| Generator layer tests | replace hard-coded `ROYGB` assumptions with the selected ordered layers |
| Main renderer | titles, counts, palette, bounds, ticks, page sizing, layer captions, legend, scope language |
| Viewer | title, statistics, selectable layers, prefix search, palette, no-Violet notice, authority text |
| Validator | layer order, entrance policy, chosen biconnectivity/terminal policy, selected widths, optional extra strata |
| Environment builder | its own explicit implementation, parameters, seed, regions, graph-hash references, and rules |
| Route tools | new dungeon ID, selected objective, equipment profile, and no inherited character itinerary |
| Documentation | author constraints versus proposals; current source/version; protected historical locations |

The preserved generator’s `li == 4` and `17` maximum-depth override are Blue-specific. The renderer’s 17.55-mile plotting boundary and fixed depth ticks are also Blue-specific. The viewer and validators contain five-color assumptions. Search for them deliberately before running a Green-only or Violet-ending dungeon.

A valid fresh dungeon can share the same method without sharing the exact node counts, envelope shape, entrance arrangement, or biconnectivity policy. When there is no selected north–south extent, either ask for it during design or supply an explicitly provisional one. Never present a convenient square footprint as an author-selected measurement.

Run the reference regression before adapting code. Then validate the new atlas against its own specification, not against the Blue Capital hash. Keep the original reference as a test fixture; do not overwrite it with the new city’s generated data.

## 31. Cumulative checkpoints and source-preservation discipline

A checkpoint should contain everything promised for its declared scope. A cumulative project checkpoint is not necessarily a complete repository export, but it must carry forward its own prior payload and account explicitly for superseded files.

For each revision:

1. Unpack the exact parent in a new workspace and verify its archive integrity.
2. Inventory and hash every payload file before editing.
3. Preserve unrelated files byte-for-byte; record deliberate modifications and their authority.
4. Add new data and regenerate only derived products affected by the change.
5. Run graph, overlay, route, source-preservation, and visual checks.
6. Build a new **complete current manifest**, not merely a copy of the parent manifest.
7. Preserve older manifests under provenance when needed.
8. ZIP safe relative paths; test archive integrity and every declared checksum after writing.
9. Report exactly which artifacts were produced and whether any repository integration occurred.

The current source archive contains an inherited manifest that verifies its listed files but does not cover all later 003/004 additions. The methodology audit found no mismatches among the listed source files, but **16 payload files are not enumerated by that inherited manifest**. This is a manifest-coverage limitation, not proof that those files are missing or corrupted. See [SOURCE_AUDIT.md](provenance/SOURCE_AUDIT.md).

This methodology package supplies its own complete manifest. It does not rewrite the prior archive. The lesson for future revisions is to preserve old provenance **and** regenerate the current complete inventory.

Do not use a ZIP filename, size, or earlier assistant statement as proof of completeness. Count actual entries, validate hashes, inspect row coverage, and test the objects being handed off.

## 32. Execution recipes and acceptance gates

### A. Reproduce the reference safely

From the extracted methodology package, in a Python environment with the recorded dependencies:

```bash
python -m pip install -r requirements-tested.txt
python tools/verify_package.py
python tools/audit_atlas.py --atlas-dir reference/blue_capital
python tools/reproduce_reference.py --output ../blue_capital_reproduction --render --viewer
```

The output directory must not already exist. The wrapper refuses an overwrite, runs the preserved generator, compares all eight graph outputs, and optionally rebuilds maps and the HTML viewer. It does not regenerate Environmental Companion 003.

No package installation was needed during the local validation reported here; the installation command is supplied for a separate future environment. A dependency pin is a tested reference, not a guarantee of wheel availability on every operating system.

### B. Validate the locked first trial

```bash
python tools/route_report.py \
  --atlas-dir reference/blue_capital \
  --route-json templates/FIRST_TRIAL_REFERENCE.json \
  --output ../first_trial_check
```

The tool preserves the exact authored node sequence and produces Markdown, CSV, and JSON reports. It does not optimize away the author’s choice.

### C. Run a bounded analytical test

```bash
python tools/route_report.py \
  --atlas-dir reference/blue_capital \
  --start R001 --target B100 \
  --output ../deepest_node_distance_test
```

That query is an analysis-only shortest-model-distance route. It is not a story event or a substitute for the B041 trial.

### D. Render an edited existing atlas without recreating it

```bash
python reference/blue_capital/tools/validate_graph.py --atlas-dir /path/to/working_blue_atlas
python reference/blue_capital/tools/render_atlas.py --atlas-dir /path/to/working_blue_atlas
python reference/blue_capital/tools/build_viewer.py --atlas-dir /path/to/working_blue_atlas
```

These preserved scripts are Blue-specific. First update JSON and all synchronized exports with a controlled edit process. Do not call the initial generator against an established graph. For a new city, use adapted versions as described in section 30.

### Acceptance gates

**Specification gate:** included strata, units, constraints, provisional assumptions, and protected sites are explicit.  
**Graph gate:** IDs, geometry, connectivity, and synchronized exports pass.  
**Map gate:** every required view derives from the same graph and labels remain usable.  
**Environment gate:** records cover the graph, obey the corrected resource/velis rules, and retain open values.  
**Route gate:** at least one complete objective-and-return test joins to actual nodes and edges.  
**Continuity gate:** no selected event, site, or character capability was silently changed.  
**Packaging gate:** every delivered file is inventoried; cumulative preservation and ZIP integrity are verified.

A failure at any gate is reported at that scope. It does not justify inventing facts to make the file appear complete.

---

## Appendix A. Essential model invariants

**One graph, many views.** Every elevation, plan, environment lookup, and route report references the same permanent IDs and source revision.

**Stable identity, changing display.** Label placement and width-order aliases can change without moving or renaming physical nodes.

**Connectivity is not accessibility.** A geological passage may require climbing, ropes, flight, clearance, or a detour.

**A line crossing is not a junction.** Only an explicitly shared node creates graph adjacency.

**Main width is not maximum extent.** Terminal arms can extend laterally beyond the principal network.

**Independent cycles are not all routes.** For this connected graph, `709 - 340 + 1 = 370` is the cycle-space dimension. It does not count all simple paths or all plausible expeditions.

**A marker is not necessarily the deepest node.** Record the actual objective and keep deeper geography intact when shortening an itinerary.

**Environment is not an encounter script.** Hotspots and resources are expectations; observations and narrative events need their own authority.

**No automatic plot advancement.** Building or querying an atlas does not move the daily ledger beyond the selected story frontier.

**Preserve before adding.** A method archive and a new city’s atlas must not overwrite the current cumulative live model.

## Appendix B. Recovered schemas and field guidance

The tables below are generated from the actual reference headers. They are not a proposed replacement schema. Empty-header templates are supplied for consistent future datasets; the original reference data remains preserved separately.

### `nodes.csv` — 340 reference rows

| Field | Meaning / control |
|---|---|
| `stratum` | Named stratum; region rows in the existing overlay use its code rather than the full name. |
| `code` | Stable stratum prefix used by IDs and the selected layer order. |
| `x_mi` | East-positive horizontal coordinate in miles. |
| `y_mi` | North-positive horizontal coordinate in miles. |
| `depth_mi` | Downward-positive depth below the entrance, in miles. |
| `network_role` | Principal network or terminal branch; geological role, not a character role. |
| `branch_id` | Terminal-arm identity; empty for principal nodes. |
| `site_type` | Graph-layer location classification; the environmental layer supplies richer descriptions. |
| `node_id` | Permanent node identity; never replace with a display-order alias. |
| `west_to_east_index` | Derived snapshot ordering by x, then y, then depth; not permanent identity. |
| `north_to_south_index` | Derived snapshot ordering by decreasing y, then x, then depth. |
| `global_index` | Convenient record position in this snapshot, not a cross-revision ID. |
| `geography_status` | Authority/proposal status of the generated geographic record. |
| `in_world_survey_status` | Separate knowledge status; the original graph leaves this unassigned. |
| `degree` | Derived number of incident graph edges. |
| `neighbors` | Pipe-separated adjacent node IDs, derived from the edge list. |

### `edges.csv` — 709 reference rows

| Field | Meaning / control |
|---|---|
| `edge_id` | Permanent passage identity. |
| `source` | One endpoint; source/target order does not imply one-way travel. |
| `target` | Other endpoint; retain both endpoint identities. |
| `kind` | principal_passage, lateral_terminal_passage, or inter_stratum_passage. |
| `strata` | Named stratum, or both names separated by a pipe for a cross-layer edge. |
| `straight_line_mi` | Three-dimensional endpoint chord length. |
| `modeled_centerline_mi` | Computed sum of lengths along the stored 3D polyline; not surveyed travel time. |
| `depth_change_source_to_target_mi` | Signed target depth minus source depth. |
| `geometry_xyz_mi` | Ordered 3D vertices including endpoints; JSON array encoded as one CSV cell. |
| `direction` | Undirected geological topology in the reference; costs may become directional later. |
| `traversal_method` | Unresolved movement method unless deliberately supplied. |
| `travel_time` | Unresolved elapsed time, not calculated from line length alone. |
| `terrain_detail` | Graph-layer detail remains open; do not confuse with the separate environment companion. |
| `geography_status` | Authority/proposal status of the generated geographic record. |

### `environment_nodes_003.csv` — 340 reference rows

| Field | Meaning / control |
|---|---|
| `node_id` | Permanent node identity; never replace with a display-order alias. |
| `stratum` | Named stratum; region rows in the existing overlay use its code rather than the full name. |
| `x_mi` | East-positive horizontal coordinate in miles. |
| `y_mi` | North-positive horizontal coordinate in miles. |
| `depth_mi` | Downward-positive depth below the entrance, in miles. |
| `network_role` | Principal network or terminal branch; geological role, not a character role. |
| `geological_type` | Proposed local chamber/junction/terrain classification. |
| `region_ids` | Pipe-separated regional and water-feature references. |
| `hydrology` | Water association; does not by itself prove a mandatory crossing. |
| `genesis_flora` | Proposed flora context, including any illustrative forest mosaic. |
| `genesis_expression_ratio` | Illustrative or open composition; not an invented measured census. |
| `invertebrate_ecology` | Possible organism context; exact species remain open. |
| `genesis_crystals` | Formation/deposit expectation, not a guaranteed current harvest. |
| `vaen_formation` | Recurring identity-bearing formation potential; exact vaen identities remain open. |
| `natural_velis` | Naturally formed field structure/observation context, not physical inscription. |
| `eldris_formation_potential` | Expected formation intensity; not fixed creature count. |
| `genesis_dust` | ELDRIS-derived only; never a naturally growing geological deposit. |
| `historical_registry` | Explicit Accord Registry ownership; no fabricated observations. |
| `survey_status` | Overlay knowledge/proposal qualifier; distinct from graph geometry status. |
| `status` | Revision/authority qualification of the row. |

### `environment_passages_003.csv` — 709 reference rows

| Field | Meaning / control |
|---|---|
| `edge_id` | Permanent passage identity. |
| `source` | One endpoint; source/target order does not imply one-way travel. |
| `target` | Other endpoint; retain both endpoint identities. |
| `kind` | principal_passage, lateral_terminal_passage, or inter_stratum_passage. |
| `modeled_centerline_mi` | Computed sum of lengths along the stored 3D polyline; not surveyed travel time. |
| `depth_change_mi` | Signed end-to-end depth change repeated from the underlying passage. |
| `difficulty` | Provisional low, medium, or hard traversal classification. |
| `difficulty_basis` | Recorded heuristic basis; exact original thresholds were not supplied. |
| `natural_obstacle` | Proposed local terrain obstacle, not a finished crossing design. |
| `hydrology_crossing` | Potential water-crossing flag, not equivalent to mere river adjacency. |
| `equipment_requirement` | Equipment/method remains open unless separately authored. |
| `traversal_time` | Elapsed-time value remains open in the saved environmental companion. |
| `fatigue_cost` | No quantified model established in these records. |
| `eldris_encounters` | Variable, not preassigned actual encounters. |
| `status` | Revision/authority qualification of the row. |

### `environment_regions_003.csv` — 44 reference rows

| Field | Meaning / control |
|---|---|
| `region_id` | Permanent regional-feature identifier. |
| `stratum` | Named stratum; region rows in the existing overlay use its code rather than the full name. |
| `feature_type` | Forest, crystal, vaen, velis, or ELDRIS formation region. |
| `name` | Reference descriptive design label; not automatically an established place name. |
| `nodes` | Pipe-separated region membership or ordered watercourse chain, depending on the table. |
| `node_count` | Number of listed members; validate against actual unique IDs. |
| `assignment_status` | Explicit status of the environmental placement. |
| `continuity_note` | Source and qualification, including whether the feature was generated as a proposal. |

### `environment_waterways_003.csv` — 24 reference rows

| Field | Meaning / control |
|---|---|
| `feature_id` | Permanent water-feature ID. |
| `stratum` | Named stratum; region rows in the existing overlay use its code rather than the full name. |
| `type` | Feature category recorded in the reference; preserve the source vocabulary and status. |
| `nodes` | Pipe-separated region membership or ordered watercourse chain, depending on the table. |
| `passage_ids` | Ordered passages corresponding to a watercourse chain; empty for unexpanded lake anchors. |
| `status` | Revision/authority qualification of the row. |
| `note` | Unresolved flow, extent, or other qualification. |

## Appendix C. Suggested output directory for a new dungeon

```text
<UNIQUE_DUNGEON_ID>_ATLAS/
  README.md
  AUTHOR_DECISIONS_AND_SCOPE.md
  DATA_DICTIONARY.md
  ENVIRONMENT_COMPANION.md
  config/
    dungeon_spec.json
    generation_parameters.json
  data/
    dungeon_graph.json
    nodes.csv
    edges.csv
    adjacency.csv
    view_index.csv
    stratum_connections.csv
    dungeon_graph.graphml
    environment_nodes.csv
    environment_passages.csv
    environment_regions.csv
    environment_waterways.csv
    environment_summary.json
  maps/
    01_MASTER_DEPTH_NETWORK.png / .svg / .pdf
    02_SECOND_DEPTH_NETWORK.png / .svg / .pdf
    <one numbered plan per selected stratum>
    <common-scale plan overlay>
    <environmental views with their own legends>
    NETWORK_MAPS.pdf
  DUNGEON_EXPLORER.html
  tools/
    <adapted generator>
    <adapted renderer>
    <adapted viewer builder>
    <environment builder, now preserved explicitly>
    <validators and route reporter>
  validation/
    <machine-readable results and visual-check record>
  provenance/
    <source decisions, parent versions, changes, supersessions>
```

The example removes revision numbers from generic file names for readability. Select an actual repository versioning convention and apply it consistently. Do not rename existing `_003` files in an established atlas without updating every reference.

Dated expeditions and character route locks should remain in their event/arc owner with references to this atlas. They need not be copied into every geography directory. Accord Registry observations can have a distinct indexed data owner when developed.

## Appendix D. New-dungeon build pseudocode

The following is a procedural summary, not a claim that the old scripts already read the new template.

```text
read approved dungeon specification
load selected mechanics and protected historical constraints
freeze a generator version, random seed, and dependency environment

for each included stratum:
    place protected locations and entrance anchors
    distribute additional principal points irregularly over the selected footprint
    assign depths within the selected band
    build local candidate connections
    prune/modify according to the selected connectivity policy
    attach lateral terminal chains without unintended downward connections

connect neighboring strata through distributed principal-network passages
assign permanent node and edge identities once
build 3D passage polylines and measure their centerline lengths
compute adjacency, indexes, and metrics
export the authoritative graph and synchronized tables
validate geometry, topology, exports, and protected constraints

render both elevations, every plan, and the shared-scale overlay
build the offline explorer from the same authoritative graph
inspect output visually; improve labels without moving physical geography

create or preserve the environmental companion against the graph hash
validate feature memberships, watercourse chains, rules, and coverage
run an explicit objective-and-return route test
report expected conditions without creating actual encounters or dates

preserve prior payload and document all deliberate changes
write a complete current manifest and validate the final ZIP
```

## Appendix E. Failure cases that must not recur

**Independent redraw:** a plan shows a different neighbor set from the elevation. Remedy: render both from the same JSON and stored edge geometry.

**Artificial crossing created by an image:** an illustrative natural passage becomes a carved bridge. Remedy: separate edge existence, terrain, and movement method; keep the no-constructed-bridges rule.

**All routes become one path:** a tree or a single inter-stratum link defeats the intended extensive network. Remedy: use selected loop-rich core policies and multiple distributed layer connections.

**Every node becomes a landmark:** randomly adding lakes, crystals, and forests to all nodes eliminates meaningful geography. Remedy: build connected regions and allow ordinary junctions.

**Dust deposits:** a resource generator labels a cavern a naturally growing Genesis Dust mine. Remedy: dust potential references ELDRIS formation and destruction only.

**Velis/sigil confusion:** a map invents floating sigils where the author selected natural velis. Remedy: retain the distinction between local field geometry and manufactured substrate inscriptions.

**A path becomes an event:** finding a route silently advances a story day or assigns a monster kill. Remedy: keep analysis, selected itinerary, and completed expedition separate.

**Deepest-node mistake:** a training marker is forced to B100 because it is deepest. Remedy: preserve the selected B041 objective and any later author-selected target.

**Proposal erasure:** regenerated files remove the statement that coordinates or environmental placements are provisional. Remedy: preserve status and provenance as data, not a casual footer.

**Regeneration over live canon:** rerunning a seeded generator renumbers locations and destroys current edits. Remedy: refuse overwrite; edit the existing graph through a controlled versioned process.

**Incomplete cumulative manifest:** a parent manifest is retained without inventorying later payload. Remedy: keep the parent under provenance and generate a complete current manifest.

**Unsupported recovery claim:** a missing environment generator is replaced with a guessed formula described as the original. Remedy: preserve the actual tables and label any new implementation honestly.

## Closing standard

The atlas is successful when a future conversation can select a permanent node, trace real connections through the dungeon, inspect its expected conditions, and produce a coherent route report without recreating geography from memory. The pictures are synchronized views of that model. The model, its authority boundaries, and its reproducible construction are the durable asset.
