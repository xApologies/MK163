# B03 qualifier — five route planning options

Selected: **B**. Distances are modeled miles to activation threshold, not elapsed-time guarantees. Source: supplied dungeon atlas and companion; this is a conversation-derived route register.

## Route A — 14.689 mi (contingency)

`R001 R033 O022 O041 Y029 Y043 G022 G048 [B011 threshold]`

## Route B — 19.260 mi (SELECTED)

`R001 R019 R022 R036 O023 O045 Y025 Y041 Y044 Y063 G027 G043 G054 [B009 threshold]`

## Route C — 21.161 mi (contingency)

`R001 R012 R020 O004 O011 O014 O038 O045 Y025 Y041 Y044 Y063 G027 G043 G054 [B009 threshold]`

## Route D — 18.972 mi (contingency)

`R001 R012 R020 O004 O011 O022 O041 O048 Y037 Y051 Y064 Y068 G037 G048 [B011 threshold]`

## Route E — 19.754 mi (contingency)

`R001 R012 R020 O004 O011 O022 O041 O048 Y037 Y051 Y064 Y068 G037 G061 G071 [B027 threshold]`


## Verification and corrected units

All five routes connect in the unchanged Blue capital atlas. Threshold distances use full preceding centerlines plus the last passage multiplied by its endpoint-depth fraction to 11.5 miles. Source C/D/E figures 22.781 / 20.362 / 22.517 mi still ran to full endpoint nodes; corrected proportional boundary distances are 21.161 / 18.972 / 19.754 mi. Source A/B already use the boundary estimate. Exact polyline clipping is a different computation and remains separately recorded; do not imply surveyed precision or elapsed-time guarantees. All supplied values remain in immutable provenance.

## Retained provisional passage detail

The earlier full-passage comparison gives hard-passage counts A=4, B=2, C=1, D=2, E=2. These are provisional environmental classifications, not encountered incidents. B009 is a reference node at 12.570923 mi depth (x=-3.437716, y=-2.954476 mi), beyond the activation boundary. The full final passage length below is not the boundary distance.


| Passage | Distance (mi) | Provisional difficulty | Natural obstacle / hydrology |
|---|---:|---|---|
| R001 → R019 | 0.859 | medium | steep_natural_shaft_or_slope; not_assigned |
| R019 → R022 | 0.451 | low | natural_passage; not_assigned |
| R022 → R036 | 0.754 | low | natural_passage; not_assigned |
| R036 → O023 | 1.485 | hard | steep_natural_shaft_or_slope; not_assigned |
| O023 → O045 | 0.821 | medium | steep_slope_or_ledge; not_assigned |
| O045 → Y025 | 2.006 | hard | steep_natural_shaft_or_slope; not_assigned |
| Y025 → Y041 | 0.927 | medium | steep_slope_or_ledge; not_assigned |
| Y041 → Y044 | 0.781 | low | natural_passage; not_assigned |
| Y044 → Y063 | 1.294 | medium | long_irregular_passage; not_assigned |
| Y063 → G027 | 4.210 | medium | steep_slope_or_ledge; not_assigned |
| G027 → G043 | 1.199 | medium | steep_slope_or_ledge; not_assigned |
| G043 → G054 | 1.477 | medium | long_irregular_passage; not_assigned |
| G054 → B009 | 4.615 | medium | steep_slope_or_ledge; not_assigned |


The vaelum intends B unless actual conditions justify a contingency; five plans are not five traveled paths. No contingency must connect to B009: each activates at its own first qualifying Blue boundary. Exact in-world survey status and encounters remain OPEN. [Graph owner](../../../../../WORLD_CLOCK/L2_WORLD_CIVILIZATION/GEOGRAPHY/BLUE_CAPITAL_DUNGEON_ATLAS/README.md) · [Numerical audit](../../../../../CHECKPOINTS/WHITE_006/ROUTE_VALIDATION.json).
