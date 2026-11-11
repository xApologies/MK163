# MK163 — Universal Diamond & Energy Structuring: Charging Matrix

**Checkpoint 012 — global World Clock / energy and diamond technology, not Yellow Arc.**

## Scope

Complete enumeration of **63 nonempty subsets** of six independently accessed basins (6 singles + 15 pairs + 20 triples + 15 quadruples + 6 quintuples + 1 sextuple). For each subset, both **7 mm** and **25 mm** diamond cubes, six stored targets Red–Violet, and both **empty→target cumulative** and **previous state→target incremental** charging times are tabulated. **756 rows**. Tables are in CSV and JSON. A smaller 63-row CSV gives Red-charge times for quick lookup.

## Locked historical input references / working assumptions

- Original **¼-inch** empty→Red single-basin reference: Red 8h, Orange 7h, Yellow 5h, Green 3h, Blue 2h, Violet 1h. Their reuse for a **7 mm** standard chip is a working calibration, not an experimentally or canonically derived resizing law.
- Stored target thresholds in normalized Red equivalents: Red 1; Orange 13; Yellow 143; Green 1001; Blue 5005; Violet 15015. Incremental requirements: 1, 12, 130, 858, 4004, 10010.
- **Input basin is distinct from stored diamond charge state.** Direct Violet input is sorted by the diamond and does not instantly create a Violet-charged diamond.
- For each selected subset S, assume independent **full-rate simultaneous transfer** and additive rates: `r(S) = sum(1/t_i for i in S)` in Red-equivalent charges/hour; `T_7(empty→target) = F_target / r(S)`; `T_7(previous→target) = (F_target−F_previous)/r(S)`.
- 25 mm extension: multiply times by `(25/7)^3 = 45.553935860058`. This **provisional** volume-capacity model assumes equal capacity per volume and unchanged total input rate; possible multi-face charging, geometric bottlenecks, and large-device engineering are not settled.
- Values are **active charging hours**, not elapsed days. Fatigue, rest, card/circle channel limits, efficiency, simultaneous access constraints, and changing rates as charge rises remain **unresolved**. Binding Circles and Genesis Cards are two direct-access mechanisms, not automatically distinct throughput rates.
- **Native White superposition is a separate pathway**: author-accepted working baseline 2h42m empty→Red for 7mm; the equal-share derivation gives about 2h36m, an unresolved calibration difference. Do not treat native White as six independent full-rate channels or interpret 2h42m as a universal fatigue limit.
- This checkpoint **does not modify** prior crystal/diamond masses, crystal prices, structural coordinates 1/7–6/7, or prime factors. White remains superposed; Ultraviolet is retired.

## Examples

| Independent direct input | 7mm empty→Red | 25mm empty→Red |
|---|---:|---:|
| Red only | 8.000000 h | 364.431487 h |
| Orange only | 7.000000 h | 318.877551 h |
| Yellow + Blue + Violet | 0.588235 h | 26.796433 h |
| All six independent | 0.434558 h | 19.795813 h |

## How to use

Filter `ALL_756_CHARGING_OUTCOMES.csv` by `channels`, `diamond_edge_mm`, and `target`. `empty_to_target_active_hours` gives the full charge time. `previous_to_target_active_hours` gives the incremental charge time. The 63-row overview provides all possible basin combinations and Red charge times. CSV stores unrounded floating-point results for calculation; round only for display.

## Integration / provenance

This is an **additive** World Clock checkpoint. Preserve the entire previous Checkpoint 011 (embedded unchanged) and its nested earlier archives. Merge these files into the existing diamond/Genesis-energy domain; do not duplicate old story arc files or overwrite canon. Historical single-basin references derive from `xApologies/MK163/WORLD_CLOCK/L2_WORLD_CIVILIZATION/TECHNOLOGY/GENESIS_DIAMONDS.md` and `xApologies/Mk-147/live-model/02_DOMAINS/DIAMONDS_CURRENCY_EQUIPMENT.md`; direct-basin assumptions and calibration are inherited from Checkpoint 011. **No GitHub push is performed.**
