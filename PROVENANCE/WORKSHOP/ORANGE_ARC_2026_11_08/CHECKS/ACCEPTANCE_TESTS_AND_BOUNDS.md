# Codex acceptance tests: required constraints, positive assertions, disallowed leakage

This is a **substantive test contract** to run against the integration, not a replacement for full topic files or existing constitutional validators.

## Hard narrative tests

1. `BOOKS/RED/ARCS/ARC_002/ARC.md` still includes Oct 22 inherited handoff: Kaira demo **shirt** in backpack, lunch/fruit, five-mile staging trip, no completed robe, no Ring. New visits append afterward.
2. Latest **seven Book Red arcs** remain Red→Orange→Yellow→Green→Blue→Violet→White; don't rewrite other arcs from this Orange material.
3. `NYX` first joins Orange via the **third dungeon-related return**, not the first moss/stone/frog return; Black Sprite bond first in Yellow.
4. The **southwest** zone is craftsmen/markets and **southeast** is inns/restaurants/commercial shops (including the adjacent abecca and raeon shops). Northwest vs northeast residences and north-offset dungeon entrance preserved. No fabricated scale-accurate master map.
5. The staging settlement is roughly **2 × 2 mi**; main city **10 × 10 mi**; separation **~5 miles**, not 7, plus actual intra-city travel.
6. Staging pricing **1.3–1.7 ×** comparable city baseline **1.0** for normal relevant services, including inns, shops, repairs and residences. Kaira's intended subcontract repair rate **0.9 × city equivalent after inspection**, NOT 0.9%. Preserve `50/110/180/200 eln` standard retail figures and no fixed repair tariff.
7. First two smithies reject her for no suitable chainmail work; **third interested**, later **one more willing**, two promising connections, no fixed names or guaranteed completed repair invoices.
8. Accord Registry is Crown body; supports service postings/socializing and refers to **independent freight**; not itself a vaelum/freight carrier. Kaira does not gain aithren professional certification in Orange.
9. Kaira meets **Vael**, the noble son, beside **raeon** shop as he exits with **two friends** and **drops two undamaged cards**; he prejudicially treats her as untreated Afflicted despite visible Awakening. She gets angry, extricates herself, recovers while browsing, buys no cards because of higher prices. Exact dialogue still OPEN. The old Village Hub/armorsmith shop first-meeting variants are superseded.
10. Her first detour **15–20 minutes** along an animal trail leads to Genesis-expressive **frog (not vaen)**, Genesis-expressive **moss** and little green translucent **mineral-stone vaen (not Genesis crystals)**. Moss and minerals share/shape a supporting local field environment. No repeat Red mushroom, no unproven alchemical identity, no early Nyx. Collects enough to fill backpack, mentally marks location and returns home.
11. The two-stage ring production is **ingot→wire spool→spiral coil→separated individual flattened rings**, physical **sigil phase-field Metal/Thermal Transduction** rather than magical conjuration. The jouneyman **operates entire process**, with **three simultaneous Stage 1 spool machines** as concrete working example, Stage 2 number OPEN.
12. **T₁** and **T₂** finite but numeric OPEN; count **300,000**, day pickups **3,6,9,11**, 11 days, earlier shirt eight elapsed days and first batch ~80k preserved. Actual product geometry and "flattened" exact meaning still OPEN.
13. Smithy architecture one/two/three bays, depth 30–40 ft; approved two-tier example **40 ft ground, upper 20 ft enclosed+20 ft promenade**, **NO overhang**. Sophisticated stone & matter-conductor operations, less greenery/water than civic center, no digital computer panels or medieval coal/soot environment.
14. Controlled **maege lights**, water-generation/dissolution, fireplaces from Genesis **Transduction** without smoke/soot/ash, maintained stone street, growth-supporting velis. Do not invent free matter, literal electronics or automatic cleaning.
15. **Green/fourth** at White Arc Book Red championship and ring only at the end of Book Red remain authoritative; no rejected Yellow outcome revival.
16. Four earlier Accord Registry role examination owners, Kaira's **54/91 Green**, and Nov 7 workshop source data remain intact. Do not accidentally reinsert superseded 52-score or earlier Guardian time rank.
17. Do not silently change AERA, MK147, MK727, _raeon, Genesis mathematical physics/API, or install an unrelated widget/technology. This package targets **MK163 only**.
18. Validate protected active spelling `Kaira`, `Nyx`, `raeon`, `abecca`, `vaen`, `maege`, `maegi`, `aithren`, `vaelum`, `ru’ne`, `ELDRIS` while allowing older dictated spellings **inside explicitly attributed historical source quotations**.

## Archive and source tests

- ZIP structure: root `MK163_ORANGE_2026_11_08/`, with `README_START_HERE.md`, `executable.md`, `MANIFEST.json`, `DECISIONS`, `PROVENANCE`, `CHECKS`, `VISUAL_EVIDENCE`, `SOURCE_ARCHIVES`.
- Run `CHECKS/verify_manifest.py` against extracted payload; all sha256/bytes must match, no duplicate member paths or case-insensitive collisions.
- Run `ZipFile.testzip()`/CRC on the outer archive **and** nested original previous checkpoint ZIPs. Verify exact unchanged Nov 7 source SHA `771e2ab681dbdddc762e935b7d3c7230c08b6c0184e1d9f641605c060d539f62`.
- Validate physical media original hashes; preserve approved image vs rejected artwork statuses rather than replacing good references with lower-resolution thumbnails.
- `git diff --check` and existing `CHECKPOINTS/TOOLS/validate_book_red_20261107.py` only if it can legitimately run on current checkpoint/delivery; do not misreport old version-specific guards as current failures. Run scoped new tests against current owner records, and no deletion of earlier bytes.
- Do not automatically track source `.zip`, PDF, or generated images unless approved by repository policy/author selection. Preserve every new unique substantive textual detail and provenance entry even if media is not committed.
- After integrating, report source hashes, exact changed paths, unresolved parameters, validation results and remote commit URL/SHA after verified push. If push fails, report failure; do not pretend success.
