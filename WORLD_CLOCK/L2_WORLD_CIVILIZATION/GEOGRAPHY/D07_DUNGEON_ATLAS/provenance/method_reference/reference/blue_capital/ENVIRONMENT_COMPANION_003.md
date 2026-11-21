# Environmental Companion 003 — Blue Capital Dungeon

**Status:** PROPOSED environmental placements on the unchanged 002 graph. This is the second, linked atlas dataset; **not** a replacement graph and **not** a historical Accord Registry survey.

## Scope and evidence
- 340 node environmental profiles and 709 passage traversal classifications, keyed to exact existing IDs.
- 44 contiguous proposed Genesis-environment regions and 24 linked waterways/lake anchors.
- Passage difficulty counts: {'medium': 417, 'low': 213, 'hard': 79}.
- Existing 002 graph SHA-256: `2f5139f399f48a62f5ee0f3eff9e05f4ff9a89badecd9841305855ef2651f4f2`.
- No node IDs, coordinates, graph edges, historical events or old catalogue values changed.

## Source-authoritative constraints
- Geological and hydrographic features are naturally formed. **No manmade or carved bridges**; rock arches and ledges may be natural.
- Crystals form in recurring favorable conditions; vaen require first Genesis expression followed by second specialized identity-bearing realization. Map hotspots without inventing vaen species.
- Genesis Dust is harvested **only from destroyed ELDRIS**, not from geological deposits. ELDRIS hotspots represent formation potential, not permanent occupants or preassigned encounter counts.
- Natural **velis** are the mapped field phenomena. `ru’ne` and physical sigils are engineered substrate inscriptions, not free-floating cave features.
- Underground large fauna is sparse due to ELDRIS; Genesis-expressed invertebrates may occur. Exact species remain OPEN.
- Forest 70% first-stage Genesis expression / 30% ordinary flora is an illustrative mosaic, not an imposed measurement.
- Each stratum's oscillation periods and ELDRIS confinement are inherited from MK163; the atlas does not create new stratum crossing rules.

## Structure
- `environment_nodes_003.csv`: exactly one row per graph node; local geology, hydrology, flora, resources, velis, formation potential and linked region IDs.
- `environment_passages_003.csv`: exactly one row per graph edge; **low / medium / hard** provisional traversal difficulty, natural obstacle category and explicit unknown equipment/time/fatigue.
- `environment_regions_003.csv`: connected proposed forest, crystal, vaen, velis and ELDRIS formation regions with stable region IDs.
- `environment_waterways_003.csv`: connected watercourses referencing real graph edges, plus anchored lake basins. Flow direction and lake extent remain OPEN.
- `environment_summary_003.json`: audit metadata and graph checksum.

## Difficulty classification (proposal, not a travel-time simulation)
Low = short/low-slope graph connection without a modeled watercourse. Medium = one or two indicative difficulties (longer passage, slope or water). Hard = multiple indicators. These are heuristic initial classifications, **not measured in-world routes**, and natural bridges, ropes, CSR and environmental hazards require future manual verification. Geometry alone cannot prove passage accessibility.

## Accord Registry ownership
The Accord Registry owns expedition and historical records, route surveys, published professional maps, recorded harvest yields and dated site reports. This companion **does not invent Registry observations**. Its `historical_registry` column is intentionally unassigned. The Registry may eventually publish the resulting surveyed environmental map once author-approved.

## Continuity holds
- R001 remains the sole mapped entrance in this atlas; no Violet stratum created.
- G062 is **a proposed ELDRIS hotspot example**, following the author's illustrative suggestion, not a confirmed historical sighting.
- Previously established Yellow harvesting cavern, Green research site, Green cave-in rescue and Blue sites remain **unanchored** to avoid inventing coordinates.
- 002 node numbering and width order remain unchanged. Existing geographical extents are proposals except the selected 3/5/8/11/16 mi E-W principal spans and established depth boundaries.
- This package should be merged by Codex as a companion in MK163 L2; AERA L1 mechanics are inherited by reference, not duplicated.
