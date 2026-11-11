# MK163 — Checkpoint 010: Audit Repair and 25 mm Diamond Charging

**Scope:** Cross-arc world-system standard. **Status:** author-approved 7 mm calibration; 25 mm extension is conditional on linear volume/capacity scaling.

## Checkpoint 009 audit

The actual 009 archive was opened and tested. Its 008 embedded archive was also opened and tested. The raw-crystal/charged-diamond mass tables and prices are in `008/REFERENCE_TABLE.csv` within embedded 008. The 7 mm charge ladder is in `009/CHARGING_LADDER.csv` within embedded 009. Checkpoint 009 did **not** include 25 mm charging times. This checkpoint repairs that omission.

## Assumptions and equations

- Equal-access White superposition 7 mm Red charge baseline = **2.7 active hours**, author-accepted working calibration. Historical old 1/4-inch times are not automatically 7 mm measurements.
- Cumulative prime-equivalence thresholds F = 1, 13, 143, 1001, 5005, 15015.
- 25 mm to 7 mm volume ratio = (25/7)^3 = 45.553935860058.
- Provisional equal energy-equivalent storage capacity per unit volume and identical charging throughput at both sizes.
- Total active time: T_7(F)=2.7F hours; T_25(F)=2.7F(25/7)^3 hours.
- Incremental time: ΔT_s= T_s(F_current)−T_s(F_previous).
- These are **active charging hours**, not continuous sessions, workdays, or calendar days. Fatigue and recovery are unspecified.
- The prime ladder as a fixed-chip charge threshold is itself an author-accepted working normalization, not an independently derived physical capacity law.
- White 2h42m differs from additive-rate calculation (~2h36m26s); preserve as provisional author-accepted calibration, not a mathematically deduced value.

## Charging times by target

| Target | 7 mm incremental h | 7 mm total h | 25 mm incremental h | 25 mm total h |
|---|---:|---:|---:|---:|
| Red | 2.700 | 2.700 | 122.996 | 122.996 |
| Orange | 32.400 | 35.100 | 1,475.948 | 1,598.943 |
| Yellow | 351.000 | 386.100 | 15,989.431 | 17,588.375 |
| Green | 2,316.600 | 2,702.700 | 105,530.248 | 123,118.622 |
| Blue | 10,810.800 | 13,513.500 | 492,474.490 | 615,593.112 |
| Violet | 27,027.000 | 40,540.500 | 1,231,186.224 | 1,846,779.337 |

## Mass and price authority

Checkpoint 008 contains the canonical Red–Violet masses and crystal prices for 7 mm and 25 mm. This checkpoint does not overwrite or recompute those values. The 25 mm charging calculation is an additional conditional model, not a revision of material mass.

## Open for author decision

Whether a 25 mm charged diamond has 45.5539× the 7 mm energy capacity; whether charging rate scales with interface/sigil area, operator ability or parallel channels; recovery between fatigue-limited sessions.

## Archive provenance

Complete Checkpoint 009 is embedded byte-for-byte at `ARCHIVE/MK163_CUMULATIVE_009_DIAMOND_AND_ENERGY_STRUCTURING.zip`, which itself embeds 008, 006 and 007. No repository push.