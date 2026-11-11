# MK163 — Genesis Crystal Normalization · Yellow Arc Working Checkpoint 007

**Author-approved revision in current conversation; NOT yet integrated into GitHub.** This is a cumulative *addition* to the closed Orange Arc checkpoint 006, not a replacement of the prior checkpoint or its historical source files. Preserve earlier decisions and provenance, marking superseded density proposals as historical only.

## Locked choices

- Six source basins Red, Orange, Yellow, Green, Blue, Violet. White is their superposition, not a seventh independent basin; no White mass derived here. Ultraviolet is retired from the active charge ladder; retain previous descriptions only as provenance.
- Reference Genesis crystal cube edge **25 mm**, Red mass **100 g**, reference volume **15.625 cm³**.
- Small Genesis crystal cube edge **7 mm**, volume **0.343 cm³**. This is a *Genesis crystal* comparison cube, not a manufactured diamond chip; the diamond-chip carbon mass is separate.
- Same-basin cubes at the two sizes have the same modeled effective mass density, so mass scales with the **cube of edge length**. Volume ratio (7/25)^3 = **0.021952**; 25-mm cube contains **45.55393586** small-cube volumes. This is volume equivalence, not an exact packing count of intact 7-mm cubes.
- The author accepted the logarithmic **phenomenological** mass normalization: `m25(F) = 100 g × [1 + 0.2 log10(F)]`; `m7(F) = m25(F) × (7/25)^3`. The 0.2 is a *selected model parameter*, not derived from conventional E=mc² or measured mineral properties.
- Prime energy equivalence remains unchanged: `13 Red = 1 Orange`, `11 Orange = 1 Yellow`, `7 Yellow = 1 Green`, `5 Green = 1 Blue`, `3 Blue = 1 Violet` (normalized cumulative factors 1, 13, 143, 1001, 5005, 15015). This is an energy-equivalence ladder, **not a direct multiplier of crystal total mass**.
- Dimensionless basin reference coordinates: Red 1/7, Orange 2/7, Yellow 3/7, Green 4/7, Blue 5/7, Violet 6/7. These are *normalized state coordinates*, not literal physical energy density. Distinguish `q_b` (coordinate), `F_b` (energy equivalence), `ρ_b` (effective mass density), and `u_b` (physical Genesis energy per volume, not calibrated in joules/cm³).
- Existing MK163 author-approved crystal market reference prices per kg remain unchanged: 200, 350, 600, 1100, 2300, 5000 eln for Red→Violet; White 31000 eln/kg remains a price only, with White physical density OPEN.

## Exact model and units

`V25 = (2.5 cm)^3 = 15.625 cm³`  
`V7 = (0.7 cm)^3 = 0.343 cm³`  
`ρ_b = m25_b / 15.625 cm³`  
`m7_b = ρ_b × 0.343 cm³`  
`q_b = k/7, k=1..6`  
`F_b = ∏ step primes through basin b`.

## Derived values

| Basin | q | F | Mass 25 mm (g) | Mass 7 mm (g) | Density (g/cm³) | Price 25 mm (eln) | Price 7 mm (eln) |
|---|---|---:|---:|---:|---:|---:|---:|
| Red | 1/7 | 1 | 100.0000 | 2.1952 | 6.4000 | 20.0000 | 0.4390 |
| Orange | 2/7 | 13 | 122.2789 | 2.6843 | 7.8258 | 42.7976 | 0.9395 |
| Yellow | 3/7 | 143 | 143.1067 | 3.1415 | 9.1588 | 85.8640 | 1.8849 |
| Green | 4/7 | 1,001 | 160.0087 | 3.5125 | 10.2406 | 176.0095 | 3.8638 |
| Blue | 5/7 | 5,005 | 173.9881 | 3.8194 | 11.1352 | 400.1726 | 8.7846 |
| Violet | 6/7 | 15,015 | 183.5305 | 4.0289 | 11.7460 | 917.6525 | 20.1443 |

Prices for cut cubes are **arithmetic implications** of the existing per-kg price schedule under the new model; actual retail markup, cutting costs, local market variations and transaction conventions remain OPEN.

## Explicit nonclaims and boundaries

1. A logarithmic mass response is an author-selected fiction material law, not a derivation from standard mass-energy equivalence. The steep prime energy ladder remains independent of the much milder mass response.
2. The 1/7..6/7 coordinates are not joules, grams, density, charge thresholds, or probabilities. They do not numerically replace F or ρ.
3. A 7-mm Genesis crystal is not automatically the same as a 7-mm **diamond chip**. A diamond chip is a sigil-grown carbon lattice; its uncharged mass is approximately 1.205645 g at real diamond density 3.515 g/cm³. Charged chip masses and capacity require a separately established Genesis energy-to-mass coupling and occupancy model. Do **not** add the entire crystal mass to a diamond without an explicit physical assumption.
4. White superposition energy and physical mass remain OPEN; no extrapolation to a seventh rung. Ultraviolet is retired as an active source/charge category per latest author decision.
5. The log formula is defined for the six canonical discrete F values. It is not evidence for a continuous physical response outside them.
6. Historical density examples (3.0–6.5 g/cm³, 10% ladder, etc.) are superseded as current crystal-mass models; retain their provenance if encountered.

## Canon integration destinations (for Codex, later)

- MK163 `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md` — append scoped current model, preserve earlier text.
- MK163 `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md` — 7-mm diamond-chip geometry and active Red–Violet classification, with distinct mass accounting.
- MK163 `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md` — reference new cube-price derivations without replacing per-kg schedule.
- MK163 `WORLD_CLOCK/CURRENT_MODEL_INDEX.md`, Yellow Arc ledger and checkpoint history — add navigation and supersession notes.
- AERA — later upstream alignment; **no AERA push is implied or performed**.

## Sources

MK163 repository: `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md`, `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md`; MK-147 `live-model/02_DOMAINS/DIAMONDS_CURRENCY_EQUIPMENT.md`; author's latest conversation decisions. Previous Orange checkpoint 006 remains separately preserved, not embedded here.
