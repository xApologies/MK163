# MK163 Checkpoint 013 — Native White Superposition Charging

**Scope:** Global World Clock; additive to Checkpoint 012, not Yellow Arc-specific.

This checkpoint adds a complete six-target charging schedule for **7 mm** and **25 mm** Genesis Diamond cubes using the **native White-superposed equal-component mathematical model**, distinct from direct Genesis Card / Binding Circle charging.

## Mathematical calibration

Historical independent-basin Red charging references: Red 8 h, Orange 7 h, Yellow 5 h, Green 3 h, Blue 2 h, Violet 1 h for the original quarter-inch chip. As in checkpoint 012, use these as a **working calibration** for 7 mm. Under equal accessible White components and fixed total native transfer budget:

`r_white = (1/6) * (1/8 + 1/7 + 1/5 + 1/3 + 1/2 + 1) = 1933/5040 Red-equivalent charges/hour`

`T_white_7mm(empty→Red) = 1/r_white = 5040/1933 hours = 2 h 36 min 26 sec (rounded)`

`T_white_7mm(empty→target) = F_target * T_white_7mm(empty→Red)`

`T_white_25mm = T_white_7mm * (25/7)^3`, with exact volume multiplier `15625/343`.

Incremental times use `F_target − F_previous`, with prior empty threshold zero. Factors: 1, 13, 143, 1001, 5005, 15015.

**Provenance/correction:** Earlier conversation and checkpoint 012 also retained a **2 h 42 min** working figure; that was an author-accepted provisional calibration, not the exact result of the equal-six-component equation. This checkpoint tabulates the exact mathematical result **2.607346094 h**, not 2.7 h. The earlier 2.7 h figures remain historical and are not silently erased. A 2.7 h alternative would require an additional efficiency calibration. Neither rate establishes a biological fatigue limit.

**Conditional assumptions:** 7 mm transfer reference inherited from historical ¼-inch size; constant throughput; native equal accessible composition; 25 mm volume proportional storage with same input throughput; no fatigue/recovery/transfer interference; prime factors are assumed charge thresholds. All times are **active hours**, not calendar hours. Native White is NOT six independent full-rate streams. Direct-basin 63-combination matrix remains intact in nested Checkpoint 012.

## Cumulative active charging hours (from empty)

| Target | 7 mm (hours) | 25 mm (hours) |
|---|---:|---:|
| Red | 2.607346 | 118.774877 |
| Orange | 33.895499 | 1544.073398 |
| Yellow | 372.850491 | 16984.807374 |
| Green | 2609.953440 | 118893.651615 |
| Blue | 13049.767201 | 594468.258074 |
| Violet | 39149.301604 | 1783404.774222 |

## Integration

Retain the entire Checkpoint 012 nested archive byte-for-byte. Add native White CSV/JSON as a **separate pathway**, not as a 64th direct basin combination. Preserve crystal and diamond mass tables, price schedule, and existing 756 direct charging outcomes. No GitHub push has been performed.
