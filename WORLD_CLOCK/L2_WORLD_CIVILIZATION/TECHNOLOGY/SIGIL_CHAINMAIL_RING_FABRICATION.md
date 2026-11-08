# OR-09 — Full manufacturing model: ingot → spool → flat chainmail rings, parallel sigil stations

**Book Red · Orange · 2026-11-08.**

## Prior repository manufacturing facts (preserve)

Kaira's first major specialty contract with the unnamed master mailwright in the **large city's Yellow District Blacksmith Row** is **300,000** Genesis-infused iron, elastic, self-closing chainmail rings at **1,000 eln base**. Planning allocation: **~25,000** demo shirt, **~250,000** future five-layer physical Chainmail Robe and **~25,000** contingency. Shirt ~23–25k rings. The only selected enchantment is **mass reduction**; no intrinsic free fire/magic/impact resistance from it. The shop has a master, with colleague/journeyman capable of producing rings. Manufacturing interval selected previously: **11 local days**, batch pickups around **commission days 3, 6, 9 and 11**. First pickup ~80,000 rings illustrative, later batch sizes OPEN. The earlier planned surcharge +100 eln is **not approved**; total enchantment costs remain OPEN. A local day is **31 hours**, not the Earth 24-hour day. The 11-day schedule is established narrative canon; do not rewrite it simply because new throughput equations are not numeric.

## Source intent: physical inspiration, not traditional manual chainmail forging

The author first considered manual wire-drawing dies and mandrels assisted by a Metal Manipulation Card, then refined the approach to **two repeatable sigil workstations**. They explicitly don't want a conventional dirty coal forge, repeated manual hand-forming of 300,000 rings, or "magic" conjuring finished armor out of nowhere. The smith acts as a **conductor of matter** and the sigil's engineered geometry performs standard repetitive fabrication with ordinary skilled oversight. Raw metal comes from a material stock/ingot, which is not multiplied without accounting for mass; no universal free-energy/material supply is authorized. Historical wire-making practices inspired the concept but are not required as direct medieval machinery in MK163.

## Stage 1: ingot-to-wire spool (wire sigil)

1. **Input:** place one compatible metal ingot at the central input **anchor** on a specialized **sigil table** (not requiring a physical anvil).
2. **Configure:** journeyman selects or verifies preset wire diameter/gauge, material treatment, field geometry, thermal conditioning, intended spool geometry and appropriate operational limits according to known tooling/math. Exact interface and sigil architecture are not specified.
3. **Activate:** physical sigil activates a bounded **phase-field projection**, isolating/containing working material in the required spatial volume.
4. **Transduction:** Metal and Thermal Manipulation alter ingot material geometry, draw/elongate it into continuous calibrated wire and arrange it into a controlled **wire spool**. This bypasses much manual melting/pouring/hammering/drawing effort. Precision is encoded by constrained geometry, not ad hoc smith hand gestures at every segment.
5. **Finite interval:** the process takes **T₁**, a positive, finite operational time determined by material, geometry and apparatus parameters (numeric rate not locked).
6. **Output:** a spool of correctly dimensioned wire with the required material characteristics, transferable to the next table. The operator checks that the result is admissible/within tolerance before moving it.

Stage 1 can include heat when necessary; **Thermal Transduction is not a coal furnace**. Spooling can occur as part of the first sigil, not a third compulsory machine. An earlier assistant suggested a die for final gauge accuracy; the later user preference is a **precision-constrained phase field**. A die or mandrel can be an optional aid, not the required canonical physics or extra mandatory stage.

## Stage 2: wire spool to split/flattened ring batch (ring sigil)

1. Move a completed spool to a **different sigil table** and place it into that table's designated **anchor/containment region**.
2. Configure required wire feed, ring inner diameter, spiral pitch, closure geometry, ring profile and separation process. The exact physical UI is OPEN.
3. Activate a distinct constrained phase field. The sigil **isolates the spool and draws its wire forward**.
4. Metal Transduction winds fed wire into a **very tight helical/spiral coil** of precisely governed geometry. This is the user's preferred "wrap it into a really tight spiral" process; a physical mandrel can be present if selected but the **phase-field geometry is authoritative**.
5. Within the same station, the sigil **separates individual rings by a cutting/parting operation along the progression/top of the formed coil**, akin to cutting a wound coil along one line to generate many separate loops, rather than a smith manually shaping one loop at a time.
6. **Output:** consistently defined **flattened chainmail rings**. The author explicitly used "perfectly defined flattened rings"; **whether this describes the entire flattened wire cross-section, flattened contact surfaces, precisely flat circular loops or an additional post-form flattening step has not been defined**. Do NOT silently equate it only with split-end flattening, and don't introduce rivets, welding or full permanent fused closure. Kaira's specialty rings must still be **elastic and self-closing** for hand/Transduction-assisted weave assembly.
7. **Finite interval:** the process takes **T₂**, a finite time for a spool/batch, separate from T₁. Exact seconds/minutes/local hours and ring yield per spool remain OPEN.
8. Completed pieces are inspected for count, consistent diameter, gauge, elasticity, cut quality, shape recovery and relevant material integrity. Some additional finishing/sorting/packaging can be manual or assisted; no guaranteed zero-defect production.

## Shop operation: journeyman, not one-by-one master work

The author expressly selects a **qualified journeyman blacksmith** (voice transcription "journeysmith" in some passages) to operate **the complete sigil process**. They load ingots and wire spools, select established process specifications, activate sigils, observe Transduction intervals and outputs, transfer spools and validate results. **Automation is the sigil's engineered repeatable geometric operation, not a human doing several manual metal manipulations simultaneously.** The master mailwright can design/approve the unusual ring specs, manage customer commitments, conduct advanced work and inspect exceptional batches, while journeymen perform dependable production. Apprentices/juniors can prepare/handle/sort supplies and learn manual smithing, but do not assume they autonomously execute restricted high-grade operations absent training.

## Parallel station scheduling — computer render-farm analogy

The author compares parallel stations to rendering many visual frames across a server farm: one lengthy sigil process can be multiplied in effective throughput by **multiple independent working stations**. A specific working example is **three separate ingot-to-spool sigil tables**, which a journeyman can **activate sequentially** and leave working **concurrently**:

- Load/activate spool Sigil A; it begins its autonomous Transduction interval.
- While A is operating, load/activate Sigil B on a second ingot.
- While A and B operate, load/activate Sigil C.
- Monitor the concurrently running states, remove each completed spool, replenish inputs and send output to the second-stage ring sigils.

There may be **one or more second-stage ring-forming tables**. No exact number of second-stage ring sigils is author-locked; the source earlier proposed at least one. Parallelizing Stage 1 alone won't guarantee finished-ring throughput increases if Stage 2 is the bottleneck. Journeyman attention, safe simultaneous setup, energy/fatigue budget, storage buffer, material availability, processing time and inspection capacity constrain sustainable operation. The user's example permits three stations running while a qualified operator supervises; do **NOT** force three separate journeymen, nor assume unlimited independent sigil operation for free.

## Capacity arithmetic and interval definitions

Let each Stage 1 cycle process one ingot into one spool of material sufficient for **R** rings at Stage 2 after waste, with required effective Stage-1 processing duration **T₁** and Stage-2 process **T₂** per spool, and finite loading/handling/inspection time **H**. For **N₁** active Stage 1 stations and **N₂** active Stage 2 stations over effective working time **W** per local day, an ideal upper-bound approximation is

```
Stage 1 spool capacity/day ≤ N₁ × W / T₁
Stage 2 spool capacity/day ≤ N₂ × W / T₂
Finished ring capacity/day ≤ R × min(Stage 1 spool capacity, Stage 2 spool capacity)
```

This ignores startup stagger, operator setup and monitoring, resource limits, defects and other overhead, so it is **illustrative only**. For a one-operator sequential setup with no overlap, per spool total is approximately `T₁ + T₂ + handling`. For multiple stations continuously operating, the slowest effective stage limits the sustained rate, subject to scheduling.

Kaira's known commission target is `300,000 / 11 = 27,272.727...` completed rings per local 31-hour day on average, including work and inspection. Three Stage-1 tables are a user-proposed working example; **do not back-solve and canonize false exact minute intervals or spools/day without selecting R, T₁, T₂, N₂ and working/attended hours**. The first ~80k ring pickup around day 3 is consistent with steady output at this aggregate rate but does not lock daily batches or a 24-hour work cycle. No universal "every blacksmith can do 27k/day" rule.

## Relation to source mathematics and materials

The two stations are **sigil-based constrained local Genesis-field Transduction**. They are not an invention of a new Genesis Field operator, a literal new fundamental topology stage or physical real-world manufacturing breakthrough. Normal engineering must obey admissible material identity, geometry, available resources, field capabilities, finite biological/operator control and system limits. The mechanical details of mass reduction enchantment, elastic self-closing material preparation, molten vs solid forming and ring profile finishing are **not derived** in this workshop. The phrase "alter the topology of the metal" is the user's engineering description of geometric shaping; do not claim topological invariants are literally changed by a specified mathematical operator without source support.

## Why this matters narratively

The 11-day schedule is feasible in a specialized established mailwright shop with multiple sigil tables, qualified journeyman operation and high-volume geometry processing, while the master continues personally meaningful work and Kaira receives staged ring batches. This supports the Age of Knowledge's theme: engineering precise sigils enables reproducible, scalable craftsmanship, not nonspecific "magic makes things". Kaira's demonstration shirt remains made by **her own labor** in ~8 elapsed days, after receiving first rings; sigils in supplier's workshop produce **rings**, not the complete woven shirt or five-layer Chainmail Robe automatically.

Sources: [OR-09 full workshop record](../../../PROVENANCE/WORKSHOP/ORANGE_ARC_2026_11_08/DECISIONS/09_SIGIL_CHAINMAIL_INGOT_SPOOL_RING_PARALLEL_TRANSDUCTION.md) · [selected author evidence](../../../PROVENANCE/WORKSHOP/ORANGE_ARC_2026_11_08/PROVENANCE/13_AUTHOR_EVIDENCE_SELECTED_VERBATIM.md) · [corrections and open questions](../../../PROVENANCE/ORANGE_2026_11_08_CORRECTIONS.md).
