# Healthcare Test — Accord Registry Helkir Certification

**Project:** MK163 / AERA-derived world implementation  
**Status:** Author-approved and locked for MK163 workshop canon  
**Classification:** Helkir (healing specialist) examination  
**Stations:** 13 consecutive trials — 4 sustainment and 9 restoration  
**Institution:** Crown-owned Accord Registry

## Examination apparatus

Each station has a physically inscribed sigil projecting a controlled biological training manifold and a connected outer chromatic assessment ring. No actual injured patients or preserved corpses are required. The instructor initiates each station. A trained Helkir uses Coherence to sustain or restore the manifold's biological topology. The projected field is an examination apparatus, not a newly invented Binding in the 1,245-record MK157 corpus.

## The thirteen tests

| Station | Test | Mode | Assessed competency |
|---|---|---|---|
| 01 | Localized Coherence Sustainment | Timed Decoherence | Sustain one biological structure against continuous Decoherence. |
| 02 | Distributed Coherence Sustainment | Timed Decoherence | Maintain coherence across several connected biological structures. |
| 03 | Progressive Decoherence Pressure | Timed Decoherence | Sustain a biological manifold as imposed Decoherence becomes progressively stronger. |
| 04 | Complex System Sustainment | Timed Decoherence | Maintain a complete interconnected biological manifold under sustained Decoherence. |
| 05 | Superficial Tissue Restoration | Restoration | Reconstruct localized damage to skin and superficial tissues. |
| 06 | Muscular Restoration | Restoration | Restore damaged muscle structure and its functional connections. |
| 07 | Skeletal Restoration | Restoration | Reconstruct fractured or displaced skeletal topology. |
| 08 | Vascular Restoration | Restoration | Restore damaged blood vessels and their structural continuity. |
| 09 | Neural Restoration | Restoration | Reconstruct delicate damaged neural structures and connections. |
| 10 | Organ Restoration | Restoration | Restore complex internal organ topology. |
| 11 | Multiple Trauma Restoration | Restoration | Repair three separately damaged regions within one projected biological manifold. |
| 12 | Critical Localized Trauma | Restoration | Restore a severely compromised structure representing a life-threatening injury. |
| 13 | Integrated Biological Restoration | Restoration | Reconstruct damage across multiple interdependent biological systems. |

## Sustainment rules — stations 01–04

- Each station begins with a fully coherent projected manifold; its assessment ring is White.
- At the instructor's signal, controlled Decoherence is applied for a predetermined interval (30 seconds was an illustrative duration, not a universal locked value).
- The candidate applies Coherence to sustain the manifold throughout the interval.
- At interval completion, the manifold deactivates and the **ring color at the end of the interval** is recorded. Do **not** substitute the lowest historical color as the recorded score.
- Deterioration follows White → Violet → Blue → Green → Yellow → Orange → Red → unlit/Failed.

## Restoration rules — stations 05–13

- Each station begins with a damaged projected biological manifold and an unlit ring.
- The candidate progressively restores biological topology by applying Coherence.
- As the structure is repaired, the ring ascends unlit/Failed → Red → Orange → Yellow → Green → Blue → Violet → White.
- The candidate can conclude when the best achievable or strategically desired level is reached. The **highest coherence attained** is the recorded score; it does not decay during the restoration attempt.
- For Multiple Trauma Restoration, three damaged regions contribute to the overall result. Full restoration of only one region does not automatically earn White.
- Exact mapping from manifold reconstruction to ring thresholds is an apparatus calibration matter, not yet numerically defined.

## Consecutive examination, fatigue, and certification

- All thirteen stations are completed consecutively. Physiological Genesis fatigue and reduced basin access carry forward; no reset between stations.
- Candidates can deliberately stop restoration at a lower score to conserve endurance for later stations.
- A candidate who cannot continue through all thirteen stations **receives no overall certification rating**, even if earlier scores were high.
- A completed examination with low scores can still fail. This is distinct from incomplete examination.
- Every station outcome: Failed/unlit = 0, Red = 1, Orange = 2, Yellow = 3, Green = 4, Blue = 5, Violet = 6, White = 7.
- For a completed examination, `overall_score = floor(sum(station_scores) / 13)`. If the result is 0, overall Failed; 1–6 are Red–Violet; 7 is White.
- White overall is possible only with thirteen White station scores. **Paragon** is the current working title for an all-White result, not yet a final in-world designation.

## Scope, provenance, and open matters

This test specification is the user's selected **13-station Helkir assessment**, not a declaration of thirteen additional spell/Binding identities. MK157 foundational Coherence Bindings include Directed Coherence, Persistent Coherence and Coherence Field; the examination is compatible with the framework but does not mandate a single Binding per station. MK163 author decisions govern this local examination implementation.

Still open: exact intervals per sustainment station, apparatus threshold calibration, permissible breaks, retry policy, candidate safety safeguards, examiner qualification, formal institutional room numbering, exact healing limits, and whether companion attribution is permitted in Helkir-specific tests. These must not be silently invented.

Protected spelling: `helkir`, `aithren`, `vaelum`, `vaen`, `ru’ne`, `maege-glass`, Kaira, Nyx.
