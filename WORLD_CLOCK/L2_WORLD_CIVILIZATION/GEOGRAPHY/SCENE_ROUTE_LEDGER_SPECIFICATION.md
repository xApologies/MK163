# Scene routes as spatially constrained author records

## Governing author principle
MK163 scenes are not free-floating descriptions of characters traveling. The map is a geometric constraint. An author establishes the position of a character, a destination, the actual roads/paths between them, the speed of the relevant mode of travel, and the intervening actions. Time passes in the story according to that structure. Once a business, residence, landmark, or character workplace has been established along the route, its position is preserved. The universal map is progressively populated by the narrative; it is not regenerated to suit a later chapter.

## Map and route entities
A city has a unique identity, square outer perimeter, nested chromatic rings, known gate positions, orthogonal streets, building footprints, functional zones and topographic features. A zone may cover a single block, many blocks, or a mixed-use set of blocks. A block is not automatically a named building. Buildings have entrances and street-facing sides, and some blocks contain several businesses. Named locations need stable IDs and, once surveyed, exact block coordinates. A character's residence should be located on a street and a building, not simply 'Orange District' forever. However, it is correct to keep the exact coordinate OPEN until the author remakes the map.

A route record includes origin, destination, route geometry, departure, travel mode, load, distance, elapsed movement time, stops and stop durations, arrival, character state, and observations along the way. A scene may involve several legs. The record distinguishes the path itself from the narrative event that occurred on that path. The same physical route can be traversed on a different day at a different speed, under a different weather condition, with different companions, and with a different purpose. The spatial geometry persists; the event timing may change.

## Eighth-mile geometry
The older city map was constructed in eighth-mile blocks. One eighth mile is exactly 660 feet, not 600 feet. The area of one 660-by-660-foot square is 435,600 square feet, or ten acres. A nominal ten-mile side corresponds to eighty such block lengths, but streets, wall thickness, canals and nonuniform block geometry can alter how many actual occupied building blocks fit within the boundary. Do not assert eighty building blocks on each side as a finalized map unless the author verifies it. A 10×10-mile city has a 100-square-mile footprint. It is not 100×100 miles.

If a path is composed of orthogonal block-length segments, a convenient planning distance is D = 0.125 × N miles, where N is the number of traversed block sides. More accurate maps should store lengths in feet, including offsets inside blocks and intersection distances. The author wants precision down to feet where the map supports it. Distances between district labels cannot be inferred from labels alone: ring widths and the actual route matter. The direct Euclidean displacement is a lower bound, not a valid walking itinerary through walls or closed streets.

## Duration and calendar
Walking time equals path length divided by realistic average movement speed plus the time spent shopping, talking, resting, waiting at gates, navigating a crowd, loading cargo, or stopping for food. Three miles per hour is a normal-human walking reference, not a hard speed for Kaira, an elderly character, a heavily loaded merchant or a trained courier. The local 31-hour day has 3100 as the end-of-day boundary in its clock notation; scene times should never silently use a 24-hour modulo. A planned 0500 wake-up and roughly 2800 sleep time are author examples, not universal mandatory citizen schedules. The nightfall reference near 2100 was discussed as a convenient average, not a calculated solar model. If exact dawn/sunset is not known, mark it OPEN.

An example of a mapped route from Orange to a Blue District location could be three hours of walking, but that is illustrative until the city map is redrawn. Once measured, the narrative must honor the value. The author specifically objected to stories where a character 'goes across town' and the prose immediately cuts to arrival without accounting for elapsed time. A time ledger makes that cut deliberate rather than contradictory.

## Directional observations and permanent business placement
When Kaira walks a street and passes a bakery on the left, that bakery should still be on the left when she traverses the same street in the same direction later, absent an explicit move, closure or redevelopment. When she reverses direction, the bakery appears on the opposite side. A recurring shopkeeper, tavern, plaza, city gate, garden or fountain should likewise retain a stable spatial identity. This provides opportunities for incidental social relationships without requiring a new plot. The map is a reusable atlas for the entire seven-book series.

The city key's 'Misc Services' designation is reserved capacity. If a scene needs a business not previously mapped, place it in a suitable Misc Services block, assign the building identity, and update the map. This is not a license to invent a bakery at every intersection or move an already established bakery for convenience. A block may remain partially Misc Services after one establishment is named.

## Recommended machine-readable scene fields
- scene_id, book, arc, chapter_working_id, author_status
- location_origin_id, location_destination_id
- street_path_ids, block_ids, gate_ids, turn_direction, left_right_landmarks
- distance_feet, distance_miles, measurement_source, uncertainty
- mode, estimated_speed_mph, load/terrain modifiers, movement_minutes
- stops with location, start time, duration, purpose and participants
- departure_local_time, arrival_local_time, local_day_index
- character_knowledge, public_knowledge, reader_knowledge
- permanent_new_map_entities, changed_map_entities, continuity_notes
- unresolved_map_coordinates and pending measurements

These fields are an authoring template, not a demand to write a database application. Do not add actual route values until measured. The established Village Hub delivery circuit is an example of this system in practice.
