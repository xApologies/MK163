# MK163 — Chromatic realm arc update (2026-11-23)

## Purpose
Apply author-selected realm events at **the actual existing entry arcs** across Books Red–Violet, preserving existing book macros, arc contracts, chronology, and earlier source provenance. Book White is **not modified**. Book Red has no selected chromatic realm entry in its current outline; the first such visit is Book Orange's Red Arc. Color names of **books**, **arcs**, **political domains** and **chromatic realms** are distinct.

## Source-verified insertion map

| Book | Arc | Chromatic realm | New author-selected event |
|---|---|---|---|
| Orange | Red | Green / Sprites | Already-bonded Black Sprite returns with Kaira and illi for community homecoming; no separation |
| Orange | Yellow | Orange / Vaelith | Symbiotic living city's **energetic** nexus healed after Black Vaelith bond, a condition of bond |
| Yellow | Yellow | Red / Dragons | Kaira ends old Chirality-specialist faction war by defeating/killing leader; Black Dragon egg bond retained |
| Green | Green | Violet / Unicorns | **NEW visit to Violet Realm**, Genesis Sanctuary trial before fourth Black Unicorn bond |
| Blue | Red | Violet / Unicorns | Existing **second** visit to Violet with the already-bonded Unicorn; not another bond |
| Blue | Yellow | Yellow / Primordials | Stabilize multiple natural velis to bring high-neon realm into safer conditions and reduce ELDRIS; fifth bond retained |
| Violet | Orange | Blue / Leviathans | Heal ELDRIS-corrupted Paragon using Black Sprite and Black Vaelith; obtain Black Leviathan egg; hatching and juvenile growth retained |

**Important chronology correction:** Existing Book Green Green Arc currently says the Black Unicorn is bonded at the White palace without traveling to Violet. The user's latest explicit decision places the Genesis Sanctuary trial and bond **in Violet Realm during Book Green**. The update explicitly supersedes that old bond location and records Book Blue Red as the later return visit. Existing palace-delegation material is historical unless separately reconciled; do not claim both first-bond locations are true.

**Other continuity correction:** Book Yellow Green Arc historically describes six *Dragon-native* domains. New author decision: every Dragon can access Elemental Transduction, Dimensional Transduction/Geometry (CSR flight) and Chirality; individuals specialize differently. Genesis Field Topology belongs to Unicorns, Resonance to Primordials and Genesis Expression to Leviathans. Preserve universal Transduction operations; advanced Blackstone three-semester milestone remains, revised course detail OPEN.

## Usage in Codex

1. Unzip this archive in a **staging folder**, not directly over the repository.
2. Ensure a clean and current local clone of `xApologies/MK163`, then run:

   ```bash
   python3 apply_update.py --repo /path/to/MK163 --check
   python3 apply_update.py --repo /path/to/MK163
   git -C /path/to/MK163 diff --check
   git -C /path/to/MK163 diff
   ```
3. Review the changed book macro sections and corresponding arc contracts. Preserve earlier provenance; the added author notes take precedence only in the stated scopes.
4. Verify no changes in `BOOKS/WHITE`, and no unrelated changes; commit and push only after review.
5. Report the resulting commit SHA and any discrepancies. **Never force-push.**

## Boundaries
- Does not invent trial stages, exact velis stabilization mechanics, travel dates, Paragon name/sex, Dragon faction motives, or new bonding rules.
- Does not overwrite entire source files or erase prior author decisions. It inserts idempotent, scoped annotations at existing headings.
- Does not alter AERA, which is a separate repository.
- No repository write is claimed by this ZIP.
