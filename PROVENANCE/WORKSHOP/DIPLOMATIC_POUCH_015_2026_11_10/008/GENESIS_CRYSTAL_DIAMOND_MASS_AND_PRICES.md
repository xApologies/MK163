# MK163 — Genesis Crystal and Diamond Mass & Crystal Pricing Standard

**Checkpoint 008 — Yellow Arc working canon, 2026-11-10.** Author-approved normalization and additive fictional mass convention. This document supersedes only prior illustrative mass tables, not unrelated AERA cosmology. Repository integration pending; no push performed.

## Definitions and scope

- **Six chromatic basin structural coordinates:** Red 1/7, Orange 2/7, Yellow 3/7, Green 4/7, Blue 5/7, Violet 6/7. These are *dimensionless energy structure coordinates*, **not** energy quantity, physical density or mass. White is the superposition, and has no assigned cube mass here. Ultraviolet is retired from the active charge-state progression; preserve old references as historical provenance.
- **Prime equivalence:** 13 Red = 1 Orange; 11 Orange = 1 Yellow; 7 Yellow = 1 Green; 5 Green = 1 Blue; 3 Blue = 1 Violet. Cumulative factors: 1, 13, 143, 1001, 5005, 15015. These describe normalized energy equivalence, not the multiplier for total mass.
- **Raw Genesis crystal reference:** 25 mm edge Red cube has exactly 100 g mass; all six raw-energy crystalline cubes use the selected phenomenological logarithmic normalization. This is fictional canon, not a consequence of measured E=mc².
- **7 mm cube:** a standardized volume comparison for raw crystal, and the standard mass-produced diamond-chip geometry. The 25 mm diamond is a larger standardized comparison object, not a chip.
- **Diamond:** manufactured carbon-lattice container; at a given basin configuration its total modeled mass equals raw Genesis-energy mass at the same cube volume plus ordinary diamond carbon-lattice mass. This additive rule is author-selected fiction, not established real-world energy storage physics. It supersedes earlier illustrative 101 g total for a 25 mm Red diamond; that total is 154.921875 g in the adopted convention.

## Equations

```
V25 = (2.5 cm)^3 = 15.625 cm^3
V7 = (0.7 cm)^3 = 0.343 cm^3
r = V7 / V25 = (7/25)^3 = 0.021952
F = [1, 13, 143, 1001, 5005, 15015]
m_raw25(F) = 100 g * [1 + 0.2 * log10(F)]
m_raw7(F) = r * m_raw25(F)
rho_carbon = 3.515 g/cm^3
m_carbon25 = rho_carbon * V25 = 54.921875 g
m_carbon7 = rho_carbon * V7 = 1.205645 g
m_charged_diamond(edge,F) = m_raw_energy(edge,F) + m_carbon(edge)
price_raw(edge,F) = mass_raw(edge,F) / 1000 * basin_price_eln_per_kg
```

**Physical clarification:** fixed volume + increasing mass implies increasing effective mass density. At fixed mass, cube edge decreases as the cube root of inverse density. The 0.2 logarithmic coefficient is an author-selected normalization, not inferred from prime factors or mass-energy equivalence. The raw crystal is modeled as crystalline Genesis energy; diamond adds a separate carbon container. Real diamond density is used as an approximation for the uncharged carbon lattice, assumed unchanged on charging for this calculation.

## Complete reference table

| Basin | Structural coordinate | Prime factor | Raw crystal 25 mm (g) | Raw crystal 7 mm (g) | Charged diamond 25 mm (g) | Charged diamond 7 mm (g) | Crystal eln/kg | Raw 25 mm price (eln) | Raw 7 mm price (eln) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Red | 1/7 | 1 | 100.0000 | 2.1952 | 154.9219 | 3.4008 | 200 | 20.0000 | 0.4390 |
| Orange | 2/7 | 13 | 122.2789 | 2.6843 | 177.2007 | 3.8899 | 350 | 42.7976 | 0.9395 |
| Yellow | 3/7 | 143 | 143.1067 | 3.1415 | 198.0286 | 4.3471 | 600 | 85.8640 | 1.8849 |
| Green | 4/7 | 1,001 | 160.0087 | 3.5125 | 214.9306 | 4.7182 | 1,100 | 176.0095 | 3.8638 |
| Blue | 5/7 | 5,005 | 173.9881 | 3.8194 | 228.9100 | 5.0250 | 2,300 | 400.1726 | 8.7846 |
| Violet | 6/7 | 15,015 | 183.5305 | 4.0289 | 238.4524 | 5.2345 | 5,000 | 917.6525 | 20.1443 |

## Established crystal market schedule

| Basin | eln per kg | eln per 100 g | eln per g |
|---|---:|---:|---:|
| Red | 200 | 20 | 0.20 |
| Orange | 350 | 35 | 0.35 |
| Yellow | 600 | 60 | 0.60 |
| Green | 1,100 | 110 | 1.10 |
| Blue | 2,300 | 230 | 2.30 |
| Violet | 5,000 | 500 | 5.00 |
| White (superposition) | 31,000 | 3,100 | 31.00 |

**Price example:** 25 mm Red raw crystal = 100 g × 0.20 eln/g = **20 eln**. A 7 mm Red raw crystal = 2.1952 g × 0.20 eln/g = **0.43904 eln**. The mass and price of a White reference cube are OPEN. The table prices **raw Genesis crystal only**. There is **no approved market price for a charged diamond chip**, Genesis Dust, or empty diamond; charged-diamond mass does not by itself establish a selling price. The diamond is reusable and charging requires time, labor, and energy; these may affect trade value. Crystal prices are per unit mass and are not automatically equal to price of equivalent stored diamond energy.

## Verification / anti-counterfeiting

A mass check at standardized geometry and charge is a useful **screen**, not proof. For instance, a 25 mm Red-charged diamond has predicted mass 154.921875 g; a visually similar ordinary red gemstone need not match. A sophisticated counterfeit might be weighted to match; verify dimensions, carbon-lattice identity, and Genesis charge-state using an appropriate sigil. Do not claim mass alone makes counterfeiting impossible.

## Provenance and repository integration

- MK163: `WORLD_CLOCK/L2_WORLD_CIVILIZATION/ECONOMY/GENESIS_CRYSTAL_MARKET_PRICES.md` — canonical price schedule, including White.
- MK163: `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md` — carbon lattice, organized energy, historical states and geometry.
- MK163: `WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_CRYSTALS_DUST_AND_VAEN.md` — resource distinction and crystal-market owner.
- Mk-147: `live-model/02_DOMAINS/DIAMONDS_CURRENCY_EQUIPMENT.md` — inherited prime energy ladder.
- This conversation, 2026-11-10: author selection of 25 mm Red 100 g, 7 mm chip, logarithmic coefficient 0.2, additive diamond mass convention, removal of active UV, and price/mass integration.

Integration must **update existing owners** rather than create duplicate conflicting canon files. Keep prior sources as historical provenance. Checkpoint 006 Orange completion remains closed; 007 is prior Yellow crystal delta; 008 adds crystal/diamond prices and mass. Do not promote any unapproved dust or diamond selling price. Do not push automatically.
