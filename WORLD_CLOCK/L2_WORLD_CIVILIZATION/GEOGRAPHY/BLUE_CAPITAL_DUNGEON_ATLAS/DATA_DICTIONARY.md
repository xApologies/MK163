# Graph data dictionary

`dungeon_graph.json` owns the model. JSON, CSV and GraphML contain the same node IDs and undirected edge endpoints. The JSON and edge CSV include proposed 3D centerline vertices; GraphML carries node coordinates and weighted connectivity.

## Nodes

`node_id`: permanent colored ID, e.g. Y023. `global_index`: sequential lookup number for this snapshot. `code`/`stratum`: R/Red, O/Orange, Y/Yellow, G/Green, B/Blue. `x_mi`, `y_mi`, `depth_mi`: east, north and downward coordinates in miles. Coordinate decimals are numeric reproducibility, not claimed survey precision.

`network_role`: principal or terminal_branch. `branch_id`: terminal-arm identity where applicable. `site_type`: unassigned junction/chamber, lateral junction, terminal chamber or surface entrance; this is not a populated biome roster. `degree` and `neighbors`: derived from the edge list. `west_to_east_index`: current sorting position by x, then y, then depth. `north_to_south_index`: current sorting position by decreasing y, then x, then depth. Sorting aliases may change; IDs do not.

`geography_status`: DESIGN_PROPOSAL_002. `in_world_survey_status`: UNASSIGNED; the author map is not automatically available to characters.

## Edges

`edge_id`: stable E-number. `source`/`target`: the two node IDs; this order does not imply one-way travel. `kind`: principal_passage, inter_stratum_passage, or lateral_terminal_passage. `geometry_xyz_mi`: four proposed 3D vertices including both endpoints. `straight_line_mi`: Euclidean endpoint chord. `modeled_centerline_mi`: sum of segment lengths in the proposed polyline, not an empirical walking distance. `depth_change_source_to_target_mi`: signed end-to-end depth change.

`direction`: UNDIRECTED_TOPOLOGY. Actual climbing, water flow and equipment could make passage costs directional; those are not specified. `traversal_method`, `travel_time`, `terrain_detail`: OPEN.

## Counts

Degree sum equals twice the edge count. For this connected undirected graph, cycle-space dimension is E - V + 1 = 709 - 340 + 1 = 370. This is a count of independent cycles, not a count of all possible routes or guaranteed practical itineraries.

## Conditions and route records — future separate owners

Future dynamic records may reference node/edge IDs for ELDRIS presence, environmental exposure, congestion, collapse/clearance, rope anchoring, visibility or supply stops. Expedition records may reference ordered node/edge sequences and dated observations. Do not overwrite fixed topology simply to reflect changing field conditions. Geological change, when deliberately selected, requires a scoped revision.
