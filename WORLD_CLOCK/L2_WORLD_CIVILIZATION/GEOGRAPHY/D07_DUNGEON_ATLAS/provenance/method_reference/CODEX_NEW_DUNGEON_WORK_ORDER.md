# Codex work order — create another dungeon using the preserved atlas method

This is a reusable task template. It does not authorize or define a new city on its own.

## Inputs required

Read the new dungeon's selected city and identity; included strata; depth intervals; principal east–west dimensions; north–south choices or explicitly provisional assumptions; entrance positions; protected events/sites; expected graph density; and any topology exceptions. Use `templates/NEW_DUNGEON_SPEC.json` to record these decisions. Its null values are deliberate missing inputs, not zero dimensions.

Do not treat Blue Capital's exact numbers, B041 marker, characters, histories, or environmental placements as universal defaults.

## Phase 1 — recover and understand

Read `DUNGEON_MAPPING_STANDARD.md`, especially authority, coordinates, stable IDs, exact generation, rendering, environment scope, and section 30's adaptation matrix. Verify the method package. Inspect the existing target repository before writing. Recover the designated source data instead of reconstructing it from thumbnails or a previous assistant's description.

## Phase 2 — implement a new parameterized build

Copy the reference implementation into a new development location and adapt it. Prefer explicit configuration loading for new code. Preserve the immutable reference files. Record the adapted code version, random seed, and dependency versions.

Replace Blue-specific assumptions throughout: layer count/order, `li == 4`, maximum depth 17, `ROYGB`, width/depth tables, titles, statistics, view menus, palette, search prefixes, and authority notes. A future Violet stratum requires real data and selected dimensions, not just a menu entry.

Construct a spatially distributed principal network with the selected loop/connectivity policy. Add multiple distributed links between adjacent strata and lateral termination arms that do not inadvertently descend. A source variable named `portals` refers to ordinary graph connections, not magical portals.

Assign permanent IDs once. Create actual 3D polylines and derive distance, adjacency, and view indexes. Preserve every authored anchor. Stop and report a conflicting hard constraint rather than moving a historical site silently.

## Phase 3 — synchronize all map products

Export graph JSON, node/edge CSVs, adjacency, display-order indexes, layer links, GraphML, and validation metrics. Render both depth projections, a plan for each selected stratum, and a shared-scale overlay from exactly the same polylines.

Preserve physical coordinates while improving label placement. Show neighboring-stratum endpoints, line-style meanings, axis units, scale qualifications, and the distinction between crossings and junctions. Produce useful image/vector/PDF exports and an offline viewer. Inspect the rendered results rather than accepting files solely because the process exited successfully.

## Phase 4 — environmental companion and routes

Write and preserve the environmental-generation program; it was absent from the historical checkpoint and must not be invented retrospectively. Record deterministic selection parameters for this new build. Place connected regions and waterways before assigning local expectations. Give every intended node and passage a keyed profile with status.

Apply the author's natural geography and corrected resource rules: no man-made/carved bridges; no default carried boat; local-basin-supported Genesis forests; first-stage expression distinct from second-stage vaen; crystals form naturally; Genesis Dust is ELDRIS-derived; naturally occurring field structures are velis, not floating manufactured sigils; large fauna is sparse while suitable invertebrates may exist.

Use low/medium/hard passage difficulty with an explicit new classification basis, not a falsely recovered old formula. Separate ordinary terrain, ambient field exposure, ELDRIS formation potential, and current encounters. The Accord Registry owns actual survey and expedition history; do not fabricate its records.

Test at least one selected-depth route and a return. Distinguish target-stratum entry, a chosen marker, and absolute deepest node. Preserve author-selected itineraries even if another route minimizes distance. Produce a node-by-node expected-conditions report with actual passage IDs and unresolved time/fatigue/encounter values retained.

## Phase 5 — validate, package, integrate

Check graph integrity, selected widths/depths, policy compliance, cross-file agreement, region/waterway connectivity, profile coverage, visual readability, route validity, and historical continuity. Include failure and review items explicitly.

Build a complete manifest with sizes and hashes for the actual output. Preserve parent payload in any cumulative checkpoint and document scoped supersessions. Reopen the final ZIP, verify integrity and checksums, and report what was really tested. Do not claim remote publication before it occurs.

## Required final handoff

Deliver the new atlas, environmental companion, reproducible tools, source/authority notes, validation results, route-test report, and integration instructions. Explain which items are author-selected, computational proposals, or still open. Report unresolved constraints rather than silently filling them with generic fantasy assumptions.
